# Notation and Shape Glossary

复核日期：2026-06-05

本词汇表统一课程中的符号、张量 shape、mask 约定、cache 约定和指标单位。它补充 [Core Concept Glossary](core-concept-glossary.md)、[Topic Dependency and Spiral Review Map](topic-dependency-map.md)、[Mathematical Derivation Audit](mathematical-derivation-audit.md)、[Worked Example Pack](worked-example-pack.md)、[Lecture Note Sample Pack](lecture-note-sample-pack.md)、[Recitation Worksheet Pack](recitation-worksheet-pack.md)、[Assessment Blueprint and Coverage Matrix](assessment-blueprint-coverage-matrix.md)、[Chapter Source and Accuracy Map](chapter-source-map.md) 和 [Assignment Handout Pack](assignment-handout-pack.md)。

使用规则：

- 章节正文、lecture notes、worked examples、recitation worksheet、written answers 和 project reports 使用本表的默认符号。
- 若某个作业或论文复盘临时使用不同符号，必须在答案开头写出 local notation，并说明如何映射回本表。
- Shape 默认写成 `[B,T,D]` 形式；概率、metric 和 cost 必须写单位或取值范围。
- 本表可以进入 student site release；不得包含隐藏测试输入、reference_solution.py、私有评分样例或真实学生提交。

## Global Symbols

| symbol | default meaning | default shape or unit | notes |
| --- | --- | --- | --- |
| B | batch size | positive integer | mini-batch dimension |
| T | current sequence length | positive integer | used for training, prefill, or full forward pass |
| S | source/cache length | positive integer | use `S` when query length differs from key/value length |
| V | vocabulary size | positive integer | token ids must be in `[0,V)` |
| D | hidden/model width | positive integer | same as `d_model` unless a local note says otherwise |
| H | query attention heads | positive integer | MHA uses `H_kv=H` |
| H_kv | key/value heads | positive integer | GQA/MQA may use `H_kv < H` |
| D_h | per-head width | positive integer | usually `D/H` for standard attention |
| L | number of Transformer layers | positive integer | not sequence length |
| K | top-k count or retrieved document count | positive integer | write `top_k` or `retrieval_k` when ambiguous |
| E | embedding matrix | `[V,D]` | token lookup returns `[B,T,D]` |
| x | hidden states | `[B,T,D]` | use `x_i` only after defining token position |
| logits | unnormalized scores over vocabulary | `[B,T,V]` | not probabilities until softmax is applied |
| labels | next-token targets or class labels | `[B,T]` or task-specific | ignored positions must be marked explicitly |
| mask | boolean or additive mask | see Mask and Broadcast Rules | specify polarity: visible, blocked, or additive negative |
| dtype_bytes | bytes per scalar | bytes | fp16/bf16 is 2, fp32 is 4, int8 is 1 |

## Module Shape Contracts

| contract_id | module | input shape | output shape | invariant |
| --- | --- | --- | --- | --- |
| NS-01 | token ids | `[B,T]` integer ids | `[B,T]` ids or token strings | ids stay in `[0,V)` |
| NS-02 | embedding lookup | `input_ids [B,T]`, `E [V,D]` | hidden states `[B,T,D]` | lookup is equivalent to one-hot times `E` |
| NS-03 | sinusoidal / RoPE positions | positions `[T]` or `[B,T]`; hidden `[B,H,T,D_h]` | rotated hidden `[B,H,T,D_h]` | RoPE requires even paired dimensions |
| NS-04 | QKV projection | hidden `[B,T,D]` | `Q,K,V [B,H,T,D_h]` | `H*D_h=D` for standard projection |
| NS-05 | attention scores | `Q [B,H,T,D_h]`, `K [B,H,S,D_h]` | scores `[B,H,T,S]` | scale by `sqrt(D_h)` before softmax |
| NS-06 | attention context | attention probabilities `[B,H,T,S]`, `V [B,H,S,D_h]` | context `[B,H,T,D_h]` | probability rows over visible keys sum to 1 |
| NS-07 | MHA output projection | context `[B,H,T,D_h]` | hidden `[B,T,D]` | head dimension is concatenated before output projection |
| NS-08 | GQA / MQA cache | K/V cache `[B,H_kv,S,D_h]` | grouped attention output `[B,H,T,D_h]` | KV heads are shared across query-head groups |
| NS-09 | Transformer block | hidden `[B,T,D]` | hidden `[B,T,D]` | residual paths require unchanged final shape |
| NS-10 | FFN / SwiGLU | hidden `[B,T,D]` | hidden `[B,T,D]` | intermediate width must be documented |
| NS-11 | LM head | hidden `[B,T,D]` | logits `[B,T,V]` | tied head reuses token embedding weights |
| NS-12 | cross entropy | logits `[B,T,V]`, labels `[B,T]` | scalar loss or token loss `[B,T]` | ignored labels do not contribute to average |
| NS-13 | generation loop | current ids `[B,t]` | next ids `[B,t+1]` | append one or more generated tokens per step |
| NS-14 | retrieval matrix | query `[D_r]`, documents `[N,D_r]` | scores `[N]`, top ids `[K]` | similarity metric and normalization must be stated |
| NS-15 | evaluation metrics | predictions and references task-specific | scalar in `[0,1]`, percent, ms, tokens/s, or cost | unit and aggregation must be explicit |

## Mask and Broadcast Rules

| rule_id | rule | expected evidence | common error |
| --- | --- | --- | --- |
| MASK-CAUSAL | Causal masks block future key positions for each query position. | visible matrix lower-triangular for full self-attention | allowing attention to future columns |
| MASK-ADDITIVE | Additive masks are applied to logits before softmax. | blocked logits use a large negative value or negative infinity | multiplying probabilities after softmax without renormalizing |
| MASK-BOOLEAN | Boolean masks must define whether `True` means visible or blocked. | function docstring or worksheet states polarity | mixing PyTorch and course conventions |
| MASK-BROADCAST | A `[T,S]` mask can broadcast to `[B,H,T,S]` only along batch/head axes. | shape trace shows batch and head singleton axes when needed | broadcasting over query or key axes accidentally |
| MASK-PADDING | Padding masks are different from causal masks and may be combined. | answer states padding and causal purposes separately | treating padding as future-token blocking |
| MASK-LABEL | Label masks control loss contribution, not attention visibility. | ignored labels use an explicit ignore index or weight zero | using attention mask as loss mask without checking target positions |

## Loss, Objective, and Optimizer Symbols

| symbol | meaning | shape or unit | boundary |
| --- | --- | --- | --- |
| y | target token ids or labels | `[B,T]` or task-specific | define whether it is right-shifted |
| log p_theta | model log probability | scalar per token or sequence | raw logits are not log probabilities |
| CE | cross entropy / next-token NLL | scalar or token average | lower CE does not prove factuality or safety |
| ppl | perplexity | `exp(mean CE)` | depends on tokenization and dataset |
| lr | learning rate | scalar | schedule must be stated |
| beta_1, beta_2 | Adam moment coefficients | scalar in `[0,1)` | not DPO beta |
| weight_decay | AdamW decoupled decay coefficient | scalar | not the same as L2 inside Adam gradient |
| beta_dpo | DPO preference scale | scalar | use a distinct name from Adam betas |
| A_lora, B_lora | LoRA low-rank factors | implementation-specific matrices | rank and target module must be stated |
| advantage | policy-gradient or GRPO relative score | scalar per sampled response | baseline/group definition must be stated |

## Serving and Evaluation Units

| symbol | meaning | unit | reporting rule |
| --- | --- | --- | --- |
| TTFT | time to first token | milliseconds | report percentile and workload |
| TPOT | time per output token | milliseconds/token | report decode workload and batch/concurrency |
| TPS | throughput | tokens/second | specify generated vs total tokens |
| P50/P95/P99 | latency percentiles | milliseconds | include request count and concurrency |
| error_rate | failed requests over total requests | ratio or percent | define timeout and non-2xx handling |
| memory | peak or allocated memory | GB or GiB | state device and dtype |
| cost | API or compute cost | USD or local currency | state denominator, such as per 1M tokens |
| UAS | unlabeled attachment score | ratio or percent | dependency heads only |
| LAS | labeled attachment score | ratio or percent | dependency heads plus labels |
| BLEU / ROUGE-L | lexical overlap metrics | ratio, percent, or package convention | package and tokenization must be named |
| EM / F1 | QA answer metrics | ratio or percent | normalization rules must be stated |

## Disambiguation Rules

| ambiguity | required resolution |
| --- | --- |
| `L` could mean layers or loss. | Use `L` for layers only in shape tables; write `loss` for objective value. |
| `K` could mean keys or top-k. | Use `K_cache` for cached keys and `top_k` for sampling/retrieval count. |
| `S` could mean source length or score. | Use `S` for source/cache length; write `scores` for attention logits. |
| `H` could mean hidden size or heads. | Use `H` for heads and `D` for hidden width in this course. |
| `beta` could mean Adam beta or DPO beta. | Use `beta_1`, `beta_2`, and `beta_dpo`. |
| mask polarity differs across libraries. | State `True means visible` or `True means blocked` at the function boundary. |
| metric values can be percent or ratio. | Write the unit next to every metric table column. |

## Assessment Use

| use case | required student evidence |
| --- | --- |
| written derivation | define symbols, assumptions, shape, unit, and boundary before final equation |
| programming assignment | preserve starter API shape contracts and report any intentional local notation |
| recitation worksheet | show shape trace and identify the first incompatible dimension |
| paper recap | map paper notation to course notation before comparing claims |
| capstone report | include split_card, metric_card, uncertainty_record, and unit-aware SLO/cost tables |
| regrade request | cite the relevant contract_id or mask rule when contesting a shape/mask issue |

## Maintenance Workflow

1. When a chapter introduces a new symbol, first check whether this glossary already has a matching entry.
2. When a derivation, worked example, assignment starter, or capstone report uses a new shape contract, add or update a `NS-*` row.
3. When a mask bug appears in tests or office hours, add the polarity or broadcast rule that would have caught it.
4. When a metric or SLO is added, specify unit, aggregation, workload, and boundary before using it in grading.
5. Run `.venv/bin/python verify_course.py` after editing this glossary or any linked formula/assignment material.

## Release Checklist

- Global Symbols define B, T, S, V, D, H, H_kv, D_h, L, K, logits, labels, mask, and dtype_bytes.
- Module Shape Contracts cover tokenization, embedding, RoPE, QKV, attention, GQA/MQA cache, Transformer block, FFN, LM head, loss, generation, retrieval, and evaluation.
- Mask and Broadcast Rules define causal, additive, boolean, broadcast, padding, and label masks.
- Loss/objective notation distinguishes Adam betas from DPO beta.
- Serving and Evaluation Units define latency, throughput, memory, cost, and classic NLP metrics.
- Disambiguation Rules cover overloaded L, K, S, H, beta, mask polarity, and metric unit conventions.
- Assessment Use links the glossary to written derivations, programming assignments, recitations, paper recaps, capstone reports, and regrade requests.
- Student site release excludes hidden tests, reference_solution.py, private grading samples, and real student submissions.
