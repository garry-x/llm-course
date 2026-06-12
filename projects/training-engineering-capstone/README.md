# LLM Training Engineering Capstone

这个项目把第 7 章和第 9 章的训练知识落成一个可运行的训练工程作品：一个 PyTorch 字符级语言模型训练闭环，覆盖数据分析、data curation gate、训练、开发集监控、checkpoint、resume、metrics、训练规划和一键运行。

默认模型很小，可以在 CPU 上跑通；有 GPU 时会自动使用 CUDA。目标不是追求模型质量，而是先掌握训练工程交付物的结构：可复现训练配置、loss 曲线、checkpoint/resume、显存与吞吐估算，以及针对失败模式的 ablation。

## 你要交付什么

| 模块 | 最低要求 | 交付内容 |
|------|----------|----------|
| Data Profile | 样本数、空样本、重复率、长度分布、字符/token 规模 | `python data_profile.py` 输出 JSON |
| Data Curation Gate | 报告数据源、过滤、去重、eval overlap、domain mixture 和 privacy 风险是否支持训练 | 报告中的 data curation 表 |
| Training | PyTorch 训练循环，记录 train_loss、val_loss、ppl、lr、grad_norm、tokens/s | `metrics.jsonl` |
| Checkpoint | 保存 latest checkpoint，包含 model/optimizer/config/global_step | `checkpoints/latest.pt` |
| Resume | 从 checkpoint 恢复并继续训练，global_step 单调增加 | `python acceptance.py` |
| Planning | 估算 steps、GPU hours、成本、checkpoint 存储 | `python plan_training.py` |
| Strategy Report | 对照 Ch07 的 `distributed_training_strategy_report`，估算 DDP/ZeRO/FSDP 类策略的每卡模型状态、global batch tokens、MFU 和 scale rehearsal 风险 | 报告中的 strategy 表 |
| Industrial Gate | 把训练 run 拆成 optimization、throughput、state/checkpoint、evaluation gate | 报告中的 gate 表 |
| Acceptance | 串联数据分析、训练、resume、规划和指标检查 | `python acceptance.py` 输出 `ACCEPTANCE: PASS` |

## 项目问题设计

这个 capstone 不只是“把训练脚本跑通”。报告需要回答一个明确的训练工程问题，并用实验支持结论。可选方向：

| 研究问题 | 比较对象 | 主要指标 | 常见结论边界 |
|----------|----------|----------|--------------|
| 学习率如何影响收敛和稳定性 | `lr=1e-3` vs `3e-4` | train/val loss、grad_norm、NaN/loss spike | tiny corpus 上的最优 lr 不能外推到大模型 |
| 序列长度如何影响质量和吞吐 | `seq_len=64` vs `128` | val PPL、tokens/s、显存/内存 | 字符级模型和 BPE 模型的长度含义不同 |
| batch size / grad accumulation 如何影响曲线 | 小 batch vs 等效大 batch | loss 方差、tokens/s、step time | CPU baseline 的吞吐结论不能直接外推 GPU |
| dropout 或 weight decay 是否缓解过拟合 | 正则开/关 | train-val gap、val loss | 数据很小时方差可能大于真实差异 |
| 数据清洗或配比是否值得 | raw data vs dedup/filter/rebalanced mix | duplicate rate、eval overlap、quality pass rate、val PPL、目标任务指标 | tiny corpus 的质量过滤规则不能直接外推到 web-scale 预训练 |

建议把项目拆成三个阶段：

| 阶段 | 交付 |
|------|------|
| Proposal | 写出研究问题、baseline、数据、训练预算、主要风险 |
| Milestone | 跑通一次训练和 resume，给出第一版曲线与失败案例 |
| Final Report | 补充 ablation、错误分析、成本估算、结论边界和复现命令 |

## 快速开始

```bash
cd projects/training-engineering-capstone
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

python acceptance.py
```

单独运行训练：

```bash
python train.py \
  --data sample_corpus.txt \
  --out-dir runs/demo \
  --steps 40 \
  --batch-size 8 \
  --seq-len 64
```

从 checkpoint 恢复：

```bash
python train.py --data sample_corpus.txt --out-dir runs/demo --steps 60 --resume
```

数据分析：

```bash
python data_profile.py --data sample_corpus.txt
```

训练规划：

```bash
python plan_training.py \
  --tokens 1000000000 \
  --seq-len 2048 \
  --micro-batch 8 \
  --grad-accum 16 \
  --gpus 8 \
  --tokens-per-second-per-gpu 2500 \
  --gpu-hour-cost 2.5
```

## 上线准备

- 固定随机种子、训练配置和数据版本。
- 数据报告包含 source inventory、过滤规则、重复率、eval overlap、domain mixture、PII/凭据风险和未覆盖风险。
- `metrics.jsonl` 至少包含 train_loss、val_loss、ppl、lr、grad_norm、tokens/s。
- `checkpoints/latest.pt` 能恢复训练，resume 后 global_step 增加。
- 能解释 global batch tokens、总 step、tokens/s/GPU、GPU hours 和预计成本。
- 能用 strategy report 说明 DDP、ZeRO/FSDP、TP/PP 或低精度训练分别解决的是容量、通信、吞吐还是 checkpoint 状态问题。
- 能说明 loss spike、nan、吞吐下降、开发集退化时的排查顺序。
- 能把训练 run 映射到 optimization、throughput、state/checkpoint、evaluation 四类 gate，并说明哪些 gate 支持继续扩容，哪些 gate 要先 debug。

## 项目报告要求

训练工程报告必须包含：

- 数据分析结果：长度分布、重复、异常样本、过滤/去重规则、eval overlap、domain mixture、PII/凭据风险和 token 预算。
- Data curation gate：按 Ch07 `training_data_curation_report` 或等价表格报告 size、dedup、quality filter、eval contamination、mixture balance 和 privacy gate；未通过时不能把训练曲线当作可扩容证据。
- 训练曲线：train loss、val loss、perplexity、lr、grad_norm 和 tokens/s。
- checkpoint resume 产出：恢复后 step 单调增加，配置和优化器状态被恢复。
- 至少一个 ablation，例如学习率、batch size、seq_len 或 dropout。
- loss spike、NaN、过拟合或吞吐下降的排查记录。
- 若使用 SFT 数据做 post-training，必须报告 chat template、assistant spans、assistant-only label mask、supervised token ratio、assistant truncation、packing mode 和是否使用 block-diagonal attention；任一 gate 未通过时，SFT loss 下降不能作为指令跟随改进证据。
- 若使用偏好数据或 RLVR/RFT 数据做 post-training，必须报告任务覆盖、安全切片、同 prompt 标签冲突、长度偏差、eval overlap 和 unsafe chosen；任一 gate 未通过时，DPO/GRPO loss 下降不能作为模型改进证据。
- 若使用 LLM-as-judge 或偏好评测替代人工检查，必须报告 position/verbosity bias、swapped-order consistency 和少量 human label agreement；未通过时不能把 judge win rate 当作训练改进证据。
- 分布式/低精度策略说明：即使本项目只在 CPU 或单 GPU 上跑，也要用 Ch07 的策略账本解释目标规模下 DDP、ZeRO/FSDP、FP8/MXFP8 或 checkpoint state 会改变哪些风险。
- 明确说明你的研究问题、baseline、结论适用条件，以及哪些结果只在 tiny corpus / CPU baseline 下成立。

### Final report 结构

报告不是运行日志拼接。建议按下面结构写，让读者能判断你的训练结论是否成立：

1. **Research question.** 用一句话提出可回答的问题，例如“在固定 token budget 下，较长 `seq_len` 是否降低 validation PPL，并以多少 tokens/s 为代价？”
2. **Hypothesis.** 写出预期机制：更长上下文可能改善依赖建模，但会降低 batch occupancy 或增加 step time。
3. **Related work.** 连接至少 2 篇论文、技术报告或官方文档，例如 AdamW、Chinchilla、ZeRO/FSDP、LoRA 或数据质量相关材料，说明你的项目采用了什么、简化了什么。
4. **Experimental setup.** 固定数据版本、source inventory、过滤/去重规则、seed、模型配置、训练步数、batch tokens、optimizer、scheduler、precision 和硬件环境。
5. **Baseline.** 至少有一个清晰 baseline，例如默认 `seq_len=64`、`lr=3e-4`、`dropout=0.1`。
6. **Ablation.** 一次只改一个主要因素；若同时改多个因素，要说明为什么无法归因。
7. **Results.** 用表格报告 train loss、val loss/PPL、grad norm、tokens/s、step time、是否出现 NaN/loss spike。
8. **Data curation gate.** 报告 total tokens/documents、weighted duplicate rate、quality pass rate、max eval overlap、domain token shares、PII/凭据风险和 action items；若做 SFT，还要报告 template/mask/packing gate。
9. **Error analysis.** 至少解释一个失败 run：学习率过高、数据重复、train/val 分叉、batch 太小、吞吐下降或 resume 异常。
10. **Strategy report.** 用 `distributed_training_strategy_report` 或等价表格报告每卡模型状态、global batch tokens、MFU、显存 gate 和 action item；若讨论 FP8/MXFP8，写清 scale/amax/checkpoint state 如何验证。
11. **Industrial gates.** 用表格报告 data curation、optimization、throughput、state/checkpoint、evaluation gate：每个 gate 的信号、阈值、通过/失败和下一步动作。
12. **Cost and scaling.** 把实验中的 tokens/s、global batch tokens、steps 和 `plan_training.py` 的 GPU hours/cost 联系起来。
13. **Limitations and reproducibility.** 明确哪些结论只适用于 tiny corpus、字符级 tokenizer、CPU/GPU 环境或这个模型规模，并列出复现命令、配置和 checkpoint/resume 路径。

### 结果表模板

SFT template/mask/packing gate：

| Dataset split | chat template | assistant spans | supervised ratio | truncated assistant tokens | packing mode | gate / action |
|---------------|---------------|-----------------|------------------|----------------------------|--------------|---------------|
| train | ChatML-like | `[(5, 24), ...]` | 0.34 | 0 | block-diagonal | pass |
| val | ChatML-like | `[(6, 18), ...]` | 0.29 | 3 | causal packed | fail: increase max_seq_len or change packing |

| Run | 变化因素 | train loss | val loss | PPL | grad_norm | tokens/s | 异常 | 结论 |
|-----|----------|------------|----------|-----|-----------|----------|------|------|
| baseline | 默认配置 | | | | | | | |
| ablation | 例如 `seq_len=128` | | | | | | | |

### Strategy report 模板

| Strategy | 每卡模型状态 | Global batch tokens | MFU | 显存 gate | Action item |
|----------|--------------|---------------------|-----|-----------|-------------|
| DDP / ZeRO / FSDP | | | | | |

### Data curation gate 模板

| Source/mix | tokens | documents | duplicate rate | quality pass rate | eval overlap | PII/secret risk | domain share | Gate | 下一步 |
|------------|--------|-----------|----------------|-------------------|--------------|-----------------|--------------|------|--------|
| baseline | | | | | | | | | |

### Industrial gate 模板

| Gate | 信号 | 阈值/判断 | 状态 | 下一步 |
|------|------|-----------|------|--------|
| Data curation | tokens/documents、duplicate、quality、eval overlap、domain mix、PII | | | |
| Optimization | train/val loss、grad_norm、NaN/loss spike | | | |
| Throughput | tokens/s、step time、dataloader wait、checkpoint overhead | | | |
| State | checkpoint/resume、lr 连续性、optimizer/scheduler/RNG/sampler state | | | |
| Evaluation | 固定 benchmark、格式/安全回归、baseline 对比 | | | |

如果两个 run 的差异小于随机波动，报告应写“不足以支持改动有效”，而不是强行给出优化结论。一个严谨的负结果仍然是合格的训练工程结论。
