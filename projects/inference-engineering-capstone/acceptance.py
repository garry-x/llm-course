import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parent


def wait_for_health(url: str, timeout_s: float) -> None:
    deadline = time.time() + timeout_s
    last_error = None
    while time.time() < deadline:
        try:
            with urlopen(f"{url}/health", timeout=1) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            if payload.get("status") == "ok":
                return
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
        time.sleep(0.25)
    raise RuntimeError(f"service did not become healthy: {last_error}")


def run_step(name: str, cmd: list[str]) -> None:
    print(f"\n== {name} ==")
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"{name} failed with exit code {result.returncode}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the full capstone acceptance check")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8020)
    parser.add_argument("--requests", type=int, default=8)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--min-tokens-per-second", type=float, default=100.0)
    args = parser.parse_args()

    url = f"http://{args.host}:{args.port}"
    benchmark_json = None
    server = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app:app",
            "--host",
            args.host,
            "--port",
            str(args.port),
        ],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        wait_for_health(url, timeout_s=10)
        print(f"service: healthy at {url}")

        run_step("evaluation", [sys.executable, "evaluate.py", "--url", url, "--cases", "eval_cases.jsonl"])

        with tempfile.NamedTemporaryFile(prefix="capstone-benchmark-", suffix=".json", delete=False) as tmp:
            benchmark_json = tmp.name
        run_step(
            "benchmark",
            [
                sys.executable,
                "benchmark.py",
                "--url",
                url,
                "--requests",
                str(args.requests),
                "--concurrency",
                str(args.concurrency),
                "--json-output",
                benchmark_json,
            ],
        )
        run_step(
            "slo",
            [
                sys.executable,
                "slo_check.py",
                "--benchmark-json",
                benchmark_json,
                "--max-p95-latency-ms",
                "2000",
                "--max-p95-ttft-ms",
                "800",
                "--max-p95-tpot-ms",
                "40",
                "--min-tokens-per-second",
                str(args.min_tokens_per_second),
            ],
        )
        run_step(
            "capacity",
            [
                sys.executable,
                "capacity_plan.py",
                "--params-b",
                "8",
                "--layers",
                "32",
                "--kv-heads",
                "8",
                "--head-dim",
                "128",
                "--context",
                "8192",
                "--batch-size",
                "16",
                "--gpu-memory-gb",
                "80",
                "--tokens-per-second",
                "5000",
                "--gpu-hour-cost",
                "2.5",
            ],
        )
        print("\nACCEPTANCE: PASS")
        return 0
    finally:
        if benchmark_json:
            Path(benchmark_json).unlink(missing_ok=True)
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait(timeout=5)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"\nACCEPTANCE: FAIL ({exc})", file=sys.stderr)
        sys.exit(1)
