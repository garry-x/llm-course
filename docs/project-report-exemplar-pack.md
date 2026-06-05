# Project Report Exemplar Pack

本包提供 synthetic / anonymized project report exemplars，用于展示高校课程中 final project 报告应如何把实现、实验、复现、错误分析和 claim 边界连成证据链。它补充 [Project Report Template and Reproducibility Checklist](project-report-template.md)、[Capstone 项目报告 Rubric](project-report-rubric.md)、[Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md)、[Data and Ethics Review](data-ethics-review.md)、[Final Project Showcase and Archive Policy](final-project-showcase-archive-policy.md)、[Capstone Project Gallery and Idea Bank](capstone-project-gallery.md) 和 [Grading Anchor Sample Feedback Pack](grading-anchor-sample-feedback-pack.md)。

这些样例不是往届真实学生报告，不包含 hidden tests、staff-only grading packet、私人反馈、学生身份或未授权数据。课程运行后若加入真实优秀项目，应按 showcase/archive policy 完成 consent、redaction、artifact_manifest 和 archived_label。

## Use Rules

| 规则 | 要求 |
|------|------|
| exemplar_id | 每个样例使用稳定 ID，例如 `EX-INF-A-01` |
| track | training engineering / inference engineering / default final project / custom |
| synthetic_status | `synthetic`、`anonymized` 或 `archived_public_report` |
| score_band | A / B / C / not_passing，不提供可复制完整答案 |
| evidence_focus | 明确样例想示范的报告证据 |
| student_visible | 必须为 Yes；若含私人评分或真实提交则不得进入本文件 |
| archive_boundary | 说明公开边界和不可复用内容 |

使用方式：

- 学生：阅读样例结构，学习如何写 evidence-backed claim；不得复制样例文字、数字或实验设置作为自己的项目结果。
- 助教：用样例统一“足够证据”和“证据不足”的判定口径。
- 教师：每轮开课后可替换为真实脱敏优秀项目，但必须保留 synthetic/anonymized/archived label。

## Exemplar Overview

| exemplar_id | track | score_band | evidence_focus | common teaching use |
|-------------|-------|------------|----------------|---------------------|
| `EX-INF-A-01` | inference engineering | A | SLO、capacity planning、RAG failure taxonomy、claim boundary | 展示系统型项目如何支撑 latency/cost/quality/safety |
| `EX-TRAIN-B-01` | training engineering | B | 数据审计、checkpoint/resume、loss curve、single_seed_limit | 展示工程完整但统计证据不足的报告 |
| `EX-DEFAULT-C-01` | default final project | C | Tiny GPT 跑通、下游任务弱、错误分析浅 | 展示“能跑”但不等于高分 |
| `EX-NP-FAIL-01` | custom / classic NLP evaluation | not_passing | 指标误用、不可复现、claim 过强 | 展示不通过条件 |

## EX-INF-A-01: Inference Engineering A-Band Exemplar

| field | content |
|-------|---------|
| exemplar_id | `EX-INF-A-01` |
| synthetic_status | synthetic |
| score_band | A |
| track | inference engineering |
| public_boundary | 可学生可见；数字为教学样例，不代表真实 benchmark |
| evidence_focus | OpenAI-compatible API、RAG eval、SLO、capacity planning、failure taxonomy、cost |

### Abstract Pattern

```text
We built a CPU-friendly OpenAI-compatible inference service with retrieval,
JSON response validation, tool-call regression tests, and a fixed benchmark.
On a 5-case evaluation set the service passed 5/5 semantic checks. With
4 requests and concurrency 2, p95 latency stayed below the course SLO,
TTFT stayed below 800 ms, and tokens/s stayed above 100. The main limitation
is that the evaluation set is small and synthetic, so we only claim that the
service satisfies the course acceptance workload, not production readiness.
```

为什么这是 A 档写法：

- 先说 workload 和 scope，不直接说“production ready”。
- 同时报告 quality、latency、throughput、SLO 和局限。
- 把 claim 限定到 course acceptance workload。

### Evidence Table

| evidence item | example content | rubric link |
|---------------|-----------------|-------------|
| primary command | `.venv/bin/python verify_course.py --capstone` | 复现性 |
| eval result | `pass_rate=5/5`, cases: kv_cache_retrieval, latency_terms, serving_checklist, json_response_format, tool_call_capacity | 指标选择 |
| benchmark | requests=4, concurrency=2, error_rate=0.00%, p95 latency < 2000 ms, TTFT p95 < 800 ms, TPOT p95 < 40 ms | 工程判断 |
| capacity plan | weights_gb、kv_cache_gb、runtime_overhead_gb、safety_margin、max_batch_by_memory | 工程判断 |
| failure cases | retrieval miss, malformed JSON, tool call timeout | 错误分析 |
| claim_audit | “SLO pass for course workload” keep; “production scale” downgrade | 表达与引用 |

### Results Pattern

| metric | value | condition | supported claim | unsupported claim |
|--------|-------|-----------|-----------------|-------------------|
| pass_rate | 5/5 | fixed course eval set | acceptance cases pass | broad user satisfaction |
| p95 latency | below SLO | requests=4, concurrency=2 | course SLO met | high-concurrency production stability |
| tokens/s | above threshold | CPU demo workload | benchmark path works | GPU serving efficiency |
| error_rate | 0.00% | small synthetic workload | no errors in acceptance run | long-tail reliability |

### Error Analysis Pattern

| case | input | expected | actual | error type | likely cause | next action |
|------|-------|----------|--------|------------|--------------|-------------|
| 1 | retrieval query with paraphrase | cite correct chunk | retrieved adjacent chunk | retrieval | chunk embedding too lexical | add rerank or query expansion |
| 2 | JSON schema with optional field | valid JSON | missing optional field | structured output | schema prompt underspecified | add schema validator and repair |
| 3 | tool call requiring numeric capacity | tool args valid | unit mismatch | tool use | prompt lacks unit convention | enforce unit tests in tool schema |

### Feedback Note

Student-visible feedback:

```text
This report makes appropriately bounded claims. The strongest evidence is the
link between fixed eval cases, SLO metrics, and capacity planning. The main
upgrade path is to broaden the evaluation set and add repeated-run variance.
```

Calibration note:

- A 档不要求“真实生产级”，但必须说明 workload、限制和未支持的 claim。
- 若缺少 P95/P99、TTFT/TPOT 或 capacity plan，应降到 B 或 C。

## EX-TRAIN-B-01: Training Engineering B-Band Exemplar

| field | content |
|-------|---------|
| exemplar_id | `EX-TRAIN-B-01` |
| synthetic_status | synthetic |
| score_band | B |
| track | training engineering |
| public_boundary | 可学生可见；数字为教学样例 |
| evidence_focus | 数据审计、训练日志、checkpoint/resume、成本估算，统计不确定性不足 |

### Strengths

| evidence item | example content | why it helps |
|---------------|-----------------|--------------|
| data audit | lines, duplicate count, character set, length p50/p95/max | 证明数据不是黑箱 |
| training log | train_loss, val_loss, lr, grad_norm, tokens/s | 可诊断训练过程 |
| checkpoint resume | final_step increases from 8 to 12 after resume | 证明恢复路径有效 |
| cost plan | tokens, global_batch_tokens, steps, GPU hours, estimated_cost_usd | 连接资源与目标 |

### Missing Evidence

| missing item | consequence | upgrade path |
|--------------|-------------|--------------|
| seed_sensitivity | 不能声称训练更稳健 | 运行 3 个 seed 或写 single_seed_limit |
| baseline comparison | 不能判断改动是否有效 | 加入 no-filter or char-level baseline |
| bootstrap CI / paired comparison | 不能写显著提升 | 用 fixed validation examples 做 paired comparison |
| contamination gate script | 数据声明缺少可复核证据 | 提交 duplicate/leakage check log |

### Example Feedback

```text
The engineering chain is credible: data audit, training run, checkpoint resume,
and cost estimate are all present. The report should not claim that the
configuration is more stable or generalizes better until it includes a baseline
and uncertainty record. Current score band: B.
```

Calibration note:

- 工程路径完整但只跑单 seed，通常是 B 档，不应给 A。
- 若日志能复现但数据审计缺失，应在数据/伦理和复现性项扣分。

## EX-DEFAULT-C-01: Default Final Project C-Band Exemplar

| field | content |
|-------|---------|
| exemplar_id | `EX-DEFAULT-C-01` |
| synthetic_status | synthetic |
| score_band | C |
| track | default final project |
| public_boundary | 可学生可见；用于说明“跑通不等于高分” |
| evidence_focus | Tiny GPT 能跑，但下游评测、错误分析和 claim audit 薄弱 |

### What The Report Has

- Tiny GPT forward pass 和训练脚本能运行。
- 生成样例有 3 个 prompt。
- 报告列出 tokenizer、embedding、attention、block 和 LM head。
- 有一条主复现命令。

### Why It Is Only C-Band

| issue | rubric impact | example |
|-------|---------------|---------|
| no fixed downstream eval | 实验设计弱 | 只展示主观挑选的 3 个输出 |
| no baseline | 指标无法解释 | 没有 greedy vs top-p 或 tiny vs baseline 对比 |
| shallow error analysis | 错误分析弱 | 只写“模型有时重复” |
| no metric_card | 指标选择弱 | 没说明 distinct-n、loss 或 human rating 的局限 |
| missing data ethics details | 数据与伦理弱 | 只写“公开数据，无风险” |

### Upgrade Checklist

| action | expected evidence |
|--------|-------------------|
| add fixed prompt set | prompt_id、expected behavior、failure label |
| add baseline | greedy vs top-p, no-RoPE vs RoPE, or smaller context baseline |
| add metric_card | metric definition、aggregation、known failure |
| add 3 failure cases | input、expected、actual、likely cause、next action |
| add claim_audit | downgrade “improves generation” to “improves distinct-n on fixed prompts” |

Student-visible feedback:

```text
This submission demonstrates that the implementation can run, but the report
does not yet provide enough evidence for strong experimental claims. Treat the
current result as a working prototype and add fixed evaluation, baseline, and
failure analysis before claiming improvement.
```

## EX-NP-FAIL-01: Not-Passing Exemplar

| field | content |
|-------|---------|
| exemplar_id | `EX-NP-FAIL-01` |
| synthetic_status | synthetic |
| score_band | not_passing |
| track | custom / classic NLP evaluation |
| public_boundary | 可学生可见；不含真实学生信息 |
| evidence_focus | 指标误用、不可复现、claim 过强 |

### Failure Pattern

报告声称：

```text
Our RAG system is significantly better and safer because ROUGE improved from
0.42 to 0.48 on our examples.
```

不通过原因：

| issue | why it fails |
|-------|--------------|
| no reproduction command | 核心结果无法复现 |
| no split_card | 不知道 examples 是 dev、test 还是手选展示样例 |
| no uncertainty_record | `0.42 -> 0.48` 不能支持 “significantly better” |
| metric misuse | ROUGE 词面重合不能单独证明 factuality 或 safety |
| no failure cases | 没有检索失败、幻觉或拒答分析 |
| missing data ethics | 不知道检索语料是否含 PII、许可证或污染风险 |

Required remediation:

1. 提交主复现命令和机器可读结果文件。
2. 填写 split_card、metric_card、uncertainty_record 和 claim_audit。
3. 把 “significantly better and safer” 降级为可证据支持的具体 claim。
4. 补至少 3 个失败案例。
5. 按 data/ethics review 说明语料来源、许可证、隐私和残余风险。

Student-visible feedback:

```text
The current report cannot pass because the main claim is not reproducible and
the metric does not support the stated conclusion. Re-submit with commands,
split/metric/uncertainty records, and bounded claims.
```

## Rubric Mapping

| rubric dimension | A-band evidence | B/C warning sign | not-passing trigger |
|------------------|-----------------|------------------|---------------------|
| 问题定义 | input/output/non-goals/success criteria explicit | vague user scenario | no measurable target |
| 复现性 | command, env, seed, logs, artifact manifest | command present but logs incomplete | no command or contradictory logs |
| 实验设计 | baseline + ablation + fixed split | only one comparison | hand-picked examples only |
| 指标选择 | metric_card + limitation + uncertainty | metric reported without limitation | metric cannot support claim |
| 错误分析 | >=3 classified failures with next action | generic failure discussion | no failure cases |
| 工程判断 | cost/latency/memory/data quality tradeoff | one engineering metric only | no engineering constraints |
| 数据与伦理 | license/PII/bias/contamination/safety/residual risk | “low risk” but little evidence | missing or false “no risk” |
| 贡献与归档 | contribution evidence + archive boundary | contribution statement only | hidden/private material exposed |

## Exemplar Review Worksheet

助教可用下表进行课堂或 office hours 练习：

| question | student answer should include |
|----------|------------------------------|
| Which claim is strongest? | claim text, supporting metric/log, scope |
| Which claim is over-stated? | missing evidence, downgrade wording |
| What evidence would move this to A-band? | baseline, uncertainty, failure case, data/ethics, capacity |
| What should not be copied? | synthetic numbers, report phrasing, exact experiment setting |
| What should be reused as pattern? | table structure, bounded claims, traceability from command to result |

## Archive Boundary

当课程运行后加入真实优秀项目：

- 把 `synthetic_status` 改成 `anonymized` 或 `archived_public_report`。
- synthetic 或 anonymized 样例不能冒充 archived public report。
- 删除 student_id、邮箱、头像、私有路径、API key、成绩、private LMS 讨论和 staff-only feedback。
- 保留 artifact_manifest、reproduction_summary、source_boundary 和 archived_label。
- 明确写“不作为本轮评分依据，也不是可复制答案”。
- 若团队只同意 institution-only，不要进入 public release。

发布前检查：

- 本文件不包含真实学生身份、hidden tests、`reference_solution.py`、private grading notes 或未授权数据。
- [Project Report Template and Reproducibility Checklist](project-report-template.md)、[Capstone 项目报告 Rubric](project-report-rubric.md)、[Final Project Showcase and Archive Policy](final-project-showcase-archive-policy.md) 和 [Capstone Project Gallery and Idea Bank](capstone-project-gallery.md) 均能链接本文件。
- `.venv/bin/python verify_course.py` 通过。
