# LLM 训练工程师课程路线与学习成果

这份文档把课程中的模型实现、训练循环、微调对齐、实验设计和大规模训练优化整理成“LLM 训练工程师”岗位路线。训练工程师的核心产出不是一个 notebook，而是一套可复现、可恢复、可观测、成本可解释的训练系统。

## 目标画像

完成路线后，你应该能独立设计和维护一个小型 LLM 训练任务：准备数据、配置训练、监控 loss/throughput/grad norm、保存 checkpoint、从中断恢复、做开发集评估，提出 baseline/ablation，并能解释显存、吞吐、GPU 小时和训练成本之间的关系。

## 学习路径

| 阶段 | 章节与项目 | 主要问题 | 学习产出 |
|------|------------|----------|----------|
| 1. 模型可训练性 | Ch01-Ch06 | 数据如何变成 logits，梯度如何穿过模型 | 能解释 token、shape、参数量、梯度路径 |
| 2. 单机训练循环 | Ch07 | 如何让 loss 稳定下降 | DataLoader、loss、optimizer、scheduler、AMP、checkpoint |
| 3. 微调与对齐 | Ch09 | 如何把预训练模型变成可用助手 | SFT/LoRA/DPO/GRPO 训练数据、loss masking、偏好优化 |
| 4. 实验设计与评估 | Ch08-Ch09、Capstone | 如何证明训练或对齐方法真的更好 | research question、baseline、ablation、对齐评估和结论边界 |
| 5. 大规模训练效率 | Ch07、Ch10 | 如何解决显存、通信、吞吐、精度和成本问题 | ZeRO/FSDP/TP/PP、FP8/FP4、MFU、tokens/s 解释 |
| 6. 工程实践 | Training Capstone | 如何证明训练任务可复现、可恢复、可观测 | acceptance 输出、metrics.jsonl、checkpoint、训练规划报告 |

## 能力目标

### A. 数据与 Token 预算

- 能区分 raw text、tokenized dataset、packed sequence、train/val split。
- 能计算 token budget、batch size、sequence length、gradient accumulation 对总 step 的影响。
- 能发现空样本、重复样本、过长样本、编码异常和数据泄漏风险。

**对应内容：**Ch01、Ch07 7.3，Training Capstone `data_profile.py`。

### B. 训练循环与优化

- 能实现 forward、loss、backward、gradient clipping、optimizer step、scheduler step。
- 能解释 AdamW、warmup+cosine、weight decay、grad norm、loss scale。
- 能判断 loss spike、nan、梯度爆炸、学习率过高、batch 太小等常见问题。

**对应内容：**Ch07 7.1-7.12，Training Capstone `train.py`。

### C. Checkpoint 与可恢复性

- 能保存 model/optimizer/scheduler/global_step/random seed/config。
- 能从 checkpoint resume，并保证 step、lr、best metric 和日志连续。
- 能区分 latest、best、periodic checkpoint 的保留策略。

**对应内容：**Ch07，Training Capstone `train.py` 与 `acceptance.py`。

### D. 监控与实验管理

- 能记录 train_loss、val_loss、perplexity、calibration/ECE、lr、grad_norm、tokens/s、samples/s。
- 能用 JSONL/CSV/W&B/TensorBoard 记录实验，并保留 config。
- 能用固定开发集判断训练是否真的改进，而不是只看训练 loss。

**对应内容：**Ch07，Ch09，Training Capstone `metrics.jsonl`。

### E. 分布式与低精度训练

- 能解释 DP、DDP、FSDP/ZeRO、TP、PP、gradient accumulation 的适用场景。
- 能解释 BF16/FP16/FP8/FP4 的收益、风险和常见数值问题。
- 能用 MFU、tokens/s/GPU、通信开销判断集群训练效率。

**对应内容：**Ch07 7.10、7.15，Ch10 10.15。

### F. 成本与训练规划

- 能从数据 tokens、模型大小、batch、context、tokens/s、GPU 单价估算训练时长和成本。
- 能估算 checkpoint 存储、日志量和数据读取吞吐需求。
- 能在成本、质量、训练时长之间做可解释 trade-off。

**对应内容：**Training Capstone `plan_training.py`。

### G. 实验设计与对齐评估

- 能把训练项目写成一个可回答问题，而不是只报告“跑通了”。
- 能设计 baseline、ablation、开发集和失败案例分类。
- 能解释 SFT/DPO/GRPO 的训练目标和最终 helpfulness、honesty、harmlessness、能力保留之间的差异。

**对应内容：**Ch08 8.7B、Ch09 9.10A、Training Capstone README。

## 学习成果

| 项目项 | 合格标准 | 产出 |
|--------|----------|------|
| 数据分析 | 能输出样本数、空样本、重复率、长度分布 | `data_profile.py` 输出 |
| 训练运行 | 能跑完整训练并持续记录 metrics | `train.py` + `metrics.jsonl` |
| Checkpoint | 能保存 latest checkpoint，并从中断 step 恢复 | `acceptance.py` resume 检查 |
| 开发集 | 能记录 val_loss / perplexity / ECE | `metrics.jsonl` |
| 监控指标 | 至少记录 loss、lr、grad_norm、tokens/s | `metrics.jsonl` |
| 训练规划 | 能估算 steps、GPU hours、成本、checkpoint 存储 | `plan_training.py` 输出 |
| 实验结论 | 项目有研究问题、baseline、ablation 和结论边界 | proposal / milestone / final report |
| 异常处理 | 能说明 nan/loss spike/吞吐下降时的排查顺序 | 复盘文档 |
| 最终运行 | 一条命令跑通训练工程闭环 | `python acceptance.py` 输出 `ACCEPTANCE: PASS` |

## 推荐 8 周节奏

| 周次 | 学习内容 | 工程任务 |
|------|----------|----------|
| 1 | Ch01-Ch02 | 做 tokenization 和 packing 练习，记录数据 shape |
| 2 | Ch03-Ch06 | 跑通可训练 GPT，检查梯度和参数量 |
| 3 | Ch07 前半 | 实现 DataLoader、cross entropy、AdamW、scheduler |
| 4 | Ch07 后半 | 实现 AMP、gradient clipping、训练日志和 loss 曲线 |
| 5 | Ch09 | 跑 SFT/LoRA/DPO/GRPO 练习，理解不同 loss |
| 6 | Ch07 分布式专题 | 学 ZeRO/FSDP/TP/PP、FP8/FP4、MFU |
| 7 | Training Capstone | 跑数据分析、训练、checkpoint/resume、规划脚本 |
| 8 | 复盘 | 写训练报告：配置、曲线、成本、失败排查、下一步 |

## 最终交付模板

```text
项目名称：
研究问题：
baseline：
数据集：
token 数：
模型配置：
训练配置：
global batch tokens：
总 step：
优化器 / scheduler：
精度：
checkpoint 策略：
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
