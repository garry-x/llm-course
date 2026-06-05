# CS224N Current Benchmark Snapshot

本文件记录本课程对 Stanford CS224N 当前公开页面的逐项复核结果，用于补充 [CS224N Benchmark Crosswalk](cs224n-benchmark-crosswalk.md)。它不是复制 CS224N 的作业或政策，而是把可公开核验的高校课程结构转化为本课程的维护证据。

复核日期：2026-06-05
基准来源：https://web.stanford.edu/class/cs224n/
公开版本：Stanford / Winter 2026

## 当前公开页要点

| 维度 | CS224N Winter 2026 公开信息 | 本课程维护动作 |
|------|-----------------------------|----------------|
| 课程定位 | Natural Language Processing with Deep Learning，覆盖 neural networks for NLP 和 cutting-edge LLM research | 本课程定位为 LLM 深度学习与工程课程，保留经典 NLP/评测专题以避免只学 decoder-only 工程 |
| Instructors / course staff / TAs | 公开页列出 instructors、course staff、teaching assistants、office hours 和 contact channel | 本课程用 [Course Staff and Office Hours Directory](course-staff-office-hours-directory.md)、[Course Communication and Announcement Policy](course-communication-policy.md) 和 [Course Staff Runbook](staff-runbook.md) 区分学生可见 staff directory、Office Hours queue、private routing、escalation matrix 和内部执行手册 |
| Lecture videos | 当前课程录播面向 enrolled students 通过 Canvas/Panopto 发布；公开历史视频通过 YouTube playlist 提供，非 enrolled students 不能访问当前录播 | 本课程用 [Lecture Media Access Policy](lecture-media-access-policy.md) 区分 live stream、current lecture recording、public historical video、caption / transcript、隐私剪辑和 public learner 边界 |
| Schedule and deadlines | 公开 schedule 按日期列出 lecture materials、events 和 deadlines；coursework 区域集中说明 assignment deadlines、project deadlines、late days 和 regrade requests | 本课程用 [Course Calendar and Deadline Ledger](course-calendar-deadline-ledger.md) 统一 lecture、assignment、project、late day、regrade window、release freeze 和 deadline change announcement，并用 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md) 管理 gradebook schema、late-day ledger、release batch 和 regrade workflow |
| Quiz / checkpoint administration | CS224N 当前公开页主要评分来自 assignments、final project 和 participation，没有要求本课程复制独立考试结构 | 本课程保留 low-stakes quick check、midterm checkpoint 和 final review quiz；若计分，按 [Assessment Administration and Exam Integrity Policy](assessment-administration-policy.md) 管理 allowed materials、makeup assessment、item security、accommodation、integrity hold 和 regrade window |
| Lecture notes / slides | 公开 schedule 每讲链接 slides、notes、code 或 readings；课程说明 notes 通常在课后上传 | 本课程用 [Lecture Notes Index](lecture-notes-index.md)、[Lecture Slide Outline](lecture-slide-outline.md)、[Lecture Notes Quality and Review Standard](lecture-notes-quality-review.md) 和 [Course Materials Index](course-materials-index.md) 管理 L1-L20 notes、slides outline、review_record、source_boundary、correction workflow 和发布状态 |
| Python/PyTorch review sessions | 公开 schedule 列出 Week 1 Python Review Session 和 Week 2 PyTorch Tutorial Session | 本课程用 [Python and PyTorch Review Session](python-pytorch-review-session.md) 把环境 smoke test、Ch01 helper、Ch02 embedding、CE loss、autograd 和 debug drill 串成可执行 handout |
| 先修 | Python、NumPy/PyTorch、college calculus、linear algebra、probability/statistics、ML foundations | [Prerequisite Diagnostic](prerequisite-diagnostic.md)、[Python and PyTorch Review Session](python-pytorch-review-session.md)、[数学与 PyTorch 先修复习](math-prerequisites.md) 和 [ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md) 覆盖 Python、PyTorch、微积分、线代、概率统计、ML objectives、generalization、evaluation、反向传播和复现纪律 |
| 参考教材 | Speech and Language Processing、Eisenstein NLP、Goldberg neural NLP primer、Deep Learning、NLP with Transformers 等 | [逐周阅读清单与复盘 Handout](reading-list.md) 包含基础论文、教材和工程资源；外部来源由 [External Source Inventory](external-source-inventory.md) 分层 |
| 作业结构 | Assignments 48%；四个 weekly assignments；每个 assignment 同时包含 written questions 和 programming parts | 本课程拆成 11 个公开测试作业套件 + 书面题库，权重 35% 编程 + 20% 书面题，保留理论/代码双轨 |
| CS224N Assignment 1 | Introduction to word vectors | 本课程 Ch01-Ch02 覆盖 BPE、embedding、word vectors、RoPE，并有 `assignments/ch01_bpe/`、`assignments/ch02_embeddings/` |
| CS224N Assignment 2 | Neural network foundations、tensor derivatives、dependency parsing | 本课程用 Ch03-Ch05、[math-prerequisites.md](math-prerequisites.md) 和 `assignments/ch11_classic_nlp/` 覆盖 attention、norm、tensor shape、dependency parsing |
| CS224N Assignment 3 | Self-attention and Transformers | 本课程 Ch03-Ch06 覆盖 attention、MHA/GQA/MLA、Transformer block、GPT assembly 和 MoE |
| CS224N Assignment 4 | Large language model benchmarking and evaluation | 本课程 Ch08-Ch10、经典 NLP 评测专题和推理 capstone 覆盖 sampling、benchmark、RAG、SLO、capacity planning |
| Staff help boundary | 公开页说明 TAs may look at code for assignments 1 and 2, but not assignments 3 and 4；final project staff/mentor 提供 project advice，但不替学生完成项目 | 本课程用 [Staff Assistance and Code Review Boundary Policy](staff-assistance-code-review-policy.md) 固化 Ch01-Ch02 limited_code_view、Ch03-Ch11 pseudocode_review、final project artifact_review、rubric_explanation 和 fairness_followup |
| Final Project | Final Project 49%；proposal 8%、milestone 6%、poster 3%、report 32%；default GPT-2 或 custom project | 本课程设置训练工程 capstone + 推理工程 capstone；新增 [Default Final Project Guide](default-final-project-guide.md)，把 GPT-2 风格实现、下游生成/评测/服务任务、proposal、milestone、poster 和 report 串成默认最终项目路径 |
| Experimental rigor | CS224N final project 含 proposal、milestone、poster 和 report；项目 advice 和 mentor 机制用于让方法、实验、结果和局限在最终提交前可评审 | 本课程用 [Capstone Proposal and Milestone Guide](capstone-proposal-milestone.md) 和 [Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md) 要求 proposal/milestone/final report 逐步收敛 split_card、metric_card、uncertainty_record、claim_audit、bootstrap CI、seed sensitivity、single_seed_limit、significance claim gate 和 contamination/leakage gate，避免项目报告只展示单次好结果 |
| Archived project reports | 公开页列出往年 CS224N Reports，作为 archived project reports；同时提醒 assignments 会变化，不要做往年作业 | 本课程用 [Final Project Showcase and Archive Policy](final-project-showcase-archive-policy.md) 管理 public archive、consent、redaction、artifact manifest、archived label 和 staff-only grading packet |
| 项目团队与贡献 | 可单人或最多 3 人；报告需写贡献；可有 external collaborators，但必须声明 | [Capstone Project Gallery and Idea Bank](capstone-project-gallery.md) 和 [Data and Ethics Review](data-ethics-review.md) 要求团队贡献、外部代码/协作者、数据来源和残余风险披露 |
| 算力 | CS224N 公开页说明 teams receive compute credits | 本课程用 [Compute Resource and Cost Guide](compute-resource-guide.md) 明确 CPU baseline、GPU/API 可选额度、成本记录、失败重跑和 fallback |
| 后半段专题 | 公开 schedule 包含 Reasoning、Tokenization and Multilinguality、Interpretability、Social and Broader Impacts、Multimodality 和 Open Questions | 本课程用 Ch08-Ch10、[classic-nlp-handout.md](classic-nlp-handout.md)、[data-ethics-review.md](data-ethics-review.md)、[frontier-seminar-handout.md](frontier-seminar-handout.md) 和项目报告 rubric 覆盖 reasoning、tokenization、多模态、可解释性、社会影响和开放问题 |
| 参与 | Participation 3%；guest lecture、feedback surveys、Ed participation、karma point | 本课程用 [Participation and Feedback Guide](participation-feedback-guide.md) 和 [Guest Speaker and External Seminar Policy](guest-speaker-seminar-policy.md) 将阅读复盘、讨论区、Office Hours、guest lecture reflection、Q&A/source audit、反馈调查、互评和 karma-style 课程贡献合并为 10% |
| Late days | 6 late days；单个 assignment/proposal/milestone 最多 3 天；超额扣分；project report 可团队 pooling | 本课程当前采用更保守的 3 late days 草案；正式授课前教师需按本校政策在 [syllabus.md](syllabus.md) 中确认，并按 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md) 维护 late-day ledger、team pooling 和 exception code |
| Regrade | Gradescope 成绩发布后 3 天内复核，可能重评整个提交 | 本课程 [Grading Calibration Guide](grading-calibration.md)、[Gradebook and LMS Operations Guide](gradebook-lms-operations.md) 和 [syllabus.md](syllabus.md) 采用 7 天复核窗口草案，需按学校政策确认；复核状态、decision id 和批量修正需留痕 |
| Honor code / academic integrity | 公开页包含 honor code、AI tools policy、late/regrade 和课程支持边界 | 本课程用 [课程政策](course-policies.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md) 和 [Academic Integrity Case Process](academic-integrity-case-process.md) 覆盖协作边界、相似性检测解释、个案取证、student_response、grade_action 和隐私沟通 |
| AI tools policy | 允许把生成式 AI 当作 collaborator，但禁止直接索要/复制答案或让 AI 实质完成作业 | 本课程 [课程政策](course-policies.md) 和 [Academic Integrity Case Process](academic-integrity-case-process.md) 采用同类边界：允许学习和调试辅助，禁止代写、伪造日志、未披露使用或无法解释提交 |
| Accessibility / well-being | 公开页包含 documented disabilities、well-being、sexual violence support 等支持信息 | 本课程 [Accessibility and Student Support Guide](accessibility-student-support.md) 覆盖学术便利、隐私、支持渠道和公平评分边界；正式开课需替换为本校联系人 |

## 当前 Schedule 主题证据矩阵

本节只记录 2026-06-05 访问公开页时能直接观察到的 schedule 主题、tutorial/session 和 project/assignment 事件。它用于检查本课程是否覆盖 CS224N 当前公开结构中的教学意图，而不是要求逐字复制作业或讲义。

| CS224N schedule marker | 公开页观察 | 本课程覆盖位置 | 课程动作 |
|------------------------|------------|----------------|----------|
| History of NLP | Week 1 第一讲从 NLP 历史与语言理解/推理引入 | Ch01、[lecture-plan.md](lecture-plan.md)、[classic-nlp-deep-dive-module.md](classic-nlp-deep-dive-module.md) | 在开课导论中说明 LLM 工程主线与经典 NLP 问题的关系 |
| Word Vectors | Week 1 包含 Word Vectors，并建议 word2vec、negative sampling、GloVe 和 embedding evaluation 阅读 | Ch02、`assignments/ch02_embeddings/`、[reading-list.md](reading-list.md) Week 1 | 保留分布假说、类比推理经验边界和 embedding evaluation 复盘题 |
| Python Review Session | Week 1 单独列出 Python Review Session | [python-pytorch-review-session.md](python-pytorch-review-session.md)、[environment-reproducibility.md](environment-reproducibility.md) | 用 `.venv` smoke test、Ch01 helper drill 和 debug worksheet 降低先修不齐风险 |
| Backpropagation and Neural Network Basics | Week 2 覆盖 backprop、matrix calculus 和神经网络基础 | [math-prerequisites.md](math-prerequisites.md)、[ml-foundations-prerequisite-bridge.md](ml-foundations-prerequisite-bridge.md)、Ch03-Ch05 | 把 softmax/CE、shape、gradcheck 和 tensor derivative 写入书面题与作业测试 |
| PyTorch Tutorial Session | Week 2 单独列出 PyTorch Tutorial Session | [python-pytorch-review-session.md](python-pytorch-review-session.md)、`assignments/ch02_embeddings/` | 用 embedding、autograd、CE loss 和 shape contract 作为 tutorial evidence |
| Transformers | Week 3 进入 Transformer 主题 | Ch03-Ch06、`assignments/ch03_attention/` 到 `assignments/ch06_gpt/` | 从 attention、MHA/GQA/MLA、block 到 GPT assembly 分层验收 |
| Final Projects: Custom and Default | Week 3 公开 project advice，并在 coursework 中区分 default/custom final project | [default-final-project-guide.md](default-final-project-guide.md)、[capstone-proposal-milestone.md](capstone-proposal-milestone.md)、[project-team-mentor-policy.md](project-team-mentor-policy.md) | 提供默认项目任务包、自定义项目边界、mentor matching 和 proposal evidence |
| Pretraining (Scaling, Systems, Data) | Week 4 覆盖预训练、scaling、systems 和 data | Ch06-Ch07、训练工程 capstone、[reading-list.md](reading-list.md) Week 4-5 | 把 decoder-only 目标、数据/参数权衡、MoE、FP8 和分布式训练写入课程主线 |
| Post-training (RLHF, SFT, DPO) | Week 4 覆盖 post-training、RLHF、SFT 和 DPO | Ch09、`assignments/ch09_alignment/` | 用 SFT loss masking、LoRA、DPO 和 GRPO 优势估计作为可测试实现 |
| Efficient Adaptation (Prompting + PEFT) | Week 5 覆盖 prompting 和 PEFT | Ch09、[reading-list.md](reading-list.md) Week 7 | 将 LoRA、prompting 边界和 reference model 条件写入推导与测试 |
| Agents, Tool Use, and RAG | Week 5 覆盖 agents、tool use 和 RAG | Ch10、推理工程 capstone、[inference-engineer-curriculum.md](inference-engineer-curriculum.md) | 用 RAG 检索、SLO、服务化 API、压测和失败案例替代只讲概念 |
| Hugging Face Transformers Tutorial Session | Week 5 额外列出 Hugging Face Transformers Tutorial Session | [reading-list.md](reading-list.md)、[environment-reproducibility.md](environment-reproducibility.md) | 本课程把 HF Transformers 作为工程阅读和可选 demo，不作为从零实现作业的前提 |
| Benchmarking and Evaluation | Week 6 单独安排 Benchmarking and Evaluation | Ch08-Ch10、[experimental-rigor-evaluation-statistics.md](experimental-rigor-evaluation-statistics.md)、[nlp-evaluation-coverage.md](nlp-evaluation-coverage.md) | 要求 split/metric/uncertainty/claim gate，防止 benchmark 数字无条件外推 |
| Reasoning 1 / Reasoning 2 | Week 6-7 连续安排 reasoning 主题 | Ch08-Ch09、[frontier-seminar-handout.md](frontier-seminar-handout.md)、[frontier-source-audit.md](frontier-source-audit.md) | 区分 CoT/self-consistency/verifier/test-time compute/RL 的证据边界 |
| Tokenization and Multilinguality | Week 7 guest lecture 主题包含 tokenization and multilinguality | Ch01、[frontier-seminar-handout.md](frontier-seminar-handout.md)、[data-ethics-review.md](data-ethics-review.md) | 将 tokenization fairness、多语种成本和 BPE failure modes 纳入 seminar 复盘 |
| Interpretability | Week 8 guest lecture 主题包含 interpretability | Ch03、Ch05、[frontier-seminar-handout.md](frontier-seminar-handout.md) | 要求 attention/FFN 诊断不能直接等同解释，必须给干预或反事实证据 |
| Social and Broader Impacts of NLP | Week 8 包含 social and broader impacts / risks | [data-ethics-review.md](data-ethics-review.md)、[frontier-seminar-handout.md](frontier-seminar-handout.md)、[course-policies.md](course-policies.md) | 把 privacy、bias、copyright、misuse、benchmark contamination 写成项目风险登记 |
| Multimodality | Week 9 guest lecture 主题包含 multimodality | Ch10、[frontier-seminar-handout.md](frontier-seminar-handout.md) | 覆盖 image encoder、projection、multimodal failure cases 和评测维度 |
| Tinker and LoRA Without Regret | Week 9 guest lecture 主题连接 LoRA / adaptation | Ch09、[reading-list.md](reading-list.md) Week 7 | 作为 PEFT / LoRA discussion 补充，不替代本课程从零实现 LoRA |
| Open Questions in NLP 2026 | Week 10 以 open questions 收束 | [frontier-seminar-handout.md](frontier-seminar-handout.md)、[course-operations-log.md](course-operations-log.md) | 要求学生把开放问题改写成可评测假设、最小实验和失败判据 |
| Assignment 1-4 release/due events | schedule 按周列出 assignment out/due 事件 | [course-calendar-deadline-ledger.md](course-calendar-deadline-ledger.md)、[assignment-handout-pack.md](assignment-handout-pack.md) | 本课程用 11 个小作业替代 4 个大作业，但保留 release/due/hidden test/regrade ledger |
| Project proposal, milestone, report, poster session | schedule 列出 proposal、milestone、final report 和 poster session 相关事件 | [capstone-proposal-milestone.md](capstone-proposal-milestone.md)、[presentation-peer-review.md](presentation-peer-review.md)、[final-project-showcase-archive-policy.md](final-project-showcase-archive-policy.md) | 每个项目阶段都有 split/metric/uncertainty/claim evidence，展示和公开归档需 consent/redaction |

## 差异解释

| 差异 | 本课程选择 | 理由 | 维护要求 |
|------|------------|------|----------|
| 权重不是 48/49/3 | 本课程采用 35/20/15/20/10 | 本课程把作业拆成更多小型公开测试，并把训练/推理工程作为两个 capstone | 每轮开课前确认工作量是否与学分匹配 |
| 项目不是单一 final project | 训练工程和推理工程分开评分，并提供默认最终项目任务包 | LLM 工程课程需要同时验证训练复现、推理服务、评测和成本规划；默认任务包用于保证没有自定义项目的学生仍有统一下游任务证据 | 项目报告 rubric 必须同时检查质量、成本、复现和失败案例 |
| 经典 NLP 不设独立正文章节 | 作为 Week 8 专题和 Ch11 作业覆盖 | 主线聚焦 decoder-only LLM，但保留 CS224N 核心的 dependency parsing、seq2seq、BERT 和 evaluation | 若课程扩展到 12 周，应把 Week 8 拆成两周 |
| Late days / regrade / checkpoint 窗口不同 | 保留本课程草案，不直接采用 Stanford 数字 | 学校政策和教学周期可能不同；本课程额外使用 low-stakes checkpoint 作诊断 | 正式授课前教师必须替换为本校正式规则，并确认 assessment administration policy |
| 外部平台不同 | 不写死 Canvas、Ed、Gradescope、Stanford OAE/CAPS | 仓库是可移植课程模板 | staff runbook 和 syllabus 需填入真实 LMS、讨论区、支持渠道 |

## 发布前 Checklist

- 本文件的复核日期不应早于本轮课程发布日期。
- 每轮开课前运行 `.venv/bin/python scripts/verify_cs224n_snapshot.py --json-out cs224n-snapshot-2026-06-05.json` 这类带日期的命令，将 pass manifest 归档到课程运行记录。
- [CS224N Benchmark Crosswalk](cs224n-benchmark-crosswalk.md) 仍需覆盖 logistics、prerequisites、reference texts、schedule、assignments、staff assistance/code review boundaries、quiz/checkpoint administration、final project、participation、office hours、late/regrade、honor code、accessibility 和 course updates。
- 若 CS224N 公开页的 assignment/project 权重或 policy 变化，本文件和 [university-course-quality-audit.md](university-course-quality-audit.md) 必须同步更新。
- 若当前 schedule 新增或删除 tutorial、guest lecture、assignment/project event，本文件的“当前 Schedule 主题证据矩阵”和 [Frontier Seminar Handout](frontier-seminar-handout.md) 必须同步更新。
- 若本课程正式采用学校 LMS、Gradescope、Ed/Discourse、云算力平台或学生支持渠道，应把仓库中的可移植模板描述替换为真实链接和负责人。
- 项目报告中的显著性、稳健性、速度、安全和泛化 claim 必须按 [Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md) 复核。
