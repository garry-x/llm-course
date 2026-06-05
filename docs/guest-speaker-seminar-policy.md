# Guest Speaker and External Seminar Policy

本流程用于把 CS224N 风格的 guest lecture、工业分享、论文报告和外部 seminar 转化为可评分、可访问、可复盘的课程活动。它补充 [Participation and Feedback Guide](participation-feedback-guide.md)、[Frontier Seminar Handout](frontier-seminar-handout.md)、[Lecture Media Access Policy](lecture-media-access-policy.md)、[Course Communication and Announcement Policy](course-communication-policy.md) 和 [Course Operations and Improvement Log](course-operations-log.md)。

## 适用范围

| 活动类型 | 典型主题 | 是否可计入参与分 | 主要交付 |
|----------|----------|------------------|----------|
| guest lecture | LLM reasoning、multimodality、interpretability、social impact、deployment | 是 | attendance 或替代任务、technical reflection、Q&A note |
| external seminar | 外部公开讲座、工业技术报告、论文作者 talk | 是，但需课程组预先确认 | source audit、课程章节连接、技术限制说明 |
| project clinic | 项目 mentor、行业工程师或研究员给项目建议 | 可计入项目过程证据，不单独替代项目成绩 | project advice log、risk update、contribution note |
| student-led paper report | 学生报告前沿论文或复现实验 | 可计入参与分或 frontier seminar 交付 | slides/notes、claim audit、discussion question |

## 活动准入

| 检查项 | 通过标准 |
|--------|----------|
| course fit | 主题能连接至少一个章节、作业、capstone 或 [Frontier Seminar Handout](frontier-seminar-handout.md) 主题 |
| source boundary | 讲者材料区分论文、模型卡、产品发布、benchmark、个人观点和未公开信息 |
| no private solution leakage | 不展示 hidden tests、`reference_solution.py`、未发布 rubric、学生私有代码或 private LMS / Ed post |
| accessibility | 直播、录播、caption / transcript、文字摘要或等价替代任务符合 [Accessibility and Student Support Guide](accessibility-student-support.md) |
| privacy and consent | 录制、截图、问答、学生姓名和项目细节遵守 [Lecture Media Access Policy](lecture-media-access-policy.md) |
| conflict boundary | 赞助、招聘、商业推广、未公开模型规格和数据许可证风险提前说明 |

## 日程与公告

| 时间 | Staff 动作 | 学生可见信息 |
|------|------------|--------------|
| T-14 天 | 确认讲者、主题、材料边界、录制许可和替代任务 | 主题、时间、地点/链接、是否计入参与分 |
| T-7 天 | 发布推荐阅读、预习问题和 Q&A 提交入口 | 阅读清单、提问模板、source boundary |
| T-1 天 | 检查字幕/录制、幻灯片可访问性、隐私剪辑风险 | 最终链接、参与分提交入口 |
| T+2 天 | 发布录播或结构化摘要，开放 reflection 提交 | 录播/摘要、deadline、rubric |
| T+7 天 | 汇总学生反馈、Q&A、课程材料改进动作 | 聚合回应，不公开个人身份 |

公告必须通过 [Course Communication and Announcement Policy](course-communication-policy.md) 规定的正式渠道发布。若时间、计分或访问方式变化，应同步更新 [Course Calendar and Deadline Ledger](course-calendar-deadline-ledger.md)。

## 参与分规则

不得把“人在现场”作为唯一评分依据。建议每次 guest speaker activity 采用 0.25%-0.5% 的小额参与分，或并入 [Participation and Feedback Guide](participation-feedback-guide.md) 的讨论区/课程贡献项。

| 证据 | 满分标准 |
|------|----------|
| attendance | 现场、直播或录播观看均可；只证明参与，不单独给满分 |
| technical reflection | 150-250 字，连接课程章节、代码或项目风险 |
| Q&A note | 至少一个技术问题、实验限制问题或部署风险问题 |
| source audit | 标出讲者使用的论文、模型卡、产品声明或非公开观点 |
| project transfer | 若用于项目，说明采用、拒绝或改写建议的原因 |

若学校不允许把出勤或问卷计入分数，保留 reflection 作为非计分学习证据，并把聚合问题写入 operations log。

## 替代任务

| 情况 | 替代任务 | 等价性要求 |
|------|----------|------------|
| 时区或课程冲突 | 观看录播或阅读 structured summary | 同样提交 technical reflection 和 Q&A note |
| 学术便利安排 | caption / transcript、延长提交窗口或口头替代 | 不降低技术连接和来源审计要求 |
| 录播不可发布 | 阅读讲者授权材料或同主题论文 | 需说明没有录播时的证据来源 |
| 讲者取消 | 使用预先准备的 external seminar reading | 保持同一 rubric 和截止时间调整公告 |

替代任务不能要求学生披露健康、身份、家庭或安全细节；具体沟通走私密渠道。

## 学生提交模板

```text
Event title:
Speaker or source:
Attendance mode: live / recording / summary / approved alternative
Course connection: chapter, assignment, capstone, or seminar topic
Technical reflection:
Question or limitation:
Source boundary: paper / model card / product claim / benchmark / personal view
Project transfer, if any:
Accessibility or participation issue, if any:
```

## Rubric

| 项目 | 权重 | 满分标准 |
|------|:--:|----------|
| Course connection | 25% | 明确连接章节公式、作业代码、capstone 或 frontier seminar 主题 |
| Technical reflection | 30% | 抓住一个具体方法、实验、系统取舍或失败模式 |
| Source boundary | 20% | 区分稳定论文、官方材料、商业声明、未复核 benchmark 和个人观点 |
| Question quality | 15% | 提出可检验、可讨论或可复现实验问题 |
| Professional participation | 10% | 尊重讲者和同学，不泄露私有材料或提交无关内容 |

## 讲者材料与录制边界

- 讲者幻灯片、demo、代码和录播默认不进入公开仓库，除非讲者明确授权。
- 若材料包含公司内部信息、未公开模型、学生项目、敏感数据或 API key，必须删除或标为 staff only。
- 学生问答进入录播前应完成隐私剪辑；不公开学生姓名、声音、面部或个人情况，除非得到明确授权。
- 公开摘要应保留技术结论、来源边界和可复核链接，不发布完整私人材料。
- 若讲者提供外部论文或代码，按 [External Source Verification Guide](external-source-verification.md) 和 [External Source Inventory](external-source-inventory.md) 登记来源。

## 项目与伦理升级

Guest speaker advice 不替代课程 rubric。项目团队若采用讲者建议，应在 proposal、milestone 或 final report 中说明：

| 证据 | 说明 |
|------|------|
| advice_summary | 讲者建议的技术点、风险或参考材料 |
| decision | 采用、拒绝、推迟或改写 |
| source_update | 新增论文、模型卡、库或 API 的引用和访问日期 |
| ethics_update | 数据、隐私、偏见、安全或许可证风险是否变化 |
| mentor_follow_up | 是否需要 mentor 或课程组复核 |

涉及高风险数据、真实用户、医疗/法律/金融场景或外部商业部署时，必须同步更新 [Data and Ethics Review](data-ethics-review.md)。

## 记录模板

| field | 内容 |
|-------|------|
| event_id | 例如 `week8-guest-reasoning` |
| event_type | guest lecture、external seminar、project clinic、student-led paper report |
| speaker_or_source | 讲者、机构或外部公开材料 |
| topic | 主题和课程连接 |
| date_time | 时间、时区和访问方式 |
| recording_status | live only、recorded enrolled-only、public summary、not recorded |
| accessibility_support | caption、transcript、summary、alternative task |
| participation_credit | 分值或非计分说明 |
| source_boundary | 论文、模型卡、产品声明、benchmark、个人观点 |
| privacy_review | checked、needs edit、staff only |
| follow_up_actions | FAQ、reading list、frontier seminar、project rubric 或 operations log 更新 |

## Staff Checklist

- 讲者、主题、录制许可、材料边界和替代任务在 T-14 天确认。
- 公告包含时间、访问方式、参与分、reflection rubric、隐私边界和提交入口。
- 幻灯片、demo 和录播经过 accessibility、privacy_review 和 source boundary 检查。
- 学生可选择 live、recording、summary 或 approved alternative，评分标准一致。
- Q&A 和反馈只发布聚合总结，不公开个人身份或私有项目细节。
- 活动结束后一周内把 follow_up_actions 写入 [Course Operations and Improvement Log](course-operations-log.md)。

## 发布前 Checklist

- syllabus、participation guide、frontier seminar handout 和 CS224N crosswalk 均链接本流程。
- [Lecture Media Access Policy](lecture-media-access-policy.md) 覆盖录制、caption / transcript、隐私剪辑和 public learner 边界。
- [Course Calendar and Deadline Ledger](course-calendar-deadline-ledger.md) 有 guest speaker 或 external seminar 的时间与提交窗口。
- `scripts/build_course_site_release.py` 把本文件列入学生安全文档。
- `.venv/bin/python verify_course.py` 通过。
