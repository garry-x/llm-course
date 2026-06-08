# Chapter 7 Assignment: Training Loop

本作业对应第 7 章训练循环。目标是把 next-token 数据切片、数据重复/泄漏诊断、训练 token budget 估算、稳定交叉熵、logits 梯度、label smoothing、校准指标、global grad norm clipping、gradient accumulation step accounting、AdamW、warmup+cosine 调度轨迹和一个可复现的小训练循环串起来。

## Files

- `starter.py`: 学生起始代码。
- `reference_solution.py`: 参考实现。
- `tests.py`: 可运行测试。

## Run

```bash
.venv/bin/python assignments/ch07_training/tests.py
```

默认测试 `reference_solution.py`。测试学生代码时：

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch07_training/tests.py
```

## Requirements

- `TextDataset[i]` 必须返回等长的 `x` 和 `y`，其中 `y` 是 `x` 右移一位的 next-token target。
- `ngram_repetition_rate` 和 `ngram_overlap_rate` 必须能发现训练语料重复和 train/eval n-gram 重叠。
- `global_batch_tokens`、`training_steps_for_token_budget` 和 `dense_lm_training_flops` 必须能把 batch 设置、token 预算和 dense LM 近似训练 FLOPs 连起来。
- `optimizer_state_memory_bytes` 必须区分参数、梯度、AdamW moments，并能粗估 ZeRO-style optimizer state sharding 后的单卡显存。
- `cross_entropy_manual` 必须使用 log-sum-exp trick，并与 `torch.nn.functional.cross_entropy` 匹配。
- `cross_entropy_logits_gradient` 必须返回 mean CE 对 logits 的梯度，并支持被 `ignore_index` 屏蔽的位置不贡献梯度。
- `label_smoothed_cross_entropy` 必须把 hard target 分布改成平滑分布，并让 `ignore_index` 位置不进入平均。
- `expected_calibration_error` 必须按置信度分桶，比较每个桶内 accuracy 与 mean confidence，并支持 `ignore_index`。
- `clip_grad_norm` 必须按所有参数梯度的全局 L2 范数统一缩放梯度，不能逐参数单独裁剪。
- `gradient_accumulation_step_accounting` 必须区分 micro-batch backward loss、optimizer step、scheduler step 和 consumed tokens。
- `AdamW` 必须实现一阶/二阶动量、偏置修正和解耦权重衰减。
- 调度器必须先 warmup 到 1，再 cosine decay 到 `min_lr_ratio`；`lr_schedule_trace` 必须能按 optimizer step 返回 lr multiplier、实际 lr 和累计 consumed tokens。
- `train` 必须执行 `zero_grad -> forward -> loss -> backward -> clip -> step -> scheduler.step`，并记录 loss history。

## Conceptual Handout

本作业的目标不是只写出一个能下降的 toy loss，而是建立训练工程师需要的完整 mental model：数据如何变成 token batch，loss 如何把梯度传回 logits 和 embedding，optimizer/scheduler 如何改变参数，训练日志如何支持诊断，显存和 FLOPs 如何约束实验规模。

### 1. 数据切片、重复与泄漏

Next-token dataset 的每个样本都应满足：

```text
x = token_ids[i : i + block_size]
y = token_ids[i + 1 : i + block_size + 1]
```

这意味着 `logits[:, t, :]` 预测 `y[:, t]`，也就是原序列里的下一个 token。常见错误是把 `x` 和 `y` 设成同一段，导致模型学习复制当前 token；或者在最后一个 token 没有 target 时仍然进入 loss。

训练数据诊断至少要看两类问题：

- 重复：`ngram_repetition_rate` 高，说明同一片段被过度重复，训练 loss 可能快速下降但泛化变差。
- 泄漏：`ngram_overlap_rate(train, eval)` 高，说明开发集可能已经出现在训练集中，val loss/PPL 会被高估为“模型变好”。

报告数据时不要只写样本数；应写 token 数、block size、train/val 切分方法、重复率、overlap rate 和异常样本处理。

### 2. Cross Entropy、梯度与校准

自回归语言模型最大化：

```text
log p(x_1, ..., x_T) = sum_t log p(x_t | x_<t)
```

训练时通常最小化 mean cross entropy。稳定实现必须使用 log-sum-exp trick：

```text
CE(z, y) = log(sum_j exp(z_j)) - z_y
```

对 logits 的梯度是：

```text
d CE / d z_j = p_j - 1[j = y]
```

若 loss 是 mean over valid tokens，梯度还要除以有效 token 数；`ignore_index` 位置的梯度必须是 0。这个细节影响 padding、SFT label mask 和 packed sequence 训练。

Perplexity 是 `exp(mean_ce)`，适合描述 next-token 预测难度，但不直接等价于 helpfulness、事实性或安全性。`expected_calibration_error` 则检查模型置信度是否与正确率一致。一个模型可以 PPL 更低但过度自信，这会影响拒答阈值、reranking 分数和上线风险控制。

### 3. Gradient Accumulation 与全局 batch tokens

训练规模通常按 token 计算，而不是按 step 粗略描述：

```text
global_batch_tokens = micro_batch_size * seq_len * grad_accum_steps * data_parallel_size
num_optimizer_steps = ceil(token_budget / global_batch_tokens)
```

Gradient accumulation 的关键是：每个 micro-batch backward 的 loss 要除以 `grad_accum_steps`，但 optimizer step 和 scheduler step 只在 accumulation group 结束时执行一次。常见错误包括：

- 每个 micro-batch 都 scheduler step，导致 warmup/decay 过快。
- 忘记 loss scaling，导致有效学习率放大。
- 只报告 micro-batch size，不报告 global batch tokens。
- consumed tokens 按样本数记，而不是按 token 数记。

训练报告必须写清 micro-batch、sequence length、accumulation、data parallel size、global batch tokens 和 optimizer steps。

### 4. AdamW、Warmup/Cosine 与梯度裁剪

AdamW 与 L2 regularization 的关键差别是 decoupled weight decay：权重衰减直接作用在参数上，而不是混入梯度再进入 Adam moments。作业中的 `AdamW` 要实现一阶/二阶动量、bias correction 和 decoupled decay；写报告时应说明 `beta1/beta2/eps/weight_decay` 的选择。

Warmup+cosine scheduler 的边界要清楚：

- warmup 阶段 lr multiplier 从 0 逐步到 1。
- decay 阶段从 1 下降到 `min_lr_ratio`。
- scheduler step 计数应等于 optimizer step，而不是 micro-batch backward 次数。

Global grad norm clipping 应把所有参数梯度看作一个大向量统一缩放。逐参数裁剪会改变方向，不等价于全局 L2 clipping。诊断时：

- `grad_norm` 长期很大且 loss spike，优先检查 lr、loss scaling、数据异常和 clipping 阈值。
- `grad_norm` 长期接近 0，优先检查 mask、冻结参数、学习率过低或梯度断开。
- 出现 NaN，先检查 logits/softmax 稳定性、mixed precision、除零和异常样本。

### 5. 显存、FLOPs 与分布式训练

Dense LM 训练 FLOPs 的常用粗估是：

```text
training_flops ~= 6 * num_params * train_tokens
```

这只是主项估算，不包含数据加载、通信、kernel inefficiency、activation checkpointing 重算和 MoE routing 开销。训练显存也不能只数参数：

- parameter memory：模型权重。
- gradient memory：每个可训练参数的梯度。
- optimizer state：AdamW 通常有两个 fp32 moments。
- activation memory：与 batch、sequence length、层数和 checkpointing 策略相关。
- temporary buffers：attention、通信和 framework 分配。

ZeRO/FSDP 通过切分 optimizer states、gradients 或 parameters 降低单卡显存；TP/PP 通过切分矩阵或层降低模型放置压力，但引入通信和 pipeline bubble。报告分布式策略时至少写：

- 哪些状态被 sharded，per-rank memory 如何变化。
- global batch tokens 是否因为 data parallel size 改变。
- tokens/s/GPU、MFU 估计和通信瓶颈。
- checkpoint 保存的是完整权重、分片权重，还是需要额外 consolidation。

### 6. 训练日志与结论写法

一个合格训练实验不能只交最终 loss。最终报告至少包含：

- research question、baseline、数据和 token budget。
- 模型配置、参数量、global batch tokens、optimizer/scheduler。
- train loss、val loss/PPL、ECE、grad_norm、lr、tokens/s 曲线。
- checkpoint/resume 行为和失败 run 处理。
- ablation：至少比较一个变量，例如 lr、batch tokens、label smoothing、数据清洗或 LoRA rank。
- 结论边界：当前数据、模型规模、训练 token、随机种子和预算下能推出什么，不能推出什么。

如果训练 loss 下降而 val loss 上升，优先怀疑过拟合、数据泄漏排查不充分、训练/验证分布不一致或正则不足。如果 tokens/s 下降，优先看 sequence length 分布、dataloader、GPU 利用率、activation checkpointing、通信和日志/保存频率。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 推导交叉熵、CE 对 logits 的梯度、label smoothing、perplexity、ECE/calibration、global grad norm clipping、gradient accumulation loss scaling、global batch tokens、训练步数、dense LM 训练 FLOPs、optimizer state 显存、AdamW 偏置修正、warmup+cosine 边界与 token 进度、n-gram 泄漏诊断和 grad clipping 的诊断意义 |
| Programming parts | 55 | 实现 dataset/dataloader、n-gram 重复/重叠率、训练预算计算、optimizer state 显存估算、稳定 cross entropy、CE logits 梯度、label-smoothed CE、ECE/calibration bins、global grad norm clipping、gradient accumulation step accounting、AdamW、scheduler、lr schedule trace 和训练循环 |
| Analysis / style | 10 | 解释梯度如何回到 LM head/embedding，并用训练日志解释 loss spike、NaN、grad_norm、校准偏差、数据重复、train/val 分叉、tokens/s 和 resume 行为 |
