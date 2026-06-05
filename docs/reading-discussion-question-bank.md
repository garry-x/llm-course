# Reading Discussion Question Bank

复核日期：2026-06-05

本题库把 [逐周阅读清单与复盘 Handout](reading-list.md) 中的论文、教材和工程文档转化为可用于课堂讨论、reading recap、paper-to-code drill、quiz/checkpoint 和 capstone proposal review 的问题。它补充 [Paper Recap Calibration Pack](paper-recap-calibration-pack.md)、[Paper-to-Code Traceability Matrix](paper-to-code-traceability-matrix.md)、[Topic Dependency and Spiral Review Map](topic-dependency-map.md)、[Safety and Societal Impact Casebook](safety-societal-impact-casebook.md)、[Model and Benchmark Card Guide](model-benchmark-card-guide.md)、[Assessment Blueprint and Coverage Matrix](assessment-blueprint-coverage-matrix.md)、[Participation and Feedback Guide](participation-feedback-guide.md)、[Recitation Worksheet Pack](recitation-worksheet-pack.md)、[Chapter Source and Accuracy Map](chapter-source-map.md) 和 [External Source Verification Guide](external-source-verification.md)。

使用边界：本题库是学生可见材料，可以进入 student site release；不得包含隐藏测试输入、reference_solution.py、私有评分样例、真实学生提交、未公开项目 idea 或教师答案要点。

## Question Schema

| field | requirement |
| --- | --- |
| question_id | Stable `RDQ-W*-*` identifier. |
| week | Reading week from the reading list. |
| reading_anchor | Paper, textbook, official doc, or source-audit object. |
| question_type | claim, mechanism, limitation, paper_to_code, metric, project, or ethics. |
| prompt | Student-facing discussion or recap question. |
| expected_evidence | What a strong answer must cite or compute. |
| course_link | Chapter, DER, worked example, assignment, capstone, or source document. |

## Core Question Bank

| question_id | week | reading_anchor | question_type | prompt | expected_evidence | course_link |
| --- | --- | --- | --- | --- | --- | --- |
| RDQ-W0-CLAIM | Week 0 | Deep Learning textbook and prerequisite bridge | claim | When a training objective improves but the validation metric worsens, what claim can and cannot be made about learning? | Distinguish optimization objective, validation metric, generalization claim, and evidence split. | ml-foundations-prerequisite-bridge.md, experimental-rigor-evaluation-statistics.md |
| RDQ-W0-PROJECT | Week 0 | Prerequisite Diagnostic | project | Which prerequisite failure would most endanger a capstone report: tensor axes, probability, gradients, or reproducible commands? | Name the failure, show how it affects evidence, and choose a remediation path. | prerequisite-diagnostic.md, topic-dependency-map.md |
| RDQ-W1-MECH | Week 1 | Sennrich et al. BPE | mechanism | Why does BPE help rare-word modeling while still producing token boundaries that may not match morphology? | Explain greedy merge counts, corpus dependence, OOV reduction, and a failure example. | Ch01, WE-CH01-BPE, assignments/ch01_bpe |
| RDQ-W1-CLAIM | Week 1 | word2vec and GloVe | limitation | Are analogy directions guaranteed by the training objective, or are they empirical structure in a trained space? | State the objective, the empirical evaluation setting, and the unsupported stronger claim. | Ch02, core-concept-glossary.md |
| RDQ-W2-MECH | Week 2 | Attention Is All You Need | mechanism | Derive why scaled dot-product attention divides scores by `sqrt(d_k)` under a variance assumption. | Include independence/variance assumptions, score variance, and softmax saturation risk. | Ch03, DER-04, WE-CH03-ATTN |
| RDQ-W2-CODE | Week 2 | Attention Is All You Need | paper_to_code | Where should a causal mask be applied in a minimal attention implementation, and what breaks if it is applied after softmax incorrectly? | Show score matrix, mask polarity, softmax effect, and value aggregation consequence. | Ch03, MASK-CAUSAL, assignments/ch03_attention |
| RDQ-W3-MECH | Week 3 | GQA paper | mechanism | How does reducing KV heads save cache memory, and what representational tradeoff should be stated? | Compare query heads, KV heads, cache tensor shape, and non-guaranteed quality. | Ch04, DER-06, WE-CH04-GQA |
| RDQ-W3-LIMIT | Week 3 | DeepSeek-V2 MLA | limitation | Which MLA claims are stable architectural ideas, and which performance claims depend on the reported system setting? | Separate latent cache mechanism from benchmark, hardware, implementation, and date-bound claims. | chapter-source-map.md, frontier-source-audit.md |
| RDQ-W4-CLAIM | Week 4 | GPT-2 and Switch Transformer | claim | What makes a model decoder-only, and why does MoE total parameter count differ from activated parameter count? | Identify causal objective, next-token labels, routing, capacity, and activated experts. | Ch06, CG-DECODER-LM, CG-MOE |
| RDQ-W4-CODE | Week 4 | Switch Transformer | paper_to_code | If a router overloads one expert, which evidence would show a capacity or balancing bug? | Use token counts per expert, dropped tokens or capacity pressure, and balancing signal. | assignments/ch06_gpt, concept-misconception-map.md |
| RDQ-W5-MECH | Week 5 | AdamW | mechanism | Why is AdamW not equivalent to adding L2 penalty inside Adam's adaptive gradient update? | Show decoupled decay, adaptive moments, parameter update order, and failure of the synonym. | Ch07, DER-10, WE-CH07-ADAMW |
| RDQ-W5-LIMIT | Week 5 | Chinchilla and ZeRO | limitation | What part of a scaling-law or distributed-training paper can be used as course evidence without copying its numeric result as a universal fact? | Include source setting, data/parameter tradeoff, hardware/software assumptions, and unsupported extrapolation. | chapter-claim-audit-ledger.md, external-source-verification.md |
| RDQ-W6-MECH | Week 6 | Nucleus Sampling | mechanism | Why is top-p not a fixed number of tokens, and how does temperature interact with the filtered distribution? | Sort probabilities, accumulate mass, identify nucleus, then discuss distribution reshaping. | Ch08, WE-CH08-TOPP, assignments/ch08_generation |
| RDQ-W6-LIMIT | Week 6 | Speculative Decoding | limitation | Under what workload or draft-model conditions would speculative decoding fail to improve wall-clock latency? | Discuss acceptance rate, target bottleneck, draft cost, batch/context, and verification overhead. | Ch08, topic-dependency-map.md |
| RDQ-W7-MECH | Week 7 | DPO | mechanism | Why does DPO compare policy-reference log-probability ratios for chosen and rejected responses? | Identify chosen, rejected, policy, reference, beta, and preference margin. | Ch09, DER-12, WE-CH09-DPO |
| RDQ-W7-SOURCE | Week 7 | DeepSeek-R1 and GRPO | limitation | How should a reading recap state GRPO reasoning claims without turning a model report into a general proof? | Include source tier, task setting, sampling assumptions, observed behavior, and unsupported stronger claim. | frontier-source-audit.md, paper-recap-calibration-pack.md |
| RDQ-W8-METRIC | Week 8 | BERT, BLEU, ROUGE, parsing metrics | metric | Why do MLM accuracy, UAS/LAS, BLEU, ROUGE, EM and F1 each need a fixed input/output contract before comparison? | State label convention, aggregation, denominator, and at least one metric failure mode. | Ch11, WE-CH11-METRICS, nlp-evaluation-coverage.md |
| RDQ-W8-ETHICS | Week 8 | Foundation model risk report | ethics | What makes a safety or ethics claim auditable rather than a generic statement of concern? | Name risk category, affected setting, evidence source, mitigation, and residual uncertainty. | data-ethics-review.md, chapter-source-map.md |
| RDQ-W9-SYSTEMS | Week 9 | PagedAttention and FlashAttention | mechanism | How do KV-cache paging and IO-aware attention target different bottlenecks in inference? | Contrast memory fragmentation, bandwidth/IO, attention computation, batch/context, and hardware assumptions. | Ch10, WE-CH10-KVCACHE, inference capstone |
| RDQ-W9-RAG | Week 9 | RAG paper and serving docs | metric | Why is retrieval hit rate insufficient evidence for RAG answer quality? | Include retriever metric, generator metric, grounding check, source freshness, and failure example. | Ch10, CG-RAG, project-report-template.md |
| RDQ-W10-PROJECT | Week 10 | Capstone sources | project | Which single claim in your capstone most needs source-boundary language, and what evidence would make it defensible? | Provide claim, source record, experiment condition, metric, uncertainty, and unsupported stronger claim. | project-report-template.md, claim-audit-worksheet.md |
| RDQ-W10-AUDIT | Week 10 | External source verification | limitation | When a model card, benchmark, API doc, or paper changes after your access date, how should your final report handle it? | State access date, volatile source status, rerun or downgrade rule, and citation update path. | external-source-verification.md, frontier-source-audit.md |

## Discussion Formats

| format_id | use_when | student_output | staff_check |
| --- | --- | --- | --- |
| RDQ-F-PAIR | Pair discussion before lecture derivation | one claim, one evidence sentence, one uncertainty | TA checks that the answer cites the reading anchor and course link. |
| RDQ-F-BOARD | Board or shared-doc derivation | formula, shape, or metric contract written step by step | Instructor checks assumptions and unsupported extrapolation. |
| RDQ-F-RECITATION | Paper-to-code drill | function, tensor, test category, or capstone module linked to the reading | TA checks the link against traceability matrix rows. |
| RDQ-F-RECAP | Individual reading recap | source_record, core_claim, technical_detail, course_link, boundary, discussion_question | Graded with paper recap calibration pack. |
| RDQ-F-PROJECT | Capstone proposal or milestone clinic | claim, source tier, metric, fallback, and risk boundary | Mentor checks feasibility and source boundary before approving scope. |

## Assessment Sampling Rules

| rule_id | rule | failure_prevented |
| --- | --- | --- |
| RDQ-R1 | Each week should sample at least one mechanism question and one limitation/source-boundary question. | Students only summarize papers without technical or audit evidence. |
| RDQ-R2 | A quiz item derived from this bank must cite the question_id and preserve the same source boundary. | Assessment asks a stronger claim than the reading supports. |
| RDQ-R3 | A paper-to-code drill must name a chapter, DER, assignment, worked example, or capstone module. | Reading discussion floats without implementation evidence. |
| RDQ-R4 | Frontier model questions must include source tier and review date before entering graded work. | Volatile claims become unqualified course facts. |
| RDQ-R5 | A project clinic question must end with a measurable claim, a metric contract, or a scope downgrade. | Capstone feedback stays generic and cannot guide revision. |

## Maintenance Workflow

1. When reading-list.md changes, add or update at least one `RDQ-*` row for every affected week.
2. When a paper recap anchor reveals a common weakness, add a matching mechanism, limitation, or source-boundary question.
3. When a chapter source boundary changes, update the corresponding `expected_evidence` and `course_link` cells before the question is reused.
4. When a question becomes an active quiz or exam item, record only the question_id and learning objective in public materials; keep the exact active assessment in the appropriate assessment policy boundary.
5. Run `.venv/bin/python verify_course.py` after editing this bank, reading-list.md, paper recap calibration, traceability matrix, or source verification docs.

## Release Checklist

- Question Schema includes question_id, week, reading_anchor, question_type, prompt, expected_evidence, and course_link.
- Core Question Bank covers Week 0 through Week 10 and includes claim, mechanism, limitation, paper_to_code, metric, project, and ethics questions.
- Every question has expected evidence and a course link.
- Discussion Formats cover pair discussion, board derivation, recitation drill, reading recap, and project clinic.
- Assessment Sampling Rules prevent unsupported source claims, implementation-free discussion, and unqualified frontier facts.
- Maintenance Workflow links updates to reading-list.md, paper recap anchors, source boundaries, active assessment boundaries, and `.venv/bin/python verify_course.py`.
- This bank is included in the student site release and excludes hidden tests, reference_solution.py, private grading samples, and real student submissions.
