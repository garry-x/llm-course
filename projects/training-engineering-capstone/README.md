# LLM Training Engineering Capstone

这个项目把第 7 章和第 9 章的训练知识落成一个可运行的训练工程作品：一个 PyTorch 字符级语言模型训练闭环，覆盖数据分析、训练、开发集监控、checkpoint、resume、metrics、训练规划和一键运行。

默认模型很小，可以在 CPU 上跑通；有 GPU 时会自动使用 CUDA。目标不是追求模型质量，而是先掌握训练工程交付物的结构。训练项目的 CPU baseline、GPU/API 额度、成本记录和降级路径按 [Compute Resource and Cost Guide](../../docs/compute-resource-guide.md) 执行。

## 你要交付什么

| 模块 | 最低要求 | 交付内容 |
|------|----------|----------|
| Data Profile | 样本数、空样本、重复率、长度分布、字符/token 规模 | `python data_profile.py` 输出 JSON |
| Training | PyTorch 训练循环，记录 train_loss、val_loss、ppl、lr、grad_norm、tokens/s | `metrics.jsonl` |
| Checkpoint | 保存 latest checkpoint，包含 model/optimizer/config/global_step | `checkpoints/latest.pt` |
| Resume | 从 checkpoint 恢复并继续训练，global_step 单调增加 | `python acceptance.py` |
| Planning | 估算 steps、GPU hours、成本、checkpoint 存储 | `python plan_training.py` |
| Acceptance | 串联数据分析、训练、resume、规划和指标检查 | `python acceptance.py` 输出 `ACCEPTANCE: PASS` |

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

## 上线检查清单

- 固定随机种子、训练配置和数据版本。
- `metrics.jsonl` 至少包含 train_loss、val_loss、ppl、lr、grad_norm、tokens/s。
- `checkpoints/latest.pt` 能恢复训练，resume 后 global_step 增加。
- 能解释 global batch tokens、总 step、tokens/s/GPU、GPU hours 和预计成本。
- 能说明 loss spike、nan、吞吐下降、开发集退化时的排查顺序。

## 项目报告 Rubric

报告评分使用 [Capstone 项目报告 Rubric](../../docs/project-report-rubric.md)。训练工程报告必须额外包含：

- 数据分析结果：长度分布、重复、异常样本和 token 预算。
- 训练曲线：train loss、val loss、perplexity、lr、grad_norm 和 tokens/s。
- checkpoint resume 产出：恢复后 step 单调增加，配置和优化器状态被恢复。
- 至少一个 ablation，例如学习率、batch size、seq_len 或 dropout。
- loss spike、NaN、过拟合或吞吐下降的排查记录。
