# Assessment Administration and Exam Integrity Policy

本政策用于管理 quiz、recap check、midterm checkpoint、final review quiz、makeup assessment 和阶段性评估的发布、执行、便利安排、诚信边界与成绩发布。它补充 [课程 Syllabus](syllabus.md)、[Assessment Blueprint and Coverage Matrix](assessment-blueprint-coverage-matrix.md)、[Assessment Item Analysis and Psychometrics Guide](assessment-item-analysis-psychometrics.md)、[Quiz and Checkpoint Guide](quiz-checkpoint-guide.md)、[Midterm and Final Review Pack](midterm-final-review-pack.md)、[Assessment Item Bank Ledger](assessment-item-bank-ledger.md)、[Course Calendar and Deadline Ledger](course-calendar-deadline-ledger.md)、[Gradebook and LMS Operations Guide](gradebook-lms-operations.md)、[Accessibility and Student Support Guide](accessibility-student-support.md)、[Academic Integrity Case Process](academic-integrity-case-process.md)、[Course Communication and Announcement Policy](course-communication-policy.md) 和 [Course Operations and Improvement Log](course-operations-log.md)。

本课程主要评分来自作业和项目；quiz / checkpoint 的目标是诊断能力、触发补救和校准教学节奏。若教师把某次 midterm checkpoint 或 final review quiz 计入成绩，必须在 syllabus、deadline ledger 和 LMS 中提前写明权重、允许材料、时间窗口、便利安排和复核窗口。

## Assessment Types

| assessment_type | 默认用途 | 是否可计分 | 管理要求 |
|-----------------|----------|------------|----------|
| lecture_quick_check | 课堂即时诊断 | 不建议单独计分 | 5-12 分钟；可口头或纸面完成 |
| recap_quiz | 讨论课复盘 | 可计入参与小分 | 使用题型池；保留通过率 |
| prerequisite_diagnostic | Week 0/1 先修诊断 | 完成/未完成 | 不排名；连接补救任务 |
| midterm_checkpoint | Ch01-Ch07 阶段能力检查 | 可计入书面/参与小分，不超过课程总评 5% | 有样卷、评分要点、补救映射和便利安排 |
| capstone_readiness_check | 项目前复现/评测准备 | 可计入 milestone | 检查项目证据，不替代最终报告 |
| final_review_quiz | 期末复习和风险诊断 | 不替代项目评分 | 可开卷讨论或短测 |
| makeup_assessment | 经批准的补测 | 与原 assessment 等价 | 覆盖同一能力目标，使用不同题面 |

## Scheduling and Announcement

每次正式计分 assessment 发布前，课程组必须公告：

| 字段 | 要求 |
|------|------|
| assessment_id | 例如 `midterm-checkpoint-2026-spring` |
| coverage | 章节、阅读、作业或项目范围 |
| weight_percent | 是否计分及权重 |
| release_at / start_at / due_at | 与 deadline ledger 一致，并写明 timezone |
| duration_minutes | 常规时长和便利安排后的时长处理原则 |
| allowed_materials | closed-book、one-page notes、open-book、calculator、local code 等 |
| delivery_mode | in-class、take-home、LMS quiz、oral check、remote proctored |
| submission_format | paper、LMS、PDF、Markdown、oral rubric |
| regrade_window | 与 gradebook/LMS 指南一致 |
| accommodation_path | 私密联系渠道和截止时间 |

口头说明、单条私信或 office-hour 答复不能单独改变 assessment 规则。任何窗口、材料或计分口径改变都必须按 [Course Communication and Announcement Policy](course-communication-policy.md) 发布公告，并同步 [Course Calendar and Deadline Ledger](course-calendar-deadline-ledger.md)。

## Allowed Materials Matrix

| 模式 | 允许 | 禁止 | 适用场景 |
|------|------|------|----------|
| closed-book | 空白纸、教师发放公式页 | 讲义、网页、AI 工具、同伴讨论 | 短时核心公式检查 |
| one-page notes | 一页个人手写或打印 notes | 联网搜索、代码运行、共享答案 | midterm checkpoint |
| open-book local | 课程章节、个人 notes、本地 starter/API 文档 | 论坛求助、AI 工具直接生成答案、他人提交 | take-home 诊断或 final review |
| coding check | 本地 `.venv`、公开 tests、starter 文件 | reference solution、hidden tests、网络下载 | capstone readiness 或 debug drill |
| oral check | 学生自己的提交和日志 | 代答、旁听提示、未披露 AI 生成推导 | 便利安排、复核或诚信澄清 |

若允许 AI 工具，必须在题面中说明可用范围和披露要求；若未明确允许，计分 assessment 默认不允许使用 AI 工具直接生成答案、代码或推导。

## Item Security and Rotation

题目安全的目标不是制造神秘感，而是保证评估测的是能力而不是提前背题。

| 项 | 规则 |
|----|------|
| item_bank_id | 每道正式题保留能力标签、使用日期、版本和来源边界 |
| learning_objective | 题目必须映射到章节、作业、reading recap 或 project rubric |
| variant_policy | 复用题型时替换数字、语料、日志片段或模型声明 |
| source_boundary | 涉及前沿模型或 benchmark 的题必须有来源等级和访问日期 |
| exposure_level | public_sample、practice_variant、active_assessment、retired |
| retirement_trigger | 泄题、公开答案流传、通过率异常高且无区分度、事实来源失效 |

正式 assessment 不应使用 hidden assignment tests、`reference_solution.py`、学生提交或私有评分脚本作为题面。样题可以公开，但 active assessment 的题面、rubric 细项和 grading notes 不应提前发布。

公开安全的题库元数据、exposure_level、variant_policy、retirement_trigger 和 makeup equivalence 规则见 [Assessment Item Bank Ledger](assessment-item-bank-ledger.md)。

## Proctoring and Identity

本课程允许按学校条件选择低负担方案。无论采用何种方式，都必须避免收集不必要的隐私信息。

| delivery_mode | 身份与诚信检查 | 隐私边界 |
|---------------|----------------|----------|
| in-class paper | 学校 ID、座位表、签名提交 | 不拍摄个人材料，除非学校政策要求 |
| LMS timed quiz | LMS 登录、时间窗口、提交日志 | 不公开 IP、设备或个人时间线 |
| take-home | honor statement、随机抽查口头解释 | 不要求持续监控 |
| remote oral check | 短时视频或音频核验 | 不录制或只按学校政策录制必要片段 |
| accessibility alternative | 私密安排、等价目标、必要 staff 知情 | 不向同伴披露安排原因 |

远程 assessment 不默认要求 intrusive proctoring。若学校要求远程监考，教师必须提前公告数据收集范围、保留时间、申诉渠道和替代方案。

## Accommodations and Makeup

便利安排和补测应改变访问方式，不改变核心学习目标。

| 情况 | 处理 |
|------|------|
| documented accommodation | 按 [Accessibility and Student Support Guide](accessibility-student-support.md) 调整时长、格式、辅助技术或提交窗口 |
| illness / emergency | 通过私密渠道申请 makeup assessment 或延期 |
| LMS outage | 对受影响学生统一补窗口，不消耗 late day |
| timezone conflict | 异步窗口或等价 oral check，保持题目安全 |
| team project conflict | 不把个人便利安排暴露给队友；项目贡献按事实记录 |

makeup assessment 必须覆盖同一能力目标，但题面、数字、语料或日志片段应不同。若原 assessment 已公开答案，补测必须使用新的 active variant。

## Integrity Incident Flow

若出现疑似泄题、异常相似答案、未披露 AI 工具、代考、共享题面或 hidden material 接触，按以下流程处理：

| 阶段 | 动作 | 学生权利 |
|------|------|----------|
| signal_triage | 收集 LMS 日志、答案相似性、时间线和题面暴露证据 | 不把 signal 当成结论 |
| private_notice | 私密通知学生说明关注点和可回应材料 | 学生可提交解释、草稿、notes 或运行记录 |
| manual_review | 至少两名 staff 对照 rubric、政策和证据复核 | 只共享必要信息 |
| grade_hold | 必要时暂缓发布相关分数 | 告知 hold 范围和预计时间 |
| resolution | no action、score adjustment、makeup、integrity referral 或 course-level remediation | 给出可理解的类别级理由 |

所有诚信个案按 [Academic Integrity Case Process](academic-integrity-case-process.md) 私密处理。公开公告只说明类别和课程层面的处理，不公布个人信息。

## Grading and Feedback Release

成绩发布应与 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md) 一致。

| release_field | 要求 |
|---------------|------|
| score_breakdown | 总分、题目或能力维度分 |
| common_misconceptions | 全班常见误区，不含个人信息 |
| rubric_version | 与 assessment 发布时版本一致 |
| regrade_open_at / regrade_close_at | 与 deadline ledger 一致 |
| makeup_status | 只对相关学生私密可见 |
| integrity_hold | 只对相关学生私密可见 |
| remediation_path | 低分模块对应补救任务 |

反馈应帮助学生改进，而不是泄露 active item bank。隐藏 rubrics、未公开变体和个案证据不进入公开材料。

## Post-Assessment Review

每次正式计分 assessment 后，课程组应记录聚合复盘：

| metric | 用途 |
|--------|------|
| participation_count | 判断覆盖率 |
| score_distribution | 识别题目过难、过易或区分度不足 |
| low_item_clusters | 安排 recap、office hours 或补救材料 |
| accommodation_count | 检查流程是否足够可访问 |
| makeup_count | 检查窗口设计和平台稳定性 |
| regrade_count | 检查 rubric 清晰度 |
| integrity_signal_count | 检查题目安全和政策说明 |
| item_retirement_decision | 更新题库状态 |

复盘摘要写入 [Course Operations and Improvement Log](course-operations-log.md)；若暴露材料错误或来源事实变化，同步更新 [Claim Audit Worksheet](claim-audit-worksheet.md) 和 [External Source Verification Guide](external-source-verification.md)。

## Staff Checklist

- syllabus、quiz/checkpoint guide、midterm/final review pack、deadline ledger、gradebook/LMS guide、accessibility guide 和 academic integrity process 均链接本政策。
- 每次计分 assessment 都有 `assessment_id`、coverage、allowed materials、duration、weight、delivery mode、regrade window 和 accommodation path。
- Active assessment 不使用 hidden tests、reference solution、学生提交或私有评分脚本。
- Makeup assessment 覆盖同一 learning objective，但使用不同题面或数据。
- 成绩发布和复核记录能回推到 rubric、gradebook、deadline ledger 和 operations log。

## 发布前 Checklist

- 学生站点发布包包含本文件。
- 本文件不包含 active item bank、hidden rubrics、reference solution、学生提交或私有监考记录。
- 若学校有正式考试政策、隐私政策或远程监考政策，开课前替换本政策中的可移植默认规则。
- `.venv/bin/python verify_course.py` 通过。
