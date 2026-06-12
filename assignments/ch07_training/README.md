# Chapter 7 Assignment: Training Loop

本作业对应第 7 章训练循环。目标是把 next-token 数据切片、数据重复/泄漏诊断、训练数据策展 gate、训练 token budget 估算、稳定交叉熵、logits 梯度、label smoothing、校准指标、global grad norm clipping、gradient accumulation step accounting、AdamW、warmup+cosine 调度轨迹、分布式训练策略账本、checkpoint/resume 完整性 gate、训练异常 runbook 和一个可复现的小训练循环串起来。

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
- `training_data_curation_report` 必须把训练前数据源清单汇总成 size、dedup、quality filter、eval contamination、domain mixture 和 privacy gate，报告 weighted duplicate/quality/PII、domain token share、action items 和是否可以进入 training rehearsal。
- `global_batch_tokens`、`training_steps_for_token_budget` 和 `dense_lm_training_flops` 必须能把 batch 设置、token 预算和 dense LM 近似训练 FLOPs 连起来。
- `optimizer_state_memory_bytes` 必须区分参数、梯度、AdamW moments，并能粗估 ZeRO-style optimizer state sharding 后的单卡显存。
- `distributed_training_strategy_report` 必须比较 DDP、ZeRO/FSDP 类策略的每卡参数/梯度/optimizer state、global batch tokens、通信模式、显存 gate 和可选 MFU gate，说明是否可以进入 scale rehearsal。
- `checkpoint_resume_integrity_report` 必须检查 checkpoint 是否包含 model、optimizer、scheduler、global_step、RNG、sampler/data cursor、低精度 scaler/scale history 等训练状态，区分 resume checkpoint 与 model-only export，并检查 atomic write、step 单调性、分布式/sharded/DCP 格式的 reshard 能力、保存间隔和 checkpoint overhead/async save。
- `cross_entropy_manual` 必须使用 log-sum-exp trick，并与 `torch.nn.functional.cross_entropy` 匹配。
- `cross_entropy_logits_gradient` 必须返回 mean CE 对 logits 的梯度，并支持被 `ignore_index` 屏蔽的位置不贡献梯度。
- `label_smoothed_cross_entropy` 必须把 hard target 分布改成平滑分布，并让 `ignore_index` 位置不进入平均。
- `expected_calibration_error` 必须按置信度分桶，比较每个桶内 accuracy 与 mean confidence，并支持 `ignore_index`。
- `clip_grad_norm` 必须按所有参数梯度的全局 L2 范数统一缩放梯度，不能逐参数单独裁剪。
- `gradient_accumulation_step_accounting` 必须区分 micro-batch backward loss、optimizer step、scheduler step 和 consumed tokens。
- `AdamW` 必须实现一阶/二阶动量、偏置修正和解耦权重衰减。
- 调度器必须先 warmup 到 1，再 cosine decay 到 `min_lr_ratio`；`lr_schedule_trace` 必须能按 optimizer step 返回 lr multiplier、实际 lr 和累计 consumed tokens。
- `train` 必须执行 `zero_grad -> forward -> loss -> backward -> clip -> step -> scheduler.step`，并记录 loss history。
- 训练异常分析题必须能把 loss spike、NaN/Inf、resume 不连续和 tokens/s 下降分别归因到数据、数值精度、优化器状态、checkpoint 完整性或系统吞吐瓶颈。
- `training_system_gate_report` 必须把训练 run 拆成 optimization、throughput、state/checkpoint 和 evaluation gate，输出 `overall_pass`、每个 gate 的信号和需要 debug 的 action items。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 推导交叉熵、CE 对 logits 的梯度、label smoothing、perplexity、ECE/calibration、global grad norm clipping、gradient accumulation loss scaling、global batch tokens、训练步数、dense LM 训练 FLOPs、optimizer state 显存、DDP/ZeRO/FSDP 分片差异、MFU、checkpoint resume state、DCP/sharded checkpoint 与 preemption loss、AdamW 偏置修正、warmup+cosine 边界与 token 进度、n-gram 泄漏诊断、data curation gate、grad clipping 的诊断意义、异常 runbook 和训练 gate 判定 |
| Programming parts | 55 | 实现 dataset/dataloader、n-gram 重复/重叠率、`training_data_curation_report`、训练预算计算、optimizer state 显存估算、`distributed_training_strategy_report`、`checkpoint_resume_integrity_report`、稳定 cross entropy、CE logits 梯度、label-smoothed CE、ECE/calibration bins、global grad norm clipping、gradient accumulation step accounting、AdamW、scheduler、lr schedule trace、训练循环和 `training_system_gate_report` |
| Analysis / style | 10 | 解释梯度如何回到 LM head/embedding，并用训练日志解释 loss spike、NaN、grad_norm、校准偏差、数据重复、train/val 分叉、数据质量/污染 gate、tokens/s、MFU、atomic checkpoint write、resharding、checkpoint overhead、resume parity、评测 gate 和最小修复实验 |
