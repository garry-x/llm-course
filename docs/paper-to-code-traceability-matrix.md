# Paper-to-Code Traceability Matrix

复核日期：2026-06-05

本矩阵把核心论文、官方技术报告和框架论文映射到课程章节、阅读周、数学推导、作业测试、项目证据和边界说明。它补充 [逐周阅读清单与复盘 Handout](reading-list.md)、[Reading Discussion Question Bank](reading-discussion-question-bank.md)、[Chapter Source and Accuracy Map](chapter-source-map.md)、[External Source Inventory](external-source-inventory.md)、[Mathematical Derivation Audit](mathematical-derivation-audit.md)、[Worked Example Pack](worked-example-pack.md)、[Assignment Handout Pack](assignment-handout-pack.md) 和 [Paper Recap Calibration Pack](paper-recap-calibration-pack.md)。目标是让教师和助教能回答三个问题：这篇论文支持哪个课程事实？学生在哪里把它落成代码或推导？哪些结论不能被过度外推？

## 使用规则

- 论文或报告只支撑其原文实验、公式、算法和发布日期内的主张；课程解释、简化实现和项目 benchmark 必须单独标注。
- 若某篇来源进入 quiz、书面题、作业 hidden tests、项目 rubric 或标准答案，必须至少有一个 `DER-xx`、assignment test、capstone gate 或 reading recap evidence。
- `A-stable` 来源可支撑基础理论；`A-volatile` 只支撑带日期的前沿报告事实；`B-implementation` 支撑框架行为和工程案例；`C-background` 只能作为学习资源。
- 每轮开课前，新增或替换论文时同步更新 source map、reading list、claim ledger、derivation audit、assignment handout 和 evidence manifest。

## Traceability Matrix

| ID | Source / paper | Source tier | Course anchor | Reading week | Derivation / concept evidence | Code or assessment evidence | Student deliverable | Boundary |
|----|----------------|-------------|---------------|--------------|-------------------------------|-----------------------------|---------------------|----------|
| P2C-01 | Sennrich et al. BPE rare words | A-stable | Ch01 Tokenization / BPE | Week 1 | DER-01 BPE merge objective and greedy boundary | `assignments/ch01_bpe/tests.py`; written BPE merge question | Reading recap explains rare-word motivation and one merge failure case | BPE frequency merge is not semantic segmentation or global compression optimum |
| P2C-02 | Mikolov word2vec and Pennington GloVe | A-stable | Ch02 Embedding / Position Encoding / RoPE | Week 1 | DER-02 embedding lookup and analogy caveat | `assignments/ch02_embeddings/tests.py`; Ch02 formula gate | Recap distinguishes training objective from vector analogy behavior | Analogy is empirical geometry, not a guaranteed linear semantic theorem |
| P2C-03 | Vaswani et al. Attention Is All You Need | A-stable | Ch03-Ch06 attention, MHA, Transformer block, decoder-only LM | Week 2 / Week 3 | DER-04 attention scaling; DER-05 causal mask; DER-06 MHA/GQA cache shapes | `assignments/ch03_attention/tests.py`; `assignments/ch04_multihead/tests.py`; `assignments/ch06_gpt/tests.py` | Handout answer derives `sqrt(d_k)` scaling and mask placement | Original paper does not validate every modern serving or alignment claim |
| P2C-04 | RoFormer / RoPE paper | A-stable | Ch02 RoPE and Ch04 positional handling | Week 3 | DER-03 relative rotation and norm preservation | `assignments/ch02_embeddings/tests.py`; Ch04 RoPE shape checks | Recap connects `R_m^T R_n = R_{n-m}` to relative positions | RoPE does not by itself guarantee long-context extrapolation; behavior depends on training distribution, frequencies and numerical range |
| P2C-05 | Ainslie et al. GQA | A-stable | Ch04 GQA / MQA KV cache tradeoff | Week 3 | DER-06 KV-head cache formula and expressivity boundary | `assignments/ch04_multihead/tests.py`; written KV cache ratio question | Paper-to-code drill maps KV heads to cache bytes | Cache savings do not imply quality is unchanged for all checkpoints or tasks |
| P2C-06 | DeepSeek-V2 MLA technical report | A-volatile | Ch04 MLA simplified latent cache | Week 3 | DER-06 MLA cache compression concept | `assignments/ch04_multihead/tests.py`; chapter claim ledger CH04-C02 | Recap marks report date and compares full MLA with teaching simplification | Teaching MLA is not production MLA and cannot reproduce report throughput |
| P2C-07 | Ba LayerNorm, Zhang RMSNorm, Shazeer SwiGLU | A-stable | Ch05 Transformer Block / Norm / FFN | Week 3 | DER-07 LayerNorm/RMSNorm dependency and FFN shape | `assignments/ch05_block/tests.py`; gradcheck notes | Written solution contrasts centering, RMS scaling and gated FFN capacity | These papers do not make one norm or FFN variant universally best; choices interact with depth, optimizer and initialization |
| P2C-08 | Radford et al. GPT-2 report | A-stable | Ch06 GPT Assembly / decoder-only objective | Week 4 | DER-08 next-token NLL and right-shift labels | `assignments/ch06_gpt_model/tests.py`; written objective question | Recap links autoregressive pretraining to label shift and causal mask | GPT-2 report does not describe modern chat alignment or API behavior |
| P2C-09 | Switch Transformer and DeepSeekMoE reports | A-stable / A-volatile | Ch06 MoE routing, capacity and load balancing | Week 4 | DER-09 router probability, capacity and auxiliary signal | `assignments/ch06_gpt_model/tests.py`; MoE router tests | Recap explains dropped tokens, capacity factor and load-balance evidence | Sparse activation does not make total training or serving cost linearly sparse |
| P2C-10 | Loshchilov AdamW, Chinchilla, ZeRO | A-stable | Ch07 Training Loop / scaling / distributed training | Week 5 | DER-10 CE and AdamW; scaling-law boundary | `assignments/ch07_training/tests.py`; training capstone acceptance | Training report includes optimizer update, data/parameter caveat and memory-state table | Scaling-law and ZeRO conclusions do not directly transfer to CPU toy models |
| P2C-11 | Holtzman nucleus sampling and speculative decoding papers | A-stable | Ch08 Generation / Search / Speculative Decoding | Week 6 | DER-11 top-p nucleus set; DER-12 speculative acceptance condition | `assignments/ch08_generation/tests.py`; decoding written questions | Recap compares top-k, top-p, temperature, draft quality and acceptance statistics | These papers do not guarantee better quality or speedup for every model; outcomes depend on model distribution and workload bottleneck |
| P2C-12 | LoRA, DPO, DeepSeek-R1 / GRPO | A-stable / A-volatile | Ch09 Fine-tuning / Alignment | Week 7 | DER-14 DPO log-ratio and GRPO whitening | `assignments/ch09_alignment/tests.py`; alignment written question | Recap separates LoRA parameter efficiency, DPO reference model and GRPO report claim | These methods do not solve safety alignment by themselves |
| P2C-13 | Kwon PagedAttention, Dao FlashAttention, Lewis RAG, Dettmers QLoRA | A-stable / B-implementation | Ch10 Inference / RAG / Serving | Week 9 | DER-13 KV cache memory; retrieval/evaluation concepts | `assignments/ch10_inference/tests.py`; inference capstone benchmark and SLO report | Project report records hardware, workload, retrieval metrics and serving SLO | These sources do not provide universal throughput, memory or quality claims; all results are configuration-specific |
| P2C-14 | Chen-Manning parser, Sutskever seq2seq, Devlin BERT, BLEU/ROUGE, foundation risks | A-stable | Classic NLP and evaluation专题 / Ch11 | Week 8 | DER-14 evaluation and masked-label concept links | `assignments/ch11_classic_nlp/tests.py`; written evaluation questions | Recap explains one classic architecture, one metric limitation and one risk category | Classic metrics and encoder-only objectives do not directly prove open-ended LLM quality |

## Coverage Requirements

| Requirement | Minimum evidence |
|-------------|------------------|
| Source coverage | At least one `A-stable` source for each stable theory chapter; every `A-volatile` model report has a date-sensitive boundary |
| Chapter coverage | Ch01-Ch10 plus classic NLP / Ch11 each appear in at least one row |
| Reading coverage | Week 1-9 appear in at least one row; Week 10 uses the matrix through capstone source audit |
| Derivation coverage | DER-01 through DER-14 appear across rows or linked concept evidence |
| Code coverage | Each assignment suite `ch01_bpe` through `ch11_classic_nlp` appears in at least one row |
| Assessment coverage | At least one row maps to written questions, one to reading recap, one to capstone evidence and one to project report |
| Boundary coverage | Every row states what the source does not prove |

## Instructor Review Protocol

1. Before publishing a reading, locate its row or add a new `P2C-xx` row with source tier, reading week, course anchor and boundary.
2. Before adding a quiz or written problem, confirm the tested claim appears in a row with `DER-xx` or assignment evidence.
3. Before updating a chapter, compare the chapter's source map row with this matrix and the [Chapter Claim Audit Ledger](chapter-claim-audit-ledger.md).
4. Before accepting a project report citation, check that the source tier and boundary match [External Source Inventory](external-source-inventory.md) and [Paper Recap Calibration Pack](paper-recap-calibration-pack.md).
5. When a frontier report changes, mark affected rows as `A-volatile`, update access dates in the relevant source audit, and avoid turning reported benchmark values into course-wide facts.

## Release Checklist

| Check | Passing evidence |
|-------|------------------|
| Matrix rows | `P2C-01` through `P2C-14` are present and have 9 populated fields |
| Source tiers | Rows use only `A-stable`, `A-volatile`, `B-implementation`, or `C-background` combinations |
| DER coverage | `DER-01` through `DER-14` are discoverable |
| Assignment coverage | `assignments/ch01_bpe` through `assignments/ch11_classic_nlp` are discoverable |
| Link coverage | README, syllabus, source map, reading list and evidence manifest link this matrix |
| Verification | `.venv/bin/python verify_course.py` reports `PASS paper-to-code traceability matrix ...` |
