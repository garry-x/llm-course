# 数学与 PyTorch 先修复习

本附录补齐高校课程中常见的线性代数、概率、反向传播和张量求导前置知识。它不是独立数学课，而是服务于本课程的实现、推导和代码审查。微积分、统计和机器学习基础到本课程项目产出的桥接见 [ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md)。

## 线性代数最小集合

学生需要熟练掌握：

- 向量、矩阵、张量的 shape 约定。
- 矩阵乘法 `A @ B` 的维度条件。
- 转置、广播、逐元素乘法和 reduction。
- 点积、范数、余弦相似度。
- softmax 前减去最大值的数值稳定性。

### 检查点

给定 `Q, K, V` 的 shape 分别为 `[B, H, T, D]`、`[B, H, S, D]`、`[B, H, S, D]`：

- `Q @ K.transpose(-2, -1)` 的 shape 是 `[B, H, T, S]`。
- attention probabilities 与 `V` 相乘后输出 `[B, H, T, D]`。
- causal mask 的 shape 可以是 `[T, S]`、`[B, T, S]` 或 `[B, H, T, S]`，但语义必须是屏蔽未来位置。

## 概率与语言模型

自回归语言模型把序列概率分解为：

```text
P(x_1, ..., x_T) = product_t P(x_t | x_<t)
```

训练时通常最大化 token 条件概率，等价于最小化 cross entropy：

```text
loss = -mean_t log P(target_t | context_t)
```

perplexity 是 `exp(loss)`，表示平均每一步仍有多少等价候选。

## 统计与 ML Foundations 入口

本课程项目报告需要的统计和机器学习基础包括：

- train / validation / test split。
- baseline、ablation 和 held-out evaluation。
- sample mean、variance、seed sensitivity 和 benchmark uncertainty。
- overfitting、data leakage 和 benchmark contamination。
- objective、metric 和 generalization boundary 的区别。

这些内容按 [ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md) 补救，并在训练/推理 capstone proposal、milestone 和 final report 中作为评分依据。

## 反向传播核心规则

需要掌握以下链式法则：

```text
z = f(y), y = g(x)
dz/dx = dz/dy * dy/dx
```

对张量实现而言，重点不是手写 Jacobian，而是理解每个参数如何从 loss 收到梯度：

- `Linear`: `y = x W^T + b`，梯度流向 `x`、`W`、`b`。
- `Embedding`: 只有被索引到的 token 行收到梯度。
- `LayerNorm`: 梯度必须考虑均值和方差对所有特征维度的耦合。
- `Attention`: `Q/K/V` 都通过 scores、softmax 和 weighted sum 收到梯度。

## Cross Entropy 推导检查

对单个样本 logits `z` 和目标类别 `y`：

```text
p_i = exp(z_i) / sum_j exp(z_j)
loss = -log p_y
d loss / d z_i = p_i - 1[i = y]
```

实现时应使用 log-sum-exp trick：

```text
logsumexp(z) = m + log(sum_i exp(z_i - m)), m = max_i z_i
```

## LayerNorm 推导检查

对最后一维归一化：

```text
mu = mean(x)
var = mean((x - mu)^2)
x_hat = (x - mu) / sqrt(var + eps)
y = gamma * x_hat + beta
```

反向传播中 `dx` 不能只写成 `dy * gamma / sqrt(var + eps)`，因为 `mu` 和 `var` 都依赖 `x`。正确实现应通过 gradcheck 或与 PyTorch 参考实现对齐。

## DPO/GRPO 推导检查

DPO 的核心比较是 chosen 与 rejected 在 policy/reference 下的 log probability ratio：

```text
logit = beta * [(logp_pi(chosen)-logp_ref(chosen)) - (logp_pi(rejected)-logp_ref(rejected))]
loss = -log sigmoid(logit)
```

GRPO 的关键不是单个样本 reward，而是同 prompt 多个响应组成的组内标准化 advantage：

```text
A_i = (r_i - mean_group(r)) / (std_group(r) + eps)
```

## PyTorch 实现纪律

- 每个核心函数都先写 shape 注释或测试。
- 涉及概率的函数要测试极端 logits、mask、空边界和 dtype。
- 涉及梯度的函数要用 `torch.autograd.gradcheck` 或与 PyTorch 官方模块对比。
- 用 `.reshape` 处理可能不连续的张量，避免无意中依赖 `.view`。
- 不在训练循环中静默吞掉 NaN；应记录 step、loss、grad_norm 和输入 batch。
