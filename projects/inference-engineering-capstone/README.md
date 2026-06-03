# LLM Inference Engineering Capstone

这个项目把课程最后几章落成一个可验收的推理工程作品：一个 OpenAI-compatible Chat API，带流式输出、RAG stub、基础指标、压测脚本和上线检查清单。

默认实现使用 `MockEngine`，不需要 GPU 或真实模型。目标是先跑通推理服务工程骨架，再把 `MockEngine` 替换为 vLLM、SGLang、TensorRT-LLM 或 llama.cpp。

## 你要交付什么

| 模块 | 最低要求 | 验收证据 |
|------|----------|----------|
| API | `POST /v1/chat/completions`，兼容 OpenAI 风格请求/响应 | `curl` 能返回 `choices[0].message.content` |
| Streaming | `stream=true` 返回 SSE token 流 | 客户端逐 chunk 收到 `data: ...` |
| RAG | 能注入检索上下文，记录命中文档 | 响应里返回 `x_retrieved_docs` |
| Metrics | 暴露请求数、token 数、TTFT、TPOT | `GET /metrics` 有 JSON 指标 |
| Benchmark | 生成 P50/P95/P99、tokens/s、错误率 | `python benchmark.py` 输出报告 |
| Evaluation | 跑固定评测集，检查 JSON/事实/拒答 | `python evaluate.py` 输出 pass rate |

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

压测：

```bash
python benchmark.py --url http://127.0.0.1:8000 --requests 50 --concurrency 5
```

评测：

```bash
python evaluate.py --url http://127.0.0.1:8000 --cases eval_cases.jsonl
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
- 最大 prompt 长度、最大输出长度、并发上限已测。
- 显存预算包含权重、KV Cache、batch 峰值和 10-20% 安全余量。
- RAG 命中率、JSON 格式正确率、安全拒答率有固定回归集。
- 指标能按模型、租户、状态码、错误类型聚合。
- 限流、超时、降级和错误响应格式明确。
