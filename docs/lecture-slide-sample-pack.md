# Lecture Slide Sample Pack

复核日期：2026-06-05

本文件提供学生可见的 slide deck 样例，用于说明正式 slides 应如何把 learning goals、visual plan、formula/shape、demo cue、quick check、accessibility text 和 source boundary 放在同一份课件中。它补充 [Lecture Slide Outline](lecture-slide-outline.md)、[Lecture Note Sample Pack](lecture-note-sample-pack.md)、[Lecture Notes Quality and Review Standard](lecture-notes-quality-review.md)、[Course Materials Index](course-materials-index.md)、[Classroom Demo Runbook](demo-runbook.md)、[Recitation Worksheet Pack](recitation-worksheet-pack.md) 和 [Paper-to-Code Traceability Matrix](paper-to-code-traceability-matrix.md)。

适用范围：正式 PDF/HTML slides 制作、课前审稿、课后替代材料、助教讨论课 recap。
使用原则：样例不替代 20 讲完整 slides；它定义可发布 slide 的质量形状。正式发布 slides 时，应在 [Course Materials Index](course-materials-index.md) 记录 version、audience、accessibility alternative 和 validation command。

## Slide Sample Rubric

| Field | Required evidence |
|-------|-------------------|
| Deck metadata | lecture id、topic、mapped chapters、reading week、assignment evidence |
| Learning goals | 2-4 个可测目标，能映射到 outcome、assignment 或 capstone |
| Slide sequence | 8-12 张代表性 slide，含 opening、concept、math、code/demo、check、evidence |
| Visual plan | 每张 slide 说明图、表、公式或代码如何呈现 |
| Speaker note | 说明教师讲解重点和不能省略的边界 |
| Accessibility text | 对颜色、图、公式或动画提供文字替代 |
| Source boundary | 区分论文事实、课程解释、模型卡/benchmark 条件 |
| Quick check | 至少一道课堂可评分题或 exit ticket |
| Post-lecture evidence | 对应作业、worksheet、reading recap、quiz 或 capstone artifact |

## Sample Deck S1: L2 Embeddings, Word Vectors, RoPE

Deck metadata: L2, Ch02, Reading Week 1, `assignments/ch02_embeddings/`, DER-02, DER-03.

Learning goals:

- Explain embedding lookup as indexed matrix rows, not a semantic guarantee.
- Distinguish word2vec/GloVe analogy behavior from their training objectives.
- Show RoPE as paired rotations that preserve norm and induce relative-position dot products.

Slide sequence:

| Slide | Type | Visual plan | Speaker note | Accessibility text |
|-------|------|-------------|--------------|--------------------|
| S1.1 | Opening | Three boxes: token id -> embedding row -> position-augmented vector | Connect Ch01 token ids to Ch02 vectors | Text lists the three-step data flow |
| S1.2 | Concept | Small embedding matrix with highlighted rows | Emphasize lookup shape `[B,T] -> [B,T,D]` | Matrix values also described in caption |
| S1.3 | Boundary | Two-column table: training objective vs analogy observation | State that analogy is empirical geometry, not a theorem | Table text contains full claim |
| S1.4 | Math | `one_hot @ E` and indexed lookup equivalence | Keep dimensions visible: `[B,T,V] @ [V,D]` | Formula repeated in alt text |
| S1.5 | RoPE visual | Pairwise 2D rotation blocks for head dim 8 | Show why odd head dimension is invalid | Each pair is labeled `(0,1)`, `(2,3)` |
| S1.6 | Relative property | `R_m^T R_n = R_{n-m}` with a short derivation | Do not claim monotonic distance decay | Boundary sentence printed on slide |
| S1.7 | Demo cue | Command `.venv/bin/python assignments/ch02_embeddings/tests.py` | Point to norm preservation and Toeplitz tests | Command and expected test names shown as text |
| S1.8 | Quick check | Given `B=2,T=4,V=100,D=16`, ask for lookup output shape | Score only shape and axis meanings | Question is text-only |
| S1.9 | Evidence | Assignment + reading recap + DER links | Students submit RoPE boundary explanation | Links are written out in slide notes |

Source boundary: word vector papers support learned representation objectives and empirical analogy behavior; they do not prove semantic relations are always linear. RoPE supports relative rotation structure; it does not by itself guarantee long-context extrapolation.

Post-lecture evidence:

- Ch02 public tests.
- Recitation Worksheet W1 shape table.
- Reading recap comparing training objective and analogy claim.

## Sample Deck S2: L5 Multi-Head Attention and GQA

Deck metadata: L5, Ch04, Reading Week 3, `assignments/ch04_multihead/`, DER-06, P2C-05.

Learning goals:

- Trace MHA reshape from `[B,T,d_model]` to `[B,H,T,D_h]`.
- Compare MHA, MQA and GQA KV cache storage.
- Explain why reducing KV heads is an efficiency/quality tradeoff, not a free improvement.

Slide sequence:

| Slide | Type | Visual plan | Speaker note | Accessibility text |
|-------|------|-------------|--------------|--------------------|
| S2.1 | Opening | Pipeline: input -> Q/K/V projections -> heads -> output projection | Anchor to Ch03 attention | Pipeline also listed as ordered text |
| S2.2 | Shape | Table of Q/K/V tensor shapes | Require students to name every axis | Table has no color-only encoding |
| S2.3 | Concept | Side-by-side head diagrams for MHA/MQA/GQA | Show which heads are shared | Caption states "Q heads are not reduced in GQA" |
| S2.4 | Formula | KV cache element count formula | Include batch, layer, seq, K/V factor and dtype | Formula variables defined below |
| S2.5 | Worked example | `n_heads=16,n_kv_heads=4,head_dim=64` cache ratio | Compute savings step by step | All numbers printed, not only arrows |
| S2.6 | Failure case | "GQA cache did not shrink" debug tree | First check: K/V projection output heads | Tree represented as bullet list |
| S2.7 | Demo cue | Ch04 tests: GQA grouping and cache size ratios | Do not reveal hidden tests | Public test category names only |
| S2.8 | Quick check | Ask whether reducing Q heads is GQA | Expected answer: no, that changes query capacity | Answer boundary is in speaker note, not on slide |
| S2.9 | Evidence | Assignment, written KV ratio question, paper-to-code row | Connect to P2C-05 | Links written as filenames |

Source boundary: GQA supports reducing KV heads as an inference-efficiency strategy. It does not imply all checkpoints preserve quality after head sharing, and it does not make attention computation free.

Post-lecture evidence:

- Ch04 public tests.
- Recitation Worksheet W3.
- Written KV cache ratio question.

## Sample Deck S3: L10 Training Loop, Checkpoint, Scaling

Deck metadata: L10, Ch07, Reading Week 5, `assignments/ch07_training/`, training capstone, DER-10.

Learning goals:

- Connect next-token labels, cross entropy and perplexity.
- Explain why AdamW decouples weight decay from Adam's adaptive gradient step.
- Identify what must be saved for checkpoint/resume evidence.

Slide sequence:

| Slide | Type | Visual plan | Speaker note | Accessibility text |
|-------|------|-------------|--------------|--------------------|
| S3.1 | Opening | Training loop cycle: batch -> forward -> loss -> backward -> optimizer -> eval | Keep CPU baseline framing | Cycle also appears as numbered list |
| S3.2 | Data | Shifted sequence table for `x` and `y` | Stress equal length, right-shift target | Table text gives each token position |
| S3.3 | Math | CE formula and logits/labels flatten shape | Explain ignore index before gather | Formula variables defined in text |
| S3.4 | Optimizer | AdamW one-step scalar example | Contrast with L2 inside Adam gradient | Update components listed separately |
| S3.5 | Scheduler | Warmup + cosine plot sketch | Point out boundary steps | Plot also described by three phases |
| S3.6 | Checkpoint | Table: model, optimizer, scheduler, step, config, seed | Resume without optimizer state is incomplete | Table usable without color |
| S3.7 | Failure case | Loss spike triage: data, lr, dtype, grad norm, logging | Require command and log evidence | Bullet list includes minimal evidence |
| S3.8 | Demo cue | Training capstone acceptance and Ch07 tests | Read logs, do not chase final toy loss | Command and expected artifacts shown |
| S3.9 | Quick check | "PPL=1 means what, and why is it not a factuality metric?" | Score limiting-case reasoning and boundary | Text-only prompt |
| S3.10 | Evidence | Training proposal checklist | Link seed/log/checkpoint/cost to capstone rubric | Checklist is textual |

Source boundary: AdamW paper supports decoupled weight decay; Chinchilla and ZeRO support scaling/memory principles under stated assumptions. Toy CPU training evidence does not prove large-model training performance.

Post-lecture evidence:

- Ch07 public tests.
- Training capstone proposal.
- Workload and pacing Week 5 planning note.

## Sample Deck S4: L18 Serving, Benchmark, SLO, Capacity

Deck metadata: L18, Ch10, Reading Week 9, `assignments/ch10_inference/`, inference capstone, DER-13.

Learning goals:

- Estimate KV cache memory with batch, layers, context, KV heads, head dim and dtype.
- Distinguish TTFT, TPOT, P50/P95/P99, tokens/s and error rate.
- Explain why RAG and serving benchmark claims are configuration-specific.

Slide sequence:

| Slide | Type | Visual plan | Speaker note | Accessibility text |
|-------|------|-------------|--------------|--------------------|
| S4.1 | Opening | Serving request lifecycle: queue -> prefill -> decode -> postprocess | Tie metrics to lifecycle stages | Lifecycle written as ordered stages |
| S4.2 | KV formula | Memory formula with K/V factor highlighted | Include batch multiplier and dtype bytes | Variables listed below formula |
| S4.3 | Worked example | Small table converting bytes to GiB | Avoid one-number shortcuts | Arithmetic shown line by line |
| S4.4 | Metrics | Timing diagram labeling TTFT and TPOT | Explain why average latency is insufficient | Diagram labels repeated in caption |
| S4.5 | SLO | Table: metric, threshold, evidence source | Require P95/P99 and error rate | Table is text-only |
| S4.6 | RAG | Retriever/generator split diagram | Retrieval hit is not factual correctness | Caption states failure boundary |
| S4.7 | Benchmark boundary | Model/hardware/context/batch/workload checklist | No benchmark number without configuration | Checklist printed as text |
| S4.8 | Demo cue | Inference capstone benchmark command | Read JSON report and SLO gates | Command and JSON fields listed |
| S4.9 | Quick check | "KV estimate is exactly half expected; what did you forget?" | Expected: K and V are both stored | Prompt text-only |
| S4.10 | Evidence | Capstone report and project peer review | Students cite hardware, workload and errors | Required fields listed |

Source boundary: PagedAttention/vLLM, FlashAttention, RAG and QLoRA papers support specific methods and measured settings. They do not provide universal throughput, memory or answer-quality guarantees.

Post-lecture evidence:

- Ch10 public tests.
- Inference capstone benchmark report.
- Project report SLO and capacity section.

## Deck Accessibility Checklist

| Check | Passing evidence |
|-------|------------------|
| Text alternative | Diagrams, arrows, colors and plots have text captions or tables |
| Formula readability | Formula slides define symbols and point to full derivation notes |
| Color independence | Correct/incorrect, masked/unmasked and pass/fail states are not color-only |
| Demo fallback | Every demo slide has command, expected artifact and fallback screenshot/text summary |
| Source boundary | Every deck has at least one explicit "does not" limitation |
| Student evidence | Every deck ends with an assignment, worksheet, reading recap, quiz or capstone artifact |

## Release Checklist

| Check | Passing evidence |
|-------|------------------|
| Deck coverage | S1-S4 cover embeddings/RoPE, attention variants, training loop and serving |
| Slide sequence | Each sample deck has 8-12 representative slides with type, visual plan, speaker note and accessibility text |
| Course binding | Each deck maps to lecture id, chapter, reading week, assignment evidence and DER/P2C evidence |
| Review links | README, slide outline, notes quality review, materials index and evidence manifest link this sample pack |
| Student safety | No hidden-test details, private grading artifacts or reference implementation appear |
| Verification | `.venv/bin/python verify_course.py` reports `PASS lecture slide sample pack ...` |
