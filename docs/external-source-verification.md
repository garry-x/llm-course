# External Source Verification Guide

本指南用于定期复核课程引用的外部论文、课程官网、官方文档、模型卡、API 文档、benchmark 和价格信息。它补充 [External Source Inventory](external-source-inventory.md)、[Chapter Source and Accuracy Map](chapter-source-map.md)、[Claim Audit Worksheet](claim-audit-worksheet.md)、[Model and Benchmark Card Guide](model-benchmark-card-guide.md)、[Frontier Source Evidence Cards](frontier-source-evidence-cards.md)、[External Expert Review Dossier](external-expert-review-dossier.md)、[前沿模型来源等级与复核记录](frontier-source-audit.md)、[Data and Ethics Review](data-ethics-review.md) 和 [Course Operations and Improvement Log](course-operations-log.md)。

## 适用范围

需要复核的外部来源包括：

- 论文、教材、课程官网和 lecture notes。
- 官方模型卡、技术报告、API 文档和代码仓库。
- 推理框架文档，例如 vLLM、SGLang、TensorRT-LLM、llama.cpp。
- benchmark、leaderboard、模型规格、API 价格、上下文长度、吞吐或显存数字。
- 学生项目报告中引用的数据集、模型、API、第三方库和评测集。

本地 Markdown/HTML 链接由 `verify_course.py` 检查；外部链接是否失效、内容是否变化、声明是否仍被来源支持，需要按本指南人工或半自动复核。

## 复核频率

| 来源类型 | 复核频率 | 原因 |
|----------|----------|------|
| 基础论文和教材 | 每次大改版 | 内容稳定，但引用位置可能变化 |
| 课程官网和公开作业页 | 每轮开课前 | 年份、作业结构、政策可能更新 |
| 官方模型卡和技术报告 | 每次引用前沿模型前 | 模型状态、参数、上下文和评测可能变化 |
| API 文档和价格 | 每次课程发布前 | 价格、限流、模型名、计费单位变化快 |
| benchmark / leaderboard | 每次使用数字前 | 任务、shot 数、评测版本和污染风险变化 |
| 框架文档 | 每次涉及安装、性能或 API 行为时 | 版本兼容性和参数名变化快 |

## 复核记录字段

每次复核至少记录：

| 字段 | 要求 |
|------|------|
| Claim | 课程正文、作业或项目报告中的具体声明 |
| Location | 文件、章节、表格或作业位置 |
| Source URL | 外部链接 |
| Source type | paper / official docs / model card / API docs / benchmark / course page |
| Access date | 访问日期 |
| Evidence | 来源中支持该 claim 的摘要，不复制长段原文 |
| Boundary | 来源没有支持的更强结论 |
| Action | keep / revise / downgrade / remove / replace source |
| Owner | 复核人 |

## 复核流程

1. 找到 claim 的最小表述，不复核一整段模糊描述。
2. 打开外部来源，确认链接可访问、页面仍是目标内容。
3. 检查来源是否支持 claim 的数字、条件、日期、版本、任务和评测设置。
4. 若来源只支持案例或模型卡声明，正文必须写成“某来源报告/声明”，不能写成普遍事实。
5. 若来源失效，优先寻找同一作者、机构或官方镜像；找不到则降级或删除 claim。
6. 更新 [Chapter Source and Accuracy Map](chapter-source-map.md) 或 [前沿模型来源等级与复核记录](frontier-source-audit.md)。
7. 对会影响正文、作业、测验或项目评分的 claim，填写 [Claim Audit Worksheet](claim-audit-worksheet.md)。
8. 运行 `.venv/bin/python verify_course.py`；涉及 capstone 或训练代码时运行 `.venv/bin/python verify_course.py --capstone --training`。

### CS224N 当前页半自动复核

CS224N 对标页属于“课程官网和公开作业页”，每轮开课前必须重新访问。可用以下命令生成可归档 manifest：

```bash
.venv/bin/python scripts/verify_cs224n_snapshot.py --json-out cs224n-snapshot-2026-06-05.json
```

通过条件：

- `status` 为 `pass`。
- `matched_marker_count` 等于 `expected_marker_count`。
- manifest 中包含 `Stanford / Winter 2026`、Assignments、Final Project、Participation、late/regrade、AI Tools Policy、Python/PyTorch/Hugging Face tutorial、Benchmarking and Evaluation、Reasoning、Tokenization and Multilinguality、Interpretability、Social and Broader Impacts、Multimodality、Open Questions 和 Final Project Poster Session 等 marker。

若脚本失败，不要只改 marker 让脚本通过；应先人工检查官方页面变化，再更新 [CS224N Current Benchmark Snapshot](cs224n-current-benchmark-snapshot.md)、[CS224N Benchmark Crosswalk](cs224n-benchmark-crosswalk.md)、[Frontier Seminar Handout](frontier-seminar-handout.md) 和课程运行日志。

### Frontier Source Evidence 半自动复核

DeepSeek/V3.2/V4 等前沿来源属于易变来源。每轮开课前或修改 [Frontier Source Evidence Cards](frontier-source-evidence-cards.md) 后，运行：

```bash
.venv/bin/python scripts/verify_frontier_sources.py --json-out frontier-sources-2026-06-05.json
```

通过条件：

- `status` 为 `pass`。
- `deepseek_v32_exp_api_news`、`deepseek_v4_pro_model_card`、`deepseek_v2_arxiv` 和 `deepseek_v3_arxiv` 均通过。
- required markers 全部匹配。
- monitor-only 的 absent markers 没有在已检查来源中出现。

若 required marker 缺失，先人工检查官方页面和模型卡是否变化，再更新 evidence card、frontier audit 和 source inventory。若 absent marker 出现，不能自动升级为课程事实；必须新增带访问日期、来源 URL、边界和 student use 的 evidence card。

## 外部链接失效处理

| 情况 | 处理 |
|------|------|
| 官方页面迁移 | 更新链接，并记录旧链接和新链接 |
| arXiv / ACL / NeurIPS 页面可用但 PDF 链接变动 | 链接到稳定 landing page |
| 模型卡删除或权限变化 | 降级 claim，不再作为作业事实 |
| API 文档改版 | 更新模型名、字段、价格或限制；保留访问日期 |
| benchmark 页面更新 | 检查任务版本、shot 数、评测集和提交日期 |
| 第三方博客失效 | 不寻找非官方转载作为 A 级证据 |

## 高风险 Claim Checklist

以下 claim 不得在没有复核记录时进入正文、作业或考试：

- 参数量、激活参数、上下文长度、训练 token 数、GPU hours。
- latency、tokens/s、FLOPs、KV cache、显存节省比例。
- benchmark 排名、准确率、pass rate、NIAH 或其他长上下文数字。
- API 价格、计费单位、rate limit、可用模型名。
- “某模型已替代某系列”“某技术是唯一/最佳方案”等解释性结论。

## 学生项目复核

学生项目报告中的外部来源按以下规则评分：

- 数据集和模型/API 必须有链接、版本或访问日期。
- benchmark 数字必须说明任务、评测版本、prompt/shot 设置和是否可能污染。
- 使用外部库必须说明版本、功能范围和学生自己的贡献。
- 若引用失效但项目结论依赖该来源，报告不能拿满“表达与引用”或“数据与伦理”分。

## 复核日志样例

| Date | Claim | Location | Source URL | Source type | Access date | Action | Owner |
|------|-------|----------|------------|-------------|-------------|--------|-------|
| 2026-06-05 | CS224N public page still lists Winter 2026 schedule, assignment weight, final project weight, participation weight, AI tools policy, and topic markers used by this course benchmark | `docs/cs224n-current-benchmark-snapshot.md`; `docs/cs224n-benchmark-crosswalk.md` | `https://web.stanford.edu/class/cs224n/` | course page | 2026-06-05 | keep; archive `cs224n-snapshot-2026-06-05.json`; rerun before each live offering | Course Staff |
| 2026-06-05 | API price, model availability, context length, benchmark rank, and latency claims are volatile and must not be treated as stable course facts without a dated source card | model benchmark cards, frontier seminar handout, capstone reports | official model/API docs or model card used by the specific claim | API docs / model card / benchmark | 2026-06-05 | downgrade if no dated primary or official source exists | Instructor |

## 发布前 Checklist

| 检查项 | 通过标准 |
|--------|----------|
| source inventory | 外部来源类型、层级和课程用途已列入 inventory |
| source map | 修改过的章节在 source map 中有对应来源 |
| claim audit | 高风险 claim 有 claim、source、boundary、action 和 student-facing use |
| frontier audit | DeepSeek/新模型/API/benchmark claim 有复核日期 |
| frontier evidence | `.venv/bin/python scripts/verify_frontier_sources.py --json-out ...` 生成 pass manifest |
| access date | 项目和阅读引用包含访问日期 |
| unstable facts | API 价格、模型规格和 leaderboard 数字重新查证 |
| CS224N snapshot | `.venv/bin/python scripts/verify_cs224n_snapshot.py --json-out ...` 生成 pass manifest |
| local verification | `.venv/bin/python verify_course.py` 通过 |
