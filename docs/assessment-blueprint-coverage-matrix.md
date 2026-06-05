# Assessment Blueprint and Coverage Matrix

复核日期：2026-06-05

本 blueprint 把课程目标、评估渠道、认知层级、证据类型和发布 gate 放在同一张可审计矩阵中。它补充 [Course Outcome Map](course-outcome-map.md)、[Topic Dependency and Spiral Review Map](topic-dependency-map.md)、[Comprehensive Review Study Guide](comprehensive-review-study-guide.md)、[Reading Discussion Question Bank](reading-discussion-question-bank.md)、[Safety and Societal Impact Casebook](safety-societal-impact-casebook.md)、[Learning Outcome Attainment Report](learning-outcome-attainment-report.md)、[Assignment Handout Pack](assignment-handout-pack.md)、[Programming Assignment Code Quality Rubric](programming-assignment-code-quality-rubric.md)、[Core Concept Glossary](core-concept-glossary.md)、[Notation and Shape Glossary](notation-shape-glossary.md)、[书面推导与概念题题库](written-problem-set.md)、[Quiz and Checkpoint Guide](quiz-checkpoint-guide.md)、[Assessment Item Bank Ledger](assessment-item-bank-ledger.md)、[Assessment Item Analysis and Psychometrics Guide](assessment-item-analysis-psychometrics.md)、[Midterm and Final Review Pack](midterm-final-review-pack.md)、[Project Report Template and Reproducibility Checklist](project-report-template.md)、[Project Submission Dossier](project-submission-dossier.md)、[Capstone Defense and Oral Exam Question Bank](capstone-defense-oral-exam-bank.md)、[Capstone 项目报告 Rubric](project-report-rubric.md)、[Grading Calibration Guide](grading-calibration.md) 和 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md)。

公开边界：本文件只发布 coverage、证据类型、最低标准和复核规则，不发布 active assessment 完整题面、隐藏测试、reference solution、学生答案或私有评分脚本。

## Blueprint Dimensions

| dimension | required value | use in review |
| --- | --- | --- |
| outcome_id | `CO1` 至 `CO6` | 与 course outcome map 一一对应 |
| assessment_channel | programming assignment、written derivation、quiz/checkpoint、capstone artifact、reading/source audit、presentation/peer review | 防止只用单一考试或单一代码测试证明能力 |
| cognitive_level | remember、understand、apply、analyze、evaluate、create | 确认课程从基础术语到开放项目逐级上升 |
| evidence_type | auto_test、written_derivation、quiz_checkpoint、capstone_artifact、peer_review、source_audit、manual_rubric | 区分自动证据和人工评分证据 |
| scoring_owner | autograder、TA、instructor、mentor、peer panel | 明确谁能改分、谁能复核 |
| gate | auto_gate、written_gate、checkpoint_gate、capstone_gate、source_gate、rubric_calibration_gate、accessibility_integrity_gate | 发布前和成绩发布前的阻断条件 |

## Outcome Coverage Matrix

| outcome_id | student_work | assessment_channel | cognitive_level | automated_evidence | manual_evidence | minimum_standard | remediation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CO1 | Ch01-Ch06 programming traces; written shape and data-flow questions; midterm checkpoint | programming assignment; written derivation; quiz/checkpoint | understand; apply; analyze | Ch01-Ch06 public/hidden tests; `run_assignment_tests.py`; causal-mask and shape checks | written BPE/attention/cache reasoning; TA review of shape trace | Student can trace tokenization, embedding, RoPE, attention, MLP, residual/norm, logits and loss without hidden state shape errors | Ch01-Ch06 tests; Board Derivation Pack; QC-W1-BPE-01; QC-W2-MASK-01; QC-W3-CACHE-01 |
| CO2 | PyTorch modules across Ch01-Ch11; debugging logs; code-quality review | programming assignment; capstone artifact | apply; analyze | assignment tests; smoke tests; acceptance tests; device/dtype checks | code review on module boundaries, initialization, masks and training loop choices | Implementations are idiomatic PyTorch and pass public tests plus hidden boundary categories | Assignment Handout Pack; Autograder Hidden Tests; Python/PyTorch Review Session |
| CO3 | DER-01 through DER-14 written derivations; midterm/final review proofs; complexity estimates | written derivation; quiz/checkpoint | understand; analyze; evaluate | formula-linked tests for BPE, attention, cache, loss, SFT/DPO and metrics | written rubric for assumptions, units, directionality and limitation statements | Derivations include variables, assumptions, units, edge cases and conclusion in the expected direction | Mathematical Derivation Audit; written-problem-set.md; midterm-final-review-pack.md |
| CO4 | Training engineering capstone; inference engineering capstone; SLO/capacity and reproducibility dossiers | capstone artifact; presentation/peer review | apply; analyze; evaluate; create | `verify_course.py --capstone --training`; SLO acceptance; project artifact manifest | mentor review of split_card, metric_card, uncertainty_record, claim_audit and downgrade decisions | Capstone result is reproducible, resource-aware, statistically qualified and tied to an engineering decision | Project Submission Dossier; Experimental Rigor Guide; QC-W9-SLO-01 |
| CO5 | Weekly paper recaps; source verification records; project citation and claim audit | reading/source audit; written derivation; capstone artifact | analyze; evaluate | manifest marker checks; source inventory checks; frontier-source audit gates | TA calibration of source_record, technical_detail, boundary and non-generalization claims | Claims distinguish official docs, papers, course notes, third-party summaries, benchmark reports and personal inference | Paper Recap Calibration Pack; External Source Verification; QC-W10-SOURCE-01 |
| CO6 | Ch11 classic NLP assignment; evaluation written questions; final review evaluation item; project metrics | programming assignment; written derivation; quiz/checkpoint; capstone artifact | remember; understand; apply; evaluate | Ch11 tests; metric smoke tests; final review coverage checks | written comparison of UAS/LAS, BLEU/ROUGE/EM/F1 assumptions and limitations | Student can select and critique classic NLP and LLM evaluation metrics for a stated task | Classic NLP Handout; NLP Evaluation Coverage; QC-W8-EVAL-01 |

## Assessment Channel Balance

| channel | target_weight | primary_outcomes | required_evidence | balancing_rule |
| --- | --- | --- | --- | --- |
| programming assignments | 35% | CO1; CO2; CO3; CO6 | public tests, hidden categories, submitted code, short written explanation | No assignment may rely only on snapshot output; at least one boundary or error-analysis item is required |
| written derivations | 20% | CO1; CO3; CO5; CO6 | written_answers, formula assumptions, units, complexity, source boundary | At least half of written credit targets reasoning not reproduced by autograder tests |
| training capstone | 15% | CO2; CO4; CO5 | training logs, data split, metric card, uncertainty record, compute budget | Single-seed or undocumented data runs cannot receive full evidence credit |
| inference capstone | 20% | CO2; CO4; CO5; CO6 | SLO report, load test, failure analysis, retrieval/generation trace, cost estimate | Throughput or latency claims require configuration and hardware context |
| reading/participation/peer review | 10% | CO5; CO6 | paper recap, seminar reflection, peer-review form, discussion worksheet | Credit is for evidence quality and question specificity, not attendance alone |

## Cognitive Level Ladder

| cognitive_level | course examples | evidence gate |
| --- | --- | --- |
| remember | define token, logit, cross entropy, UAS/LAS, BLEU, ROUGE, EM, F1 | quiz_checkpoint |
| understand | explain BPE merge, causal masking, RoPE rotation, KV-cache memory and metric assumptions | written_gate |
| apply | implement modules in PyTorch and run deterministic tests | auto_gate |
| analyze | diagnose shape, dtype, leakage, instability, latency and metric failure modes | auto_gate; manual_rubric |
| evaluate | compare decoding, alignment, evaluation and source claims under stated constraints | source_gate; rubric_calibration_gate |
| create | build, report and defend a training or inference capstone with reproducibility evidence | capstone_gate |

## Sampling and Rotation Rules

| rule_id | rule | evidence |
| --- | --- | --- |
| blueprint_sample_coverage | Each graded term samples every `CO1`-`CO6` at least once through automatic evidence and once through manual evidence | outcome matrix and gradebook category map |
| item_bank_rotation | Active quiz/checkpoint variants must be selected from the item bank and logged with exposure_level, variant_policy and retirement_trigger | Assessment Item Bank Ledger; QC-W1-BPE-01; QC-W2-MASK-01; QC-W8-EVAL-01; QC-W9-SLO-01; QC-W10-SOURCE-01 |
| makeup_equivalence | Makeup assessment uses the same outcome_id and cognitive_level but changes numbers, corpus, log snippets or claim sources | QC-MAKEUP-EQUIV-01; Assessment Administration Policy |
| hidden_boundary | Hidden tests may assess boundary categories but cannot become quiz题面、written reference answer or public review answer | Autograder Hidden Tests; Private Autograder Operations |
| source_audit_rotation | Each offering samples at least one model/API claim and one benchmark/evaluation claim for source-level review | External Source Verification; Frontier Source Audit |
| capstone_readiness | Capstone checkpoints cannot proceed to final report without split_card, metric_card, uncertainty_record and claim_audit | Project Submission Dossier; Project Report Rubric |

## Evidence and Grading Gates

| gate | blocks release when | required record |
| --- | --- | --- |
| auto_gate | assignment, capstone or release tests fail, or public/hidden category naming is missing | test command, commit/version, failed suite, remediation owner |
| written_gate | derivation rubric lacks assumptions, variables, units, edge cases or grading anchors | rubric version, anchor sample, TA calibration note |
| checkpoint_gate | quiz/checkpoint lacks assessment_id, allowed materials, duration, makeup path or item-bank link | assessment administration record |
| capstone_gate | project evidence lacks split_card, metric_card, uncertainty_record, claim_audit or reproducibility manifest | project submission dossier |
| source_gate | paper/model/benchmark claim lacks source level, access date, configuration or boundary statement | source_record and claim_audit |
| rubric_calibration_gate | TA grading drift exceeds threshold or no anchor sample exists for a manual category | grading calibration and drift audit record |
| accessibility_integrity_gate | timing, accommodation, remote assessment or integrity process was changed without public notice | LMS announcement, accommodation path, case record |

## Gap Audit

| gap_check | status | evidence |
| --- | --- | --- |
| all outcomes represented | covered | `CO1`, `CO2`, `CO3`, `CO4`, `CO5`, `CO6` appear in graded channels |
| each outcome has automatic and manual evidence | covered | outcome matrix includes automated_evidence and manual_evidence for every row |
| no single artifact dominates assessment | covered | assessment channel balance splits programming, written, capstone, reading and peer evidence |
| classic NLP and evaluation are not optional extras | covered | CO6 links Ch11, final review and project metric evidence |
| source and frontier uncertainty are graded | covered | CO5 requires source_record, access date, configuration and non-generalization boundary |
| create-level evidence exists | covered | CO4 capstones require reproducible artifact, decision record and presentation defense |
| makeup and accessibility are blueprint-aware | covered | makeup equivalence preserves outcome_id and cognitive_level while changing item surface |

## Release Checklist

- [ ] Syllabus links this assessment blueprint before the term starts.
- [ ] Course Outcome Map lists this file as the assessment blueprint.
- [ ] Assessment Item Bank Ledger, Quiz and Checkpoint Guide, Assignment Handout Pack and Written Problem Set link this file.
- [ ] Gradebook categories match the Assessment Channel Balance table.
- [ ] `verify_course.py` passes `check_assessment_blueprint_coverage_matrix`.
- [ ] Student-safe release includes this file and excludes active assessment internals.
