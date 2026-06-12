# LLM Inference Engineering Capstone

这个项目把课程最后几章落成一个可运行的推理工程作品：一个 OpenAI-compatible Chat API，带流式输出、RAG stub、基础指标、压测脚本和上线准备说明。

默认实现使用 `MockEngine`，不需要 GPU 或真实模型。目标是先跑通推理服务工程骨架，再把 `MockEngine` 替换为 vLLM、SGLang、TensorRT-LLM 或 llama.cpp。推理项目重点覆盖 OpenAI-compatible API、RAG/JSON/tool 回归、continuous batching admission、speculative decoding gate、TTFT/TPOT/P95/P99、tokens/s、显存估算和容量规划。

## 你要交付什么

| 模块 | 最低要求 | 交付内容 |
|------|----------|----------|
| API | `POST /v1/chat/completions`，兼容 OpenAI 风格请求/响应 | `curl` 能返回 `choices[0].message.content` |
| Streaming | `stream=true` 返回 SSE token 流 | 客户端逐 chunk 收到 `data: ...` |
| RAG | 能注入检索上下文，记录命中文档 | 响应里返回 `x_retrieved_docs` |
| Structured Output | `response_format={"type":"json_object"}` 返回可解析 JSON | `evaluate.py` 检查 JSON key |
| Tool Calling | 接收 OpenAI 风格 `tools` schema，返回 `tool_calls`，并在执行前做 schema/权限/预算 gate | `evaluate.py` 检查工具名，报告记录 gate |
| Reasoning Budget | 对 greedy、self-consistency、best-of-N 或 verifier rerank 做 quality/token/latency/cost gate | 报告中的 generation policy 表 |
| Speculative Decoding | 若采用或讨论 draft/EAGLE/MTP/n-gram/suffix 推测解码，做 acceptance/speedup/draft overhead/quality/workload gate | 报告中的 speculative gate 表 |
| Admission Control | 若采用 vLLM/SGLang/TensorRT-LLM 或讨论高并发服务，报告 `max_num_seqs`、`max_num_batched_tokens`、active KV tokens、chunked prefill 和 queue wait gate | 报告中的 admission 表 |
| Metrics | 暴露请求数、token 数、TTFT、TPOT | `GET /metrics` 有 JSON 指标 |
| Benchmark | 生成 P50/P95/P99、tokens/s、错误率 | `python benchmark.py` 输出报告 |
| PD Breakdown | 拆分 prefill、KV transfer、decode queue、TPOT 和 active KV tokens | 报告中的 PD 指标表 |
| PD Pool Plan | 用 QPS、prompt/output 长度、prefix cache、worker 吞吐、KV transfer 和 decode KV 容量估算 P/D worker pool | 报告中的 P/D capacity 表 |
| SLO Check | 将压测 JSON 与延迟/吞吐/错误率目标对比 | `python slo_check.py` 输出 PASS/FAIL |
| Evaluation | 跑固定评测集，检查 JSON/事实/拒答 | `python evaluate.py` 输出 pass rate |
| Capacity | 估算权重显存、KV Cache、最大 batch、token 成本 | `python capacity_plan.py` 输出容量计划 |
| Acceptance | 自动启动服务并串联评测、压测、SLO、容量估算 | `python acceptance.py` 输出 ACCEPTANCE |

## 项目问题设计

这个 capstone 的重点不是“启动一个 API”，而是回答一个推理工程问题。建议从以下方向选择一个主问题：

| 研究问题 | 比较对象 | 主要指标 | 常见结论边界 |
|----------|----------|----------|--------------|
| RAG 是否改善固定问答集 | no-RAG vs RAG top-k=3/8 | pass rate、检索命中、TTFT、prompt tokens | 检索库小不代表真实知识库表现 |
| 结构化输出策略是否可靠 | prompt-only JSON vs JSON mode / retry | JSON 有效率、重试次数、latency | MockEngine 的格式稳定性不能代表真实模型 |
| 并发增加如何影响尾延迟 | concurrency 1/2/5/10 | P50/P95/P99、tokens/s、error rate | 本地 CPU 网络开销与 GPU serving 不同 |
| 容量规划对上下文长度多敏感 | context 4K/8K/32K | KV Cache GB、max batch、$/1M tokens | 估算公式不包含全部 runtime overhead |
| prefill/decode 解耦是否值得 | single pool vs P/D pool sizing | required prefill/decode workers、KV transfer utilization、active KV tokens、SLO pass | KV transfer 或 decode KV memory 可能抵消 prefill 分离收益 |
| continuous batching 参数是否合理 | base config vs tuned `max_num_seqs` / `max_num_batched_tokens` / chunked prefill | admitted/queued、queue wait、active KV tokens、P95 TTFT/TPOT | 更大 batch 可能提高吞吐但破坏尾延迟或 KV 预算 |
| speculative decoding 是否值得启用 | baseline vs draft/EAGLE/MTP/n-gram/suffix | acceptance rate、speedup、draft overhead、P95 TPOT、quality regression、memory overhead | 高接受率仍可能被 draft 成本、高 QPS batch、额外显存或质量回归抵消 |
| reasoning/test-time compute 是否值得上线 | greedy vs self-consistency/best-of-N/verifier rerank | pass rate、output tokens、P95 latency、cost/request | 多采样提升可能被延迟、成本或 verifier 偏差抵消 |
| 多模态输入如何改变服务成本 | 文本请求 vs 图像/文档请求的视觉 token 预算 | prefill tokens、TTFT、KV Cache、任务 pass rate | 视觉 encoder 和裁剪策略会显著改变结果 |

建议把项目拆成三个阶段：

| 阶段 | 交付 |
|------|------|
| Proposal | 写出服务场景、SLO、baseline、评测集、容量假设 |
| Milestone | 跑通 API、评测、压测和容量估算，给出第一版失败案例 |
| Final Report | 补充 ablation、尾延迟分析、成本估算、降级方案和结论边界 |

## 快速开始

```bash
cd projects/inference-engineering-capstone
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

uvicorn app:app --host 127.0.0.1 --port 8000
```

一键运行：

```bash
python acceptance.py --port 8020 --requests 8 --concurrency 2
```

这条命令会自动启动本地服务，依次执行 health、`evaluate.py`、`benchmark.py`、`slo_check.py` 和 `capacity_plan.py`，最后关闭服务。

非流式请求：

```bash
curl -s http://127.0.0.1:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"mock-llm","messages":[{"role":"user","content":"解释 KV Cache"}],"max_tokens":64}'
```

流式请求：

```bash
curl -N http://127.0.0.1:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"mock-llm","stream":true,"messages":[{"role":"user","content":"什么是 TTFT?"}],"max_tokens":32}'
```

结构化 JSON 请求：

```bash
curl -s http://127.0.0.1:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"mock-llm","response_format":{"type":"json_object"},"messages":[{"role":"user","content":"输出推理服务运行结果"}],"max_tokens":256}'
```

工具调用请求：

```bash
curl -s http://127.0.0.1:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"mock-llm","messages":[{"role":"user","content":"请调用工具估算 8B 模型容量"}],"tools":[{"type":"function","function":{"name":"capacity_plan","description":"Estimate inference memory and cost.","parameters":{"type":"object","properties":{"params_b":{"type":"number"},"context":{"type":"integer"},"gpu_memory_gb":{"type":"number"}}}}}]}'
```

压测：

```bash
python benchmark.py --url http://127.0.0.1:8000 --requests 50 --concurrency 5 \
  --json-output benchmark_report.json
```

SLO 目标：

```bash
python slo_check.py --benchmark-json benchmark_report.json \
  --max-p95-latency-ms 2000 --max-p95-ttft-ms 800 \
  --max-p95-tpot-ms 40 --min-tokens-per-second 100
```

评测：

```bash
python evaluate.py --url http://127.0.0.1:8000 --cases eval_cases.jsonl
```

容量与成本估算：

```bash
python capacity_plan.py \
  --params-b 8 --layers 32 --kv-heads 8 --head-dim 128 \
  --context 8192 --batch-size 16 --gpu-memory-gb 80 \
  --tokens-per-second 5000 --gpu-hour-cost 2.5
```

## 替换真实推理引擎

从 `app.py` 的 `MockEngine.generate()` 开始替换：

| 目标引擎 | 替换点 | 注意事项 |
|----------|--------|----------|
| vLLM | 调用 vLLM OpenAI server 或 Python engine | 关注 continuous batching、prefix cache、TPOT |
| SGLang | 调用 SGLang runtime/server | 关注结构化输出和 RadixAttention |
| TensorRT-LLM | 调用部署好的 TRT-LLM endpoint | 关注模型编译、engine 版本和 GPU 绑定 |
| llama.cpp | 调用 llama-server OpenAI-compatible API | 关注 GGUF 量化、CPU/RAM、Apple Metal |

## 上线准备

- P95 TTFT、P95 TPOT、P99 total latency 已测。
- 若采用或讨论 prefill/decode 解耦，必须单独报告 prefill、KV transfer、decode queue、TPOT 和 active KV tokens，不能只给端到端 P95。
- 若采用或讨论 speculative decoding，必须单独报告 accepted/draft tokens、target verify steps、draft_ms、speedup、quality regression、memory overhead 和 QPS/workload fit，不能只给引擎支持或 `num_speculative_tokens`。
- 若采用或讨论 continuous batching，必须单独报告 `max_num_seqs`、`max_num_batched_tokens`、chunked prefill、admitted/queued、queue wait、active KV tokens 和 queued reasons，不能只给平均 tokens/s。
- SLO 目标可重复执行，失败时能指出是错误率、延迟还是吞吐不达标。
- 最大 prompt 长度、最大输出长度、并发上限已测。
- 显存预算包含权重、KV Cache、batch 峰值和 10-20% 安全余量。
- 每 1M tokens 的 GPU 成本已估算，且知道成本对 tokens/s 和 GPU 小时价格的敏感性。
- RAG 命中率、JSON 格式正确率、安全拒答率有固定回归集。
- 工具调用能校验 schema、权限和循环预算，返回 `tool_calls`，并记录工具执行结果。
- 指标能按模型、租户、状态码、错误类型聚合。
- 限流、超时、降级和错误响应格式明确。

## 项目报告要求

推理工程报告必须包含：

- 固定评测集 pass rate 与失败案例。
- 若使用 LLM-as-judge 或人工偏好近似指标，必须报告 position/verbosity bias、swapped-order consistency 和少量 human label agreement；未通过时不能把 judge win rate 作为上线依据。
- P50/P95/P99 latency、TTFT、TPOT、tokens/s 和错误率。
- 权重显存、KV Cache、runtime overhead、安全余量和每 1M tokens 成本。
- RAG、JSON structured output、tool calling 和 reasoning budget 的回归用例。
- 超时、限流、降级、格式错误和安全拒答策略。
- 明确说明你的研究问题、baseline、workload、结论适用条件，以及哪些结果只在 MockEngine / 本地 CPU 下成立。

### Final report 结构

推理项目的报告应回答“这个服务在什么 workload 下是否值得上线或灰度”，而不是只说明 API 能启动：

1. **Service scenario.** 描述目标场景：客服 RAG、结构化抽取、工具调用、长文档问答、多模态文档理解等。
2. **Research question.** 提出可测问题，例如“RAG top-k 从 3 增到 8 是否提高 pass rate，代价是多少 TTFT 和 prompt tokens？”
3. **Related work.** 连接至少 2 篇论文、技术报告或官方文档，例如 vLLM/PagedAttention、FlashAttention、RAG、Orca、SGLang、TensorRT-LLM、structured output 或 model card，说明项目采用和简化了什么。
4. **Workload definition.** 固定请求数量、并发、prompt token 分布、max output tokens、是否 streaming、是否 RAG/tool/JSON、是否多样本 reasoning 或 verifier rerank。
5. **Baseline.** 明确 baseline，例如 no-RAG、prompt-only JSON、concurrency=1 或默认 capacity setting。
6. **Ablation.** 一次只改变一个工程因素：top-k、concurrency、context length、JSON mode/retry、SLO threshold 或容量假设。
7. **Quality result.** 报告 pass rate、失败案例、RAG 命中/引用问题、JSON 解析失败、tool call schema/permission/budget 问题、reasoning budget gate、judge reliability audit 和安全拒答/过度拒答。
8. **System result.** 报告 P50/P95/P99 latency、TTFT、TPOT、tokens/s、error rate，并说明瓶颈在排队、prefill、decode、RAG 检索还是后处理。
9. **Continuous batching admission.** 若采用或讨论 high-concurrency serving，报告 `max_num_seqs`、`max_num_batched_tokens`、prefix cache、chunked prefill、admitted/queued、queue wait 和 active KV gate。
10. **Speculative decoding gate.** 若采用或讨论 speculative decoding，报告 acceptance rate、speedup、draft overhead、tokens per verify step、quality regression、memory overhead 和 QPS/workload fit，并说明是否启用。
11. **PD / KV transfer analysis.** 若 workload 中长 prompt、RAG 或多模态请求造成 TTFT 波动，拆分 prefill、KV transfer、decode queue、TPOT 和 active KV tokens，判断是否需要 prefill/decode 解耦。
12. **Capacity and cost.** 用 `capacity_plan.py` 估算权重显存、KV Cache、active KV tokens、admission limit、max batch、每 1M tokens 成本和安全余量。
13. **Decision and reproducibility.** 给出上线判断：通过、需要灰度、需要降级策略，或不建议上线；同时写清不能外推到真实模型/GPU/更大知识库的部分，并列出服务启动、评测、压测、SLO 和容量估算命令。

### 结果表模板

| Run | 改动 | pass rate | P95 TTFT | P95 TPOT | P99 latency | tokens/s | error rate | 成本/风险结论 |
|-----|------|-----------|----------|----------|-------------|----------|------------|----------------|
| baseline | 默认配置 | | | | | | | |
| ablation | 例如 RAG top-k=8 | | | | | | | |

### Generation policy 模板

| Strategy | accuracy/pass rate | samples/request | output tokens/request | P95 latency | cost/request | Gate | 结论 |
|----------|--------------------|-----------------|-----------------------|-------------|--------------|------|------|
| greedy / self-consistency / best-of-N | | | | | | | |

### Prefill/Decode 解耦指标模板

| Run | P95 prefill | P95 KV transfer | P95 decode queue | P95 TPOT | max active KV tokens | likely bottleneck | SLO 结论 |
|-----|-------------|-----------------|------------------|----------|----------------------|-------------------|----------|
| unified baseline | | | | | | | |
| PD experiment / estimate | | | | | | | |

### Speculative decoding gate 模板

| Run | method | acceptance rate | speedup | draft overhead | tokens/verify step | quality regression | memory overhead | QPS fit | 结论 |
|-----|--------|-----------------|---------|----------------|--------------------|--------------------|-----------------|---------|------|
| baseline vs speculative | | | | | | | | | |

### Continuous batching admission 模板

| Config | max_num_seqs | max_num_batched_tokens | chunked prefill | admitted | queued | max queue wait | active KV tokens | action |
|--------|--------------|------------------------|-----------------|----------|--------|----------------|------------------|--------|
| baseline | | | | | | | | |

### P/D capacity 模板

| Workload | QPS | effective prefill tok/s | decode tok/s | KV transfer tok/s | prefill workers | decode workers | KV links | KV memory gate | 结论 |
|----------|-----|-------------------------|--------------|-------------------|-----------------|----------------|----------|----------------|------|
| baseline | | | | | | | | | |

### 失败分类模板

| 类别 | 判定方式 | 例子 | 下一步动作 |
|------|----------|------|------------|
| Retrieval miss | relevant doc 未进入 top-k | 知识库有答案但未召回 | 改 chunk、embedding、hybrid/RRF |
| Context packing miss | relevant doc 召回但未进入最终 prompt | token budget 被重复 chunk 占满 | MMR、rerank、压缩上下文 |
| Generation error | evidence 在 prompt 中但答案错误 | 引用正确但结论错 | 调 prompt、模型、decode、评测集 |
| Format/tool error | JSON 不可解析或 tool schema 错 | `tool_calls` 缺参数 | schema 校验、约束解码、重试 |
| Serving error | 超时、429、5xx 或 P95/P99 超 SLO | 并发升高后尾延迟爆炸 | 限流、队列隔离、capacity 扩容 |

一个合格结论应同时包含质量和系统代价。例如“top-k=8 pass rate 从 72% 到 78%，但 P95 TTFT 从 650ms 到 1250ms，且 context packing miss 未下降，因此只建议在离线问答或更宽松 SLO 下使用”，比“top-k=8 更好”更严谨。
