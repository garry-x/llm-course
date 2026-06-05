# Chapter 5 Assignment: Transformer Block

本作业对应第 5 章的归一化、前馈网络和完整 Decoder Block 练习。目标是把 `LayerNorm`、`RMSNorm`、`FFN`、`SwiGLU` 和 Pre-Norm `TransformerBlock` 写成可测试模块，并用梯度检查验证核心反向传播。

## Files

- `starter.py`: 学生起始代码。
- `reference_solution.py`: 参考实现。
- `tests.py`: 可运行测试。

## Run

```bash
.venv/bin/python assignments/ch05_block/tests.py
```

默认测试 `reference_solution.py`。测试学生代码时：

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch05_block/tests.py
```

## Requirements

- 不允许调用 `nn.LayerNorm` 实现 `LayerNorm`。
- `LayerNormFunction.backward` 需要返回 `x`、`gamma`、`beta` 的正确梯度。
- `RMSNorm` 只做 RMS 缩放，不做均值中心化。
- `TransformerBlock` 使用 Pre-Norm：`RMSNorm -> MHA -> residual` 和 `RMSNorm -> SwiGLU -> residual`。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 推导 LayerNorm/RMSNorm，比较 Pre-Norm/Post-Norm 梯度路径，计算 FFN/SwiGLU 参数量 |
| Programming parts | 55 | 实现 LayerNorm、RMSNorm、FFN/SwiGLU 和 Pre-Norm TransformerBlock |
| Analysis / style | 10 | 说明数值稳定性、梯度检查、残差路径和跳过子层的投机实现风险 |
