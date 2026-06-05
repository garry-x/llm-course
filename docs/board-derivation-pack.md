# Board Derivation and Instructor Notes Pack

本文件补充 [Lecture Notes Index](lecture-notes-index.md)、[Lecture Slide Outline](lecture-slide-outline.md)、[Mathematical Derivation Audit](mathematical-derivation-audit.md) 和 [书面推导与概念题题库](written-problem-set.md)。它给教师和助教提供可直接用于板书、讨论课和评分校准的推导脚本：每个核心结论都包含符号、推导步骤、shape 检查、常见误区、课堂 quick check 和评分证据。

复核日期：2026-06-05

## 符号约定

| 符号 | 含义 |
|------|------|
| `B` | batch size |
| `T` / `L` | sequence length / context length |
| `V` | vocabulary size |
| `D` | model hidden size |
| `H` | attention head count |
| `D_h` | per-head hidden size, usually `D / H` |
| `H_kv` | KV head count for MQA/GQA/MLA-style cache analysis |
| `b` | bytes per scalar for dtype, e.g. FP16 = 2 |
| `x_t` | token at position `t` |
| `q_t, k_t, v_t` | query/key/value vectors |

## 课堂板书脚本

### 1. BPE Merge 不是全局最优压缩

目标：学生能解释 BPE 每步贪心 merge 的局部目标，并说明词表大小、序列长度和多语言覆盖之间的权衡。

推导步骤：

1. 把语料写成字符或 byte 序列，统计所有相邻 pair 的频次。
2. 选择当前频次最高的 pair `(a, b)`，加入新 token `ab`。
3. 重新扫描语料，把非重叠的 `(a, b)` 替换成 `ab`。
4. 每轮只优化当前 pair 的出现次数，不回溯此前 merge。

Shape / 复杂度：

- 输入是一批 token 序列；merge 后序列长度通常下降，但词表大小上升。
- 朴素实现每轮重新统计 pair，复杂度约为 `O(num_merges * corpus_tokens)`；工程实现会用更高效的计数更新。

常见误区：

- “BPE 总能找到最短编码”是错的；它是贪心近似。
- byte-level BPE 通常避免 OOV，但不意味着所有语言的 token 成本相同。

Quick check：给 `low lower newest widest`，让学生手算前 2 轮 merge，并解释为什么第二轮需要重新统计。

评分证据：Ch01 BPE tests、书面题 Ch01、reading recap 中的多语言 token 成本分析。

### 2. Embedding Lookup 等价于 One-Hot 矩阵乘法

目标：学生能从线性代数解释 `nn.Embedding`，并理解 embedding 参数量。

推导步骤：

1. 设 embedding matrix `E in R^{V x D}`。
2. token id `i` 对应 one-hot 向量 `e_i in R^V`。
3. `e_i^T E` 只取出 `E` 的第 `i` 行，因此等价于 `E[i]`。
4. 对 batch 序列 `input_ids in Z^{B x T}`，输出 shape 是 `[B, T, D]`。

常见误区：

- embedding lookup 不是不可微操作；被查到的行会收到梯度。
- 类比推理是训练后向量空间里的经验结构，不是训练目标直接保证的线性规则。

Quick check：如果 `V=50,000, D=768`，embedding 参数量是多少？若 tied LM head 会减少哪部分参数？

评分证据：Ch02 embedding tests、Ch06 weight tying tests、书面题 Ch02。

### 3. Sinusoidal / RoPE 的相对位置结构

目标：学生能证明 RoPE 点积只依赖相对位移，并知道长上下文外推不是自动保证。

推导步骤：

1. 把每两个维度看成一个 2D block。
2. 位置 `m` 对 query 做旋转：`q'_m = R_m q`；位置 `n` 对 key 做旋转：`k'_n = R_n k`。
3. 点积：

```text
(R_m q)^T (R_n k)
= q^T R_m^T R_n k
= q^T R_{n-m} k
```

4. 关键是旋转矩阵的群性质：`R_m^T = R_{-m}`，`R_{-m} R_n = R_{n-m}`。

Shape 检查：

- 输入 `[B, H, T, D_h]`。
- RoPE 只作用在最后一维的成对 channel 上；`D_h` 必须能按 2D block 配对。

常见误区：

- RoPE 是位置相关的线性正交变换，不是非线性函数。
- “只依赖相对位移”不等于任意长度都能稳定外推；训练长度、频率设计、数值范围和注意力模式都会影响表现。

Quick check：为什么 `R_m^T R_n` 而不是 `R_m R_n`？让学生写出转置来自哪个点积步骤。

评分证据：Ch02 RoPE tests、书面题 Ch02、Ch04 MLA/RoPE 边界说明。

### 4. Attention Scaling: `Var(q^T k)=D_h`

目标：学生能推导 `sqrt(D_h)` 缩放来自方差控制，而不是经验魔法数。

推导步骤：

1. 假设 `q_i` 和 `k_i` 独立，均值 0，方差 1。
2. `q^T k = sum_i q_i k_i`。
3. `E[q_i k_i] = 0`。
4. `Var(q_i k_i) = E[q_i^2]E[k_i^2] = 1`。
5. 独立求和：`Var(q^T k)=D_h`。
6. 除以 `sqrt(D_h)` 后，score 方差约为 1，softmax 不易过早饱和。

Shape 检查：

- `Q: [B,H,T,D_h]`
- `K^T: [B,H,D_h,T]`
- score: `[B,H,T,T]`

常见误区：

- scaling 必须在 softmax 前。
- mask 应在 softmax 前加到 logits 上，而不是 softmax 后把概率置零。

Quick check：如果 `D_h=128`，未缩放 score 的标准差约是多少？这会怎样影响 softmax？

评分证据：Ch03 attention tests、书面题 Ch03、L3/L4 quick check。

### 5. Causal Mask 的 Logit 级应用

目标：学生能解释未来 token 泄露和 mask broadcast。

推导步骤：

1. causal score matrix 是 `[T,T]`，第 `i` 行只能看 `j <= i`。
2. 把不可见位置加上 `-inf` 或极大负数。
3. 对最后一维做 softmax，未来位置概率变为 0。
4. 如果 softmax 后再 mask，剩余概率和不再等于 1，除非重新归一化；这会改变 attention 语义。

常见误区：

- `[T,T]` mask broadcast 到 `[B,H,T,T]` 时，batch/head 维不能错放。
- padding mask 和 causal mask 可以组合，但含义不同。

Quick check：三 token 序列中，第 2 个位置可见哪些列？第 1 行 softmax 后再 mask 会发生什么？

评分证据：Ch03 causal mask tests、discussion failure drill。

### 6. MHA / GQA / MLA 的参数与 KV Cache 区分

目标：学生能区分参数量、计算量和 cache 显存。

推导步骤：

1. 标准 MHA 的 Q/K/V/O 投影参数量约为 `4D^2`。
2. GQA 减少的是 KV head 数，不一定减少 Q head 数。
3. 每层 KV cache 元素数：

```text
2 * B * T * H_kv * D_h
```

其中 `2` 表示 K 和 V。
4. MLA 把缓存内容压到 latent 表示；教学实现只保留 latent cache 的核心思想，不代表生产模型完整细节。

常见误区：

- head 数增加不必然提升质量。
- KV cache 少不等于 attention 计算免费。
- RoPE 与 MLA 的固定解压矩阵一般不能简单交换或统一吸收。

Quick check：`B=4, T=8192, layers=32, H_kv=8, D_h=128, FP16` 的 KV cache 大约多少 GB？

评分证据：Ch04 GQA/MLA tests、Ch10 KV cache tests、书面题 Ch04/Ch10。

### 7. LayerNorm / RMSNorm 的依赖关系

目标：学生能说明归一化的维度和反向传播依赖。

推导步骤：

1. 对最后一维 `D` 计算均值 `mu` 和方差 `sigma^2`。
2. `x_hat = (x - mu) / sqrt(sigma^2 + eps)`。
3. 输出 `y = gamma * x_hat + beta`。
4. 反向传播中 `mu` 和 `sigma^2` 都依赖 `x`，不能当常数。
5. RMSNorm 去掉中心化，只用 root mean square 缩放。

常见误区：

- LayerNorm 不是 BatchNorm；它通常不跨 batch 统计。
- Pre-norm 更利于深层训练稳定，但不是唯一正确结构。

Quick check：输入 `[B,T,D]` 时 LayerNorm 的 `normalized_shape` 应是什么？

评分证据：Ch05 gradcheck、RMSNorm tests、书面题 Ch05。

### 8. Next-Token NLL / Cross Entropy

目标：学生能从自回归分解推导 next-token loss，并处理 `ignore_index`。

推导步骤：

1. 自回归分解：

```text
p(x_1,...,x_T) = product_t p(x_t | x_<t)
```

2. 最大化 log likelihood 等价于最小化：

```text
- sum_t log p(x_t | x_<t)
```

3. 对 vocab logits 做 softmax 后，单 token loss 是 cross entropy。
4. 对 logits 的梯度是 `p_i - 1[i=y]`。
5. `ignore_index` 必须在 gather / indexing 前处理，否则非法 label 会越界。

常见误区：

- labels 需要右移；模型在位置 `t` 预测 `t+1`。
- perplexity 是平均 NLL 的指数，不等于事实正确率。

Quick check：为什么 padding token 不应计入 loss？如果先 gather 再 mask 会出什么错？

评分证据：Ch07 CE tests、training capstone loss log、书面题 Ch07。

### 9. AdamW 与 Adam + L2 的区别

目标：学生能说明 decoupled weight decay 为什么不是普通 L2 penalty。

推导步骤：

1. Adam 用一阶/二阶矩估计更新梯度方向。
2. 若把 L2 penalty 加进 gradient，正则项也会经过 Adam 的自适应缩放。
3. AdamW 把 weight decay 从 gradient update 中解耦：

```text
theta <- theta - lr * adam_update
theta <- theta - lr * weight_decay * theta
```

4. 这样 weight decay 的含义更接近直接缩小参数。

常见误区：

- weight decay、learning rate schedule、gradient clipping 是三件事。
- warmup/cosine 的收益依赖模型规模、batch、optimizer 和训练时长。

Quick check：同样的 `weight_decay=0.1`，Adam + L2 和 AdamW 为什么可能更新方向不同？

评分证据：Ch07 AdamW tests、training capstone plan。

### 10. DPO Log-Ratio 的方向

目标：学生能判断 chosen/rejected 写反会优化相反目标。

推导步骤：

1. 对 chosen 和 rejected response 分别计算 sequence log prob。
2. 策略模型 log-ratio：

```text
log pi(y_chosen|x) - log pi(y_rejected|x)
```

3. reference 模型 log-ratio 用同样方向计算。
4. DPO 优化的是策略相对 reference 更偏向 chosen 的程度。
5. 若 chosen/rejected 方向写反，loss 会奖励错误 response。

常见误区：

- DPO 不是“只提高 chosen 概率”；它比较 chosen/rejected，并带 reference 约束。
- reference model 不是可选装饰，缺失它会改变目标。

Quick check：给两组 log prob，让学生手算 policy ratio、reference ratio 和 preference margin。

评分证据：Ch09 DPO tests、书面题 Ch09。

### 11. GRPO Group Advantage Whitening

目标：学生能解释 group-relative advantage 的来源和边界。

推导步骤：

1. 对同一 prompt 采样一组 responses。
2. 每个 response 得到 reward。
3. 在组内计算均值和标准差。
4. advantage:

```text
A_i = (r_i - mean(r_group)) / (std(r_group) + eps)
```

5. 组内白化降低 reward scale 对更新的影响。

常见误区：

- GRPO 是 DeepSeek-R1 报告中的强化学习方案，不是完整安全对齐方案。
- reward 设计决定了优化方向；奖励函数错误会系统性放大问题。

Quick check：如果同组 reward 全相同，advantage 应如何处理？为什么要加 `eps`？

评分证据：Ch09 GRPO tests、frontier-source-audit、书面题 Ch09。

### 12. KV Cache 显存公式

目标：学生能从 shape 推导 KV cache 显存，并区分权重显存和缓存显存。

推导步骤：

1. 每层 K cache shape: `[B, H_kv, T, D_h]`。
2. 每层 V cache shape 相同。
3. 每层元素数：`2 * B * H_kv * T * D_h`。
4. 全模型乘以 `layers` 和 dtype bytes：

```text
memory_bytes = 2 * B * layers * H_kv * T * D_h * b
```

5. 工程估算还要加权重、activation peak、allocator fragmentation、runtime overhead 和安全余量。

常见误区：

- KV cache 随 batch 和 context 线性增长。
- 量化权重不一定等于量化 KV cache。
- 平均延迟不能代表 SLO；需要 P95/P99、TTFT、TPOT、error rate。

Quick check：`B` 翻倍和 `T` 翻倍分别如何影响 cache？GQA 减少的是哪个变量？

评分证据：Ch10 KV cache tests、inference capstone capacity plan、书面题 Ch10。

## 20 讲 Quick Check 对照

| 讲次 | 课堂检查问题 | 最低合格答案 |
|------|--------------|--------------|
| L1 | BPE 为什么不能保证全局最优？ | 每步只选当前最高频 pair，不回溯 |
| L2 | RoPE 点积推导的关键矩阵等式是什么？ | `R_m^T R_n = R_{n-m}` |
| L3 | Attention scaling 除以什么？为什么？ | `sqrt(D_h)`；控制 score 方差 |
| L4 | Mask 应在 softmax 前还是后？ | 前；否则概率语义被破坏 |
| L5 | GQA 减少的是 Q head 还是 KV head？ | KV head |
| L6 | LayerNorm 反向传播为什么不能把均值当常数？ | 均值/方差依赖输入 |
| L7 | labels 为什么右移？ | 位置 `t` 预测 `t+1` |
| L8 | 激活参数少为什么不等于服务成本线性下降？ | routing、通信、capacity、cache 和 kernel 仍有成本 |
| L9 | AdamW 与 Adam+L2 的关键区别？ | weight decay 与自适应梯度更新解耦 |
| L10 | checkpoint/resume 最少要保存什么？ | model、optimizer、scheduler、step、config/seed |
| L11 | top-p 的候选数是否固定？ | 不固定，取累计概率达到阈值的最小集合 |
| L12 | 推测解码何时可能不加速？ | 接受率低、draft 慢、瓶颈不在 decode |
| L13 | LoRA 初始输出为何应接近 base？ | 常见初始化使低秩增量初始接近 0 |
| L14 | DPO chosen/rejected 写反会怎样？ | 优化相反偏好 |
| L15 | BLEU/ROUGE 能否证明开放式回答正确？ | 不能，只是特定自动指标 |
| L16 | 数据污染为什么影响 benchmark？ | 评测样本泄漏会夸大泛化能力 |
| L17 | KV cache 公式中的 `2` 来自哪里？ | K 和 V 两份缓存 |
| L18 | 为什么平均延迟不够？ | SLO 需要尾延迟和错误率 |
| L19 | 复现包缺 seed 会怎样？ | 难以复核训练和评测波动 |
| L20 | 前沿模型数字如何进入报告？ | 标注来源、日期、任务设置和边界 |

## 评分使用规则

- 书面题评分优先看推导链条、shape 和边界条件，不只看最终结论。
- 课堂 quick check 不建议单独高权重计分；用于决定 recap、discussion drill 和 office-hour 优先级。
- 助教批改前应抽取 2-3 个本文件中的推导作为校准样例，记录在 [Grading Calibration Guide](grading-calibration.md) 或 [Course Operations and Improvement Log](course-operations-log.md)。
- 若章节、作业测试或前沿来源变更，本文件对应推导也必须同步复核。

## 发布前 Checklist

| 检查项 | 通过标准 |
|--------|----------|
| 核心推导 | 覆盖 BPE、Embedding、RoPE、attention scaling、mask、MHA/GQA/MLA、Norm、CE、AdamW、DPO、GRPO、KV cache |
| Shape 证据 | 每个张量推导至少说明一个关键 shape 或复杂度 |
| 误区边界 | 每个脚本至少列出一个常见误区或适用边界 |
| Quick check | L1-L20 均有可在课堂 3-8 分钟完成的问题 |
| 评分衔接 | 每个核心推导能映射到作业、书面题、capstone 或 reading recap |
