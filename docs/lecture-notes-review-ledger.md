# Lecture Notes Review Ledger

本台账记录 L1-L20 当前 lecture notes / chapter-as-notes / handout 的复核状态。它把 [Lecture Notes Quality and Review Standard](lecture-notes-quality-review.md) 中的 `review_record` 模板落实为逐讲证据，并与 [Lecture Notes Index](lecture-notes-index.md)、[Lecture Slide Outline](lecture-slide-outline.md)、[Board Derivation and Instructor Notes Pack](board-derivation-pack.md)、[Classroom Demo Runbook](demo-runbook.md)、[Course Materials Index](course-materials-index.md) 和 [Chapter Claim Audit Ledger](chapter-claim-audit-ledger.md) 一起维护。

复核日期：2026-06-05
复核范围：L1-L20 的学生可见 notes、章节正文、专题 handout、项目 README、板书推导和可运行证据。
发布口径：`ready` 表示可作为本轮学生课前/课后材料；若后续正式 slides、录屏或 notebook 发布，应在本台账追加对应 material_id 和 review record。

## Review Ledger

| lecture_id | material_id | reviewer | review_date | status | notation_checked | derivation_checked | code_binding_checked | source_boundary_checked | accessibility_checked | affected_materials | change_summary | verification_command |
|------------|-------------|----------|-------------|--------|------------------|--------------------|----------------------|-------------------------|----------------------|--------------------|----------------|----------------------|
| L1 | Ch01; math-prerequisites.md | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | Ch01, Ch01 BPE tests, reading recap | BPE merge、byte-level tokenizer、成本边界复核 | `.venv/bin/python verify_course.py` |
| L2 | Ch02 | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | Ch02, Ch02 embeddings tests, written proof | one-hot lookup、word vector 类比边界、RoPE 相对位置复核 | `.venv/bin/python verify_course.py` |
| L3 | Ch03 | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | Ch03 attention tests, board derivation pack | attention scaling 方差假设和 score shape 复核 | `.venv/bin/python verify_course.py` |
| L4 | Ch03; classic-nlp-handout.md | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | Ch03 causal mask tests, classic NLP drill | causal mask、softmax+CE、transition parsing preview 复核 | `.venv/bin/python verify_course.py` |
| L5 | Ch04 | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | Ch04 MHA/GQA tests, written problem | MHA/GQA 参数量、KV head 和 cache 边界复核 | `.venv/bin/python verify_course.py` |
| L6 | Ch04-Ch05 | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | Ch04 MLA tests, Ch05 block tests | MLA latent cache、RoPE 边界、LayerNorm/RMSNorm 复核 | `.venv/bin/python verify_course.py` |
| L7 | Ch06 | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | Ch06 GPT tests, assignment handout | next-token labels、weight tying、参数审计复核 | `.venv/bin/python verify_course.py` |
| L8 | Ch06 | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | Ch06 MoE router tests, written audit | top-k routing、activated parameters、load balancing 复核 | `.venv/bin/python verify_course.py` |
| L9 | Ch07 | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | Ch07 loss/optimizer tests, board derivation pack | CE、AdamW、warmup+cosine、ignore_index 复核 | `.venv/bin/python verify_course.py` |
| L10 | Ch07; training capstone README | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | training capstone, compute guide | checkpoint/resume、tokens/s、GPU hours 和曲线诊断复核 | `.venv/bin/python verify_course.py --capstone --training` |
| L11 | Ch08 | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | Ch08 generation tests, written problem | greedy/top-k/top-p、候选集和重复退化边界复核 | `.venv/bin/python verify_course.py` |
| L12 | Ch08 | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | Ch08 speculative decoding tests, frontier audit | speculative decoding、structured output、MTP 来源边界复核 | `.venv/bin/python verify_course.py` |
| L13 | Ch09 | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | Ch09 LoRA/SFT tests, assignment handout | SFT label mask、LoRA rank/scaling、参数冻结复核 | `.venv/bin/python verify_course.py` |
| L14 | Ch09 | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | Ch09 DPO/GRPO tests, written proof | DPO log-ratio、GRPO whitening、alignment 边界复核 | `.venv/bin/python verify_course.py` |
| L15 | classic-nlp-handout.md; nlp-evaluation-coverage.md | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | Ch11 tests, classic NLP handout | dependency parsing、beam search、BERT/MLM、metric failure cases 复核 | `.venv/bin/python verify_course.py` |
| L16 | data-ethics-review.md | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | data ethics form, project report rubric | license、PII、contamination、safety risk matrix 复核 | `.venv/bin/python verify_course.py` |
| L17 | Ch10 | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | Ch10 KV/RAG tests, chapter claim ledger | KV cache、INT8、RAG chunk overlap 和检索边界复核 | `.venv/bin/python verify_course.py` |
| L18 | Ch10; inference capstone README | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | inference capstone benchmark/SLO, capacity plan | TTFT/TPOT/TPS、P95/P99、capacity plan 复核 | `.venv/bin/python verify_course.py --capstone --training` |
| L19 | capstone READMEs; project-report-rubric.md | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | project template, experimental rigor guide | seed/log/checkpoint/report 复现链和 claim_audit 复核 | `.venv/bin/python verify_course.py --capstone --training` |
| L20 | presentation-peer-review.md; course-operations-log.md | instructor | 2026-06-05 | ready | Yes | Yes | Yes | Yes | Yes | presentation rubric, operations log | final claim/evidence/risk alignment 和课程改进闭环复核 | `.venv/bin/python verify_course.py --capstone --training` |

## Review Exceptions and Follow-Up

| exception_id | lecture_id | issue | action | owner | due |
|--------------|------------|-------|--------|-------|-----|
| none-current | L1-L20 | 当前无阻塞性 review exception | 下一轮发布正式 PDF slides、录屏或 notebook 后追加 material-specific review record | instructor | next release |

## Evidence Requirements

| check_id | 当前证据 |
|----------|----------|
| notation_checked | Lecture Notes Index、Board Derivation Pack、章节公式和 assignment tests 符号一致 |
| derivation_checked | board derivation pack、written problem set、instructor solution guide 覆盖核心推导 |
| code_binding_checked | 每讲连接 assignment tests、demo command、capstone acceptance 或 project rubric |
| source_boundary_checked | Chapter Source and Accuracy Map、Chapter Claim Audit Ledger、External Source Inventory、Frontier Source Audit |
| accessibility_checked | HTML chapter alt text / captions、lecture media access policy、accessibility support guide |

## 发布前 Checklist

- L1-L20 均有 `ready` 或明确 exception；不能有 planned/draft 却作为评分材料。
- 每讲 `notation_checked`、`derivation_checked`、`code_binding_checked`、`source_boundary_checked` 和 `accessibility_checked` 均为 `Yes`，否则必须在 exception 表中解释。
- verification command 必须使用 `.venv/bin/python`。
- 涉及 capstone、training、inference、release package 或项目验收的讲次必须使用 `.venv/bin/python verify_course.py --capstone --training`。
- 本台账更新后运行 `.venv/bin/python verify_course.py`。
