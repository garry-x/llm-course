# Data and Ethics Review

本指南用于训练工程、推理工程和自定义项目的数据/伦理审查。它把数据来源、许可证、隐私、偏见、评测污染、安全边界和模型卡引用整理成可提交、可评分、可复核的交付物。模型卡、API 文档和 benchmark claim 的证据卡按 [Model and Benchmark Card Guide](model-benchmark-card-guide.md) 填写；课堂讨论和项目审查案例见 [Safety and Societal Impact Casebook](safety-societal-impact-casebook.md)；课程内置和学生提交的数据集、模型、tokenizer、checkpoint、评测集合和 runtime asset 的资产级登记按 [Dataset, Model, and Artifact Provenance Registry](dataset-model-artifact-registry.md) 执行。

## 适用范围

学生在以下情况必须提交 Data and Ethics Review：

- 使用任何公开或私有数据集训练、微调、评测或构建 RAG。
- 使用第三方模型、API、embedding 模型、reranker 或 LLM-as-judge。
- 项目涉及医疗、法律、金融、教育、招聘、身份识别、政治、儿童或其他高影响场景。
- 报告中使用 benchmark、leaderboard、模型卡或官方 API 文档作为证据。

若项目只使用课程内置 toy corpus，也需要提交简版审查，说明数据来源、局限和不能外推的结论。

## 提交格式

建议 1-2 页，必须包含：

| 项 | 必填内容 |
|----|----------|
| 数据清单 | 数据集名称、链接、版本、访问日期、许可证、用途 |
| 模型/API 清单 | 模型名、提供方、版本或日期、模型卡/文档链接、用途 |
| 处理流程 | 收集、过滤、切分、去重、tokenization、检索或评测流程 |
| 风险登记 | 隐私、偏见、幻觉、评测污染、安全拒答、版权/引用 |
| 缓解措施 | 具体检查、过滤、拒答、人工审查或实验限制 |
| 残余风险 | 即使采取缓解措施后仍不能保证什么 |
| 报告位置 | 最终报告中哪些表格、图或结论依赖这些数据/模型 |

## 数据来源与许可证

每个数据源至少记录：

```text
Dataset:
URL:
Version/date:
License/terms:
Access date:
Used for: train / validation / test / RAG / demo / benchmark
Contains human text: yes/no/unknown
Redistribution allowed: yes/no/unknown
Commercial use allowed: yes/no/unknown/not applicable
```

评分标准：

- 满分：能说明许可证或使用条款如何影响训练、评测、发布和报告引用。
- 部分分：列出链接和访问日期，但许可证说明不完整。
- 不通过：无法说明数据来源，或使用不允许再分发的数据却提交到公开仓库。

## 隐私与 PII

必须检查：

- 是否包含姓名、邮箱、电话、地址、身份证号、账号、病历、财务信息或聊天记录。
- 是否包含少数样本即可识别个人的组合信息。
- RAG 是否可能把敏感文档原文返回给用户。
- 日志是否保存 prompt、response、IP、API key 或用户标识。

最低缓解措施：

- 对 toy 项目：说明没有使用真实用户数据，或列出人工构造方式。
- 对真实数据：去除或脱敏 PII，记录过滤规则和误删/漏删风险。
- 对 RAG：限制检索语料范围，给出敏感文档拒答或截断策略。
- 对服务日志：不记录密钥，不在报告中粘贴真实敏感 prompt。

## 偏见与代表性

项目需要回答：

- 数据主要来自哪些语言、地区、领域、群体或平台？
- 哪些群体或任务被系统性低估或缺失？
- 评测集是否只覆盖成功样例或高资源语言？
- 指标是否会掩盖少数类别失败？

最低缓解措施：

- 报告至少一个代表性局限。
- 对分类或检索项目，按类别、语言或场景拆分至少一个指标。
- 对生成项目，提供至少 3 个失败案例，并说明是否与数据分布相关。

## 评测污染与数据泄漏

实验 split、contamination/leakage gate、benchmark contamination 和 claim 降级规则与 [Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md) 保持一致。

必须区分：

- `train/validation/test` 泄漏：同一或近似样本出现在多个 split。
- benchmark contamination：公开 benchmark 可能出现在预训练、微调或 prompt 调参过程中。
- RAG leakage：答案文档或标签被直接放入检索上下文，导致指标虚高。

最低检查：

- 训练工程：报告重复样本、split 策略和验证集构造。
- 推理工程：固定评测集不应在 prompt 调参中反复手动过拟合。
- RAG 项目：说明检索语料和评测答案之间的关系。

## 安全边界

高风险请求至少覆盖以下类别中的 3 类：

- 医疗、法律、金融等专业建议。
- 自伤、暴力、违法操作或危险物质。
- 隐私提取、身份识别或社会工程。
- 恶意代码、绕过安全机制或凭证窃取。
- 偏见、仇恨、骚扰或歧视性输出。

项目报告需要说明：

- 哪些请求应拒答或转向安全建议。
- 哪些请求允许给一般信息但不能给操作步骤。
- 固定安全回归用例如何运行。
- 失败时如何记录和降级。

## 模型卡与 API 文档

若使用第三方模型或 API，必须引用：

- 模型卡或官方文档。
- 版本、发布日期或访问日期。
- context length、价格、速率限制、输入输出限制等与项目相关的条件。
- 已知限制或安全说明。

不要把模型卡声明直接扩展为普遍事实。若报告写“模型 X 支持 1M context”，应说明这是哪个模型卡、哪个日期、哪个版本的声明。

## 最终报告必含小节

每个 capstone 最终报告必须包含 `Data, Ethics, and Limitations` 小节，至少回答：

1. 数据和模型/API 从哪里来，许可证或使用条款是什么？
2. 你检查了哪些隐私、偏见、污染或安全风险？
3. 你采取了哪些缓解措施？
4. 哪些风险仍然存在？
5. 哪些结论只能在本实验条件下成立，不能外推？

## 评分 Rubric

| 维度 | 分值 | 满分证据 |
|------|:--:|----------|
| 来源与许可证 | 20 | 数据、模型、API 有链接、版本、访问日期和使用条款 |
| 隐私与 PII | 20 | 明确检查敏感字段、日志和 RAG 泄漏风险 |
| 偏见与代表性 | 15 | 至少一个按场景/类别/语言拆分的局限或指标 |
| 污染与泄漏 | 15 | 说明 split、benchmark contamination 或 RAG leakage |
| 安全边界 | 15 | 至少 3 类高风险请求和固定回归/拒答策略 |
| 残余风险 | 15 | 清楚说明不能保证的结论和外推边界 |

不通过条件：

- 无法说明数据来源。
- 使用真实敏感数据但没有隐私处理。
- 报告中包含不应公开的个人信息、密钥、私有文档或未授权数据。
- 高影响场景没有安全边界或人工复核说明。
- 把模型卡、leaderboard 或 benchmark 数字当作无条件事实。

## 审查记录模板

```text
Project:
Reviewer:
Date:

Data sources:
Model/API sources:
License/terms concerns:
PII/privacy concerns:
Bias/representativeness concerns:
Contamination/leakage concerns:
Safety boundary concerns:
Required changes before final:
Residual risks accepted:
```
