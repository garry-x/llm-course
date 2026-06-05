# Project Report Template and Reproducibility Checklist

本模板用于默认最终项目、训练工程 Capstone 和推理工程 Capstone 的最终报告。它把 [Capstone 项目报告 Rubric](project-report-rubric.md) 转成学生可直接填写、助教可逐项复核的报告结构。实验比较、统计不确定性、split 和 claim 边界按 [Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md) 管理；模型卡、API 文档、leaderboard 和 benchmark claim 按 [Model and Benchmark Card Guide](model-benchmark-card-guide.md) 填写；安全、伦理与社会影响案例按 [Safety and Societal Impact Casebook](safety-societal-impact-casebook.md) 对照；数据、模型、tokenizer、checkpoint、评测集合和 runtime asset 的 provenance 按 [Dataset, Model, and Artifact Provenance Registry](dataset-model-artifact-registry.md) 管理；proposal、milestone、final report、presentation 和 archive candidate 的提交包按 [Project Submission Dossier](project-submission-dossier.md) 管理；展示后可能抽样使用 [Capstone Defense and Oral Exam Question Bank](capstone-defense-oral-exam-bank.md) 复核个人贡献、代码理解和 claim 边界；报告样例和常见分档见 [Project Report Exemplar Pack](project-report-exemplar-pack.md)。项目提案和 milestone 仍按 [Capstone Proposal and Milestone Guide](capstone-proposal-milestone.md) 管理。

## 使用规则

- 报告建议 6-10 页；附录、日志和机器可读评测文件不计入正文页数。
- 所有数字必须能从命令、日志、配置或评测文件复现。
- 有比较结论的实验必须提交 split_card、metric_card、uncertainty_record 和 claim_audit。
- 若使用团队、外部代码、AI 工具或第三方数据，必须在 Contributions and Disclosure 中说明。
- 报告中的高风险 claim 必须给出来源、访问日期和适用边界。
- 若希望报告、poster 或 slides 进入公开项目归档，必须按 [Final Project Showcase and Archive Policy](final-project-showcase-archive-policy.md) 完成 consent、redaction 和 archive boundary 检查。
- 参考 [Project Report Exemplar Pack](project-report-exemplar-pack.md) 时只能学习结构、证据链和 claim 边界，不得复制 synthetic 数字、措辞或实验设置。

## Title and Metadata

必填字段：

- Project title.
- Track：default final project / training engineering / inference engineering / custom project.
- Team members and roles.
- Repository commit or submission version.
- Primary reproduction command.
- Date and environment.

助教复核：

- commit 或版本号能定位提交。
- primary command 能启动核心复现流程。
- 团队成员与贡献声明一致。

## Abstract

用 120-180 字回答：

- 问题是什么。
- 方法是什么。
- 最重要的结果是什么。
- 最大局限是什么。

避免写法：

- 只写“我们实现了一个系统”，没有指标。
- 只写最好结果，不写实验条件。
- 使用“显著提升”“稳定可靠”等没有证据的词。

## Problem Definition

必须包含：

- 用户场景或研究问题。
- 输入、输出和非目标。
- 最小成功标准。
- 为什么课程章节足以支持该项目。

推荐表格：

| 项目 | 内容 |
|------|------|
| Input | |
| Output | |
| Non-goals | |
| Success criteria | |
| Main risk | |

## Method and Implementation

默认最终项目必须说明：

- tokenizer、embedding、attention、block、LM head 和 loss 的数据流。
- 模型配置：layers、hidden size、heads、context length、参数量。
- 使用了哪些课程 starter/reference、外部库或自写模块。

训练工程项目必须说明：

- dataset、dataloader、loss、optimizer、scheduler、checkpoint 和 resume。
- seed、batch tokens、训练 step、验证频率和日志格式。

推理工程项目必须说明：

- API surface、错误格式、streaming/JSON/tool/RAG 支持情况。
- benchmark、SLO、capacity planning 和回归评测用例。

## Data, Ethics, and Limitations

按 [Data and Ethics Review](data-ethics-review.md) 填写：

| 检查项 | 报告内容 |
|--------|----------|
| Data source | 数据集、链接、版本、访问日期 |
| License | 许可证和允许用途 |
| PII / privacy | 是否包含敏感信息，如何处理 |
| Bias / coverage | 语言、主题、人群或场景偏差 |
| Contamination | 是否可能污染评测集 |
| Split card | split_id、train/dev/test 用途、dev_policy、test_policy |
| Safety boundary | 哪些高风险请求或场景不覆盖 |
| Residual risk | 即使采取措施后仍不能保证什么 |

不允许只写“无风险”。如果项目只使用合成数据，也要说明生成方法、人工检查方式和外推边界。

## Experiments

每个实验必须包含：

- Research question.
- Baseline.
- Changed variable.
- Fixed controls.
- Metric.
- Split card.
- Metric card.
- Uncertainty record：bootstrap_ci、seed_sensitivity、paired_comparison 或 single_seed_limit。
- Reproduction command.
- Expected failure mode.

推荐表格：

| Exp | Question | Baseline | Variable | Metric | Command | Result file |
|-----|----------|----------|----------|--------|---------|-------------|
| E1 | | | | | | |
| E2 | | | | | | |

最低要求：

- 至少一个 baseline。
- 至少一个 ablation 或对照实验。
- 至少一个固定评测集或固定 prompt 集。
- 指标局限必须写清楚。
- 若写“显著提升”“稳健”“更快”“更安全”或“泛化”，必须满足 significance claim gate。

## Results

训练项目至少报告：

- train loss、validation loss、perplexity。
- lr、grad_norm、tokens/s。
- checkpoint resume 证据。
- 数据审计摘要。

推理项目至少报告：

- pass rate 或质量指标。
- P50/P95/P99 latency。
- TTFT、TPOT、tokens/s、error rate。
- capacity planning：weights、KV cache、runtime overhead、safety margin。

默认最终项目至少报告：

- Task A/B/C 的固定输入、指标、失败判定和结果。
- 生成质量对比和至少一个系统或评测指标。

所有图表必须有标题、单位、实验条件和数据来源。

若比较两个系统，结果表必须包含 95% CI、seed 列表、paired wins/losses/ties 或 single_seed_limit；没有不确定性记录的数字只能作为 preliminary evidence。

## Error Analysis

至少 3 个失败案例。推荐格式：

| Case | Input | Expected | Actual | Error type | Likely cause | Next action |
|------|-------|----------|--------|------------|--------------|-------------|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

错误类型示例：

- 数据问题：重复、污染、覆盖不足、标注噪声。
- 模型问题：上下文不足、重复生成、格式不稳、偏好数据偏差。
- 系统问题：超时、限流、缓存失效、RAG 检索失败。
- 评测问题：指标与目标不一致、样例过窄、人工评分不一致。

## Cost and Reproducibility

必须包含：

- Environment：Python、PyTorch、依赖版本、CPU/GPU、内存。
- Commands：训练、评测、压测或验收命令。
- Randomness：seed 或随机性说明。
- Artifacts：日志、metrics、checkpoint、benchmark report、capacity report。
- Cost：GPU hours、API 调用、云成本或 CPU baseline 耗时。

推荐命令块：

```bash
.venv/bin/python verify_course.py
.venv/bin/python verify_course.py --capstone --training
```

项目特定命令应追加到上面之后，并指向机器可读输出文件。

## Contributions and Disclosure

团队项目必须填写：

| Member | Contribution | Evidence |
|--------|--------------|----------|
| | | |

必须披露：

- 外部代码或库。
- 外部协作者或 mentor 建议。
- AI 工具使用环节。
- 与其他课程、工作项目或公开仓库共享的内容。

## Conclusion and Open Questions

必须回答：

- 本实验条件下可以支持什么结论。
- 哪些结论不能外推。
- 如果再做两周，优先补哪个实验。
- 哪个风险仍需要人工审查或更多数据。

## Final Submission Checklist

| 检查项 | 必须证据 |
|--------|----------|
| Reproduction command | 一条主命令或清晰命令序列 |
| Environment | Python/PyTorch/依赖/硬件版本 |
| Data provenance | 数据链接、版本、许可证、访问日期；对应 artifact_manifest 和 registry ID |
| Metrics | 机器可读日志或评测文件 |
| Split card | split_id、train/dev/test 用途和 leakage_check |
| Metric card | 指标定义、局限、aggregation 和适用边界 |
| Uncertainty record | bootstrap_ci、seed_sensitivity、paired_comparison 或 single_seed_limit |
| Baseline / ablation | 至少一个 baseline 和一个对照 |
| Error analysis | 至少 3 个失败案例 |
| Cost | GPU/API/CPU 成本或耗时 |
| Ethics | 数据、隐私、偏见、污染、安全和残余风险 |
| Contributions | 团队、外部代码、AI 工具和协作者披露 |
| Claim audit | 高风险 claim 有来源和适用边界，并补充统计证据 |

## TA Review Checklist

助教评分前应先检查：

- 报告数字能否从提交文件追溯到命令或日志。
- split_card、metric_card、uncertainty_record 和 claim_audit 是否支撑 claim 强度。
- failure cases 是否真实反映模型、数据或系统问题。
- data/ethics section 是否有具体风险，而不是模板化空话。
- contribution statement 是否和代码、日志、展示一致。
- rubric 中每个扣分点是否有文件或行号证据。
