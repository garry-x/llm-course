# Experimental Rigor and Evaluation Statistics Guide

本指南把项目、作业扩展实验和 frontier seminar 中的实验结论从“跑出了一个数字”提升为可复核的课程证据。它补充 [Project Report Template and Reproducibility Checklist](project-report-template.md)、[Project Submission Dossier](project-submission-dossier.md)、[Capstone 项目报告 Rubric](project-report-rubric.md)、[Model and Benchmark Card Guide](model-benchmark-card-guide.md)、[Data and Ethics Review](data-ethics-review.md)、[Dataset, Model, and Artifact Provenance Registry](dataset-model-artifact-registry.md) 和 [经典 NLP 与评测覆盖说明](nlp-evaluation-coverage.md)。

## Scope

适用对象：

- 默认最终项目、训练工程 capstone、推理工程 capstone。
- 自定义项目、外部 seminar 复盘中的小规模实验。
- 作业 `extra_experiments.md` 中声明性能、质量或效率改进的部分。

不适用对象：

- 只验证 API shape、公式方向或单元测试的基础作业题。
- 没有比较结论的 smoke test。
- 教师课堂 demo 中明确标注为 illustration 的一次性输出。

## Evaluation Split Protocol

每个有质量结论的项目必须记录数据切分：

| 字段 | 必须证据 | 常见扣分 |
|------|----------|----------|
| split_id | 数据切分名称、版本或生成脚本 commit | 只写 train/dev/test，没有可复现来源 |
| train_source | 训练数据来源、过滤规则、时间范围 | 把验证集或测试集样本用于训练、调参或 prompt 编写 |
| dev_policy | dev set 用于调参、早停或 prompt 选择的规则 | 多次看 test set 后再改系统 |
| test_policy | test set 只能用于最终报告或冻结后复核 | 报告中把 dev 和 test 混用 |
| leakage_check | 去重、near-duplicate、prompt 泄漏、retrieval contamination 或 benchmark contamination 检查 | 没有说明 RAG 语料是否包含答案或标签 |

最低要求：

- 训练、调参和最终测试的用途必须分开。
- 如果样本量小于 100，报告必须说明 split variance 和人工审查范围。
- 如果使用公开 benchmark、课程固定 prompt 或往年项目数据，必须记录 access date 和 contamination risk。

## Metric Selection and Limits

每个指标都要写清楚支持什么结论、不支持什么结论：

| 指标类型 | 可支持结论 | 不能单独支持 |
|----------|------------|--------------|
| Perplexity / loss | next-token objective 的拟合趋势 | 下游任务质量、事实性或安全性 |
| BLEU / ROUGE | n-gram overlap 或摘要相似度 | 语义正确、无幻觉、用户满意 |
| EM / F1 | 固定答案集上的抽取或分类表现 | 开放生成可靠性 |
| pass rate | 固定回归用例是否通过 | 未覆盖场景的泛化 |
| P50/P95/P99 latency | 当前负载、硬件和并发下的延迟分布 | 所有部署环境的稳定性 |
| tokens/s / cost | 当前实现和硬件条件下的吞吐或成本 | 质量更好或用户体验更好 |

项目报告必须至少包含一个 quality metric、一个 robustness/error metric 或 failure taxonomy，以及一个 resource metric。

## Uncertainty and Confidence Intervals

如果报告比较两个系统、两个 prompt、两个模型或两个工程设置，必须给出不确定性说明。可选方法：

| 方法 | 适用场景 | 最低记录 |
|------|----------|----------|
| bootstrap confidence interval | 固定评测集上的 accuracy、F1、ROUGE、pass rate、latency percentile | bootstrap 次数、随机 seed、95% CI |
| repeated-run seed sensitivity | 训练、小样本 fine-tuning、采样式生成、随机检索索引 | seed 列表、均值、标准差、最好/最差结果 |
| paired comparison | 同一批输入比较两个系统输出 | wins/losses/ties、人工判定规则、冲突处理 |
| load-test variance | 推理服务 benchmark | 并发、请求数、warmup、P50/P95/P99、错误率 |

最低要求：

- 少于 30 个样本的比较不能写成“显著提升”，只能写成 preliminary evidence。
- 若只跑一个 seed，必须说明 single_seed_limit。
- latency 或 tokens/s 结果必须记录硬件、并发、warmup、batch size 和上下文长度。

## Significance Claim Gate

报告中出现以下词语时，必须提供相应证据：

| Claim phrase | 需要的证据 |
|--------------|------------|
| significantly better / 显著提升 | 置信区间不重叠、paired test、bootstrap CI 或明确的统计检验 |
| robust / 稳健 | 多 seed、多数据子集、edge cases 或压力测试 |
| faster / 更快 | 同一硬件、同一 workload、同一 measurement protocol |
| safer / 更安全 | 安全测试集、拒答/误拒分析、残余风险说明 |
| generalizes / 泛化 | held-out split、外部分布样本或严格说明外推边界 |

如果没有达到 gate，报告必须改用：

- “在本固定评测集上更高”。
- “在 single_seed 条件下观察到”。
- “在当前硬件和并发下更快”。
- “需要更大样本或人工复核确认”。

## Error Analysis and Failure Taxonomy

每个项目至少提交 3 个失败案例；高风险项目建议提交 10 个。失败案例必须覆盖：

- input、expected、actual、metric impact。
- error type：data、model、system、evaluation、safety、cost。
- likely cause。
- next action。

报告不能只挑最容易解释的失败。助教抽查时应至少选择一个学生未主动展示的 dev/test case。

## Contamination and Leakage Gate

以下情况必须在报告中显式说明，否则项目不能得到高分：

| 风险 | 检查动作 |
|------|----------|
| train/test duplicate | exact 和 near-duplicate 抽查，记录阈值 |
| prompt leakage | prompt、few-shot examples、RAG context 不包含标签或标准答案 |
| retrieval contamination | 检索库不直接包含测试答案；若包含，改用 closed-book 或 citation-aware metric |
| benchmark contamination | 公开 benchmark 只作为参考；最终结论要有自建 held-out set 或人工错误分析 |
| hidden test leakage | 不引用 hidden tests 输入、seed、断言或评分脚本细节 |

如果无法排除污染，报告必须把结论降级为 diagnostic result，并写明不能外推。

## Minimum Evidence Packet

最终报告和项目提交至少包含：

| Artifact | 文件或字段 |
|----------|------------|
| experiment_table | question、baseline、variable、metric、command、result_file |
| split_card | split_id、train/dev/test 用途、leakage_check |
| metric_card | metric、definition、limit、aggregation |
| uncertainty_record | bootstrap_ci、seed_sensitivity、paired_comparison 或 single_seed_limit |
| failure_cases | 至少 3 个案例和 taxonomy |
| resource_record | hardware、batch、context、concurrency、cost、latency 或 tokens/s |
| claim_audit | 高风险 claim、证据、适用边界 |

## TA Audit Checklist

评分前至少抽查：

- 报告表格中的数字能否追溯到 result_file、日志或命令。
- test set 是否只在冻结后使用。
- ablation 是否只改变一个关键变量，且 fixed controls 清楚。
- confidence interval、seed sensitivity 或 single_seed_limit 是否与 claim 强度一致。
- failure taxonomy 是否包含模型、数据、系统或评测原因，而不是只写“效果不好”。
- leakage_check 是否覆盖训练数据、RAG 语料、prompt 和公开 benchmark。

## 发布前 Checklist

- [Project Report Template and Reproducibility Checklist](project-report-template.md) 必须链接本指南，并要求 split_card、metric_card、uncertainty_record 和 claim_audit。
- [Capstone 项目报告 Rubric](project-report-rubric.md) 必须把统计严谨性纳入实验设计、指标选择和不通过条件。
- [Data and Ethics Review](data-ethics-review.md) 必须与 contamination/leakage gate 使用同一套字段。
- [经典 NLP 与评测覆盖说明](nlp-evaluation-coverage.md) 必须提醒项目同时报告质量、资源、错误分析和不确定性。
