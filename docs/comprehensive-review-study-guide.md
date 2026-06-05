# Comprehensive Review Study Guide

复核日期：2026-06-05

本指南把期中 checkpoint、期末复习、书面题、worked examples、reading discussion、recitation worksheet 和 capstone readiness 组织成一条学生可执行的综合复习路径。它补充 [Midterm and Final Review Pack](midterm-final-review-pack.md)、[Quiz and Checkpoint Guide](quiz-checkpoint-guide.md)、[书面推导与概念题题库](written-problem-set.md)、[Worked Example Pack](worked-example-pack.md)、[Topic Dependency and Spiral Review Map](topic-dependency-map.md)、[Reading Discussion Question Bank](reading-discussion-question-bank.md)、[Assessment Blueprint and Coverage Matrix](assessment-blueprint-coverage-matrix.md)、[Concept Mastery and Misconception Map](concept-misconception-map.md)、[Notation and Shape Glossary](notation-shape-glossary.md) 和 [Learning Analytics and Remediation Plan](learning-analytics-remediation-plan.md)。

使用边界：本指南可以进入 student site release；它只给复习路径、公开样题、诊断阈值和补救入口，不包含隐藏测试输入、reference_solution.py、私有评分样例、真实学生提交或教师答案要点。

## Review Outcomes

| outcome_id | student_can_do | primary_evidence | review_source |
| --- | --- | --- | --- |
| CR-O1 | Trace data flow from tokens to logits with shape annotations. | BPE, embedding, RoPE, attention, block, GPT parameter and shape explanations. | midterm-final-review-pack.md, notation-shape-glossary.md |
| CR-O2 | Derive core formulas with assumptions and boundary conditions. | RoPE relative position, attention scaling, CE gradient, AdamW, DPO, KV cache. | mathematical-derivation-audit.md, written-problem-set.md |
| CR-O3 | Diagnose implementation failures without hidden tests. | Shape, mask, dtype, NaN, loss spike, cache, RAG and metric failure explanations. | recitation-worksheet-pack.md, concept-misconception-map.md |
| CR-O4 | Connect readings to code, metrics and source boundaries. | Reading recap, paper-to-code link, source tier, supported and unsupported claims. | reading-discussion-question-bank.md, paper-to-code-traceability-matrix.md |
| CR-O5 | Prepare capstone evidence with reproducibility and evaluation discipline. | Seed, command, log, metric contract, uncertainty, source audit, failure analysis. | project-report-template.md, experimental-rigor-evaluation-statistics.md |

## Two-Pass Review Schedule

| review_id | timing | pass_goal | tasks | exit_check |
| --- | --- | --- | --- | --- |
| CR-S1 | 10-14 days before checkpoint or final review | Rebuild prerequisites and notation. | Read topic-dependency-map.md TD-L0 through TD-L3; redo WE-CH01-BPE, WE-CH02-ROPE and WE-CH03-ATTN; write one page of symbols and shapes. | Can explain B, T, V, D, H, H_kv, D_h, logits, labels and mask without notes. |
| CR-S2 | 7-10 days before | Work core derivations from memory. | Solve written-problem-set.md Ch02, Ch03, Ch07 and Ch10 derivations; compare against public scoring criteria. | Each derivation states assumptions, shape, formula step and limitation. |
| CR-S3 | 5-7 days before | Practice integrated midterm/final tasks. | Complete one Midterm Checkpoint Sample block and two Final Review Sample blocks under time limit. | Score at least 70 percent using public rubric; mark every miss with a failure category. |
| CR-S4 | 3-5 days before | Repair weak dependencies. | Use Dependency Failure Signals and Learning Analytics playbooks for shape, mask, objective, metric, source or systems failures. | Every repeated error maps to a concrete worksheet, worked example or reading question. |
| CR-S5 | 1-2 days before | Consolidate source and project evidence. | Review reading-discussion-question-bank.md Week 7-10 and project-report-template.md claim audit fields. | Can rewrite one overclaim into a scoped, evidenced claim with access date and metric. |
| CR-S6 | Day of review | Reduce avoidable mistakes. | Skim formula/shape sheet, allowed materials policy and personal error log. | Knows allowed materials, duration, regrade boundary and first action for stuck questions. |

## Self-Diagnostic Checklist

| diagnostic_id | prompt | ready_signal | remediation |
| --- | --- | --- | --- |
| CR-D-SHAPE | Can I write the shape of attention scores, context, logits, labels and KV cache from memory? | Yes for at least 5 unseen shape prompts. | Use notation-shape-glossary.md, WE-CH03-ATTN and TD-F-SHAPE. |
| CR-D-MASK | Can I distinguish causal mask, padding mask and label mask, including where each is applied? | Can build a two-token counterexample and explain softmax or loss behavior. | Use concept-misconception-map.md and recitation worksheet mask drills. |
| CR-D-FORMULA | Can I derive RoPE, attention scaling, CE gradient, AdamW and DPO without copying? | Each derivation has assumptions and an unsupported-claim boundary. | Use mathematical-derivation-audit.md and written-problem-set.md. |
| CR-D-OBJECTIVE | Can I separate pretraining, SFT, LoRA, DPO, GRPO, sampling and evaluation? | Can name inputs, labels, ignored tokens or comparison pairs for each objective. | Use core-concept-glossary.md and worked-example-pack.md. |
| CR-D-METRIC | Can I define CE/PPL, UAS/LAS, BLEU, ROUGE, EM/F1, TTFT, TPOT, TPS and P95? | Each metric includes unit, aggregation, denominator and failure mode. | Use notation-shape-glossary.md and WE-CH11-METRICS. |
| CR-D-SOURCE | Can I state what a paper, model card, benchmark or API doc supports and does not support? | Can fill source_record, core_claim, technical_detail, course_link and boundary. | Use reading-discussion-question-bank.md and paper-recap-calibration-pack.md. |
| CR-D-CAPSTONE | Can I turn a demo result into a reproducible project claim? | Claim includes config, command, seed or access date, metric, uncertainty and failure case. | Use project-report-template.md and experimental-rigor-evaluation-statistics.md. |

## Error Log Template

Students should keep a short error log during review rather than rereading everything equally.

| field | what_to_write |
| --- | --- |
| error_id | Stable local ID such as `my-E07-mask-softmax`. |
| source | Sample question, written problem, reading question, worksheet, quiz or project clinic. |
| category | shape, mask, formula, objective, metric, source, systems, reproducibility or policy. |
| first_wrong_step | The earliest incorrect assumption, formula, shape, source claim or interpretation. |
| corrected_rule | One sentence that would prevent the same error next time. |
| evidence_to_redo | Worked example, worksheet, derivation, reading question or project checklist to repeat. |
| cleared_when | Observable evidence such as two correct unseen prompts or one corrected source audit. |

## Practice Set Sequence

| sequence_id | target | practice_order | stop_condition |
| --- | --- | --- | --- |
| CR-P-MIDTERM | Ch01-Ch07 checkpoint readiness | WE-CH01 through WE-CH07, written Ch01-Ch07 selected problems, Midterm Checkpoint Sample, source/reproducibility fragment. | All five midterm modules score at least 70 percent and no category repeats twice. |
| CR-P-FINAL | Ch08-Ch11 and capstone readiness | WE-CH08 through WE-CH11, Final Review Sample A-E, RDQ Week 7-10, one project claim audit. | Can explain decoding, alignment, metrics, serving and source boundaries in one integrated answer. |
| CR-P-SHAPE | Persistent shape or mask weakness | Notation glossary, Ch03 mask drill, Ch04 GQA cache row, Ch10 KV cache formula, two unseen shape prompts. | Two consecutive unseen prompts are correct without notes. |
| CR-P-SOURCE | Persistent source-boundary weakness | Paper recap required fields, RDQ limitation questions, claim audit worksheet, external source verification. | One overclaim is rewritten with source tier, date, setting and unsupported stronger claim. |
| CR-P-PROJECT | Capstone readiness | Project report template, experimental rigor checklist, dataset/artifact registry, data ethics review, final review question E. | Proposal or report claim has reproducible evidence and a fallback if the main experiment fails. |

## Staff Use

| staff_action | when_to_use | evidence |
| --- | --- | --- |
| CR-STAFF-RECAP | At least 30 percent of students miss the same diagnostic category. | Aggregate category, chosen recap, follow-up worksheet and exit criterion. |
| CR-STAFF-OH | Office hours show repeated blocker for the same dependency. | Topic dependency failure ID, FAQ or worksheet update, and privacy-preserving note. |
| CR-STAFF-CALIBRATE | Scores cluster too high, too low or too inconsistently on a review sample. | Assessment item analysis, anchor sample comparison and rubric clarification. |
| CR-STAFF-SCOPE | Capstone review reveals missing reproducibility, metric or source evidence. | Project mentor note, revised scope, source boundary and fallback evidence. |

## Release Checklist

- Review Outcomes cover data flow, derivations, implementation diagnosis, reading/source evidence and capstone evidence.
- Two-Pass Review Schedule includes at least six timed review stages with exit checks.
- Self-Diagnostic Checklist covers shape, mask, formula, objective, metric, source and capstone readiness.
- Error Log Template includes source, category, first wrong step, corrected rule, redo evidence and clearance evidence.
- Practice Set Sequence maps midterm, final, shape, source and project review to existing course materials.
- Staff Use connects aggregate review failures to recap, office hours, calibration and scope adjustment.
- Student site release excludes hidden tests, reference_solution.py, private grading samples, real student submissions and instructor-only answer keys.
