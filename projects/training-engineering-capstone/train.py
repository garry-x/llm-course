import argparse
import json
import math
import random
import time
from pathlib import Path

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ModuleNotFoundError as exc:
    raise SystemExit(
        "PyTorch is required for train.py. Install it with: pip install -r requirements.txt"
    ) from exc


def set_seed(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


class CharDataset:
    def __init__(self, path: Path, train_ratio: float = 0.9):
        text = path.read_text(encoding="utf-8")
        if len(text) < 128:
            raise ValueError("training corpus is too small; provide at least 128 characters")

        chars = sorted(set(text))
        self.stoi = {ch: i for i, ch in enumerate(chars)}
        self.itos = {i: ch for ch, i in self.stoi.items()}
        tokens = torch.tensor([self.stoi[ch] for ch in text], dtype=torch.long)
        split = max(1, min(len(tokens) - 1, int(len(tokens) * train_ratio)))
        self.train = tokens[:split]
        self.val = tokens[split:]
        if len(self.val) < 2:
            self.val = self.train

    @property
    def vocab_size(self) -> int:
        return len(self.stoi)

    def get_batch(self, split: str, batch_size: int, seq_len: int, device: torch.device):
        data = self.train if split == "train" else self.val
        if len(data) <= seq_len + 1:
            data = self.train
        max_start = max(1, len(data) - seq_len - 1)
        starts = torch.randint(0, max_start, (batch_size,))
        x = torch.stack([data[i : i + seq_len] for i in starts]).to(device)
        y = torch.stack([data[i + 1 : i + 1 + seq_len] for i in starts]).to(device)
        return x, y


class TinyLM(nn.Module):
    def __init__(self, vocab_size: int, seq_len: int, d_model: int, layers: int, heads: int, dropout: float):
        super().__init__()
        self.seq_len = seq_len
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.position_embedding = nn.Embedding(seq_len, d_model)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=heads,
            dim_feedforward=4 * d_model,
            dropout=dropout,
            batch_first=True,
            norm_first=True,
            activation="gelu",
        )
        self.blocks = nn.TransformerEncoder(encoder_layer, num_layers=layers)
        self.ln_f = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size)

    def forward(self, idx: torch.Tensor, targets: torch.Tensor | None = None):
        _, t = idx.shape
        if t > self.seq_len:
            raise ValueError(f"sequence length {t} exceeds model context {self.seq_len}")

        pos = torch.arange(0, t, device=idx.device)
        x = self.token_embedding(idx) + self.position_embedding(pos)[None, :, :]
        causal_mask = torch.triu(torch.ones(t, t, device=idx.device, dtype=torch.bool), diagonal=1)
        x = self.blocks(x, mask=causal_mask)
        logits = self.lm_head(self.ln_f(x))
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
        return logits, loss


@torch.no_grad()
def evaluate(model: nn.Module, dataset: CharDataset, args: argparse.Namespace, device: torch.device) -> float:
    model.eval()
    losses = []
    for _ in range(args.eval_batches):
        x, y = dataset.get_batch("val", args.batch_size, args.seq_len, device)
        _, loss = model(x, y)
        losses.append(float(loss.item()))
    model.train()
    return sum(losses) / len(losses)


def build_scheduler(optimizer: torch.optim.Optimizer, args: argparse.Namespace):
    def lr_lambda(step: int) -> float:
        if step < args.warmup_steps:
            return max(0.01, (step + 1) / max(1, args.warmup_steps))
        progress = (step - args.warmup_steps) / max(1, args.steps - args.warmup_steps)
        return 0.1 + 0.9 * 0.5 * (1.0 + math.cos(math.pi * min(1.0, progress)))

    return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)


def write_jsonl(path: Path, payload: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def save_checkpoint(path: Path, model, optimizer, scheduler, args, dataset, global_step: int, best_val_loss: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "scheduler": scheduler.state_dict(),
            "config": vars(args),
            "global_step": global_step,
            "best_val_loss": best_val_loss,
            "vocab": {"stoi": dataset.stoi, "itos": dataset.itos},
            "rng_state": torch.get_rng_state(),
            "cuda_rng_state_all": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
        },
        path,
    )


def train(args: argparse.Namespace) -> None:
    set_seed(args.seed)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = out_dir / "metrics.jsonl"
    checkpoint_path = out_dir / "checkpoints" / "latest.pt"

    device = torch.device("cuda" if torch.cuda.is_available() and not args.cpu else "cpu")
    dataset = CharDataset(Path(args.data))
    model = TinyLM(dataset.vocab_size, args.seq_len, args.d_model, args.layers, args.heads, args.dropout).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    scheduler = build_scheduler(optimizer, args)

    global_step = 0
    best_val_loss = float("inf")
    if args.resume:
        if not checkpoint_path.exists():
            raise FileNotFoundError(f"cannot resume; checkpoint not found: {checkpoint_path}")
        checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
        model.load_state_dict(checkpoint["model"])
        optimizer.load_state_dict(checkpoint["optimizer"])
        scheduler.load_state_dict(checkpoint["scheduler"])
        global_step = int(checkpoint["global_step"])
        best_val_loss = float(checkpoint["best_val_loss"])
        if "rng_state" in checkpoint:
            torch.set_rng_state(checkpoint["rng_state"])
        if torch.cuda.is_available() and checkpoint.get("cuda_rng_state_all") is not None:
            torch.cuda.set_rng_state_all(checkpoint["cuda_rng_state_all"])

    config = vars(args) | {"device": str(device), "vocab_size": dataset.vocab_size}
    (out_dir / "config.json").write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")

    model.train()
    amp_enabled = args.amp and device.type == "cuda"
    scaler = torch.cuda.amp.GradScaler(enabled=amp_enabled)
    start_time = time.perf_counter()
    for step in range(global_step + 1, args.steps + 1):
        iter_start = time.perf_counter()
        x, y = dataset.get_batch("train", args.batch_size, args.seq_len, device)
        with torch.cuda.amp.autocast(enabled=amp_enabled):
            _, loss = model(x, y)
        scaler.scale(loss).backward()
        scaler.unscale_(optimizer)
        grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), args.grad_clip)
        scaler.step(optimizer)
        scaler.update()
        scheduler.step()
        optimizer.zero_grad(set_to_none=True)

        tokens = args.batch_size * args.seq_len
        iter_time = max(1e-9, time.perf_counter() - iter_start)
        if step % args.log_every == 0 or step == 1:
            write_jsonl(
                metrics_path,
                {
                    "type": "train",
                    "step": step,
                    "train_loss": float(loss.item()),
                    "lr": float(scheduler.get_last_lr()[0]),
                    "grad_norm": float(grad_norm),
                    "tokens_per_second": float(tokens / iter_time),
                    "device": str(device),
                    "amp": bool(amp_enabled),
                },
            )

        if step % args.eval_every == 0 or step == args.steps:
            val_loss = evaluate(model, dataset, args, device)
            best_val_loss = min(best_val_loss, val_loss)
            write_jsonl(
                metrics_path,
                {
                    "type": "eval",
                    "step": step,
                    "val_loss": float(val_loss),
                    "perplexity": float(math.exp(min(20.0, val_loss))),
                    "best_val_loss": float(best_val_loss),
                },
            )

        if step % args.save_every == 0 or step == args.steps:
            save_checkpoint(checkpoint_path, model, optimizer, scheduler, args, dataset, step, best_val_loss)

    total_time = time.perf_counter() - start_time
    print(
        json.dumps(
            {
                "status": "ok",
                "out_dir": str(out_dir),
                "final_step": args.steps,
                "best_val_loss": best_val_loss,
                "elapsed_seconds": round(total_time, 3),
                "device": str(device),
            },
            ensure_ascii=False,
        )
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a tiny PyTorch character language model")
    parser.add_argument("--data", default="sample_corpus.txt")
    parser.add_argument("--out-dir", default="runs/demo")
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--seq-len", type=int, default=64)
    parser.add_argument("--d-model", type=int, default=64)
    parser.add_argument("--layers", type=int, default=2)
    parser.add_argument("--heads", type=int, default=4)
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--weight-decay", type=float, default=0.1)
    parser.add_argument("--warmup-steps", type=int, default=5)
    parser.add_argument("--grad-clip", type=float, default=1.0)
    parser.add_argument("--eval-batches", type=int, default=4)
    parser.add_argument("--log-every", type=int, default=1)
    parser.add_argument("--eval-every", type=int, default=10)
    parser.add_argument("--save-every", type=int, default=10)
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--cpu", action="store_true", help="Force CPU even when CUDA is available")
    parser.add_argument("--amp", action="store_true", help="Use CUDA automatic mixed precision")
    return parser.parse_args()


if __name__ == "__main__":
    train(parse_args())
