# Model and Benchmark Card Guide

复核日期：2026-06-05

本指南把模型卡、API 文档、benchmark 报告、leaderboard 和本地评测输出转成可填写、可评分、可复核的证据卡。它补充 [External Source Verification Guide](external-source-verification.md)、[External Source Inventory](external-source-inventory.md)、[Chapter Source and Accuracy Map](chapter-source-map.md)、[Chapter Claim Audit Ledger](chapter-claim-audit-ledger.md)、[Project Report Template and Reproducibility Checklist](project-report-template.md)、[Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md)、[Dataset, Model, and Artifact Provenance Registry](dataset-model-artifact-registry.md)、[Data and Ethics Review](data-ethics-review.md)、[Safety and Societal Impact Casebook](safety-societal-impact-casebook.md)、[Capstone Proposal and Milestone Guide](capstone-proposal-milestone.md) 和 [Reading Discussion Question Bank](reading-discussion-question-bank.md)。

使用边界：本指南可进入 student site release；不得包含 hidden tests、reference_solution.py、private grading samples 或 real student submissions。

## Card Schema

| field | required evidence | grading use |
|-------|-------------------|-------------|
| card_id | 唯一 ID，例如 MBC-PROJ-01 | 把报告 claim 追踪到证据卡 |
| source_kind | model card、API docs、benchmark report、leaderboard、local run | 判断复核频率和来源等级 |
| source_record | 标题或文档名、URL、version_or_date、access_date、source_tier | 复核易变来源和引用边界 |
| claimed_property | context length、price、quality score、latency、tokens/s、safety rate 等 | 找到要被支持的最小声明 |
| configuration | model version、prompt、shot、split、metric、hardware、batch、concurrency、context length | 防止把配置相关数字写成普遍事实 |
| supported_claim | 来源或实验能直接支持的表述 | 允许写入正文、报告或 slides |
| unsupported_claim | 来源或实验不能推出的更强结论 | 防止过度外推 |
| verification_action | keep、revise、downgrade、rerun、remove、needs staff review | 形成助教复核动作 |
| course_link | 对应章节、阅读、项目、评测或伦理文档 | 连接课程证据链 |

## Model Card Checklist

| check_id | question | full_credit_evidence | common_failure | course_link |
|----------|----------|----------------------|----------------|-------------|
| MBC-MODEL-ID | 模型名称、版本、提供方是否唯一定位 | official model card 或 API docs 中的 model name、revision、release date、access_date | 只写模型家族名，无法定位具体版本 | External Source Inventory |
| MBC-MODEL-DATE | 来源是否易变，访问日期是否记录 | access_date、version_or_date、复核人和引用位置 | 把今天的 API 名称、价格或上下文长度当作长期事实 | External Source Verification Guide |
| MBC-MODEL-CONTEXT | context length、tokenizer 和输入限制是否来自来源 | context window、tokenizer 或 API limit 的来源摘要 | 写成“能处理所有长文档任务” | Ch02、Ch10 |
| MBC-MODEL-TRAINING | 训练数据或训练目标是否只按来源边界描述 | source-reported training data summary、objective、known unknowns | 把模型卡摘要写成完整数据审计 | Data and Ethics Review |
| MBC-MODEL-LICENSE | license、terms、允许用途和归档边界是否记录 | license name、terms link、commercial or research boundary | 忽略模型权重、API、数据集之间的许可差异 | Dataset, Model, and Artifact Provenance Registry |
| MBC-MODEL-SAFETY | safety limitation、known risk 和 residual risk 是否记录 | safety note、refusal behavior、known failure、residual risk | 写成“模型安全”但无测试集或误拒分析 | Safety and Societal Impact Casebook |
| MBC-MODEL-ACCESS | API availability、rate limit、region、quota 或硬件要求是否记录 | API status、rate limit、quota、hardware note、fallback | 复现实验依赖不可用 API 但没有替代路径 | Compute Resource and Cost Guide |
| MBC-MODEL-VOLATILITY | 前沿模型数字是否被标成报告值而非课程定理 | “source reports X as of date” 写法和重查计划 | 把模型卡、新闻稿或 leaderboard 写成独立验证结论 | Frontier Source Audit |

## Benchmark Card Checklist

| check_id | question | full_credit_evidence | common_failure | course_link |
|----------|----------|----------------------|----------------|-------------|
| MBC-BENCH-TASK | task 名称、版本和评测目标是否明确 | benchmark name、task version、input/output definition | 只写“某榜单分数高” | Experimental Rigor and Evaluation Statistics Guide |
| MBC-BENCH-DATA | dataset split、样本范围和污染风险是否记录 | split_id、sample count、dedup 或 contamination note | dev/test 混用或 RAG 语料包含答案 | Project Submission Dossier |
| MBC-BENCH-PROMPT | prompt、shot 数、decoding 和 tool policy 是否固定 | prompt template、shots、temperature、tool settings | 改 prompt 后仍引用旧数字 | Reading Discussion Question Bank |
| MBC-BENCH-METRIC | metric 定义、聚合方式和不支持的结论是否说明 | metric_card、aggregation、confidence interval 或 limit | 用 BLEU/ROUGE 单独证明语义正确 | Classic NLP Evaluation Coverage |
| MBC-BENCH-BASELINE | baseline 是否可复现且公平 | baseline version、same split、same metric、same budget where relevant | 只和弱 baseline 比，或不同设置比较 | Project Report Rubric |
| MBC-BENCH-HARDWARE | serving benchmark 是否记录硬件、软件和负载 | GPU/CPU、runtime version、batch、concurrency、warmup、context | tokens/s 不写硬件和并发 | Ch10 Inference |
| MBC-BENCH-CONTAM | benchmark contamination 或 leakage 是否检查 | leakage_check、retrieval corpus boundary、training overlap note | 公开题被 prompt 或语料提前看过 | Data and Ethics Review |
| MBC-BENCH-UNCERT | 是否记录 seed、CI、variance 或样本量限制 | bootstrap CI、seed list、single_seed_limit、sample size note | 单次运行写成显著提升 | Experimental Rigor and Evaluation Statistics Guide |
| MBC-BENCH-SLO | latency、cost 或 availability claim 是否绑定 workload | TTFT、TPOT、P50/P95/P99、error rate、request mix、cost unit | 把课堂压测写成 production-ready | Compute Resource and Cost Guide |

## Course Card Examples

| example_id | source_kind | student_claim | supported_rewrite | required_card_fields | course_link |
|------------|-------------|---------------|-------------------|----------------------|-------------|
| MBC-EX-VOLATILE-CONTEXT | model card | Model X supports 1M context, so it solves long-document QA | Source Y reports context length Z as of access_date; this supports an input limit under source conditions, not answer quality | source_record、claimed_property、configuration、unsupported_claim | Ch02、Ch10 |
| MBC-EX-SERVING-BENCH | local run | Our server is production-ready at 300 tokens/s | Under hardware H, model M, workload W and concurrency C, the run measured P95 latency and tokens/s; production readiness needs broader load and failure testing | configuration、MBC-BENCH-HARDWARE、MBC-BENCH-SLO | Ch10 Inference |
| MBC-EX-RAG-QUALITY | benchmark report | Retrieval hit rate proves answers are correct | Retrieval hit rate supports evidence availability on split S; answer correctness requires generation metric or human review | MBC-BENCH-DATA、MBC-BENCH-METRIC、unsupported_claim | RAG Project |
| MBC-EX-LEADERBOARD | leaderboard | This model is generally best | Leaderboard L reports score S on task T and version V as of access_date; it does not prove general quality outside that benchmark | source_kind、source_record、claimed_property、configuration | Frontier Seminar |
| MBC-EX-API-PRICE | API docs | This project will always cost less than budget B | API docs reported unit price P and rate limit R as of access_date; final cost must be rechecked before release and tied to token counts | source_record、verification_action、course_link | Compute Resource and Cost Guide |

## Claim Rewrite Rules

| rule_id | risky wording | required rewrite | evidence |
|---------|---------------|------------------|----------|
| MBC-R1 | Model X supports 1M context, so it understands long documents | Source Y reports context limit Z as of access_date; this supports input size, not task quality | model card plus task evaluation |
| MBC-R2 | Benchmark score S proves model quality | Benchmark B version V reports metric S under task, prompt, shot and metric settings | benchmark card |
| MBC-R3 | System A is faster | System A was faster under same hardware, workload, batch, context, concurrency and warmup protocol | serving benchmark card |
| MBC-R4 | API cost is fixed | API docs reported unit price and rate limit on access_date; recheck before release and archive token accounting | API docs card |
| MBC-R5 | Model is safer | Safety result must name test set, refusal metric, false refusal, failure examples and residual risk | safety card and case analysis |
| MBC-R6 | We improved performance | With one run or small sample, write preliminary evidence and report seed, sample size and uncertainty limit | uncertainty_record |

## Student Submission Template

```yaml
card_id:
source_kind:
source_record:
  title_or_doc:
  url:
  version_or_date:
  access_date:
  source_tier:
claimed_property:
configuration:
supported_claim:
unsupported_claim:
verification_action:
course_link:
```

## Staff Review Workflow

1. Require a model/benchmark card whenever a project, reading recap, frontier seminar or report uses a model card, API docs, leaderboard, benchmark, price, context length, latency, tokens/s, safety or quality claim.
2. Check source tier and access date against [External Source Inventory](external-source-inventory.md) and [External Source Verification Guide](external-source-verification.md).
3. Compare supported_claim and unsupported_claim with the actual project report, slides, README or reading recap wording.
4. Route unstable facts to [frontier-source-audit.md](frontier-source-audit.md) and high-risk claims to [Claim Audit Worksheet](claim-audit-worksheet.md).
5. If the claim affects a graded assessment, record the item or rubric boundary so later corrections can be handled through [Course Errata and Correction Ledger](course-errata-correction-ledger.md).

## Release Checklist

- Card Schema has source_kind、source_record、supported_claim、unsupported_claim、verification_action and course_link.
- Model Card Checklist covers ID/date/context/training/license/safety/access/volatility.
- Benchmark Card Checklist covers task/data/prompt/metric/baseline/hardware/contamination/uncertainty/SLO.
- Course Card Examples include volatile context, serving benchmark, RAG quality, leaderboard and API price.
- Claim Rewrite Rules force date, version, task, metric, workload and uncertainty boundaries.
- Student Submission Template is present and contains access_date and source_tier.
- Staff Review Workflow routes unstable facts and graded assessment changes.
- student site release excludes hidden tests、reference_solution.py、private grading samples and real student submissions.
