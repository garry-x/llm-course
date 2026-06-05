# Workload and Pacing Calibration

复核日期：2026-06-05

本文件用于校准 10-12 周高校课程的学习负荷、难度阶梯和截止节奏。它补充 [课程 Syllabus](syllabus.md)、[Course Calendar and Deadline Ledger](course-calendar-deadline-ledger.md)、[Assignment Handout Pack](assignment-handout-pack.md)、[Recitation Worksheet Pack](recitation-worksheet-pack.md)、[Reading List](reading-list.md)、[Learning Analytics and Remediation Plan](learning-analytics-remediation-plan.md)、[Compute Resource and Cost Guide](compute-resource-guide.md) 和 [Course Operations and Improvement Log](course-operations-log.md)。

目标不是把每名学生的时间固定成同一个数字，而是给教师、助教和学生一个可审计的 workload budget：每周学什么、预计投入多少小时、什么时候应触发补救、什么时候应降载或拆分。

## Calibration Assumptions

| Assumption | Default |
|------------|---------|
| Offering length | 10 周压缩版；12 周扩展版可拆分 Week 8 和 Week 10 |
| Contact time | 每周 2 次 lecture，每次 80-90 分钟；1 次 discussion / recitation 50-75 分钟 |
| Student preparation | 每周 1-2 小时阅读；项目周增加 1-2 小时 project planning |
| Assignment cadence | 每周一个小型编程+书面作业；capstone milestone 与作业错峰 |
| Expected weekly effort | 普通周 8-11 小时；capstone 周 10-13 小时 |
| Overload boundary | 连续两周超过 13 小时或低分簇集中在同一模块时，触发 pacing review |

## Weekly Workload Budget

| Week | Main topic | Lecture hours | Reading hours | Assignment hours | Recitation / quiz hours | Project hours | Total target | Pacing note |
|------|------------|:--:|:--:|:--:|:--:|:--:|:--:|-------------|
| Week 1 | BPE, Embedding, RoPE | 3.0 | 1.5 | 4.0 | 1.0 | 0.0 | 9.5 | 重点在环境、shape 和 round trip；Borderline 学生参加 review session |
| Week 2 | Attention and masking | 3.0 | 1.5 | 4.5 | 1.0 | 0.0 | 10.0 | mask / softmax / backprop 是第一处难度跃迁 |
| Week 3 | MHA, GQA, MLA, Block | 3.0 | 1.5 | 5.0 | 1.0 | 0.0 | 10.5 | cache shape 与 norm/FFN 可拆成 12 周版两次作业 |
| Week 4 | GPT assembly and MoE | 3.0 | 1.5 | 4.5 | 1.0 | 0.5 | 10.5 | 参数审计、MoE routing 和 next-token objective 合并复习 |
| Week 5 | Training loop | 3.0 | 1.5 | 5.0 | 1.0 | 1.5 | 12.0 | training proposal 开始；checkpoint 和 loss 诊断需要 office hours 支持 |
| Week 6 | Generation and decoding | 3.0 | 1.5 | 4.5 | 1.0 | 1.0 | 11.0 | top-p / speculative decoding 与训练项目反馈错峰 |
| Week 7 | SFT, LoRA, DPO, GRPO | 3.0 | 1.5 | 5.0 | 1.0 | 1.5 | 12.0 | alignment 作业概念密度高；DPO/GRPO 需 recitation worksheet |
| Week 8 | Classic NLP and evaluation | 3.0 | 2.0 | 4.0 | 1.0 | 2.0 | 12.0 | 经典 NLP、评测和同伴 review 并行；12 周版建议拆分 |
| Week 9 | Inference, RAG, serving | 3.0 | 1.5 | 5.0 | 1.0 | 2.0 | 12.5 | serving benchmark 和 inference proposal 需固定 SLO 和机器配置 |
| Week 10 | Capstone, frontier seminar, final review | 3.0 | 1.0 | 1.5 | 1.0 | 6.0 | 12.5 | 不再新增重型作业；重点是报告、展示、复现和来源边界 |

## Difficulty Ladder

| Level | Weeks | Cognitive demand | Evidence |
|-------|-------|------------------|----------|
| D1 Foundations | Week 1-2 | shape、lookup、mask、softmax、最小 PyTorch API | Ch01-Ch03 tests; quick checks; recitation W1-W2 |
| D2 Architecture | Week 3-4 | head reshape、cache、norm、residual、decoder-only objective、MoE | Ch04-Ch06 tests; written shape and parameter audits |
| D3 Optimization and generation | Week 5-7 | CE/AdamW、scheduler、sampling、SFT/LoRA/DPO/GRPO | Ch07-Ch09 tests; midterm checkpoint; project proposal |
| D4 Evaluation and systems | Week 8-9 | classic NLP metrics、RAG、SLO、capacity planning、source boundary | Ch10-Ch11 tests; peer review; inference proposal |
| D5 Synthesis | Week 10 | reproducible project report、demo、artifact archive、frontier source audit | capstone acceptance; project report rubric; final showcase |

## Assignment Load Guardrails

| Guardrail | Passing condition | Action when exceeded |
|-----------|------------------|----------------------|
| Public test runtime | Each chapter public test suite should run in seconds on CPU | Split slow tests or move to optional/project path |
| Starter scope | One assignment should focus on 3-6 core functions or a tightly related module | Move extra experiments to optional analysis |
| Written questions | 2-3 required written questions per assignment | Convert additional questions to review pack or discussion worksheet |
| Hidden test category count | Hidden categories cover boundary conditions, not unrelated new features | Retire categories that require unstated APIs |
| Capstone overlap | Proposal/milestone should not coincide with the heaviest new programming assignment without support | Add project clinic, extend feedback window, or reduce optional tasks |
| Reading density | Required readings should fit 1-2 hours per week | Move extra papers to optional or seminar |

## Overload Signals and Pacing Actions

| Signal | Threshold | Evidence source | Pacing action |
|--------|-----------|-----------------|---------------|
| workload_over_13h | median self-report > 13 hours for two consecutive weeks | midterm/final feedback; participation survey | reduce optional analysis, add recap, or shift reading to optional |
| public_test_blocker | same public test blocks >= 30% of students | assignment logs; office hours triage | publish category hint and add failure drill |
| written_low_cluster | written item average < 60% with common misconception | quiz/checkpoint; grading calibration | add board derivation recap and worksheet |
| project_scope_risk | >= 3 teams miss seed/log/metric/source boundary | project milestone review | run project clinic and require revised scope |
| reading_recap_gap | >= 30% missing technical_detail or source_boundary | paper recap calibration | add paper-to-code drill |
| regrade_spike | regrade requests > 15% of submissions or same rubric dispute > 5 cases | gradebook/LMS operations | pause release if needed; revise rubric explanation |

## 10-to-12 Week Expansion Map

| 10-week pressure point | 12-week adjustment | Benefit |
|------------------------|-------------------|---------|
| Week 3 combines MHA/GQA/MLA and norm/FFN | Split Ch04 attention variants and Ch05 block/norm into separate weeks | More time for cache and gradcheck |
| Week 7 combines SFT/LoRA/DPO/GRPO | Move GRPO/source boundary discussion into seminar week | Reduces alignment concept density |
| Week 8 combines classic NLP, evaluation, ethics and peer review | Split classic NLP architectures and evaluation/ethics | Allows more metric failure examples |
| Week 10 combines final review, frontier seminar and capstone showcase | Separate final project rehearsal and public showcase | More time for reproducibility review |

## Student Time-Planning Template

```text
Week:
Lecture preparation hours:
Reading hours:
Programming hours:
Written-question hours:
Recitation / office hours:
Project hours:
First blocker:
Evidence I can submit:
What I will move to office hours:
```

## Staff Review Protocol

1. 每周 staff meeting 对照 workload budget、quick check 通过率、office hours 高频问题和 project risk。
2. 若触发 [Learning Analytics and Remediation Plan](learning-analytics-remediation-plan.md) 的 pacing signal，记录 action owner 和 follow-up result。
3. 若作业负荷超过 guardrail，先调整 optional tasks、reading density 或 feedback timing，不降低核心 learning objective。
4. 若 10 周版连续两周超过 overload boundary，改用 12 周 expansion map 或拆分项目里程碑。
5. 每轮开课后把真实 self-report、作业耗时、regrade spike 和 project scope risk 写入 [Course Operations and Improvement Log](course-operations-log.md)。

## Release Checklist

| Check | Passing evidence |
|-------|------------------|
| Weekly budget | Week 1-10 each has lecture, reading, assignment, recitation/project and total target hours |
| Difficulty ladder | D1-D5 map to weeks, cognitive demand and evidence |
| Guardrails | assignment load guardrails include runtime, starter scope, written questions, hidden categories, capstone overlap and reading density |
| Overload actions | overload signals include threshold, evidence source and pacing action |
| Expansion path | 10-to-12 week map covers at least four pressure points |
| Link coverage | syllabus, calendar ledger, assignment handout, reading list, recitation worksheet, learning analytics plan and operations log link this calibration |
| Verification | `.venv/bin/python verify_course.py` reports `PASS workload and pacing calibration ...` |
