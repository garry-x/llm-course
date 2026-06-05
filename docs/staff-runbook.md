# Course Staff Runbook

课堂观察、期中反馈 response memo、期末课程评估和下一轮改进任务按 [Teaching Observation and Course Evaluation Dossier](teaching-observation-course-evaluation.md) 执行。

本手册用于教师、课程经理和助教在真实开课时统一执行流程。它补充 [课程 Syllabus](syllabus.md)、[Course Communication and Announcement Policy](course-communication-policy.md)、[Student FAQ and Troubleshooting Guide](student-faq-troubleshooting.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md)、[Discussion Section and Office Hours Guide](discussion-office-hours-guide.md)、[Participation and Feedback Guide](participation-feedback-guide.md)、[Learning Analytics and Remediation Plan](learning-analytics-remediation-plan.md)、[TA Training and Certification Dossier](ta-training-certification.md)、[Grading Calibration Guide](grading-calibration.md)、[Grading Drift Audit Ledger](grading-drift-audit-ledger.md)、[Compute Resource and Cost Guide](compute-resource-guide.md)、[Accessibility and Student Support Guide](accessibility-student-support.md) 和 [Course Operations and Improvement Log](course-operations-log.md)。

## 角色与职责

| 角色 | 主要职责 | 不应承担 |
|------|----------|----------|
| 主讲教师 | 课程目标、内容准确性、评分政策、学术诚信、最终项目风险裁决 | 日常重复答疑的全部负担 |
| 课程经理 | 日程、公告、LMS/Gradescope、会议记录、运行日志、跨助教协调 | 替代教师做政策裁决 |
| Head TA | 助教排班、讨论课质量、评分校准、复核初筛、隐藏测试协调 | 独自修改 rubric 而不记录 |
| Discussion TA | 带讨论课、维护 drill、汇总 exit ticket、高频问题反馈 | 代写作业核心实现 |
| Project Mentor | 审查 proposal/milestone、指出项目风险、检查复现证据 | 替学生设计完整实验或写代码 |
| Autograder Owner | 维护公开/隐藏测试、容差、日志和评分映射 | 向学生公开隐藏输入 |

每轮开课前应把真实姓名、联系方式、Office Hours 时间和职责填入课程内部表格；公开页面只公布学生需要的联系渠道。

## 开课前 Checklist

| 时间 | 检查项 | 负责人 |
|------|--------|--------|
| T-4 周 | 确认 syllabus、评分权重、late day、复核窗口、AI 工具政策 | 主讲教师 |
| T-3 周 | 跑通 `.venv/bin/python verify_course.py --capstone --training` | 课程经理 |
| T-3 周 | 按 [Classroom Demo Runbook](demo-runbook.md) 完成课堂 demo dry run | Discussion TA |
| T-3 周 | 按 [Compute Resource and Cost Guide](compute-resource-guide.md) 确认 CPU baseline、GPU/API 额度和成本记录模板 | 课程经理 |
| T-3 周 | 审查作业 README、starter、reference、公开测试和隐藏测试类别 | Head TA |
| T-2 周 | 配置 LMS/Gradescope、讨论区、课程邮箱、仓库权限 | 课程经理 |
| T-2 周 | 完成 [TA Training and Certification Dossier](ta-training-certification.md) 中对应角色的 training/certification | Head TA |
| T-2 周 | 完成助教评分校准样例和讨论课排班 | Head TA |
| T-1 周 | 发布 prerequisite diagnostic、环境安装说明和 Week 1 阅读 | 课程经理 |
| T-1 周 | 检查可及性流程和私密求助渠道 | 主讲教师 |

开课前必须保留一次 dry run 记录，包括命令输出、失败项、修复人和修复日期。

## 权限与工具

| 工具 | 必需配置 |
|------|----------|
| LMS / Canvas | syllabus、公告、作业入口、成绩列、复核窗口 |
| Gradescope 或等价系统 | autograder image、timeout、公开/隐藏分项、late day |
| 讨论区 | 公告、作业问题、项目问题、政策问题、私密提问 |
| 课程邮箱 | 个人情况、便利安排、复核升级、学术诚信 |
| 代码仓库 | 教师/助教私有权限、公开材料分支、隐藏测试隔离 |
| 会议记录 | 每周 staff meeting、评分校准、项目风险、运行日志 |

隐藏测试、参考解、复核记录和学生个人情况不应放在公开仓库或公开讨论区。

## 公告模板

### 每周开场公告

```text
Week:
本周主题：
必读材料：
作业/项目截止：
讨论课安排：
Office Hours：
常见问题：
需要私下联系课程组的事项：
```

### 作业发布公告

```text
Assignment:
发布时间：
截止时间：
本地运行命令：
提交文件：
评分组成：
公开测试说明：
隐藏测试类别：
late day 规则：
复核窗口：
```

### 成绩发布公告

```text
Assignment:
成绩已发布：
分项说明：
常见扣分：
隐藏测试类别级反馈：
复核截止：
复核材料要求：
下一步补救建议：
```

## 每周 Staff Meeting

建议每周 30-45 分钟，固定议程：

| 顺序 | 议题 | 产出 |
|------|------|------|
| 1 | 上周 quick check、exit ticket、Office Hours 高频问题 | 需要 recap 的 2-3 个主题 |
| 2 | 作业公开/隐藏测试失败分布 | handout、hint 或测试更新任务 |
| 3 | 评分校准和复核争议 | 需要统一口径的 rubric 项 |
| 4 | 项目 milestone 风险 | 需要 mentor 跟进的团队 |
| 5 | 算力额度与成本异常 | 需要降级、排队或追加额度的项目 |
| 6 | 参与证据与反馈调查 | 阅读复盘、讨论区、期中/期末反馈的改进动作 |
| 7 | 学生支持与可及性问题 | 只记录聚合问题和流程改进 |
| 8 | 前沿来源或内容准确性更新 | source audit 或章节修订任务 |

会议后把可公开的共性问题写成公告或更新 [Student FAQ and Troubleshooting Guide](student-faq-troubleshooting.md)，把运行证据写入 [Course Operations and Improvement Log](course-operations-log.md)。

## 作业发布与评分交接

发布前：

- Autograder Owner 跑公开测试、隐藏测试和 reference solution。
- Head TA 检查 rubric 与隐藏测试类别是否一致。
- Discussion TA 准备本周 shape drill 和 failure drill。
- 课程经理发布公告并确认提交入口可见。

评分中：

- 每个助教先批同一组校准样例。
- 分差超过 [Grading Calibration Guide](grading-calibration.md) 阈值时暂停批改并统一口径。
- 隐藏测试异常或大面积失败时先判断是否为题意、测试或环境问题，再发布成绩。

评分后：

- 发布类别级反馈，不泄露隐藏输入。
- 记录 Top 3 失败类型和复核争议。
- 把需要修订的作业 README、测试或讲义加入改进任务看板。

## Office Hours 排班

排班原则：

- 每周至少覆盖一次概念/数学答疑和一次代码/工程答疑。
- 作业截止前 48 小时增加短时段答疑，但不代写核心实现。
- 项目周安排 mentor-specific slot，覆盖训练、推理、评测和数据/伦理。
- 私密事项使用课程邮箱或 LMS 私密消息，不在公开队列中讨论。

每次 Office Hours 后记录问题类别、最小复现、是否需要 recap、是否需要更新材料。

## 事故与升级流程

| 事件 | 初步处理 | 升级 |
|------|----------|------|
| autograder 误判 | 暂停发布或标记成绩待确认，复查测试和 reference | Head TA + 主讲教师 |
| 隐藏测试泄露 | 立即替换受影响测试，记录影响范围 | 主讲教师 |
| 大面积环境失败 | 发布临时 workaround 和补测窗口 | 课程经理 |
| 学术诚信疑似问题 | 收集证据，不在公开区讨论 | 主讲教师按学校流程 |
| 可及性或健康相关请求 | 转私密渠道，只共享必要信息 | 主讲教师 |
| 前沿事实错误 | 降级或移除正文 claim，更新来源审计 | 主讲教师 |

所有事故都应记录日期、影响范围、处理动作、对学生的补救和后续预防任务。

## 期末收尾

期末后一周内完成：

- 汇总成绩分布、作业失败分布和复核结果。
- 归档脱敏优秀项目报告和展示材料。
- 更新 [Capstone Project Gallery and Idea Bank](capstone-project-gallery.md) 的归档记录。
- 完成 [Course Operations and Improvement Log](course-operations-log.md) 的期末课程复盘。
- 列出下一轮开课前必须完成的 3-7 个改进任务。

## Staff Handoff Template

```text
Course offering:
Staff:
Tools and access:
Known fragile tests:
Known chapter/source issues:
Most common student blockers:
Project teams needing follow-up:
Open regrade or integrity cases:
Accessibility/support process notes:
Next offering priorities:
```
