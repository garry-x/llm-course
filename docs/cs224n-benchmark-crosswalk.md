# CS224N Benchmark Crosswalk

本文件把本课程与 Stanford CS224N 公开课程结构逐项对照。它不是复制 CS224N 的作业或讲义，而是用公开结构作为高校课程完整性的审计基准：先修、阅读、作业、项目、参与、政策、office hours、schedule 和持续更新机制都必须有本课程内证据。当前公开页的具体复核结果见 [CS224N Current Benchmark Snapshot](cs224n-current-benchmark-snapshot.md)。

复核日期：2026-06-05
基准来源：https://web.stanford.edu/class/cs224n/

## 当前公开页复核摘要

| 项目 | 复核结果 |
|------|----------|
| 复核日期 | 2026-06-05 |
| 公开版本 | Stanford / Winter 2026 |
| 评分结构 | Assignments 48%、Final Project 49%、Participation 3% |
| 作业结构 | 四个 weekly assignments，均含 written questions 和 programming parts |
| Final Project | proposal 8%、milestone 6%、poster 3%、report 32%；default GPT-2 或 custom project |
| 课程政策 | 公开页包含 late days、regrade、honor code、AI tools policy、accessibility、well-being 和支持渠道 |
| 本课程动作 | 已将具体差异和维护要求记录到 [CS224N Current Benchmark Snapshot](cs224n-current-benchmark-snapshot.md) |

## 对标范围

| CS224N 公开结构 | 本课程对应证据 | 当前状态 | 后续维护 |
|-----------------|----------------|----------|----------|
| Course homepage and logistics | `README.md`、[课程 Syllabus](syllabus.md)、[Course Materials Index](course-materials-index.md)、[Course Staff and Office Hours Directory](course-staff-office-hours-directory.md) | 已有课程入口、验收命令、材料索引、发布规则、staff 角色、office hours 和联系渠道 | 每轮开课填入真实时间、地点、LMS/讨论区链接和 staff directory |
| Prerequisites | [Prerequisite Diagnostic](prerequisite-diagnostic.md)、[Python and PyTorch Review Session](python-pytorch-review-session.md)、[数学与 PyTorch 先修复习](math-prerequisites.md)、[ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md) | 已覆盖 Python、NumPy/PyTorch、college calculus、linear algebra、probability/statistics、ML foundations、反向传播、复现纪律和 Week 1/2 review session | 根据学生诊断结果调整补救材料、ML foundations bridge 和 review session drill |
| Python/PyTorch review sessions | [Python and PyTorch Review Session](python-pytorch-review-session.md)、[Environment and Reproducibility Guide](environment-reproducibility.md) | 已覆盖环境 smoke test、Ch01 helper、Ch02 embedding/RoPE、CE loss、autograd 和 debug drill | 根据 Week 1/2 真实失败模式更新 review handout 和 FAQ |
| Reference texts and readings | [逐周阅读清单与复盘 Handout](reading-list.md)、[Chapter Source and Accuracy Map](chapter-source-map.md) | 已按 Week 1-10 给出必读/选读、来源等级和复盘题 | 开课前复核论文版本、教材版本和外链 |
| Schedule and lecture slides / notes | [10 周 / 20 讲 Lecture Plan](lecture-plan.md)、[Lecture Slide Outline](lecture-slide-outline.md)、[Lecture Notes Index](lecture-notes-index.md)、[Lecture Notes Quality and Review Standard](lecture-notes-quality-review.md)、[课程 Syllabus](syllabus.md) | 已把 10 周课程拆成 20 讲，含目标、推导、demo、quick check、slide deck 大纲、notes 索引、review record 和 correction workflow | 用真实校历替换周次；正式 PDF/录屏发布后更新 materials index，并按 notes quality review 复核 |
| Current schedule topic evidence | [CS224N Current Benchmark Snapshot](cs224n-current-benchmark-snapshot.md)、[Frontier Seminar Handout](frontier-seminar-handout.md)、[逐周阅读清单与复盘 Handout](reading-list.md) | 已把 Winter 2026 公开 schedule 中的 Python/PyTorch/Hugging Face tutorial、Benchmarking and Evaluation、Reasoning、Tokenization and Multilinguality、Interpretability、Social and Broader Impacts、Multimodality、Tinker and LoRA、Open Questions、assignment/project events 映射到本课程材料 | 每轮开课前重新访问官方 schedule；若新增或删除主题，更新 snapshot、reading-list、frontier seminar 和 lecture plan |
| Current page refresh script | [External Source Verification Guide](external-source-verification.md)、`scripts/verify_cs224n_snapshot.py` | 已提供可执行脚本检查官方页是否仍包含对标 marker，并输出可归档 JSON manifest | 每轮开课前运行脚本；若 marker 缺失，先人工复核官方页面变化，再更新 snapshot/crosswalk/seminar |
| Course calendar and deadlines | [Course Calendar and Deadline Ledger](course-calendar-deadline-ledger.md)、[Course Communication and Announcement Policy](course-communication-policy.md)、[Gradebook and LMS Operations Guide](gradebook-lms-operations.md) | 已把 lecture schedule、assignment release/due、project proposal/milestone/report、late day、regrade window、gradebook schema、late-day ledger 和改期公告集中为 single source of truth | 开课前用真实校历、LMS/Gradescope 链接、学校时区、gradebook export 和 regrade workflow 替换 week-relative 时间 |
| Quiz / checkpoint administration | [Quiz and Checkpoint Guide](quiz-checkpoint-guide.md)、[Midterm and Final Review Pack](midterm-final-review-pack.md)、[Assessment Administration and Exam Integrity Policy](assessment-administration-policy.md) | 已覆盖 quick check、recap quiz、midterm checkpoint、final review、allowed materials、makeup assessment、item security、accommodation、integrity flow 和 feedback release | 若正式计分，开课前确认 assessment_id、窗口、权重、allowed materials、makeup 和 regrade window |
| Lecture videos and media access | [Lecture Media Access Policy](lecture-media-access-policy.md)、[Course Materials Index](course-materials-index.md)、[Accessibility and Student Support Guide](accessibility-student-support.md) | 已区分 live stream、current lecture recording、public historical video、caption / transcript、隐私剪辑和 public learner 边界 | 若加入真实录播平台，开课前填入平台、访问对象、字幕/文字稿和剪辑流程 |
| Assignments with written and programming parts | `assignments/ch01_bpe/` 到 `assignments/ch11_classic_nlp/`、[Assignment Handout Pack](assignment-handout-pack.md)、[书面推导与概念题题库](written-problem-set.md) | 已有 11 个可运行测试套件、作业 handout 摘要和书面题库 | 正式开课时配置 LMS/Gradescope 和隐藏测试 |
| Staff assistance and code review boundaries | [Staff Assistance and Code Review Boundary Policy](staff-assistance-code-review-policy.md)、[Course Staff and Office Hours Directory](course-staff-office-hours-directory.md)、[Discussion Section and Office Hours Guide](discussion-office-hours-guide.md) | 已区分 Ch01-Ch02 limited_code_view、Ch03-Ch11 pseudocode_review、final project artifact_review、rubric_explanation、public/private channel 和 fairness_followup | 每轮开课前按当轮作业难度、honor code 和 staff capacity 调整 assistance matrix |
| Final project with proposal, milestone, poster/report | [Capstone Proposal and Milestone Guide](capstone-proposal-milestone.md)、[Default Final Project Guide](default-final-project-guide.md)、[Compute Resource and Cost Guide](compute-resource-guide.md)、[Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md)、[Capstone 项目报告 Rubric](project-report-rubric.md)、[项目展示与同伴 Review Rubric](presentation-peer-review.md)、[Final Project Showcase and Archive Policy](final-project-showcase-archive-policy.md) | 已有训练/推理两个 capstone、默认 GPT-2 风格最终项目任务包、自定义项目边界、资源预算、CPU fallback、展示互评、实验统计审计、报告 rubric 和公开归档边界；proposal/milestone/final report 都必须逐步收敛 split_card、metric_card、uncertainty_record、claim_audit、bootstrap CI / seed sensitivity / single_seed_limit 和 contamination/leakage gate | 课程运行后按 consent/redaction 规则归档脱敏优秀项目，并抽查统计结论与 claim 强度是否匹配 |
| Default project and custom project options | [Default Final Project Guide](default-final-project-guide.md)、[Capstone Project Gallery and Idea Bank](capstone-project-gallery.md) | 已定义默认三任务包、训练/推理项目、自定义项目类型、导师匹配和贡献声明 | 根据 staff 专长更新项目池 |
| Computing resources for projects | [Compute Resource and Cost Guide](compute-resource-guide.md)、两个 capstone README | 已定义 CPU baseline、GPU/API 可选扩展、额度公平使用、成本记录、失败重跑和降级路径 | 若课程提供真实云额度或共享 GPU，需在开课前填入平台、额度和申请流程 |
| Participation credit | [Participation and Feedback Guide](participation-feedback-guide.md)、[Guest Speaker and External Seminar Policy](guest-speaker-seminar-policy.md) | 已覆盖讨论区贡献、Office Hours 准备、反馈调查、guest lecture reflection、外部 seminar、替代任务、Q&A/source audit 和 karma-style 课程贡献 | 根据真实参与数据调整评分阈值 |
| Office hours and discussion forum | [Course Staff and Office Hours Directory](course-staff-office-hours-directory.md)、[Discussion Section and Office Hours Guide](discussion-office-hours-guide.md)、[Course Staff Runbook](staff-runbook.md) | 已有学生可见 staff 角色、联系渠道、Office Hours 类型、queue policy、escalation matrix、讨论课 drill、office-hour triage 和排班规则 | 每周把真实问题写入 operations log |
| Late days and regrade requests | [课程 Syllabus](syllabus.md)、[课程政策](course-policies.md)、[Grading Calibration Guide](grading-calibration.md)、[Gradebook and LMS Operations Guide](gradebook-lms-operations.md) | 已定义迟交、复核、协作、AI 工具、评分校准、gradebook column、late-day ledger、release batch、regrade decision 和争议处理 | 按学校政策替换 late-day 数量、复核窗口、LMS 字段和成绩册导出流程 |
| Honor code and AI policy | [课程政策](course-policies.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md)、[Academic Integrity Case Process](academic-integrity-case-process.md) | 已区分允许协作、禁止行为、AI 使用披露、相似性检测解释、个案取证和隐私沟通 | 每轮开课前与学校正式政策对齐 |
| Accessibility and student support | [Accessibility and Student Support Guide](accessibility-student-support.md) | 已覆盖学术便利安排、材料可访问性、隐私边界和支持渠道 | 填入本校正式联系人和处理时限 |
| Course updates and archived evidence | [Course Operations and Improvement Log](course-operations-log.md)、[External Source Verification Guide](external-source-verification.md) | 已有运行记录、来源复核、改进任务和前沿内容更新流程 | 每次改版记录日期、证据和处理动作 |

## 内容覆盖对照

| CS224N 风格主题 | 本课程覆盖位置 | 证据类型 |
|-----------------|----------------|----------|
| Word vectors and representation learning | Ch02、`assignments/ch02_embeddings/`、[reading-list.md](reading-list.md) Week 1 | 章节、代码测试、书面题、阅读复盘 |
| Neural network foundations and tensor derivatives | Ch03-Ch05、[math-prerequisites.md](math-prerequisites.md)、[written-problem-set.md](written-problem-set.md) | 公式推导、shape 检查、gradcheck、书面题 |
| Dependency parsing | [经典 NLP 专题 Handout](classic-nlp-handout.md)、`assignments/ch11_classic_nlp/` | 专题讲义、UAS/LAS 测试、书面题 |
| Self-attention and Transformers | Ch03-Ch06、`assignments/ch03_attention/` 到 `assignments/ch06_gpt/` | 章节、PyTorch 实现、测试、复杂度分析 |
| LLM benchmarking and evaluation | Ch08-Ch10、[经典 NLP 与评测覆盖说明](nlp-evaluation-coverage.md)、[Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md)、推理 capstone | BLEU/ROUGE/EM/F1、RAG 评测、benchmark、SLO、bootstrap confidence interval、seed sensitivity、significance claim gate 和 contamination/leakage gate |
| Large language model training and alignment | Ch07-Ch09、训练 capstone、`assignments/ch07_training/` 到 `assignments/ch09_alignment/` | dataset、CE/AdamW/scheduler、SFT、LoRA、DPO、GRPO |
| Interpretability, multimodality, social impact, open questions | [Frontier Seminar Handout](frontier-seminar-handout.md)、Ch03、Ch05、Ch10、[Data and Ethics Review](data-ethics-review.md) | seminar 短报告、反事实解释实验、多模态失败案例、风险登记、开放问题实验设计 |
| Ethics, citation, and project responsibility | [Data and Ethics Review](data-ethics-review.md)、[课程政策](course-policies.md) | 项目审查表、引用规则、风险说明 |

## 权重对照

CS224N 公开页面把课程成绩主要放在 assignments、final project 和 participation 上。本课程采用相同的大类，但按 LLM 工程课程目标拆分为：

| 类别 | 本课程权重 | 对标说明 |
|------|------------|----------|
| 编程作业 | 35% | 对应 CS224N assignments 的编程部分，强调核心模块从零实现和测试 |
| 书面推导与概念题 | 20% | 对应 assignments 的 written questions，强化 shape、复杂度和数学推导 |
| 训练工程 Capstone | 15% | 对应 final project 的模型训练、复现和报告能力 |
| 推理工程 Capstone | 20% | 对应 final project 的评测、系统指标和服务化能力 |
| 阅读复盘、课堂参与与反馈 | 10% | 对应 participation、guest lecture、feedback survey、discussion / Ed participation 和 karma-style 课程贡献 |

## 仍需人工确认的项目

| 项目 | 为什么不能完全自动验收 | 需要的人工证据 |
|------|------------------------|----------------|
| 正式 LMS / Gradescope 配置 | 仓库只能提供发布包和测试策略，不能证明真实平台配置 | 截图、配置导出、隐藏测试运行记录 |
| 课堂讲授质量 | 讲义和 lecture plan 不能证明教师讲授效果 | 课堂观察、学生反馈、exit ticket 聚合 |
| 项目报告深度 | 自动验收只能证明最小可运行，不等于优秀研究/工程报告 | 评分样例、助教校准记录、复现审查 |
| 课程政策合规性 | 不同学校政策不同 | 教师按本校 honor code、可及性和隐私政策签核 |

## 发布前 Checklist

- README、syllabus 和 quality audit 均链接本 crosswalk。
- `verify_course.py` 通过，并检查本文件关键标记。
- CS224N 基准页或目标高校课程页在开课前重新访问，记录日期。
- 若目标高校课程结构变化，更新“对标范围”和“权重对照”。
- 若本课程新增 slides、notebook、录屏或 LMS 页面，同步更新 materials index 和 operations log。
