# LLM Inference Engineering Capstone

这个项目把课程最后几章落成一个可验收的推理工程作品：一个 OpenAI-compatible Chat API，带流式输出、RAG stub、基础指标、压测脚本和上线检查清单。

默认实现使用 `MockEngine`，不需要 GPU 或真实模型。目标是先跑通推理服务工程骨架，再把 `MockEngine` 替换为 vLLM、SGLang、TensorRT-LLM 或 llama.cpp。

## 你要交付什么

| 模块 | 最低要求 | 验收证据 |
|------|----------|----------|
| API | `POST /v1/chat/completions`，兼容 OpenAI 风格请求/响应 | `curl` 能返回 `choices[0].message.content` |
| Streaming | `stream=true` 返回 SSE token 流 | 客户端逐 chunk 收到 `data: ...` |
| RAG | 能注入检索上下文，记录命中文档 | 响应里返回 `x_retrieved_docs` |
| Structured Output | `response_format={"type":"json_object"}` 返回可解析 JSON | `evaluate.py` 检查 JSON key |
| Tool Calling | 接收 OpenAI 风格 `tools` schema，返回 `tool_calls` | `evaluate.py` 检查工具名 |
| Metrics | 暴露请求数、token 数、TTFT、TPOT | `GET /metrics` 有 JSON 指标 |
| Benchmark | 生成 P50/P95/P99、tokens/s、错误率 | `python benchmark.py` 输出报告 |
| SLO Check | 将压测 JSON 与延迟/吞吐/错误率目标对比 | `python slo_check.py` 输出 PASS/FAIL |
| Evaluation | 跑固定评测集，检查 JSON/事实/拒答 | `python evaluate.py` 输出 pass rate |
| Capacity | 估算权重显存、KV Cache、最大 batch、token 成本 | `python capacity_plan.py` 输出容量计划 |

## 快速开始

```bash
cd projects/inference-engineering-capstone
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

uvicorn app:app --host 127.0.0.1 --port 8000
```

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
  -d '{"model":"mock-llm","response_format":{"type":"json_object"},"messages":[{"role":"user","content":"输出推理服务验收结果"}],"max_tokens":256}'
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

SLO 门禁：

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

## 上线验收清单

- P95 TTFT、P95 TPOT、P99 total latency 已测。
- SLO 门禁可重复执行，失败时能指出是错误率、延迟还是吞吐不达标。
- 最大 prompt 长度、最大输出长度、并发上限已测。
- 显存预算包含权重、KV Cache、batch 峰值和 10-20% 安全余量。
- 每 1M tokens 的 GPU 成本已估算，且知道成本对 tokens/s 和 GPU 小时价格的敏感性。
- RAG 命中率、JSON 格式正确率、安全拒答率有固定回归集。
- 工具调用能校验 schema、返回 `tool_calls`，并记录工具执行结果。
- 指标能按模型、租户、状态码、错误类型聚合。
- 限流、超时、降级和错误响应格式明确。
