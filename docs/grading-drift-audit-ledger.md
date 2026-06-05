# Grading Drift Audit Ledger

复核日期：2026-06-05

本台账用于 Head TA、教师和阅卷助教在正式批改前、中、后记录评分漂移、双评抽样、rubric 分歧、anchor sample 更新和批量复核动作。它补充 [Grading Calibration Guide](grading-calibration.md)、[Grading Anchor Sample Feedback Pack](grading-anchor-sample-feedback-pack.md)、[TA Training and Certification Dossier](ta-training-certification.md)、[Gradebook and LMS Operations Guide](gradebook-lms-operations.md)、[Course Operations and Improvement Log](course-operations-log.md)、[Course Staff Runbook](staff-runbook.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md)、[Project Submission Dossier](project-submission-dossier.md) 和 [Course Errata and Correction Ledger](course-errata-correction-ledger.md)。

本文件是 staff-facing calibration record，不进入学生站点发布包。学生可见反馈仍通过 gradebook/LMS、assignment feedback 和 regrade decision 记录发布。

## Drift Signals

| signal_id | signal | threshold | action |
|-----------|--------|-----------|--------|
| GD-DELTA-03 | second_reader_delta on same submission | > 3% and <= 8% | Head TA resolves boundary item and records calibration note |
| GD-DELTA-08 | second_reader_delta on same submission | > 8% | pause grading for affected rubric item; instructor adjudicates |
| GD-RUBRIC-AMB | repeated rubric ambiguity | >= 3 cases in one release_batch | update grading calibration and student-visible clarification if needed |
| GD-HIDDEN-BUG | hidden-test bug or category mismatch | any confirmed case | freeze release_batch, patch test/rubric, batch regrade affected students |
| GD-DIST-SHIFT | grader score distribution deviates from peer median | > 10 percentage points after comparable sample mix | audit sample mix, recalibrate anchors, double-grade boundary submissions |
| GD-CAPSTONE-CLAIM | capstone claim/evidence mismatch | any headline result unsupported by logs | require second reader and claim downgrade or report correction |
| GD-REGRADES | regrade requests indicate systematic issue | >= 10% of submissions or >= 5 related requests | open batch review and publish release note category |

## Calibration Session Schema

| field | required_content |
|-------|------------------|
| session_id | stable ID, for example `CAL-2026-A3-PRE` |
| assignment_id | assignment, quiz, written set, capstone milestone or final report |
| release_batch | grade release batch or grading window |
| rubric_version | rubric or handout version used for grading |
| graders | participating graders or role IDs |
| anchor_samples | anchor IDs or synthetic samples reviewed |
| sample_size | number of submissions or samples double-graded |
| disagreement_summary | main rubric items with disagreement |
| rule_added_or_clarified | concrete rule added to grading guide, anchor pack or rubric |
| follow_up_owner | Head TA, instructor, grader, autograder contact or course manager |
| status | planned / in_progress / resolved / escalated |

## Current Calibration Sessions

| session_id | assignment_id | release_batch | rubric_version | graders | anchor_samples | sample_size | disagreement_summary | rule_added_or_clarified | follow_up_owner | status |
|------------|---------------|---------------|----------------|---------|----------------|-------------|----------------------|--------------------------|-----------------|--------|
| CAL-2026-CH02-PRE | ch02_embeddings | dry-run-2026-06-05 | handout-v1 | Instructor; Head TA | WR-ROPE-FULL-01; WR-ROPE-PARTIAL-01 | 3 | RoPE external length claims and analogy wording strength | Cap “unconditional extrapolation” claims at partial credit; require boundary sentence for full credit | Head TA | resolved |
| CAL-2026-CH03-PRE | ch03_attention | dry-run-2026-06-05 | handout-v1 | Instructor; Head TA | WR-ATTN-NOTPASS-01; CODE-ATTN-PARTIAL-01 | 4 | mask-before-softmax explanation vs implementation boundary | If mask direction is wrong, do not award high conceptual score even if terms appear | Instructor | resolved |
| CAL-2026-CAPSTONE-PRE | capstone_final_report | dry-run-2026-06-05 | project-rubric-v1 | Instructor; Project Mentor | CAP-INF-FULL-01; CAP-TRAIN-PARTIAL-01; CAP-NOTPASS-01 | 5 | runnable demo over-weighted relative to reproducibility evidence | A-band requires log-backed metrics, artifact_manifest, claim_audit and failure cases | Project Mentor | resolved |

## Double-Grading Sampling Plan

| submission_type | required_sample | priority_cases | resolver |
|-----------------|-----------------|----------------|----------|
| written derivations | at least 10% or 5 submissions, whichever is larger | grade boundaries, unusual notation, unsupported strong claims | Head TA |
| programming assignments | at least 5% plus all integrity_hold cases | public-pass/hidden-fail, manual override, import or hardcoding suspicion | Head TA + Autograder Contact |
| project proposal/milestone | all custom projects and 20% of default projects | data risk, external collaborator, compute request, unclear baseline | Project Mentor |
| final report/capstone | all reports within 5 points of grade boundary and all A-band candidates | log/report mismatch, source boundary, public archive candidate | Instructor |
| regrade requests | 100% by a grader other than original grader | rubric ambiguity, hidden category dispute, batch error claim | Head TA |

## Drift Audit Metrics

| metric | formula_or_source | target | action_if_exceeded |
|--------|-------------------|--------|--------------------|
| mean_second_reader_delta | mean(abs(original_score - second_reader_score) / max_score) | <= 3% | recalibrate disputed rubric items |
| high_delta_rate | count(delta > 8%) / double_graded_count | <= 5% | pause affected item and instructor adjudication |
| regrade_change_rate | count(revised_score != original_score) / regrade_count | <= 25% | inspect rubric clarity and grader consistency |
| upward_regrade_bias | count(upward) / changed_regrades | monitor only | check whether original grading was too strict |
| hidden_category_mismatch_count | confirmed hidden category feedback mismatch | 0 | freeze release_batch and batch regrade |
| capstone_log_mismatch_rate | log/report mismatch cases / capstone reports reviewed | <= 10% | require submission dossier correction and second reader |
| anchor_coverage | anchors_used / planned_anchor_count | 100% before grading | block grading start until anchors reviewed |

## Pause and Recalibration Triggers

| trigger | pause_scope | required_resolution |
|---------|-------------|---------------------|
| GD-DELTA-08 appears twice on same rubric item | affected rubric item | instructor decision, updated calibration note, second pass on affected samples |
| hidden-test category feedback is wrong | affected assignment release_batch | patch feedback category, identify affected students, publish release note category |
| rubric interpretation changes after grading begins | affected submissions not yet released | document rule, review already graded boundary cases, announce if student-facing |
| grade distribution outlier by grader | grader batch | sample-mix audit and Head TA second read |
| capstone A-band reports lack reproducible logs | capstone A-band candidates | require dossier evidence before finalizing A-band |

## Regrade and Batch Correction Linkage

| linkage_field | usage |
|---------------|-------|
| regrade_decision_id | connects LMS request to grader decision and possible batch correction |
| release_batch | identifies whether a grading issue affects a published batch |
| rubric_version | confirms whether students were graded against the published rubric |
| affected_students | private list kept in gradebook/LMS records, not in public docs |
| calibration_update_needed | triggers update to grading calibration guide, anchor pack or instructor solution guide |
| errata_id | used when grading issue also requires public correction or announcement |

## Staff Review Workflow

1. Before grading: review planned anchor samples, rubric_version, hidden category feedback labels and sampling plan.
2. During grading: double-grade required sample, watch drift signals and pause if thresholds trigger.
3. Before release: compute drift audit metrics, resolve high-delta cases, confirm student_visible_feedback is public-safe.
4. After release: analyze regrade requests, batch-correct systematic errors and update calibration materials.
5. End of term: summarize drift metrics in operations log without student identifiers.

## Release Checklist

| 检查项 | 通过标准 |
|--------|----------|
| drift signals | GD-DELTA-03、GD-DELTA-08、GD-RUBRIC-AMB、GD-HIDDEN-BUG、GD-DIST-SHIFT、GD-CAPSTONE-CLAIM 和 GD-REGRADES 均定义 |
| session schema | session_id、assignment_id、release_batch、rubric_version、graders、anchor_samples、sample_size、disagreement_summary、rule、owner 和 status 均可记录 |
| current sessions | Ch02、Ch03 和 capstone dry-run calibration sessions 已记录 |
| sampling plan | written、programming、proposal/milestone、final report 和 regrade request 都有 double-grading sampling rule |
| metrics | second-reader delta、high-delta rate、regrade change、hidden mismatch、capstone mismatch 和 anchor coverage 均有 threshold/action |
| pause triggers | rubric drift、hidden category bug、grader outlier 和 capstone evidence mismatch 都能暂停并复核 |
| linked records | grading calibration、anchor pack、gradebook/LMS、operations log、staff runbook、project dossier 和 errata ledger 均链接本文件 |
| student safety | 本文件标记 staff-facing，不进入 student site release |
