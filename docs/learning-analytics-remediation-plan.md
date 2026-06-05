# Learning Analytics and Remediation Plan

复核日期：2026-06-05

本计划把 quiz、作业测试、recitation worksheet、office hours、阅读复盘、项目 milestone 和 gradebook 聚合信号转化为可执行的补救教学动作。它补充 [Quiz and Checkpoint Guide](quiz-checkpoint-guide.md)、[Assessment Item Analysis and Psychometrics Guide](assessment-item-analysis-psychometrics.md)、[Learning Outcome Attainment Report](learning-outcome-attainment-report.md)、[Concept Mastery and Misconception Map](concept-misconception-map.md)、[Topic Dependency and Spiral Review Map](topic-dependency-map.md)、[Recitation Worksheet Pack](recitation-worksheet-pack.md)、[Weekly Teaching Reflection and Adjustment Log](weekly-teaching-reflection-adjustment-log.md)、[Workload and Pacing Calibration](workload-pacing-calibration.md)、[Gradebook and LMS Operations Guide](gradebook-lms-operations.md)、[Participation and Feedback Guide](participation-feedback-guide.md)、[Teaching Observation and Course Evaluation Dossier](teaching-observation-course-evaluation.md)、[Course Staff Runbook](staff-runbook.md)、[Accessibility and Student Support Guide](accessibility-student-support.md) 和 [Course Operations and Improvement Log](course-operations-log.md)。

目标不是用数据替代教师判断，而是确保学生在进入下一模块、midterm checkpoint 或 capstone 前，能收到及时、可解释、可复核的补救路径。

## Data Sources

| Signal ID | Source | Granularity | Student-visible use | Privacy boundary |
|-----------|--------|-------------|---------------------|------------------|
| LA-QUIZ | quick check / recap quiz | aggregate by concept and item type | 发布 common issues、recap topic、补救 worksheet | 不公布个人分数或题目答案库 |
| LA-ASSIGN | public/hidden category results | aggregate by assignment and failure category | 发布类别级 feedback、FAQ、discussion drill | 不泄露 hidden-test input 或其他学生代码 |
| LA-WORKSHEET | recitation worksheet exit ticket | aggregate by worksheet field | 安排 recap、shape drill、paper-to-code drill | 不公开个人 exit ticket |
| LA-OH | office hours triage | aggregate by question category | 更新 FAQ、office hours slot 和 starter hints | 不记录健康、家庭或诚信细节 |
| LA-READING | paper recap rubric fields | aggregate by missing field | 安排 source audit 或 paper-to-code drill | 不公开学生原文复盘 |
| LA-PROJECT | proposal/milestone/project report checks | team-level mentor view plus aggregate course risk | 安排 mentor check、scope downgrade 或 project clinic | 不公开团队内部冲突或私密请求 |
| LA-GRADEBOOK | LMS gradebook export | private individual plus aggregate distribution | 发布成绩分布摘要和补救建议 | 个人成绩、late days、accommodation 和 integrity hold 只在授权人员内可见 |

## Trigger Thresholds

| Trigger ID | Condition | Evidence | Required action | Owner | SLA |
|------------|-----------|----------|-----------------|-------|-----|
| TR-SHAPE-30 | 同一 shape invariant 错误率 >= 30% | LA-QUIZ or LA-WORKSHEET | 下一讲 5-8 分钟 recap；追加对应 worksheet shape table | Discussion TA | next lecture |
| TR-MASK-20 | mask / ignore-index / label-direction 错误率 >= 20% | LA-ASSIGN or LA-QUIZ | 发布 failure drill；office hours 加一段最小反例演示 | Head TA | 48 hours |
| TR-SOURCE-30 | 阅读复盘中 source boundary 缺失率 >= 30% | LA-READING | 安排 paper-to-code drill；更新 paper recap feedback | Discussion TA | next recitation |
| TR-PROJECT-RISK | milestone 缺 seed/log/metric/source boundary 的团队数 >= 3 | LA-PROJECT | 开 project clinic；要求风险团队提交 revised scope | Project Mentor | 1 week |
| TR-REPRO-20 | reproducibility check 未通过率 >= 20% | LA-PROJECT or LA-QUIZ | 指派 capstone rehearsal worksheet；检查第一条复现命令 | Project Mentor | 1 week |
| TR-REVIEW-8 | 双评或复核分差超过 8 分 | LA-GRADEBOOK | 暂停该 rubric 项批改；重新校准 anchor sample | Head TA | before release |
| TR-OH-3 | 同一 blocker 在一周 office hours 出现 >= 3 次 | LA-OH | 更新 FAQ、discussion guide 或 starter hint | Course Manager | 72 hours |
| TR-ACCESS | 学生正式便利安排或支持请求影响评估形式 | private support channel | 提供等价任务或时间/形式调整 | Instructor | per school policy |

## Remediation Playbooks

| Playbook ID | Use when | Student task | Staff evidence | Exit criterion |
|-------------|----------|--------------|----------------|----------------|
| RP-SHAPE | shape trace or tensor axis confusion | 完成对应 [Recitation Worksheet Pack](recitation-worksheet-pack.md) 的 shape table，并解释 axis meaning | worksheet snapshot or oral check note | 学生能独立写出 2 个新 shape |
| RP-MASK | attention mask, SFT label mask, MLM label mask 或 ignore-index 错误 | 写一个最小反例，说明正确 mask 应出现在 softmax/loss 的哪个阶段 | minimal reproduction and corrected explanation | 学生能解释失败输入和修复条件 |
| RP-NUMERIC | NaN、overflow、grad norm、scheduler 或 dtype 问题 | 提交 1 页 debug trace：command、seed、log、hypothesis、next check | office hours triage note | log 不再缺命令/seed/step |
| RP-SOURCE | 论文、模型卡或 benchmark claim 过强 | 填写 source tier、access date、supported claim、unsupported stronger claim | paper recap field check | source boundary 字段完整 |
| RP-REPRO | 项目报告缺复现链 | 运行 capstone acceptance 或项目第一条复现命令，并记录环境和输出摘要 | command output and artifact path | 第三方能复跑首个结果 |
| RP-PROJECT-SCOPE | 项目指标、数据、算力或时间风险过高 | 提交 revised scope：baseline、fixed eval set、fallback、mentor question | mentor checkpoint note | scope 与资源和周历匹配 |

## Weekly Review Workflow

| Step | Input | Staff action | Public output |
|------|-------|--------------|---------------|
| 1. collect | quiz summary、assignment category failures、worksheet exit tickets、office hours triage、reading recap fields | Course Manager 汇总聚合信号 | none |
| 2. classify | Concept Mastery and Misconception Map categories | Head TA 标记 shape / math / implementation / source / reproducibility / policy | none |
| 3. choose action | Trigger Thresholds and Remediation Playbooks | Staff meeting 选择 recap、worksheet、FAQ、project clinic 或 calibration | weekly announcement common issues |
| 4. deliver | lecture slot、recitation、office hours、project mentor check | 负责 staff 执行动作并记录完成状态 | student-visible remediation instructions |
| 5. verify | follow-up quiz、worksheet, office-hour oral check, project rerun, grade release audit | 判断是否达成 exit criterion | aggregate improvement note |
| 6. log | Course Operations and Improvement Log | 记录日期、信号、动作、owner、结果和下一步 | only aggregate, no personal details |

## Student-Facing Feedback Template

```text
Topic:
Observed pattern: aggregate category only
Why it matters:
What to redo:
Evidence to submit:
Deadline or suggested date:
Office hours / discussion support:
What this does not imply about your grade:
```

## Operations Log Template

```text
date:
signal_id:
trigger_id:
affected_module:
aggregate_evidence:
action_taken:
owner:
student_visible_message:
privacy_check:
exit_criterion:
follow_up_result:
next_action:
```

## Privacy and Fairness Rules

- 使用聚合类别触发课程级补救；个人成绩、late days、accommodation、健康、家庭、身份、诚信个案和 regrade 细节不进入公开材料。
- 补救任务用于恢复学习路径，不应作为额外惩罚；若要计分，必须在 syllabus、gradebook 和 assessment policy 中预先说明。
- 同一能力目标的补救任务可以更换数字、语料、日志或论文，但必须保持等价难度。
- 对正式便利安排、医疗或突发事件，使用私密渠道和等价 assessment，不把原因透露给队友或全班。
- 任何由 hidden tests 得出的反馈只能发布类别级信息，例如 "mask broadcast failure"，不得发布隐藏输入、断言细节或私有参考解。

## Release Checklist

| Check | Passing evidence |
|-------|------------------|
| Signal coverage | LA-QUIZ、LA-ASSIGN、LA-WORKSHEET、LA-OH、LA-READING、LA-PROJECT、LA-GRADEBOOK all present |
| Trigger coverage | at least 8 trigger rows with condition, evidence, action, owner and SLA |
| Playbook coverage | RP-SHAPE、RP-MASK、RP-NUMERIC、RP-SOURCE、RP-REPRO、RP-PROJECT-SCOPE all present |
| Privacy boundary | guide states aggregate-only public reporting and excludes personal grades, accommodations, integrity and hidden-test details |
| Link coverage | quiz guide、misconception map、recitation worksheet、gradebook/LMS、participation guide、staff runbook and operations log link this plan |
| Verification | `.venv/bin/python verify_course.py` reports `PASS learning analytics remediation plan ...` |
