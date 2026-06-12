# 数学与 PyTorch 先修复习

本附录汇总高校课程中常见的线性代数、概率、反向传播和张量求导前置知识。它不是独立数学课，而是服务于每章的实现、推导和代码分析；遇到章节内的 shape、mask、loss 或梯度问题时再回来查阅。微积分、统计和机器学习基础到本课程项目产出的桥接见 [ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md)。

## 全课程符号与 Shape 约定

为了避免每章重复解释符号，本课程默认使用以下约定。若某一章采用不同符号，会在该章局部说明。

| 符号 | 含义 | 常见 shape 或单位 |
|------|------|------------------|
| `B` | batch size | 标量 |
| `T` | query 序列长度或当前输入长度 | 标量 |
| `S` | key/value 序列长度，可能与 `T` 不同 | 标量 |
| `V` | vocabulary size | 标量 |
| `d_model` | residual stream hidden size | 标量 |
| `H` | query attention heads | 标量 |
| `H_kv` | KV heads，GQA/MQA 中可小于 `H` | 标量 |
| `D` / `d_head` | 每个 head 的维度 | `d_model / H` |
| `N` | 参数量或训练样本数，按上下文区分 | count |
| `M` | MoE expert 数或矩阵行数，按上下文区分 | count |
| `input_ids` | token id 序列 | `[B, T]` |
| `embedding_weight` | token embedding table | `[V, d_model]` |
| `hidden_states` | residual stream | `[B, T, d_model]` |
| `logits` | 词表未归一化分数 | `[B, T, V]` |
| `labels` | 目标 token ids，可能含 `ignore_index=-100` | `[B, T]` |
| `Q` | query states | `[B, H, T, D]` |
| `K, V_attn` | key/value states | `[B, H_kv, S, D]` 或重复后 `[B, H, S, D]` |
| `attention_scores` | scaled dot-product logits | `[B, H, T, S]` |
| `attention_mask` | `True` 表示可见，`False` 表示屏蔽 | 可广播到 `[B, H, T, S]` |

两个容易混淆的字母：

- `V` 在 embedding/LM head 中通常表示 vocab size；在 attention 中 `V_attn` 表示 value tensor。代码里应避免把它们写成同一个变量名。
- `D` 在 attention 公式中常表示 `d_head`，在训练 scaling law 中也可能表示训练 token budget。书面推导必须先定义。

## 核心张量流

decoder-only LLM 的最小前向路径是：

```text
input_ids [B,T]
  -> token embeddings [B,T,d_model]
  -> Transformer blocks [B,T,d_model]
  -> lm_head logits [B,T,V]
  -> shifted CE loss against labels [B,T]
```

next-token loss 的对齐关系是：

```text
logits[:, t, :] predicts input_ids[:, t+1]
shift_logits = logits[:, :-1, :]
shift_labels = labels[:, 1:]
```

因此，如果一个 batch 的序列长度是 `T`，最多只有 `T-1` 个 next-token 监督位置。SFT、padding 和 prompt mask 会进一步通过 `ignore_index=-100` 移除无效位置，mean reduction 的分母应是有效 token 数，而不是 `B*T`。

## Mask 语义

本课程默认 mask 在 softmax 或 loss 前应用：

| 场景 | mask 作用 | 常见错误 |
|------|-----------|----------|
| Causal attention | 屏蔽未来 key | softmax 后再乘 mask，导致概率和不为 1 |
| Padding attention | 屏蔽 padding key | 只屏蔽 padded query，仍让真实 token attend 到 padding key |
| SFT / causal LM labels | `-100` 位置不参与 loss | gather 前直接用 `-100` 做索引 |
| MLM labels | 只在 masked positions 上计算 CE | 把未 mask token 也放进平均分母 |
| Constrained decoding | 非法 token logits 置为 `-inf` | 采样后再过滤，破坏概率语义 |

## 常用目标函数与评测对象

| 名称 | 公式或计算对象 | 回答的问题 | 不回答的问题 |
|------|----------------|------------|--------------|
| Causal LM CE | `-mean log p(x_t | x_<t)` | 模型是否拟合 next-token 分布 | 回答是否真实、有用、安全 |
| Perplexity | `exp(CE)` | 平均 token 预测难度 | 开放式任务质量 |
| SFT loss | 只对 assistant response 的 shifted labels 做 CE | 模型是否学习回答格式和示例行为 | 偏好质量或安全边界 |
| DPO loss | policy/reference chosen-rejected log-ratio | policy 是否相对 reference 提升 chosen | 偏好数据是否无偏 |
| PPO/GRPO surrogate | policy ratio、advantage、clip/KL | 策略更新是否朝 reward 方向且受约束 | reward 是否代表真实质量 |
| Recall@k / MRR / nDCG | 检索排序与相关标签 | RAG 是否找到相关证据 | 生成是否忠实使用证据 |
| BLEU / ROUGE | n-gram 或 LCS 重合 | 输出与参考文本的词面重合 | 事实一致性或语义等价 |
| EM / token F1 | 标准化答案或 token overlap | 抽取式 QA 的短答案匹配 | 多答案开放式质量 |
| Span F1 | `(type,start,end)` 精确实体匹配 | NER/entity extraction 边界和类型 | token-level 部分正确性 |
| TTFT / TPOT / tokens/s | 服务延迟与吞吐 | 用户等待、生成速度和容量成本 | 语义质量 |

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
- `Cross entropy`: 有效 token 的 logits 梯度是 `softmax(z)-one_hot(y)`；被 `ignore_index` 屏蔽的位置不进入平均，也不向 logits 传梯度。

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
