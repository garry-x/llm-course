# Chapter 5 Assignment: Transformer Block

本作业对应第 5 章的归一化、前馈网络和完整 Decoder Block 练习。目标是把 `LayerNorm`、`RMSNorm`、`FFN`、`SwiGLU` 和 Pre-Norm `TransformerBlock` 写成可测试模块，并把 4x GELU FFN 与 SwiGLU 8/3 宽度的参数预算推导转成可计算函数。

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
- `swiglu_hidden_size_for_param_budget` 和 `ffn_parameter_counts` 需要按 bias-free 矩阵参数量解释 8/3 宽度来源。
- `TransformerBlock` 使用 Pre-Norm：`RMSNorm -> MHA -> residual` 和 `RMSNorm -> SwiGLU -> residual`。
- `estimate_block_resources` 估算单个 block 的参数量、主要 FLOPs、attention score 显存和主要激活显存。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 推导 LayerNorm/RMSNorm，比较 Pre-Norm/Post-Norm 梯度路径，计算 FFN/SwiGLU 参数量、FLOPs、激活显存和 8/3 宽度来源，并解释 probing/patching/ablation 的结论边界 |
| Programming parts | 55 | 实现 LayerNorm、RMSNorm、FFN/SwiGLU、SwiGLU 参数预算函数、Pre-Norm TransformerBlock 和 block resource estimator |
| Analysis / style | 10 | 说明数值稳定性、梯度检查、残差路径、SwiGLU 门控含义、资源估算边界、组件可解释性实验和跳过子层的投机实现风险 |
