# Core Concept Glossary

复核日期：2026-06-05

本词汇表统一课程中高频技术术语的课程内定义、常见误讲边界、评估证据和来源边界。它补充 [Concept Mastery and Misconception Map](concept-misconception-map.md)、[Topic Dependency and Spiral Review Map](topic-dependency-map.md)、[Chapter Source and Accuracy Map](chapter-source-map.md)、[Notation and Shape Glossary](notation-shape-glossary.md)、[Worked Example Pack](worked-example-pack.md)、[Assessment Blueprint and Coverage Matrix](assessment-blueprint-coverage-matrix.md)、[External Source Verification Guide](external-source-verification.md) 和 [前沿模型来源等级与复核记录](frontier-source-audit.md)。

使用规则：

- 章节正文、lecture notes、slides、quiz、written answers、paper recap 和 capstone report 应使用本表的课程内定义。
- 若论文或框架文档使用不同术语，学生必须先说明 paper/framework definition，再映射到本表。
- 本表只约束课程内讲法；前沿模型规格、benchmark、API、价格和硬件性能仍以 source audit 的日期和来源等级为准。
- 本表可以进入 student site release；不得包含隐藏测试输入、reference_solution.py、私有评分样例或真实学生提交。

## Definition Schema

| field | requirement |
| --- | --- |
| concept_id | Stable `CG-*` identifier. |
| term | Course-facing English or bilingual term. |
| course definition | Definition students may use in written answers and reports. |
| not this | Common overclaim, vague wording, or incorrect synonym. |
| evidence anchor | Chapter, assignment, worked example, derivation, metric, or project evidence. |
| source boundary | Stable theory, implementation detail, metric definition, or volatile source claim. |

## Core Concepts

| concept_id | term | course definition | not this | evidence anchor | source boundary |
| --- | --- | --- | --- | --- | --- |
| CG-TOKEN-BPE | Byte Pair Encoding / BPE | A greedy subword merge procedure that repeatedly merges currently frequent adjacent symbols under a fixed training corpus and vocabulary budget. | Not semantic optimal segmentation or a guarantee of morpheme boundaries. | Ch01, WE-CH01-BPE, DER-01, `assignments/ch01_bpe/` | stable algorithmic procedure |
| CG-EMBED | Embedding lookup | A trainable table lookup equivalent to multiplying one-hot token indicators by an embedding matrix. | Not the token meaning itself and not a guarantee that analogy directions are linear. | Ch02, DER-02, notation glossary `E [V,D]` | stable implementation math |
| CG-POSITION | Positional encoding | Additional position-dependent information supplied so a sequence model can distinguish order. | Not always learned, not always absolute, and not a universal long-context guarantee. | Ch02, Ch04, source map Ch02 | stable concept with implementation variants |
| CG-ROPE | Rotary Position Embedding / RoPE | A paired rotation of query/key dimensions that makes attention scores depend on relative position through rotation differences. | Norm preservation is not semantic preservation or unlimited extrapolation. | WE-CH02-ROPE, DER-03, `assignments/ch02_embeddings/` | stable theory with extrapolation boundary |
| CG-ATTN | Scaled dot-product attention | A differentiable weighted aggregation using scaled query-key dot products, masking, softmax, and value mixing. | Attention weights alone are not a complete causal explanation of model reasoning. | Ch03, WE-CH03-ATTN, DER-04, DER-05 | stable theory and implementation detail |
| CG-CAUSAL-MASK | Causal mask | A mask that prevents each autoregressive query position from attending to future key positions. | Not the same as padding mask or label/loss mask. | Ch03, notation rules MASK-CAUSAL and MASK-LABEL | stable implementation contract |
| CG-MHA | Multi-head attention | Parallel attention heads that project hidden states into multiple query/key/value subspaces and concatenate head outputs. | More heads do not automatically mean better quality. | Ch04, source map Ch04, assignment tests | stable architecture definition |
| CG-GQA | Grouped-query attention | An attention variant where multiple query heads share fewer key/value heads to reduce KV-cache memory. | Not a reduction in query-head count and not a free quality guarantee. | WE-CH04-GQA, DER-06, `assignments/ch04_multihead/` | implementation detail with tradeoff boundary |
| CG-MLA | Multi-head latent attention / MLA | A DeepSeek-reported KV compression design that stores lower-dimensional latent cache states in its full system context. | The course simplified MLA exercise is not proof of paper-level speed, memory, or quality. | Ch04 source map, frontier-source-audit.md | volatile/frontier implementation claim |
| CG-LAYERNORM | LayerNorm | A normalization over the last hidden dimension using input-dependent mean and variance plus learned scale/shift. | Not a fixed affine rescaling independent of the current input. | Ch05, DER-07, Ch05 gradcheck tests | stable normalization math |
| CG-RMSNORM | RMSNorm | A normalization using root mean square scaling without centering by the mean. | Not LayerNorm without beta only, and not zero-mean normalization. | WE-CH05-NORM, Ch05 tests | stable normalization math |
| CG-FFN | Feed-forward network / FFN | Token-wise nonlinear capacity inside a Transformer block, usually expanding then projecting the hidden dimension. | Not a replacement for attention and not sequence mixing by itself. | Ch05, assignment tests, source map Ch05 | stable architecture definition |
| CG-DECODER-LM | Decoder-only language model | An autoregressive Transformer stack trained to predict next tokens under a causal mask. | Not the same objective as encoder-only MLM or seq2seq conditional generation. | Ch06, DER-08, DER-09 | stable model-family definition |
| CG-MOE | Mixture of Experts / MoE | A sparse routing architecture where tokens activate selected expert sub-networks under routing and balancing constraints. | Activated parameters are fewer than total parameters, but system cost is not automatically linear in activated count. | Ch06, MoE router tests, source map Ch06 | architecture concept with systems boundary |
| CG-CE-PPL | Cross entropy and perplexity | Cross entropy is average negative log likelihood; perplexity is its exponential under a fixed tokenization and dataset. | Low perplexity does not prove factual correctness, safety, or human preference quality. | Ch07, DER-09, `assignments/ch07_training/` | stable objective with metric boundary |
| CG-ADAMW | AdamW | Adam with decoupled weight decay applied separately from the adaptive gradient update. | Not identical to Adam with L2 penalty in the gradient. | WE-CH07-ADAMW, DER-10 | stable optimizer definition |
| CG-SAMPLING | Top-k / top-p sampling | Decoding filters or reshapes a probability distribution before sampling tokens. | Top-p is not a fixed number of tokens and diversity is not human quality. | WE-CH08-TOPP, Ch08 tests | stable decoding procedure |
| CG-SPECDEC | Speculative decoding | A draft/target decoding procedure that can reduce target-model calls when acceptance correction assumptions hold. | Not unconditional lossless speedup and not independent of draft quality or serving bottlenecks. | Ch08, assignment stats tests | stable algorithm with systems boundary |
| CG-SFT | Supervised fine-tuning / SFT | Training on prompt-response examples, usually masking prompt and padding tokens so loss applies to response targets. | Not pretraining on all prompt tokens and not inherently preference alignment. | Ch09, SFT mask tests | stable training procedure |
| CG-LORA | Low-Rank Adaptation / LoRA | A parameter-efficient method that adds trainable low-rank updates to selected base-model modules. | Not a guarantee of unchanged behavior after merge or universal quality preservation. | Ch09, LoRA tests, project reports | stable adaptation method with configuration boundary |
| CG-DPO | Direct Preference Optimization / DPO | A preference objective comparing chosen and rejected response log-probability ratios against a reference model. | Not raw chosen log-probability maximization and not full safety alignment. | WE-CH09-DPO, DER-12 | stable objective with safety boundary |
| CG-GRPO | Group Relative Policy Optimization / GRPO | A group-relative reinforcement-learning objective using within-prompt candidate comparisons and advantage normalization. | Not a complete solution to reward noise, sampling coverage, or safety. | Ch09, GRPO tests, frontier source audit | frontier-adjacent objective claim |
| CG-KVCACHE | KV cache | Stored key/value tensors reused during incremental decoding to avoid recomputing past token projections. | Not model weight memory and not independent of batch, layers, heads, context, and dtype. | WE-CH10-KVCACHE, DER-06, DER-13 | stable systems accounting |
| CG-RAG | Retrieval-augmented generation / RAG | A pipeline that retrieves external context and conditions generation on retrieved evidence. | Retrieval hit is not answer correctness, and RAG is not automatic factuality. | Ch10, RAG tests, project report template | stable pipeline with evaluation boundary |
| CG-SLO | Serving SLO | A predeclared service target over workload-specific latency, throughput, error rate, and capacity metrics. | Average latency alone is not an SLO, and toy runs do not prove production readiness. | Ch10, inference capstone, notation units | systems metric definition |
| CG-EVAL-METRIC | Evaluation metric | A task-specific quantitative score with a fixed input/output convention, aggregation, and known failure modes. | A single metric is not general model quality. | Ch11, DER-14, experimental rigor guide | metric definition with interpretation boundary |
| CG-SOURCE-BOUNDARY | Source boundary | The explicit limit on what a paper, model card, official doc, benchmark, or course experiment supports. | Not a decorative citation and not permission to generalize beyond configuration/date/task. | chapter-source-map.md, claim audit ledger, external-source-verification.md | source governance rule |

## Cross-Reference Map

| concept group | required companion |
| --- | --- |
| Shape-bearing terms | Use [Notation and Shape Glossary](notation-shape-glossary.md) for dimensions, mask polarity, and units. |
| Misconception-prone terms | Use [Concept Mastery and Misconception Map](concept-misconception-map.md) for quick checks and remediation. |
| Formula-heavy terms | Use [Mathematical Derivation Audit](mathematical-derivation-audit.md) for assumptions, shape/units, evidence, and boundary. |
| Worked examples | Use [Worked Example Pack](worked-example-pack.md) for small reproducible traces. |
| Source-sensitive terms | Use [Chapter Source and Accuracy Map](chapter-source-map.md), [External Source Verification Guide](external-source-verification.md), and [前沿模型来源等级与复核记录](frontier-source-audit.md). |
| Assessment terms | Use [Assessment Blueprint and Coverage Matrix](assessment-blueprint-coverage-matrix.md), [Assessment Item Bank Ledger](assessment-item-bank-ledger.md), and [书面推导与概念题题库](written-problem-set.md). |

## Definition Quality Rules

| rule_id | rule | failure signal |
| --- | --- | --- |
| CG-R1 | A definition must name the mechanism, not only the intuition. | “attention finds important words” without Q/K/V, score, mask, or value mixing |
| CG-R2 | A definition must state the boundary when a term is often overclaimed. | “RAG fixes hallucination” without retrieval/generation evaluation |
| CG-R3 | A metric definition must include unit, range, aggregation, and failure mode. | “P95 is good” without workload, request count, or threshold |
| CG-R4 | A frontier concept must include source tier and review date before entering assessment. | “GRPO proves reasoning” without source boundary |
| CG-R5 | A project report must map local terminology back to course terminology. | custom names for data split, metric, or cache without mapping |

## Maintenance Workflow

1. When a chapter adds a new term that appears in a heading, assignment, quiz, or capstone rubric, add a `CG-*` row.
2. When office hours reveal a repeated definitional confusion, update both this glossary and the misconception map.
3. When a source changes or a frontier model claim is downgraded, update the source boundary cell before the term is used in assessment.
4. When a term has a tensor or unit convention, cross-link the relevant notation glossary row or metric unit.
5. Run `.venv/bin/python verify_course.py` after editing this glossary or any linked source/assessment material.

## Release Checklist

- Definition Schema includes concept_id, term, course definition, not this, evidence anchor, and source boundary.
- Core Concepts include tokenization, embeddings, positions, RoPE, attention, masks, MHA/GQA/MLA, normalization, FFN, decoder-only LM, MoE, CE/PPL, AdamW, sampling, speculative decoding, SFT, LoRA, DPO, GRPO, KV cache, RAG, SLO, evaluation metrics, and source boundary.
- Every concept row has a misconception or overclaim boundary.
- Cross-Reference Map links terminology to notation, misconception, derivation, worked example, source, and assessment evidence.
- Definition Quality Rules cover mechanism, boundary, metric, frontier, and project terminology.
- Student site release excludes hidden tests, reference_solution.py, private grading samples, and real student submissions.
