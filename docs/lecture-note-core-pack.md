# Lecture Note Core Pack

本文件补充 [Lecture Notes Index](lecture-notes-index.md)、[Lecture Note Sample Pack](lecture-note-sample-pack.md)、[Lecture Notes Quality and Review Standard](lecture-notes-quality-review.md)、[Lecture Notes Review Ledger](lecture-notes-review-ledger.md)、[Board Derivation and Instructor Notes Pack](board-derivation-pack.md)、[Mathematical Derivation Audit](mathematical-derivation-audit.md)、[Notation and Shape Glossary](notation-shape-glossary.md)、[Worked Example Pack](worked-example-pack.md) 和 [Paper-to-Code Traceability Matrix](paper-to-code-traceability-matrix.md)。

复核日期：2026-06-05
适用范围：L2/L4/L6/L12/L15 的学生可见核心讲义、讨论课 recap、书面题审稿和 TA 答疑口径。

## Coverage Contract

本包选择的讲次不是随意样例，而是课程准确性风险较高的五类主题：

| lecture | topic | why it needs a core note | executable evidence |
|---------|-------|--------------------------|---------------------|
| L2 | embedding, analogy, RoPE | 词向量类比容易被误写成训练目标保证；RoPE 容易被误写成单调距离衰减 | `assignments/ch02_embeddings/tests.py` |
| L4 | causal mask, softmax, CE gradient | mask 的时机、广播和归一化经常导致实现错误 | `assignments/ch03_attention/tests.py` |
| L6 | MHA/GQA/MLA, norm, block | cache 节省、latent projection 和 residual path 容易被过度解释 | `assignments/ch04_multihead/tests.py`; `assignments/ch05_block/tests.py` |
| L12 | speculative decoding, constraints, frontier source boundary | 分布保持、速度收益和 MTP/preview 模型声明必须分开 | `assignments/ch08_generation/tests.py`; `scripts/verify_frontier_sources.py` |
| L15 | dependency parsing, seq2seq, BERT, evaluation | CS224N 风格 NLP 基础不能被 decoder-only prompt 叙事替代 | `assignments/ch11_classic_nlp/tests.py` |

每个核心 note 必须包含：Learning goals、Notation ledger、Core derivation、Shape checks、Code binding、Common misconceptions、Source boundary、Accessibility notes、Quick check 和 Post-lecture evidence。

## Core L2: Embedding, Analogy, and RoPE

Status: ready
Mapped materials: Ch02, DER-02, DER-03, `assignments/ch02_embeddings/`.

Learning goals:

- Explain embedding lookup as a linear selection operation without implying that token identity is continuous.
- State what a word analogy vector test can reveal and what it cannot prove.
- Derive the RoPE relative-position identity used by the attention score.

Notation ledger:

| Symbol | Meaning |
|--------|---------|
| `V` | vocabulary size |
| `D` | embedding dimension |
| `E` | embedding table `[V,D]` |
| `x_t` | token id at position `t` |
| `R_t` | block rotation matrix for RoPE position `t` |

Core derivation:

Embedding lookup can be written as:

```text
embedding(x_t) = one_hot(x_t) @ E
```

This expression is useful for shape reasoning: `one_hot(x_t)` has shape `[V]`, so the result has shape `[D]`. It does not mean that the one-hot vector itself contains semantic geometry. The geometry comes from training pressure on `E`.

For analogy reasoning, the usual diagnostic computes:

```text
argmax_w cosine(E[w], E[b] - E[a] + E[c])
```

This is a probe of learned linear regularities. It is not an objective term and does not prove that all semantic relations are encoded as a single global linear transform.

For RoPE, each two-dimensional feature pair is rotated by position. The key identity is:

```text
(R_m q)^T (R_n k) = q^T R_m^T R_n k = q^T R_(n-m) k
```

The identity shows that the score can depend on relative offset under the rotation construction. It does not require attention scores to decay monotonically with distance for every learned `q,k`.

Shape checks:

- Token ids: `[B,T]`
- Embeddings: `[B,T,D]`
- RoPE input per head: `[B,H,T,D_h]`
- RoPE requires an even per-head dimension if implemented as paired rotations.

Code binding:

- `assignments/ch02_embeddings/tests.py` checks embedding parameter count, sinusoidal buffer shape, RoPE norm preservation and relative-position score structure.
- Verification command: `.venv/bin/python assignments/ch02_embeddings/tests.py`.

Common misconceptions:

- “Analogy vectors prove semantic relations are linear” is too strong.
- “RoPE makes attention decrease with distance” is too strong.
- “Norm preservation means semantic preservation” is false.

Source boundary:

- Word2Vec and GloVe results support empirical linear regularities under specific corpora and objectives.
- RoPE paper supports the relative-position rotation construction.
- Course examples are diagnostics, not universal semantic guarantees.

Accessibility notes:

- Show analogy vectors as text equations and nearest-neighbor tables, not only arrows on a diagram.
- RoPE rotation should include a two-dimensional numeric example for students who cannot inspect animated visuals.

Quick check:

Given `E[king] - E[man] + E[woman]`, state two reasons why a nearest neighbor result should be reported as evidence, not proof.

Post-lecture evidence:

- Ch02 public tests.
- Written derivation of `R_m^T R_n = R_(n-m)`.
- One paragraph explaining the boundary of analogy reasoning.

## Core L4: Causal Mask and Cross-Entropy Gradient

Status: ready
Mapped materials: Ch03, DER-05, DER-09, `assignments/ch03_attention/`.

Learning goals:

- Apply a causal mask at the logit level and explain the resulting probability support.
- Distinguish mask shape, broadcast shape and attention score shape.
- Derive the softmax cross-entropy gradient used in next-token training.

Notation ledger:

| Symbol | Meaning |
|--------|---------|
| `S` | attention scores `[B,H,T,T]` |
| `M` | additive or boolean mask broadcastable to `S` |
| `P` | attention probabilities after softmax |
| `z` | logits for one vocab row |
| `y` | gold class id |

Core derivation:

For causal attention, invalid future positions are excluded before softmax:

```text
S_masked[i,j] = S[i,j] if j <= i else -inf
P[i,:] = softmax(S_masked[i,:])
```

Masking after softmax changes the sum of probabilities unless the row is renormalized, so it is not the same operation.

For one cross-entropy row:

```text
p_i = exp(z_i) / sum_j exp(z_j)
L = -log p_y
dL/dz_i = p_i - 1[i = y]
```

The derivation is local to one row. In sequence training, ignored labels must be removed from the reduction and must not be gathered as real class ids.

Shape checks:

- Scores: `[B,H,T,T]`
- Causal mask: `[T,T]`, `[1,1,T,T]` or another broadcastable shape
- Vocab logits: `[B,T,V]`
- Labels: `[B,T]`

Code binding:

- `assignments/ch03_attention/tests.py` checks 2D/3D masks and manual attention computation.
- `assignments/ch07_training/tests.py` checks stable cross entropy and ignore-index behavior.
- Verification commands: `.venv/bin/python assignments/ch03_attention/tests.py`; `.venv/bin/python assignments/ch07_training/tests.py`.

Common misconceptions:

- “Mask after softmax is fine because future probabilities become zero” misses renormalization.
- “A `[T,T]` mask always works” is incomplete; it must be broadcastable to the score tensor.
- “CE loss directly measures factual correctness” is false.

Source boundary:

- The Transformer formulation supports scaled dot-product attention and masking before softmax.
- The CE gradient is a standard supervised-learning derivation.
- Course tests prove implementation invariants on small tensors, not convergence of a large model.

Accessibility notes:

- Provide one row of masked logits as text, including the `-inf` entries.
- If showing a triangular mask image, include its allowed/disallowed coordinate rule.

Quick check:

For `T=4`, write the allowed key indices for query position `2` under zero-based causal masking.

Post-lecture evidence:

- Ch03 and Ch07 public tests.
- Written explanation of why post-softmax masking changes row sums.
- One shape table for scores, mask and probabilities.

## Core L6: MHA, GQA, MLA, Norm, and Block Boundaries

Status: ready
Mapped materials: Ch04-Ch05, DER-06, DER-07, `assignments/ch04_multihead/`, `assignments/ch05_block/`.

Learning goals:

- Compare MHA, GQA and MLA by parameter projection, KV cache and attention work.
- Explain what LayerNorm/RMSNorm changes and what residual connections preserve.
- Identify which efficiency claims are implementation-dependent.

Notation ledger:

| Symbol | Meaning |
|--------|---------|
| `H_q` | number of query heads |
| `H_kv` | number of key/value heads |
| `D_h` | per-head dimension |
| `L` | cached context length |
| `D_latent` | latent cache dimension in MLA-style notes |

Core derivation:

For standard KV cache, per layer and per sequence element:

```text
cache elements = 2 * H_kv * D_h
```

For a batch/context window:

```text
total elements = B * L * N_layers * 2 * H_kv * D_h
```

GQA reduces `H_kv` while keeping more query heads. This reduces KV cache storage and K/V projection outputs. It does not remove the need to compute attention scores for query heads.

MLA-style latent cache stores compressed latent states and reconstructs or projects K/V information as needed. It can reduce cache memory, but matrix absorption or latent projection does not make attention free.

For Pre-Norm:

```text
x_(l+1) = x_l + F(Norm(x_l))
```

The residual path gives a direct additive route. It does not guarantee stable training for arbitrary depth, optimizer, initialization or data.

Shape checks:

- MHA Q/K/V before attention: `[B,H,T,D_h]`
- GQA K/V can use `[B,H_kv,T,D_h]` and repeat or index groups for query heads.
- Transformer block input/output: `[B,T,D_model]`
- Norm statistics are computed over feature dimension, not over the time dimension.

Code binding:

- `assignments/ch04_multihead/tests.py` checks MHA/GQA/MLA shapes and cache ratios.
- `assignments/ch05_block/tests.py` checks LayerNorm gradcheck, RMSNorm behavior and Pre-Norm block gradient flow.
- Verification commands: `.venv/bin/python assignments/ch04_multihead/tests.py`; `.venv/bin/python assignments/ch05_block/tests.py`.

Common misconceptions:

- “GQA reduces all attention compute by the same factor as KV heads” is too strong.
- “MLA compression makes attention free” is false.
- “Pre-Norm guarantees no gradient problems” is false.

Source boundary:

- MHA is stable textbook Transformer material.
- GQA and MLA are implementation and model-family design choices; claims must include workload and architecture conditions.
- Course cache arithmetic is an engineering model and should be checked against real kernels before capacity promises.

Accessibility notes:

- Put head counts and cache formulas in tables.
- Any diagram comparing heads must label query heads and KV heads separately.

Quick check:

If `H_q=32`, `H_kv=8`, `D_h=128`, compute the per-token K+V cache elements for one layer and state what this number does not include.

Post-lecture evidence:

- Ch04 and Ch05 public tests.
- Written KV cache calculation.
- One boundary statement about GQA or MLA efficiency.

## Core L12: Speculative Decoding, Constraints, and Frontier Source Boundaries

Status: ready
Mapped materials: Ch08, [Frontier Source Evidence Cards](frontier-source-evidence-cards.md), `assignments/ch08_generation/`, `scripts/verify_frontier_sources.py`.

Learning goals:

- Distinguish distribution-preserving speculative decoding from heuristic approximation.
- Explain why latency speedup depends on draft quality, acceptance rate and hardware scheduling.
- Apply source levels before using preview-model or model-card claims in coursework.

Notation ledger:

| Symbol | Meaning |
|--------|---------|
| `p` | target model distribution |
| `q` | draft model distribution |
| `K` | number of proposed draft tokens |
| `a` | acceptance indicator or acceptance rate |
| `SLO` | service-level objective such as P95 latency |

Core derivation:

Speculative decoding proposes tokens from `q` and verifies them under `p`. In distribution-preserving variants, the accept/reject correction is designed so final samples follow the target distribution. The exact correction depends on the algorithm. The course claim should be:

```text
speedup is possible when draft work + verification work < target-only work
```

not:

```text
speculative decoding is always faster
```

Constrained decoding is different: it restricts the valid next-token set using a grammar, schema or finite-state rule. It can improve format validity, but it can also reduce diversity, expose tokenizer edge cases or force awkward outputs.

Shape checks:

- Target logits at each step: `[B,V]`
- Draft proposal ids: `[B,K]`
- Acceptance mask: `[B,K]`
- Constraint mask over vocab: `[B,V]`

Code binding:

- `assignments/ch08_generation/tests.py` checks greedy, top-k, top-p, invalid hyperparameters and speculative decoding budget/statistics.
- `scripts/verify_frontier_sources.py` checks official/primary source markers and monitor-only absent-marker boundaries.
- Verification commands: `.venv/bin/python assignments/ch08_generation/tests.py`; `.venv/bin/python scripts/verify_frontier_sources.py --json-out /tmp/frontier_sources_check.json`.

Common misconceptions:

- “Distribution-preserving” does not mean every implementation is exact.
- “Higher acceptance rate always means lower latency” ignores batching, memory bandwidth and verification cost.
- “Model-card preview claims can be used as exam facts” is false unless the source level allows it.

Source boundary:

- Speculative decoding papers support the distribution-correction idea under algorithm assumptions.
- Course implementation is a small correctness exercise, not a production serving benchmark.
- D-level frontier claims are monitor-only and should not be used as current course facts.

Accessibility notes:

- Use a text timeline showing draft proposal, accepted prefix, rejected token and fallback sample.
- For source cards, provide source id and status in text, not color alone.

Quick check:

Give one condition where speculative decoding preserves the target distribution but still fails to improve P95 latency.

Post-lecture evidence:

- Ch08 public tests.
- Frontier source verifier JSON manifest.
- One source-boundary paragraph for a preview-model claim.

## Core L15: Classic NLP, Encoder-Decoder, BERT, and Evaluation

Status: ready
Mapped materials: [Classic NLP Deep-Dive Teaching Module](classic-nlp-deep-dive-module.md), [经典 NLP 专题 Handout](classic-nlp-handout.md), `assignments/ch11_classic_nlp/`.

Learning goals:

- Compute UAS/LAS for a small dependency parse example.
- Write the seq2seq teacher-forcing objective and explain exposure bias.
- Build BERT-style MLM labels and distinguish them from causal LM labels.
- Judge what BLEU, ROUGE-L, EM and token F1 can and cannot support.

Notation ledger:

| Symbol | Meaning |
|--------|---------|
| `h_i` | predicted or gold head for token `i` |
| `l_i` | dependency label for token `i` |
| `x` | source sequence |
| `y` | target sequence |
| `M` | selected MLM mask positions |

Core derivation:

Dependency parsing metrics:

```text
UAS = count(pred_head_i == gold_head_i) / n
LAS = count(pred_head_i == gold_head_i and pred_label_i == gold_label_i) / n
```

Seq2seq objective:

```text
p(y | x) = product_t p(y_t | y_<t, x)
L = - sum_t log p(y_t^gold | y_<t^gold, x)
```

At inference, the prefix is model-generated, so teacher-forcing training and autoregressive decoding condition on different prefix distributions.

BERT-style MLM:

```text
L_MLM = - sum_{i in M} log p(x_i | x_not_masked)
```

Only selected mask positions receive labels. Non-mask positions use ignore labels in the assignment implementation.

Shape checks:

- Dependency heads: list length `n`
- BLEU hypothesis/reference tokens: list of tokens
- MLM input ids: `[T]`
- MLM labels: `[T]` with ignore entries outside `M`

Code binding:

- `assignments/ch11_classic_nlp/tests.py` checks UAS/LAS, BLEU, ROUGE-L, QA EM/F1 and MLM label masking.
- Verification command: `.venv/bin/python assignments/ch11_classic_nlp/tests.py`.

Common misconceptions:

- “Dependency parsing is just attention visualization” is false.
- “Beam search is the training algorithm” is false.
- “BERT and GPT only differ by mask token” is too shallow.
- “High BLEU proves semantic correctness” is false.

Source boundary:

- Dependency parsing, seq2seq attention and BERT objectives are stable neural NLP foundations.
- BLEU/ROUGE/EM/F1 are useful scoring tools under task assumptions, not universal quality measures.
- Decoder-only LLM coverage does not replace encoder-only and encoder-decoder concepts in a university NLP course.

Accessibility notes:

- Parser traces should include stack, buffer and arc tables.
- Metric examples should show numerator and denominator explicitly.

Quick check:

Given three predicted heads where two heads match and only one matching head has the correct label, compute UAS and LAS.

Post-lecture evidence:

- Ch11 public tests.
- One seq2seq exposure-bias short answer.
- One metric failure case with claim-strength judgment.

## TA Review Checklist

| item | pass criterion |
|------|----------------|
| Field completeness | Each core note includes the ten required fields from the Lecture Note Sample Pack |
| Executable binding | Each note points to a public test or source verifier command |
| Boundary control | Each note contains at least two explicit cannot/does-not boundary statements |
| CS224N alignment | L15 preserves dependency parsing, seq2seq, BERT and evaluation coverage |
| Source safety | L12 separates algorithm facts, implementation exercises and frontier source levels |
| Student usability | Each note has a quick check and post-lecture evidence suitable for grading or recap |

## Release Checklist

| check | command or evidence |
|-------|---------------------|
| Core note links | `.venv/bin/python verify_course.py` |
| Assignment evidence | `.venv/bin/python run_assignment_tests.py` |
| Frontier source evidence | `.venv/bin/python scripts/verify_frontier_sources.py --json-out /tmp/frontier_sources_check.json` |
| Human review | update [Lecture Notes Review Ledger](lecture-notes-review-ledger.md) if a core note changes after release |
