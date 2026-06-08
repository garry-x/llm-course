# Ch03 Scaled Dot-Product Attention 作业测试

本目录把第 3 章的编程练习整理成可自动验收的作业入口，覆盖 QKV 投影、Scaled Dot-Product Attention、self-attention permutation equivariance、softmax/attention 反向传播、Q/K/V 手写梯度、attention entropy、attention score 显存估算、Causal Mask、causal+padding mask 合成、因果注意力和注意力热力图函数。

## 文件说明

| 文件 | 用途 |
|------|------|
| `starter.py` | 学生起始代码，包含需要实现的 TODO |
| `reference_solution.py` | 教师参考实现，用于验证测试本身 |
| `tests.py` | `unittest` 测试，覆盖 shape、缩放、mask、置换等变性、softmax Jacobian、attention logits gradient、Q/K/V gradients、attention entropy、attention score 显存、因果约束、padding key 屏蔽和可视化返回值 |

## 学生运行方式

```bash
cp assignments/ch03_attention/starter.py assignments/ch03_attention/student_solution.py
# 编辑 student_solution.py 完成 TODO
STUDENT_MODULE=student_solution .venv/bin/python assignments/ch03_attention/tests.py
```

也可以直接让测试加载 `starter.py`：

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch03_attention/tests.py
```

也可以直接验证课程内置参考实现：

```bash
.venv/bin/python assignments/ch03_attention/tests.py
```

## Conceptual Handout

Attention 是后续 MHA/GQA/MLA、KV Cache、FlashAttention、RAG context packing 和推理服务成本分析的共同基础。本作业要求你不仅实现 forward，还要能解释每个张量的语义、mask 为什么必须在 softmax 前应用、梯度如何从输出回到 Q/K/V，以及 attention heatmap 能支持什么结论。

### 1. Q/K/V 的张量语义

对输入 `X in R^{B x T x d_model}`，线性投影得到：

```text
Q = X W_q,  K = X W_k,  V = X W_v
```

单头作业里常用 shape 是 `[B, T, d_k]`。attention score 为：

```text
scores = Q K^T / sqrt(d_k)
```

输出为：

```text
A = softmax(scores)
O = A V
```

其中 `scores[b, i, j]` 表示第 `i` 个 query 位置对第 `j` 个 key 位置的匹配分数；`A[b, i, :]` 是一个概率分布；`O[b, i, :]` 是对所有 value 的加权和。报告中必须区分 score、probability 和 context/output，不能把它们都称为“attention”。

### 2. 为什么要除以 `sqrt(d_k)`

若 `q` 和 `k` 的各维近似独立、均值为 0、方差为 1，则：

```text
Var(q dot k) = d_k
```

`d_k` 越大，未缩放 logits 的方差越大，softmax 更容易饱和。饱和后分布接近 one-hot，很多位置梯度很小。除以 `sqrt(d_k)` 可以让 score 方差回到近似常数尺度，训练更稳定。

### 3. Mask 必须在 softmax 前应用

Causal mask 和 padding mask 都是在约束哪些 key 位置可见。正确做法是把不可见位置的 score 设为 `-inf` 或足够大的负数，再 softmax：

```text
scores = scores.masked_fill(~mask, -inf)
A = softmax(scores)
```

如果先 softmax 再把未来位置乘 0，剩余概率和不再等于 1；如果再手动归一化，还可能在全 mask 行除以 0。作业中的 `combine_causal_padding_mask` 要返回 `[B, T, T]`：query 维度受 causal 约束，key 维度受 padding 约束。padding query 是否参与 loss 是另一个问题，通常由 label mask 或 loss mask 处理。

### 4. Self-attention 的置换等变性

没有位置编码、没有 mask 时，self-attention 对序列顺序没有内建偏好。若 `P` 是位置置换矩阵，则：

```text
Attention(PX) = P Attention(X)
```

这不是说 attention 不处理序列，而是说模型需要位置编码或 mask 才能区分“相同 token 集合的不同顺序”。`self_attention_permutation_error` 用数值实验验证这一点，是理解 Ch02 positional encoding 和 Ch03 attention 的连接点。

### 5. Softmax Jacobian 与 attention 反向传播

对 `p = softmax(z)`，Jacobian 是：

```text
J_ij = p_i (1[i=j] - p_j)
```

它不是对角矩阵，因为一个 logit 变化会影响所有 softmax 概率。对单个 query：

```text
o = p V
```

若上游梯度是 `g = dL/do`，则先有：

```text
dL/dp_i = g dot V_i
```

再通过 softmax Jacobian 得到 `dL/dz`。最后由：

```text
z = Q K^T / sqrt(d_k)
```

得到 Q/K 的梯度；V 的梯度来自 `O = A V`。本作业要求写 `attention_logits_gradient` 和 `attention_qkv_gradients`，目的就是让你看到 attention 不是只会 forward 的模块，而是完整可微计算图。

### 6. Entropy、显存与 heatmap 边界

`attention_entropy` 衡量每个 query 的 attention 分布尖锐程度。低 entropy 表示概率集中，高 entropy 表示更均匀；但它不等于“模型解释”。一个高权重位置可能是语法占位、分隔符、复制路径或 artifact，不一定是人类意义上的因果依据。

Dense attention score 显存主项为：

```text
score_bytes = batch_size * n_heads * seq_len * seq_len * dtype_bytes
```

这是二次项。即使没有保存全部 attention weights，训练反向传播和某些实现仍会受到 `T^2` 的计算/显存压力。这个公式是 Ch04 GQA/MLA、Ch10 FlashAttention 和 KV Cache 成本分析的前置知识。

Heatmap 只适合作为调试和诊断工具：

- 检查 causal mask 是否泄漏未来 token。
- 检查 padding key 是否仍被注意。
- 观察特殊 token、重复 token 或分隔符是否吸走概率。
- 不能仅凭 heatmap 宣称模型“理解了”某个词，也不能替代 ablation、patching 或任务指标。

最终报告应包含一个 shape trace、一个 mask bug 或数值稳定性案例、一个反向传播小推导，以及一个 heatmap 解释边界。这样才能达到课程级 attention 作业的要求。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 推导 `1/sqrt(d_k)` scaling、self-attention 置换等变性、softmax Jacobian、attention logits 到 Q/K/V 的链式法则、attention entropy、mask 加在 softmax 前的原因、causal mask 与 padding mask 的形状广播、复杂度和 heatmap 解释边界 |
| Programming parts | 55 | 实现 QKV projection、scaled dot-product attention、置换等变性数值验证、softmax/attention backward helpers、Q/K/V gradient helper、attention entropy、attention score 显存估算、causal mask、causal+padding mask 合成和 attention visualization |
| Analysis / style | 10 | 解释 mask 数值稳定性、attention heatmap 的适用范围和常见 shape bug |
