# Course Operations and Improvement Log

学习数据触发补救教学、project clinic、FAQ 更新或评分校准的阈值与隐私边界见 [Learning Analytics and Remediation Plan](learning-analytics-remediation-plan.md)；讲后 quick check、exit ticket、office hours、作业失败类别、阅读复盘和项目 milestone 如何转成下一讲调整，见 [Weekly Teaching Reflection and Adjustment Log](weekly-teaching-reflection-adjustment-log.md)；课程目标 direct/indirect evidence、达标阈值和下一轮改进动作见 [Learning Outcome Attainment Report](learning-outcome-attainment-report.md)；课堂同行观察、期中/期末课程评估和 response memo 闭环见 [Teaching Observation and Course Evaluation Dossier](teaching-observation-course-evaluation.md)；独立专家复核范围、严重度和闭环状态见 [External Expert Review Dossier](external-expert-review-dossier.md)；每周 workload、难度阶梯、超载信号和 10/12 周节奏调整见 [Workload and Pacing Calibration](workload-pacing-calibration.md)。

本文件用于每轮开课期间持续记录课程运行证据，并把学生反馈、测试失败、评分争议、项目复现和来源更新转化为可追踪的改进任务。它补充 [Course Outcome Map](course-outcome-map.md)、[Student FAQ and Troubleshooting Guide](student-faq-troubleshooting.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md)、[Discussion Section and Office Hours Guide](discussion-office-hours-guide.md)、[Grading Calibration Guide](grading-calibration.md)、[Grading Drift Audit Ledger](grading-drift-audit-ledger.md)、[Compute Resource and Cost Guide](compute-resource-guide.md)、[Data and Ethics Review](data-ethics-review.md)、[Course Errata and Correction Ledger](course-errata-correction-ledger.md)、[Pre-Semester Readiness Audit](presemester-readiness-audit.md) 和 [前沿模型来源等级与复核记录](frontier-source-audit.md)。

开课前 readiness evidence packet 见 [Pre-Semester Readiness Audit](presemester-readiness-audit.md)。该文件记录 CS224N current snapshot verifier、课程总门禁、release safety、browser smoke、作业测试和人工 sign-off 边界；作业公开测试 readiness marker 为 `ASSIGNMENT TESTS: PASS (11 suite(s))`。机器可读 evidence manifest 由 `scripts/generate_course_evidence_manifest.py --check --json-out ...` 生成，并应与每次开课前 readiness 记录一起归档。

## 使用范围

每周课程结束后由主讲教师或助教更新一次；每次作业发布、成绩发布、项目 milestone、复核截止和前沿资料更新后也应补充对应记录。记录目标不是存档所有聊天内容，而是保留能改善课程质量、评分一致性和复现能力的证据。当前记录使用 `dry-run baseline` 标注开课前可验证证据；真实开课后应追加 `live offering` 行，而不是覆盖 dry-run 行。

## 每周运行记录

| 周次 | 日期 | 章节/讲次 | 课堂 quick check 通过率 | Exit ticket 高频困惑 | 计划调整 | 负责人 |
|------|------|-----------|-------------------------|----------------------|----------|--------|
| Week 1 | 2026-06-05 dry-run baseline | Ch01-Ch02 | readiness proxy: quiz/checkpoint guide and lecture plan linked | likely themes: BPE merge boundary, embedding lookup shape, RoPE norm vs semantic claim | add WTR-2026-L02-ROPE recap and keep Ch02 source-boundary wording under review | Instructor |
| Week 2 | 2026-06-05 dry-run baseline | Ch03 | readiness proxy: attention assignment public tests pass through verifier | likely themes: causal mask broadcast, mask-before-softmax order, attention score shape | route WTR-2026-L03-MASK to recitation worksheet and quick check | Discussion TA |

填写要求：

- 高频困惑至少聚合为 2-4 个主题，例如 shape、mask、梯度、评测口径、来源边界。
- 计划调整必须指向具体材料，例如章节段落、作业 README、讨论课 drill 或 office-hour 示例。
- 若 quick check 通过率低于 70%，下一次课前应安排 5-10 分钟 recap。

## Quiz 与阶段 Checkpoint 记录

| 时间 | 类型 | 覆盖范围 | 平均通过率 | 低分模块 | 补救动作 | 负责人 |
|------|------|----------|------------|----------|----------|--------|
| Week 5 | Midterm checkpoint dry run | Ch01-Ch07 | readiness proxy: assessment item bank, written problems, and public tests aligned | likely modules: mask direction, GQA cache units, CE label shift, AdamW update order | prepare recap set from concept-misconception map and worked examples | Instructor |
| Week 9 | Capstone checkpoint dry run | Ch08-Ch10 and project evidence | readiness proxy: inference capstone acceptance pass | likely modules: TTFT/TPOT separation, RAG retrieval evidence, SLO capacity assumptions | require project dossier metric card and benchmark configuration before final demo | Project Mentor |

记录要求：

- quick check、recap quiz 和 midterm checkpoint 的题目设计按 [Quiz and Checkpoint Guide](quiz-checkpoint-guide.md) 执行。
- 只记录聚合通过率和低分模块，不公开个人排名。
- 若某模块低于 70%，下一讲或讨论课必须安排 recap，并给出补救材料。

## Demo Dry Run 记录

| 讲次 | Demo | 命令或形式 | 结果 | 失败原因 | 修复动作 | 负责人 |
|------|------|------------|------|----------|----------|--------|
| L1 | BPE merge dry run | `.venv/bin/python assignments/ch01_bpe/tests.py` | PASS in course verifier | no demo failure in readiness run | keep board fallback showing non-overlapping pair merge | Instructor |
| L3 | Attention mask dry run | `.venv/bin/python assignments/ch03_attention/tests.py` | PASS in course verifier, one plotting test skipped when matplotlib unavailable | optional plotting dependency only | teach core mask behavior without relying on matplotlib | Discussion TA |
| L18 | Inference capstone smoke | `.venv/bin/python verify_course.py --capstone --training` | PASS in readiness evidence | no SLO failure in dry-run configuration | rerun after project code changes and before milestone publication | Project Mentor |

记录要求：

- dry run 按 [Classroom Demo Runbook](demo-runbook.md) 执行。
- 失败原因按 environment、path、shape、dtype、numerical、dependency、policy 分类。
- 若课堂前无法修复，应准备 board-work 备用方案，不临场依赖不稳定 demo。

## 作业复盘记录

| 作业 | 发布日期 | 提交人数 | 公开测试中位通过率 | 迟交/环境问题 | 题意问题 | 后续修改 |
|------|----------|----------|--------------------|---------------|----------|----------|
| ch01_bpe | 2026-06-05 dry-run baseline | no live submissions | reference solution public suite 9/9 | no live late/environment data; README command checked | likely confusion: non-overlapping merge and byte decode errors | keep BPE worked example and FAQ command self-check |
| ch02_embeddings | 2026-06-05 dry-run baseline | no live submissions | reference solution public suite 8/8 | no live late/environment data; PyTorch available in `.venv` | likely confusion: RoPE relative score property vs monotonic decay | keep Ch02 claim audit and WTR-2026-L02-ROPE recap |

复盘时至少检查：

- 学生是否能按 README 中的命令运行公开测试。
- 失败集中在算法理解、数值容差、shape、dtype、边界输入、依赖环境还是提交格式。
- 是否需要在 handout 中增加反例、输入输出 shape、禁止假设或评分说明。

## 隐藏测试统计

| 作业 | 隐藏边界测试通过率 | 隐藏性质测试通过率 | Top 3 失败类别 | 是否疑似过窄公开测试 | 调整动作 |
|------|--------------------|--------------------|----------------|----------------------|----------|
| ch02_embeddings | private-run required before live grading | private-run required before live grading | expected categories: odd dimension rejection, norm preservation tolerance, relative-position score invariance | public tests cover core properties; private edge cases remain staff-side | archive hidden-run manifest in private storage and keep private autograder manifest outside student release |
| ch03_attention | private-run required before live grading | private-run required before live grading | expected categories: bool/additive mask handling, all-future masking, score scaling dtype | public tests cover 2D/3D masks; private pathological masks remain staff-side | compare hidden category rates with WTR-2026-L03-MASK |

处理规则：

- 不记录隐藏输入原文，只记录失败类别和 rubric 映射。
- 若隐藏通过率远低于公开通过率，优先检查公开测试是否缺少边界或性质测试。
- 若同一隐藏项大面积失败且题意不清，应修订题面并对受影响学生统一处理。

## 讨论课与 Office Hours 记录

| 周次 | 讨论课主题 | Office Hours 高频问题 | 典型最小复现 | 已更新材料 | 未解决问题 |
|------|------------|-----------------------|--------------|------------|------------|
| Week 2 | causal mask and attention shape dry run | likely: `[B,T,T]` vs `[B,H,T,T]`, `-inf` masking, softmax axis | `assignments/ch03_attention/tests.py::test_mask_blocks_positions_for_2d_and_3d_masks` | `weekly-teaching-reflection-adjustment-log.md`, `recitation-worksheet-pack.md` | live offering will confirm whether FAQ needs a mask broadcast entry |
| Week 5 | training-loop debugging dry run | likely: device mismatch, missing `zero_grad`, validation mode, label shift | `assignments/ch07_training/tests.py` public suite | `programming-assignment-code-quality-rubric.md`, `learning-analytics-remediation-plan.md` | live offering will confirm if optimizer trace needs extra worksheet |

记录口径：

- 高频问题按概念、代码、环境、项目设计、评分政策、引用规范分类。
- 最小复现只保留命令、报错摘要、输入形状和定位结论，避免记录个人隐私。
- 更新材料应链接到具体文件或章节，例如 `chapters/ch03.html`、作业 README 或 `docs/math-prerequisites.md`。

## 学生 FAQ 更新记录

| 日期 | 来源 | 高频问题 | FAQ 更新位置 | 是否需要公告 | 负责人 |
|------|------|----------|--------------|--------------|--------|
| 2026-06-05 | dry-run review of assignment commands | students may run system Python instead of `.venv/bin/python` | `student-faq-troubleshooting.md` environment self-check | Yes, include in first-week announcement | Course Staff |
| 2026-06-05 | dry-run review of hidden-test boundaries | students may ask for hidden input details after public tests pass | `student-faq-troubleshooting.md` and `assignment-submission-guide.md` integrity boundary | No separate announcement; include in assignment release note | Head TA |

记录要求：

- 只记录可公开、已脱敏的共性问题。
- 若同一问题一周内出现 3 次以上，应更新 [Student FAQ and Troubleshooting Guide](student-faq-troubleshooting.md) 或作业 README。
- 若 FAQ 更新影响评分、迟交、复核或学术诚信，必须同步更新 syllabus 或 course policies。

## 项目复现记录

| 项目 | Milestone | 复现命令 | 结果 | 失败原因 | 数据/伦理问题 | 修复要求 |
|------|-----------|----------|------|----------|---------------|----------|
| training capstone | readiness acceptance | `.venv/bin/python verify_course.py --training` | PASS through full verifier evidence | no dry-run failure; CPU path used | sample corpus provenance recorded; live projects must add dataset cards | rerun after project code changes; require project submission dossier |
| inference capstone | readiness acceptance | `.venv/bin/python verify_course.py --capstone` | PASS through full verifier evidence | no dry-run SLO failure | mock/API boundary documented; live projects must add data and safety review | rerun before final showcase; require benchmark card and SLO report |

复现检查至少覆盖：

- 提交包是否包含 README、固定 seed、环境说明、日志、metrics、报告和必要数据说明。
- 训练项目是否能恢复 checkpoint 并解释 loss、tokens/s、成本和失败曲线。
- 推理项目是否能跑 health、eval、benchmark、SLO、capacity plan，并解释延迟和成本。
- 数据与伦理审查是否覆盖许可证、PII、偏见、污染、安全边界和残余风险。

## 算力额度与成本记录

| 日期 | 项目/队伍 | 资源 | 额度或运行时长 | 估算成本 | 失败重跑 | 降级路径 | 负责人 |
|------|-----------|------|----------------|----------|----------|----------|--------|
| 2026-06-05 | training capstone readiness | CPU | 12 acceptance steps in local `.venv` | local dry-run cost not billed | no repeated failure | keep CPU fallback and small corpus path | Instructor |
| 2026-06-05 | inference capstone readiness | mock engine on local CPU | acceptance eval plus benchmark smoke | local dry-run cost not billed | no repeated failure | keep mock engine before requiring vLLM/SGLang/TensorRT-LLM | Project Mentor |

记录要求：

- 资源字段和成本口径按 [Compute Resource and Cost Guide](compute-resource-guide.md) 执行。
- 只记录项目级额度和成本，不公开个人账号、API key、账单截图中的敏感信息。
- 若同一配置反复失败，应要求项目降级或修改实验设计，而不是继续消耗共享额度。
- 若使用外部云、公司账号或个人 API key，报告中必须披露但评分不得奖励资源优势本身。

## 阅读复盘与来源审计记录

| 周次 | 阅读材料 | 高质量样例 | 常见问题 | 来源边界争议 | 需要更新的课程 claim |
|------|----------|------------|----------|--------------|-----------------------|
| Week 1 | BPE and word vector readings dry run | recap includes claim, method, limitation, and code link | likely: treating greedy BPE as globally optimal | BPE compression intuition must stay heuristic-scoped | keep Ch01 source audit wording and reading question bank prompt |
| Week 8 | classic NLP and evaluation readings dry run | recap distinguishes metric definition, dataset split, and model-quality claim | likely: BLEU/ROUGE/F1 used without task boundary | metric names cannot stand in for evidence quality | add WTR-2026-L15-EVAL metric-card mini case |

审计重点：

- 学生是否能区分论文、官方文档、模型卡、博客和二手解读。
- 复盘是否把论文主张连接到课程代码、实验限制或评测指标。
- 前沿模型相关主张是否需要更新复核日期、来源等级或降级表述。

## 课堂参与与反馈调查记录

| 时间 | 证据来源 | 提交/参与率 | 高频反馈 | 已采取动作 | 暂不改变原因 |
|------|----------|-------------|----------|------------|--------------|
| Week 5 | midterm feedback dry-run protocol | live participation pending | likely: workload density around Ch06-Ch07 and project proposal timing | teaching-observation dossier includes CE-2026-MID-WORKLOAD response path | keep 10-week path but document 12-week expansion option |
| Week 10 | final course review dry-run protocol | live participation pending | likely: project reproducibility and source-boundary confidence | project submission dossier and defense bank require artifact and claim evidence | no live data yet; update after first offering |

记录要求：

- 只记录聚合反馈，不记录学生个人身份或敏感信息。
- 期中反馈后一周内给学生发布聚合回应。
- 反馈动作应指向具体材料、讨论课、作业 README、rubric、staff runbook 或支持渠道。
- 若学校不允许将反馈调查计入分数，应在 [Participation and Feedback Guide](participation-feedback-guide.md) 中改为不计分但保留改进流程。

## 复核与评分争议记录

| 日期 | 作业/项目 | 争议类型 | 初评依据 | 复核结论 | 是否影响其他学生 | 后续校准 |
|------|-----------|----------|----------|----------|------------------|----------|
| 2026-06-05 | ch02_embeddings dry-run | possible ambiguity in RoPE property wording | public tests require norm and relative-position score invariance, not monotonic decay | wording already scoped by claim audit; monitor live questions | if many students cite monotonic decay, issue class-wide clarification | align rubric note with notation/shape glossary |
| 2026-06-05 | capstone dry-run | possible SLO metric configuration mismatch | acceptance report separates TTFT, TPOT, P95 latency, tokens/s, and capacity | require benchmark configuration in project report | applies to all project teams | calibrate capstone defense question sampling |

争议类型建议使用：测试误判、题意不清、环境差异、人工评分不一致、引用/协作边界、迟交政策、隐藏测试边界。

## 前沿来源更新记录

| 日期 | 主题 | 旧表述 | 新来源 | 来源等级 | 处理方式 | 负责人 |
|------|------|--------|--------|----------|----------|--------|
| 2026-06-05 | CS224N current benchmark snapshot | 手工快照缺少可执行 manifest | `https://web.stanford.edu/class/cs224n/` + `scripts/verify_cs224n_snapshot.py` | C-background | 保留并新增半自动复核脚本；38/38 marker matched | Course Staff |
| 2026-06-05 | Frontier source evidence cards | 前沿模型 claim 只有等级表，缺少逐条 source card | `frontier-source-evidence-cards.md` | A-volatile / unsupported | 新增 DSA、V4 参数/context、CSA+HCA、reasoning modes 和 D 级 monitor-only 证据卡 | Course Staff |
| 2026-06-05 | Frontier source verifier | 前沿 evidence card 缺少可重复官方页 marker 检查 | `scripts/verify_frontier_sources.py --json-out frontier-sources-2026-06-05.json` | A-volatile / B-implementation | 新增半自动 verifier；4/4 source checks pass，monitor-only absent markers 未出现 | Course Staff |
| 2026-06-05 | Course readiness evidence | readiness 证据分散在文档和命令输出中 | `scripts/generate_course_evidence_manifest.py --check` | C-background | 机器可读 evidence manifest 通过：111 required evidence files、63 marker checks、0 missing files/markers；全部 `COURSE_DOCS` `docs/*.md` 已进入 manifest，并覆盖 syllabus、lecture plan、reading list、written/instructor/grading packet、source inventory 和 classic NLP deep-dive evidence | Course Staff |
| 2026-06-05 | Course operations evidence | 运行日志以空模板为主 | `course-operations-log.md` dry-run baseline records | C-background | 改写为带日期、证据口径、owner 和 live-offering follow-up 的运行记录 | Course Staff |

更新规则：

- API 价格、模型规格、benchmark、模型卡和推理框架能力属于易变信息，改动前应重新查证。
- 未找到 A 级来源的前沿数字不得作为稳定事实写入正文。
- 外部来源复核字段和失效处理按 [External Source Verification Guide](external-source-verification.md) 执行。
- 每次来源更新后运行 `.venv/bin/python verify_course.py`，并检查相关章节公式、链接和来源映射。

## 改进任务看板

| 状态 | 优先级 | 来源 | 任务 | 验收标准 | Owner | Due |
|------|--------|------|------|----------|-------|-----|
| Backlog | High | 隐藏测试统计 | 每次作业发布后记录公开/隐藏测试通过率和高频失败类别 | 下一次作业说明或讨论课材料引用该统计 | Course Staff | 每次作业复盘后 |
| In Progress | Medium | Office Hours | 汇总 shape、mask、环境和 capstone 设计类高频问题 | Student FAQ 或 Discussion Guide 至少更新 1 条对应说明 | TA Lead | 每周 staff meeting 前 |
| Done | Low | 阅读复盘 | 建立来源等级、核心结论和复现实验建议的阅读复盘模板 | Reading List 和 Participation Guide 均引用该模板 | Instructor | 开课前 |

任务进入 Done 前必须满足：

- 有对应材料、测试、rubric 或政策文件的实际修改。
- 有验证命令或人工审查证据。
- 若影响评分，已同步到评分校准或作业发布流程。

## 期末课程复盘

| 项目 | 证据 | 结论 | 下一轮动作 |
|------|------|------|------------|
| 学习目标达成 | Outcome Map + dry-run verifier + project readiness evidence | design_ready; real student attainment still requires live direct/indirect evidence | collect gradebook aggregate, project rubric sample, and course evaluation after first offering |
| 作业质量 | public assignment tests + hidden-test design + code-quality rubric | public suite and rubrics ready; private hidden-run evidence remains staff-side | archive private autograder manifest and compare failure categories after each release |
| 授课节奏 | lecture plan + weekly reflection log + workload calibration | 10-week path documented with 12-week expansion option | update WTR records after each lecture and publish category-level response when needed |
| 项目复现 | capstone acceptance + project submission dossier + report rubric | training and inference readiness pass; live project quality needs human review | require artifact manifest, metric card, claim audit, and defense record |
| 来源准确性 | source map + frontier audit + CS224N snapshot verifier | source governance ready with dated snapshot and review cadence | rerun source verifier before each offering and after volatile API/model claims change |

期末复盘应产出下一轮开课的 3-7 个高优先级任务，并同步到本文件的改进任务看板。
