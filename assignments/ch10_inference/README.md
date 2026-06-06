# Chapter 10 Assignment: Inference Engineering

本作业对应第 10 章推理优化与工程落地。目标是实现 KV Cache、显存估算、prefix cache 复用估算、INT8 量化、最小 RAG、contrastive retrieval training、pairwise reranker training、检索质量指标、hybrid retrieval / reranking、MMR 多样化选择、RAG context packing、基准指标和 LSH 检索。

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
- `prefix_cache_savings` 必须按请求到达顺序计算最长可复用历史前缀、每条请求新增 prefill token、总节省 token 和 prefix cache hit rate。
- benchmark summary 应报告 TTFT、TPOT、tokens/s 和显存。
- benchmark summary 应记录任务、样本量、baseline、指标、风险、不确定性和结论边界。
- LSH 检索应在同桶内返回余弦相似度最高的候选。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 推导 KV cache 显存、prefix cache 节省率、量化误差、InfoNCE/in-batch negatives、pairwise reranker loss、RAG chunk/overlap、Recall@k/MRR/nDCG、MMR、context packing、RAG 失败分解、多模态 token 成本、TTFT/TPOT/tokens/s 和 SLO 的上线意义 |
| Programming parts | 55 | 实现 KV cache、显存估算、prefix cache 复用估算、INT8 量化、contrastive retrieval loss、pairwise reranker loss、RAG/LSH、检索质量指标、RRF/rerank/MMR、context packing、benchmark 指标汇总和结论边界摘要 |
| Analysis / style | 10 | 说明 latency/cost/quality/safety 的上线取舍、RAG 检索与生成错误边界、多模态失败模式和前沿 benchmark 适用范围 |
