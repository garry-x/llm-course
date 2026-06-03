import asyncio
import json
import time
import uuid
from dataclasses import dataclass, field
from statistics import mean
from typing import AsyncIterator, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field


class ResponseFormat(BaseModel):
    type: Literal["text", "json_object"] = "text"


class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str


class ToolFunction(BaseModel):
    name: str
    description: str = ""
    parameters: dict = Field(default_factory=dict)


class ToolSpec(BaseModel):
    type: Literal["function"] = "function"
    function: ToolFunction


class ChatRequest(BaseModel):
    model: str = "mock-llm"
    messages: list[Message]
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    top_p: float = Field(1.0, ge=0.0, le=1.0)
    max_tokens: int = Field(128, ge=1, le=2048)
    stream: bool = False
    use_rag: bool = True
    response_format: ResponseFormat = Field(default_factory=ResponseFormat)
    tools: list[ToolSpec] = Field(default_factory=list)
    tool_choice: Literal["auto", "none"] = "auto"


@dataclass
class Metrics:
    request_count: int = 0
    error_count: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    ttft_ms: list[float] = field(default_factory=list)
    tpot_ms: list[float] = field(default_factory=list)

    def snapshot(self) -> dict:
        return {
            "request_count": self.request_count,
            "error_count": self.error_count,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "avg_ttft_ms": mean(self.ttft_ms) if self.ttft_ms else 0,
            "avg_tpot_ms": mean(self.tpot_ms) if self.tpot_ms else 0,
            "tokens_per_second": 1000 / mean(self.tpot_ms) if self.tpot_ms else 0,
        }


class SimpleRAG:
    def __init__(self) -> None:
        self.docs = [
            "KV Cache stores previous keys and values so decoding avoids recomputing history.",
            "TTFT measures time to first token. TPOT measures time per output token.",
            "Continuous batching lets finished requests leave and new requests join each decode step.",
            "Quantization reduces memory bandwidth pressure by storing weights in lower precision.",
        ]

    def retrieve(self, query: str, k: int = 2) -> list[str]:
        lowered = query.lower()
        preferred = []
        keyword_docs = [
            (["kv", "cache", "缓存", "pagedattention"], self.docs[0]),
            (["ttft", "tpot", "延迟", "指标", "首 token"], self.docs[1]),
            (["batch", "batching", "并发", "上线", "吞吐", "服务"], self.docs[2]),
            (["量化", "显存", "带宽", "int4", "int8"], self.docs[3]),
        ]
        for keywords, doc in keyword_docs:
            if any(keyword in lowered for keyword in keywords):
                preferred.append(doc)
        if preferred:
            return preferred[:k]

        query_terms = set(query.lower().split())
        scored = []
        for doc in self.docs:
            score = len(query_terms & set(doc.lower().split()))
            scored.append((score, doc))
        return [doc for _, doc in sorted(scored, reverse=True)[:k]]


class MockEngine:
    async def generate(self, max_tokens: int, response_format: ResponseFormat) -> AsyncIterator[str]:
        text = build_mock_response(response_format)
        tokens = text[:max_tokens]
        for ch in tokens:
            await asyncio.sleep(0.003)
            yield ch


app = FastAPI(title="LLM Inference Engineering Capstone")
metrics = Metrics()
rag = SimpleRAG()
engine = MockEngine()


def count_tokens(text: str) -> int:
    return max(1, len(text) // 2)


def build_prompt(req: ChatRequest, docs: list[str]) -> str:
    messages = "\n".join(f"{m.role}: {m.content}" for m in req.messages)
    context = "\n".join(f"- {doc}" for doc in docs)
    return f"Context:\n{context}\n\nMessages:\n{messages}\nassistant:"


def build_mock_response(response_format: ResponseFormat) -> str:
    if response_format.type == "json_object":
        return json.dumps(
            {
                "answer": "这是一个结构化推理服务响应。",
                "metrics": ["TTFT", "TPOT", "tokens_per_second"],
                "next_action": "run_benchmark_and_slo_check",
            },
            ensure_ascii=False,
        )
    return (
        "这是一个推理工程 mock 响应。"
        "真实系统应替换为 vLLM/SGLang/TensorRT-LLM/llama.cpp。"
        "先拆 TTFT、TPOT、吞吐、显存和错误率，再决定优化策略。"
    )


def build_tool_call(req: ChatRequest, user_text: str) -> dict | None:
    if req.tool_choice == "none" or not req.tools:
        return None

    lowered = user_text.lower()
    should_call = any(token in lowered for token in ["工具", "tool", "capacity", "容量", "显存", "成本"])
    if not should_call:
        return None

    tool = req.tools[0]
    name = tool.function.name
    if name == "capacity_plan":
        arguments = {"params_b": 8, "context": 8192, "gpu_memory_gb": 80}
    else:
        arguments = {"query": user_text[:80]}

    return {
        "id": "call_" + uuid.uuid4().hex[:12],
        "type": "function",
        "function": {
            "name": name,
            "arguments": json.dumps(arguments, ensure_ascii=False),
        },
    }


def execute_tool_call(tool_call: dict) -> dict:
    name = tool_call["function"]["name"]
    arguments = json.loads(tool_call["function"]["arguments"])
    if name == "capacity_plan":
        result = {
            "summary": "8B FP16 model with 8K context fits in an 80GB GPU for the demo batch.",
            "estimated_total_gb": 37.25,
            "next_action": "run capacity_plan.py with production parameters",
        }
    else:
        result = {
            "summary": "mock tool executed",
            "echo": arguments,
        }
    return {"name": name, "arguments": arguments, "result": result}


async def collect_generation(max_tokens: int, response_format: ResponseFormat) -> tuple[str, float, float, int]:
    start = time.perf_counter()
    first_at = None
    chunks = []
    async for token in engine.generate(max_tokens, response_format):
        if first_at is None:
            first_at = time.perf_counter()
        chunks.append(token)
    end = time.perf_counter()
    completion_tokens = count_tokens("".join(chunks))
    ttft = ((first_at or end) - start) * 1000
    tpot = ((end - (first_at or start)) * 1000 / max(completion_tokens, 1))
    return "".join(chunks), ttft, tpot, completion_tokens


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/metrics")
async def get_metrics() -> dict:
    return metrics.snapshot()


@app.post("/v1/chat/completions")
async def chat_completions(req: ChatRequest):
    if not req.messages:
        raise HTTPException(status_code=400, detail="messages must not be empty")

    user_text = "\n".join(m.content for m in req.messages if m.role == "user")
    docs = rag.retrieve(user_text) if req.use_rag else []
    prompt = build_prompt(req, docs)
    prompt_tokens = count_tokens(prompt)
    request_id = "chatcmpl-" + uuid.uuid4().hex
    created = int(time.time())

    metrics.request_count += 1
    metrics.prompt_tokens += prompt_tokens

    tool_call = build_tool_call(req, user_text)
    if tool_call:
        tool_result = execute_tool_call(tool_call)
        content = ""
        completion_tokens = count_tokens(json.dumps(tool_call, ensure_ascii=False))
        metrics.ttft_ms.append(0)
        metrics.tpot_ms.append(0)
        metrics.completion_tokens += completion_tokens
        return JSONResponse({
            "id": request_id,
            "object": "chat.completion",
            "created": created,
            "model": req.model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content,
                    "tool_calls": [tool_call],
                },
                "finish_reason": "tool_calls",
            }],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            },
            "x_retrieved_docs": docs,
            "x_tool_results": [tool_result],
            "x_metrics": {"ttft_ms": 0, "tpot_ms": 0},
            "x_valid_json": None,
        })

    if req.stream:
        async def stream() -> AsyncIterator[str]:
            start = time.perf_counter()
            first_at = None
            completion = 0
            async for token in engine.generate(req.max_tokens, req.response_format):
                if first_at is None:
                    first_at = time.perf_counter()
                    metrics.ttft_ms.append((first_at - start) * 1000)
                completion += count_tokens(token)
                payload = {
                    "id": request_id,
                    "object": "chat.completion.chunk",
                    "created": created,
                    "model": req.model,
                    "choices": [{"index": 0, "delta": {"content": token}, "finish_reason": None}],
                }
                yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
            end = time.perf_counter()
            metrics.completion_tokens += completion
            if first_at:
                metrics.tpot_ms.append((end - first_at) * 1000 / max(completion, 1))
            yield "data: [DONE]\n\n"

        return StreamingResponse(stream(), media_type="text/event-stream")

    content, ttft, tpot, completion_tokens = await collect_generation(req.max_tokens, req.response_format)
    valid_json = None
    if req.response_format.type == "json_object":
        try:
            json.loads(content)
            valid_json = True
        except json.JSONDecodeError:
            valid_json = False
    metrics.ttft_ms.append(ttft)
    metrics.tpot_ms.append(tpot)
    metrics.completion_tokens += completion_tokens
    return JSONResponse({
        "id": request_id,
        "object": "chat.completion",
        "created": created,
        "model": req.model,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": content},
            "finish_reason": "stop",
        }],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        },
        "x_retrieved_docs": docs,
        "x_metrics": {"ttft_ms": ttft, "tpot_ms": tpot},
        "x_valid_json": valid_json,
    })
