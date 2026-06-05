# Chapter 10 Assignment: Inference Engineering

本作业对应第 10 章推理优化与工程落地。目标是实现 KV Cache、显存估算、INT8 量化、最小 RAG、基准指标和 LSH 检索。

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
- benchmark summary 应报告 TTFT、TPOT、tokens/s 和显存。
- metric card 应记录任务、样本量、baseline、指标、风险、不确定性和结论边界。
- LSH 检索应在同桶内返回余弦相似度最高的候选。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 推导 KV cache 显存、量化误差、RAG chunk/overlap、RAG 失败分解、多模态 token 成本、TTFT/TPOT/tokens/s 和 SLO 的上线意义 |
| Programming parts | 55 | 实现 KV cache、显存估算、INT8 量化、RAG/LSH、benchmark 指标汇总和 metric card |
| Analysis / style | 10 | 说明 latency/cost/quality/safety 的上线取舍、RAG 检索与生成错误边界、多模态失败模式和前沿 benchmark 来源边界 |
