# Chapter 10 Assignment: Inference Engineering

本作业对应第 10 章推理优化与工程落地。目标是实现 KV Cache、显存估算、prefix cache 复用估算、INT8 量化、最小 RAG、contrastive retrieval training、pairwise reranker training、检索质量指标、hybrid retrieval / reranking、MMR 多样化选择、RAG context packing、RAG 失败归因、基准指标和 LSH 检索。

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
- `prefix_cache_savings` 必须按请求到达顺序计算最长可复用历史前缀、每条请求新增 prefill token、总节省 token 和 prefix cache hit rate。
- benchmark summary 应报告 TTFT、TPOT、tokens/s 和显存。
- benchmark summary 应记录任务、样本量、baseline、指标、风险、不确定性和结论边界。
- LSH 检索应在同桶内返回余弦相似度最高的候选。

## Conceptual Handout

本作业不是把一组 helper 函数填完即可。你需要把一次 LLM 请求拆成四条链路：模型计算、显存占用、检索上下文和服务指标。最终报告应能回答“为什么慢、为什么贵、为什么质量不稳定、下一步优化是否真的改善目标 workload”。

### 1. KV Cache 与容量规划

Decoder-only 推理分为 prefill 和 decode。Prefill 一次处理整段 prompt，注意力计算接近矩阵乘；decode 每步只追加一个 token，但每层都要读取历史 K/V，因此长上下文和大 batch 会让显存带宽成为瓶颈。KV Cache 显存主项为：

```text
kv_bytes = batch_size * n_layers * seq_len * n_kv_heads * d_head * 2 * dtype_bytes
```

这里的 `2` 分别对应 K 和 V。若使用 GQA/MQA，`n_kv_heads` 小于 query heads，可以显著降低 KV Cache；但这不等于 attention 计算免费，也不等于权重显存减少。做容量规划时至少同时报告：

- 权重显存、KV Cache 显存、框架/碎片化安全余量。
- 平均和 P95 输入长度、输出长度、active KV tokens。
- admission limit：按活跃 token 限流，而不是只按请求数限流。
- P50/P95/P99 latency、TTFT、TPOT、tokens/s 和错误率。

一个常见错误是只写“70B fp16 需要约 140GB 权重”，却不计算 32K/128K 上下文下的 KV Cache。对长上下文服务来说，KV Cache 往往决定能同时服务多少请求。

### 2. Prefix Cache、Batching 与 SLO

Prefix cache 只复用已经计算过的公共前缀。它降低 prefill token work，但不会减少后续 decode 的全部成本。`prefix_cache_savings` 按请求到达顺序计算最长可复用历史前缀，帮助你判断系统 prompt、RAG 模板或多轮对话历史是否真的带来 cache hit。

Continuous batching 会提升 GPU 利用率，但也会让不同请求互相影响。报告 benchmark 时不要只写平均 latency：

- TTFT 主要反映排队、prefill 和首 token 生成体验。
- TPOT 主要反映 decode 阶段每 token 的稳定速度。
- P95/P99 反映用户能否接受尾延迟。
- tokens/s 是吞吐指标，不等价于单个用户体验。
- SLO 需要绑定 workload：并发数、输入/输出长度分布、采样参数和 cache 命中率。

如果一次优化让 tokens/s 上升但 P95 TTFT 变差，结论不能简单写“优化成功”。你要说明它适合吞吐优先的 batch job，还是适合交互式产品。

### 3. RAG 的训练、排序与失败归因

RAG 不是“把检索结果塞进 prompt”。一个合格系统至少包含 retrieval、reranking、context packing、generation 和 citation/answer evaluation。作业中的函数分别对应这些环节：

- `contrastive_inbatch_loss`：训练 bi-encoder，让 query 与对应文档向量接近，并把同 batch 其他文档当作 negatives。
- `pairwise_reranker_loss`：训练 cross-encoder 或 scorer，使 chosen 文档分数高于 rejected 文档。
- `recall_at_k` / `reciprocal_rank_at_k` / `ndcg_at_k`：分别衡量是否命中、首个相关文档位置和分级相关性排序质量。
- `reciprocal_rank_fusion`：融合 dense 与 sparse 排序，降低单一检索器失效风险。
- `maximal_marginal_relevance`：在 query relevance 与 chunk 多样性之间折中，避免 prompt 被近重复片段占满。
- `build_rag_context`：在 context budget 和 reserved output tokens 下选择带 citation 的 chunk。
- `rag_answer_diagnostics`：把失败归因到 retrieval miss、context/citation miss、generation error 或 success。

报告 RAG 结果时，要分开写“相关文档是否被检索到”“是否被放进上下文”“答案是否使用了正确 citation”“生成是否忠实”。如果 Recall@k 已经失败，继续调 prompt 通常不是第一优先级；如果检索命中但 citation 错，问题更可能在 context packing、引用格式或生成阶段。

### 4. 量化、LSH 与近似方法的边界

INT8 per-channel quantization 用每个输出通道自己的 scale，通常比 per-tensor scale 更稳。它降低权重显存和带宽压力，但会引入重构误差；因此作业要求用 `nrmse` 看量化前后差异。真实系统中还需要关心校准数据、activation outlier、KV cache 量化和 kernel 支持。

LSH 用随机超平面把向量分桶，只在同桶中搜索候选，适合说明 approximate nearest neighbor 的核心思想。它不能保证全局最优邻居；若 query 落到空桶或相关文档被 hash 到不同桶，就会 miss。报告近似检索时应同时写召回损失、延迟收益和失败样例。

### 5. Benchmark 结论写法

`build_benchmark_summary` 的目标是训练你把一次实验写成受条件约束的结论，而不是写一个分数表。合格结论至少包含：

- task 和 sample size。
- baseline 与当前方法。
- metrics：质量指标、系统指标和成本指标分开写。
- risks：评测污染、judge bias、检索泄漏、样本量过小、长尾输入缺失等。
- uncertainty：是否需要 bootstrap CI、重复运行或扩大样本。
- conclusion：这组结果支持什么，不支持什么。

示例：`hybrid retrieval + rerank` 在 25 个固定 RAG QA 样本上 pass rate 从 0.68 到 0.80，但 P95 latency 从 240ms 到 320ms；这支持“进入更大 dev set 和延迟优化实验”，不支持“生产中一定更好”。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 推导 KV cache 显存、prefix cache 节省率、量化误差、InfoNCE/in-batch negatives、pairwise reranker loss、RAG chunk/overlap、Recall@k/MRR/nDCG、MMR、context packing、RAG 失败分解、多模态 token 成本、TTFT/TPOT/tokens/s 和 SLO 的上线意义 |
| Programming parts | 55 | 实现 KV cache、显存估算、prefix cache 复用估算、INT8 量化、contrastive retrieval loss、pairwise reranker loss、RAG/LSH、检索质量指标、RRF/rerank/MMR、context packing、RAG 失败归因、benchmark 指标汇总和结论边界摘要 |
| Analysis / style | 10 | 说明 latency/cost/quality/safety 的上线取舍、RAG 检索与生成错误边界、多模态失败模式和前沿 benchmark 适用范围 |
