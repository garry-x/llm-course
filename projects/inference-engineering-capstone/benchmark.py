import argparse
import asyncio
import statistics
import time

import httpx


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0
    values = sorted(values)
    idx = min(len(values) - 1, int((pct / 100) * (len(values) - 1)))
    return values[idx]


async def one_request(client: httpx.AsyncClient, url: str, prompt: str) -> dict:
    started = time.perf_counter()
    resp = await client.post(
        f"{url}/v1/chat/completions",
        json={
            "model": "mock-llm",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 96,
        },
        timeout=30,
    )
    elapsed_ms = (time.perf_counter() - started) * 1000
    resp.raise_for_status()
    data = resp.json()
    usage = data["usage"]
    return {
        "latency_ms": elapsed_ms,
        "ttft_ms": data["x_metrics"]["ttft_ms"],
        "tpot_ms": data["x_metrics"]["tpot_ms"],
        "tokens": usage["completion_tokens"],
    }


async def run(url: str, requests: int, concurrency: int) -> None:
    prompts = [
        "解释 KV Cache 和 PagedAttention 的区别",
        "如何优化 TTFT 和 TPOT",
        "生产推理服务上线前要检查什么",
        "RAG 在推理系统中解决什么问题",
    ]
    sem = asyncio.Semaphore(concurrency)
    async with httpx.AsyncClient() as client:
        async def guarded(i: int) -> dict:
            async with sem:
                return await one_request(client, url, prompts[i % len(prompts)])

        started = time.perf_counter()
        results = await asyncio.gather(*(guarded(i) for i in range(requests)))
        total_s = time.perf_counter() - started

    latencies = [r["latency_ms"] for r in results]
    ttft = [r["ttft_ms"] for r in results]
    tpot = [r["tpot_ms"] for r in results]
    total_tokens = sum(r["tokens"] for r in results)
    print("Benchmark report")
    print(f"requests: {requests}, concurrency: {concurrency}")
    print(f"total_time_s: {total_s:.2f}")
    print(f"tokens_per_second: {total_tokens / total_s:.2f}")
    print(f"latency_ms p50/p95/p99: {statistics.median(latencies):.1f} / {percentile(latencies, 95):.1f} / {percentile(latencies, 99):.1f}")
    print(f"ttft_ms p50/p95: {statistics.median(ttft):.1f} / {percentile(ttft, 95):.1f}")
    print(f"tpot_ms p50/p95: {statistics.median(tpot):.1f} / {percentile(tpot, 95):.1f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    parser.add_argument("--requests", type=int, default=20)
    parser.add_argument("--concurrency", type=int, default=4)
    args = parser.parse_args()
    asyncio.run(run(args.url.rstrip("/"), args.requests, args.concurrency))
