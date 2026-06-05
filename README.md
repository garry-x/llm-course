<p align="center">
  <img src="images/favicon.svg" width="64" alt="LLM 深度学习">
</p>

<h1 align="center">LLM 深度学习</h1>

<p align="center">
  <strong>从代码出发，10 章构建一个完整的大语言模型</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/chapters-10-orange" alt="10 chapters">
  <img src="https://img.shields.io/badge/exercises-103_(53编程+50概念)-blue" alt="103 exercises">
  <img src="https://img.shields.io/badge/sections-127-yellow" alt="127 sections">
  <img src="https://img.shields.io/badge/DeepSeek-V2→R1→V3→V4-green" alt="DeepSeek">
  <img src="https://img.shields.io/badge/iPad_Pro-optimized-purple" alt="iPad Pro">
  <img src="https://img.shields.io/badge/docker-ready-blue" alt="Docker">
  <img src="https://img.shields.io/badge/db-IndexedDB-red" alt="IndexedDB">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="license">
</p>

---

## 关于本课程

这是一门**从代码出发**的 LLM 实战课程。不做概念浏览，而是用 Python 和 PyTorch 逐行实现大语言模型的每一个核心组件。

**每章的学习循环：**
> 深度理论 → 理解"为什么" → 编程练习（你写代码）→ 对照参考解答 → 概念练习巩固

融入 **DeepSeek 开源技术体系**（V2 MLA → R1 GRPO → V3 FP8/MoE → V4 CSA+HCA/mHC），用真实的工业级设计来理解每一个组件。

## 初学者怎么学

这门课覆盖从基础组件到工业前沿的完整链路。第一次学习时不要把所有高级专题都当成必修，可以按三遍路线推进：

| 阶段 | 章节 | 目标 | 建议 |
|------|------|------|------|
| 第一遍：主线必学 | Ch01-Ch06 | 把文本变成 token，搭出能前向传播的 GPT | 代码练习必须动手写；DeepSeek 扩展先理解动机即可 |
| 第二遍：跑起来 | Ch07-Ch08 | 训练小模型，并让模型生成文本 | 重点看 loss、optimizer、sampling 的输入输出形状 |
| 第三遍：进阶选读 | Ch09-Ch10 | 微调、对齐、RAG、推理优化和前沿架构 | 先掌握概念地图，再回头补公式和工程细节 |

**最低前置要求：**会 Python 函数、列表/字典、基础矩阵乘法，知道 PyTorch 张量的 `shape`。如果数学推导暂时吃力，先抓住每节的“输入是什么、输出是什么、形状怎么变”。

## 高校课程规格

如果目标是达到类似 Stanford CS224N 的高校课程水准，本课程不只要求“读完章节”，还要求可评分、可复现、可引用。建议按以下方式组织：

| 评估项 | 权重 | 交付证据 |
|--------|:--:|----------|
| 章节编程作业 | 35% | 每章核心代码、运行输出、测试或错误分析 |
| 书面推导与概念题 | 20% | 关键公式推导、复杂度分析、选择题解释 |
| 训练工程 Capstone | 15% | 数据审计、训练日志、checkpoint/resume、成本估算 |
| 推理工程 Capstone | 20% | API、压测、评测、SLO 与容量规划报告 |
| 阅读复盘与同伴 review | 10% | 论文摘要、复现实验记录、互评反馈 |

课程质量审计、CS224N 对标矩阵、当前 CS224N 公开页快照、推荐周历、内容准确性维护规则见 [高校课程质量审计与升级路线](docs/university-course-quality-audit.md#高校课程质量审计与升级路线)、[CS224N Benchmark Crosswalk](docs/cs224n-benchmark-crosswalk.md#cs224n-benchmark-crosswalk) 和 [CS224N Current Benchmark Snapshot](docs/cs224n-current-benchmark-snapshot.md#当前公开页要点)。正式授课安排、学习目标证据映射、20 讲计划、课程日历与截止日台账、课件大纲、lecture notes 索引、lecture notes 审稿标准、lecture notes 逐讲复核台账、lecture note 样例包、板书推导脚本、数学推导审计、课堂 demo runbook、课程材料索引、课程直播/录播/文字稿政策、版本归档政策、课程沟通与公告政策、学生可见 staff 与 office hours 目录、staff assistance 与 code review 边界、选课/旁听/公开使用政策、讨论课/答疑、学生 FAQ、环境复现、测验与阶段检查、assessment item bank、assessment administration、概念误区诊断、期中/期末样卷、课堂参与与反馈、guest speaker / external seminar 流程、staff 执行手册、政策、学术诚信个案处理与相似性检测流程、学生支持与可及性、先修诊断、Python/PyTorch review session、先修复习、ML foundations bridge、逐周阅读、paper recap 校准、paper-to-code traceability、前沿 seminar、逐章来源映射、逐章 claim 审计台账、claim 复核工作表、外部来源清单、外部来源复核、前沿来源证据卡、外部专家复核、作业 handout、书面题库、教师答案要点、评分校准、作业提交与发布、成绩册与 LMS 运行、隐藏测试设计、经典 NLP 专题、项目提案与里程碑、项目团队与导师政策、默认最终项目、项目报告模板、项目报告样例、实验严谨性与统计评测、项目展示与公开归档政策、项目选题与归档、算力资源与成本、数据与伦理审查、项目评分、展示互评、课程运行改进闭环和前沿来源复核见 [课程 Syllabus](docs/syllabus.md#课程目标)、[Course Outcome Map](docs/course-outcome-map.md#course-outcome-map)、[10 周 / 20 讲 Lecture Plan](docs/lecture-plan.md#授课结构)、[Course Calendar and Deadline Ledger](docs/course-calendar-deadline-ledger.md)、[Lecture Slide Outline](docs/lecture-slide-outline.md#slide-deck-模板)、[Lecture Notes Index](docs/lecture-notes-index.md#notes-发布状态)、[Lecture Notes Quality and Review Standard](docs/lecture-notes-quality-review.md)、[Lecture Notes Review Ledger](docs/lecture-notes-review-ledger.md)、[Lecture Note Sample Pack](docs/lecture-note-sample-pack.md)、[Board Derivation and Instructor Notes Pack](docs/board-derivation-pack.md#课堂板书脚本)、[Mathematical Derivation Audit](docs/mathematical-derivation-audit.md)、[Classroom Demo Runbook](docs/demo-runbook.md#demo-环境检查)、[Course Materials Index](docs/course-materials-index.md#course-materials-index)、[Lecture Media Access Policy](docs/lecture-media-access-policy.md)、[Material Versioning and Archive Policy](docs/material-versioning-archive-policy.md)、[Course Communication and Announcement Policy](docs/course-communication-policy.md)、[Course Staff and Office Hours Directory](docs/course-staff-office-hours-directory.md)、[Staff Assistance and Code Review Boundary Policy](docs/staff-assistance-code-review-policy.md)、[Enrollment, Audit, and Public Use Policy](docs/enrollment-audit-public-use-policy.md)、[Discussion Section and Office Hours Guide](docs/discussion-office-hours-guide.md)、[Student FAQ and Troubleshooting Guide](docs/student-faq-troubleshooting.md)、[Environment and Reproducibility Guide](docs/environment-reproducibility.md)、[Quiz and Checkpoint Guide](docs/quiz-checkpoint-guide.md)、[Assessment Item Bank Ledger](docs/assessment-item-bank-ledger.md)、[Assessment Administration and Exam Integrity Policy](docs/assessment-administration-policy.md)、[Concept Mastery and Misconception Map](docs/concept-misconception-map.md)、[Midterm and Final Review Pack](docs/midterm-final-review-pack.md)、[Participation and Feedback Guide](docs/participation-feedback-guide.md)、[Guest Speaker and External Seminar Policy](docs/guest-speaker-seminar-policy.md)、[Course Staff Runbook](docs/staff-runbook.md)、[课程政策](docs/course-policies.md)、[Academic Integrity Case Process](docs/academic-integrity-case-process.md)、[Accessibility and Student Support Guide](docs/accessibility-student-support.md)、[Prerequisite Diagnostic](docs/prerequisite-diagnostic.md)、[Python and PyTorch Review Session](docs/python-pytorch-review-session.md)、[数学与 PyTorch 先修复习](docs/math-prerequisites.md)、[ML Foundations Prerequisite Bridge](docs/ml-foundations-prerequisite-bridge.md)、[逐周阅读清单与复盘 Handout](docs/reading-list.md)、[Paper Recap Calibration Pack](docs/paper-recap-calibration-pack.md)、[Paper-to-Code Traceability Matrix](docs/paper-to-code-traceability-matrix.md)、[Frontier Seminar Handout](docs/frontier-seminar-handout.md)、[Chapter Source and Accuracy Map](docs/chapter-source-map.md)、[Chapter Claim Audit Ledger](docs/chapter-claim-audit-ledger.md)、[Claim Audit Worksheet](docs/claim-audit-worksheet.md)、[External Source Inventory](docs/external-source-inventory.md)、[External Source Verification Guide](docs/external-source-verification.md)、[Frontier Source Evidence Cards](docs/frontier-source-evidence-cards.md)、[External Expert Review Dossier](docs/external-expert-review-dossier.md)、[Assignment Handout Pack](docs/assignment-handout-pack.md)、[书面推导与概念题题库](docs/written-problem-set.md)、[Instructor Solution Guide](docs/instructor-solution-guide.md)、[Grading Calibration Guide](docs/grading-calibration.md)、[Assignment Submission and Release Guide](docs/assignment-submission-guide.md)、[Gradebook and LMS Operations Guide](docs/gradebook-lms-operations.md)、[Autograder 与隐藏测试设计指南](docs/autograder-hidden-tests.md)、[经典 NLP 专题 Handout](docs/classic-nlp-handout.md)、[Classic NLP Deep-Dive Teaching Module](docs/classic-nlp-deep-dive-module.md)、[经典 NLP 与评测覆盖说明](docs/nlp-evaluation-coverage.md)、[Capstone Proposal and Milestone Guide](docs/capstone-proposal-milestone.md)、[Project Team and Mentor Policy](docs/project-team-mentor-policy.md)、[Default Final Project Guide](docs/default-final-project-guide.md)、[Project Report Template and Reproducibility Checklist](docs/project-report-template.md)、[Project Report Exemplar Pack](docs/project-report-exemplar-pack.md)、[Experimental Rigor and Evaluation Statistics Guide](docs/experimental-rigor-evaluation-statistics.md)、[Final Project Showcase and Archive Policy](docs/final-project-showcase-archive-policy.md)、[Capstone Project Gallery and Idea Bank](docs/capstone-project-gallery.md)、[Compute Resource and Cost Guide](docs/compute-resource-guide.md)、[Data and Ethics Review](docs/data-ethics-review.md)、[Capstone 项目报告 Rubric](docs/project-report-rubric.md)、[项目展示与同伴 Review Rubric](docs/presentation-peer-review.md)、[Course Operations and Improvement Log](docs/course-operations-log.md) 和 [前沿模型来源等级与复核记录](docs/frontier-source-audit.md)。

评估覆盖矩阵见 [Assessment Blueprint and Coverage Matrix](docs/assessment-blueprint-coverage-matrix.md)，用于把 CO1-CO6、programming/written/quiz/capstone/reading 渠道、认知层级和 grading gate 对齐。

课程目标达成度报告见 [Learning Outcome Attainment Report](docs/learning-outcome-attainment-report.md)，用于把 CO1-CO6 的 direct/indirect evidence、达标阈值、dry-run 状态和下一轮改进动作汇总为可审计记录。

题目质量统计复核见 [Assessment Item Analysis and Psychometrics Guide](docs/assessment-item-analysis-psychometrics.md)，用于在 quiz/checkpoint 后检查 item_difficulty_p、item_discrimination_d、distractor_efficiency、rubric fit、fairness flag 和 item retire/revise 决策。

课堂同行观察、期中反馈 response memo、期末课程评估和下一轮改进闭环见 [Teaching Observation and Course Evaluation Dossier](docs/teaching-observation-course-evaluation.md)。

助教训练、评分校准、office-hours 边界、项目 mentor、隐私/可及性/诚信 routing 的 staff-facing 签核见 [TA Training and Certification Dossier](docs/ta-training-certification.md)。

评分锚点样例和学生可见反馈口径见 [Grading Anchor Sample Feedback Pack](docs/grading-anchor-sample-feedback-pack.md)，用于把 written、programming、capstone、reading、peer review 和 regrade 的双评边界落实为可复用 anchor sample。

高风险讲次的学生可见核心讲义见 [Lecture Note Core Pack](docs/lecture-note-core-pack.md)，覆盖 L2/L4/L6/L12/L15 的类比推理、RoPE、mask/CE、GQA/MLA、推测解码、来源边界和经典 NLP 对标主题。

学生可见的讨论课 worksheet 见 [Recitation Worksheet Pack](docs/recitation-worksheet-pack.md)，覆盖 shape drill、failure drill、paper-to-code link、source boundary、exit ticket 和 capstone rehearsal。

编程作业代码质量评分口径见 [Programming Assignment Code Quality Rubric](docs/programming-assignment-code-quality-rubric.md)，用于把 API contract、shape discipline、向量化 PyTorch、数值稳定、dtype/device、边界处理、可读性、复现和反硬编码纳入人工复核。

学习数据触发补救教学的规则见 [Learning Analytics and Remediation Plan](docs/learning-analytics-remediation-plan.md)，用于把 quiz、作业、recitation、office hours、reading recap、project milestone 和 gradebook 聚合信号转化为 recap、worksheet、project clinic、FAQ 或评分校准动作。

每周讲后复盘与下次课调整见 [Weekly Teaching Reflection and Adjustment Log](docs/weekly-teaching-reflection-adjustment-log.md)，用于把 quick check、exit ticket、office hours、作业失败类别、阅读复盘和项目 milestone 的聚合证据转化为下一讲 recap、worksheet、FAQ、handout、rubric 或 source patch。

课程 workload、难度阶梯和 10/12 周节奏调整见 [Workload and Pacing Calibration](docs/workload-pacing-calibration.md)，用于校准每周 lecture、reading、assignment、recitation 和 capstone 负荷。

代表性课件样例见 [Lecture Slide Sample Pack](docs/lecture-slide-sample-pack.md)，用于检查 slides 的 learning goals、visual plan、formula/shape、demo cue、quick check、accessibility text 和 source boundary。

核心术语定义见 [Core Concept Glossary](docs/core-concept-glossary.md)，用于统一 BPE、embedding、RoPE、attention、GQA、MLA、LayerNorm、MoE、CE/PPL、DPO、RAG、SLO、evaluation metric 和 source boundary 等术语的课程内定义、不要误讲成什么、证据锚点和来源边界。

知识点依赖、章节 unlock path 和 spiral review 路径见 [Topic Dependency and Spiral Review Map](docs/topic-dependency-map.md)，用于说明 RoPE、attention、training、alignment、RAG、serving metric 和 capstone evidence 之间的先修关系与补救入口。

统一符号、shape、mask、cache、loss、optimizer、serving metric 和 classic NLP metric 单位见 [Notation and Shape Glossary](docs/notation-shape-glossary.md)，用于约束章节正文、作业、讨论课、paper recap 和 capstone 报告中的维度与单位写法。

逐章可复算小例子见 [Worked Example Pack](docs/worked-example-pack.md)，用于把 BPE、RoPE、attention、GQA、Norm、GPT 参数、AdamW、top-p、DPO、KV cache 和经典 NLP metrics 的输入、shape、worked trace、常见错误和评估证据对齐。

阅读讨论题库见 [Reading Discussion Question Bank](docs/reading-discussion-question-bank.md)，用于把逐周阅读、paper recap、paper-to-code drill、quiz/checkpoint 和 capstone clinic 连接成可评分的问题条目。

综合复习路径见 [Comprehensive Review Study Guide](docs/comprehensive-review-study-guide.md)，用于把 midterm/final 样题、书面题、worked examples、阅读讨论题、错题日志和 capstone readiness 串成两轮复习计划。

安全、伦理与社会影响案例见 [Safety and Societal Impact Casebook](docs/safety-societal-impact-casebook.md)，用于把 privacy、bias、safety、contamination、misuse、copyright、access 和 evaluation 风险落成可讨论、可评分、可复核的案例。

模型卡、API 文档、leaderboard 和 benchmark 数字的引用模板见 [Model and Benchmark Card Guide](docs/model-benchmark-card-guide.md)，用于把 context length、价格、latency、tokens/s、安全和质量 claim 写成有来源日期、配置边界和不支持结论的证据卡。

Capstone 展示后的项目答辩和个人口头追问题库见 [Capstone Defense and Oral Exam Question Bank](docs/capstone-defense-oral-exam-bank.md)，用于验证个人贡献、代码理解、实验边界、复现证据、来源 claim 和安全风险。

教师私有 autograder 运行流程见 [Private Autograder Operations Guide](docs/private-autograder-operations.md) 和 [scripts/run_private_autograder.py](scripts/run_private_autograder.py)，用于生成公开 dry run、隐藏测试 manifest、LMS entrypoint 和复核归档证据。

开课前 readiness 证据包见 [Pre-Semester Readiness Audit](docs/presemester-readiness-audit.md)，集中记录 CS224N current snapshot verifier、课程总门禁、student release safety、browser smoke、作业测试、capstone 验收要求和人工 sign-off 边界。

机器可读 evidence manifest 由 [scripts/generate_course_evidence_manifest.py](scripts/generate_course_evidence_manifest.py) 生成；当前 readiness 证据覆盖 `required_evidence_files: 111`、`required_marker_checks: 63`、全部 `COURSE_DOCS` 文档、核心教学包、教师/评分包、来源清单、classic NLP deep-dive、release safety、capstone gate 和人工 sign-off 边界。

课程数据、模型、tokenizer、checkpoint、评测集合和 runtime asset 的资产级来源登记见 [Dataset, Model, and Artifact Provenance Registry](docs/dataset-model-artifact-registry.md)，用于把 data ethics、source inventory、环境复现和项目报告中的 provenance 要求落到可检查的 artifact ID。

项目 proposal、milestone、final report、presentation 和 archive candidate 的统一提交包见 [Project Submission Dossier](docs/project-submission-dossier.md)，用于把 artifact_manifest、split_card、metric_card、uncertainty_record、claim_audit、leakage_check、run log 和贡献披露连成可审计证据链。

课程内容勘误、修订、公告、验证和评分影响处理见 [Course Errata and Correction Ledger](docs/course-errata-correction-ledger.md)，用于记录学生或 staff 发现的问题如何进入 patch、verification、announcement 和 regrade/release closure。

**章节作业测试：**第 1-10 章已提供可运行作业测试入口：[assignments/ch01_bpe/](assignments/ch01_bpe/) · [assignments/ch02_embeddings/](assignments/ch02_embeddings/) · [assignments/ch03_attention/](assignments/ch03_attention/) · [assignments/ch04_multihead/](assignments/ch04_multihead/) · [assignments/ch05_block/](assignments/ch05_block/) · [assignments/ch06_gpt/](assignments/ch06_gpt/) · [assignments/ch07_training/](assignments/ch07_training/) · [assignments/ch08_generation/](assignments/ch08_generation/) · [assignments/ch09_alignment/](assignments/ch09_alignment/) · [assignments/ch10_inference/](assignments/ch10_inference/)。经典 NLP 与评测补充作业见 [assignments/ch11_classic_nlp/](assignments/ch11_classic_nlp/)。

## 面向 LLM 推理工程师的能力矩阵

如果你的目标是成为 LLM 推理工程师，学习目标不只是“懂 Transformer”，而是能把模型稳定、低成本、可观测地服务给真实用户。课程按以下能力组织：

| 能力 | 对应章节 | 你需要能做什么 |
|------|----------|----------------|
| 模型结构读懂 | Ch01-Ch06 | 看懂 tokenizer、attention、KV Cache 来源、logits 输出和参数规模 |
| 生成与延迟拆解 | Ch08 | 区分 prefill/decode，解释 TTFT、TPOT、TPS、吞吐和采样质量 |
| 显存与带宽优化 | Ch04, Ch10 | 计算 KV Cache、理解 MQA/GQA/MLA、量化、FlashAttention 和显存瓶颈 |
| 推理服务架构 | Ch10 | 选择 vLLM/SGLang/TensorRT-LLM/llama.cpp，理解 batching、prefix cache、并发调度 |
| 检索与工具调用 | Ch08-Ch10 | 设计结构化输出、RAG、Agent 工具链和失败兜底 |
| 评测与上线 | Ch09-Ch10 | 设计质量/安全/延迟/成本指标，做压测、回归评估和上线检查 |

**课程最终项目：**[LLM Inference Engineering Capstone](projects/inference-engineering-capstone/) 会带你部署一个 OpenAI-compatible Chat API：支持流式输出、结构化 JSON、工具调用、RAG、基础指标、压测报告、P50/P95/P99 延迟和 tokens/s 成本估算。先用 mock engine 跑通服务骨架，再替换为 vLLM / SGLang / TensorRT-LLM / llama.cpp。

**毕业验收标准：**如果你想按岗位能力学习，先看 [LLM 推理工程师课程路线与毕业验收](inference-engineer-curriculum.html)（详细 Markdown 版在 [docs/inference-engineer-curriculum.md](docs/inference-engineer-curriculum.md)）。它把章节、练习、Capstone、压测、评测和上线复盘映射到可检查的能力证据。

## 面向 LLM 训练工程师的能力矩阵

如果你的目标是成为 LLM 训练工程师，学习目标要从“能跑一个 loss”推进到“能交付可复现、可恢复、可观测、成本可解释的训练系统”。课程按以下能力补齐：

| 能力 | 对应章节 | 你需要能做什么 |
|------|----------|----------------|
| 数据与 Token 预算 | Ch01, Ch07 | 审计样本、重复、长度分布和 token 规模，估算训练 step |
| 训练循环工程 | Ch06-Ch07 | 组织 PyTorch Dataset/DataLoader、forward、loss、backward、optimizer、scheduler |
| 稳定性与恢复 | Ch07 | 使用 seed、grad clipping、checkpoint、resume 和异常排查保护训练 |
| 监控与评测 | Ch07-Ch09 | 记录 train_loss、val_loss、ppl、lr、grad_norm、tokens/s，并解释曲线 |
| 微调与对齐 | Ch09 | 区分 SFT、LoRA、DPO、GRPO 的数据格式、损失和适用场景 |
| 分布式与成本 | Ch07, Ch10 | 理解 AMP、FSDP/ZeRO、global batch tokens、GPU hours 和 checkpoint 存储 |

**训练最终项目：**[LLM Training Engineering Capstone](projects/training-engineering-capstone/) 会带你实现一个 PyTorch 字符级语言模型训练闭环：数据审计、训练、验证、checkpoint、resume、metrics、训练规划和一键验收。默认模型很小，CPU 可跑通；有 GPU 时可直接迁移到 CUDA 环境。

**毕业验收标准：**按 [LLM 训练工程师课程路线与毕业验收](training-engineer-curriculum.html)（详细 Markdown 版在 [docs/training-engineer-curriculum.md](docs/training-engineer-curriculum.md)）交付训练报告、指标日志、checkpoint 恢复证明和成本规划。

## 快速开始

### Docker 部署（推荐）

```bash
git clone https://github.com/garry-x/llm-learner.git && cd llm-learner

# 构建并启动 (默认 :8080)
./serve.sh docker-build
./serve.sh docker-up

# 指定端口 (如 :3000)
./serve.sh docker-build -p 3000
./serve.sh docker-up -p 3000

# 管理命令
./serve.sh docker-logs        # 实时日志
./serve.sh docker-restart     # 重启
./serve.sh docker-down        # 停止并删除

# 或使用 docker compose
docker compose up -d
PORT=3000 docker compose up -d
```

### 本地开发

```bash
./serve.sh                    # 默认 0.0.0.0:8080
./serve.sh serve -p 3000      # 指定端口
```

### 课程验证

本仓库推荐使用根目录下的 `.venv` 运行本地验收；如果你已经激活等价虚拟环境，也可以把 `.venv/bin/python` 替换为 `python`。先确认 PyTorch 可导入：

```bash
.venv/bin/python -c "import sys, torch; print(sys.version.split()[0], torch.__version__)"

.venv/bin/python verify_course.py               # 校验章节统计、链接、Chromium 渲染、JS/Python 语法和 Capstone 用例
.venv/bin/python run_assignment_tests.py         # 运行章节作业测试（当前覆盖 Ch01-Ch10 与 Ch11 经典 NLP；Ch02-Ch10 需要 PyTorch）
.venv/bin/python scripts/generate_course_evidence_manifest.py --check  # 生成并检查课程 readiness evidence manifest
.venv/bin/python verify_course.py --capstone --training  # 发布/期末门禁：运行推理与训练 Capstone 一键验收
```

### CLI 命令一览

| 命令 | 说明 | 支持 `-p` |
|------|------|:---------:|
| `serve` | 本地 Python HTTP 服务器 | ✓ |
| `docker-build` | 构建镜像 (`--build-arg LISTEN_PORT`) | ✓ |
| `docker-up` | 启动容器 (自动检测/终止端口占用) | ✓ |
| `docker-down` | 停止 + 删除容器 | |
| `docker-logs` | 实时 nginx 日志 | |
| `docker-restart` | = down + up | |

**环境要求：** Docker 或 Python 3.10+ / 现代浏览器（Safari / Chrome / Edge），本地验收需要 Chromium/Chrome 执行章节渲染 smoke test；推荐 iPad Pro 或桌面端阅读。

## 课程大纲

| # | 章节 | 编程产出 | 练习 |
|---|------|---------|:--:|
| 1 | **环境搭建与分词** — 实现 BPE Tokenizer | `BPETokenizer` ~80行 | 5+5 |
| 2 | **嵌入层与位置编码** — TokenEmbedding + RoPE + PromptEng | `TokenEmbedding` + `RoPE` ~60行 | 4+5 |
| 3 | **单头自注意力** — Scaled Dot-Product Attention | `ScaledDotProductAttention` ~40行 | 5+5 |
| 4 | **多头注意力与 MLA** — MHA → GQA → DeepSeek MLA | `MultiHeadAttention` ~60行 | 5+5 |
| 5 | **Transformer Block** — RMSNorm + FFN/SwiGLU + mHC | `TransformerBlock` ~50行 | 5+5 |
| 6 | **组装 GPT + DeepSeekMoE** — GPT-2 124M 完整模型 | `GPTModel` ~100行 | 5+5 |
| 7 | **训练循环** — AdamW/Muon + FP8/FP4 + 分布式 | 完整训练脚本 ~120行 | 6+5 |
| 8 | **文本生成** — 采样策略 + MTP 推测解码 + 约束生成 | 文本生成器 ~60行 | 6+5 |
| 9 | **微调与对齐** — SFT/LoRA/DPO/GRPO + R1 推理 | SFT + LoRA + GRPO ~190行 | 6+5 |
| 10 | **推理优化与前沿** — KV Cache/量化/RAG/vLLM/Triton/生产服务/多模态 | KV Cache + 量化 + RAG + LSH + 服务蓝图 | 6+5 |

> **总计：53 道编程练习 + 50 道概念练习，127 小节，约 10+ 小时学习时间**

## DeepSeek 技术融入

前沿模型信息变化很快。下表用于建立技术地图；具体数字和模型规格按 [前沿模型来源等级与复核记录](docs/frontier-source-audit.md) 维护，正文中的 V3.2/V4 结论应理解为“截至 2026-06-05 的模型卡/技术报告信息”；D 级 monitor-only 项不能作为作业、考试或项目评分事实。

| 技术 | 来源等级 | 复核日期 | 对应章节 | 要点 |
|------|----------|----------|---------|------|
| MLA (Multi-head Latent Attention) | A：DeepSeek-V2/V3 技术报告 | 2026-06-05 | Ch04 | KV Cache 压缩，潜在向量解耦 RoPE |
| GRPO (Group Relative Policy Optimization) | A：DeepSeek-R1 论文/Nature 条目 | 2026-06-05 | Ch09 | 无需 Critic，组内白化优势，RL 激励推理能力 |
| DeepSeekMoE + Aux-Loss-Free | A：DeepSeek-V3 技术报告 | 2026-06-05 | Ch06 | 671B→37B 稀疏激活，动态偏置负载均衡 |
| FP8 Mixed Precision + DualPipe | A：DeepSeek-V3 技术报告 | 2026-06-05 | Ch07 | FP8 混合精度，通信计算重叠 |
| MTP (Multi-Token Prediction) | A：DeepSeek-V3 技术报告 | 2026-06-05 | Ch08 | 训练/推理双重增益，推测解码草稿信号 |
| DSA (DeepSeek Sparse Attention) | A：DeepSeek API 新闻/DeepSeek-V3.2 论文 | 2026-06-05 | Ch10 | 可学习 top-k 稀疏，长上下文降计算成本 |
| CSA + HCA Hybrid Attention | A：DeepSeek-V4 模型卡 | 2026-06-05 | Ch10 | 模型卡报告 1M 上下文 27% FLOPs / 10% KV |
| Engram 外部记忆 | D：monitor-only，未保留具体 benchmark 数字 | 2026-06-05 | Ch10 | 仅作“模型内建外部记忆 + LSH 检索”的前沿案例，不作为课程事实 |
| mHC (Manifold-Constrained Hyper-Connections) | A：DeepSeek-V4 模型卡/Transformers 配置 | 2026-06-05 | Ch05 | Birkhoff 约束，Sinkhorn-Knopp，残差连接扩展 |
| Muon Optimizer | A：DeepSeek-V4 模型卡 | 2026-06-05 | Ch07 | 动量矩阵正交化替代 AdamW，Newton-Schulz 迭代 |

## 项目结构

```
llm-learner/
├── index.html                # 课程首页：Hero + 仪表板 + 章节目录
├── inference-engineer-curriculum.html # 推理工程师毕业验收页
├── training-engineer-curriculum.html  # 训练工程师毕业验收页
├── css/style.css              # 暖色 editorial 风格，暗色/浅色双主题
├── js/
│   ├── db.js                  # IndexedDB 持久化存储层
│   └── app.js                 # 搜索/主题/字号/进度/笔记/TOC/键盘导航
├── chapters/                  # 10 章，纯 HTML（~8,000 行）
│   └── ch01.html ~ ch10.html
├── docs/
│   ├── inference-engineer-curriculum.md  # 推理工程师学习路线与毕业验收
│   └── training-engineer-curriculum.md   # 训练工程师学习路线与毕业验收
├── projects/
│   ├── inference-engineering-capstone/
│   │   ├── acceptance.py      # 一键验收：health + 评测 + 压测 + SLO + 容量估算
│   │   ├── app.py             # OpenAI-compatible Chat API + SSE + RAG stub + metrics
│   │   ├── benchmark.py       # 并发压测，输出 P50/P95/P99、TTFT/TPOT、tokens/s
│   │   ├── capacity_plan.py   # 显存、最大 batch 和每 1M tokens 成本估算
│   │   ├── evaluate.py        # 固定评测集回归检查
│   │   ├── slo_check.py       # 读取压测 JSON，检查延迟/吞吐/错误率 SLO
│   │   └── eval_cases.jsonl
│   └── training-engineering-capstone/
│       ├── acceptance.py      # 一键验收：数据审计 + 训练 + resume + 规划
│       ├── data_audit.py      # 语料行数、重复、长度和字符规模审计
│       ├── plan_training.py   # step、GPU hours、成本和 checkpoint 存储估算
│       ├── train.py           # PyTorch tiny LM 训练循环 + checkpoint/resume
│       └── sample_corpus.txt
├── images/                    # 11 张 SVG 概念示意图 + favicon（支持暗色模式）
│   ├── bpe-pipeline.svg       # BPE 训练与编解码流程
│   ├── rope-rotation.svg      # RoPE 旋转位置编码原理
│   ├── attention-flow.svg     # Scaled Dot-Product Attention 数据流
│   ├── transformer-arch.svg   # GPT 架构全景
│   ├── mha-gqa-mla.svg        # MHA / GQA / MLA KV Cache 压缩对比
│   ├── transformer-block.svg  # Transformer Block 内部结构
│   ├── gpt-params.svg         # GPT-2 124M 参数分解
│   ├── training-loop.svg      # 训练循环 + 优化器演进
│   ├── sampling-strategies.svg# 4 种采样策略对比
│   ├── rlhf-dpo-grpo.svg      # RLHF / DPO / GRPO 对齐方法对比
│   ├── gpu-memory.svg         # GPU 内存层次 — A100 架构
│   └── favicon.svg/.png/.ico  # ComfyUI + FLUX.1-dev 生成
├── Dockerfile                 # nginx:alpine, gzip, ARG LISTEN_PORT
├── docker-compose.yml         # 一键部署，PORT 环境变量可配
├── .dockerignore
├── verify_course.py           # 课程级验证入口
├── serve.sh                   # CLI: serve + docker-build/up/down/logs/restart
└── README.md
```

## 页面特性

| 特性 | 说明 |
|------|------|
| 👤 **用户账户** | 多账户切换，随机头像颜色，localStorage + IndexedDB 持久化 |
| 📝 **章节笔记** | 右下角滑出面板，自动关联当前阅读小节，按用户隔离 |
| 💾 **IndexedDB 存储** | 双写策略：localStorage 缓存(即时) + IDB 持久化(备份)，不丢数据 |
| 🐳 **Docker 部署** | nginx:alpine，gzip 压缩，`LISTEN_PORT` 可配，<10MB 镜像 |
| 🎨 **暗色/浅色双主题** | CSS 变量驱动，一键切换，localStorage 持久化 |
| 📝 **编程练习驱动** | 每章 4-6 道编程题，参考解答可折叠（`LLM.toggleSolution`） |
| 📐 **KaTeX 数学渲染** | 内联 + 块级公式，渲染失败红色降级显示 LaTeX 源码 |
| 🔍 **章节搜索** | 侧边栏按章节标题/描述实时过滤 |
| 📑 **自动目录生成** | JS 读取 `section.card` 生成 TOC，scroll 高亮当前小节 |
| 📊 **阅读进度条** | 顶部 3px 渐变，GPU 合成（`transform: scaleX` + rAF 节流） |
| 📋 **代码复制** | Clipboard API + `execCommand` HTTP 回退，📋→✓ 反馈 |
| ⌨️ **键盘导航** | ← → 切换章节，Esc 关闭侧边栏 |
| 📱 **响应式** | 桌面 / iPad Pro / 手机三级断点（960/640px），触控 ≥44px |
| 🔤 **可调字号** | 小(14px) / 中(16px) / 大(18px)，localStorage 持久化 |
| 🖼️ **11 张 SVG 图表** | CSS filter 暗色适配（`invert + hue-rotate`） |
| 🏷️ **矢量 favicon** | SVG/PNG/ICO + apple-touch-icon (ComfyUI + FLUX.1-dev 生成) |

## 延伸阅读

**基础论文：**
- Vaswani et al. (2017) — [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- Radford et al. (2019) — [Language Models are Unsupervised Multitask Learners (GPT-2)](https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)
- Hoffmann et al. (2022) — [Training Compute-Optimal Large Language Models (Chinchilla)](https://arxiv.org/abs/2203.15556)

**DeepSeek 系列：**
- DeepSeek-V2 — [MLA + DeepSeekMoE](https://arxiv.org/abs/2405.04434) · V3 — [FP8 + MTP + Aux-Loss-Free](https://arxiv.org/abs/2412.19437) · V3.2 — [DSA 稀疏注意力](https://api-docs.deepseek.com/news/news250929) · R1 — [GRPO 推理涌现 (Nature 2025)](https://www.nature.com/articles/s41586-025-09422-z) · V4 — [CSA+HCA + mHC + Muon](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)

**动手实践：**
- Andrej Karpathy — [Neural Networks: Zero to Hero](https://www.youtube.com/playlist?list=PLAqhIrjkxBUWIvTOCzB7XwZBt03h4H3kW) · [nanoGPT](https://github.com/karpathy/nanoGPT)
- Sebastian Raschka — [Build a Large Language Model (From Scratch)](https://www.manning.com/books/build-a-large-language-model-from-scratch)
- 南京大学 — [LLM 从零到一实现之路](https://github.com/NJUDeepEngine/llm-course-lecture)

**推理与部署：**
- Kwon et al. (2023) — [vLLM: Efficient Memory Management for Large Language Model Serving](https://arxiv.org/abs/2309.06180)
- Tillet et al. (2019) — [Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations](https://dl.acm.org/doi/10.1145/3315508.3329973)
- Dao et al. (2022) — [FlashAttention: Fast and Memory-Efficient Exact Attention](https://arxiv.org/abs/2205.14135)
- Frantar et al. (2023) — [GPTQ: Accurate Post-Training Quantization for GPT](https://arxiv.org/abs/2210.17323)

**对齐与微调：**
- Hu et al. (2021) — [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
- Rafailov et al. (2023) — [Direct Preference Optimization (DPO)](https://arxiv.org/abs/2305.18290)
- Ouyang et al. (2022) — [Training Language Models to Follow Instructions (InstructGPT)](https://arxiv.org/abs/2203.02155)
