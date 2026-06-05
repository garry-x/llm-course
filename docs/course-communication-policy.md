# Course Communication and Announcement Policy

本政策用于统一课程公告、讨论区、私密消息、课程邮箱、Office Hours 和紧急事项的使用边界。高校课程中的沟通渠道不是附属品：它决定学生能否及时获得作业说明、评分变更、支持渠道、项目反馈和内容更正。

本政策补充 [课程 Syllabus](syllabus.md)、[Course Staff and Office Hours Directory](course-staff-office-hours-directory.md)、[Discussion Section and Office Hours Guide](discussion-office-hours-guide.md)、[Student FAQ and Troubleshooting Guide](student-faq-troubleshooting.md)、[Course Staff Runbook](staff-runbook.md)、[Participation and Feedback Guide](participation-feedback-guide.md)、[Accessibility and Student Support Guide](accessibility-student-support.md)、[Course Errata and Correction Ledger](course-errata-correction-ledger.md) 和 [Course Operations and Improvement Log](course-operations-log.md)。

## 渠道总览

| 渠道 | 适合内容 | 不适合内容 | 响应目标 |
|------|----------|------------|----------|
| 课程公告 | syllabus 更新、作业发布、截止时间、成绩发布、重大勘误、系统故障 | 单个学生的私密问题 | 下次课程活动前发布 |
| 公开讨论区 | 概念问题、公开测试、环境配置、阅读材料、公开项目设计问题 | 隐藏测试、参考答案、其他学生代码、个人敏感信息 | 1-2 个工作日 |
| 私密消息或课程邮箱 | 学术便利安排、健康或家庭情况、迟交说明、评分复核升级、协作披露 | 可公开回答的普通概念题 | 2 个工作日 |
| Office Hours | shape 推导、debug 最小复现、项目 scope、milestone 风险 | 代写核心实现、查看隐藏测试、公开个人困难 | 按周排班 |
| LMS / Gradescope 等平台 | 正式提交、成绩、复核窗口、作业发布包 | 长篇技术讨论或私密健康信息 | 按平台规则 |
| 学校正式支持渠道 | 紧急健康、安全、残障服务、心理健康、性暴力或身份安全问题 | 普通作业 debug | 按学校正式流程 |

## 公告规则

所有影响评分、截止时间、提交入口、测试口径、项目要求或课程政策的变更，都必须通过课程公告发布。只在课堂口头说明或只在讨论区回复一个学生，不足以构成正式变更。

公告至少包含：

- 变更主题。
- 影响范围：章节、作业、项目、评分、政策或工具。
- 生效时间。
- 学生需要采取的动作。
- 相关文档链接。
- 是否影响已提交作业或项目。

重大勘误应同时更新相关材料，并在 [Course Operations and Improvement Log](course-operations-log.md) 记录影响范围和处理动作。

## 公开讨论区规则

学生可以公开提问：

- 章节概念、公式、shape、mask、指标解释。
- 公开测试失败和环境配置。
- 作业 README、starter API 或提交格式的歧义。
- 项目 proposal/milestone 的公开范围问题。
- 阅读材料或来源等级问题。

学生不得公开发布：

- 隐藏测试输入、隐藏测试输出或评分脚本细节。
- 参考解答、完整作业代码或其他学生提交。
- 个人健康、身份、安全、家庭、便利安排或成绩争议细节。
- API key、私有数据、私有路径、未授权文档或敏感日志。

助教回复公开问题时应给出定位路径、最小反例或文档链接；不应贴出完整答案或替学生完成核心实现。

## 私密渠道规则

以下问题应使用私密消息或课程邮箱：

- 学术便利安排和可访问性请求。
- 迟交、疾病、家庭或安全相关说明。
- 评分复核升级或学术诚信沟通。
- 团队项目贡献争议。
- 外部协作者、共享项目或敏感数据披露。
- 任何不应暴露给全班的个人信息。

课程组处理私密问题时只共享必要信息。例如，便利安排只告知需要执行安排的教师或助教；评分争议只在负责复核的 staff 内处理；健康或安全事项按学校正式流程升级。

## Office Hours 规则

Office Hours 的目标是帮助学生形成 debug 和推理能力，而不是替学生完成作业。高质量求助应包含：

- 课程项目或作业编号。
- 运行命令和工作目录。
- Python/PyTorch 版本。
- 第一个失败测试或 traceback。
- 输入 shape 或最小样例。
- 已尝试的定位步骤。
- 希望 staff 回答的具体问题。

Office Hours 后，助教只记录聚合问题类别、最小复现摘要和需要更新的材料，不记录无关个人隐私。若同一问题多次出现，应更新 [Student FAQ and Troubleshooting Guide](student-faq-troubleshooting.md)、作业 README、discussion guide 或发布公告。

学生可见的 staff 角色、office hours 类型、queue policy、private routing 和 escalation matrix 见 [Course Staff and Office Hours Directory](course-staff-office-hours-directory.md)。

## 评分和复核沟通

成绩发布公告应说明：

- 分项成绩和 rubric 映射。
- 常见扣分类型。
- 隐藏测试类别级反馈。
- 复核窗口和复核材料要求。
- 补救材料或下一步学习建议。

复核请求必须指向具体评分项、提交文件和理由。复核可能提高或降低成绩，因为 staff 会重新检查相关评分项。隐藏测试输入、参考答案和评分脚本不通过复核公开。

## 课程勘误和内容更正

如果学生或 staff 发现课程内容错误，处理顺序如下：

1. 公开讨论区或私密渠道收到报告。
2. staff 判断是否影响公式、代码、作业、项目、评分或来源准确性。
3. 若影响评分或提交要求，发布课程公告。
4. 修改相关章节、文档、测试或发布包。
5. 运行 `.venv/bin/python verify_course.py`；重大项目或发布变更运行 `.venv/bin/python verify_course.py --capstone --training`。
6. 在 [Course Errata and Correction Ledger](course-errata-correction-ledger.md)、operations log 或 source audit 中记录处理动作。

前沿模型、API 价格、benchmark、模型卡和框架行为属于易变信息，必须按 [External Source Verification Guide](external-source-verification.md) 复核后再改正文。

## Staff 使用规范

课程团队应遵守：

- 公开问题优先公开回答，避免同一问题被重复私信处理。
- 涉及个人情况的问题转私密渠道，不要求学生公开解释。
- 政策变更、评分口径变更和截止时间变更必须公告。
- 讨论区答复若形成新规则，应同步更新 syllabus、FAQ、assignment guide 或 project guide。
- 不在公开仓库、公开讨论区或公告中记录学生个人敏感信息。

## 发布前 Checklist

| 检查项 | 通过标准 |
|--------|----------|
| 渠道边界 | 公告、公开讨论区、私密消息、课程邮箱、Office Hours 和学校正式支持渠道均有用途说明 |
| 公告权威性 | 影响评分、截止时间、提交入口、测试口径或政策的变更必须公告 |
| 隐私边界 | 个人健康、便利安排、成绩争议、贡献争议和安全事项必须转私密渠道 |
| 支持响应 | 公开问题、私密问题和 Office Hours 有响应目标或排班规则 |
| 勘误流程 | 内容错误能连接到公告、材料修改、验证命令和 operations/source audit 记录 |
| 学生行动 | FAQ 和 Office Hours 模板说明提问时应提供命令、环境、shape、traceback 和最小复现 |
