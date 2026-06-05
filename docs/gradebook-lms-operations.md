# Gradebook and LMS Operations Guide

本指南用于把 LMS / Gradescope、成绩册、late-day 账本、成绩发布和 regrade request 串成可审计流程。它补充 [课程 Syllabus](syllabus.md)、[Course Calendar and Deadline Ledger](course-calendar-deadline-ledger.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md)、[Grading Calibration Guide](grading-calibration.md)、内部 `grading-drift-audit-ledger.md`、内部 `grading-anchor-sample-feedback-pack.md`、[课程政策](course-policies.md)、[Course Staff and Office Hours Directory](course-staff-office-hours-directory.md)、[Learning Analytics and Remediation Plan](learning-analytics-remediation-plan.md) 和 [Academic Integrity Case Process](academic-integrity-case-process.md)。

目标不是规定某个学校必须使用某个平台，而是确保正式开课时任何 Canvas、Moodle、Blackboard、Gradescope 或自建 LMS 都能保留同等证据：每个分数来自哪份提交、哪个 rubric 项、哪个 late-day 规则、哪个复核决定。

## Gradebook Schema

成绩册至少保留以下列。若 LMS 不支持全部字段，应导出 CSV 或表格由 course manager 保管。

| column_id | 类型 | 用途 |
|-----------|------|------|
| student_id | private | 学校学号或 LMS ID，不在公开榜单出现 |
| student_display_name | private | 成绩核对使用；公开反馈中应脱敏 |
| enrollment_status | public-safe | enrolled、credit/no-credit、auditor、withdrawn |
| assignment_id | public-safe | `ch01_bpe`、`project_proposal`、`final_report` 等 |
| grade_category | public-safe | programming、written、quiz、participation、project |
| raw_score | private | autograder 或人工 rubric 原始分 |
| max_score | public-safe | 该项满分 |
| normalized_score | private | 归一化到课程权重前的百分比 |
| weight_percent | public-safe | syllabus 中该项权重 |
| weighted_points | private | `normalized_score * weight_percent` |
| submission_timestamp | private | LMS 原始提交时间和时区 |
| due_timestamp | public-safe | 来自 deadline ledger 的截止时间 |
| late_days_used | private | 本项消耗 late day 数 |
| late_penalty | private | late-day 用尽后的扣分 |
| extension_reason_code | private | accommodation、illness、platform_outage、instructor_exception |
| grader_id | private | 批改人或 autograder job id |
| rubric_version | public-safe | 与发布时 rubric 对齐的版本 |
| release_batch | private | 本次成绩发布批次 |
| regrade_status | private | none、requested、in_review、resolved、escalated |
| regrade_decision_id | private | 复核决定记录 ID |
| integrity_hold | private | 是否因学术诚信或 hidden-test leakage 暂缓发布 |
| student_visible_feedback | public-safe | 可给学生看的类别级反馈摘要 |

## Weight Reconciliation

成绩册权重必须能回推到 syllabus。每次成绩发布前执行以下检查：

| 检查 | 通过标准 |
|------|----------|
| category sum | 编程作业、书面题、capstone、participation 等大类合计为 100% |
| item mapping | 每个 `assignment_id` 属于且只属于一个 grade_category |
| max score | `raw_score <= max_score`，异常值有人工记录 |
| weighted total | 每个学生的 `weighted_points` 合计可复算 |
| late-day application | late-day 消耗和 penalty 与 deadline ledger 一致 |
| missing submission | 缺交、延期、平台故障和人工豁免有 reason code |
| hold visibility | integrity hold、OAE/accommodation 和私人困难不在公开反馈中泄露 |

建议在每次发布前抽查 5 名学生，手算一个 assignment、一个 written item、一个 late-day item 和一个 project milestone，确认 LMS 导出的总分能复算。

## Late-Day Ledger

late-day 账本应独立于单个作业页面，避免学生团队项目、延期和平台故障互相覆盖。

| 字段 | 要求 |
|------|------|
| student_id | 只在私密成绩册中保存 |
| late_days_initial | 开课时发放数量 |
| late_days_used_total | 截至当前批次累计使用 |
| late_days_remaining | 自动计算，不能为负；超出部分进入 penalty |
| assignment_id | 消耗 late day 的具体项目 |
| days_charged | 本项消耗数量 |
| pooled_team_days | final report 是否按团队规则池化 |
| exception_code | approved extension、platform outage 或 instructor exception |
| audit_note | 只写必要事实，不写健康、身份或家庭细节 |

项目团队作业必须区分个人 late days 和团队 pooled days。若团队报告允许 team pooling / pooled late days，成绩册需记录每名成员贡献的 late-day 数，避免把一个学生的便利安排暴露给队友。

## Grade Release Checklist

成绩发布前，course manager、Head TA 或 instructor 至少完成：

1. 确认 [Course Calendar and Deadline Ledger](course-calendar-deadline-ledger.md) 中 release、due、late-day 和 regrade window 没有冲突。
2. 确认 autograder job、hidden-test category feedback、manual rubric、written feedback 和 grading anchor sample feedback 已归档。
3. 确认 `rubric_version` 与学生发布的 handout 一致；若 rubric 有变更，公告中写明原因和影响范围。
4. 确认所有 extension、platform outage、integrity hold 和 regrade carry-over 已从公开统计中脱敏。
5. 抽查权重复算和 late-day ledger。
6. 准备学生可见 release note。

成绩发布说明至少包含：

| 字段 | 说明 |
|------|------|
| release_batch | 批次名和发布时间 |
| covered_items | 本次发布的 assignment 或 project milestone |
| grading_basis | public tests、hidden categories、written rubric、manual review |
| common_issues | 常见失败类别，不泄露隐藏输入 |
| late_day_policy | 本批次如何扣 late day 或 penalty |
| regrade_open_at | 复核开始时间 |
| regrade_close_at | 复核截止时间 |
| contact_path | LMS regrade request、private message 或 course email |

## Regrade Workflow

regrade request 必须保留原始提交和原始反馈，不能用修改后的代码或报告替代。

| 状态 | 触发 | 处理人 | 学生可见说明 |
|------|------|--------|--------------|
| requested | 学生在窗口内提交具体 rubric 项和理由 | Head TA triage | 已收到，等待分类 |
| in_review | 可能存在测试、rubric 或人工判断问题 | 原 grader 以外的 TA 或 Head TA | 正在复查指定项 |
| resolved | 分数维持、上调或下调 | Head TA | 给出类别级理由 |
| escalated | 涉及政策、诚信、便利安排或持续争议 | Instructor | 转入 instructor review |
| closed_late | 超出窗口且无批准延期 | Course Manager | 说明窗口规则 |

复核记录字段：

| field | 要求 |
|-------|------|
| regrade_decision_id | 唯一 ID |
| original_score | 复核前分数 |
| revised_score | 复核后分数 |
| affected_rubric_items | 具体 rubric 项 |
| decision_reason | 简短、可给学生看的理由 |
| reviewer_id | 处理人 |
| resolved_at | 完成时间 |
| calibration_update_needed | 是否需要更新 grading calibration |
| affected_students | 若是系统性错误，列出需要批量修正范围 |

若复核暴露 hidden test bug、rubric ambiguity 或 LMS 导入错误，应批量复核受影响学生，并在 release note 中说明类别和影响范围。

## Privacy and Access Control

成绩册访问应遵循 minimum privileges / 最小权限原则。

| 角色 | 可访问 | 不可访问 |
|------|--------|----------|
| Instructor | 全部成绩、复核、诚信和便利安排摘要 | 不需要的健康或家庭细节 |
| Course Manager | LMS 配置、deadline、成绩发布、late-day ledger | reference solution、hidden-test source |
| Head TA | rubric、批改记录、复核、类别级 hidden feedback | 无关学生的便利安排细节 |
| Grader / Discussion TA | 被分配项目的提交、rubric 和反馈 | 全班总成绩、私人复核或诚信档案 |
| Project Mentor | 项目范围、milestone feedback、公开报告草稿 | 章节作业成绩、hidden tests、私人便利安排 |

学生可见反馈只包含自己的分数、自己的类别级反馈、自己的 late-day 使用和复核入口。公开讨论区不得贴个人分数、相似性报告、hidden-test 结果、健康/身份/家庭信息或便利安排细节。

## Operations Log Hooks

每次成绩发布或大规模复核后，把以下摘要写入 [Course Operations and Improvement Log](course-operations-log.md) 或等价内部记录：

| 记录 | 用途 |
|------|------|
| release_batch | 追踪成绩发布日期和覆盖项目 |
| grade_distribution_summary | 只记录聚合分布，不暴露个人 |
| hidden_failure_categories | 更新 recitation、FAQ 和 hidden-test 设计 |
| regrade_count | 监控 rubric 清晰度 |
| late_day_usage_summary | 检查工作量和 deadline 设计 |
| calibration_updates | 连接 [Grading Calibration Guide](grading-calibration.md) 和内部 `grading-anchor-sample-feedback-pack.md` |
| policy_exceptions | 供 instructor 复盘，不进学生公开材料 |

## Staff Checklist

- syllabus、assignment submission guide、course policies、grading calibration 和 staff directory 均链接本指南。
- 学生站点发布包包含本指南，但不包含 `grading-calibration.md`、`autograder-hidden-tests.md`、`staff-runbook.md` 或 `instructor-solution-guide.md`。
- 每次成绩发布都能从 gradebook column 回推到 rubric、deadline ledger、late-day ledger 和 regrade workflow。
- `.venv/bin/python verify_course.py` 通过。

## 发布前 Checklist

- 真实开课前替换 LMS 名称、course email、regrade window 和 late-day 数量。
- 若学校有正式隐私、FERPA、GDPR 或本地数据保护要求，按学校政策更新 access control。
- 若采用 Gradescope，确认导出 CSV 包含 `submission_timestamp`、rubric item score 和 regrade status。
- 若采用 Canvas/Moodle/Blackboard，确认 weighted gradebook 与 syllabus 权重一致。
