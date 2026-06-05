# Lecture Note Sample Pack

本文件提供可直接给学生阅读的 lecture note 样例，用于说明正式 notes 应如何把 learning goals、notation、derivation、shape checks、code binding、source boundary、quick check 和 post-lecture evidence 放在同一份讲义里。它补充 [Lecture Notes Index](lecture-notes-index.md)、[Lecture Notes Quality and Review Standard](lecture-notes-quality-review.md)、[Lecture Notes Review Ledger](lecture-notes-review-ledger.md)、[Lecture Slide Sample Pack](lecture-slide-sample-pack.md)、[Notation and Shape Glossary](notation-shape-glossary.md)、[Worked Example Pack](worked-example-pack.md)、[Mathematical Derivation Audit](mathematical-derivation-audit.md)、[Board Derivation and Instructor Notes Pack](board-derivation-pack.md) 和 [Paper Recap Calibration Pack](paper-recap-calibration-pack.md)。

复核日期：2026-06-05
适用范围：L1-L20 正式 notes 写作、TA discussion recap、学生复盘样例和替代文字材料。
使用原则：样例不是替代 20 讲正文；它定义 notes 的质量形状。新增正式 notes 时，应至少达到本文件四个样例的结构完整度。

## Sample Packet Rubric

| Field | Required evidence |
|-------|-------------------|
| Learning goals | 2-4 条可测目标，能映射到作业、书面题或 capstone |
| Notation ledger | 写清核心符号、shape、单位或 metric |
| Core derivation | 有中间步骤、假设和不能外推的边界 |
| Shape checks | 至少一个输入/输出、mask、cache 或 metric shape |
| Code binding | 指向 assignment test、demo command、capstone module 或 verifier |
| Common misconceptions | 至少 2 个常见错误或错误表述 |
| Source boundary | 区分论文事实、课程解释、模型卡/benchmark 条件 |
| Accessibility notes | 说明图、公式、板书或 demo 的文字替代 |
| Quick check | 一道课堂或课后可评分小题 |
| Post-lecture evidence | 学生提交或 TA 检查的证据 |

## Sample L1: Tokenization and BPE

Status: ready
Mapped materials: Ch01, `assignments/ch01_bpe/`, [Reading List Week 1](reading-list.md), DER-01.

Learning goals:

- Explain why byte-level BPE reduces unknown-character failures without guaranteeing equal token cost across languages.
- Trace one BPE merge round from pair counts to updated token sequences.
- Distinguish local greedy compression from global optimality.

Notation ledger:

| Symbol | Meaning |
|--------|---------|
| `V` | target vocabulary size |
| `N` | current corpus token count |
| `(a,b)` | adjacent token pair |
| `freq(a,b)` | count after the current corpus segmentation |

Core derivation:

1. Start from byte or character tokens.
2. Count adjacent pairs under the current segmentation.
3. Select the highest-frequency pair `(a,b)`.
4. Replace non-overlapping occurrences of `(a,b)` with a new token `ab`.
5. Recount pairs before the next merge.

The derivation supports a local compression heuristic: if `(a,b)` occurs many times, replacing it can reduce current sequence length. It does not prove that the final vocabulary is globally shortest or semantically optimal.

Shape checks:

- Input: list of token-id sequences.
- Output after one merge: list of token-id sequences with length usually lower but not guaranteed for every example.
- Vocabulary size increases by one per accepted merge.

Code binding:

- `assignments/ch01_bpe/tests.py` checks adjacent pair counting, non-overlapping merge, round trip decode, CJK/ASCII handling and invalid vocab size.
- Verification command: `.venv/bin/python assignments/ch01_bpe/tests.py`.

Common misconceptions:

- “BPE finds the optimal tokenizer” is too strong.
- “byte-level means every language has the same token cost” is false.

Source boundary:

- Sennrich et al. supports subword units for rare word handling.
- GPT-2/tiktoken style byte-level implementations support reversibility in practice.
- Course discussion about multilingual cost is an engineering implication and must be measured on a corpus.

Accessibility notes:

- Pair-count examples should be provided as text tables, not only board marks.
- If showing colored merge highlights, include token strings and merge numbers.

Quick check:

Given `low lower newest widest`, compute the first merge if `lo` and `es` tie. State the tie-breaking policy before scoring.

Post-lecture evidence:

- Public Ch01 tests.
- A short reading recap explaining one tokenizer failure case.
- Written answer that states why greedy merge is not a global optimum proof.

## Sample L3: Scaled Dot-Product Attention

Status: ready
Mapped materials: Ch03, `assignments/ch03_attention/`, [Mathematical Derivation Audit](mathematical-derivation-audit.md) DER-04 and DER-05.

Learning goals:

- Derive the `sqrt(d_k)` scaling from variance assumptions.
- Identify the shape of score, mask, probability and context tensors.
- Explain why causal mask is applied at the logit level before softmax.

Notation ledger:

| Symbol | Meaning |
|--------|---------|
| `B` | batch size |
| `H` | number of attention heads |
| `T` | sequence length |
| `D_h` | per-head dimension |
| `Q,K,V` | query, key and value tensors |

Core derivation:

Assume `q_i` and `k_i` are independent, zero-mean and unit-variance. Then:

```text
q^T k = sum_i q_i k_i
E[q_i k_i] = 0
Var(q_i k_i) = E[q_i^2]E[k_i^2] = 1
Var(q^T k) = D_h
```

Dividing logits by `sqrt(D_h)` keeps the approximate score variance near one before softmax. This is an initialization-scale argument, not a universal guarantee about gradients in all trained layers.

Shape checks:

- `Q: [B,H,T,D_h]`
- `K^T: [B,H,D_h,T]`
- `scores: [B,H,T,T]`
- causal mask can be `[T,T]` or broadcastable to `[B,H,T,T]`

Code binding:

- `assignments/ch03_attention/tests.py` checks scaled attention against manual computation and validates 2D/3D mask behavior.
- Verification command: `.venv/bin/python assignments/ch03_attention/tests.py`.
- Browser render gate checks formula accessibility for the chapter page.

Common misconceptions:

- Scaling after softmax is wrong; the distribution is already formed.
- Softmax-after-mask and mask-after-softmax are not equivalent unless renormalized.

Source boundary:

- The Transformer paper states the scaling motivation.
- The variance proof uses simplifying independence assumptions.
- Attention heatmaps are diagnostic visuals, not causal explanations of model reasoning.

Accessibility notes:

- Provide shape tables in text form.
- If displaying attention heatmaps, include axis labels and a written interpretation.

Quick check:

For `D_h=64`, estimate the unscaled dot-product standard deviation and explain the effect on softmax saturation.

Post-lecture evidence:

- Ch03 public tests.
- One written derivation of `Var(q^T k)`.
- A failure analysis for applying mask after softmax.

## Sample L9: Cross Entropy and AdamW

Status: ready
Mapped materials: Ch07, `assignments/ch07_training/`, training capstone, DER-09 and DER-10.

Learning goals:

- Derive next-token cross entropy from autoregressive maximum likelihood.
- Explain why stable log-softmax avoids overflow.
- Distinguish AdamW decoupled weight decay from Adam with L2 penalty.

Notation ledger:

| Symbol | Meaning |
|--------|---------|
| `x_t` | token at position `t` |
| `V` | vocabulary size |
| `logits` | unnormalized scores `[B,T,V]` |
| `labels` | target ids `[B,T]` |
| `ignore_index` | label excluded from loss |

Core derivation:

Autoregressive language modeling factorizes:

```text
p(x_1,...,x_T) = product_t p(x_t | x_<t)
```

Maximizing log likelihood is equivalent to minimizing:

```text
- sum_t log p(x_t | x_<t)
```

With vocab logits, this becomes cross entropy at each predicted token. Padding, prompt-only tokens or unavailable labels must be excluded before invalid indexing or gather operations.

Shape checks:

- logits `[B,T,V]`
- labels `[B,T]`
- token loss `[B,T]` before masking or reduction
- scalar loss after averaging over valid labels

Code binding:

- `assignments/ch07_training/tests.py` checks stable cross entropy, AdamW update and scheduler boundaries.
- Verification command: `.venv/bin/python assignments/ch07_training/tests.py`.
- Training capstone acceptance checks train logs, checkpoint/resume and planning evidence.

Common misconceptions:

- Perplexity is not factual accuracy.
- AdamW is not the same update as adding L2 penalty to Adam gradients.

Source boundary:

- AdamW paper supports decoupled weight decay.
- Chinchilla-style scaling laws describe compute/data tradeoffs under specific training regimes.
- Course toy training logs are correctness evidence, not large-model scaling evidence.

Accessibility notes:

- Loss curves should include text summaries of trend, best step and failure mode.
- If showing optimizer update diagrams, include the update equations in text.

Quick check:

If labels contain `-100`, why must the implementation avoid gathering logits at index `-100` before masking?

Post-lecture evidence:

- Ch07 public tests.
- Training run log with loss, lr and grad_norm.
- One paragraph distinguishing AdamW and Adam+L2.

## Sample L18: Serving SLO and Capacity

Status: ready
Mapped materials: Ch10, inference engineering capstone, DER-13.

Learning goals:

- Compute KV cache memory from batch, layers, context, KV heads, head dim and dtype.
- Distinguish TTFT, TPOT, TPS and P95/P99 latency.
- Connect benchmark metrics to a capacity plan and an SLO decision.

Notation ledger:

| Symbol | Meaning |
|--------|---------|
| `B` | active batch size |
| `L` | context length |
| `N_layers` | number of transformer layers |
| `H_kv` | KV head count |
| `D_h` | head dimension |
| `bytes` | bytes per scalar |

Core derivation:

KV cache memory for one model instance is approximately:

```text
2 * B * L * N_layers * H_kv * D_h * bytes
```

The factor `2` comes from storing both K and V. This estimates cache memory, not weight memory, activation memory, allocator fragmentation or request scheduler overhead.

Shape checks:

- Per layer K cache: `[B,H_kv,L,D_h]`
- Per layer V cache: `[B,H_kv,L,D_h]`
- Benchmark output: latency in ms, throughput in tokens/s, capacity in GB or USD per 1M tokens

Code binding:

- `assignments/ch10_inference/tests.py` checks KV cache memory, quantization, RAG and benchmark summary.
- Verification command: `.venv/bin/python assignments/ch10_inference/tests.py`.
- Inference capstone acceptance checks health, eval, benchmark, SLO and capacity plan.

Common misconceptions:

- Lower KV cache does not make attention compute free.
- Average latency is not enough for an SLO; tail latency matters.
- A toy server passing health check is not production readiness.

Source boundary:

- PagedAttention and serving-framework papers support design patterns under measured workloads.
- Vendor/model-card latency numbers are volatile and configuration-dependent.
- Course capstone SLO is a reproducible teaching gate, not a universal production SLA.

Accessibility notes:

- Benchmark charts need table alternatives with P50/P95/P99 and error rate.
- Capacity calculations should show units, not just final numbers.

Quick check:

For `B=2`, `L=4096`, `N_layers=32`, `H_kv=8`, `D_h=128`, FP16, estimate KV cache GB and state what the estimate excludes.

Post-lecture evidence:

- Ch10 public tests.
- Inference capstone benchmark JSON and SLO report.
- Capacity plan with model, hardware, context length and cost assumptions.

## TA Review Checklist

| Check | Passing evidence |
|-------|------------------|
| Four representative notes | L1, L3, L9 and L18 samples cover tokenization, attention, training and serving |
| Field completeness | Every sample includes learning goals, notation, derivation, shape checks, code binding, misconceptions, source boundary, accessibility, quick check and post-lecture evidence |
| Course binding | Every sample links to assignment tests, DER ID or capstone evidence |
| Boundary control | Every sample states what the derivation or metric does not prove |
| Student usability | Each quick check can be answered without hidden tests or instructor-only materials |

## Release Checklist

- This pack is student-visible and contains no hidden tests, reference solutions or grading-only notes.
- Every sample remains consistent with [Lecture Notes Quality and Review Standard](lecture-notes-quality-review.md).
- If a sample is promoted into a full lecture handout, update [Lecture Notes Review Ledger](lecture-notes-review-ledger.md) and [Course Materials Index](course-materials-index.md).
- Run `.venv/bin/python verify_course.py` after editing this pack.
