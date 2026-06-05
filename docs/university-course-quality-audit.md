# 高校课程质量审计与升级路线

本文档把本课程从"自学教程"升级到"可授课、可评分、可复现"的高校课程规格。参考对象包括 Stanford CS224N 这类课程的公开结构：明确先修要求、讲义/阅读材料、理论+编程作业、项目里程碑、评分权重、协作与引用政策。逐项对照见 [CS224N Benchmark Crosswalk](cs224n-benchmark-crosswalk.md)，当前公开页复核见 [CS224N Current Benchmark Snapshot](cs224n-current-benchmark-snapshot.md)。

## 目标标准

高校课程水平不只意味着内容多，还意味着每个知识点能被教学、练习、评估和复现。课程需要同时满足以下要求：

| 维度 | 合格标准 | 当前证据 | 差距 |
|------|----------|----------|------|
| 高校课程对标 | 与 CS224N 类课程的公开结构有逐项 crosswalk，能说明本课程在 logistics、先修、阅读、作业、项目、参与、政策、支持和更新机制上的证据 | 已新增 [CS224N Benchmark Crosswalk](cs224n-benchmark-crosswalk.md) 和 [CS224N Current Benchmark Snapshot](cs224n-current-benchmark-snapshot.md)，按 CS224N Winter 2026 公开结构列出本课程对应材料、具体权重差异和人工证据边界 | 每轮开课前需要重新访问目标高校课程页并记录复核日期 |
| 内容覆盖 | 覆盖神经 NLP/LLM 的核心路径：表示学习、神经网络基础、注意力、Transformer、预训练、微调、评测、RAG/Agent、推理系统 | 10 章覆盖 BPE、Embedding、Attention、Transformer Block、GPT、训练、生成、对齐、推理优化；另有 [经典 NLP 专题 Handout](classic-nlp-handout.md)、[Classic NLP Deep-Dive Teaching Module](classic-nlp-deep-dive-module.md)、[经典 NLP 与评测覆盖说明](nlp-evaluation-coverage.md) 和 `assignments/ch11_classic_nlp/` 补充作业 | BERT/encoder-only、seq2seq/NMT、dependency parsing 已可拆成 2-4 讲专题模块；若课程扩展为完整 NLP 课，仍可继续新增独立 HTML 正文章节 |
| 先修诊断 | 学生能在开课前评估 Python、PyTorch、数学、反向传播和复现纪律准备度 | 已新增 [Prerequisite Diagnostic](prerequisite-diagnostic.md)，包含分级标准、诊断题、补救任务和教师使用建议 | 课程运行后可按真实学生薄弱点调整题库 |
| 阶段性测验 | quick check、recap quiz、midterm checkpoint、final review 和 capstone readiness 有题型、通过阈值、补救路径、样卷和轮换记录 | 已新增 [Quiz and Checkpoint Guide](quiz-checkpoint-guide.md) 与 [Midterm and Final Review Pack](midterm-final-review-pack.md)，并接入 syllabus 与 operations log | 课程运行后按真实通过率调整题库 |
| 概念定义一致性 | 高频术语有课程内定义、误讲边界、证据锚点和来源边界 | 已新增 [Core Concept Glossary](core-concept-glossary.md)，覆盖 tokenization、embedding、RoPE、attention、GQA/MLA、normalization、MoE、training/alignment、RAG、serving SLO、evaluation metric 和 source boundary | 课程运行后按真实误区继续扩充定义 |
| 知识依赖路径 | 核心概念有先修关系、章节 unlock path、spiral review 和失败信号到补救材料的映射 | 已新增 [Topic Dependency and Spiral Review Map](topic-dependency-map.md)，覆盖 prerequisite、tokenization、attention、Transformer block、LM/training、generation/alignment、evaluation/serving 和 capstone evidence 层级 | 课程运行后按真实 quiz、worksheet、office hours 和项目 milestone 失败模式调整 review 节奏 |
| 数学严谨性 | 关键算法有公式、形状、复杂度和边界条件 | 多数章节已有 KaTeX、shape、复杂度分析；已新增 [数学与 PyTorch 先修复习](math-prerequisites.md)、[Notation and Shape Glossary](notation-shape-glossary.md)、[书面推导与概念题题库](written-problem-set.md)、[Board Derivation and Instructor Notes Pack](board-derivation-pack.md) 和 [Instructor Solution Guide](instructor-solution-guide.md) | 可继续开发隐藏评分样例 |
| 可复算例子 | 每章核心概念有小规模 worked example，把公式、shape、代码、常见错误和评估证据连接起来 | 已新增 [Worked Example Pack](worked-example-pack.md)，覆盖 Ch01-Ch11 的 BPE、RoPE、attention、GQA、Norm、GPT 参数、AdamW、top-p、DPO、KV cache 和经典 NLP metric 例子 | 课程运行后可按真实错题增加更多变体 |
| 编程实践 | 作业能从零实现核心模块，并包含测试/验收、发布、提交、代码质量和复核流程 | 53 道编程练习、两个 capstone、`verify_course.py`；Ch01-Ch10 已有自动测试入口和评分 Rubric；已新增 [Assignment Handout Pack](assignment-handout-pack.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md)、[Programming Assignment Code Quality Rubric](programming-assignment-code-quality-rubric.md) 与 [Autograder 与隐藏测试设计指南](autograder-hidden-tests.md) | 可继续把指南落实成真实私有 autograder 环境 |
| 阅读体系 | 每周/每章有必读、选读、原论文和综述 | README 与章节底部已有延伸阅读；10 章顶部已加入学习目标、课前阅读、课后阅读；已新增 [逐周阅读清单与复盘 Handout](reading-list.md) | 可继续按真实开课年份更新阅读版本和课堂讨论题 |
| 评估机制 | 有作业权重、项目里程碑、评分 rubrics | README 与 [课程 Syllabus](syllabus.md) 已加入评分方案、作业节奏和 capstone 里程碑；作业、两个 capstone、项目提案/milestone、项目展示和同伴 review 均有 rubric | 可继续按真实班级校历填写具体日期 |
| 参与与反馈 | 课堂参与、讨论区贡献、Office Hours 准备、同伴 review 和期中/期末反馈有评分与改进流程 | 已新增 [Participation and Feedback Guide](participation-feedback-guide.md)，并接入 syllabus、staff runbook 和 operations log | 课程运行后用真实问卷结果调整节奏和材料 |
| 学生 FAQ | 学生能自助排查环境、作业测试、shape/mask、capstone、评分复核和支持渠道问题 | 已新增 [Student FAQ and Troubleshooting Guide](student-faq-troubleshooting.md)，并接入 syllabus、staff runbook 和 operations log | 课程运行后按真实高频问题持续更新 |
| 项目生态 | 最终项目有默认项目、自定义项目边界、选题库、导师匹配、贡献声明、报告样例、答辩追问和报告归档口径 | 已新增 [Default Final Project Guide](default-final-project-guide.md)、[Capstone Project Gallery and Idea Bank](capstone-project-gallery.md)、[Project Report Exemplar Pack](project-report-exemplar-pack.md) 和 [Capstone Defense and Oral Exam Question Bank](capstone-defense-oral-exam-bank.md)，并接入 syllabus、proposal guide、报告 rubric 和 showcase/archive policy | 课程运行后可用 consent/redaction 流程把 synthetic 样例替换或补充为真实脱敏优秀项目 |
| 算力与成本 | 项目有 CPU baseline、GPU/API 额度规则、成本记录、失败重跑和降级路径 | 已新增 [Compute Resource and Cost Guide](compute-resource-guide.md)，并接入 syllabus、capstone proposal、staff runbook 和 operations log | 若课程提供真实云额度或共享 GPU，应填入平台和配额 |
| 学习目标证据 | 每个课程目标能映射到教学材料、学生交付、自动证据和人工评分证据 | 已新增 [Course Outcome Map](course-outcome-map.md)，覆盖 6 个 syllabus outcome、自动门禁覆盖矩阵和人工审查清单 | 课程运行后继续补真实学生样例和隐藏测试统计 |
| 评分一致性 | 助教批改有校准流程、双评规则、满分/部分分/不通过样例和复核口径 | 已新增 [Grading Calibration Guide](grading-calibration.md)，覆盖书面题、代码作业、capstone、阅读复盘和同伴 review | 课程运行后继续加入真实争议样例 |
| 授课执行 | 每周主题能展开到单次课堂目标、推导、demo、讨论课、答疑和课堂检查 | 已新增 [10 周 / 20 讲 Lecture Plan](lecture-plan.md)、[Classroom Demo Runbook](demo-runbook.md)、[Discussion Section and Office Hours Guide](discussion-office-hours-guide.md) 与 [Weekly Teaching Reflection and Adjustment Log](weekly-teaching-reflection-adjustment-log.md)，覆盖每讲目标、核心推导、课堂 demo、quick check、讨论课 drill、demo dry run、office-hour triage 和讲后下次课调整 | 教师可按班级节奏替换具体日期和课堂活动 |
| 材料发布 | 每讲章节、阅读、lecture notes、demo、作业证据、slide outline 和发布状态有统一索引 | 已新增 [Course Materials Index](course-materials-index.md)、[Lecture Slide Outline](lecture-slide-outline.md)、[Lecture Notes Index](lecture-notes-index.md) 与 [Board Derivation and Instructor Notes Pack](board-derivation-pack.md)，覆盖 20 讲材料映射、notes、板书推导、demo 规则、slides/notes/recording 规则、课件大纲和版本记录 | 若后续加入正式 PDF slides、notebook 或录屏，应持续更新发布状态 |
| Staff 执行 | 教师、课程经理和助教有职责分工、开课清单、权限配置、公告模板、排班、事故升级和交接模板 | 已新增 [Course Staff Runbook](staff-runbook.md)，覆盖真实开课执行流程 | 每轮开课前填入真实 staff、工具和排班 |
| 学术规范 | 明确协作、引用、AI 工具、复现要求 | 已新增 [课程 Syllabus](syllabus.md) 和 [课程政策：协作、引用与 AI 工具](course-policies.md) | 教师可按学校规则微调迟交和复核流程 |
| 学生支持与可及性 | 课程明确学术便利安排、支持渠道、隐私边界、材料可访问性和公平评分边界 | 已新增 [Accessibility and Student Support Guide](accessibility-student-support.md)，并接入 syllabus 与课程政策 | 教师按本校正式流程填入联系人和处理时限 |
| 数据与伦理 | 项目有数据来源、许可证、隐私、偏见、污染、安全边界和残余风险审查 | 已新增 [Data and Ethics Review](data-ethics-review.md)，并接入 capstone 提案和项目报告 rubric | 课程运行后继续加入真实项目审查样例 |
| 运行改进 | 课程运行后能把隐藏测试统计、答疑记录、复核争议、项目复现和来源更新转化为改进任务 | 已新增 [Course Operations and Improvement Log](course-operations-log.md) 与 [Weekly Teaching Reflection and Adjustment Log](weekly-teaching-reflection-adjustment-log.md)，覆盖每周运行、讲后复盘、作业复盘、隐藏测试、Office Hours、项目复现、复核和来源更新；开课前证据包见 [Pre-Semester Readiness Audit](presemester-readiness-audit.md) | 每轮开课后按真实证据更新任务看板 |
| 准确性维护 | 对基础理论和前沿模型信息标注来源、日期、验证证据和不确定性 | 已新增 [Chapter Source and Accuracy Map](chapter-source-map.md)、[Claim Audit Worksheet](claim-audit-worksheet.md)、[External Source Inventory](external-source-inventory.md)、[External Source Verification Guide](external-source-verification.md)、[Model and Benchmark Card Guide](model-benchmark-card-guide.md)、[External Expert Review Dossier](external-expert-review-dossier.md) 与 [前沿模型来源等级与复核记录](frontier-source-audit.md)，并将未逐条复核的 V4/Engram 数字降级或移除 | 仍需定期复核快速变化的模型卡、API 价格和 benchmark |

## 建议评分方案

如果将本课程作为 10-12 周高校课程使用，建议按以下权重评分：

| 项目 | 权重 | 证据 |
|------|------|------|
| 章节编程作业 | 35% | 每章提交核心代码、单元测试输出、简短错误分析 |
| 书面推导与概念题 | 20% | 公式推导、复杂度分析、选择题解释 |
| 训练工程 Capstone | 15% | 数据审计、训练日志、checkpoint/resume、成本估算 |
| 推理工程 Capstone | 20% | OpenAI-compatible API、压测、评测、SLO 报告 |
| 阅读复盘与课堂参与 | 10% | 论文摘要、复现实验记录、同伴 review |

## 最终验收 Rubric

要把课程判定为“可授课、可评分、可复现”，不能只看章节数量。最终验收按以下 rubric 执行：

| 维度 | 通过标准 | 自动证据 | 人工证据 |
|------|----------|----------|----------|
| 章节脚手架 | 10 章均包含学习目标、课前阅读、课后阅读、评估证据 | `verify_course.py` 检查章节标记 | 教师抽查目标是否可测 |
| CS224N 对标 | 课程有逐项 crosswalk 和当前公开页快照，覆盖 course logistics、prerequisites、reference texts、schedule、assignments、final project、participation、office hours、late/regrade、honor code、accessibility 和 course updates | `docs/cs224n-benchmark-crosswalk.md`、`docs/cs224n-current-benchmark-snapshot.md` | 教师每轮开课前按目标高校课程页更新复核日期 |
| 编程作业 | Ch01-Ch10 与经典 NLP 补充作业均有 README、starter、reference、tests | `run_assignment_tests.py` 必须报告 11 个 suite 全通过 | 隐藏用例覆盖边界条件 |
| 作业发布 | 作业有 handout 摘要、发布前 checklist、学生提交包、LMS/Gradescope 配置、成绩发布说明和复核材料规范 | `docs/assignment-handout-pack.md`、`docs/assignment-submission-guide.md` | 助教按 LMS 实际配置留存运行记录 |
| 隐藏评分 | 作业有公开测试、隐藏边界测试、隐藏性质测试、人工复核和失败日志规范 | `docs/autograder-hidden-tests.md` | 教师/助教在 LMS 或 Gradescope 中实现私有用例 |
| 数学与形状 | 核心公式配有 shape、mask、复杂度或边界说明 | KaTeX/HTML 静态扫描无格式错误 | 助教抽查推导题和代码一致性 |
| 复现能力 | 两个 Capstone 可编译，有验收入口和固定样例 | `verify_course.py --capstone --training` | 学生报告含 seed、日志、失败分析 |
| 工程质量 | 推理、训练、RAG、评测、SLO 有最小可运行实现 | capstone acceptance 与作业测试 | 项目报告按 latency/cost/quality/safety 评分 |
| 学术规范 | 阅读、引用、协作和 AI 工具使用有明确要求 | README/audit 文档存在相关条款 | 课程政策由教师在 syllabus 中确认 |
| 学生支持 | 课程有学术便利安排、支持渠道、隐私边界、可访问材料要求和公平评分边界 | `docs/accessibility-student-support.md` | 教师按学校正式流程替换联系人和紧急支持路径 |
| 先修诊断 | 课程有 placement/diagnostic、分级阈值、补救任务和教师干预建议 | `docs/prerequisite-diagnostic.md` | 教师按班级背景调整阈值 |
| 阶段检查 | 课程有 quick check、recap quiz、midterm checkpoint、final review、补救路径、诚信边界、样卷和题目轮换记录 | `docs/quiz-checkpoint-guide.md`、`docs/midterm-final-review-pack.md` | 教师按通过率调整 recap 和题库 |
| Syllabus | 课程目标、先修、周安排、作业节奏、里程碑、迟交和复核集中成正式授课文件 | `docs/syllabus.md` | 教师按校历填入具体日期和课堂地点 |
| Outcome Map | 每个课程目标有教学材料、学生交付、自动证据、人工评分证据和最低通过标准 | `docs/course-outcome-map.md` | 课程运行后用学生样例校准标准 |
| Lecture Plan | 10 周课程展开为 20 讲，且每讲有目标、核心推导、demo、quick check 和课后证据 | `docs/lecture-plan.md` | 教师按课堂反馈调整时间分配和例题 |
| Demo Runbook | 20 讲课堂 demo 有命令、预期输出、常见失败和备用方案 | `docs/demo-runbook.md` | 教师每轮开课前完成 dry run 并记录失败项 |
| Materials Index / Slides / Notes | 每讲有章节/讲义、阅读、lecture notes、板书推导、demo、作业证据、slide outline、发布状态和版本记录 | `docs/course-materials-index.md`、`docs/lecture-slide-outline.md`、`docs/lecture-notes-index.md` 与 `docs/board-derivation-pack.md` | 课程经理每次发布正式 slides、notes、notebook 或录屏后更新 |
| Discussion / Office Hours | 每周有可执行的 shape drill、failure drill、paper-to-code drill、office-hour triage 和 exit ticket 汇总 | `docs/discussion-office-hours-guide.md` | 助教按真实答疑记录更新高频问题 |
| Student FAQ | 学生有集中 FAQ 与 troubleshooting，覆盖环境、测试、PyTorch shape/mask、capstone、评分复核和提问模板 | `docs/student-faq-troubleshooting.md` | 课程团队按 Office Hours 和复核记录持续更新 |
| Staff Runbook | 课程团队有角色职责、开课前 checklist、权限配置、公告模板、每周会议、评分交接、事故升级和期末交接 | `docs/staff-runbook.md` | 课程经理每轮开课前更新真实排班和工具权限 |
| 参与反馈 | 课程有参与评分 rubric、讨论区规则、期中/期末反馈调查、嘉宾讲座替代任务和聚合记录流程 | `docs/participation-feedback-guide.md` | 教师每轮开课后把反馈动作写入 operations log |
| 课程覆盖透明度 | 明确 LLM 主线与经典 NLP 专题之间的边界 | `docs/nlp-evaluation-coverage.md` | 教师决定是否把专题扩成独立讲次 |
| 前沿专题讨论 | CS224N 风格后半段 seminar 主题有可布置、可评分、可连接项目的材料 | `docs/frontier-seminar-handout.md` 覆盖 interpretability、多模态、社会影响和开放问题 | 教师可按当年 guest lecture 或项目方向替换阅读 |
| 书面评估 | 每章有可评分推导题、复杂度题、概念题和经典 NLP 专题题 | `docs/written-problem-set.md` 与 `docs/instructor-solution-guide.md` | 教师/助教选择正式题和隐藏题 |
| 评分校准 | 批改前有样例校准、双评一致性规则和复核处理流程 | `docs/grading-calibration.md` | 教师定期审查分差和争议样例 |
| 阅读评估 | 每周阅读材料有必读/选读、复盘问题、来源等级和提交模板 | `docs/reading-list.md` | 教师抽查复盘是否连接到代码、实验和来源边界 |
| 来源映射 | 每章核心结论能追溯到论文、教材、课程官网或官方文档，并有课程内验证证据；高风险 claim 有逐条 audit 表 | `docs/chapter-source-map.md`、`docs/claim-audit-worksheet.md` | 教师在改版时抽查正文与来源是否一致 |
| 外部来源清单 | 外部来源按稳定论文、前沿模型、框架文档、背景学习资源和 runtime asset 分层 | `docs/external-source-inventory.md` | 教师每轮开课前抽查高风险来源是否仍可访问 |
| 外部来源复核 | 外部论文、课程官网、模型卡、API 文档、benchmark 和价格有复核频率、记录字段、失效处理和发布前 checklist | `docs/external-source-verification.md` | 教师每轮开课前抽查易变来源 |
| 独立专家复核 | 课程内容、数学推导、来源、作业、评估、项目、可及性和发布安全有独立审阅范围、严重度和闭环记录 | `docs/external-expert-review-dossier.md` | 教师每轮开课前抽查 S0/S1 是否关闭 |
| 项目报告 | Capstone 不只跑通，还能按报告质量评分；默认最终项目需覆盖 GPT-2 风格实现与下游任务证据 | `docs/default-final-project-guide.md`、`docs/project-report-rubric.md` 和 capstone README | 助教检查 ablation、错误分析和引用 |
| 项目过程 | Capstone 有提案、milestone、导师反馈记录和最终提交包检查 | `docs/capstone-proposal-milestone.md` | 教师/助教在第 5/7/9 周给出项目风险反馈 |
| 项目选题与归档 | Capstone 有默认项目、自定义项目边界、选题库、导师匹配、贡献声明和报告归档规则 | `docs/capstone-project-gallery.md` | 教师每轮开课后归档脱敏优秀报告 |
| 算力与成本 | Capstone 有 CPU baseline、共享资源公平使用、GPU/API 成本记录、失败重跑和 fallback 规则 | `docs/compute-resource-guide.md` | 课程经理按真实平台记录额度、账单和异常 |
| 数据/伦理审查 | 项目必须审查数据来源、许可证、PII、偏见、污染、安全边界、模型卡和残余风险 | `docs/data-ethics-review.md` | 教师按项目场景判断是否需要额外人工审查 |
| 展示互评 | 项目展示、阅读复盘和同伴 review 有表单和评分标准 | `docs/presentation-peer-review.md` | 教师抽查 review 是否具体、可执行、尊重事实 |
| 运行改进闭环 | 课程运行后有隐藏测试统计、答疑记录、讲后复盘、复核争议、项目复现和来源更新记录；开课前有 readiness evidence packet | `docs/course-operations-log.md`、`docs/weekly-teaching-reflection-adjustment-log.md`、`docs/presemester-readiness-audit.md` | 教师每轮开课后更新改进任务看板 |
| 前沿准确性 | DeepSeek/V4/新模型声明有来源等级、复核日期和 monitor-only 降级边界 | `docs/frontier-source-audit.md` | D 级项不能进入作业、考试或项目评分事实；若后续找到 A 级来源再升级 |
| 开课前 readiness audit | 课程发布前有可归档命令证据、release safety、浏览器渲染、作业测试、CS224N snapshot 和人工 sign-off 边界 | `docs/presemester-readiness-audit.md` | Instructor / Course Manager 在正式 LMS 和 staff roster 配置后签核 |

最终验收命令：

```bash
.venv/bin/python verify_course.py
.venv/bin/python run_assignment_tests.py
.venv/bin/python verify_course.py --capstone --training
```

其中前两条是每次内容变更必须通过的基础门禁；capstone 验收在课程发布、期末项目或重大改版时运行。

## 推荐周历

| 周次 | 主题 | 对应内容 | 交付 |
|------|------|----------|------|
| 1 | Python/PyTorch 复习、Tokenization、Word Vectors | Ch01-Ch02 | BPE tokenizer + embedding 实验 |
| 2 | 反向传播复习、Attention 基础 | Ch03 | 手写 attention + causal mask 测试 |
| 3 | Transformer 与多头注意力 | Ch04-Ch05 | MHA/GQA/MLA 对比报告 |
| 4 | GPT 组装与参数/显存估算 | Ch06 | GPTModel forward pass + 参数审计 |
| 5 | 预训练目标、优化器、训练稳定性 | Ch07 | 微型 GPT 训练日志 |
| 6 | 生成、采样、推测解码、约束解码 | Ch08 | 采样策略定量对比 |
| 7 | SFT、LoRA、DPO、RLHF/GRPO | Ch09 | 偏好优化小实验 |
| 8 | 评测、benchmark、RAG、Agent | Ch08-Ch10 | 固定评测集 + RAG demo |
| 9 | 推理系统、KV Cache、vLLM、量化 | Ch10 | 推理压测与容量规划 |
| 10 | 项目展示与报告 | 两个 Capstone | 项目报告、复现包、口头展示 |

## 内容准确性维护规则

1. 基础理论优先引用论文、教材或官方文档；博客只作为辅助解释。
2. 前沿模型规格必须标注来源和发布日期，优先使用模型卡、技术报告、官方发布说明。
3. 对未充分同行评审或仍在 preview 的内容，正文要明确写成"案例/模型卡信息"，不能当作稳定基础理论。
4. 每次更新模型规格后运行：

```bash
.venv/bin/python verify_course.py
```

并用浏览器加载相关章节，确认 KaTeX、图表和链接仍能正常显示。

## 下一阶段补强清单

| 优先级 | 任务 | 验收方式 |
|--------|------|----------|
| Done | 为每章增加"学习目标 + 课前阅读 + 课后阅读" | 10 章顶部均有学习目标、课前阅读、课后阅读和评估证据 |
| Done | 新增 CS224N 对标矩阵 | [CS224N Benchmark Crosswalk](cs224n-benchmark-crosswalk.md) 覆盖 logistics、prerequisites、readings、schedule、assignments、final project、participation、office hours、policies、accessibility 和 updates |
| Done | 为 53 道编程练习补独立测试入口 | Ch01-Ch10 均有作业目录、starter、reference、tests，并由 `run_assignment_tests.py` 统一运行 |
| Done | 新增反向传播、矩阵微积分、张量求导复习附录 | [数学与 PyTorch 先修复习](math-prerequisites.md) 覆盖 Attention、CE、LayerNorm、DPO、GRPO |
| Done | 新增先修诊断测验 | [Prerequisite Diagnostic](prerequisite-diagnostic.md) 覆盖 Python、PyTorch、线代概率、反向传播、复现纪律、分级阈值和补救任务 |
| Done | 新增阶段性测验与 checkpoint 指南 | [Quiz and Checkpoint Guide](quiz-checkpoint-guide.md) 覆盖 quick check、recap quiz、midterm checkpoint、capstone readiness、补救路径和题目轮换 |
| Done | 新增期中 checkpoint 与期末复习样卷 | [Midterm and Final Review Pack](midterm-final-review-pack.md) 覆盖 Ch01-Ch07 样卷、Ch08-Ch10/经典 NLP/capstone 复习题、评分要点和补救映射 |
| Done | 增加 BERT/encoder-only、seq2seq/NMT、benchmark/evaluation 的专题材料 | [经典 NLP 与评测覆盖说明](nlp-evaluation-coverage.md) 明确专题与交付 |
| Done | 新增经典 NLP 与评测补充作业 | `assignments/ch11_classic_nlp/` 覆盖 UAS/LAS、BLEU、ROUGE-L、QA EM/F1 和 BERT MLM mask |
| Done | 为两个 Capstone 增加项目报告 rubric | [Capstone 项目报告 Rubric](project-report-rubric.md) 和两个项目 README 均已链接 |
| Done | 新增协作、引用和 AI 工具政策 | [课程政策](course-policies.md) 明确允许/禁止范围与复现要求 |
| Done | 新增学生支持与可及性指南 | [Accessibility and Student Support Guide](accessibility-student-support.md) 覆盖学术便利安排、材料可访问性、支持渠道、隐私边界、学习困难干预和公平评分 |
| Done | 建立前沿内容来源等级表 | [前沿模型来源等级与复核记录](frontier-source-audit.md) 标出 A/B/C/D 来源，并把无 A 级来源的前沿项降级为 D 级 monitor-only |
| Done | 降级或复核 Ch09/Ch10 中 V4 推断性表述 | “R1 统一”“Engram/NIAH” 已改为来源边界说明或移除具体数字 |
| Done | 新增书面推导与概念题题库 | [书面推导与概念题题库](written-problem-set.md) 覆盖 Ch01-Ch10 与经典 NLP 专题 |
| Done | 新增经典 NLP 专题 handout 与 deep-dive 模块 | [经典 NLP 专题 Handout](classic-nlp-handout.md) 覆盖 dependency parsing、seq2seq、BERT、evaluation、ethics；[Classic NLP Deep-Dive Teaching Module](classic-nlp-deep-dive-module.md) 可拆成 2-4 讲并覆盖 oracle trace、seq2seq equations、beam search、MLM objective 和 assessment pack |
| Done | 新增教师/助教答案要点 | [Instructor Solution Guide](instructor-solution-guide.md) 覆盖 Ch01-Ch10、经典 NLP、常见扣分点 |
| Done | 新增评分校准指南 | [Grading Calibration Guide](grading-calibration.md) 覆盖助教校准流程、双评规则、书面题样例、代码作业、capstone、阅读复盘和复核处理 |
| Done | 新增作业提交与发布指南 | [Assignment Submission and Release Guide](assignment-submission-guide.md) 覆盖发布前 checklist、学生提交包、LMS/Gradescope 配置、成绩发布和复核材料 |
| Done | 新增作业 handout 包 | [Assignment Handout Pack](assignment-handout-pack.md) 覆盖 11 个作业的 written questions、programming parts、评分权重、提交物和隐藏测试边界 |
| Done | 新增 autograder 与隐藏测试设计指南 | [Autograder 与隐藏测试设计指南](autograder-hidden-tests.md) 覆盖 Ch01-Ch10、两个 capstone、数值容差、失败日志和防投机检查 |
| Done | 新增 capstone 提案与 milestone 指南 | [Capstone Proposal and Milestone Guide](capstone-proposal-milestone.md) 覆盖项目提案模板、milestone 检查表、导师反馈记录和最终提交包 |
| Done | 新增默认最终项目指南 | [Default Final Project Guide](default-final-project-guide.md) 覆盖 GPT-2 风格实现、三个下游任务、proposal、milestone、poster/report、贡献声明和不通过条件 |
| Done | 新增 capstone 项目选题与归档指南 | [Capstone Project Gallery and Idea Bank](capstone-project-gallery.md) 覆盖默认项目、自定义项目边界、选题库、导师匹配、贡献声明和报告归档 |
| Done | 新增算力资源与成本指南 | [Compute Resource and Cost Guide](compute-resource-guide.md) 覆盖 CPU baseline、GPU/API 额度、公平使用、成本记录、失败重跑和降级路径 |
| Done | 新增数据与伦理审查指南 | [Data and Ethics Review](data-ethics-review.md) 覆盖数据来源、许可证、PII、偏见、评测污染、安全边界、模型卡和残余风险 |
| Done | 新增正式课程 syllabus | [课程 Syllabus](syllabus.md) 覆盖目标、先修、周安排、作业节奏、capstone 里程碑、迟交和复核 |
| Done | 新增课程学习目标证据映射 | [Course Outcome Map](course-outcome-map.md) 覆盖 6 个课程目标、证据等级、自动门禁覆盖矩阵和人工审查清单 |
| Done | 新增 10 周 / 20 讲 lecture plan | [10 周 / 20 讲 Lecture Plan](lecture-plan.md) 覆盖每讲目标、核心推导、课堂 demo、quick check、discussion section 和 office hours 模板 |
| Done | 新增课堂 demo runbook | [Classroom Demo Runbook](demo-runbook.md) 覆盖 20 讲 demo 命令、预期输出、常见失败和备用方案 |
| Done | 新增课程材料发布索引 | [Course Materials Index](course-materials-index.md) 覆盖 20 讲章节、阅读、demo、作业证据、发布状态、slides/notes/recording 规则和版本记录 |
| Done | 新增 20 讲课件大纲 | [Lecture Slide Outline](lecture-slide-outline.md) 覆盖每讲 slide 标题、核心 slides、demo、quick check 和课后证据 |
| Done | 新增 20 讲 lecture notes 索引 | [Lecture Notes Index](lecture-notes-index.md) 覆盖每讲 notes、板书推导、复盘问题、证据和发布 checklist |
| Done | 新增板书推导与教师讲稿包 | [Board Derivation and Instructor Notes Pack](board-derivation-pack.md) 覆盖 BPE、Embedding、RoPE、attention scaling、mask、MHA/GQA/MLA、Norm、CE、AdamW、DPO、GRPO、KV cache 和 L1-L20 quick check |
| Done | 新增讨论课与 office hours 指南 | [Discussion Section and Office Hours Guide](discussion-office-hours-guide.md) 覆盖 Week 1-10 shape drill、failure drill、paper-to-code drill、office-hour triage 和 exit ticket 汇总 |
| Done | 新增学生 FAQ 与 troubleshooting 指南 | [Student FAQ and Troubleshooting Guide](student-faq-troubleshooting.md) 覆盖环境、公开/隐藏测试、shape/mask、capstone、复核和提问模板 |
| Done | 新增 staff 执行手册 | [Course Staff Runbook](staff-runbook.md) 覆盖角色职责、开课 checklist、工具权限、公告模板、每周 staff meeting、作业评分交接、Office Hours 排班、事故升级和期末交接 |
| Done | 新增课堂参与与反馈调查指南 | [Participation and Feedback Guide](participation-feedback-guide.md) 覆盖参与评分、讨论区规则、期中/期末反馈、嘉宾讲座替代任务和聚合反馈闭环 |
| Done | 新增项目展示与同伴 review rubric | [项目展示与同伴 Review Rubric](presentation-peer-review.md) 覆盖展示评分、互评表单、阅读复盘和来源检查 |
| Done | 新增逐周阅读清单与复盘 handout | [逐周阅读清单与复盘 Handout](reading-list.md) 覆盖 Week 1-10 必读、选读、复盘问题、来源等级和提交模板 |
| Done | 新增逐章来源与准确性映射 | [Chapter Source and Accuracy Map](chapter-source-map.md) 覆盖 Ch01-Ch10、经典 NLP 专题、权威来源、验证证据和常见误讲边界 |
| Done | 新增 claim 复核工作表 | [Claim Audit Worksheet](claim-audit-worksheet.md) 覆盖 claim 类型、来源等级、边界、学生用途、处理动作和逐章最低审查清单 |
| Done | 新增外部来源清单 | [External Source Inventory](external-source-inventory.md) 区分 A-stable、A-volatile、B-implementation、C-background 和 runtime asset |
| Done | 新增外部来源复核指南 | [External Source Verification Guide](external-source-verification.md) 覆盖复核频率、记录字段、外链失效处理、高风险 claim、学生项目引用和发布前 checklist |
| Done | 新增前沿 seminar handout | [Frontier Seminar Handout](frontier-seminar-handout.md) 覆盖 interpretability、多模态、社会影响、开放问题、评分 rubric 和项目连接 |
| Done | 新增课程运行与改进记录 | [Course Operations and Improvement Log](course-operations-log.md) 覆盖每周运行、作业复盘、隐藏测试统计、答疑、项目复现、复核争议、来源更新和改进任务看板 |
| Done | 新增开课前 readiness evidence packet | [Pre-Semester Readiness Audit](presemester-readiness-audit.md) 记录 CS224N snapshot verifier、课程总门禁、release safety、browser smoke、作业测试和人工 sign-off 边界 |
