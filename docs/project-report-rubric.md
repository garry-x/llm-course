# Capstone 项目报告 Rubric

本 rubric 用于默认最终项目、训练工程和推理工程两个 Capstone。自动检查只证明项目能跑通；高校课程评分还需要检查复现性、实验设计、统计不确定性、错误分析和工程判断。默认最终项目的任务包见 Default Final Project Guide，学生最终报告建议按 Project Report Template and Reproducibility Checklist 提交；proposal、milestone、final report、presentation 和 archive candidate 的提交包按 Project Submission Dossier 检查；展示后的项目答辩和个人口头追问按 Capstone Defense and Oral Exam Question Bank 记录；实验比较、confidence interval、seed sensitivity 和 significance claim gate 按 Experimental Rigor and Evaluation Statistics Guide 执行；安全、伦理与社会影响案例按 Safety and Societal Impact Casebook 检查。A/B/C/not_passing 报告产出样例见 Project Report Exemplar Pack。

## 通用评分

| 维度 | 分值 | 通过标准 |
|------|:--:|----------|
| 问题定义 | 8 | 清楚说明目标、用户场景、约束和非目标 |
| 复现性 | 12 | 提供命令、环境、seed、数据版本、依赖版本和运行日志 |
| 实验设计 | 18 | 有 baseline、变量控制、至少一个 ablation 或对照实验，并提交 split_card 与 leakage_check |
| 指标选择 | 12 | 指标与目标一致，解释指标局限，并给出 metric_card、bootstrap CI、seed sensitivity 或 single_seed_limit |
| 错误分析 | 14 | 至少 3 个失败案例，按原因分类并提出改进 |
| 工程判断 | 14 | 能解释成本、延迟、稳定性、内存或数据质量取舍 |
| 表达与引用 | 8 | 报告结构清晰，引用论文/文档/模型卡，图表可读 |
| 数据与伦理 | 8 | 按 Data and Ethics Review 提交数据来源、许可证、隐私、偏见、污染、安全边界和残余风险 |
| 贡献与归档 | 6 | 团队项目有贡献声明，自定义项目说明外部协助；优秀项目归档需符合 Capstone Project Gallery and Idea Bank |

## 训练工程加分检查

- 数据分析覆盖长度分布、重复、异常样本和 token 预算。
- 训练曲线包含 train/val loss、perplexity、lr、grad_norm、tokens/s。
- checkpoint resume 后 step 单调增加，配置和优化器状态被恢复。
- 报告说明 loss spike、NaN、过拟合或吞吐下降的排查顺序。
- 若比较训练设置，至少报告 seed sensitivity、validation split variance 或 single_seed_limit。

## 推理工程加分检查

- 压测报告包含 P50/P95/P99 latency、TTFT、TPOT、tokens/s 和错误率。
- 容量规划包含权重显存、KV Cache、runtime overhead、安全余量和成本。
- RAG/JSON/tool calling 至少有固定回归用例。
- 报告说明超时、限流、降级、格式错误和安全拒答的处理策略。
- latency、tokens/s 或 pass rate 的比较必须记录 workload、warmup、concurrency 和置信区间或 repeated-run 方差。

## 默认最终项目加分检查

- 至少完成 Tiny GPT 语言建模、生成质量对比、固定评测/服务化三个任务。
- 能解释 GPT-2 风格模型中 tokenizer、embedding、attention、block、LM head 和 loss 的数据流。
- 下游任务有固定输入、指标、失败判定和至少 3 个错误案例。
- 报告说明哪些部分来自课程 starter/reference、外部库、AI 工具或团队成员贡献。

## 不通过条件

出现以下任一情况，项目报告不能通过：

- 无法复现核心结果。
- 未提交日志或日志与报告数字矛盾。
- 使用参考代码但未说明修改点。
- 只展示成功样例，没有失败分析。
- 指标只报告平均值，没有 P95/P99 或边界情况。
- 写“显著提升”“稳健”“更快”“更安全”或“泛化”，但没有 confidence interval、paired comparison、seed sensitivity、load-test variance 或明确 single_seed_limit。
- 没有 split_card、metric_card、uncertainty_record 或 claim_profile。
- 缺少必要的数据与伦理审查，或公开了敏感数据、密钥、私有文档、未授权数据。
