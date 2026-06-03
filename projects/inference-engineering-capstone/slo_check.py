import argparse
import json
import sys


def check(name: str, value: float, op: str, threshold: float) -> tuple[bool, str]:
    if op == "<=":
        ok = value <= threshold
    elif op == ">=":
        ok = value >= threshold
    else:
        raise ValueError(f"unsupported operator: {op}")
    status = "PASS" if ok else "FAIL"
    return ok, f"{status} {name}: {value:.4f} {op} {threshold:.4f}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check benchmark report against inference service SLO")
    parser.add_argument("--benchmark-json", required=True)
    parser.add_argument("--max-error-rate", type=float, default=0.01)
    parser.add_argument("--max-p95-latency-ms", type=float, default=2000.0)
    parser.add_argument("--max-p95-ttft-ms", type=float, default=800.0)
    parser.add_argument("--max-p95-tpot-ms", type=float, default=40.0)
    parser.add_argument("--min-tokens-per-second", type=float, default=1.0)
    args = parser.parse_args()

    with open(args.benchmark_json, "r", encoding="utf-8") as f:
        report = json.load(f)

    checks = [
        check("error_rate", report["error_rate"], "<=", args.max_error_rate),
        check("latency_ms.p95", report["latency_ms"]["p95"], "<=", args.max_p95_latency_ms),
        check("ttft_ms.p95", report["ttft_ms"]["p95"], "<=", args.max_p95_ttft_ms),
        check("tpot_ms.p95", report["tpot_ms"]["p95"], "<=", args.max_p95_tpot_ms),
        check("tokens_per_second", report["tokens_per_second"], ">=", args.min_tokens_per_second),
    ]

    passed = True
    for ok, line in checks:
        passed = passed and ok
        print(line)

    print(f"SLO: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
