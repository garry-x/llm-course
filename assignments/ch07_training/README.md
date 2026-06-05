# Chapter 7 Assignment: Training Loop

本作业对应第 7 章训练循环。目标是把 next-token 数据切片、稳定交叉熵、AdamW、warmup+cosine 调度和一个可复现的小训练循环串起来。

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
- `cross_entropy_manual` 必须使用 log-sum-exp trick，并与 `torch.nn.functional.cross_entropy` 匹配。
- `AdamW` 必须实现一阶/二阶动量、偏置修正和解耦权重衰减。
- 调度器必须先 warmup 到 1，再 cosine decay 到 `min_lr_ratio`。
- `train` 必须执行 `zero_grad -> forward -> loss -> backward -> clip -> step -> scheduler.step`，并记录 loss history。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 推导交叉熵、perplexity、AdamW 偏置修正、warmup+cosine 边界和 grad clipping 的诊断意义 |
| Programming parts | 55 | 实现 dataset/dataloader、稳定 cross entropy、AdamW、scheduler 和训练循环 |
| Analysis / style | 10 | 用训练日志解释 loss spike、NaN、grad_norm、tokens/s 和 resume 行为 |
