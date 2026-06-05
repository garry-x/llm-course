# LLM 深度学习课程 Syllabus

本 syllabus 面向 10-12 周高校课程使用。它把章节、阅读、作业、项目、评分、协作政策、学生支持和验收命令集中到一份可授课文件中；与 CS224N 公开课程结构的对照见 [CS224N Benchmark Crosswalk](cs224n-benchmark-crosswalk.md)，当前公开页复核证据见 [CS224N Current Benchmark Snapshot](cs224n-current-benchmark-snapshot.md)，每次课的目标、推导、demo 和课堂检查点见 [10 周 / 20 讲 Lecture Plan](lecture-plan.md)，每周讲后复盘与下次课调整见 [Weekly Teaching Reflection and Adjustment Log](weekly-teaching-reflection-adjustment-log.md)，workload、难度阶梯和 10/12 周节奏调整见 [Workload and Pacing Calibration](workload-pacing-calibration.md)，lecture、作业、项目、late day 和 regrade window 的 single source of truth 见 [Course Calendar and Deadline Ledger](course-calendar-deadline-ledger.md)，成绩册、LMS、late-day 账本和 regrade workflow 见 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md)，课件组织见 [Lecture Slide Outline](lecture-slide-outline.md)，每讲 notes、板书推导和复盘证据见 [Lecture Notes Index](lecture-notes-index.md)，每讲 notes 的审稿、来源边界和更正流程见 [Lecture Notes Quality and Review Standard](lecture-notes-quality-review.md)，核心术语定义见 [Core Concept Glossary](core-concept-glossary.md)，知识点先修、章节 unlock path 和 spiral review 路径见 [Topic Dependency and Spiral Review Map](topic-dependency-map.md)，统一符号、shape、mask 和 metric 单位见 [Notation and Shape Glossary](notation-shape-glossary.md)，逐章可复算小例子见 [Worked Example Pack](worked-example-pack.md)，可直接用于授课和讨论课的推导脚本见 [Board Derivation and Instructor Notes Pack](board-derivation-pack.md)，课堂演示复现命令见 [Classroom Demo Runbook](demo-runbook.md)，每讲材料发布状态见 [Course Materials Index](course-materials-index.md)，直播、录播、公开历史视频、字幕和文字稿边界见 [Lecture Media Access Policy](lecture-media-access-policy.md)，材料版本、旧版归档和 retired 边界见 [Material Versioning and Archive Policy](material-versioning-archive-policy.md)，公告、讨论区、私密渠道和 Office Hours 边界见 [Course Communication and Announcement Policy](course-communication-policy.md)，学生可见 staff、Office Hours 和联系入口见 [Course Staff and Office Hours Directory](course-staff-office-hours-directory.md)，staff assistance 和 code review 边界见 [Staff Assistance and Code Review Boundary Policy](staff-assistance-code-review-policy.md)，正式选课、Credit / No Credit、旁听、自学者和公开使用边界见 [Enrollment, Audit, and Public Use Policy](enrollment-audit-public-use-policy.md)，学生常见问题见 [Student FAQ and Troubleshooting Guide](student-faq-troubleshooting.md)，测验和阶段 checkpoint 见 [Quiz and Checkpoint Guide](quiz-checkpoint-guide.md)，quiz、midterm checkpoint、final review、makeup 和评估诚信流程见 [Assessment Administration and Exam Integrity Policy](assessment-administration-policy.md)，概念掌握、常见误区和补救路径见 [Concept Mastery and Misconception Map](concept-misconception-map.md)，可发布样卷和期末复习题见 [Midterm and Final Review Pack](midterm-final-review-pack.md)，前沿 seminar 讨论见 [Frontier Seminar Handout](frontier-seminar-handout.md)，安全、伦理与社会影响案例见 [Safety and Societal Impact Casebook](safety-societal-impact-casebook.md)，模型卡、API 文档、leaderboard 和 benchmark 证据卡见 [Model and Benchmark Card Guide](model-benchmark-card-guide.md)，guest lecture、外部 seminar 和替代任务流程见 [Guest Speaker and External Seminar Policy](guest-speaker-seminar-policy.md)，项目团队、导师、外部协作者和贡献声明规则见 [Project Team and Mentor Policy](project-team-mentor-policy.md)，疑似学术诚信、AI 工具披露和相似性检测个案处理见 [Academic Integrity Case Process](academic-integrity-case-process.md)，助教讨论课和 office hours 流程见 [Discussion Section and Office Hours Guide](discussion-office-hours-guide.md)，staff 执行流程见 [Course Staff Runbook](staff-runbook.md)，算力额度、CPU fallback 和成本记录见 [Compute Resource and Cost Guide](compute-resource-guide.md)，学生支持和可及性流程见 [Accessibility and Student Support Guide](accessibility-student-support.md)。

## 课程目标

完成课程后，学生应能：

- 从 tokenizer、embedding、attention、Transformer block 到 GPT model 解释 decoder-only LLM 的完整数据流。
- 用 PyTorch 实现并测试核心模块，而不是只调用现成 API。
- 推导或解释关键公式：BPE merge、RoPE 相对位置、attention scaling、LayerNorm、cross entropy、DPO/GRPO、KV Cache 显存。
- 设计并复现训练工程与推理工程实验，报告 seed、环境、日志、指标和失败案例。
- 区分基础理论、论文结论、模型卡声明、新闻报道和社区传闻。
- 理解经典 NLP 专题：dependency parsing、seq2seq/NMT、BERT/encoder-only、BLEU/ROUGE/F1/EM 和安全/伦理评测。

## 先修要求

最低要求：

- Python 基础：函数、类、列表/字典、文件读写。
- PyTorch 基础：tensor shape、broadcast、`nn.Module`、autograd、optimizer。
- 数学基础：矩阵乘法、向量点积、概率分布、导数和链式法则。

建议课前完成：

- 完成 [Prerequisite Diagnostic](prerequisite-diagnostic.md)，确认 Python、PyTorch、线性代数、概率、反向传播和复现纪律的薄弱项。
- 若 Python 或 PyTorch 诊断为 Borderline，参加 [Python and PyTorch Review Session](python-pytorch-review-session.md)，并提交 shape trace 与第一个失败测试记录。
- 阅读 [数学与 PyTorch 先修复习](math-prerequisites.md)、[ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md) 和 [逐周阅读清单与复盘 Handout](reading-list.md) Week 0。
- 跑通 `.venv/bin/python verify_course.py`。
- 跑通 Ch01 作业测试。

## 评分结构

| 项目 | 权重 | 交付 |
|------|:--:|------|
| 章节编程作业 | 35% | Ch01-Ch10 starter 实现、测试输出、错误分析 |
| 书面推导与概念题 | 20% | 每次作业 2-3 道推导/复杂度/概念题 |
| 训练工程 Capstone | 15% | 数据审计、训练日志、checkpoint/resume、成本估算 |
| 推理工程 Capstone | 20% | API、评测、压测、SLO、容量规划、错误分析 |
| 阅读复盘、课堂参与与反馈 | 10% | 论文摘要、来源审计、paper recap calibration、讨论课/Office Hours 准备、互评反馈、guest lecture reflection、期中/期末反馈 |

作业 handout 摘要见 [Assignment Handout Pack](assignment-handout-pack.md)，书面题来自 [书面推导与概念题题库](written-problem-set.md)，综合复习路径见 [Comprehensive Review Study Guide](comprehensive-review-study-guide.md)，课程目标、评估渠道、认知层级和 evidence gate 的总表见 [Assessment Blueprint and Coverage Matrix](assessment-blueprint-coverage-matrix.md)，课程目标 direct/indirect evidence 与达标阈值汇总见 [Learning Outcome Attainment Report](learning-outcome-attainment-report.md)，阅读复盘按 [逐周阅读清单与复盘 Handout](reading-list.md)、[Reading Discussion Question Bank](reading-discussion-question-bank.md)、[Paper Recap Calibration Pack](paper-recap-calibration-pack.md) 和 [Paper-to-Code Traceability Matrix](paper-to-code-traceability-matrix.md) 评分，课堂参与、讨论区贡献、discussion worksheet、Office Hours 准备、guest lecture reflection 和反馈调查按 [Participation and Feedback Guide](participation-feedback-guide.md)、[Recitation Worksheet Pack](recitation-worksheet-pack.md) 与 [Guest Speaker and External Seminar Policy](guest-speaker-seminar-policy.md) 执行，期中/期末反馈、课堂同行观察和课程评估改进闭环按 [Teaching Observation and Course Evaluation Dossier](teaching-observation-course-evaluation.md) 执行，quiz/checkpoint 的 item bank、item analysis、allowed materials、makeup、便利安排和诚信边界按 [Assessment Item Bank Ledger](assessment-item-bank-ledger.md)、[Assessment Item Analysis and Psychometrics Guide](assessment-item-analysis-psychometrics.md) 与 [Assessment Administration and Exam Integrity Policy](assessment-administration-policy.md) 执行，成绩册字段、权重复算、late-day ledger 和成绩发布按 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md) 执行，评分参考 [Instructor Solution Guide](instructor-solution-guide.md)。编程作业公开测试和隐藏测试按 [Autograder 与隐藏测试设计指南](autograder-hidden-tests.md) 设计，代码质量人工复核按 [Programming Assignment Code Quality Rubric](programming-assignment-code-quality-rubric.md) 执行。项目提案和 milestone 按 [Capstone Proposal and Milestone Guide](capstone-proposal-milestone.md) 管理，默认最终项目按 [Default Final Project Guide](default-final-project-guide.md) 执行，最终报告建议按 [Project Report Template and Reproducibility Checklist](project-report-template.md) 提交，实验 split、metric、uncertainty、claim audit 和 contamination/leakage gate 按 [Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md) 复核，poster session、公开报告归档和展示材料公开边界按 [Final Project Showcase and Archive Policy](final-project-showcase-archive-policy.md) 执行，默认/自定义项目选题、导师匹配和报告归档按 [Capstone Project Gallery and Idea Bank](capstone-project-gallery.md) 执行。项目数据和伦理审查按 [Data and Ethics Review](data-ethics-review.md) 执行，项目报告按 [Capstone 项目报告 Rubric](project-report-rubric.md) 评分，展示和同伴 review 按 [项目展示与同伴 Review Rubric](presentation-peer-review.md) 评分，展示后的项目答辩和个人口头追问按 [Capstone Defense and Oral Exam Question Bank](capstone-defense-oral-exam-bank.md) 抽样记录。

## 周安排

| 周 | 主题 | 阅读 | 作业/交付 |
|----|------|------|-----------|
| 1 | Tokenization 与 Embedding | Ch01-Ch02；[reading-list.md](reading-list.md) Week 1 | A1：BPE + embedding/RoPE；书面题 Ch01-Ch02；阅读复盘 |
| 2 | Attention 与反向传播复习 | Ch03；[reading-list.md](reading-list.md) Week 2；math prerequisites | A2：scaled attention + causal mask；书面题 Ch03 |
| 3 | MHA/GQA/MLA 与 Transformer Block | Ch04-Ch05；[reading-list.md](reading-list.md) Week 3 | A3：MHA/GQA/MLA + block；书面题 Ch04-Ch05 |
| 4 | GPT 组装与 MoE | Ch06；[reading-list.md](reading-list.md) Week 4 | A4：GPTModel + MoE router；书面题 Ch06 |
| 5 | Training Loop | Ch07；[reading-list.md](reading-list.md) Week 5 | A5：dataset/CE/AdamW/scheduler/train；训练项目提案 |
| 6 | Generation 与 Decoding | Ch08；[reading-list.md](reading-list.md) Week 6 | A6：top-k/top-p/speculative decoding；书面题 Ch08 |
| 7 | Fine-tuning 与 Alignment | Ch09；[reading-list.md](reading-list.md) Week 7 | A7：SFT/LoRA/DPO/GRPO；训练 capstone 初版 |
| 8 | 经典 NLP 与评测专题 | [经典 NLP 专题 Handout](classic-nlp-handout.md)；[reading-list.md](reading-list.md) Week 8 | A8：dependency/seq2seq/BERT/evaluation 书面题；同伴 review |
| 9 | Inference Engineering | Ch10；[reading-list.md](reading-list.md) Week 9 | A9：KV cache/RAG/benchmark；推理项目提案 |
| 10 | Capstone 展示与前沿 seminar | 两个 capstone README、rubric；[reading-list.md](reading-list.md) Week 10；[frontier-seminar-handout.md](frontier-seminar-handout.md) | 训练 capstone + 推理 capstone 报告、演示、复现包；前沿开放问题短报告 |

12 周版本建议把第 8 周拆成两周：一周讲 dependency parsing/seq2seq/BERT，一周讲 evaluation/ethics/safety；第 10 周项目展示也可拆成训练项目和推理项目两次。20 讲细化安排见 [lecture-plan.md](lecture-plan.md)。

## 作业节奏

- 作业在对应周第一次课后发布。
- 建议截止时间为下一周第一次课前 24 小时。
- 作业发布、提交包、LMS/Gradescope 配置和复核材料按 [Assignment Submission and Release Guide](assignment-submission-guide.md) 执行；成绩册字段、权重复算和 late-day 账本按 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md) 执行。
- staff 对学生代码、伪代码、项目 artifact 和 regrade 材料的查看边界按 [Staff Assistance and Code Review Boundary Policy](staff-assistance-code-review-policy.md) 执行。
- 每次编程作业必须提交：代码、测试输出、错误分析。
- 公开测试全过不等于满分；正式评分还包含隐藏边界测试、隐藏性质测试和必要的人工复核。
- 每次书面作业必须提交：推导过程、shape、边界条件和必要引用。
- 若使用 AI 工具，报告中必须说明使用环节。
- 阅读复盘按 [逐周阅读清单与复盘 Handout](reading-list.md) 提交，必须包含核心结论、技术细节、代码连接、来源审计和批判性问题。
- 第 8-10 周的同伴 review 必须包含复现尝试、最强证据、最大风险、改进建议和来源检查。

章节作业入口：

- `assignments/ch01_bpe/`
- `assignments/ch02_embeddings/`
- `assignments/ch03_attention/`
- `assignments/ch04_multihead/`
- `assignments/ch05_block/`
- `assignments/ch06_gpt/`
- `assignments/ch07_training/`
- `assignments/ch08_generation/`
- `assignments/ch09_alignment/`
- `assignments/ch10_inference/`
- `assignments/ch11_classic_nlp/`：经典 NLP 与评测补充作业，用于第 8 周 dependency parsing、BLEU/ROUGE、QA EM/F1 和 BERT MLM mask。

## Capstone 里程碑

项目提案、milestone、导师反馈记录和最终提交包格式见 [Capstone Proposal and Milestone Guide](capstone-proposal-milestone.md)。训练/推理项目的 CPU baseline、GPU/API 额度、成本记录和降级路径按 [Compute Resource and Cost Guide](compute-resource-guide.md) 执行。

训练工程 Capstone：

| 时间 | 交付 |
|------|------|
| 第 5 周 | 项目提案：数据、模型规模、训练预算、风险 |
| 第 7 周 | 初版：数据审计、训练日志、checkpoint/resume |
| 第 10 周 | 最终报告：ablation、错误分析、成本估算、复现命令 |

推理工程 Capstone：

| 时间 | 交付 |
|------|------|
| 第 8 周 | 项目提案：API 设计、评测集、SLO、容量目标 |
| 第 9 周 | 初版：OpenAI-compatible API、评测、benchmark、SLO |
| 第 10 周 | 最终报告：P50/P95/P99、TTFT/TPOT、RAG/JSON/tool 回归、成本估算 |

项目展示与同伴 review：

| 时间 | 交付 |
|------|------|
| 第 8 周 | Review 训练 capstone 初版：复现尝试、最强证据、最大风险 |
| 第 9 周 | Review 推理 capstone 初版：SLO、评测集、容量规划风险 |
| 第 10 周 | 最终展示：slides/讲稿、问答、同伴 review 修改说明 |

## 迟交与复核

建议迟交政策：

- 每名学生有 3 个 late days。
- 单次作业最多使用 2 个 late days。
- late days 用完后，每迟交 24 小时扣 10%。
- Capstone 最终展示不接受迟交，除非教师批准特殊情况。

复核政策：

- 复核请求必须在成绩发布后 7 天内提交。
- 请求必须指出具体评分项、提交文件和理由。
- 复核会重新检查相关部分，分数可能上调或下调。
- LMS 中的 regrade request、复核状态、决定 ID 和批量修正按 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md) 留痕。

## 协作与 AI 工具

课程遵循 [课程政策：协作、引用与 AI 工具](course-policies.md)。学术诚信个案、相似性检测和 AI 工具争议处理见 [Academic Integrity Case Process](academic-integrity-case-process.md)。

简要规则：

- 可以讨论思路、论文、debug 假设和测试失败原因。
- 最终代码、推导和报告必须独立完成。
- 禁止复制他人提交、共享隐藏测试或伪造日志。
- AI 工具可以辅助学习和调试，但学生必须能解释提交内容，并在报告中披露使用环节。

## 学生支持与可及性

课程遵循 [Accessibility and Student Support Guide](accessibility-student-support.md)。教师应在开课第一周说明公开讨论区、私密消息、课程邮箱和 Office Hours 的使用边界。

基本原则：

- 学生如有正式学术便利安排，应尽早通过私密渠道联系教师或课程组。
- 课程团队可调整提交时间、展示形式、材料格式或辅助技术使用方式，但不降低核心学习目标。
- 不要求学生在公开讨论区披露健康、身份或个人困难。
- 涉及紧急健康或安全问题时，学生应联系学校正式支持渠道；课程组按本校政策协助处理。

## 引用与来源

所有论文、官方文档、模型卡、博客和第三方库都需要引用。外部来源先按 [External Source Inventory](external-source-inventory.md) 区分稳定论文、前沿模型、框架文档、背景学习资源和 runtime asset；前沿模型事实必须遵循 [前沿模型来源等级与复核记录](frontier-source-audit.md)。

最低引用格式：

- 作者或机构。
- 标题。
- 链接。
- 访问日期。
- 使用位置。

## 课程验收命令

基础门禁：

```bash
.venv/bin/python verify_course.py
.venv/bin/python run_assignment_tests.py
```

发布或期末门禁：

```bash
.venv/bin/python verify_course.py --capstone --training
```

教师在发布课程、更新章节、更新模型规格或调整作业后，应运行上述命令，并浏览相关章节确认公式、链接和图表正常。
