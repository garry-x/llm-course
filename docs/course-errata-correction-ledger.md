# Course Errata and Correction Ledger

复核日期：2026-06-05

本台账用于记录课程正文、作业、测试、项目指南、来源引用、公式、代码片段、slides/notes 和学生站点发布包中的错误报告、影响评估、修订动作、公告与验证证据。它补充 [Course Communication and Announcement Policy](course-communication-policy.md)、[Material Versioning and Archive Policy](material-versioning-archive-policy.md)、[Course Operations and Improvement Log](course-operations-log.md)、[Chapter Claim Audit Ledger](chapter-claim-audit-ledger.md)、[Claim Audit Worksheet](claim-audit-worksheet.md)、[External Source Verification Guide](external-source-verification.md)、[External Expert Review Dossier](external-expert-review-dossier.md)、[Lecture Notes Quality and Review Standard](lecture-notes-quality-review.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md)、[Private Autograder Operations Guide](private-autograder-operations.md) 和 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md)。

目标是把“发现错误 -> 判断影响 -> 修订材料 -> 公告学生 -> 重新验证 -> 处理评分影响”做成可追踪闭环。若错误影响评分、截止时间、提交入口、测试口径、项目要求或课程政策，正式变更必须通过课程公告发布。

## Severity Levels

| severity | 定义 | 最低处理 |
|----------|------|----------|
| S0 blocker | 阻止大部分学生提交、运行或访问正式材料 | 24 小时内公告 workaround；修复后重新发布并记录受影响范围 |
| S1 grading-impacting | 影响评分、rubric、隐藏测试、公开测试、截止时间或项目要求 | 公告、修订材料、批量复核或补测窗口、运行 verifier |
| S2 conceptual | 公式、shape、来源边界、概念解释或代码片段有误，但不直接改变已评分结果 | 修订材料、记录 claim/source impact、必要时发布勘误 |
| S3 presentation | typo、排版、链接文本、图注或非评分说明错误 | 修订材料；若学生已被误导，加入公告或 FAQ |
| S4 source-drift | 外部链接、模型卡、API、benchmark、价格、context 或框架行为更新 | 按 source verification 复核，更新来源等级、访问日期和边界 |

## Ledger Schema

| field | required_content |
|-------|------------------|
| errata_id | 稳定 ID，例如 `ERR-2026-06-05-CH02-01` |
| reported_at | 报告日期 |
| reporter_channel | public forum、private email、office hours、staff review、verifier、student release smoke |
| affected_material | 章节、作业、测试、rubric、project guide、source map、slide/note 或 release 包 |
| severity | S0 / S1 / S2 / S3 / S4 |
| issue_summary | 最小可复核问题描述 |
| impact_scope | 影响哪些学生、提交、评分项、章节或项目 claim |
| correction_action | keep / clarify / patch / replace / retire / regrade / announce |
| verification_evidence | 命令、人工审查、source verification 或 release smoke 证据 |
| announcement_status | not_needed / draft / posted / posted_with_regrade / posted_with_workaround |
| owner | 负责人 |
| status | open / fixed_pending_verify / fixed_announced / closed |

## Current Errata Ledger

| errata_id | reported_at | reporter_channel | affected_material | severity | issue_summary | impact_scope | correction_action | verification_evidence | announcement_status | owner | status |
|-----------|-------------|------------------|-------------------|----------|---------------|--------------|-------------------|----------------------|---------------------|-------|--------|
| ERR-2026-06-05-CH02-01 | 2026-06-05 | student report | `chapters/ch02.html` formula text | S2 conceptual | 类比推理段落出现 malformed `\text{vec(` 公式片段 | Ch02 lecture/reading；未影响作业测试 | patch | `.venv/bin/python verify_course.py` passed; formula attribute scan passed | not_needed | Course Staff | closed |
| ERR-2026-06-05-WORDING-01 | 2026-06-05 | verifier | `docs/dataset-model-artifact-registry.md` release checklist | S3 presentation | release wording gate flagged informal draft-style artifact wording | student release docs wording only | clarify | `.venv/bin/python verify_course.py` passed after wording update | not_needed | Course Staff | closed |
| ERR-2026-06-05-ARTIFACT-REGISTRY-01 | 2026-06-05 | staff review | project data/model artifact provenance | S2 conceptual | project datasets, model cards, checkpoints and runtime assets lacked one asset-level registry | final project/capstone provenance review | replace | `check_dataset_model_artifact_registry()` passed; evidence manifest marker check passed | not_needed | Course Staff | closed |
| ERR-2026-06-05-PROJECT-DOSSIER-01 | 2026-06-05 | staff review | project submission process | S2 conceptual | proposal/milestone/final report evidence existed but lacked one submission dossier | project grading and TA review workflow | replace | `check_project_submission_dossier()` passed; evidence manifest marker check passed | not_needed | Course Staff | closed |

## Intake and Triage Workflow

| step | action | evidence |
|------|--------|----------|
| T1 intake | 记录报告渠道、原始位置、最小复现和 reporter 可见性 | forum link、email summary、office-hours note 或 verifier output |
| T2 classify | 判定 severity、是否影响评分、是否涉及来源 drift、是否需私密处理 | Severity Levels + privacy boundary |
| T3 owner | 指派 content owner、assignment owner、source owner、autograder owner 或 course manager | owner 字段 |
| T4 patch plan | 决定 clarify、patch、replace、retire、regrade、announce 或 workaround | correction_action |
| T5 verify | 运行相关测试、source verification、browser smoke 或人工审查 | verification_evidence |
| T6 announce | 若影响评分、deadline、提交入口、测试口径、项目要求或政策，发布公告 | announcement_status |
| T7 close | 同步 operations log、source/claim audit、gradebook/LMS 或 release manifest | status = closed |

## Announcement Template

```text
Subject:
Errata ID:
Affected material:
What changed:
Who is affected:
Student action:
Grading or deadline impact:
Verification command or evidence:
Updated documents:
Regrade or support path:
```

公告不得包含学生个人身份、私密提交、hidden test 输入、`reference_solution.py`、API key、私有路径或未授权数据。

## SLA and Escalation

| severity | first response | correction target | escalation |
|----------|----------------|-------------------|------------|
| S0 blocker | same day | 24 hours | Instructor + Course Manager + Autograder Contact |
| S1 grading-impacting | 1 business day | before next grading action | Instructor + Head TA + Gradebook Owner |
| S2 conceptual | 2 business days | next lecture or next release | Content Owner + Source Owner |
| S3 presentation | 5 business days | next minor release | Content Owner |
| S4 source-drift | 2 business days for volatile claims | before citing updated number | Source Owner + Instructor |

## Cross-Update Rules

| error_type | must_update |
|------------|-------------|
| formula / derivation error | affected chapter, [Mathematical Derivation Audit](mathematical-derivation-audit.md), written problem or board derivation if used |
| source or frontier claim drift | [Chapter Source and Accuracy Map](chapter-source-map.md), [Chapter Claim Audit Ledger](chapter-claim-audit-ledger.md), [External Source Inventory](external-source-inventory.md), frontier audit if relevant |
| assignment API or test bug | assignment README/tests, assignment release manifest, hidden-test operations, gradebook/regrade note |
| project rubric or dossier ambiguity | project guide, project submission dossier, report template, rubric and announcement |
| site release or rendering bug | site release builder, browser smoke, material versioning/archive record |
| grading-impacting issue | course announcement, gradebook/LMS operations, regrade window and operations log |

## Student-Facing Report Form

Students should include:

```text
Affected file or page:
Section, exercise, or line if visible:
What seems wrong:
Why it matters:
Minimal reproduction or screenshot:
Whether it affects a submission or grade:
Can this be discussed publicly? yes/no
```

Do not include hidden test inputs, full reference solutions, other students' code, API keys, private data, private logs, or personal sensitive information in a public report.

## Release Checklist

| 检查项 | 通过标准 |
|--------|----------|
| severity coverage | S0-S4 severity levels define response and correction expectations |
| ledger schema | errata_id、reported_at、channel、affected_material、severity、impact、action、verification、announcement、owner 和 status 均可记录 |
| current ledger | 至少记录当前轮次已处理的 content, release wording, artifact registry 和 project dossier 修订 |
| workflow closure | intake、classify、owner、patch plan、verify、announce、close 七步完整 |
| cross-update rules | formula、source、assignment、project、site release 和 grading-impacting issue 均有同步规则 |
| linked governance | communication、versioning、operations log、claim audit、source verification、lecture notes、assignment release、autograder 和 gradebook 均链接本文件 |
| verifier gate | `verify_course.py` 检查 severity、schema、ledger rows、SLA、cross-update rules、report form、链接和 release inclusion |
