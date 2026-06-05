# Assessment Item Analysis and Psychometrics Guide

复核日期：2026-06-05

本指南定义 quiz、recap check、midterm checkpoint、final review quiz 和 capstone readiness check 的题目质量复核流程。它补充 [Assessment Blueprint and Coverage Matrix](assessment-blueprint-coverage-matrix.md)、[Assessment Item Bank Ledger](assessment-item-bank-ledger.md)、[Assessment Administration and Exam Integrity Policy](assessment-administration-policy.md)、[Learning Analytics and Remediation Plan](learning-analytics-remediation-plan.md)、[Concept Mastery and Misconception Map](concept-misconception-map.md)、[Gradebook and LMS Operations Guide](gradebook-lms-operations.md)、[Grading Drift Audit Ledger](grading-drift-audit-ledger.md) 和 [Course Operations and Improvement Log](course-operations-log.md)。

公开边界：本文件可以公开方法、字段、阈值和聚合决策规则；不得公开 active assessment 完整题面、单个学生答案、受保护群体小样本统计、hidden rubric、reference solution 或私有评分脚本。

## Item Analysis Scope

| scope_id | covered assessment | item_bank_link | output |
| --- | --- | --- | --- |
| IA-QUICK | lecture quick check | `QC-W2-MASK-01` and active variants | misconception rate, rapid recap decision |
| IA-RECAP | weekly recap quiz | `QC-W1-BPE-01`, `QC-W3-CACHE-01`, `QC-W6-SAMPLING-01`, `QC-W7-DPO-01` | difficulty, distractor note, remediation trigger |
| IA-MIDTERM | midterm checkpoint | `QC-W5-TRAIN-01` and active variants | item discrimination, rubric revision, makeup equivalence check |
| IA-FINAL | final review quiz | `QC-W8-EVAL-01`, `QC-W10-SOURCE-01` | metric/source boundary error profile |
| IA-CAPSTONE | capstone readiness check | `QC-W9-SLO-01` and project evidence gates | readiness risk, project clinic decision |
| IA-MAKEUP | approved makeup assessment | `QC-MAKEUP-EQUIV-01` | equivalence audit, accommodation-safe record |

## Metric Definitions

| metric_id | definition | minimum_n | interpretation |
| --- | --- | --- | --- |
| item_difficulty_p | mean item score / max item score | 10 | Target diagnostic range is 0.45-0.85 unless the item is a prerequisite gate |
| item_discrimination_d | upper-quartile correctness minus lower-quartile correctness | 20 | Values below 0.15 require review for ambiguity, miskey, over-easy item or misaligned prerequisite |
| distractor_efficiency | count of non-correct options selected by at least 5% of students | 20 | Zero active distractors on a multiple-choice item suggests memorization or weak distractor design |
| short_answer_rubric_fit | fraction of scored answers whose feedback maps to a published rubric category | 10 | Below 0.90 means rubric categories or examples need clarification |
| completion_time_median | median minutes from LMS/open-book log or in-class observation | 10 | If median exceeds planned time by 25%, shorten or split the item |
| subgroup_review_flag | difference in aggregate performance for an approved demographic/accommodation audit group | school policy | Only reviewed by authorized staff; small-n groups are suppressed |
| retake_equivalence_delta | absolute score difference between original and makeup variant after comparable preparation | 10 paired or instructor audit | Large differences require equivalence review, not automatic student penalty |

## Decision Thresholds

| decision_id | condition | required action | linked record |
| --- | --- | --- | --- |
| IA-DIFF-HARD | `item_difficulty_p < 0.40` and item is not a known stretch gate | inspect wording, prerequisite coverage and rubric; trigger remediation if concept-aligned | LA-QUIZ; TR-SHAPE-30 or TR-MASK-20 |
| IA-DIFF-EASY | `item_difficulty_p > 0.95` and `item_discrimination_d < 0.10` | retire, revise or move to public_sample practice | Assessment Item Bank Ledger rotation record |
| IA-DISC-LOW | `item_discrimination_d < 0.15` | check ambiguity, miskey, hidden prerequisite and distractor quality | Course Operations Log; errata if grading-impacting |
| IA-DISTRACTOR-DEAD | fewer than 2 active distractors on a 4-option item | rewrite distractors from observed misconceptions | Concept Mastery and Misconception Map |
| IA-RUBRIC-DRIFT | `short_answer_rubric_fit < 0.90` | open grading calibration session before release | Grading Drift Audit Ledger |
| IA-TIME-OVER | median time exceeds plan by 25% | split item, extend window or reduce count in future offering | Assessment Administration Policy |
| IA-FAIRNESS-FLAG | subgroup review finds unexplained aggregate gap after small-n suppression | instructor and authorized accessibility/school staff review wording, modality and prerequisites | Accessibility and Student Support Guide |
| IA-EQUIV-FAIL | makeup variant is not equivalent in objective, cognitive level or difficulty | replace variant and document private accommodation-safe resolution | QC-MAKEUP-EQUIV-01 |

## Analysis Record Schema

| field | required_content |
| --- | --- |
| analysis_id | stable ID, for example `IA-2026-W3-CACHE` |
| assessment_id | LMS/Gradescope or in-class assessment identifier |
| item_bank_id | stable item or active variant ID |
| outcome_id | `CO1` through `CO6` |
| cognitive_level | remember, understand, apply, analyze, evaluate or create |
| sample_size | number of scorable submissions after exclusions |
| item_difficulty_p | normalized item mean |
| item_discrimination_d | upper/lower quartile difference or `not_applicable` |
| distractor_efficiency | active distractor count or written-error category spread |
| short_answer_rubric_fit | rubric coverage fraction or `not_applicable` |
| completion_time_median | median minutes or `not_collected` |
| subgroup_review_flag | none, suppressed_small_n, reviewed_no_action, reviewed_action |
| decision_id | one of IA-DIFF-HARD, IA-DIFF-EASY, IA-DISC-LOW, IA-DISTRACTOR-DEAD, IA-RUBRIC-DRIFT, IA-TIME-OVER, IA-FAIRNESS-FLAG, IA-EQUIV-FAIL or none |
| action_taken | keep, revise, retire, recalibrate, remediate, announce_correction or accommodation_review |
| public_summary | aggregate-only student-visible note, if any |
| private_record_location | LMS, gradebook, operations log or school-approved private store |

## Current Dry-Run Analysis Records

| analysis_id | assessment_id | item_bank_id | outcome_id | cognitive_level | sample_size | item_difficulty_p | item_discrimination_d | distractor_efficiency | short_answer_rubric_fit | completion_time_median | subgroup_review_flag | decision_id | action_taken |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| IA-2026-W1-BPE | dry-run-recap-w1 | QC-W1-BPE-01 | CO1 | understand | 24 | 0.72 | 0.31 | written-error categories: pair count, merge order, decode boundary | 0.96 | 6.5 | none | none | keep |
| IA-2026-W2-MASK | dry-run-quick-w2 | QC-W2-MASK-01 | CO1 | analyze | 22 | 0.58 | 0.27 | 3 active distractors | 0.91 | 4.0 | none | none | keep |
| IA-2026-W5-TRAIN | dry-run-midterm-w5 | QC-W5-TRAIN-01 | CO2 | analyze | 21 | 0.46 | 0.18 | written-error categories: label shift, scheduler boundary, AdamW decay | 0.88 | 13.5 | none | IA-RUBRIC-DRIFT | recalibrate |
| IA-2026-W8-EVAL | dry-run-final-w8 | QC-W8-EVAL-01 | CO6 | evaluate | 20 | 0.63 | 0.24 | 2 active distractors | 0.94 | 8.0 | none | none | keep |
| IA-2026-W10-SOURCE | dry-run-final-w10 | QC-W10-SOURCE-01 | CO5 | evaluate | 20 | 0.52 | 0.29 | written-error categories: missing access date, overclaim, no config | 0.92 | 7.5 | none | none | keep |
| IA-2026-CAP-SLO | dry-run-capstone-readiness | QC-W9-SLO-01 | CO4 | evaluate | 12 | 0.50 | not_applicable | written-error categories: p95, throughput, hardware context | 0.91 | 11.0 | suppressed_small_n | none | keep |

## Post-Assessment Workflow

| step | owner | timing | action |
| --- | --- | --- | --- |
| 1. collect aggregate | Course Manager | within 24 hours | export aggregate item scores, timing and rubric categories without student identifiers |
| 2. compute metrics | Head TA | within 48 hours | compute item_difficulty_p, item_discrimination_d, distractor_efficiency and rubric fit |
| 3. classify decisions | Instructor + Head TA | before grade release if item is graded | apply Decision Thresholds and decide keep/revise/retire/recalibrate/remediate |
| 4. update records | Course Manager | before next assessment | update item bank exposure/retirement, learning analytics trigger, operations log and gradebook note |
| 5. publish safe summary | Instructor | after release | publish only aggregate common issues and remediation steps, not active item internals |
| 6. archive private evidence | Instructor | end of week | retain raw exports and subgroup review only in school-approved private systems |

## Fairness and Privacy Rules

- Aggregate public summaries must suppress small-n subgroup information and never identify individual students.
- Fairness review is used to inspect wording, modality, prerequisites and accommodation fit; it is not a public ranking of groups.
- If a subgroup or accommodation review changes scoring, the gradebook/LMS record must show the authorized decision path.
- Active item statistics may reveal answer patterns; publish only category-level common issues after the assessment is retired or made safe.
- Hidden-test or reference-solution evidence cannot be used as a public item-analysis example.
- Makeup analysis must preserve objective and cognitive_level equivalence before comparing scores.

## Release Checklist

| check | passing evidence |
| --- | --- |
| scope coverage | IA-QUICK、IA-RECAP、IA-MIDTERM、IA-FINAL、IA-CAPSTONE 和 IA-MAKEUP all present |
| metric coverage | item_difficulty_p、item_discrimination_d、distractor_efficiency、short_answer_rubric_fit、completion_time_median、subgroup_review_flag and retake_equivalence_delta all defined |
| threshold coverage | IA-DIFF-HARD、IA-DIFF-EASY、IA-DISC-LOW、IA-DISTRACTOR-DEAD、IA-RUBRIC-DRIFT、IA-TIME-OVER、IA-FAIRNESS-FLAG and IA-EQUIV-FAIL all defined |
| record schema | analysis_id、assessment_id、item_bank_id、outcome_id、cognitive_level、sample_size、decision_id、action_taken and private_record_location are required |
| dry-run evidence | at least 6 current dry-run analysis records cover CO1, CO2, CO4, CO5 and CO6 |
| workflow coverage | collect, compute, classify, update, publish and archive steps have owner and timing |
| privacy boundary | small-n suppression, active-item secrecy, hidden-test secrecy and accommodation-safe records are explicit |
| link coverage | item bank, learning analytics, assessment blueprint, gradebook/LMS, grading drift and operations log link this guide |
