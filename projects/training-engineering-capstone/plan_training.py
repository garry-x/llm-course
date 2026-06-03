import argparse
import math


def main() -> None:
    parser = argparse.ArgumentParser(description="Plan LLM training steps, time, and cost")
    parser.add_argument("--tokens", type=int, required=True)
    parser.add_argument("--seq-len", type=int, default=2048)
    parser.add_argument("--micro-batch", type=int, default=8)
    parser.add_argument("--grad-accum", type=int, default=16)
    parser.add_argument("--gpus", type=int, default=8)
    parser.add_argument("--tokens-per-second-per-gpu", type=float, default=2500.0)
    parser.add_argument("--gpu-hour-cost", type=float, default=2.5)
    parser.add_argument("--checkpoint-gb", type=float, default=20.0)
    parser.add_argument("--checkpoint-interval", type=int, default=1000)
    args = parser.parse_args()

    global_batch_tokens = args.seq_len * args.micro_batch * args.grad_accum * args.gpus
    steps = math.ceil(args.tokens / global_batch_tokens)
    cluster_tokens_per_second = args.tokens_per_second_per_gpu * args.gpus
    hours = args.tokens / max(cluster_tokens_per_second, 1e-9) / 3600
    cost = hours * args.gpus * args.gpu_hour_cost
    checkpoint_count = max(1, math.ceil(steps / args.checkpoint_interval))
    checkpoint_storage_gb = checkpoint_count * args.checkpoint_gb

    print("Training plan")
    print(f"tokens: {args.tokens}")
    print(f"global_batch_tokens: {global_batch_tokens}")
    print(f"steps: {steps}")
    print(f"cluster_tokens_per_second: {cluster_tokens_per_second:.2f}")
    print(f"gpu_hours: {hours * args.gpus:.2f}")
    print(f"wall_clock_hours: {hours:.2f}")
    print(f"estimated_cost_usd: {cost:.2f}")
    print(f"checkpoint_count: {checkpoint_count}")
    print(f"checkpoint_storage_gb: {checkpoint_storage_gb:.2f}")


if __name__ == "__main__":
    main()
