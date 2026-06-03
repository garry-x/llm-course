import argparse
import asyncio
import json
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
    try:
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
            "ok": True,
            "latency_ms": elapsed_ms,
            "ttft_ms": data["x_metrics"]["ttft_ms"],
            "tpot_ms": data["x_metrics"]["tpot_ms"],
            "tokens": usage["completion_tokens"],
        }
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "tokens": 0}


def summarize(results: list[dict], requests: int, concurrency: int, total_s: float) -> dict:
    successes = [r for r in results if r["ok"]]
    latencies = [r["latency_ms"] for r in successes]
    ttft = [r["ttft_ms"] for r in successes]
    tpot = [r["tpot_ms"] for r in successes]
    total_tokens = sum(r["tokens"] for r in successes)
    return {
        "requests": requests,
        "concurrency": concurrency,
        "success_count": len(successes),
        "error_count": requests - len(successes),
        "error_rate": (requests - len(successes)) / max(requests, 1),
        "total_time_s": total_s,
        "tokens_per_second": total_tokens / total_s if total_s else 0,
        "latency_ms": {
            "p50": statistics.median(latencies) if latencies else 0,
            "p95": percentile(latencies, 95),
            "p99": percentile(latencies, 99),
        },
        "ttft_ms": {
            "p50": statistics.median(ttft) if ttft else 0,
            "p95": percentile(ttft, 95),
        },
        "tpot_ms": {
            "p50": statistics.median(tpot) if tpot else 0,
            "p95": percentile(tpot, 95),
        },
    }


async def run(url: str, requests: int, concurrency: int) -> dict:
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

    return summarize(results, requests, concurrency, total_s)


def print_report(report: dict) -> None:
    print("Benchmark report")
    print(f"requests: {report['requests']}, concurrency: {report['concurrency']}")
    print(f"success_count: {report['success_count']}, error_count: {report['error_count']}")
    print(f"error_rate: {report['error_rate']:.2%}")
    print(f"total_time_s: {report['total_time_s']:.2f}")
    print(f"tokens_per_second: {report['tokens_per_second']:.2f}")
    print(
        "latency_ms p50/p95/p99: "
        f"{report['latency_ms']['p50']:.1f} / {report['latency_ms']['p95']:.1f} / {report['latency_ms']['p99']:.1f}"
    )
    print(f"ttft_ms p50/p95: {report['ttft_ms']['p50']:.1f} / {report['ttft_ms']['p95']:.1f}")
    print(f"tpot_ms p50/p95: {report['tpot_ms']['p50']:.1f} / {report['tpot_ms']['p95']:.1f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    parser.add_argument("--requests", type=int, default=20)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--json-output", help="Write machine-readable benchmark report to this path")
    args = parser.parse_args()
    report = asyncio.run(run(args.url.rstrip("/"), args.requests, args.concurrency))
    print_report(report)
    if args.json_output:
        with open(args.json_output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
            f.write("\n")
