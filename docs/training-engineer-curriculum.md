# LLM 训练工程师能力视图与学习成果

这份文档把课程中的模型实现、训练循环、微调对齐、实验设计和大规模训练优化整理成“LLM 训练工程师”能力视图。它用于检查章节产出是否覆盖岗位能力，不是独立补课路径；训练工程师的核心产出不是一个 notebook，而是一套可复现、可恢复、可观测、成本可解释的训练系统。

## 目标画像

完成课程后，你应该能独立设计和维护一个小型 LLM 训练任务：准备数据、配置训练、监控 loss/throughput/grad norm、保存完整 checkpoint、从中断恢复、做开发集评估，提出 baseline/ablation，并能解释显存、吞吐、分布式策略、MFU、GPU 小时、checkpoint overhead 和训练成本之间的关系。

## 章节能力映射

| 阶段 | 章节与项目 | 主要问题 | 学习产出 |
|------|------------|----------|----------|
| 1. 模型可训练性 | Ch01-Ch07 | 数据如何变成 logits，梯度如何穿过模型 | 能解释 token、shape、参数量、梯度路径和数据策展 gate |
| 2. 单机训练循环 | Ch07 | 如何让 loss 稳定下降 | DataLoader、loss、optimizer、scheduler、AMP、checkpoint/resume gate |
| 3. 微调与对齐 | Ch09 | 如何把预训练模型变成可用助手 | SFT/偏好数据 gate、LoRA/DPO/GRPO/DAPO/GSPO 训练数据、loss masking、偏好优化与 reasoning RL 日志 |
| 4. 实验设计与评估 | Ch08-Ch09、Capstone | 如何证明训练或对齐方法真的更好 | research question、baseline、ablation、对齐评估和结论边界 |
| 5. 大规模训练效率 | Ch07、Ch10 | 如何解决显存、通信、吞吐、精度和成本问题 | ZeRO/FSDP2/TP/PP、FP8/MXFP8、MFU、tokens/s 解释 |
| 6. 工程实践 | Training Capstone | 如何证明训练任务可复现、可恢复、可观测 | acceptance 输出、metrics.jsonl、checkpoint integrity、训练规划与 strategy report |

## 能力目标

### A. 数据与 Token 预算

- 能区分 raw text、tokenized dataset、packed sequence、train/val split。
- 能计算 token budget、batch size、sequence length、gradient accumulation 对总 step 的影响。
- 能发现空样本、重复样本、过长样本、编码异常和数据泄漏风险。
- 能报告 n-gram repetition 和 train/eval overlap，避免把数据泄漏误判为泛化能力提升。
- 能用 size、dedup、quality filter、eval contamination、domain mixture 和 privacy gate 判断数据是否可以进入训练 rehearsal。

**对应内容：**Ch01、Ch07 7.3-7.3B，Training Capstone `data_profile.py` 与 data curation gate 表。

### B. 训练循环与优化

- 能实现 forward、loss、backward、gradient clipping、optimizer step、scheduler step。
- 能解释 AdamW、warmup+cosine、weight decay、grad norm、loss scale。
- 能判断 loss spike、nan、梯度爆炸、学习率过高、batch 太小等常见问题。
- 能区分 micro-batch loss、accumulated backward loss、optimizer step、scheduler step 和 consumed tokens。

**对应内容：**Ch07 7.1-7.12，Training Capstone `train.py`。

### C. Checkpoint 与可恢复性

- 能保存 model/optimizer/scheduler/global_step/random seed/config、sampler/data cursor 和低精度 scaler/scale history。
- 能从 checkpoint resume，并保证 step、lr、best metric 和日志连续。
- 能区分 latest、best、periodic checkpoint 和 model-only export；知道 export 权重不能替代可恢复训练状态。
- 能检查 atomic write、latest pointer、checkpoint interval、checkpoint overhead 和 async/overlap 保存策略。
- 能说明 FSDP/ZeRO 下 checkpoint 还需要 shard metadata、sharded/DCP 类格式和 load-time reshard 能力。

**对应内容：**Ch07，`checkpoint_resume_integrity_report`，Training Capstone `train.py` 与 `acceptance.py`。

### D. 监控与实验管理

- 能记录 train_loss、val_loss、perplexity、calibration/ECE、lr、grad_norm、tokens/s、samples/s。
- 能用 JSONL/CSV/W&B/TensorBoard 记录实验，并保留 config。
- 能用固定开发集判断训练是否真的改进，而不是只看训练 loss。

**对应内容：**Ch07，Ch09，Training Capstone `metrics.jsonl`。

### E. 分布式与低精度训练

- 能解释 DP、DDP、FSDP2/ZeRO、TP、PP、gradient accumulation 的适用场景。
- 能解释 BF16/FP16/FP8/MXFP8/FP4 的收益、风险和常见数值问题。
- 能用 MFU、tokens/s/GPU、通信开销判断集群训练效率。
- 能估算 parameters、gradients、AdamW moments、activations、temporary buffers 和 checkpoint 对单卡显存的影响。
- 能说明 ZeRO/FSDP 分别切分哪些训练状态，TP/PP 如何改变通信路径和 pipeline bubble。
- 能用 `distributed_training_strategy_report` 或等价表格比较 per-rank memory、global batch tokens、MFU、显存 gate 和 scale rehearsal action item。
- 能把 `checkpoint_resume_integrity_report` 或等价表格接到分布式策略报告中，说明目标 world size 下是否能安全恢复和 reshard。

**对应内容：**Ch07 7.10、7.15，Ch10 10.15。

### F. 成本与训练规划

- 能从数据 tokens、模型大小、batch、context、tokens/s、GPU 单价估算训练时长和成本。
- 能估算 checkpoint 存储、日志量和数据读取吞吐需求。
- 能在成本、质量、训练时长之间做可解释 trade-off。

**对应内容：**Training Capstone `plan_training.py`。

### G. 实验设计与对齐评估

- 能把训练项目写成一个可回答问题，而不是只报告“跑通了”。
- 能设计 baseline、ablation、开发集和失败案例分类。
- 能在 SFT 前审计 chat template、assistant-only mask、supervised token ratio、truncation 和 packing 边界；能在 DPO/GRPO 前审计 post-training 数据的任务覆盖、偏好标签冲突、长度偏差、eval overlap 和 unsafe chosen。
- 能解释 SFT/DPO/GRPO/DAPO/GSPO 的训练目标、rollout/ratio/length 诊断和最终 helpfulness、honesty、harmlessness、能力保留之间的差异。

**对应内容：**Ch08 8.7B、Ch09 9.6A 与 9.10A、Training Capstone README。

## 学习成果

| 项目项 | 合格标准 | 产出 |
|--------|----------|------|
| 数据分析 | 能输出样本数、空样本、重复率、长度分布和 token 预算 | `data_profile.py` 输出 |
| 数据策展 gate | 能报告数据源、过滤/去重、eval overlap、domain mixture 和 privacy 风险，并给出是否训练的判断 | data curation gate 表 |
| SFT 数据协议 gate | 能报告 chat template、assistant spans、supervised token ratio、assistant truncation、packing mode 和 block-diagonal attention 使用情况 | `sft_chat_template_mask_report` 表 |
| Post-training 数据 gate | 能报告 SFT/偏好/RLVR 数据的任务覆盖、安全切片、长度偏差、标签冲突、eval overlap 和 unsafe chosen 风险 | `post_training_data_audit` 表 |
| Reasoning RL 训练日志 | 能把 GRPO/DAPO/GSPO 的 reward、pass rate、completion length、entropy、clip fraction、approx KL、sequence ratio 和 rollout 有效比例放进同一张诊断表 | reasoning RL run log |
| 训练运行 | 能跑完整训练并持续记录 metrics | `train.py` + `metrics.jsonl` |
| Checkpoint | 能保存 latest checkpoint，并从中断 step 恢复；能证明 optimizer/scheduler/RNG/sampler/scaler state 完整、写入原子、分布式 checkpoint 可 reshard | `acceptance.py` resume 检查 + checkpoint integrity 表 |
| 开发集 | 能记录 val_loss / perplexity / ECE | `metrics.jsonl` |
| 监控指标 | 至少记录 loss、lr、grad_norm、tokens/s | `metrics.jsonl` |
| 显存规划 | 能拆分参数、梯度、optimizer state、activation 和 checkpoint 存储 | 显存估算表 |
| 分布式规划 | 能解释 ZeRO/FSDP2/TP/PP 选择、per-rank memory、tokens/s/GPU、MFU、sharded checkpoint 和 action item | strategy report + checkpoint integrity + 训练规划说明 |
| 训练规划 | 能估算 steps、GPU hours、成本、checkpoint 存储 | `plan_training.py` 输出 |
| 实验结论 | 项目有研究问题、baseline、ablation 和结论边界 | proposal / milestone / final report |
| 异常处理 | 能说明 nan/loss spike/吞吐下降时的排查顺序 | 复盘文档 |
| 最终运行 | 一条命令跑通训练工程闭环 | `python acceptance.py` 输出 `ACCEPTANCE: PASS` |

## 推荐 8 周节奏

| 周次 | 学习内容 | 工程任务 |
|------|----------|----------|
| 1 | Ch01-Ch02 | 做 tokenization、packing 和数据质量练习，记录数据 shape 与重复/污染风险 |
| 2 | Ch03-Ch06 | 跑通可训练 GPT，检查梯度和参数量 |
| 3 | Ch07 前半 | 实现 DataLoader、cross entropy、AdamW、scheduler |
| 4 | Ch07 后半 | 实现 AMP、gradient clipping、训练日志和 loss 曲线 |
| 5 | Ch09 | 跑 SFT/post-training data audit/LoRA/DPO/GRPO 练习，理解不同 loss 与 DAPO/GSPO 式 rollout 诊断 |
| 6 | Ch07 分布式专题 | 学 ZeRO/FSDP2/TP/PP、FP8/MXFP8、MFU、distributed checkpoint/resume |
| 7 | Training Capstone | 跑数据分析、训练、checkpoint/resume integrity、规划脚本和 strategy report |
| 8 | 复盘 | 写训练报告：配置、曲线、成本、失败排查、下一步 |

## 最终交付模板

```text
项目名称：
研究问题：
baseline：
数据集：
data curation gate：
post-training data gate：
reasoning RL run log：
token 数：
模型配置：
训练配置：
global batch tokens：
总 step：
优化器 / scheduler：
精度：
分布式策略 / MFU：
optimizer state / activation memory：
checkpoint 策略：
checkpoint integrity gate：
resume 是否验证：
train loss：
val loss / ppl：
tokens/s：
GPU hours：
预计成本：
ablation：
结论边界：
主要风险：
下一步实验：
```
