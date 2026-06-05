# Topic Dependency and Spiral Review Map

复核日期：2026-06-05

本地图把课程核心概念组织成 prerequisite graph、chapter unlock path 和 spiral review schedule。它补充 [Core Concept Glossary](core-concept-glossary.md)、[Notation and Shape Glossary](notation-shape-glossary.md)、[Worked Example Pack](worked-example-pack.md)、[Concept Mastery and Misconception Map](concept-misconception-map.md)、[Comprehensive Review Study Guide](comprehensive-review-study-guide.md)、[Course Outcome Map](course-outcome-map.md)、[Assessment Blueprint and Coverage Matrix](assessment-blueprint-coverage-matrix.md)、[Learning Analytics and Remediation Plan](learning-analytics-remediation-plan.md)、[Recitation Worksheet Pack](recitation-worksheet-pack.md)、[Chapter Source and Accuracy Map](chapter-source-map.md) 和 [Paper-to-Code Traceability Matrix](paper-to-code-traceability-matrix.md)。目标是让学生知道：进入某章前必须会什么，本章解锁后续哪些任务，若某个依赖断裂应回到哪份例题、符号表或补救路径。

## Dependency Layers

| layer_id | concepts | depends_on | evidence | failure_if_missing |
| --- | --- | --- | --- | --- |
| TD-L0-PREREQ | Python tensor indexing, matrix multiplication, gradients, probability, reproducible commands | none inside course; checked by prerequisite diagnostic | prerequisite-diagnostic.md, math-prerequisites.md, python-pytorch-review-session.md | Students cannot interpret batch, sequence, vocabulary, hidden dimension, seed, or loss trace. |
| TD-L1-TOKEN | BPE, vocabulary, token ids, embedding lookup, position information | TD-L0-PREREQ | Ch01-Ch02, CG-TOKEN-BPE, CG-EMBED, WE-CH01-BPE, WE-CH02-ROPE | Students treat tokens as words or embeddings as semantic facts instead of trainable numeric representations. |
| TD-L2-ATTN | query/key/value projections, scaled scores, causal mask, softmax, value mixing | TD-L1-TOKEN | Ch03, CG-ATTN, CG-CAUSAL-MASK, NS-03, WE-CH03-ATTN | Students cannot locate whether an error is in score scaling, mask polarity, or value aggregation. |
| TD-L3-BLOCK | MHA, GQA, RoPE in attention, residual stream, normalization, FFN | TD-L2-ATTN | Ch04-Ch05, CG-GQA, CG-LAYERNORM, CG-RMSNORM, WE-CH04-GQA, WE-CH05-NORM | Students memorize Transformer labels but cannot trace tensor shapes through a block. |
| TD-L4-LM | decoder-only stack, logits, cross entropy, perplexity, parameter accounting, MoE routing | TD-L3-BLOCK | Ch06-Ch07, CG-DECODER-LM, CG-MOE, CG-CE-PPL, WE-CH06-PARAMS | Students confuse model family, objective, metric, and capacity accounting. |
| TD-L5-TRAIN | optimizer states, AdamW, batching, checkpointing, eval loop, reproducibility evidence | TD-L4-LM | Ch07, training capstone, WE-CH07-ADAMW, experimental-rigor-evaluation-statistics.md | Students can run a script but cannot explain why a result is valid or reproducible. |
| TD-L6-GEN-ALIGN | top-k, top-p, temperature, SFT masks, LoRA, preference pairs, DPO, GRPO boundary | TD-L5-TRAIN | Ch08-Ch09, CG-SAMPLING, CG-SFT, CG-LORA, CG-DPO, WE-CH08-TOPP, WE-CH09-DPO | Students overclaim generation quality or alignment from a single objective or sample. |
| TD-L7-EVAL-SERVE | KV cache, batching, throughput, latency percentiles, SLO, RAG evidence, task metrics | TD-L6-GEN-ALIGN plus TD-L3-BLOCK | Ch10-Ch11, CG-KVCACHE, CG-RAG, CG-SLO, CG-EVAL-METRIC, WE-CH10-KVCACHE, WE-CH11-METRICS | Students report averages or retrieval hits without workload, metric contract, or source boundary. |
| TD-L8-CAPSTONE | scoped experiment, baseline, fixed eval set, source boundary, cost and failure analysis | TD-L7-EVAL-SERVE | project-report-template.md, project-report-rubric.md, capstone-proposal-milestone.md | Students produce demos without audit-ready evidence, reproducibility, or defensible claims. |

## Chapter Dependency Graph

| graph_id | chapter | depends_on | unlocks | evidence | remediation |
| --- | --- | --- | --- | --- | --- |
| TD-CH01 | Ch01 Tokenization and BPE | TD-L0-PREREQ | Ch02 embeddings, Ch06 LM input pipeline | WE-CH01-BPE, CG-TOKEN-BPE, assignment ch01 | revisit prerequisite diagnostic and BPE worked example |
| TD-CH02 | Ch02 Embeddings and Positions | Ch01, TD-L1-TOKEN | Ch03 attention, Ch04 RoPE in attention | WE-CH02-ROPE, CG-EMBED, CG-ROPE, NS-02 | revisit notation rows for E, positions, q and k shapes |
| TD-CH03 | Ch03 Attention | Ch02, TD-L2-ATTN | Ch04 MHA/GQA, Ch05 Transformer block, Ch06 decoder LM | WE-CH03-ATTN, MASK-CAUSAL, DER-04 | run attention mask drill and write one score matrix by hand |
| TD-CH04 | Ch04 Multi-Head Attention | Ch03, Ch02 RoPE | Ch05 block, Ch10 KV cache accounting | WE-CH04-GQA, CG-GQA, CG-MLA, DER-06 | compare query heads and KV heads before coding cache logic |
| TD-CH05 | Ch05 Transformer Block | Ch03 attention, Ch04 heads | Ch06 GPT, Ch07 training stability | WE-CH05-NORM, CG-LAYERNORM, CG-FFN | redo residual, norm, and FFN shape trace before debugging gradients |
| TD-CH06 | Ch06 GPT and MoE | Ch05, Ch01-Ch03 data flow | Ch07 training, Ch08 generation, Ch09 adaptation | WE-CH06-PARAMS, CG-DECODER-LM, CG-MOE | separate model family, parameter count, and objective vocabulary |
| TD-CH07 | Ch07 Training | Ch06 logits and loss | Ch08 decoding experiments, Ch09 alignment, training capstone | WE-CH07-ADAMW, CG-CE-PPL, CG-ADAMW | rerun seed, loss, eval split, and optimizer state explanation |
| TD-CH08 | Ch08 Generation | Ch07 probability distribution and eval loop | Ch09 preference learning, Ch10 serving evaluation | WE-CH08-TOPP, CG-SAMPLING, speculative decoding tests | compare filtered probability mass before interpreting quality |
| TD-CH09 | Ch09 Fine-Tuning and Alignment | Ch07 training, Ch08 generation samples | alignment projects, safety and source-boundary critique | WE-CH09-DPO, CG-SFT, CG-LORA, CG-DPO | check label masks, reference model role, and unsupported safety claims |
| TD-CH10 | Ch10 Inference Systems and RAG | Ch04 KV geometry, Ch08 generation | inference capstone, SLO report | WE-CH10-KVCACHE, CG-KVCACHE, CG-RAG, CG-SLO | compute cache memory and latency metric definitions before tuning |
| TD-CH11 | Ch11 Classic NLP and Evaluation | Ch03 structured scoring, Ch08 metrics, source boundary rules | evaluation critique, final project metric section | WE-CH11-METRICS, CG-EVAL-METRIC, nlp-evaluation-coverage.md | state metric contract, aggregation, and failure mode before comparing systems |

## Spiral Review Schedule

| review_id | week | review_focus | new_topic | reactivated_prior_concept | quick_evidence |
| --- | --- | --- | --- | --- | --- |
| TD-SR-W1 | Week 1 | token ids, tensor axes, reproducible commands | BPE and embeddings | prerequisites from TD-L0-PREREQ | Ch01 quiz plus WE-CH01-BPE trace |
| TD-SR-W2 | Week 2 | position and shape notation | RoPE and scaled attention | Ch01 vocabulary and embedding lookup | Ch02-Ch03 worksheet shape table |
| TD-SR-W3 | Week 3 | causal mask and value mixing | MHA, GQA, Transformer block | Ch03 score matrix and mask polarity | attention and GQA recitation drill |
| TD-SR-W4 | Week 4 | residual, normalization, logits | GPT and MoE | Ch05 block shape invariants | parameter-count worked example and quiz |
| TD-SR-W5 | Week 5 | CE/PPL and optimizer state | AdamW and training loop | Ch06 logits, labels, and loss masks | training assignment test categories |
| TD-SR-W6 | Week 6 | probability filtering | top-k, top-p, speculative decoding | CE distribution and eval split | WE-CH08-TOPP plus decoding failure drill |
| TD-SR-W7 | Week 7 | label masks and preference pairs | SFT, LoRA, DPO, GRPO boundary | Ch07 training reproducibility | WE-CH09-DPO and paper recap boundary |
| TD-SR-W8 | Week 8 | cache shape and workload metrics | KV cache, batching, SLO, RAG | Ch04 heads and Ch08 generation | WE-CH10-KVCACHE plus SLO worksheet |
| TD-SR-W9 | Week 9 | metric contract and error analysis | classic NLP metrics and evaluation critique | source boundary and fixed eval set | WE-CH11-METRICS plus project metric check |
| TD-SR-W10 | Week 10 | claim audit and reproducibility | capstone presentation and final report | all prior layers TD-L1 through TD-L8 | project report rubric and source audit |

## Dependency Failure Signals

| failure_id | signal | likely_broken_dependency | immediate_action | staff_follow_up |
| --- | --- | --- | --- | --- |
| TD-F-SHAPE | Student cannot write input/output shapes for a module row. | TD-L0-PREREQ or TD-L1-TOKEN | Use notation-shape-glossary.md and fill a recitation shape table. | Trigger TR-SHAPE-30 when the pattern appears in aggregate. |
| TD-F-MASK | Student applies causal, padding, or label mask at the wrong stage. | TD-L2-ATTN or TD-L6-GEN-ALIGN | Build a two-token or two-example minimal counterexample. | Trigger TR-MASK-20 and publish a mask drill. |
| TD-F-OBJECTIVE | Student confuses CE, perplexity, SFT, DPO, or GRPO. | TD-L4-LM through TD-L6-GEN-ALIGN | Compare the exact log-probability terms and ignored tokens. | Route to concept-misconception-map.md objective checks. |
| TD-F-METRIC | Student reports quality, latency, retrieval, or BLEU/F1 without a metric contract. | TD-L7-EVAL-SERVE | State unit, aggregation, workload, and failure mode. | Route to assessment blueprint and experimental rigor review. |
| TD-F-SOURCE | Student cites a paper, benchmark, model card, or API doc beyond what it supports. | TD-L8-CAPSTONE source boundary | Fill supported claim and unsupported stronger claim. | Trigger TR-SOURCE-30 when paper recaps show repeated gaps. |
| TD-F-SYSTEMS | Student optimizes throughput, memory, or cost without cache, batch, dtype, or SLO context. | TD-L7-EVAL-SERVE | Recompute KV cache memory and latency percentile definitions. | Route to inference capstone mentor check. |

## Student Navigation Rules

1. If RoPE is blocked, revisit Ch02, CG-ROPE, NS-02, WE-CH02-ROPE, then explain which paired dimensions rotate and what the source boundary does not prove.
2. If attention mask is blocked, revisit Ch03, MASK-CAUSAL, WE-CH03-ATTN, then write a score matrix before running code.
3. If training loss is blocked, revisit Ch06 logits, Ch07 CE/PPL, NS label rows, WE-CH07-ADAMW, then separate model output, target labels, ignored tokens, and optimizer update.
4. If alignment is blocked, revisit Ch08 sampling, Ch09 SFT/DPO, WE-CH09-DPO, then identify chosen, rejected, policy, reference, and beta before making quality claims.
5. If serving evaluation is blocked, revisit Ch04 head geometry, Ch10 KV cache, WE-CH10-KVCACHE, then state batch, context, dtype, layers, heads, and latency percentile.
6. If project evidence is blocked, revisit TD-L8-CAPSTONE, project-report-template.md, experimental-rigor-evaluation-statistics.md, and chapter-source-map.md before revising a claim.

## Staff Review Workflow

1. Before a module starts, compare the upcoming chapter row with quiz and assignment results from the previous week.
2. During recitation, use the relevant failure signal row to select one shape, mask, objective, metric, source, or systems drill.
3. After grading, map repeated failures to Learning Analytics trigger IDs, then record only aggregate actions in public updates.
4. When a chapter, assignment, metric, or paper recap changes, update the corresponding TD-L, TD-CH, and TD-SR rows in the same change.
5. Before release, run `.venv/bin/python verify_course.py` and confirm this document is included in the student site release without hidden tests, reference_solution.py, private grading samples, or real student submissions.

## Release Checklist

- Dependency Layers cover prerequisites, tokenization, attention, block architecture, LM/training, generation/alignment, evaluation/serving, and capstone evidence.
- Chapter Dependency Graph has rows TD-CH01 through TD-CH11 with depends_on, unlocks, evidence, and remediation.
- Spiral Review Schedule has rows TD-SR-W1 through TD-SR-W10 and reactivates prior concepts each week.
- Dependency Failure Signals cover shape, mask, objective, metric, source, and systems failures.
- Student Navigation Rules point to glossary, notation, worked example, assessment, and source-boundary materials.
- Staff Review Workflow connects aggregate failures to learning analytics without exposing hidden tests or private records.
- This map is included in the student site release and evidence manifest.
