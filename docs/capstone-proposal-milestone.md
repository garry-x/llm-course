# Capstone Proposal and Milestone Guide

本指南用于把两个 capstone 从“最终报告一次性交付”拆成可指导、可反馈、可评分的项目流程。它补充 `projects/*/README.md`、[Default Final Project Guide](default-final-project-guide.md)、[Capstone Project Gallery and Idea Bank](capstone-project-gallery.md)、[Project Team and Mentor Policy](project-team-mentor-policy.md)、[Project Report Template and Reproducibility Checklist](project-report-template.md)、[Project Submission Dossier](project-submission-dossier.md)、[Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md)、[Model and Benchmark Card Guide](model-benchmark-card-guide.md)、[Capstone Defense and Oral Exam Question Bank](capstone-defense-oral-exam-bank.md)、[Compute Resource and Cost Guide](compute-resource-guide.md)、`project-report-rubric.md` 和 `presentation-peer-review.md`。

## 交付时间线

| 时间 | 训练工程 Capstone | 推理工程 Capstone | 评分用途 |
|------|-------------------|-------------------|----------|
| 第 5 周 | 训练项目提案 | 选题预登记 | 确认可行性、数据风险和资源预算 |
| 第 7 周 | 训练 milestone | 推理项目提案 | 检查最小闭环、日志和风险 |
| 第 9 周 | 报告草稿与同伴 review | 推理 milestone | 检查 SLO、评测集、容量规划和回归用例 |
| 第 10 周 | 最终报告与展示 | 最终报告与展示 | 按报告 rubric、展示 rubric 和复现包评分 |

提案和 milestone 不替代最终报告。它们的作用是尽早暴露不可复现、指标不清、数据不合规或工程目标过大的问题。

## 项目提案模板

每份提案建议 1-2 页，必须包含以下内容。

### 基本信息

- 项目标题。
- 个人或团队成员。
- 选择的 capstone 方向：训练工程 / 推理工程。
- 项目类型：默认最终项目任务包 / 默认训练工程项目 / 默认推理工程项目 / 自定义项目。
- 一句话目标。
- 最小成功标准。

### 问题定义

- 用户或研究场景。
- 输入和输出。
- 明确非目标：本项目不会解决什么。
- 为什么课程现有章节足以支持这个项目。
- 若为自定义项目，说明它如何符合 [Capstone Project Gallery and Idea Bank](capstone-project-gallery.md) 中的边界和风险要求。

### 数据与来源

- 数据集名称、链接、版本和许可证。
- 数据规模：样本数、token 数或文件大小。
- 数据质量风险：重复、污染、PII、有害内容、语言偏置。
- 若使用合成数据，说明生成方法和人工检查方式。
- 数据和伦理审查按 [Data and Ethics Review](data-ethics-review.md) 提交，最终报告必须包含 `Data, Ethics, and Limitations` 小节。

### 方法与 baseline

- 最小 baseline。
- 计划改变的变量。
- 至少一个 ablation 或对照实验。
- 预期失败模式。

### 评测指标

- 主要指标。
- 辅助指标。
- 指标局限。
- 固定评测样例或回归用例。
- `split_card` 草案：split_id、train/dev/test 用途、dev_policy、test_policy。
- `metric_card` 草案：指标定义、aggregation、局限和适用边界。
- `uncertainty_plan`：bootstrap CI、seed sensitivity、paired comparison、load-test variance 或 single_seed_limit。
- `claim_audit` 草案：哪些结论只能写成 preliminary evidence，哪些 claim 需要显著性或稳健性证据。

提案阶段不要求已经跑完实验，但必须能说明最终报告如何满足 [Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md) 的 significance claim gate。

### 资源与复现计划

- 运行环境：CPU/GPU、内存、依赖版本。
- 预计训练或压测耗时。
- 预计 GPU hours、API 请求数或云额度消耗。
- CPU fallback、小配置 fallback 或 mock engine fallback。
- 若申请共享 GPU/API key，说明为什么 CPU baseline 不足以回答项目问题。
- seed、配置文件和日志路径。
- 最终复现命令。

资源预算、额度公平使用和成本记录按 [Compute Resource and Cost Guide](compute-resource-guide.md) 执行。没有资源预算或降级路径的提案不应批准追加 GPU/API 额度。

### 风险登记表

| 风险 | 可能影响 | 缓解措施 | 触发降级条件 |
|------|----------|----------|--------------|
| 数据过小或质量差 | 指标不稳定 | 增加数据审计和固定验证集 | val loss 或评测方差过大 |
| 资源不足 | 训练或压测跑不完 | 缩小模型、batch 或请求数 | 单次运行超过预算 |
| 指标不匹配目标 | 结论不可解释 | 增加人工失败案例分析 | 指标提升但样例变差 |
| contamination/leakage | 结论虚高或不可复核 | 记录 leakage_check、prompt leakage、retrieval contamination 和 benchmark contamination | 无法排除污染时把结论降级为 diagnostic result |
| uncertainty too high | 小样本或单 seed 造成结论不稳 | 增加 bootstrap、paired comparison、repeated seeds 或明确 single_seed_limit | CI 过宽或不同 seed 方向相反 |

## 训练工程提案加项

训练工程项目必须额外说明：

- 模型规模：层数、hidden size、head 数、参数量估计。
- token 预算：训练 token、batch token、训练 step。
- checkpoint 策略：保存频率、保留数量、resume 验证方式。
- 训练监控：train/val loss、perplexity、lr、grad_norm、tokens/s。
- 数据审计：长度分布、重复样本、异常字符、空行、泄漏风险。

训练工程最小成功标准示例：

- `data_audit.py` 输出可解释的数据统计。
- `train.py` 至少完成 1 次验证并写入 metrics。
- checkpoint resume 后 `step` 单调增加。
- 报告能解释一次 loss、吞吐或数据质量问题。

## 推理工程提案加项

推理工程项目必须额外说明：

- API surface：请求/响应字段、错误格式、streaming 或 JSON mode。
- 评测集：固定 prompt、期望行为、失败判定。
- SLO：错误率、P95 latency、TTFT、TPOT、tokens/s。
- 容量规划：模型权重、KV cache、batch、context、显存安全余量。
- 回归用例：RAG、JSON response、tool calling、安全拒答或限流。

推理工程最小成功标准示例：

- 服务有 `/health` 或等价健康检查。
- `evaluate.py` 至少覆盖 5 个固定用例。
- `benchmark.py` 输出 P50/P95/P99、TTFT、TPOT 和错误率。
- `slo_check.py` 能用机器可读报告判定 PASS/FAIL。

## Milestone 模板

milestone 建议 2-4 页，重点不是“最终结果好看”，而是证明项目风险已经被发现并收敛。

### 必交内容

- 从提案到当前版本的变更。
- 已完成的最小闭环。
- 当前最好结果和对应命令。
- 至少 2 个失败案例。
- `split_card` 更新版和 `leakage_check` 初步结果。
- `metric_card` 更新版，说明指标局限是否改变项目结论。
- `uncertainty_record` 初稿：bootstrap_ci、seed_sensitivity、paired_comparison、load-test variance 或 single_seed_limit。
- `claim_audit` 初稿：把“显著提升”“稳健”“更快”“更安全”“泛化”等词映射到证据或降级措辞。
- 下一阶段计划。
- 需要助教或教师反馈的问题。

### 训练 milestone 检查表

| 检查项 | 必须证据 |
|--------|----------|
| 数据审计 | `data_audit.py` 输出或等价报告 |
| 训练闭环 | 一次 train + validation 日志 |
| checkpoint | 保存文件、resume 命令和 step 恢复证据 |
| 指标日志 | `metrics.jsonl` 或等价机器可读日志 |
| 初步分析 | loss 曲线、吞吐、过拟合或数据异常说明 |
| 统计严谨性 | split_card、metric_card、uncertainty_record 和 claim_audit 初稿 |

### 推理 milestone 检查表

| 检查项 | 必须证据 |
|--------|----------|
| 服务闭环 | 本地启动命令和健康检查 |
| 固定评测 | 至少 5 个评测样例和 pass/fail 输出 |
| 压测 | latency、TTFT、TPOT、tokens/s、错误率 |
| SLO | 机器可读 benchmark 报告和 SLO 判定 |
| 容量规划 | 权重显存、KV cache、batch/context、成本估计 |
| 统计严谨性 | fixed workload、warmup、concurrency、uncertainty_record 和 single_seed_limit 或 repeated-run 记录 |

## Milestone 评分

| 维度 | 分值 | 满分证据 |
|------|:--:|----------|
| 目标收敛 | 20 | 问题、非目标和成功标准比提案更清楚 |
| 最小闭环 | 25 | 可用一条命令复现核心流程 |
| 指标与日志 | 20 | 指标机器可读，报告数字可追溯 |
| 风险处理 | 20 | 失败案例具体，下一步计划能降低风险 |
| 反馈质量 | 15 | 提出具体、可回答、与项目成败相关的问题 |

若 milestone 已经写出比较结论，但没有 split_card、metric_card、uncertainty_record 或 claim_audit，`指标与日志` 和 `风险处理` 不能拿满分。

不通过条件：

- 只有想法，没有可运行证据。
- 只展示成功样例，没有失败案例。
- 报告数字无法从日志或命令复现。
- milestone 与提案目标完全脱节且未说明原因。

## 导师反馈记录

每次项目反馈建议记录以下字段：

| 字段 | 内容 |
|------|------|
| 日期 | 反馈日期 |
| 反馈人 | 教师、助教或同伴 |
| 项目版本 | commit、压缩包版本或提交编号 |
| 最大风险 | 当前最可能导致项目失败的问题 |
| 必改项 | 下一次提交前必须完成的事项 |
| 可选项 | 有余力时可以改进的事项 |
| 复核证据 | 下次如何证明问题已经解决 |
| statistics_gate | split、metric、uncertainty、claim 或 leakage 中必须先解决的门禁 |
| downgrade_decision | 是否把项目范围、claim 强度或资源申请降级 |

## 最终提交包

最终提交必须让助教能在新环境中复现核心结论：

- 源代码。
- `README.md` 或报告中的复现命令。
- 环境依赖和版本。
- 固定 seed 或随机性说明。
- 数据来源和处理脚本。
- 训练日志、评测报告或压测报告。
- split_card、metric_card、uncertainty_record、claim_audit 和 leakage_check。
- 最终报告。
- 展示材料。
- 同伴 review 修改说明。

最终报告建议按 [Project Report Template and Reproducibility Checklist](project-report-template.md) 组织，仍按 [Capstone 项目报告 Rubric](project-report-rubric.md) 评分；展示和互评按 [项目展示与同伴 Review Rubric](presentation-peer-review.md) 评分。

完整提交包字段、阶段 acceptance matrix 和 TA review procedure 见 [Project Submission Dossier](project-submission-dossier.md)。最终提交前必须确认 `artifact_manifest`、`split_card`、`metric_card`、`uncertainty_record`、`claim_audit`、`leakage_check`、`run_log.txt`、机器可读 metrics、data ethics review 和 contributions record 均能互相对齐。
