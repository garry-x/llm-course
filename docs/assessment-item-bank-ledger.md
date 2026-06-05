# Assessment Item Bank Ledger

本文件记录 quiz、recap check、midterm checkpoint、final review 和 capstone readiness check 的公开安全题库元数据。它补充 [Assessment Blueprint and Coverage Matrix](assessment-blueprint-coverage-matrix.md)、[Assessment Item Analysis and Psychometrics Guide](assessment-item-analysis-psychometrics.md)、[Quiz and Checkpoint Guide](quiz-checkpoint-guide.md)、[Midterm and Final Review Pack](midterm-final-review-pack.md)、[Assessment Administration and Exam Integrity Policy](assessment-administration-policy.md)、[Course Calendar and Deadline Ledger](course-calendar-deadline-ledger.md)、[Gradebook and LMS Operations Guide](gradebook-lms-operations.md) 和 [Course Operations and Improvement Log](course-operations-log.md)。

复核日期：2026-06-05
公开口径：本文件只记录能力标签、样题来源、变体策略、曝光等级、退役触发和评分证据，不包含 active assessment 的完整题面、隐藏 rubric、学生答案、监考记录或私有评分脚本。
维护原则：每道正式计分题必须能映射到章节、作业、reading recap、project rubric 或 capstone evidence；题面可变，但能力目标和评分标准必须稳定。

## Exposure Levels

| exposure_level | 含义 | 可公开内容 | 禁止公开 |
|----------------|------|------------|----------|
| public_sample | 学生可见样题或复习题 | 能力目标、题面、评分要点、补救路径 | 隐藏测试、active 变体答案库 |
| practice_variant | 讨论课或作业后练习变体 | 题型、数字/语料变体、讲评摘要 | 即将用于计分的同题面 |
| active_assessment | 当前或即将计分题 | 只公开 assessment 规则、范围和 allowed materials | 完整题面、细项 rubric、参考答案 |
| retired | 不再用于计分 | 可公开讲评、常见错误和参考思路 | 仍可复用的私有变体 |

## Item Metadata Schema

| Field | Required content |
|-------|------------------|
| item_bank_id | 稳定编号，例如 `QC-W2-MASK-01` |
| assessment_type | lecture_quick_check、recap_quiz、midterm_checkpoint、final_review_quiz、capstone_readiness_check |
| learning_objective | 章节、DER ID、claim ID、assignment 或 project rubric |
| source_material | 对应章节、handout、paper recap、capstone README 或 review pack |
| exposure_level | public_sample、practice_variant、active_assessment、retired |
| variant_policy | 如何替换数字、语料、日志片段、模型声明或 metric |
| evidence_required | 学生答案必须包含的 shape、formula、boundary、command 或 source record |
| remediation_link | 低分后对应的补救材料 |
| retirement_trigger | 何时退役或替换 |

## Public-Safe Item Bank

| item_bank_id | assessment_type | learning_objective | source_material | exposure_level | variant_policy | evidence_required | remediation_link | retirement_trigger |
|--------------|-----------------|--------------------|-----------------|----------------|----------------|-------------------|------------------|--------------------|
| QC-W1-BPE-01 | recap_quiz | DER-01; Ch01 BPE | Ch01; Midterm Review Q1 | public_sample | 替换小语料、pair tie 和 vocab target | pair counts、merge rule、greedy boundary | Ch01 tests; Board Derivation Pack BPE | 平均通过率 >95% 且无区分度 |
| QC-W2-MASK-01 | lecture_quick_check | DER-05; Ch03 causal mask | Quiz Guide Week 2; Midterm Review Q3 | public_sample | 替换 `T`、mask 形状和 decode query 场景 | lower-triangular visibility、softmax-before-mask rationale | Ch03 tests; discussion mask drill | 学生只记答案矩阵，不能解释 broadcast |
| QC-W3-CACHE-01 | recap_quiz | DER-06; Ch04/Ch10 KV cache | Ch04; Ch10; Midterm Review Q3 | practice_variant | 替换 batch、layers、context、KV heads、dtype | formula with K/V factor、bytes/GiB estimate、GQA boundary | Ch04/Ch10 tests; Mathematical Derivation Audit | 公式或单位错误率连续两周低于 5% |
| QC-W5-TRAIN-01 | midterm_checkpoint | DER-09; DER-10; Ch07 training loop | Midterm Review Q4; Training capstone | public_sample | 替换日志片段、optimizer setting、scheduler boundary | right-shift labels、CE/AdamW distinction、failure diagnosis | Ch07 tests; training capstone README | 题面日志被公开复用为标准答案 |
| QC-W6-SAMPLING-01 | recap_quiz | DER-11; Ch08 sampling | Final Review Q A | practice_variant | 替换概率分布、`k`、`p` 和 max token condition | top-k/top-p retained set、renormalization or quality boundary | Ch08 tests; Paper Recap Calibration PR-B1 | 通过率 >95% 且 discussion 无新错误 |
| QC-W7-DPO-01 | recap_quiz | DER-12; Ch09 DPO/GRPO | Final Review Q B | practice_variant | 替换 chosen/rejected log-prob table 和 group rewards | log-ratio direction、advantage whitening boundary | Ch09 tests; alignment written problem | chosen/rejected 方向题被背诵化 |
| QC-W8-EVAL-01 | final_review_quiz | DER-14; Ch11 evaluation | Final Review Q C; Classic NLP handout | public_sample | 替换 metric examples、reference answers 或 parse labels | UAS/LAS, BLEU/ROUGE/EM/F1 assumptions and limitation | Ch11 tests; Experimental Rigor Guide | 指标定义变化或题面样例进入公开答案库 |
| QC-W9-SLO-01 | capstone_readiness_check | DER-13; inference capstone SLO | Final Review Q D; inference capstone | practice_variant | 替换 benchmark JSON、concurrency、SLO thresholds | TTFT/TPOT/P95/error-rate judgment and capacity caveat | inference capstone acceptance; SLO report | 真实项目改用不同 SLO schema |
| QC-W10-SOURCE-01 | final_review_quiz | source boundary; project evidence | Final Review Q E; External Source Verification | public_sample | 替换模型卡/API/benchmark claim 和 access date | source level、access date、configuration, non-generalization statement | Paper Recap Calibration Pack; Frontier Source Audit | 官方来源页面结构变化 |
| QC-MAKEUP-EQUIV-01 | makeup_assessment | same objective as affected assessment | Assessment Administration Policy | active_assessment | 使用同一能力目标但替换数字、语料、日志和 claim | equivalence map, allowed materials, private accommodation path | accessibility guide; gradebook/LMS guide | 原题答案公开或学生完成补测 |

## Rotation Procedure

1. 每次计分 assessment 前，从本表选择能力目标；若使用 `public_sample`，必须创建新的 `active_assessment` 变体，不直接复用公开题面。
2. 变体只能替换数字、语料、日志片段、模型声明、metric 表或 source claim；不能改变学习目标和评分证据。
3. 每次使用后在 [Course Operations and Improvement Log](course-operations-log.md) 记录 item_bank_id、平均通过率、低分簇和是否退役。
4. 若 item 平均通过率低于 60%，下一讲或讨论课安排 recap；若高于 95% 且无区分度，替换为更诊断性的变体。
5. 若题面、答案、hidden rubric 或 active variant 泄露，立即把 exposure_level 改为 `retired`，并按 [Academic Integrity Case Process](academic-integrity-case-process.md) 处理。

## Equivalence and Makeup Rules

| Scenario | Equivalent requirement |
|----------|------------------------|
| illness / emergency makeup | 同一 learning_objective，替换题面数据和日志片段 |
| accommodation alternative | 保持能力目标，调整时长、口头/书面形式或辅助技术 |
| remote oral check | 使用学生自己的推导、日志或项目证据，不引入新隐藏测试 |
| LMS outage | 统一补窗口或替代提交，不消耗 late day |
| integrity retake | 使用 retired 不同源变体，并保留私密 review record |

## Release Checklist

- 不包含 active assessment 完整题面、隐藏 rubric、reference solution 或学生提交。
- 至少覆盖 Week 1-10 的核心能力：tokenization、mask、cache、training、sampling、alignment、evaluation、serving、source audit。
- 每个 item 都有 learning_objective、variant_policy、evidence_required、remediation_link 和 retirement_trigger。
- Makeup equivalence 规则覆盖 illness、accommodation、remote oral check、LMS outage 和 integrity retake。
- 本文件与 quiz/checkpoint guide、midterm/final review pack、assessment administration policy、deadline ledger、gradebook/LMS guide 和 operations log 互相链接。
