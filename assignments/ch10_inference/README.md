# Chapter 10 Assignment: Inference Engineering

本作业对应第 10 章推理优化与工程落地。目标是实现 KV Cache、显存估算、prefix cache 复用估算、continuous batching admission gate、INT8 量化、最小 RAG、contrastive retrieval training、pairwise reranker training、检索质量指标、hybrid retrieval / reranking、MMR 多样化选择、RAG context packing、RAG 失败归因、structured output reliability gate、tool use 工程协议校验、MCP/tool runtime security gate、基准指标、production rollout gate、serving overload response gate、prefill/decode 解耦 trace 报告、P/D worker pool 容量规划、speculative decoding 服务 gate、long-context serving gate 和 LSH 检索。

## Files

- `starter.py`: 学生起始代码。
- `reference_solution.py`: 参考实现。
- `tests.py`: 可运行测试。

## Run

```bash
.venv/bin/python assignments/ch10_inference/tests.py
```

默认测试 `reference_solution.py`。测试学生代码时：

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch10_inference/tests.py
```

## Requirements

- `AttentionWithCache` 的逐 token 增量输出应与整段 causal attention 输出一致。
- KV Cache 显存公式必须包含 batch size、层数、KV 头数、head dim、序列长度和 dtype bytes。
- INT8 量化使用 per-output-channel 对称 scale，零权重不能产生 NaN。
- RAG 检索使用余弦相似度，返回按相关性降序排列的 chunk。
- `contrastive_inbatch_loss` 应使用 normalized query/document embeddings、in-batch negatives 和 InfoNCE cross entropy 训练 bi-encoder retrieval embedding。
- `pairwise_reranker_loss` 应使用 chosen/rejected query-document scores 训练 cross-encoder reranker，使相关文档分数高于无关文档。
- `recall_at_k`、`reciprocal_rank_at_k` 和 `ndcg_at_k` 必须把是否命中、首个相关结果位置和分级相关性排序质量分开度量。
- `reciprocal_rank_fusion` 和 `rerank_documents` 必须能把 dense/sparse 排序融合，并用 query-document scorer 对候选文档重排。
- `maximal_marginal_relevance` 必须在 query 相似度和已选文档冗余度之间做贪心折中，避免 prompt 中塞入近重复 chunk。
- `build_rag_context` 必须在 context token budget 和预留输出 token 约束下装配带 citation 的 chunk，并报告 selected citations、used tokens 和 skipped chunks。
- `rag_answer_diagnostics` 必须把端到端 RAG 结果拆成 retrieval recall/MRR、citation precision/recall 和 failure mode，区分 retrieval miss、context/citation miss、generation error 和 success。
- `structured_output_reliability_report` 必须把 JSON parse、schema adherence、repair retry/latency、fallback/refusal 和 safety violation 分开做 gate；可解析 JSON 不等于满足业务 schema，更不能替代 safety/output guardrail。
- `validate_tool_call_plan` 必须在执行前校验 tool registry、参数 schema、权限风险、调用次数和重复循环预算；tool use 设计题还必须写清 observation 回填和失败恢复。
- `tool_runtime_security_report` 必须把 MCP/远程工具的 server trust、权限/用户同意、敏感数据外发、外部 observation 隔离、递归 LLM sampling 和 runtime budget 分开做 gate；schema 通过不代表工具可执行。
- `prefix_cache_savings` 必须按请求到达顺序计算最长可复用历史前缀、每条请求新增 prefill token、总节省 token 和 prefix cache hit rate。
- `continuous_batching_admission_report` 必须把一批待调度请求按 priority/waiting 排序，检查 `max_num_seqs`、`max_num_batched_tokens`、active KV tokens、prefix cache、chunked prefill 和 queue wait SLO，输出 admitted/queued、queued reasons、gate 信号和 action items。
- benchmark summary 应报告 TTFT、TPOT、tokens/s 和显存。
- benchmark summary 应记录任务、样本量、baseline、指标、风险、不确定性和结论边界。
- `production_rollout_gate_report` 必须把候选模型/配置的 offline quality、安全、SLO、错误率、成本、canary 样本/流量、control comparison、监控字段和 rollback readiness 放进同一张发布 gate；离线评测提升不能直接推出全量发布。
- `serving_overload_response_report` 必须把运行期 queue、TTFT、TPOT、KV cache usage、swapping、错误率、timeout、租户配额和 degraded/scaleout readiness 放进同一张过载响应 gate；SLO 已经变坏时要能区分限流、load shedding、降级、扩容、回滚或 incident page。
- `prefill_decode_disaggregation_report` 必须把请求拆成 prefill、KV transfer、decode queue、TPOT 和 active KV tokens，报告 P95、likely bottleneck、SLO 是否通过和违反项。
- `pd_pool_capacity_plan` 必须把 workload 的 QPS、平均 prompt/output tokens、prefix cache 命中率、active requests 映射到 prefill、decode、KV transfer 和 KV memory 四类容量 gate，输出所需 worker/link 数、likely bottleneck、action items 和是否应该修订 P/D 部署方案。
- `speculative_serving_gate_report` 必须把 Ch08 的 speculative decoding 接受率账本升级为服务上线判断：报告 acceptance rate、speedup、draft overhead、tokens per verify step、质量/分布校验、额外显存、QPS/workload fit，并在收益不足或风险过高时给出 action items。
- `long_context_serving_gate_report` 必须把长上下文上线判断拆成 context fit、long-context quality、position robustness 和 serving cost gate：检查是否截断/溢出，needle/citation recall 是否足够，head/middle/tail 位置覆盖和准确率是否稳定，以及 P95 TTFT/latency、KV cache usage、prefix cache hit rate 是否满足 SLO。
- LSH 检索应在同桶内返回余弦相似度最高的候选。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 推导 KV cache 显存、prefix cache 节省率、continuous batching token/seq/KV admission、量化误差、InfoNCE/in-batch negatives、pairwise reranker loss、RAG chunk/overlap、Recall@k/MRR/nDCG、MMR、context packing、RAG 失败分解、structured output parse/schema/retry gate、tool schema/权限/循环预算、MCP trust/consent/data-egress/observation isolation、canary/rollback release gate、过载/load shedding/租户隔离 gate、多模态 token 成本、TTFT/TPOT/tokens/s、prefill/decode 解耦、KV transfer、P/D pool sizing、speculative decoding gate 和 long-context gate 的上线意义 |
| Programming parts | 55 | 实现 KV cache、显存估算、prefix cache 复用估算、`continuous_batching_admission_report`、INT8 量化、contrastive retrieval loss、pairwise reranker loss、RAG/LSH、检索质量指标、RRF/rerank/MMR、context packing、RAG 失败归因、`structured_output_reliability_report`、`validate_tool_call_plan`、`tool_runtime_security_report`、benchmark 指标汇总、`production_rollout_gate_report`、`serving_overload_response_report`、`prefill_decode_disaggregation_report`、`pd_pool_capacity_plan`、`speculative_serving_gate_report`、`long_context_serving_gate_report` 和结论边界摘要 |
| Analysis / style | 10 | 说明 latency/cost/quality/safety 的上线取舍、RAG 检索与生成错误边界、长上下文 context rot/position robustness/citation recall 与 KV 成本边界、structured output 的 schema adherence/repair/fallback/safety trade-off、tool use 的 schema/权限/预算/失败恢复、MCP/remote tool trust boundary、canary/control/rollback 发布判断、queue/KV/decode/error/quota 过载响应、continuous batching/prefix cache/chunked prefill/prefill-decode/KV transfer/active KV memory/speculative decoding 的瓶颈归因、多模态失败模式和前沿 benchmark 适用范围 |
