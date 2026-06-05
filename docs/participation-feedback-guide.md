# Participation and Feedback Guide

本指南用于把课堂参与、讨论区贡献、阅读复盘、同伴 review、问卷反馈和课程改进连接成可评分、可复盘的机制。它补充 [课程 Syllabus](syllabus.md)、[逐周阅读清单与复盘 Handout](reading-list.md)、[Reading Discussion Question Bank](reading-discussion-question-bank.md)、[Paper Recap Calibration Pack](paper-recap-calibration-pack.md)、[Recitation Worksheet Pack](recitation-worksheet-pack.md)、[Learning Analytics and Remediation Plan](learning-analytics-remediation-plan.md)、[Weekly Teaching Reflection and Adjustment Log](weekly-teaching-reflection-adjustment-log.md)、[Teaching Observation and Course Evaluation Dossier](teaching-observation-course-evaluation.md)、[Discussion Section and Office Hours Guide](discussion-office-hours-guide.md)、[Guest Speaker and External Seminar Policy](guest-speaker-seminar-policy.md)、[Course Staff Runbook](staff-runbook.md) 和 [Course Operations and Improvement Log](course-operations-log.md)。

## 评分范围

参与分不奖励“发言次数”本身，而奖励能帮助学习目标达成的具体证据：

| 类型 | 证据 | 不计分或低分情况 |
|------|------|------------------|
| 阅读复盘 | 摘要、技术细节、代码连接、来源审计、批判性问题 | 只复述摘要，缺少来源或技术判断 |
| 讨论课参与 | shape drill、failure drill、paper-to-code drill 的现场或课后提交 | 只复制他人答案，不能解释 |
| 讨论区贡献 | 回答同学问题、给出最小复现、指出文档不清处 | 泄露隐藏测试、贴完整答案、误导性回复 |
| Office Hours 准备 | 带命令、traceback、shape 推导或最小反例来求助 | 只说“跑不了”，没有证据 |
| 同伴 review | 复现尝试、最强证据、最大风险、具体改进建议 | 泛泛夸赞或只改格式 |
| guest lecture / external seminar | technical reflection、Q&A note、source audit、project transfer | 只签到、不连接课程、不区分来源边界 |
| 课程反馈调查 | 期中/期末反馈，指出材料、节奏、作业或支持流程问题 | 人身攻击、无可执行信息 |

## 参与评分 Rubric

建议将“阅读复盘与课堂参与”10% 拆成：

| 项目 | 权重 | 满分标准 |
|------|:--:|----------|
| 阅读复盘 | 4% | 每周提交，能连接论文、代码、实验限制和来源等级 |
| 讨论课/Office Hours 准备 | 2% | 能展示 shape 推导、最小复现或失败分析 |
| 同伴 review | 2% | 对项目或阅读复盘给出可执行、可验证的建议 |
| 讨论区或课程贡献 | 1% | 回答问题、整理 FAQ、发现文档/测试问题 |
| guest lecture / external seminar 或反馈调查 | 1% | 完成 technical reflection、Q&A/source audit 或期中/期末反馈，给出具体改进建议 |

若学校不允许按问卷完成情况计分，可把反馈调查改为不计分但强烈鼓励，并保留聚合反馈用于课程改进。

阅读复盘的 A/B/C/not-passing anchor sample、必填字段和 TA 分差校准流程按 [Paper Recap Calibration Pack](paper-recap-calibration-pack.md) 执行。

## 讨论区贡献规则

允许：

- 提问时附上命令、环境、traceback、输入 shape 和已尝试步骤。
- 用概念、伪代码、最小反例或文档链接帮助同学定位问题。
- 指出 handout、README、rubric 或测试反馈中不清楚的地方。

不允许：

- 发布隐藏测试输入、参考解、完整作业答案或其他学生提交。
- 诱导他人共享私有评分信息。
- 把未经验证的前沿模型数字当作课程事实传播。
- 对个人健康、身份、便利安排或成绩争议做公开评论。

## 期中反馈调查

建议第 5 周结束后发布，问题应短、可执行：

| 题目 | 目的 |
|------|------|
| 哪一章或哪类推导最阻碍你继续学习？ | 调整 recap 和讨论课 |
| 哪个作业说明最不清楚？请指出具体段落或命令 | 修订 handout |
| 公开测试失败信息是否能帮助定位问题？ | 改进 autograder feedback |
| Office Hours 或讨论区是否解决了你的问题？ | 调整支持渠道 |
| 你希望第 6-10 周增加哪类示例？ | 调整后半程节奏 |

处理要求：

- 一周内发布聚合回应，不公开个人身份。
- 至少列出 3 个会采取的改进动作和 3 个暂不改变的原因。
- 将动作写入 [Course Operations and Improvement Log](course-operations-log.md)。

## 期末反馈调查

期末调查用于下一轮课程改版：

| 题目 | 目的 |
|------|------|
| 哪个章节最有效地帮助你理解 LLM？ | 保留有效设计 |
| 哪个作业最能检验真实理解？ | 评估作业质量 |
| 哪个项目 milestone 最有帮助或最浪费？ | 调整项目流程 |
| 阅读清单是否过多、过少或缺少关键来源？ | 更新 reading list |
| 课程支持渠道是否公平、及时、可访问？ | 改进 staff runbook |
| 下一轮开课最应该修复什么？ | 生成改进任务 |

期末反馈必须和成绩分布、隐藏测试统计、复核记录、项目复现记录一起分析，不能只看主观满意度。

## 嘉宾讲座或外部报告

若课程加入嘉宾讲座、工业分享或论文报告，可计入参与分，但必须按 [Guest Speaker and External Seminar Policy](guest-speaker-seminar-policy.md) 有交付证据：

- 150-250 字技术反思。
- 一个连接课程章节的技术点。
- 一个来源边界或实验限制问题。
- 一个可在项目中复用或避免的工程经验。

不得把出勤本身作为唯一评分依据；录播、文字摘要或替代任务应按 [Guest Speaker and External Seminar Policy](guest-speaker-seminar-policy.md) 和 [Accessibility and Student Support Guide](accessibility-student-support.md) 处理。

## 参与证据记录

助教每周记录聚合数据，不记录无关个人隐私：

| 周次 | 阅读复盘提交率 | 讨论区高质量贡献 | Office Hours 高频问题 | 反馈动作 |
|------|----------------|------------------|-----------------------|----------|
| Week 1 dry-run baseline | live submission pending; reading-list and discussion question bank ready | likely contributions: BPE boundary question, RoPE claim boundary, environment command self-check | likely issues: `.venv/bin/python` path, tensor shape notation, byte-level BPE decode errors | publish first-week reminder linking FAQ, reading recap rubric, and WTR-2026-L02-ROPE recap |
| Week 5 dry-run baseline | live submission pending; midterm feedback protocol ready | likely contributions: minimal repro for training-loop bugs and source card examples | likely issues: device mismatch, validation mode, workload around Ch06-Ch07 | aggregate themes into course operations log and teaching observation response memo |

高质量贡献样例可以脱敏后加入 FAQ、lecture recap 或作业说明。低质量或违规贡献按课程政策处理。

## 学生提交模板

```text
Week:
Reading or topic:
Core claim:
Technical detail:
Connection to code or assignment:
Source level and uncertainty:
Question for discussion:
If asking for help, command/traceback/minimal reproduction:
```

## Staff Checklist

| 时间 | 动作 |
|------|------|
| Week 1 | 说明参与分、讨论区规则、隐藏测试边界和求助证据 |
| 每周 | 汇总阅读复盘、exit ticket、讨论区和 Office Hours 高频问题 |
| Week 5 | 发布期中反馈调查并一周内回应 |
| Week 8-10 | 收集同伴 review 和项目复现反馈 |
| 期末 | 发布期末反馈调查，汇总改进任务并写入 operations log |
