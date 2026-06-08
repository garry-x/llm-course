# Ch02 Embedding 与位置编码作业测试

本目录把第 2 章的编程练习整理成可自动验收的作业入口，覆盖 TokenEmbedding、one-hot 矩阵乘法形式的 embedding lookup、word vector 共现统计、skip-gram negative sampling、SGNS 中心向量梯度、shifted PMI、GloVe 加权最小二乘目标、cosine similarity、3CosAdd 类比、SinusoidalEncoding、RoPE 以及 RoPE 相对位置性质验证。

## 文件说明

| 文件 | 用途 |
|------|------|
| `starter.py` | 学生起始代码，包含需要实现的 TODO |
| `reference_solution.py` | 教师参考实现，用于验证测试本身 |
| `tests.py` | `unittest` 测试，覆盖 shape、one-hot lookup 等价性、共现计数、SGNS loss、SGNS center gradient、shifted PMI、GloVe loss、cosine similarity、3CosAdd、buffer、范数保持和相对位置性质 |

## 学生运行方式

```bash
cp assignments/ch02_embeddings/starter.py assignments/ch02_embeddings/student_solution.py
# 编辑 student_solution.py 完成 TODO
STUDENT_MODULE=student_solution .venv/bin/python assignments/ch02_embeddings/tests.py
```

也可以直接让测试加载 `starter.py`：

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch02_embeddings/tests.py
```

也可以直接验证课程内置参考实现：

```bash
.venv/bin/python assignments/ch02_embeddings/tests.py
```

## Conceptual Handout

本作业连接两件事：文本 token 如何进入神经网络，以及模型如何知道 token 的相对/绝对位置。完成代码只是第一步；报告需要解释为什么 embedding lookup 等价于 one-hot 矩阵乘法，为什么 word vectors 能从共现统计中学到语义结构，以及 RoPE 为什么让 attention score 依赖相对位置。

### 1. Embedding lookup 是参数矩阵索引

设词表大小为 `V`，隐藏维度为 `D`，embedding matrix 为 `E in R^{V x D}`。一个 token id `i` 的 one-hot 向量 `e_i` 满足：

```text
embedding(i) = e_i @ E = E[i]
```

所以 embedding lookup 不是 magic table，而是一个可训练矩阵的行选择。`TokenEmbedding` 输出 shape 应为 `[B, T, D]`，参数量是 `V * D`。本作业要求把 lookup 显式写成 one-hot matmul，是为了让学生理解：

- token id 本身没有连续意义，连续表示来自被索引的参数行。
- 词表越大，embedding 和 tied LM head 参数越多。
- tokenizer 改变 token 数和 token id 分布，会改变训练样本、上下文长度和 embedding 更新频率。
- 乘以 `sqrt(d_model)` 是 Transformer 早期实现中的尺度处理，目的是让 embedding 与 positional encoding 的数值尺度更可控。

### 2. 共现统计、SGNS 与 shifted PMI

Word vectors 的经典思想是 distributional hypothesis：出现在相似上下文中的词倾向有相似语义。`build_cooccurrence_matrix` 使用固定窗口统计 center->context 的有向共现。窗口大小、方向和边界处理都会改变矩阵，因此报告中要写清楚你统计的对象。

Skip-gram with negative sampling 对一个 center、一个 positive context 和若干 negative contexts 的目标可以写成：

```text
L = -log sigmoid(v_c dot u_pos) - sum_k log sigmoid(-v_c dot u_neg_k)
```

它推动 center vector 靠近正样本 context，远离负样本 context。对 center vector 的梯度方向应能解释为：

```text
dL/dv_c = (sigmoid(v_c dot u_pos)-1) u_pos
          + sum_k sigmoid(v_c dot u_neg_k) u_neg_k
```

在理想化假设下，SGNS 与矩阵分解有联系：模型隐式逼近 `PMI(i,j) - log(k)`，其中 `k` 是 negative samples 数。`shifted_pmi_matrix` 让你把这个关系写成可计算矩阵。注意 PMI 对低频共现很敏感；零共现位置不是有限大负数，而应被视为未观测或 `-inf`。

### 3. GloVe 是加权最小二乘，不是同一个 loss

GloVe 直接拟合共现计数的对数：

```text
J = sum_{i,j} f(X_ij) * (w_i dot wtilde_j + b_i + btilde_j - log X_ij)^2
```

权重函数 `f(X_ij)` 降低低频噪声和超高频项的影响。与 SGNS 相比，GloVe 更显式地使用全局共现矩阵；SGNS 更像从局部窗口样本和负采样构造分类目标。报告中比较两者时，应说明数据来源、目标函数、负样本/权重处理和对低频词的影响，而不是只写“都学词向量”。

### 4. Cosine similarity 与 3CosAdd 的边界

Cosine similarity 只比较方向，不比较向量长度。3CosAdd 类比使用：

```text
query = v_b - v_a + v_c
```

然后找 cosine similarity 最高的词，并排除输入词 `a,b,c`。这个方法能在某些词向量空间里得到 `man:king :: woman:queen` 之类结果，但它不是训练目标直接保证的。报告中应包含至少一个 failure case，例如：

- 多义词：`apple` 是水果还是公司。
- 性别/职业偏见：类比可能放大语料偏见。
- 低频词：向量不稳定，cosine 排名噪声大。
- 子词 tokenizer 下，一个词可能被拆成多个 token，word-level analogy 不再直接适用。

### 5. Sinusoidal encoding 与 RoPE

固定 sinusoidal encoding 给每个绝对位置一个确定向量，直接加到 token embedding 上。它没有训练参数，应注册为 buffer 而不是 parameter；这也是测试检查 `named_buffers()` 的原因。

RoPE 不把位置向量相加，而是把 Q/K 的偶数维成对旋转。对二维子空间，位置 `m` 的旋转矩阵为 `R_m`，两个位置 `m,n` 的点积满足：

```text
(R_m q)^T (R_n k) = q^T R_{n-m} k
```

因此 attention score 能自然依赖相对距离 `n-m`。实现时要注意：

- head dimension 必须是偶数，才能成对旋转。
- `cos/sin` 的 shape 要能广播到 `[B, H, T, D]` 或课程约定的 Q/K shape。
- RoPE 通常只作用于 Q/K，不作用于 V。
- dtype/device 要随输入迁移，否则 GPU 或 mixed precision 下会出错。
- 超过训练长度外推时，频率设计、base、缩放策略和上下文分布都会影响稳定性。

最终报告应把 Ch01 的 tokenizer 成本、Ch02 的 embedding 参数量和 RoPE 的上下文建模联系起来：同一段文本被切成更多 token，不仅增加 embedding lookup 次数，也增加 attention 长度、KV Cache 和位置编码外推压力。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 推导 embedding 参数量，解释 one-hot 与 lookup 等价性，比较 word2vec/GloVe 的统计目标，推导 SGNS 正负样本对中心向量的梯度、PMI/shifted PMI，计算 cosine similarity 与 3CosAdd 类比，证明 self-attention 的置换等变性，推导 RoPE 点积依赖相对位置 |
| Programming parts | 55 | 实现 `TokenEmbedding`、`embedding_lookup_as_matmul`、共现矩阵、SGNS loss、SGNS center gradient、shifted PMI、GloVe weighted loss、cosine similarity、3CosAdd、`SinusoidalEncoding`、`RoPE` 和相对位置数值验证 |
| Analysis / style | 10 | 说明 RoPE 外推失败模式、odd head dimension 拒绝策略和 dtype/device 迁移 |
