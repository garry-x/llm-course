# Teaching Observation and Course Evaluation Dossier

复核日期：2026-06-05

本 dossier 用于把课堂同行观察、期中反馈、期末课程评估、作业/项目证据和课程组复盘连接成可审计的质量改进闭环。它补充 [课程 Syllabus](syllabus.md)、[Learning Outcome Attainment Report](learning-outcome-attainment-report.md)、[Participation and Feedback Guide](participation-feedback-guide.md)、[Course Operations and Improvement Log](course-operations-log.md)、[Learning Analytics and Remediation Plan](learning-analytics-remediation-plan.md)、[Weekly Teaching Reflection and Adjustment Log](weekly-teaching-reflection-adjustment-log.md)、[Lecture Notes Quality and Review Standard](lecture-notes-quality-review.md)、[Lecture Slide Sample Pack](lecture-slide-sample-pack.md)、[External Expert Review Dossier](external-expert-review-dossier.md)、[Course Staff Runbook](staff-runbook.md)、[Course Communication and Announcement Policy](course-communication-policy.md) 和 [Accessibility and Student Support Guide](accessibility-student-support.md)。

公开边界：本文件可以公开观察维度、聚合反馈、response memo 和改进动作；不得公开学生个人反馈、身份信息、医疗/便利安排、未公开 staff 人事评价、未发布成绩分布或具体学生提交。

## Evaluation Sources

| source_id | source | timing | evidence | privacy boundary |
| --- | --- | --- | --- | --- |
| CE-PEER-OBS | peer classroom observation | Week 2-4 and Week 7-9 | observation rubric, notes on learning goals, board work, pacing and inclusivity | no student identifiers; observer notes stored staff-side |
| CE-MID-SURVEY | midterm student feedback survey | end of Week 5 | aggregate responses, top themes, response memo | no raw comments in public release |
| CE-END-SURVEY | end-of-term course evaluation | after final project | aggregate course ratings, qualitative themes, next-offering actions | follow school policy for official evaluation data |
| CE-ANALYTICS | learning analytics summary | weekly and after major assessments | trigger/action records, item analysis, remediation completion | aggregate only; no personal grade or accommodation details |
| CE-GRADING | grading and regrade evidence | before and after release windows | drift metrics, regrade themes, rubric clarifications | no student-level grade records in public docs |
| CE-CAPSTONE | project reproducibility and showcase evidence | milestone and final | reproducibility pass rate, common project risks, archive readiness | no private team conflict or sensitive data |

## Peer Observation Rubric

| dimension | strong evidence | needs attention | follow-up |
| --- | --- | --- | --- |
| learning_goal_alignment | lecture states outcome, derivation, demo and assessment connection | activity is interesting but not linked to CO/DER/project evidence | revise lecture plan and slide opening |
| technical_accuracy | formulas, notation, code contracts and source boundaries match audited materials | unqualified claim, notation drift or code mismatch appears | open errata or derivation/source audit item |
| board_and_slide_clarity | shapes, variables, assumptions and failure modes are visible and sequenced | students see final formula but not derivation path | update board script or slide sample notes |
| active_learning | quick check, worksheet or demo asks students to reason, not copy | participation is passive or only asks for definitions | add shape drill, failure drill or paper-to-code prompt |
| pacing_and_workload | time spent matches weekly workload budget and prerequisite ladder | rushed proof, unexplained jump or overload signal | adjust workload pacing and recap plan |
| inclusion_accessibility | captions, contrast, readable math, microphone/recording and alternative participation are addressed | students with accommodations or remote access face avoidable friction | update accessibility support and media policy |
| assessment_alignment | quiz/checkpoint or assignment evidence directly tests stated skill | assessment rewards recall not targeted reasoning | update assessment blueprint or item bank |

## Midterm Feedback Response Protocol

| step | owner | due | required output |
| --- | --- | --- | --- |
| 1. collect | Course Manager | Week 5 + 2 days | survey export with identifiers removed or restricted per school policy |
| 2. code themes | Head TA | Week 5 + 4 days | 5-8 aggregate themes mapped to workload, clarity, support, assessment, source boundary or project scope |
| 3. triangulate | Instructor | Week 6 staff meeting | compare themes with analytics triggers, office-hours issues, item analysis and gradebook categories |
| 4. publish response memo | Instructor | within 1 week | student-visible memo: will change, will not change, why, timeline |
| 5. update artifacts | assigned owners | before next affected module | concrete edits to lecture notes, assignment handout, FAQ, rubric, schedule or support channel |
| 6. verify impact | Head TA | two weeks later | follow-up signal: exit ticket, quiz item, office-hours volume or project milestone risk |

## End-of-Term Course Review

| review_area | evidence | decision question | next-offering artifact |
| --- | --- | --- | --- |
| outcome attainment | Course Outcome Map, grade distribution, capstone evidence | Which COs were under-supported or over-assessed? | updated assessment blueprint and lecture plan |
| content accuracy | errata ledger, source audit, derivation audit, student-reported issues | Which claims, formulas or examples need correction before reuse? | errata closure and source map patch |
| workload and pacing | workload calibration, survey themes, office-hours load | Which weeks exceeded target effort or compressed too much material? | 10/12-week pacing update |
| assessment quality | item analysis, grading drift, regrade themes | Which items or rubrics should be retired, revised or promoted? | item bank rotation and grading calibration update |
| project quality | project dossier, reproducibility results, showcase feedback | Which project milestones improved final evidence? | capstone guide and report template updates |
| support and accessibility | staff runbook, accessibility records, participation feedback | Which support channels were timely, fair and accessible? | staff runbook and communication policy updates |

## Current Evaluation Ledger

| record_id | date | source_id | finding | action | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| CE-2026-OBS-L3 | 2026-06-05 | CE-PEER-OBS | Attention lecture needs explicit mask-before-softmax failure contrast | add failure drill reference to Ch03 discussion and slide notes | Discussion TA | planned |
| CE-2026-MID-WORKLOAD | 2026-06-05 | CE-MID-SURVEY | Week 5 block/code/debug workload likely exceeds target if Ch06 and Ch07 land together | use workload-pacing 12-week expansion option or add recap buffer | Instructor | planned |
| CE-2026-ITEM-W5 | 2026-06-05 | CE-ANALYTICS | QC-W5-TRAIN-01 dry-run rubric fit below target | open IA-RUBRIC-DRIFT and grading calibration session | Head TA | in_progress |
| CE-2026-CAP-REPRO | 2026-06-05 | CE-CAPSTONE | Capstone reports need earlier artifact_manifest rehearsal | require project dossier check at milestone | Project Mentor | planned |
| CE-2026-SOURCE | 2026-06-05 | CE-END-SURVEY | Students need more examples of source-level downgrade decisions | add one frontier-source audit mini case to final review | Instructor | planned |

## Student-Visible Response Memo Template

```text
Thank you for the midterm feedback.
What we heard:
What we will change by date:
What we will keep and why:
Where to get help:
What evidence we will watch next:
Privacy note:
```

## Staff Observation Note Template

```text
observer_role:
lecture_id:
observed_segment:
learning_goal_alignment:
technical_accuracy:
board_and_slide_clarity:
active_learning:
pacing_and_workload:
inclusion_accessibility:
assessment_alignment:
recommended_change:
student_visible_summary:
private_follow_up:
```

## Release Checklist

| check | passing evidence |
| --- | --- |
| source coverage | CE-PEER-OBS、CE-MID-SURVEY、CE-END-SURVEY、CE-ANALYTICS、CE-GRADING and CE-CAPSTONE all present |
| rubric coverage | peer observation rubric includes learning goals, technical accuracy, board/slide clarity, active learning, pacing, accessibility and assessment alignment |
| response protocol | collect, code, triangulate, publish, update and verify steps have owner and due date |
| review coverage | outcome, accuracy, workload, assessment, project and support/accessibility review areas are defined |
| current ledger | at least 5 evaluation records with source_id, action, owner and status |
| templates | student-visible response memo and staff observation note templates are included |
| privacy boundary | no public student identifiers, raw comments, accommodation details or staff personnel evaluation |
| link coverage | participation guide, operations log, learning analytics, lecture quality, staff runbook and accessibility guide link this dossier |
