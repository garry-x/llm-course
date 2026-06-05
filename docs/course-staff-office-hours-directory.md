# Course Staff and Office Hours Directory

本目录用于把教师、课程经理、助教、项目 mentor、Office Hours 和联系渠道整理成学生可见的支持入口。它补充 [课程 Syllabus](syllabus.md)、[Course Communication and Announcement Policy](course-communication-policy.md)、[Discussion Section and Office Hours Guide](discussion-office-hours-guide.md)、[Participation and Feedback Guide](participation-feedback-guide.md)、[Project Team and Mentor Policy](project-team-mentor-policy.md)、[Staff Assistance and Code Review Boundary Policy](staff-assistance-code-review-policy.md)、[Gradebook and LMS Operations Guide](gradebook-lms-operations.md) 和内部 [Course Staff Runbook](staff-runbook.md)。

## 学生可见 Staff 角色

| 角色 | 学生应联系的事项 | 不适合处理 |
|------|------------------|------------|
| Instructor | 课程目标、政策解释、最终项目范围、学术诚信、复核升级 | 普通环境安装或公开测试 debug |
| Course Manager | 日程、公告、LMS / Gradescope、gradebook export、late-day ledger、lecture media、提交入口、课程邮箱分流 | 独立裁决成绩或政策争议 |
| Head TA | 作业口径、讨论课质量、评分校准入口、regrade triage、Office Hours 覆盖 | 私自修改 rubric、公开隐藏测试或单独改 gradebook 权重 |
| Discussion TA | shape drill、公开测试 debug、章节概念、作业提问、讨论课材料 | 代写核心函数或查看其他学生代码 |
| Project Mentor | proposal、milestone、实验风险、复现证据、数据/伦理问题 | 替团队完成实验设计、代码或报告 |
| Autograder Contact | 提交格式、公开测试运行、环境故障、类别级隐藏测试反馈 | 透露 hidden tests、`reference_solution.py` 或评分脚本 |

每轮正式开课前，课程组应在 LMS 或学生站点填入真实姓名、时区、公开联系方式和 Office Hours 链接。公开目录只展示学生需要的信息；staff-only 权限、隐藏测试负责人和评分校准记录不进入学生发布包。

## 联系渠道

| 渠道 | 用途 | 响应目标 | 隐私边界 |
|------|------|----------|----------|
| Public forum | 概念、公开测试、环境、阅读材料、公开项目范围 | 1-2 个工作日 | 不贴完整答案、hidden tests、个人信息或其他学生代码 |
| Private message | 便利安排、迟交说明、成绩争议、团队贡献、学术诚信沟通 | 2 个工作日 | 只在必要 staff 范围内共享 |
| Course email | 紧急个人情况、无法进入 LMS、外部询问、正式升级 | 2 个工作日；紧急事项按学校流程 | 不作为普通作业 debug 的首选 |
| Office Hours queue | shape 推导、最小复现、项目 scope、失败定位 | 按排班处理 | 队列中只写问题摘要，不写敏感信息 |
| LMS / Gradescope | 正式提交、成绩、regrade request、发布包、个人 late-day 记录 | 按平台规则 | 不在平台公开区贴私密材料 |

影响评分、截止时间、提交入口或政策的答复，必须同步为正式公告或文档更新；单条私信不能改变全班规则。

## Office Hours 类型

| 类型 | 适合问题 | 学生准备 |
|------|----------|----------|
| Concept / math hours | RoPE、attention scaling、LayerNorm、DPO/GRPO、KV cache 公式 | 写出当前推导、卡住的等式和希望验证的假设 |
| Coding / debugging hours | starter API、公开测试、shape、mask、dtype、device、seed | 提供命令、cwd、Python/PyTorch 版本、第一个失败测试和最小样例 |
| Project mentor hours | proposal、milestone、SLO、训练预算、数据/伦理、报告结构 | 提供项目目标、当前 evidence、风险登记和下一步决策 |
| Regrade support hours | rubric 理解、复核材料准备、类别级反馈解释 | 带具体评分项、原始提交和复核理由 |
| Accessibility / private support | 便利安排、健康或安全影响、团队冲突 | 通过私密渠道预约，不在公开队列写细节 |

Office Hours 不能替代独立完成作业。staff 可以讲定位路径、最小反例、shape 推导、rubric 解释和公开文档链接，但不能写核心实现、查看隐藏测试、共享参考解或替学生完成报告。

作业代码查看边界按 [Staff Assistance and Code Review Boundary Policy](staff-assistance-code-review-policy.md) 执行：Ch01-Ch02 可在 office hours 中采用 limited_code_view，有限查看局部代码片段帮助学生建立调试方法；Ch03-Ch11 和 final project 默认转为 pseudocode_review、shape、最小复现、日志和 artifact_review。

## 排班与覆盖要求

| 周期 | 最低覆盖 | 备注 |
|------|----------|------|
| 每周 | 至少 1 次 concept / math hours 和 1 次 coding / debugging hours | 与本周章节和作业截止匹配 |
| 作业截止前 48 小时 | 增加短时段 office hours 或 forum watch | 不延长 deadline，除非正式公告 |
| Project 周 | 增加 mentor hours，覆盖训练、推理、评测、数据/伦理 | 默认项目可用 group clinic |
| Week 1-2 | Python / PyTorch review support | 连接 [Python and PyTorch Review Session](python-pytorch-review-session.md) |
| Week 8-10 | final project、guest seminar、poster/report support | 连接 [Guest Speaker and External Seminar Policy](guest-speaker-seminar-policy.md) 和 showcase 流程 |

排班应写入 course calendar、LMS 或课程站点，并说明时区、地点/链接、是否支持远程、是否需要预约和队列入口。

## Queue Policy

| 字段 | 学生填写 |
|------|----------|
| course_item | 章节、作业、项目或政策问题 |
| question_type | concept、coding、project、regrade、private routing |
| command_or_context | 运行命令、阅读位置、rubric 项或项目 milestone |
| first_failure | 第一个 traceback、assert message、shape mismatch 或具体困惑 |
| minimal_reproduction | 最小输入、tensor shape、短日志或报告段落 |
| requested_help | 希望 staff 判断、解释或确认的具体问题 |

队列只记录问题摘要。健康、身份、安全、便利安排、团队冲突、成绩争议和学术诚信相关内容应转私密消息或课程邮箱。

## Escalation Matrix

| 情况 | 初始联系人 | 升级到 | 学生可期待 |
|------|------------|--------|------------|
| 公开测试或环境大面积失败 | Discussion TA 或 Autograder Contact | Head TA + Course Manager | 公告、workaround、补测窗口或测试修复说明 |
| rubric 或成绩复核争议 | Head TA | Instructor | regrade decision 和必要的类别级解释 |
| hidden test leakage 或诚信疑似 | Private channel | Instructor | 按 [Academic Integrity Case Process](academic-integrity-case-process.md) 私密处理 |
| 项目 scope 或 mentor 分歧 | Project Mentor | Instructor | scope decision、风险调整或补充问答 |
| 学术便利或个人困难 | Private message 或 Course email | Instructor / school support | 必要范围内共享和可执行安排 |
| 内容事实错误 | Public forum 或 Course email | Instructor + source owner | 勘误、材料更新和验证命令 |

## Public Directory Template

```text
Course offering:
Timezone:
Primary public forum:
Private contact:
Course email:
LMS / Gradescope:

Instructor:
Course Manager:
Head TA:
Discussion TAs:
Project Mentors:
Autograder Contact:

Office Hours:
- Concept / math:
- Coding / debugging:
- Project mentor:
- Regrade support:
- Private support routing:
```

## Staff Handoff Fields

这些字段供课程团队每轮开课前填充并复核；学生目录只公开必要部分。

| field | 内容 |
|-------|------|
| staff_name | 公开显示姓名或角色名 |
| role | Instructor、Course Manager、Head TA、Discussion TA、Project Mentor、Autograder Contact |
| contact_scope | public forum、private message、course email、LMS |
| office_hours_type | concept、coding、project、regrade、private routing |
| timezone | staff 所在时区或课程统一时区 |
| coverage_weeks | 覆盖周次或项目阶段 |
| backup_contact | staff 不可用时的备份角色 |
| escalation_owner | 需要升级时的负责人 |
| privacy_notes | 是否处理便利安排、成绩争议、项目冲突或学术诚信 |

## Staff Checklist

- 开课前公开 instructor、course manager、Head TA、讨论课 TA 或等价支持角色。
- 公开渠道、私密渠道、课程邮箱、LMS / Gradescope 和 Office Hours queue 均有用途说明。
- 每周 office hours 覆盖 concept / math、coding / debugging；项目周覆盖 project mentor support。
- 队列模板要求 command、cwd、traceback、shape 或 minimal reproduction。
- 私密事项有明确转接路径，不出现在公开队列或公开讨论区。
- 影响评分、deadline、policy 或测试口径的答复同步为公告或文档更新。
- 每周把高频问题聚合到 [Course Operations and Improvement Log](course-operations-log.md)、FAQ 或 discussion guide。
- Staff assistance 若超出本政策边界，应记录 fairness_followup 并升级给 Head TA 或 Instructor。

## 发布前 Checklist

- syllabus、communication policy、discussion guide、project mentor policy 和 CS224N crosswalk 均链接本目录。
- 学生站点发布包包含本文件，但不包含 staff-only runbook、hidden tests、grading calibration 或 instructor solution。
- Office Hours 信息包含时区、访问方式、队列入口、远程/线下模式和私密路由。
- `.venv/bin/python verify_course.py` 通过。
