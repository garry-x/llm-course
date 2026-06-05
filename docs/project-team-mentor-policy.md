# Project Team and Mentor Policy

本政策用于管理 final project / capstone 的团队规模、导师匹配、外部协作者、共享项目、贡献声明和争议处理。它补充 [Capstone Proposal and Milestone Guide](capstone-proposal-milestone.md)、[Capstone Project Gallery and Idea Bank](capstone-project-gallery.md)、[Default Final Project Guide](default-final-project-guide.md)、[Project Report Template and Reproducibility Checklist](project-report-template.md)、[Capstone 项目报告 Rubric](project-report-rubric.md)、[Capstone Defense and Oral Exam Question Bank](capstone-defense-oral-exam-bank.md)、[Data and Ethics Review](data-ethics-review.md)、[Compute Resource and Cost Guide](compute-resource-guide.md)、[Course Staff and Office Hours Directory](course-staff-office-hours-directory.md)、[Staff Assistance and Code Review Boundary Policy](staff-assistance-code-review-policy.md) 和 [课程政策](course-policies.md)。

本课程允许默认项目和自定义项目并行，但评分标准始终围绕可复现证据、技术解释、贡献边界和风险披露。团队越大，越需要更清楚的任务分工、日志证据和个人贡献说明。

## 团队规模

| 团队规模 | 适用场景 | 额外要求 |
|----------|----------|----------|
| 1 人 | 默认训练项目、默认推理项目、小型自定义项目 | 个人负责全部复现命令、日志、报告和展示 |
| 2 人 | 一个训练/推理主线加一个评测或报告主线 | proposal 写清主责分工；milestone 展示两人各自证据 |
| 3 人 | 范围明确、工作量确实更大的自定义项目或默认最终项目扩展 | 必须有任务 owner 表、贡献证据、每周同步记录和风险降级路径 |

默认建议 1-2 人。3 人团队不是加分项；如果交付物不能证明每位成员有实质贡献，教师可以要求补充问答、拆分评分或降级项目范围。

## 组队规则

- 每名学生只能参与一个本课程 final project。
- 团队应在 proposal 前确认成员、项目方向和最小成功标准。
- proposal 提交后更换成员需要教师批准，并说明对贡献、进度和评分的影响。
- 若成员退出或长期无法参与，团队应在 milestone 前提交 revised scope 和贡献记录。
- 不允许用“挂名成员”换取更大项目范围或更多资源额度。

## Mentor 匹配

每个自定义项目应在 proposal 后分配一名教师或助教 mentor。默认项目可由 discussion section 或 office hours 集中支持；只有范围超出默认路径或存在高风险数据/资源问题时才需要单独 mentor。学生可见的 project mentor hours、queue policy 和 escalation matrix 见 [Course Staff and Office Hours Directory](course-staff-office-hours-directory.md)。

| 项目类型 | 推荐 mentor 背景 | 必问问题 |
|----------|------------------|----------|
| 训练工程 | PyTorch、优化器、checkpoint、数据审计 | token budget 是否可行；loss/吞吐/恢复证据是否可复现 |
| 推理工程 | serving、RAG、benchmark、SLO、容量规划 | 评测集是否固定；P95/TTFT/TPOT 是否能从报告复现 |
| 经典 NLP / evaluation | dependency parsing、BLEU/ROUGE/F1、标注协议 | 指标是否支持结论；错误分析是否覆盖指标盲点 |
| alignment / safety | SFT、LoRA、DPO/GRPO、安全评测 | 数据来源和偏好标签是否可解释；风险边界是否写清 |
| 高风险数据或应用 | 数据治理、隐私、安全或课程负责人 | 许可证、PII、污染、滥用风险和残余风险是否可接受 |

Mentor 可以做：

- 帮助收窄问题、明确非目标和最小成功标准。
- 指出数据、资源、评测或复现风险。
- 建议相关课程材料、论文或 baseline。
- 在 milestone 后判断是否需要降级范围。

Mentor 不可以做：

- 代写代码、报告、实验设计或结论。
- 调试隐藏测试或泄露评分脚本。
- 替学生选择最终结论。
- 对单个团队承诺额外评分优势。

Mentor 默认不审阅完整项目实现；可按 [Staff Assistance and Code Review Boundary Policy](staff-assistance-code-review-policy.md) 做 artifact_review：检查日志、metric table、ablation plan、risk register、source boundary、data/ethics form、report outline，以及 [Capstone Proposal and Milestone Guide](capstone-proposal-milestone.md) 要求的 split_card、metric_card、uncertainty_record、claim_audit 和 leakage_check。

## 外部协作者与共享项目

本节对应 final project 中的 external collaborators 和 shared project 披露边界。

学生可以使用外部资源，但必须披露贡献边界：

| 情况 | 是否允许 | 披露要求 |
|------|----------|----------|
| 使用开源库、模型或公开数据集 | 允许 | 引用链接、版本、许可证、使用位置和学生自己的改动 |
| 与非本课程人员讨论项目方向 | 允许 | 报告中说明对方角色和建议范围 |
| 与实验室、公司或社团项目相关 | 有条件允许 | proposal 中说明已有代码/数据/目标，明确本课程新增贡献 |
| 与另一门课共享项目 | 有条件允许 | 两门课的要求都必须满足；报告说明哪些工作用于本课程评分 |
| 使用商业 API 或云服务 | 有条件允许 | 披露模型/API、日期、费用、限制、失败重跑和替代方案 |
| 使用未授权私有数据或他人代码 | 不允许 | 必须更换数据/代码或降级为可公开复现任务 |

外部协作者不能代替学生完成本课程要求的实现、评测、报告或展示。若外部资源占据核心贡献，项目应降级为案例分析或更换题目。

## 贡献声明

最终报告必须包含贡献声明。建议使用以下结构：

| 成员 | 负责部分 | 可复核证据 | 外部协助或 AI 工具 | 自评贡献比例 |
|------|----------|------------|--------------------|--------------|
| Student A | 数据审计、训练循环、loss 分析 | commit、metrics、命令、报告段落 | 使用官方 PyTorch 文档；AI 用于调试假设 | 40% |
| Student B | 服务接口、benchmark、SLO | commit、benchmark JSON、SLO 输出 | 使用 FastAPI 文档；同伴 review 建议 | 35% |
| Student C | 报告整合、错误分析、展示 | report diff、失败案例表、slides | 使用 grammar checker；引用外部论文 | 25% |

贡献比例不是自动分数，但它帮助教师判断团队工作是否公平。贡献声明必须和 commit、日志、实验表、报告段落或展示记录一致。

## 不均衡贡献处理

若团队内部贡献严重不均衡，课程组按以下流程处理：

1. 要求团队补交事实记录：任务 owner、commit、日志、会议记录、报告段落和实验输出。
2. 对每位成员进行 5-10 分钟项目问答，问题围绕其声明贡献。
3. 根据证据决定是否要求补交个人说明、拆分展示、单独评分或调整项目范围。
4. 只记录必要事实，不在公开讨论区披露个人困难或敏感信息。

常见触发条件：

- 成员无法解释自己负责的代码、指标或报告段落。
- 提交历史、日志和贡献声明明显不一致。
- 团队报告缺少某成员可复核证据。
- 组员私下反馈长期无法联系或未完成承诺任务。

## Mentor Checkpoint 模板

每次 mentor meeting 建议记录：

| 字段 | 内容 |
|------|------|
| project_id | 项目标题或提交编号 |
| meeting_date | 日期 |
| attendees | 参会学生和 mentor |
| current_scope | 当前目标和非目标 |
| strongest_evidence | 当前最可信的结果、日志或评测 |
| largest_risk | 最可能导致项目失败的问题 |
| required_next_step | 下次提交前必须完成的动作 |
| downgrade_trigger | 触发降级范围的条件 |
| follow_up_evidence | 下次如何证明问题已解决 |
| statistics_gate | split、metric、uncertainty、claim 或 leakage 中必须先解决的门禁 |

这些记录用于帮助学生收敛项目，不替代最终报告，也不作为隐藏评分信息公开。

## 发布前 Checklist

| 检查项 | 通过标准 |
|--------|----------|
| 团队规模 | proposal 写明 1/2/3 人团队和每位成员职责 |
| Mentor 匹配 | 自定义项目有 mentor 背景匹配和第一次反馈记录 |
| 外部协作者 | 报告披露外部人员、课程共享、开源库、API 和 AI 工具 |
| 贡献声明 | 每位成员有可复核证据，不只写笼统描述 |
| 不均衡处理 | 有事实记录、私密处理流程和单独评分选项 |
| 资源公平 | 多人项目没有未经说明地按人数线性扩大 GPU/API 额度 |
