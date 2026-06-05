# Learning Outcome Attainment Report

复核日期：2026-06-05

本报告用于把 `CO1`-`CO6` 的直接证据、间接证据、达标阈值、当前 dry-run 状态、缺口和改进动作汇总成课程级 outcome attainment 记录。它补充 [Course Outcome Map](course-outcome-map.md)、[Assessment Blueprint and Coverage Matrix](assessment-blueprint-coverage-matrix.md)、[Programming Assignment Code Quality Rubric](programming-assignment-code-quality-rubric.md)、[Assessment Item Analysis and Psychometrics Guide](assessment-item-analysis-psychometrics.md)、[Gradebook and LMS Operations Guide](gradebook-lms-operations.md)、[Learning Analytics and Remediation Plan](learning-analytics-remediation-plan.md)、[Teaching Observation and Course Evaluation Dossier](teaching-observation-course-evaluation.md)、[Project Submission Dossier](project-submission-dossier.md)、[Course Operations and Improvement Log](course-operations-log.md) 和 [Pre-Semester Readiness Audit](presemester-readiness-audit.md)。

解释边界：当前报告是 pre-semester / dry-run attainment dossier，用于证明课程设计和验证证据已经具备 outcome-level 追踪能力；真实学生 attainment 必须在开课后由 gradebook、rubric、project dossier、quiz/item analysis、student feedback 和 course evaluation 数据更新。不得把 `COURSE VERIFY: PASS` 解释为真实学生学习结果已经达成。

## Attainment Evidence Taxonomy

| evidence_type | definition | examples | limitation |
| --- | --- | --- | --- |
| direct_auto | student artifact or course artifact checked by executable tests | assignment tests, capstone acceptance, formula/link/render gates | proves implementation or artifact behavior, not full reasoning |
| direct_manual | scored student work reviewed by rubric | written derivations, project report, presentation, paper recap, code review | requires calibration and double-grading audit |
| indirect_student | student perception or participation evidence | midterm feedback, exit tickets, office-hours themes, course evaluation | cannot alone prove mastery |
| indirect_staff | staff observation or operational evidence | peer observation, teaching evaluation ledger, staff runbook notes | reflects delivery quality, not individual mastery |
| readiness_proxy | pre-semester design and dry-run evidence | manifest, release safety, source audit, sample packs | must be replaced or supplemented with real offering data |

## Outcome Attainment Targets

| outcome_id | direct_auto_target | direct_manual_target | indirect_target | minimum_action_threshold |
| --- | --- | --- | --- | --- |
| CO1 | >= 80% of students pass Ch01-Ch06 public tests and no hidden shape category below 65% | >= 75% meet written shape/data-flow rubric | <= 20% report persistent shape-flow confusion after Week 4 | if below target, add shape recap and revise Ch03/Ch04 worksheets |
| CO2 | >= 80% pass programming assignments without hardcoding or API-contract violations | >= 75% pass code review boundary on modules, masks and initialization | office-hours implementation blockers decline after remediation | if below target, add PyTorch review drill and revise starter hints |
| CO3 | formula-linked tests pass and written sets cover at least 5 of 7 derivation families | >= 70% meet assumptions, units, shape and boundary rubric | derivation anxiety or notation confusion below 25% in midterm survey | if below target, add board derivation recap and anchor feedback |
| CO4 | >= 80% of teams pass capstone acceptance or approved scoped fallback | >= 75% meet reproducibility, metric, uncertainty and claim-audit rubric | project risk count decreases by final milestone | if below target, require project clinic and dossier resubmission |
| CO5 | source audit and manifest gates pass; reading recap submissions include source tier | >= 75% meet source_record, technical_detail and boundary rubric | overclaim/source-boundary feedback theme below 20% | if below target, add source downgrade mini case and citation clinic |
| CO6 | Ch11 tests and final evaluation item pass thresholds | >= 75% can justify metric choice and limitation | evaluation-metric misconception below 20% after final review | if below target, add classic NLP/evaluation recitation and item revision |

## Current Dry-Run Attainment Matrix

| outcome_id | direct_auto_evidence | direct_manual_proxy | indirect_proxy | dry_run_status | gap_to_real_attainment |
| --- | --- | --- | --- | --- | --- |
| CO1 | Ch01-Ch06 suites pass; browser/render/formula gates pass | written problem set and lecture note samples include shape/data-flow rubrics | peer observation ledger flags Ch03 mask contrast action | design_ready | needs real student written work, hidden category stats and exit tickets |
| CO2 | 11 assignment suites pass; starter/reference/tests API contracts aligned | grading calibration and assignment handout define module/code-review criteria | office-hours and learning analytics playbooks define implementation blockers | design_ready | needs real submissions, hardcoding audit and hidden boundary results |
| CO3 | mathematical derivation audit covers DER-01 through DER-14 | instructor solution guide and grading anchors define derivation feedback | midterm feedback protocol can track notation/derivation confusion | design_ready | needs real scored written derivations and double-grading sample |
| CO4 | inference and training capstone acceptance commands defined; project dossier required files checked | project rubric, exemplar pack and mentor review process define manual evidence | teaching evaluation ledger flags artifact_manifest rehearsal | design_ready | needs real team dossiers, reproducibility attempts and mentor decisions |
| CO5 | source inventory, frontier audit and evidence manifest pass marker checks | paper recap calibration pack and source verification guide define rubric evidence | evaluation ledger includes source downgrade teaching action | design_ready | needs real reading recaps and project citation/source audits |
| CO6 | Ch11 classic NLP tests pass; evaluation coverage and final review items mapped | written problem set, classic NLP module and project metric rubric define manual evidence | item analysis dry-run includes QC-W8-EVAL-01 | design_ready | needs real final review results and project metric critique evidence |

## Direct Evidence Collection Plan

| collection_id | outcome_id | artifact | owner | timing | required_fields |
| --- | --- | --- | --- | --- | --- |
| LOA-AUTO-ASSIGN | CO1; CO2; CO3; CO6 | assignment public/hidden category summary | Autograder Contact | each assignment release | assignment_id, category, pass_rate, failure_theme, remediation |
| LOA-WRITTEN | CO1; CO3; CO5; CO6 | written derivation rubric export | Head TA | each written set | rubric_version, sample_size, score_distribution, anchor_used, drift_flag |
| LOA-QUIZ | CO1; CO3; CO5; CO6 | item analysis summary | Head TA | each quiz/checkpoint | item_bank_id, item_difficulty_p, item_discrimination_d, decision_id |
| LOA-CAPSTONE | CO2; CO4; CO5; CO6 | project submission dossier and rubric | Project Mentor | milestone and final | artifact_manifest, split_card, metric_card, uncertainty_record, claim_audit |
| LOA-READING | CO5; CO6 | paper recap rubric export | Discussion TA | weekly | source_record, technical_detail, boundary, feedback_theme |
| LOA-EVAL | all COs | end-of-term course review | Instructor | end of term | outcome_status, evidence_summary, action_for_next_offering |

## Indirect Evidence and Triangulation

| signal | paired_direct_evidence | use | cannot_be_used_for |
| --- | --- | --- | --- |
| midterm feedback themes | quiz/item analysis, written scores, office-hours categories | identify delivery or workload causes behind weak outcomes | raising grades without direct evidence |
| peer observation notes | lecture notes review, demo runbook, assessment blueprint | decide whether teaching delivery needs revision | proving individual student mastery |
| office-hours frequency | assignment failure categories and learning analytics triggers | identify blockers and update FAQ/recitation | publishing personal support details |
| end-of-term evaluation | gradebook, capstone dossier, source/errata logs | prioritize next offering improvements | replacing direct outcome assessment |
| project showcase feedback | project rubric and reproducibility records | test whether capstone evidence is communicable | substituting for reproducibility logs |

## Attainment Status Codes

| status | meaning | allowed use |
| --- | --- | --- |
| design_ready | course has mapped materials, assessments, rubrics and verifier evidence, but no real offering data yet | pre-semester readiness |
| partially_attained | some direct evidence meets target, but at least one channel or subgroup/gate is below target | midterm or end-term review |
| attained | direct_auto and direct_manual targets met, indirect signals do not contradict, and no unresolved grading/source/accessibility gate remains | end-term course report |
| over_assessed | outcome has high evidence load relative to importance or repeated low-value items | blueprint revision |
| under_supported | outcome has repeated weak evidence or student/staff signals indicate insufficient instruction | remediation and next-offering action |
| inconclusive | evidence missing, too small, not comparable or privacy-suppressed | collect stronger evidence before claiming attainment |

## Closing the Loop Actions

| action_id | trigger | required_update | verification |
| --- | --- | --- | --- |
| LOA-RECAP | CO1 or CO3 below threshold | add board recap, worksheet and quick-check variant | follow-up item improves or confusion declines |
| LOA-ASSIGN-REVISION | CO2 hidden/public gap exceeds threshold | revise handout, public boundary tests or starter hint | next release category gap narrows |
| LOA-RUBRIC-CAL | direct_manual drift or low rubric fit | update grading calibration, anchor samples and rubric wording | drift audit passes before release |
| LOA-PROJECT-CLINIC | CO4 capstone evidence below threshold | require mentor clinic and revised dossier | project dossier passes required fields |
| LOA-SOURCE-CASE | CO5 source boundary weak | add source downgrade mini case and reading recap feedback | source_record completeness improves |
| LOA-EVAL-RECITATION | CO6 metric critique weak | add classic NLP/evaluation recitation | final review metric item improves |

## Release Checklist

| check | passing evidence |
| --- | --- |
| taxonomy coverage | direct_auto、direct_manual、indirect_student、indirect_staff and readiness_proxy defined |
| target coverage | `CO1` through `CO6` each have direct_auto_target, direct_manual_target and indirect_target |
| dry-run matrix | all six outcomes have current dry_run_status and gap_to_real_attainment |
| collection plan | assignment, written, quiz, capstone, reading and end-term evidence collection IDs exist |
| status codes | design_ready, partially_attained, attained, over_assessed, under_supported and inconclusive are defined |
| loop actions | LOA-RECAP、LOA-ASSIGN-REVISION、LOA-RUBRIC-CAL、LOA-PROJECT-CLINIC、LOA-SOURCE-CASE and LOA-EVAL-RECITATION are defined |
| boundary statement | report explicitly says dry-run evidence does not prove real student attainment |
| link coverage | outcome map, assessment blueprint, learning analytics, teaching evaluation, gradebook/LMS, project dossier and operations log link this report |
