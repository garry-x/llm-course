# Capstone Defense and Oral Exam Question Bank

复核日期：2026-06-05

本题库用于 capstone 展示后的口头追问、项目答辩和必要时的个人 oral exam。它补充 [项目展示与同伴 Review Rubric](presentation-peer-review.md)、[Project Report Template and Reproducibility Checklist](project-report-template.md)、[Capstone 项目报告 Rubric](project-report-rubric.md)、[Project Submission Dossier](project-submission-dossier.md)、[Capstone Proposal and Milestone Guide](capstone-proposal-milestone.md)、[Project Team and Mentor Policy](project-team-mentor-policy.md)、[Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md)、[Model and Benchmark Card Guide](model-benchmark-card-guide.md)、[Data and Ethics Review](data-ethics-review.md)、[Safety and Societal Impact Casebook](safety-societal-impact-casebook.md)、[Final Project Showcase and Archive Policy](final-project-showcase-archive-policy.md)、[Assessment Administration and Exam Integrity Policy](assessment-administration-policy.md) 和 [Academic Integrity Case Process](academic-integrity-case-process.md)。

使用边界：本题库可以进入 student site release。题目是 defense category 和公开练习题，不包含 hidden tests、reference_solution.py、private grading samples、real student submissions 或未公开评分脚本。

## Defense Format

| format_id | use_case | duration | question_mix | evidence_record |
|-----------|----------|----------|--------------|-----------------|
| DEF-GROUP-QA | 普通项目展示后的组内问答 | 3-5 分钟 | 2 个项目级问题加 1 个边界问题 | presentation notes、rubric comments |
| DEF-ROTATING | poster session 或大型班级轮转 | 每组 5-8 分钟 | 1 个方法问题、1 个实验问题、1 个复现或来源问题 | station checklist、staff initials |
| DEF-INDIVIDUAL | 团队贡献不清、AI 工具披露不足或代码理解存疑 | 每人 5-10 分钟 | 2 个个人贡献问题、1 个代码或实验追问 | individual oral record、contribution note |
| DEF-REMEDIAL | 报告证据不足但允许补交说明 | 10-15 分钟 | 重点问不支持 claim、失败案例和降级计划 | remediation decision、allowed resubmission |
| DEF-ARCHIVE | 公开归档候选项目的归档前复核 | 5-10 分钟 | 复现、redaction、source boundary 和 public safety | archive_record、redaction note |

## Question Schema

| field | meaning | required evidence |
|-------|---------|-------------------|
| question_id | 稳定 ID，例如 `DEF-METHOD-01` | 便于记录抽样和复核 |
| category | contribution、method、experiment、reproducibility、source、safety、failure、communication | 映射到报告 rubric 和展示 rubric |
| prompt | 可公开给学生准备的追问 | 不能泄露 hidden tests 或私有评分样例 |
| strong_answer_evidence | 满分回答必须包含的证据 | 文件、命令、日志、图表、source card 或失败案例 |
| weak_answer_signal | 需要追问或降级的信号 | 只讲口号、无法定位代码、无法说明边界 |
| course_link | 相关课程证据 | 对应 guide、rubric、dossier 或章节 |

## Core Defense Questions

| question_id | category | prompt | strong_answer_evidence | weak_answer_signal | course_link |
|-------------|----------|--------|------------------------|--------------------|-------------|
| DEF-CONTRIB-01 | contribution | 你个人负责的最关键 artifact 是什么，如何证明它不是只来自队友或外部工具 | contributions.md、commit or file pointer、run_log、AI tool disclosure | 只说“我参与了整体设计”，不能指向具体 artifact | Project Team and Mentor Policy |
| DEF-CONTRIB-02 | contribution | 如果现在只让你维护项目一个月，你最先重写或监控哪一部分 | failure case、risk register、owned module、next action | 只给泛泛愿望，没有工程优先级 | Project Submission Dossier |
| DEF-METHOD-01 | method | 请画出从输入到输出的最小数据流或服务流，并标出课程章节中的对应组件 | diagram、shape/API fields、Ch01-Ch10 connection | 只能描述 demo 页面，不能说明数据流 | Project Report Template |
| DEF-METHOD-02 | method | 你的 baseline 为什么公平，哪一个变量被固定，哪一个变量被改变 | baseline config、fixed controls、changed variable、split_card | baseline 与主方法数据、硬件或 prompt 不一致 | Experimental Rigor and Evaluation Statistics Guide |
| DEF-METHOD-03 | method | 如果删除一个核心模块，结果会如何变化，你如何验证 | ablation plan or result、metric_card、failure expectation | 无 ablation 或无法预测影响方向 | Project Report Rubric |
| DEF-EXP-01 | experiment | 报告里最重要的数字来自哪条命令、哪个文件和哪个配置 | reproduction command、metrics file、config、commit | 数字只能从 slides 看到，不能回到日志 | Project Submission Dossier |
| DEF-EXP-02 | experiment | 你的 metric 支持什么结论，不支持什么结论 | metric_card、known_limit、unsupported claim | 把单个 metric 写成总体质量 | Model and Benchmark Card Guide |
| DEF-EXP-03 | experiment | 你的结论如果只跑了一个 seed 或小样本，应如何降级表述 | uncertainty_record、single_seed_limit、preliminary evidence wording | 仍使用 robust、significant、generalizes 等强词 | Experimental Rigor and Evaluation Statistics Guide |
| DEF-EXP-04 | experiment | 训练项目中 loss spike、过拟合或吞吐下降的第一排查步骤是什么 | train log、grad_norm、lr、data audit、checkpoint note | 只说“调参”，没有诊断顺序 | Training Capstone |
| DEF-EXP-05 | experiment | 推理项目中 P95 latency、TTFT、TPOT 或 tokens/s 的 workload 条件是什么 | benchmark_report、hardware、concurrency、context、warmup | 只报平均 latency 或 tokens/s | Inference Capstone |
| DEF-REPRO-01 | reproducibility | 另一名 TA 在新机器上复现时最可能失败在哪里，你如何降低风险 | environment record、dependency version、fallback、run_log | 没有环境、seed 或 fallback | Environment and Reproducibility Guide |
| DEF-REPRO-02 | reproducibility | checkpoint、model、tokenizer、dataset 或 eval set 的 provenance 如何定位 | artifact_manifest、registry ID、license/access | artifact 名称不唯一或来源不清 | Dataset, Model, and Artifact Provenance Registry |
| DEF-SOURCE-01 | source | 你引用的一个模型卡、API 文档或 leaderboard 支持了什么，不能支持什么 | model/benchmark card、access_date、unsupported_claim | 把来源报告值说成普遍事实 | Model and Benchmark Card Guide |
| DEF-SOURCE-02 | source | 如果该外部来源明天更新或失效，你的报告哪一句需要修改 | source tier、verification_action、downgrade_decision | 没有访问日期或替代来源 | External Source Verification Guide |
| DEF-SAFETY-01 | safety | 你的项目最主要的隐私、偏见、安全、污染或 misuse 风险是什么 | data_ethics_review、risk type、mitigation、residual risk | 只写“无风险”或只依赖模型提供方声明 | Safety and Societal Impact Casebook |
| DEF-SAFETY-02 | safety | 如果要公开归档，必须删除或改写哪些内容 | redaction checklist、consent_status、archive_record | 把 grading packet 或敏感 artifact 公开 | Final Project Showcase and Archive Policy |
| DEF-FAIL-01 | failure | 请选择一个失败案例，说明 root cause、证据和下一个可执行实验 | error case、error type、likely cause、next action | 只讲“模型表现不好”，没有例子 | Project Report Template |
| DEF-FAIL-02 | failure | 哪个失败模式会让你的 headline claim 不成立 | claim_audit、risk register、downgrade boundary | headline claim 与失败案例无关 | Project Report Rubric |
| DEF-COMM-01 | communication | 用两句话向非本课程同学解释你的项目结论和限制 | concise claim、limitation、evidence reference | 只有营销式结论，没有限制 | Presentation Peer Review |
| DEF-COMM-02 | communication | 如果老师只看一页附录，哪三项证据最能支持你的评分 | report section、metrics、logs、artifact_manifest | 选择漂亮截图而非可复核证据 | Project Submission Dossier |

## Track-Specific Follow-Ups

| question_id | track | prompt | expected_evidence | course_link |
|-------------|-------|--------|-------------------|-------------|
| DEF-TRAIN-01 | training | token budget、batch tokens、validation frequency 和 checkpoint policy 如何影响训练结论 | config、metrics.jsonl、checkpoint resume evidence | Ch07 Training |
| DEF-TRAIN-02 | training | 如果 validation loss 下降但生成样例变差，你会如何解释 | loss curve、sample output、metric limitation、error analysis | Ch08 Generation |
| DEF-TRAIN-03 | training | 数据重复、异常字符或长度分布如何影响你的模型 | data_audit、dedup note、length histogram | Data and Ethics Review |
| DEF-INFER-01 | inference | 并发翻倍或 context 翻倍后，容量瓶颈在哪里 | KV cache estimate、P95 latency、memory budget | Ch10 Inference |
| DEF-INFER-02 | inference | RAG 检索命中率和最终答案正确率为什么不是同一件事 | retrieval metric、generation metric、failure case | Model and Benchmark Card Guide |
| DEF-INFER-03 | inference | 你的服务如何处理超时、限流、格式错误或安全拒答 | API error policy、regression cases、SLO report | Inference Capstone |
| DEF-DEFAULT-01 | default | Tiny GPT 的 tokenizer、embedding、attention、block、LM head 和 loss 如何串起来 | data-flow trace、shape annotations、course module links | Ch01-Ch06 |
| DEF-DEFAULT-02 | default | 下游任务评测为什么能或不能证明模型质量 | fixed inputs、metric_card、error cases | Classic NLP and Evaluation |

## Scoring Rubric

| dimension | full_credit | partial_credit | no_credit |
|-----------|-------------|----------------|-----------|
| evidence grounding | 回答能定位到文件、命令、日志、配置、图表或 source card | 能说明方向但证据定位不完整 | 只复述 slides 或口号 |
| technical ownership | 能解释自己负责模块的代码路径、输入输出、失败模式和修改理由 | 能解释项目整体但个人贡献证据弱 | 无法说明自己贡献或核心代码 |
| claim discipline | 明确 supported claim、unsupported claim、uncertainty 和降级措辞 | 能说出部分限制但未连接到 claim | 继续使用过强结论 |
| reproducibility | 能说明环境、seed、artifact、复现命令和 fallback | 有命令但缺 artifact 或环境边界 | 无法说明如何复现 |
| risk awareness | 能说明数据、伦理、安全、来源或公开归档风险及 residual risk | 只说明一种风险或缓解较泛 | 声称无风险或忽略明显风险 |

## Sampling Rules

| rule_id | rule | evidence |
|---------|------|----------|
| DEF-SAMPLE-CO4 | 每个 capstone 至少抽 1 个 method/experiment/reproducibility 问题 | presentation notes |
| DEF-SAMPLE-CO5 | 使用模型卡、API、leaderboard 或 benchmark claim 的项目至少抽 1 个 source 问题 | model/benchmark card |
| DEF-SAMPLE-SAFETY | 涉及用户数据、RAG、公开 API、安全或归档候选的项目至少抽 1 个 safety 问题 | data_ethics_review |
| DEF-SAMPLE-TEAM | 团队项目每名成员至少回答 1 个个人贡献或代码理解问题 | individual oral record |
| DEF-SAMPLE-REMEDIAL | 报告证据不足时，追问必须记录 downgrade_decision 或 allowed resubmission | remediation decision |

## Oral Record Template

```text
defense_id:
project_id:
student_or_team:
format_id:
question_ids:
evidence_checked:
answer_summary:
rubric_dimension:
score_or_decision:
downgrade_decision:
follow_up_required:
reviewer:
date:
```

## Staff Workflow

1. 展示前按项目类型、风险和报告 claim 选择 3-5 个候选问题，不提前指定具体抽题顺序。
2. 展示当天记录 question_ids、evidence_checked 和 answer_summary；不要记录不必要的个人隐私。
3. 若回答暴露报告数字不可复现、贡献不清、source overclaim 或安全风险，按 Project Submission Dossier、Academic Integrity Case Process 或 Course Errata and Correction Ledger 路由。
4. 对团队项目，若个人回答与 contributions.md 明显不一致，启动 individual oral follow-up，而不是直接用团队展示覆盖个人评分。
5. 成绩发布前确认 oral record 只支持 rubric decision，不包含 hidden tests、private grading samples、real student submissions 或未授权敏感数据。

## Release Checklist

- Defense Format 覆盖 group QA、rotating poster、individual oral、remedial 和 archive review。
- Question Schema 包含 question_id、category、prompt、strong_answer_evidence、weak_answer_signal 和 course_link。
- Core Defense Questions 至少覆盖 contribution、method、experiment、reproducibility、source、safety、failure 和 communication。
- Track-Specific Follow-Ups 覆盖 training、inference 和 default final project。
- Scoring Rubric 覆盖 evidence grounding、technical ownership、claim discipline、reproducibility 和 risk awareness。
- Sampling Rules 覆盖 CO4、CO5、safety、team 和 remedial 场景。
- Oral Record Template 可用于保存 defense_id、question_ids、evidence_checked、downgrade_decision 和 follow_up_required。
- student site release 排除 hidden tests、reference_solution.py、private grading samples、real student submissions 和未公开评分脚本。
