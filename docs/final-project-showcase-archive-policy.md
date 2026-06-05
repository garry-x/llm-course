# Final Project Showcase and Archive Policy

本政策用于管理 final project poster session、项目展示、公开报告归档、优秀样例发布、项目 artifact 保留和公开/校内/教师内部边界。它补充 [Capstone Project Gallery and Idea Bank](capstone-project-gallery.md)、[项目展示与同伴 Review Rubric](presentation-peer-review.md)、[Capstone Defense and Oral Exam Question Bank](capstone-defense-oral-exam-bank.md)、[Project Report Template and Reproducibility Checklist](project-report-template.md)、[Project Submission Dossier](project-submission-dossier.md)、[Project Report Exemplar Pack](project-report-exemplar-pack.md)、[Capstone 项目报告 Rubric](project-report-rubric.md)、[Project Team and Mentor Policy](project-team-mentor-policy.md)、[Data and Ethics Review](data-ethics-review.md)、[Material Versioning and Archive Policy](material-versioning-archive-policy.md)、[Enrollment, Audit, and Public Use Policy](enrollment-audit-public-use-policy.md) 和 [Course Communication and Announcement Policy](course-communication-policy.md)。

参照 CS224N Winter 2026 公开页的 final project 结构：final project 包含 proposal、milestone、poster 和 report，往年 project reports 作为 archived public reports 提供。本课程采用同类原则，但要求公开前完成 consent、redaction、source boundary 和 reproducibility artifact 检查，并把 public archive packet 与 staff-only grading packet 分开。

课程尚未运行时，[Project Report Exemplar Pack](project-report-exemplar-pack.md) 提供 synthetic/anonymized 样例，不能冒充 archived public report；课程运行后加入真实样例时必须替换 `synthetic_status` 并保留 archived_label。

## Showcase 形式

| 形式 | 默认对象 | 交付材料 | 评分关系 | 公开边界 |
|------|----------|----------|----------|----------|
| in-class poster session | enrolled students、staff、approved guests | poster 或 slides、2 分钟 pitch、问答记录 | 可作为 poster/presentation 分项证据 | 不默认公开 |
| recorded presentation | enrolled students、staff | 录制视频、讲稿、问答补充 | 适合可访问性或时区替代 | 不含学生隐私或未授权数据时可校内分享 |
| public project abstract | public learner | 标题、摘要、成员可选署名、来源边界 | 不替代正式评分 | 需 consent 和 redaction |
| archived final report | public learner 或 institution-only | 报告 PDF/Markdown、复现摘要、artifact manifest | 仅作历史样例 | 不作为本轮评分依据 |
| staff-only evaluation packet | staff | 原始报告、评分表、复核记录、隐藏反馈 | 评分与争议处理 | 不公开 |

## Poster Session 运行规则

- 每组建议 5-8 分钟展示，2-3 分钟问答；大型班级可改为 poster walk、分会场或异步 recorded presentation。
- 展示必须覆盖 problem、method、result、failure case、reproducibility、risk 和 next step。
- 展示材料必须包含一条 primary reproduction command 或最小 acceptance command。
- 不能只展示成功 demo；至少说明一个失败案例或指标局限。
- 如需替代展示形式，按 [Accessibility and Student Support Guide](accessibility-student-support.md) 执行，核心评分目标不降低。

## 公开归档资格

项目要进入 public archive，必须同时满足：

| 要求 | 通过标准 |
|------|----------|
| consent | 团队成员明确同意公开范围；不同意公开的成员不被署名或暴露身份 |
| redaction | 删除学生 ID、邮箱、私人路径、API key、账号、成绩、私密反馈和未授权截图 |
| data license | 数据来源、许可证、访问日期和使用范围写清楚 |
| model/API boundary | 模型卡、API 文档、第三方库和外部服务引用可复核 |
| reproducibility summary | 至少保留环境、命令、seed、metrics、硬件/成本条件和 artifact manifest |
| safety review | 数据伦理、PII、偏见、污染、安全边界和残余风险有说明 |
| archived label | 明确标注 archived public report，不作为本轮课程评分依据 |

## Redaction Checklist

公开前必须删除或替换：

- 学生证件号、邮箱、电话号码、头像、可识别照片和个人困难说明。
- API key、token、云账号、账单截图、私有 bucket、私有路径和内部 URL。
- hidden tests、`reference_solution.py`、评分脚本、未发布 rubric、private LMS / Ed post。
- 未授权数据、受限模型输出、第三方版权材料和不可公开的公司/实验室信息。
- 过度详细的安全绕过、攻击 payload 或敏感数据样例。

## Artifact Retention

| artifact | 最低保留对象 | 保留目的 | 公开性 |
|----------|--------------|----------|--------|
| final report | staff；可选 public archive | 评分、复核、下一轮样例 | 可公开但需 redaction |
| poster/slides | staff；可选 public archive | 展示评分、样例 | 可公开但需 consent |
| code snapshot | staff 或 institution archive | 复现与学术诚信 | 通常不公开完整提交 |
| logs/metrics | staff；可选摘要公开 | 复核报告数字 | 公开时脱敏 |
| peer reviews | staff | 参与评分与改进 | 不公开个人 review |
| grading notes | staff | 复核与校准 | 不公开 |

## Archive Record Template

| 字段 | 说明 |
|------|------|
| project_id | 例如 `2026-spring-rag-latency-01` |
| title | 公开标题 |
| track | default final project / training / inference / custom |
| visibility | public / institution-only / staff-only |
| consent_status | all consented / partial consent / no public release |
| redaction_status | checked / needs edit / staff-only |
| artifact_manifest | report、poster、code snapshot、logs、metrics、demo video |
| source_boundary | 数据、模型、API、第三方库和访问日期 |
| reproduction_summary | primary command、environment、seed、hardware、cost |
| archived_label | 明确写 archived public report |

## 学生说明

学生提交最终项目时应知道：

- 评分不要求项目公开；public archive 是可选项。
- 公开与否不影响正式成绩。
- 公开样例不是可复制答案；下一轮学生不能直接复用往届代码、报告文字或实验结果。
- 若项目含敏感数据、公司数据、未授权材料或高风险安全内容，默认 staff-only。
- 团队成员可要求不公开姓名、视频、头像或个人贡献细节。

## Staff Checklist

| 时间 | 动作 |
|------|------|
| Week 8-9 | 告知展示形式、poster rubric、公开归档可选性和 consent 流程 |
| 展示前 72 小时 | 冻结 presentation format、rubric 和 required evidence |
| 展示当天 | 记录问答、高风险 claim、复现疑点和可归档候选 |
| 成绩发布前 | 区分 grading packet、public archive packet 和 staff-only notes |
| 课程结束后 | 完成 consent、redaction、artifact manifest 和 archived label 检查 |

## 发布前 Checklist

- [Capstone Project Gallery and Idea Bank](capstone-project-gallery.md) 的项目报告归档规则引用本政策。
- [项目展示与同伴 Review Rubric](presentation-peer-review.md) 的展示交付物能映射到 poster session 规则。
- [Project Report Template and Reproducibility Checklist](project-report-template.md) 包含 consent、redaction 或 archive boundary 提醒。
- [Material Versioning and Archive Policy](material-versioning-archive-policy.md) 将公开项目样例标为 archived。
- [Data and Ethics Review](data-ethics-review.md) 覆盖 PII、license、bias、contamination 和 safety boundary。
- 运行 `.venv/bin/python verify_course.py`；正式期末发布或站点大改版前运行 `.venv/bin/python verify_course.py --capstone --training`。
