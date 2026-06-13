# Chapter 10 Assignment: Inference Engineering

This assignment corresponds to Chapter 10 Inference Optimization and Engineering Deployment. The goal is to implement KV Cache, memory estimation, prefix cache reuse estimation, continuous batching admission gate, INT8 quantization, minimal RAG, contrastive retrieval training, pairwise reranker training, retrieval quality metrics, hybrid retrieval / reranking, MMR diversification, RAG context packing, RAG failure attribution, structured output reliability gate, tool use engineering protocol validation, MCP/tool runtime security gate, benchmark metrics, production rollout gate, serving overload response gate, prefill/decode disaggregation trace report, P/D worker pool capacity planning, speculative decoding service gate, long-context serving gate, and LSH retrieval.

## Files

- `starter.py`: Student starter code.
- `reference_solution.py`: Reference implementation.
- `tests.py`: Runnable tests.

## Run

```bash
.venv/bin/python assignments/ch10_inference/tests.py
```

By default, tests `reference_solution.py`. To test student code:

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch10_inference/tests.py
```

## Requirements

- The per-token incremental output of `AttentionWithCache` must be consistent with the full causal attention output.
- The KV Cache memory formula must include batch size, number of layers, number of KV heads, head dimension, sequence length, and dtype bytes.
- INT8 quantization uses per-output-channel symmetric scale; zero weights must not produce NaN.
- RAG retrieval uses cosine similarity, returning chunks sorted by relevance in descending order.
- `contrastive_inbatch_loss` should use normalized query/document embeddings, in-batch negatives, and InfoNCE cross entropy to train bi-encoder retrieval embeddings.
- `pairwise_reranker_loss` should use chosen/rejected query-document scores to train a cross-encoder reranker, ensuring relevant document scores are higher than irrelevant ones.
- `recall_at_k`, `reciprocal_rank_at_k`, and `ndcg_at_k` must separately measure whether a hit occurred, the position of the first relevant result, and the quality of graded relevance ranking.
- `reciprocal_rank_fusion` and `rerank_documents` must be able to fuse dense/sparse rankings and re-rank candidate documents using a query-document scorer.
- `maximal_marginal_relevance` must make a greedy trade-off between query similarity and redundancy among already selected documents, avoiding near-duplicate chunks in the prompt.
- `build_rag_context` must assemble chunks with citations under the constraints of a context token budget and reserved output tokens, and report selected citations, used tokens, and skipped chunks.
- `rag_answer_diagnostics` must decompose end-to-end RAG results into retrieval recall/MRR, citation precision/recall, and failure modes, distinguishing between retrieval miss, context/citation miss, generation error, and success.
- `structured_output_reliability_report` must separately gate JSON parsing, schema adherence, repair retry/latency, fallback/refusal, and safety violations; parseable JSON does not equal meeting the business schema, nor can it replace safety/output guardrails.
- `validate_tool_call_plan` must validate the tool registry, parameter schema, permission risks, call count, and repetition loop budget before execution; tool use design questions must also clearly describe observation backfill and failure recovery.
- `tool_runtime_security_report` must separately gate MCP/remote tool server trust, permissions/user consent, sensitive data egress, external observation isolation, recursive LLM sampling, and runtime budget; passing schema does not mean the tool is executable.
- `prefix_cache_savings` must calculate the longest reusable historical prefix, new prefill tokens per request, total saved tokens, and prefix cache hit rate based on request arrival order.
- `continuous_batching_admission_report` must sort a batch of pending requests by priority/waiting time, check `max_num_seqs`, `max_num_batched_tokens`, active KV tokens, prefix cache, chunked prefill, and queue wait SLO, and output admitted/queued, queued reasons, gate signals, and action items.
- The benchmark summary should report TTFT, TPOT, tokens/s, and memory.
- The benchmark summary should record the task, sample size, baseline, metrics, risks, uncertainties, and conclusion boundaries.
- `production_rollout_gate_report` must place the candidate model/configuration's offline quality, safety, SLO, error rate, cost, canary samples/traffic, control comparison, monitoring fields, and rollback readiness into a single release gate; offline evaluation improvements alone cannot directly trigger a full rollout.
- `serving_overload_response_report` must place runtime queue, TTFT, TPOT, KV cache usage, swapping, error rate, timeout, tenant quota, and degraded/scaleout readiness into a single overload response gate; when SLO has already degraded, it must distinguish between rate limiting, load shedding, degradation, scaling, rollback, or incident page.
- `prefill_decode_disaggregation_report` must decompose requests into prefill, KV transfer, decode queue, TPOT, and active KV tokens, reporting P95, likely bottleneck, whether SLO is met, and violations.
- `pd_pool_capacity_plan` must map workload QPS, average prompt/output tokens, prefix cache hit rate, and active requests to four capacity gates: prefill, decode, KV transfer, and KV memory, outputting required worker/link counts, likely bottleneck, action items, and whether the P/D deployment plan should be revised.
- `speculative_serving_gate_report` must upgrade the speculative decoding acceptance rate ledger from Ch08 to a service launch decision: report acceptance rate, speedup, draft overhead, tokens per verify step, quality/distribution validation, additional memory, QPS/workload fit, and provide action items when benefits are insufficient or risks are too high.
- `long_context_serving_gate_report` must decompose the long-context launch decision into context fit, long-context quality, position robustness, and serving cost gates: check for truncation/overflow, whether needle/citation recall is sufficient, whether head/middle/tail position coverage and accuracy are stable, and whether P95 TTFT/latency, KV cache usage, and prefix cache hit rate meet SLO.
- LSH retrieval should return the candidate with the highest cosine similarity within the same bucket.

## Grading Rubric

| Item | Points | Criteria |
|------|:--:|------|
| Written questions | 35 | Derive the significance of KV cache memory, prefix cache savings rate, continuous batching token/seq/KV admission, quantization error, InfoNCE/in-batch negatives, pairwise reranker loss, RAG chunk/overlap, Recall@k/MRR/nDCG, MMR, context packing, RAG failure decomposition, structured output parse/schema/retry gate, tool schema/permissions/loop budget, MCP trust/consent/data-egress/observation isolation, canary/rollback release gate, overload/load shedding/tenant isolation gate, multimodal token cost, TTFT/TPOT/tokens/s, prefill/decode disaggregation, KV transfer, P/D pool sizing, speculative decoding gate, and long-context gate |
| Programming parts | 55 | Implement KV cache, memory estimation, prefix cache reuse estimation, `continuous_batching_admission_report`, INT8 quantization, contrastive retrieval loss, pairwise reranker loss, RAG/LSH, retrieval quality metrics, RRF/rerank/MMR, context packing, RAG failure attribution, `structured_output_reliability_report`, `validate_tool_call_plan`, `tool_runtime_security_report`, benchmark metric summary, `production_rollout_gate_report`, `serving_overload_response_report`, `prefill_decode_disaggregation_report`, `pd_pool_capacity_plan`, `speculative_serving_gate_report`, `long_context_serving_gate_report`, and conclusion boundary summary |
| Analysis / style | 10 | Explain latency/cost/quality/safety launch trade-offs, RAG retrieval and generation error boundaries, long-context context rot/position robustness/citation recall and KV cost boundaries, structured output schema adherence/repair/fallback/safety trade-offs, tool use schema/permissions/budget/failure recovery, MCP/remote tool trust boundary, canary/control/rollback launch decisions, queue/KV/decode/error/quota overload response, bottleneck attribution for continuous batching/prefix cache/chunked prefill/prefill-decode/KV transfer/active KV memory/speculative decoding, multimodal failure modes, and the applicability scope of frontier benchmarks |