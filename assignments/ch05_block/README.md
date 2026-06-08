# Chapter 5 Assignment: Transformer Block

本作业对应第 5 章的归一化、前馈网络和完整 Decoder Block 练习。目标是把 `LayerNorm`、`RMSNorm`、`FFN`、`SwiGLU` 和 Pre-Norm `TransformerBlock` 写成可测试模块，并把 RMSNorm 输入梯度、4x GELU FFN 与 SwiGLU 8/3 宽度的参数预算、Pre-Norm/Post-Norm 梯度路径推导转成可计算函数。

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
- `rms_norm_input_gradient` 需要写出 RMSNorm 对输入的梯度，并与 autograd 对齐。
- `swiglu_hidden_size_for_param_budget` 和 `ffn_parameter_counts` 需要按 bias-free 矩阵参数量解释 8/3 宽度来源。
- `residual_gradient_path_factors` 需要在线性化标量残差模型中比较 Pre-Norm 与 Post-Norm 的逐层梯度因子。
- `TransformerBlock` 使用 Pre-Norm：`RMSNorm -> MHA -> residual` 和 `RMSNorm -> SwiGLU -> residual`。
- `estimate_block_resources` 估算单个 block 的参数量、主要 FLOPs、attention score 显存和主要激活显存。
- `activation_checkpointing_tradeoff` 估算 activation checkpointing 省下的激活显存和额外重算 FLOPs。

## Conceptual Handout

Transformer block 是 LLM 的重复计算单元。一个 block 的设计会同时影响训练稳定性、梯度路径、参数量、激活显存和推理延迟。本作业要求你从公式、PyTorch 模块和资源估算三个角度理解 LayerNorm/RMSNorm、FFN/SwiGLU、residual path 和 activation checkpointing。

### 1. LayerNorm 与 RMSNorm 的区别

LayerNorm 对最后一维做均值和方差归一化：

```text
mu = mean(x)
var = mean((x - mu)^2)
y = gamma * (x - mu) / sqrt(var + eps) + beta
```

RMSNorm 不减去均值，只按 RMS 缩放：

```text
rms = sqrt(mean(x^2) + eps)
y = gamma * x / rms
```

RMSNorm 参数更少、计算更简单，现代 LLM 常用它替代 LayerNorm。它不保证输出均值为 0，因此不能用 LayerNorm 的直觉替代 RMSNorm。`rms_norm_input_gradient` 让你推导一个重要事实：归一化层的反向传播不是逐元素独立的，因为 `rms` 依赖同一 token 的所有 feature。

报告中应说明：

- `eps` 防止接近零方差或零 RMS 时数值爆炸。
- `gamma` 是可训练缩放；RMSNorm 通常没有 `beta`。
- 低精度训练中 Norm 的 dtype、eps 和累积精度会影响稳定性。

### 2. FFN、SwiGLU 与 8/3 宽度

标准 GELU FFN 常写作：

```text
FFN(x) = W_2 GELU(W_1 x)
```

若 hidden width 为 `4 * d_model`，bias-free 参数量是：

```text
params_gelu = d_model * 4d_model + 4d_model * d_model = 8 d_model^2
```

SwiGLU 有 gate、value 和 output 三个矩阵：

```text
SwiGLU(x) = W_o (SiLU(W_g x) * W_v x)
```

若希望参数预算接近 `8 d_model^2`，则：

```text
3 * d_model * d_ff = 8 * d_model^2
d_ff = 8/3 * d_model
```

这就是作业里 `swiglu_hidden_size_for_param_budget` 的来源。SwiGLU 通常比同预算 GELU FFN 表达能力更强，但它不是免费午餐：多一个投影分支会影响 kernel、激活保存和实现复杂度。

### 3. Pre-Norm 为什么更适合深层网络

Decoder block 可以用 Pre-Norm：

```text
x_{l+1} = x_l + Sublayer(Norm(x_l))
```

也可以用 Post-Norm：

```text
x_{l+1} = Norm(x_l + Sublayer(x_l))
```

在线性化标量模型中，Pre-Norm 的残差路径梯度近似含有直接的 `1 + ...` 项；Post-Norm 的梯度还会整体乘上 norm slope。深层模型中，Pre-Norm 更容易保留穿过 residual stream 的梯度通道，因此现代 decoder-only LLM 多采用 Pre-Norm 或其变体。

`residual_gradient_path_factors` 是一个 toy diagnostic，不是完整理论证明。报告中要说明它展示的是趋势：直接 residual path 能缓解梯度消失，但真实训练还取决于初始化、优化器、学习率、Norm 实现、深度和数据。

### 4. Block 资源估算

一个 block 的资源主项包括：

- attention 参数：Q/K/V/O projection。
- FFN 参数：GELU 两矩阵或 SwiGLU 三矩阵。
- norm 参数：每层 `gamma`，LayerNorm 还可能有 `beta`。
- FLOPs：QKV projection、attention scores、attention-value matmul、output projection、FFN/SwiGLU。
- activation memory：训练时需要保存中间激活用于反向传播。
- attention score memory：dense `[B, H, T, T]` 是二次项。

`estimate_block_resources` 的目的不是给出硬件 profiler 级精确数字，而是训练你识别主导项。报告中必须写清单位和假设：batch size、sequence length、dtype bytes、head 数、FFN width，以及是否使用 checkpointing、FlashAttention 或 fused kernels。

### 5. Activation checkpointing 的 trade-off

Activation checkpointing 用重算换显存：前向时不保存部分中间激活，反向时重新计算这些前向结果。粗略地：

```text
saved_memory = activation_bytes * checkpointed_fraction
extra_flops ~= forward_flops * checkpointed_fraction
```

训练总 FLOPs baseline 常近似为 `forward + backward ~= 3 * forward_flops`；checkpointing 会在反向中增加重算。它适合显存受限的训练，但会降低吞吐。报告中应说明这不是“无损优化”：它改变了 wall-clock time、GPU 利用率和 recompute/communication overlap。

### 6. 组件可解释性的边界

本章涉及 probing、patching 和 ablation 的结论边界。一个组件输出变化并不自动证明“模型使用了该机制”。更严谨的说法应该区分：

- Probing：某个表示中可线性读出信息，不等于模型决策依赖该信息。
- Activation patching：替换激活改变输出，支持因果诊断，但依赖干预位置和分布。
- Ablation：移除模块造成性能下降，说明模块有功能贡献，但不说明具体内部算法。

最终报告应把实现、梯度和资源连起来：一个合格 Transformer block 不只是 forward shape 正确，还应能解释为什么使用 RMSNorm/SwiGLU/Pre-Norm，资源主项在哪里，checkpointing 换来的显存是否值得。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 推导 LayerNorm/RMSNorm forward 与 RMSNorm 输入梯度，比较 Pre-Norm/Post-Norm 梯度路径，计算 FFN/SwiGLU 参数量、FLOPs、激活显存、checkpointing 重算成本和 8/3 宽度来源，并解释 probing/patching/ablation 的结论边界 |
| Programming parts | 55 | 实现 LayerNorm、RMSNorm、RMSNorm input gradient、FFN/SwiGLU、SwiGLU 参数预算函数、Pre/Post-Norm 梯度路径诊断、Pre-Norm TransformerBlock、block resource estimator 和 checkpointing tradeoff estimator |
| Analysis / style | 10 | 说明数值稳定性、梯度检查、残差路径、SwiGLU 门控含义、资源估算边界、组件可解释性实验和跳过子层的投机实现风险 |
