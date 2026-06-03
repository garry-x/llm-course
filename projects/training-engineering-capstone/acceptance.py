import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(command)}")
    return result.stdout


def read_metrics(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    try:
        import torch  # noqa: F401
    except ModuleNotFoundError as exc:
        raise RuntimeError("PyTorch is required. Run: pip install -r requirements.txt") from exc

    audit = json.loads(run([sys.executable, "data_audit.py", "--data", "sample_corpus.txt"]))
    require(audit["characters"] >= 128, "sample corpus is too small")
    require(audit["duplicate_non_empty_lines"] >= 1, "data audit should detect the intentional duplicate line")

    plan_output = run(
        [
            sys.executable,
            "plan_training.py",
            "--tokens",
            "1000000",
            "--seq-len",
            "128",
            "--micro-batch",
            "4",
            "--grad-accum",
            "2",
            "--gpus",
            "1",
            "--tokens-per-second-per-gpu",
            "1000",
            "--gpu-hour-cost",
            "1.5",
        ]
    )
    require("estimated_cost_usd" in plan_output, "training plan must include cost estimate")

    with tempfile.TemporaryDirectory(prefix="llm-training-acceptance-") as tmp:
        out_dir = Path(tmp)
        base = [
            sys.executable,
            "train.py",
            "--data",
            "sample_corpus.txt",
            "--out-dir",
            str(out_dir),
            "--batch-size",
            "4",
            "--seq-len",
            "32",
            "--d-model",
            "32",
            "--layers",
            "1",
            "--heads",
            "2",
            "--eval-batches",
            "2",
            "--log-every",
            "1",
            "--eval-every",
            "4",
            "--save-every",
            "4",
            "--cpu",
        ]
        run(base + ["--steps", "8"])
        run(base + ["--steps", "12", "--resume"])

        checkpoint = out_dir / "checkpoints" / "latest.pt"
        metrics_path = out_dir / "metrics.jsonl"
        require(checkpoint.exists(), "latest checkpoint was not saved")
        require(metrics_path.exists(), "metrics.jsonl was not written")

        metrics = read_metrics(metrics_path)
        train_rows = [row for row in metrics if row.get("type") == "train"]
        eval_rows = [row for row in metrics if row.get("type") == "eval"]
        require(max(row["step"] for row in train_rows) >= 12, "resume did not advance train step")
        require(max(row["step"] for row in eval_rows) >= 12, "resume did not advance eval step")
        require(all("tokens_per_second" in row for row in train_rows), "train metrics must include tokens/s")
        require(all("val_loss" in row and "perplexity" in row for row in eval_rows), "eval metrics are incomplete")

    print("ACCEPTANCE: PASS")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"ACCEPTANCE: FAIL ({exc})", file=sys.stderr)
        sys.exit(1)
