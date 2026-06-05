# Frontier Source Evidence Cards

复核日期：2026-06-05

This file records dated evidence cards for volatile frontier-model claims that appear in the course. It complements [前沿模型来源等级与复核记录](frontier-source-audit.md), [External Source Inventory](external-source-inventory.md), [External Source Verification Guide](external-source-verification.md), [Chapter Claim Audit Ledger](chapter-claim-audit-ledger.md), [Claim Audit Worksheet](claim-audit-worksheet.md), [Model and Benchmark Card Guide](model-benchmark-card-guide.md), and [Course Operations and Improvement Log](course-operations-log.md).

Scope: DeepSeek/V3.2/V4 claims used as lecture examples, source-boundary exercises, reading discussion prompts, or capstone evidence checks. These cards do not make model-card claims into stable theory. They only state what a dated source currently supports and what the course may safely do with it.

## Evidence Card Schema

| field | requirement |
|-------|-------------|
| card_id | Stable ID beginning with `FSEC-` |
| claim | Minimal course claim being checked |
| source_url | Primary or official source URL |
| source_kind | technical report / API news / model card / official repository / unsupported |
| access_date | Date the source was checked |
| evidence_summary | Short paraphrase of what the source supports |
| boundary | Stronger conclusion not supported by the source |
| course_action | keep / qualify / downgrade / remove / monitor-only |
| student_use | lecture / reading / assignment / quiz / capstone / not for scoring |

## Current Evidence Cards

| card_id | claim | source_url | source_kind | access_date | evidence_summary | boundary | course_action | student_use |
|---------|-------|------------|-------------|-------------|------------------|----------|---------------|-------------|
| FSEC-DSA-2026-0605 | DeepSeek-V3.2-Exp introduces DeepSeek Sparse Attention for long-context efficiency | `https://api-docs.deepseek.com/news/news250929` | API news | 2026-06-05 | Official API news describes V3.2-Exp as an experimental model built on V3.1-Terminus and introducing DSA for long-context training and inference efficiency | Does not prove a general sparse-attention theorem or a course-wide benchmark number | qualify | lecture / reading |
| FSEC-V4-ARCH-2026-0605 | DeepSeek-V4-Pro and Flash are model-card-reported MoE models with 1M context and stated activated/total parameter counts | `https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro` | model card | 2026-06-05 | Model card reports V4-Pro, V4-Flash, total/activated parameter counts, 1M context, precision notes, CSA+HCA, mHC, Muon, post-training and reasoning modes | Model-card claims do not prove independent benchmark superiority or production suitability | qualify | lecture / reading / capstone source audit |
| FSEC-V4-EFF-2026-0605 | V4 model card reports 27% single-token inference FLOPs and 10% KV cache relative to V3.2 in the 1M-token setting | `https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro` | model card | 2026-06-05 | Model card states the relative FLOPs and KV-cache figures for its specified comparison setting | Not a universal serving cost or latency claim; assignments must not require the numeric result as a stable fact | qualify | lecture / reading only |
| FSEC-V4-REASON-2026-0605 | V4 model card reports three reasoning effort modes and on-policy distillation | `https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro` | model card | 2026-06-05 | Model card describes non-think, think, and think-max style modes and a post-training pipeline with on-policy distillation | Does not support the claim that a separate R1-style model family is no longer needed | qualify | lecture / reading |
| FSEC-V4-MTP-MONITOR-2026-0605 | V4 has a deeper MTP or speculative-decoding integration | no supporting primary source in checked V4 model card | unsupported | 2026-06-05 | The checked V4 model card did not provide support for MTP/speculative-decoding integration | Cannot be taught as a current V4 fact; upgrade only after a dated model card or technical report supports it | monitor-only | not for scoring |
| FSEC-ENGRAM-MONITOR-2026-0605 | Engram external memory and specific NIAH improvements are V4 facts | no supporting primary source in checked V4 model card | unsupported | 2026-06-05 | The checked V4 model card did not provide support for Engram or the removed NIAH numeric claim | Keep only as a source-boundary example; no benchmark number may appear in assignments, quizzes, or rubrics | monitor-only | not for scoring |
| FSEC-R1-UNIFY-MONITOR-2026-0605 | V4 makes a separate R1 line unnecessary | no supporting primary source in checked V4 model card | unsupported | 2026-06-05 | The model card supports reasoning modes and distillation, but not the broader product-line conclusion | Must be framed as unsupported course inference and not as a fact | downgrade | not for scoring |
| FSEC-V2V3-REPORTS-2026-0605 | DeepSeek-V2/V3 reports support MLA, DeepSeekMoE, auxiliary-loss-free balancing, MTP and V3 parameter figures as report-scoped claims | `https://arxiv.org/abs/2405.04434`; `https://arxiv.org/abs/2412.19437` | technical report | 2026-06-05 | Technical report pages identify DeepSeek-V2 and DeepSeek-V3 reports used by the course source map | Reported architecture and numeric claims remain report-scoped and must not be generalized to all LLMs | qualify | lecture / assignment where source boundary is stated |

## Upgrade and Downgrade Rules

| condition | action |
|-----------|--------|
| A primary source supports a previously monitor-only claim with version, date and configuration | Add a new `FSEC-` row, update `frontier-source-audit.md`, and decide whether the claim remains reading-only |
| A model card supports a model feature but not a benchmark or product conclusion | Keep the feature as model-card-reported and downgrade the stronger conclusion |
| A claim depends on screenshots, social posts, news summaries or unverifiable secondary sources | Mark it `D` or `unsupported`, use only as source-boundary training, and exclude it from scoring facts |
| A numeric benchmark enters lecture, assignment, quiz, or capstone rubric | Require task, shot/configuration, access date, model version, comparison set, and unsupported-conclusion boundary |
| An official source changes or disappears | Open [Course Errata and Correction Ledger](course-errata-correction-ledger.md), update source inventory, and rerun `.venv/bin/python verify_course.py` |

## Release Checklist

- Every `A-volatile` frontier claim used in README, lecture, reading or capstone guidance has a dated evidence card or a linked source-audit row.
- `monitor-only` and `unsupported` cards are explicitly excluded from assignment, quiz, exam, hidden-test and rubric facts.
- Dated source cards use primary or official URLs where available.
- Evidence summaries are paraphrased and do not copy long source passages.
- Changes are synchronized with `frontier-source-audit.md`, `external-source-inventory.md`, `chapter-claim-audit-ledger.md`, and `course-operations-log.md`.
