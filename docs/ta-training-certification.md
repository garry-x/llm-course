# TA Training and Certification Dossier

复核日期：2026-06-05

本 dossier 用于记录 Head TA、Discussion TA、Project Mentor、Autograder Contact 和 Course Manager 在开课前必须完成的训练、校准、模拟场景和签核。它补充 [Course Staff Runbook](staff-runbook.md)、[Grading Calibration Guide](grading-calibration.md)、[Grading Drift Audit Ledger](grading-drift-audit-ledger.md)、[Grading Anchor Sample Feedback Pack](grading-anchor-sample-feedback-pack.md)、[Private Autograder Operations Guide](private-autograder-operations.md)、[Teaching Observation and Course Evaluation Dossier](teaching-observation-course-evaluation.md)、[Accessibility and Student Support Guide](accessibility-student-support.md)、[Academic Integrity Case Process](academic-integrity-case-process.md) 和 [Course Operations and Improvement Log](course-operations-log.md)。

发布边界：本文件是 staff-facing certification record，不进入 student site release。学生可见的支持入口仍由 [Course Staff and Office Hours Directory](course-staff-office-hours-directory.md) 和 [Staff Assistance and Code Review Boundary Policy](staff-assistance-code-review-policy.md) 发布。本文件不得包含真实学生姓名、个人反馈、成绩细节、accommodation 细节、hidden tests、`reference_solution.py`、私有评分脚本或 staff 人事评价。

## Certification Scope

| role | required_before | certification_owner | evidence |
| --- | --- | --- | --- |
| Head TA | grading starts, office hours schedule published | Instructor | calibration practicum, drift trigger quiz, escalation simulation |
| Discussion TA | first discussion section | Head TA | recitation rehearsal, office-hours simulation, source-boundary scenario |
| Project Mentor | proposal feedback begins | Instructor | project scope simulation, artifact review, data/ethics routing |
| Autograder Contact | assignment release dry run | Head TA | public/hidden category mapping, release dry run, incident simulation |
| Course Manager | LMS and announcement channels open | Instructor | gradebook/LMS dry run, privacy routing, communication drill |

## Competency Modules

| module_id | competency | required artifact | passing standard |
| --- | --- | --- | --- |
| TA-CONTENT | content accuracy and source boundary | answer 6 concept/source prompts across Ch01-Ch11 | no unqualified frontier claim; formulas and source levels match audited docs |
| TA-GRADING | rubric calibration | grade 4 anchor samples and compare with expected bands | mean deviation <= 3% and no high-stakes rubric reversal |
| TA-DEBUG | office-hours debugging boundary | simulate 3 student support cases | gives minimal reproduction path without writing core solution |
| TA-AUTOGRADER | public/hidden test handling | map 5 failure categories to feedback labels | no hidden input, reference solution or private script disclosure |
| TA-PROJECT | capstone mentor boundary | review 2 synthetic project dossiers | identifies split_card, metric_card, uncertainty_record and claim_audit gaps |
| TA-PRIVACY | privacy, accessibility and integrity routing | route 5 sensitive scenarios | uses private channel, least-necessary sharing and school process |
| TA-COMMS | announcement and response memo quality | draft one grade-release note and one feedback response | public-safe, actionable and consistent with policy |

## Certification Matrix

| staff_role | TA-CONTENT | TA-GRADING | TA-DEBUG | TA-AUTOGRADER | TA-PROJECT | TA-PRIVACY | TA-COMMS |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Head TA | required | required | required | required | recommended | required | required |
| Discussion TA | required | recommended | required | optional | optional | required | recommended |
| Project Mentor | required | recommended | recommended | optional | required | required | required |
| Autograder Contact | recommended | recommended | optional | required | optional | required | required |
| Course Manager | optional | optional | optional | recommended | optional | required | required |

## Calibration Practicum

| practicum_id | task | materials | pass_condition |
| --- | --- | --- | --- |
| CAL-WRITTEN-01 | grade RoPE and attention written anchors | Grading Anchor Sample Feedback Pack; Instructor Solution Guide | score within expected band and feedback names missing assumption/shape/boundary |
| CAL-CODE-01 | classify public-pass/hidden-fail code cases | Autograder Hidden Tests; Private Autograder Operations | maps failure to category without exposing hidden input |
| CAL-CAPSTONE-01 | grade synthetic capstone excerpts | Project Report Exemplar Pack; Project Report Rubric | distinguishes runnable demo from reproducible evidence |
| CAL-RECAP-01 | score paper recap anchors | Paper Recap Calibration Pack | identifies source_record, technical_detail and boundary quality |
| CAL-DRIFT-01 | respond to high second-reader delta | Grading Drift Audit Ledger | pauses affected item and records calibration update |

## Office Hours Simulation Bank

| scenario_id | situation | expected_staff_response | forbidden_response |
| --- | --- | --- | --- |
| OH-SHAPE-01 | student shows Ch03 mask broadcast failure | ask for command, first failing assertion, tensor shapes and minimal input; guide mask-before-softmax reasoning | paste full attention implementation |
| OH-ROPE-01 | student claims RoPE guarantees infinite context | point to derivation boundary and ask for supported vs unsupported claim | state unqualified extrapolation guarantee |
| OH-TRAIN-01 | student has NaN during Ch07 training | request seed, loss log, dtype, grad norm and first bad step | tune hyperparameters until final answer works |
| OH-RUBRIC-01 | student asks why hidden test failed | explain category-level feedback and regrade path | reveal hidden input or exact expected output |
| OH-PROJECT-01 | team asks mentor to fix RAG pipeline | review artifact evidence, failure taxonomy and downgrade options | write project code or final report conclusion |

## Privacy, Accessibility, and Integrity Scenario Bank

| scenario_id | issue | routing | evidence_to_record |
| --- | --- | --- | --- |
| PAI-ACCESS-01 | approved accommodation changes timed quiz format | private channel; Instructor; school policy | accommodation path and equivalent assessment, no public reason |
| PAI-HEALTH-01 | student requests deadline change for emergency | private channel; Course Manager + Instructor | deadline decision ID, late-day impact, private note location |
| PAI-INTEGRITY-01 | similarity report flags two submissions | Academic Integrity Case Process | evidence packet and case status, no public accusation |
| PAI-TEAM-01 | project teammate dispute affects contribution | Project Team and Mentor Policy | contribution statement update and mentor escalation |
| PAI-GRADE-01 | grader made systematic rubric error | Grading Drift Audit Ledger; Course Errata Ledger if student-facing | release_batch, affected category, correction action |

## Current Certification Ledger

| certification_id | staff_role | module_id | evidence | reviewer | status |
| --- | --- | --- | --- | --- | --- |
| TA-CERT-2026-HEAD-GRADING | Head TA | TA-GRADING | CAL-WRITTEN-01; CAL-DRIFT-01 dry-run | Instructor | ready |
| TA-CERT-2026-DISCUSSION-DEBUG | Discussion TA | TA-DEBUG | OH-SHAPE-01; OH-TRAIN-01 rehearsal | Head TA | ready |
| TA-CERT-2026-MENTOR-PROJECT | Project Mentor | TA-PROJECT | CAL-CAPSTONE-01; OH-PROJECT-01 rehearsal | Instructor | ready |
| TA-CERT-2026-AUTOGRADER | Autograder Contact | TA-AUTOGRADER | CAL-CODE-01; hidden category mapping dry-run | Head TA | ready |
| TA-CERT-2026-MANAGER-PRIVACY | Course Manager | TA-PRIVACY | PAI-ACCESS-01; PAI-HEALTH-01 routing drill | Instructor | ready |
| TA-CERT-2026-COMMS | Head TA; Course Manager | TA-COMMS | grade-release note and response memo dry-run | Instructor | ready |

## Recertification and Escalation

| trigger | required_recertification | escalation |
| --- | --- | --- |
| new assignment or rubric changed | TA-GRADING and TA-AUTOGRADER affected modules | Head TA confirms before release |
| hidden-test bug or category mismatch | CAL-CODE-01 plus incident debrief | Instructor signs correction path |
| grading drift threshold exceeded | CAL-DRIFT-01 and anchor re-review | pause grading until resolved |
| new project modality or external collaborator pattern | TA-PROJECT and TA-PRIVACY | Project Mentor + Instructor review |
| accessibility or integrity routing mistake | TA-PRIVACY scenario replay | Instructor and school support process |
| staff gives over-boundary code help | TA-DEBUG and Staff Assistance policy review | fairness_followup and possible public clarification |

## Release Checklist

| check | passing evidence |
| --- | --- |
| role coverage | Head TA、Discussion TA、Project Mentor、Autograder Contact and Course Manager all included |
| competency coverage | TA-CONTENT、TA-GRADING、TA-DEBUG、TA-AUTOGRADER、TA-PROJECT、TA-PRIVACY and TA-COMMS all defined |
| practicum coverage | written, code, capstone, recap and drift calibration practicums exist |
| simulation coverage | office-hours scenarios cover shape, RoPE, training, rubric and project mentor boundaries |
| privacy scenario coverage | accessibility, health/emergency, integrity, team conflict and systematic grading error scenarios exist |
| ledger coverage | at least 6 current certification records with reviewer and ready status |
| recertification coverage | rubric, hidden-test, grading drift, project modality, privacy and over-boundary help triggers exist |
| student-release safety | file is staff-facing and excluded from student site release |
