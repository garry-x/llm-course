# Ch04 多头注意力 / GQA / MLA 作业测试

本目录把第 4 章的编程练习整理成可自动验收的作业入口，覆盖 MHA、单头参数等价性、GQA KV head 重复、GQA head mapping、简化版 MLA、MLA 矩阵吸收等价性、KV Cache 大小计算和跨层显存预算。

## 文件说明

| 文件 | 用途 |
|------|------|
| `starter.py` | 学生起始代码，包含需要实现的 TODO |
| `reference_solution.py` | 教师参考实现，用于验证测试本身 |
| `tests.py` | `unittest` 测试，覆盖 shape、mask、参数量、KV head repeat、GQA head mapping、MLA latent score 等价性、cache 压缩比和 batch/layer/dtype 显存预算 |

## 学生运行方式

```bash
cp assignments/ch04_multihead/starter.py assignments/ch04_multihead/student_solution.py
# 编辑 student_solution.py 完成 TODO
STUDENT_MODULE=student_solution .venv/bin/python assignments/ch04_multihead/tests.py
```

也可以直接让测试加载 `starter.py`：

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch04_multihead/tests.py
```

也可以直接验证课程内置参考实现：

```bash
.venv/bin/python assignments/ch04_multihead/tests.py
```

## Conceptual Handout

Ch04 的目标是把 Ch03 的单头 attention 扩展到真实 LLM 使用的多头结构，并把架构选择连接到推理显存。MHA、MQA、GQA 和 MLA 的差异不只是“head 数不同”，而是 Q/K/V 投影、KV Cache 保存内容、RoPE 处理和 serving 成本都不同。

### 1. Multi-head attention 的参数和 shape

标准 MHA 把 `d_model` 切成 `n_heads` 个 head，每个 head 维度：

```text
d_head = d_model / n_heads
```

常见实现不是给每个 head 单独建一套小矩阵，而是用一个大线性层一次性投影，再 reshape 到 `[B, H, T, D_head]`。若 Q/K/V/O 都是 bias-free `d_model x d_model`，参数量主项为：

```text
params_mha = 4 * d_model^2
```

这解释了为什么“多头”通常不会让参数量乘以 head 数；它改变的是表示分组和 attention 子空间，而不是简单复制整个模型。

### 2. MQA/GQA 的核心是减少 KV heads

推理时，每层每个请求都要缓存历史 K/V。标准 MHA 保存 `n_heads` 份 K 和 `n_heads` 份 V；MQA/GQA 让多个 query heads 共享更少的 KV heads。GQA 的 head mapping 可写成：

```text
kv_head = query_head // (n_heads / n_kv_heads)
```

例如 `n_heads=8, n_kv_heads=2` 时，Q heads `[0,1,2,3]` 使用 KV head 0，Q heads `[4,5,6,7]` 使用 KV head 1。`repeat_kv_heads` 在计算 attention 时把 `[B, H_kv, T, D]` 重复到 `[B, H_q, T, D]`，但 KV Cache 只需要保存 `H_kv` 份。

这带来一个重要区分：

- GQA 减少的是推理 KV Cache 和 K/V 投影计算/存储压力。
- GQA 不减少 Q heads 数，也不自动减少所有参数量。
- KV sharing 可能损失部分 head-specific 表达能力，通常需要训练或从 MHA checkpoint 转换后微调。

### 3. KV Cache 显存预算必须乘上 batch 和 layers

单 token、单层的 KV 元素数是：

```text
kv_elements_per_token_per_layer = 2 * n_kv_heads * d_head
```

完整服务预算必须写成：

```text
kv_bytes = batch_size * n_layers * seq_len * 2 * n_kv_heads * d_head * dtype_bytes
```

`compare_kv_cache_budget` 的意义是让学生比较：

- MHA：`n_kv_heads = n_heads`
- MQA：`n_kv_heads = 1`
- GQA：`1 < n_kv_heads < n_heads`
- MLA：缓存低维 latent 或压缩后的表示

报告中不能只写压缩比，还要写具体 batch、layers、seq_len、dtype。长上下文服务里，KV Cache 常常比 attention score heatmap 更接近真实 serving bottleneck。

### 4. MLA 的 latent cache 和矩阵吸收

MLA 的核心动机是把 K/V 信息压进低维 latent cache，再在计算时恢复或等价变换。作业中的简化 MLA 重点检查一个数学事实：若 K 是由 latent 表示乘上解压矩阵得到，

```text
K = C W_up
score = Q K^T
```

则可以把矩阵乘法重排为：

```text
score = Q W_up^T C^T
```

也就是先把 Q 投到 latent-compatible 空间，再和 cached latent 做点积，不必显式 materialize 完整 K。这个 `mla_absorbed_attention_scores` 是理解 MLA 工程收益的关键。

但 MLA 不是“免费压缩”：

- latent 维度太小会限制表达。
- RoPE 与低维 latent cache 的结合更复杂，不能简单套标准 RoPE。
- 实际实现要考虑 kernel、layout、prefill/decode 分离和模型训练方式。
- 课程作业是简化版，用来理解矩阵等价和 cache 预算，不等同于完整 DeepSeek MLA。

### 5. 报告应回答的工程问题

一个合格 Ch04 报告至少回答：

- 给定 `d_model, n_heads, n_kv_heads, seq_len, batch_size, n_layers, dtype_bytes`，MHA/GQA/MLA 的 KV Cache 各是多少？
- GQA head mapping 是否正确？每个 KV head 被多少 Q heads 共享？
- MQA/GQA 减少显存后，可能在哪些任务或 head 行为上损失能力？
- MLA absorbed score 的矩阵维度是否一致，为什么它能避免显式解压 K？
- mask 在 `[B,H,T,T]` 或可广播 shape 下如何作用到每个 head？

最终结论要把 Ch04 和 Ch10 连起来：GQA/MLA 的架构选择会改变 active KV tokens 的容量上限、长上下文请求的 admission limit 和服务端每个 batch 能承载的请求数量。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 计算 MHA 参数量，比较 MHA/MQA/GQA/MLA 的 KV cache，写出 Q head 到 KV head 的映射，推导 MLA 的 K 解压矩阵吸收等价式，解释 head redundancy、RoPE 与 latent cache 的边界，并能把 batch/layers/dtype 纳入显存预算 |
| Programming parts | 55 | 实现 MHA、单头对照、`repeat_kv_heads`、GQA、GQA head mapping、简化 MLA、MLA absorbed scores、KV cache 分析和跨层显存预算 |
| Analysis / style | 10 | 说明 head grouping、head redundancy、latent cache、mask broadcast 和实现复杂度取舍 |
