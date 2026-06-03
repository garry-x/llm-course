import argparse
from dataclasses import dataclass


DTYPE_BYTES = {
    "fp32": 4.0,
    "bf16": 2.0,
    "fp16": 2.0,
    "fp8": 1.0,
    "int8": 1.0,
    "int4": 0.5,
}


@dataclass
class ModelConfig:
    params_b: float
    layers: int
    kv_heads: int
    head_dim: int
    weight_dtype: str
    kv_dtype: str


def gb_from_bytes(value: float) -> float:
    return value / (1024 ** 3)


def weight_memory_gb(cfg: ModelConfig) -> float:
    return gb_from_bytes(cfg.params_b * 1_000_000_000 * DTYPE_BYTES[cfg.weight_dtype])


def kv_cache_gb(cfg: ModelConfig, context: int, batch_size: int) -> float:
    bytes_per_token = 2 * cfg.layers * cfg.kv_heads * cfg.head_dim * DTYPE_BYTES[cfg.kv_dtype]
    return gb_from_bytes(bytes_per_token * context * batch_size)


def estimate(args: argparse.Namespace) -> dict:
    cfg = ModelConfig(
        params_b=args.params_b,
        layers=args.layers,
        kv_heads=args.kv_heads,
        head_dim=args.head_dim,
        weight_dtype=args.weight_dtype,
        kv_dtype=args.kv_dtype,
    )
    weights = weight_memory_gb(cfg)
    kv = kv_cache_gb(cfg, args.context, args.batch_size)
    runtime_overhead = weights * args.runtime_overhead_ratio
    total = (weights + kv + runtime_overhead) * (1 + args.safety_margin)
    hourly_tokens = args.tokens_per_second * 3600
    cost_per_million = args.gpu_hour_cost / max(hourly_tokens / 1_000_000, 1e-9)
    max_batch_by_memory = int(
        max(
            0,
            (
                args.gpu_memory_gb / (1 + args.safety_margin)
                - weights
                - runtime_overhead
            )
            / max(kv_cache_gb(cfg, args.context, 1), 1e-9)
        )
    )
    return {
        "weight_gb": weights,
        "kv_cache_gb": kv,
        "runtime_overhead_gb": runtime_overhead,
        "total_with_margin_gb": total,
        "fits_gpu": total <= args.gpu_memory_gb,
        "max_batch_by_memory": max_batch_by_memory,
        "cost_per_1m_tokens_usd": cost_per_million,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM inference memory and cost capacity planner")
    parser.add_argument("--params-b", type=float, default=8.0, help="Model parameter count in billions")
    parser.add_argument("--layers", type=int, default=32)
    parser.add_argument("--kv-heads", type=int, default=8)
    parser.add_argument("--head-dim", type=int, default=128)
    parser.add_argument("--context", type=int, default=8192)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--weight-dtype", choices=sorted(DTYPE_BYTES), default="fp16")
    parser.add_argument("--kv-dtype", choices=sorted(DTYPE_BYTES), default="fp16")
    parser.add_argument("--gpu-memory-gb", type=float, default=80.0)
    parser.add_argument("--runtime-overhead-ratio", type=float, default=0.10)
    parser.add_argument("--safety-margin", type=float, default=0.15)
    parser.add_argument("--tokens-per-second", type=float, default=5000.0)
    parser.add_argument("--gpu-hour-cost", type=float, default=2.50)
    args = parser.parse_args()

    result = estimate(args)
    print("Capacity plan")
    print(f"model_params_b: {args.params_b}")
    print(f"context: {args.context}, batch_size: {args.batch_size}")
    print(f"weight_dtype: {args.weight_dtype}, kv_dtype: {args.kv_dtype}")
    print(f"weight_gb: {result['weight_gb']:.2f}")
    print(f"kv_cache_gb: {result['kv_cache_gb']:.2f}")
    print(f"runtime_overhead_gb: {result['runtime_overhead_gb']:.2f}")
    print(f"total_with_margin_gb: {result['total_with_margin_gb']:.2f}")
    print(f"gpu_memory_gb: {args.gpu_memory_gb:.2f}")
    print(f"fits_gpu: {result['fits_gpu']}")
    print(f"max_batch_by_memory: {result['max_batch_by_memory']}")
    print(f"cost_per_1m_tokens_usd: {result['cost_per_1m_tokens_usd']:.4f}")


if __name__ == "__main__":
    main()
