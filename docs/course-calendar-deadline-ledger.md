# Course Calendar and Deadline Ledger

本台账用于把 lecture schedule、assignment release、assignment due date、project proposal、milestone、poster/report、quiz、guest lecture、late day、regrade window 和课程公告连接成一个可审计的时间源。它补充 [课程 Syllabus](syllabus.md)、[10 周 / 20 讲 Lecture Plan](lecture-plan.md)、[Workload and Pacing Calibration](workload-pacing-calibration.md)、[Course Materials Index](course-materials-index.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md)、[Capstone Proposal and Milestone Guide](capstone-proposal-milestone.md)、[Assessment Administration and Exam Integrity Policy](assessment-administration-policy.md)、[Guest Speaker and External Seminar Policy](guest-speaker-seminar-policy.md)、[Course Communication and Announcement Policy](course-communication-policy.md)、[Enrollment, Audit, and Public Use Policy](enrollment-audit-public-use-policy.md) 和 [Course Operations and Improvement Log](course-operations-log.md)。

参照 CS224N Winter 2026 公开页的 schedule/deadline 组织方式：课程 schedule 列出每次 lecture 的日期、材料、events 和 deadlines；assignment deadlines、project deadlines、late days 与 regrade requests 在 course page 中集中说明。本课程采用同类原则，但用可移植的台账格式表达。

## 使用规则

- 本台账是课程时间安排的 single source of truth；syllabus、LMS / Gradescope、公告、作业 README 和项目 handout 的日期必须与本台账一致。
- 所有时间必须写出 timezone，例如 Asia/Shanghai、Pacific Time 或学校本地时区。
- 改动 assignment due date、project deadline、regrade window、late day rule、quiz window 或 release date 时，必须同步更新本台账并按 [Course Communication and Announcement Policy](course-communication-policy.md) 发布公告。
- 课堂口头说明、讨论区回复或私信不能单独改变正式截止时间。
- archived / retired materials 的旧 deadline 不作为本轮课程依据。

## 时间字段

| 字段 | 说明 |
|------|------|
| term | 课程轮次，例如 `2026-spring` 或学校内部 term code |
| timezone | 所有 deadline 使用的时区 |
| lecture_date | 课堂日期；若异步课程则写 release date |
| release_at | 材料或作业对学生开放时间 |
| due_at | 正式提交截止时间 |
| grace_or_late_policy | grace period、late day 或迟交扣分规则 |
| regrade_open_at | 成绩发布后复核窗口开始时间 |
| regrade_close_at | 复核窗口结束时间 |
| source_of_truth | LMS / Gradescope / course site / announcement id |
| change_log | 若改期，记录公告 id、原因和影响范围 |

## 10 周台账模板

| 周 | Lecture | 主题 | 材料 release | 作业或项目 release | 正式 due | 复核或反馈窗口 |
|----|---------|------|---------------|--------------------|-----------|----------------|
| Week 1 | L1-L2 | Course setup、BPE、Embedding、RoPE | 课前 48 小时 | A1 Ch01-Ch02 release | Week 2 课前 24 小时 | prerequisite remediation check |
| Week 2 | L3-L4 | Attention、causal mask、backprop | 课前 48 小时 | A2 Ch03 release | Week 3 课前 24 小时 | A1 grade/regrade window |
| Week 3 | L5-L6 | MHA/GQA/MLA、Transformer block | 课前 48 小时 | A3 Ch04-Ch05 release | Week 4 课前 24 小时 | A2 grade/regrade window |
| Week 4 | L7-L8 | GPT assembly、MoE、model scaling | 课前 48 小时 | A4 Ch06 release | Week 5 课前 24 小时 | A3 grade/regrade window |
| Week 5 | L9-L10 | Training loop、optimizer、checkpoint | 课前 48 小时 | A5 Ch07 release；training proposal release | Week 6 课前 24 小时 | midterm feedback survey |
| Week 6 | L11-L12 | Generation、sampling、speculative decoding | 课前 48 小时 | A6 Ch08 release；training proposal due | Week 7 课前 24 小时 | A5 grade/regrade window |
| Week 7 | L13-L14 | SFT、LoRA、DPO、GRPO | 课前 48 小时 | A7 Ch09 release；training milestone release | Week 8 课前 24 小时 | project mentor matching |
| Week 8 | L15-L16 | Classic NLP、evaluation、ethics；guest lecture / external seminar option | 课前 48 小时 | A8 Ch11 release；peer review release；guest speaker reflection release | Week 9 课前 24 小时 | training milestone feedback；guest speaker reflection window |
| Week 9 | L17-L18 | Inference、RAG、serving、benchmark | 课前 48 小时 | A9 Ch10 release；inference proposal release | Week 10 课前 24 小时 | inference mentor matching |
| Week 10 | L19-L20 | Capstone demo、frontier seminar、final review | 课前 48 小时 | final report/poster instructions | 学校期末提交窗口 | final regrade and reflection window |

## Review Session 台账

| Session | 建议时间 | 对应材料 | 参加对象 | 验收 |
|---------|----------|----------|----------|------|
| Python Review Session | Week 1 L1 后或 L2 前 | [Python and PyTorch Review Session](python-pytorch-review-session.md) | Python 基础 Borderline、跨语言转入、Ch01 helper 未通过学生 | 能实现 pair counting、non-overlapping merge 和最小 run log |
| PyTorch Tutorial Session | Week 2 L3 前或 L3 后 | [Python and PyTorch Review Session](python-pytorch-review-session.md) | PyTorch 基础 Borderline、shape 推导不稳、Ch02 starter 未通过学生 | 能解释 `[B,T,D]` 到 logits、next-token CE 和第一个失败测试 |

## 作业与项目截止台账

| 项目 | release_at | due_at | allowed late days | late cap | regrade window | source_of_truth |
|------|------------|--------|-------------------|----------|----------------|-----------------|
| A1 Ch01-Ch02 | Week 1 L1 后 | Week 2 课前 24 小时 | syllabus policy | assignment cap | 成绩发布后 7 天 | LMS / Gradescope |
| A2 Ch03 | Week 2 L3 后 | Week 3 课前 24 小时 | syllabus policy | assignment cap | 成绩发布后 7 天 | LMS / Gradescope |
| A3 Ch04-Ch05 | Week 3 L5 后 | Week 4 课前 24 小时 | syllabus policy | assignment cap | 成绩发布后 7 天 | LMS / Gradescope |
| A4 Ch06 | Week 4 L7 后 | Week 5 课前 24 小时 | syllabus policy | assignment cap | 成绩发布后 7 天 | LMS / Gradescope |
| A5 Ch07 | Week 5 L9 后 | Week 6 课前 24 小时 | syllabus policy | assignment cap | 成绩发布后 7 天 | LMS / Gradescope |
| A6 Ch08 | Week 6 L11 后 | Week 7 课前 24 小时 | syllabus policy | assignment cap | 成绩发布后 7 天 | LMS / Gradescope |
| A7 Ch09 | Week 7 L13 后 | Week 8 课前 24 小时 | syllabus policy | assignment cap | 成绩发布后 7 天 | LMS / Gradescope |
| A8 Ch11 classic NLP | Week 8 L15 后 | Week 9 课前 24 小时 | syllabus policy | assignment cap | 成绩发布后 7 天 | LMS / Gradescope |
| A9 Ch10 | Week 9 L17 后 | Week 10 课前 24 小时 | syllabus policy | assignment cap | 成绩发布后 7 天 | LMS / Gradescope |
| Training capstone proposal | Week 5 L10 后 | Week 6 L12 前 | syllabus policy | proposal cap | feedback window 3-5 天 | LMS / project tracker |
| Training capstone milestone | Week 7 L14 后 | Week 8 L16 前 | syllabus policy | milestone cap | mentor feedback window 3-5 天 | LMS / project tracker |
| Inference capstone proposal | Week 9 L17 后 | Week 9 L18 前 | syllabus policy | proposal cap | feedback window 3-5 天 | LMS / project tracker |
| Final report/poster | Week 10 L19 后 | 学校期末提交窗口 | syllabus policy | final project cap | final regrade window | LMS / project tracker |
| Guest speaker reflection | Week 8-10 guest lecture 后 24 小时内 | 活动后 7 天内 | participation policy | accessibility alternative allowed | feedback response window 7 天 | LMS / course site |

## 变更控制

| 变更类型 | 最低公告要求 | 需要同步更新 |
|----------|--------------|--------------|
| release_at 改动 | 说明新发布时间和原因 | 本台账、materials index、LMS |
| due_at 延后 | 说明影响范围、late day 是否消耗、已提交学生如何处理 | 本台账、syllabus、Gradescope |
| due_at 提前 | 默认不允许；若学校校历强制变化，至少提前一周公告 | 本台账、syllabus、LMS、discussion forum |
| regrade window 改动 | 说明成绩发布批次和新窗口 | 本台账、grading calibration、Gradescope |
| assessment window 改动 | 说明 assessment_id、allowed materials、makeup 和受影响学生 | 本台账、assessment administration policy、LMS |
| hidden test 或 rubric 改动 | 说明是否影响已提交作业和统一处理方式 | assignment guide、autograder notes、operations log |
| project deadline 改动 | 说明团队 late day、mentor feedback 和 compute window 的影响 | project guide、mentor tracker、compute guide |

## Release Freeze

| 时间点 | 冻结内容 | 允许改动 |
|--------|----------|----------|
| 作业 release 前 24 小时 | README、starter API、公开 tests、rubric、submission instructions | 拼写、链接、环境说明 |
| 作业 due 前 24 小时 | 公开测试、rubric、提交入口、late policy | 只允许修复阻塞提交的错误，并公告 |
| 项目 due 前 72 小时 | report template、rubric、required eval cases、presentation format | 只允许补充 FAQ 或非必需示例 |
| 期末提交窗口 | final report/poster 要求、regrade policy | 只允许学校级紧急调整 |

## Staff Checklist

| 时间 | 动作 |
|------|------|
| 开课前 | 用学校校历替换 Week-relative due_at，并确认 timezone |
| 每次作业发布前 | 确认 `README.md`、LMS / Gradescope、assignment release manifest 和本台账一致 |
| 每次成绩发布前 | 填写 regrade_open_at、regrade_close_at 和成绩发布公告 |
| 每次计分 assessment 前 | 确认 assessment_id、allowed materials、duration、makeup window 和 accommodation path |
| 每周 staff meeting | 检查下两周 release、due、mentor feedback 和 compute window |
| 期末前 | 冻结 final report/poster 要求，确认 final regrade window |

## 发布前 Checklist

- [课程 Syllabus](syllabus.md) 的作业节奏、迟交和复核口径与本台账一致。
- [Assignment Submission and Release Guide](assignment-submission-guide.md) 的 LMS / Gradescope 发布步骤引用本台账。
- [Capstone Proposal and Milestone Guide](capstone-proposal-milestone.md) 的 proposal、milestone 和 final report 节点能映射到本台账。
- [Course Communication and Announcement Policy](course-communication-policy.md) 明确任何 deadline 改动必须公告。
- [Assessment Administration and Exam Integrity Policy](assessment-administration-policy.md) 明确 quiz/checkpoint 的 allowed materials、makeup、便利安排和诚信边界。
- [Course Operations and Improvement Log](course-operations-log.md) 记录真实开课后的延期、复核和改期原因。
- 运行 `.venv/bin/python verify_course.py`；正式期末发布或站点大改版前运行 `.venv/bin/python verify_course.py --capstone --training`。
