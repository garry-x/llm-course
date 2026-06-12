"""Reference solution for Chapter 7 training-loop assignment."""

import math
from dataclasses import dataclass

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset


class TextDataset(Dataset):
    def __init__(self, data_path, tokenizer, block_size=1024):
        with open(data_path, "r", encoding="utf-8") as f:
            text = f.read()
        self.tokens = tokenizer.encode(text)
        self.block_size = block_size
        if len(self.tokens) < block_size + 1:
            raise ValueError("tokenized text must contain at least block_size + 1 tokens")

    def __len__(self):
        return (len(self.tokens) - 1) // self.block_size

    def __getitem__(self, idx):
        if idx < 0 or idx >= len(self):
            raise IndexError(idx)
        start = idx * self.block_size
        end = start + self.block_size
        x = torch.tensor(self.tokens[start:end], dtype=torch.long)
        y = torch.tensor(self.tokens[start + 1 : end + 1], dtype=torch.long)
        return x, y


def create_dataloader(data_path, tokenizer, batch_size=8, block_size=1024, shuffle=True, num_workers=0):
    dataset = TextDataset(data_path, tokenizer, block_size)
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=False,
        drop_last=True,
    )


def _ngrams(token_ids, n):
    if n <= 0:
        raise ValueError("n must be positive")
    ids = [int(token_id) for token_id in token_ids]
    return [tuple(ids[i : i + n]) for i in range(len(ids) - n + 1)]


def ngram_repetition_rate(token_ids, n=4):
    grams = _ngrams(token_ids, n)
    if not grams:
        return 0.0
    unique = set()
    repeats = 0
    for gram in grams:
        if gram in unique:
            repeats += 1
        else:
            unique.add(gram)
    return repeats / len(grams)


def ngram_overlap_rate(train_token_ids, eval_token_ids, n=8):
    train_grams = set(_ngrams(train_token_ids, n))
    eval_grams = _ngrams(eval_token_ids, n)
    if not train_grams or not eval_grams:
        return 0.0
    overlap = sum(1 for gram in eval_grams if gram in train_grams)
    return overlap / len(eval_grams)


def global_batch_tokens(micro_batch_size, seq_len, grad_accum_steps=1, data_parallel_size=1):
    values = [micro_batch_size, seq_len, grad_accum_steps, data_parallel_size]
    if any(value <= 0 for value in values):
        raise ValueError("batch size, seq_len, grad accumulation, and data parallel size must be positive")
    return int(micro_batch_size * seq_len * grad_accum_steps * data_parallel_size)


def training_steps_for_token_budget(token_budget, global_batch_tokens_value):
    if token_budget <= 0:
        raise ValueError("token_budget must be positive")
    if global_batch_tokens_value <= 0:
        raise ValueError("global_batch_tokens_value must be positive")
    return math.ceil(token_budget / global_batch_tokens_value)


def dense_lm_training_flops(num_params, train_tokens):
    if num_params <= 0 or train_tokens <= 0:
        raise ValueError("num_params and train_tokens must be positive")
    return 6 * int(num_params) * int(train_tokens)


def optimizer_state_memory_bytes(
    num_params,
    param_dtype_bytes=2,
    grad_dtype_bytes=2,
    optimizer_state_dtype_bytes=4,
    num_moments=2,
    data_parallel_size=1,
    shard_optimizer_states=False,
):
    values = [num_params, param_dtype_bytes, grad_dtype_bytes, optimizer_state_dtype_bytes, data_parallel_size]
    if any(value <= 0 for value in values):
        raise ValueError("counts, dtype bytes, and data_parallel_size must be positive")
    if num_moments < 0:
        raise ValueError("num_moments must be non-negative")

    param_bytes = int(num_params) * int(param_dtype_bytes)
    grad_bytes = int(num_params) * int(grad_dtype_bytes)
    optimizer_state_bytes = int(num_params) * int(num_moments) * int(optimizer_state_dtype_bytes)
    per_rank_optimizer_state_bytes = optimizer_state_bytes / int(data_parallel_size) if shard_optimizer_states else optimizer_state_bytes
    total_bytes = param_bytes + grad_bytes + per_rank_optimizer_state_bytes
    return {
        "param_bytes": param_bytes,
        "grad_bytes": grad_bytes,
        "optimizer_state_bytes": optimizer_state_bytes,
        "per_rank_optimizer_state_bytes": per_rank_optimizer_state_bytes,
        "total_bytes": total_bytes,
        "total_gb": total_bytes / (1024**3),
    }


def cross_entropy_manual(logits, targets):
    batch, seq_len, vocab_size = logits.shape
    logits_flat = logits.reshape(batch * seq_len, vocab_size)
    targets_flat = targets.reshape(batch * seq_len)
    logits_max = logits_flat.max(dim=-1, keepdim=True).values
    logits_stable = logits_flat - logits_max
    log_probs = logits_stable - logits_stable.exp().sum(dim=-1, keepdim=True).log()
    nll = -log_probs.gather(dim=-1, index=targets_flat.unsqueeze(-1)).squeeze(-1)
    return nll.mean()


def cross_entropy_logits_gradient(logits, targets, ignore_index=None):
    if logits.dim() != 3:
        raise ValueError("logits must have shape [batch, seq_len, vocab_size]")
    if targets.shape != logits.shape[:2]:
        raise ValueError("targets must have shape [batch, seq_len]")

    vocab_size = logits.size(-1)
    probs = F.softmax(logits, dim=-1)
    grad = probs.clone()

    if ignore_index is None:
        valid = torch.ones_like(targets, dtype=torch.bool)
        safe_targets = targets
    else:
        valid = targets != ignore_index
        safe_targets = targets.masked_fill(~valid, 0)

    if torch.any((safe_targets[valid] < 0) | (safe_targets[valid] >= vocab_size)):
        raise ValueError("target token id out of vocabulary range")

    grad.scatter_add_(
        dim=-1,
        index=safe_targets.unsqueeze(-1),
        src=-valid.to(logits.dtype).unsqueeze(-1),
    )
    valid_count = int(valid.sum().item())
    if valid_count == 0:
        raise ValueError("at least one non-ignored target is required")
    grad = grad * valid.to(logits.dtype).unsqueeze(-1)
    return grad / valid_count


def label_smoothed_cross_entropy(logits, targets, epsilon=0.1, ignore_index=None):
    if logits.dim() != 3:
        raise ValueError("logits must have shape [batch, seq_len, vocab_size]")
    if targets.shape != logits.shape[:2]:
        raise ValueError("targets must have shape [batch, seq_len]")
    if not 0.0 <= epsilon < 1.0:
        raise ValueError("epsilon must be in [0, 1)")
    vocab_size = logits.size(-1)
    if vocab_size < 2:
        raise ValueError("vocab_size must be at least 2 for label smoothing")

    valid = torch.ones_like(targets, dtype=torch.bool)
    gather_targets = targets
    if ignore_index is not None:
        valid = targets != ignore_index
        gather_targets = targets.masked_fill(~valid, 0)
    if torch.any((gather_targets[valid] < 0) | (gather_targets[valid] >= vocab_size)):
        raise ValueError("target token id out of vocabulary range")
    if not torch.any(valid):
        raise ValueError("at least one non-ignored target is required")

    log_probs = F.log_softmax(logits.float(), dim=-1)
    nll = -log_probs.gather(dim=-1, index=gather_targets.unsqueeze(-1)).squeeze(-1)
    non_target_log_probs = log_probs.sum(dim=-1) - log_probs.gather(dim=-1, index=gather_targets.unsqueeze(-1)).squeeze(-1)
    smooth_loss = -non_target_log_probs / (vocab_size - 1)
    loss = (1.0 - float(epsilon)) * nll + float(epsilon) * smooth_loss
    return loss[valid].mean()


def clip_grad_norm(parameters, max_norm, eps=1e-6):
    if max_norm <= 0:
        raise ValueError("max_norm must be positive")
    if eps <= 0:
        raise ValueError("eps must be positive")

    params = [p for p in parameters if p.grad is not None]
    if not params:
        return {"total_norm": 0.0, "clip_coef": 1.0}

    grad_norms = torch.stack([p.grad.detach().float().norm(2) for p in params])
    total_norm = grad_norms.norm(2)
    clip_coef = min(1.0, float(max_norm) / (float(total_norm.item()) + float(eps)))
    if clip_coef < 1.0:
        for p in params:
            p.grad.detach().mul_(clip_coef)
    return {"total_norm": float(total_norm.item()), "clip_coef": clip_coef}


def gradient_accumulation_step_accounting(micro_batch_losses, grad_accum_steps, tokens_per_micro_batch):
    """Account for loss scaling, optimizer steps, scheduler steps, and consumed tokens."""
    if grad_accum_steps <= 0 or tokens_per_micro_batch <= 0:
        raise ValueError("grad_accum_steps and tokens_per_micro_batch must be positive")
    if not micro_batch_losses:
        raise ValueError("micro_batch_losses must be non-empty")
    if len(micro_batch_losses) % grad_accum_steps != 0:
        raise ValueError("micro_batch_losses must contain complete accumulation groups")

    losses = [float(loss) for loss in micro_batch_losses]
    if any(not math.isfinite(loss) for loss in losses):
        raise ValueError("micro_batch_losses must be finite")

    scaled_losses = [loss / grad_accum_steps for loss in losses]
    optimizer_steps = len(losses) // grad_accum_steps
    group_raw_means = []
    group_backward_sums = []
    for start in range(0, len(losses), grad_accum_steps):
        group = losses[start : start + grad_accum_steps]
        scaled_group = scaled_losses[start : start + grad_accum_steps]
        group_raw_means.append(sum(group) / grad_accum_steps)
        group_backward_sums.append(sum(scaled_group))

    return {
        "scaled_losses": scaled_losses,
        "group_raw_means": group_raw_means,
        "group_backward_loss_sums": group_backward_sums,
        "optimizer_steps": optimizer_steps,
        "scheduler_steps": optimizer_steps,
        "consumed_tokens": len(losses) * int(tokens_per_micro_batch),
    }


class AdamW:
    def __init__(self, params, lr=3e-4, betas=(0.9, 0.95), eps=1e-8, weight_decay=0.1):
        self.params = list(params)
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.weight_decay = weight_decay
        self.t = 0
        self.m = [torch.zeros_like(p) for p in self.params]
        self.v = [torch.zeros_like(p) for p in self.params]

    def zero_grad(self):
        for p in self.params:
            p.grad = None

    def step(self, grads=None):
        self.t += 1
        with torch.no_grad():
            for i, p in enumerate(self.params):
                g = grads[i] if grads is not None else p.grad
                if g is None:
                    continue
                self.m[i].mul_(self.beta1).add_(g, alpha=1 - self.beta1)
                self.v[i].mul_(self.beta2).addcmul_(g, g, value=1 - self.beta2)
                m_hat = self.m[i] / (1 - self.beta1**self.t)
                v_hat = self.v[i] / (1 - self.beta2**self.t)
                if self.weight_decay > 0:
                    p.mul_(1 - self.lr * self.weight_decay)
                p.addcdiv_(m_hat, v_hat.sqrt().add(self.eps), value=-self.lr)


def get_cosine_schedule_with_warmup(optimizer, num_warmup_steps, num_training_steps, min_lr_ratio=0.1):
    def lr_lambda(current_step):
        if current_step < num_warmup_steps:
            return float(current_step) / float(max(1, num_warmup_steps))
        progress = float(current_step - num_warmup_steps) / float(
            max(1, num_training_steps - num_warmup_steps)
        )
        progress = min(1.0, max(0.0, progress))
        cosine_decay = 0.5 * (1.0 + math.cos(math.pi * progress))
        return cosine_decay * (1 - min_lr_ratio) + min_lr_ratio

    return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)


def lr_schedule_trace(base_lr, num_warmup_steps, num_training_steps, min_lr_ratio=0.1, tokens_per_step=None):
    if base_lr <= 0:
        raise ValueError("base_lr must be positive")
    if num_warmup_steps < 0:
        raise ValueError("num_warmup_steps must be non-negative")
    if num_training_steps <= 0:
        raise ValueError("num_training_steps must be positive")
    if num_warmup_steps > num_training_steps:
        raise ValueError("num_warmup_steps cannot exceed num_training_steps")
    if not 0 <= min_lr_ratio <= 1:
        raise ValueError("min_lr_ratio must be in [0, 1]")
    if tokens_per_step is not None and tokens_per_step <= 0:
        raise ValueError("tokens_per_step must be positive when provided")

    steps = []
    for step in range(num_training_steps + 1):
        if num_warmup_steps > 0 and step < num_warmup_steps:
            multiplier = step / num_warmup_steps
            phase = "warmup"
        else:
            denom = max(1, num_training_steps - num_warmup_steps)
            progress = (step - num_warmup_steps) / denom
            progress = min(1.0, max(0.0, progress))
            cosine_decay = 0.5 * (1.0 + math.cos(math.pi * progress))
            multiplier = cosine_decay * (1.0 - min_lr_ratio) + min_lr_ratio
            phase = "cosine"

        row = {
            "step": step,
            "phase": phase,
            "lr_multiplier": float(multiplier),
            "lr": float(base_lr * multiplier),
        }
        if tokens_per_step is not None:
            row["consumed_tokens"] = int(step * tokens_per_step)
        steps.append(row)

    return {
        "base_lr": float(base_lr),
        "num_warmup_steps": int(num_warmup_steps),
        "num_training_steps": int(num_training_steps),
        "min_lr_ratio": float(min_lr_ratio),
        "tokens_per_step": None if tokens_per_step is None else int(tokens_per_step),
        "steps": steps,
    }


def training_system_gate_report(metrics, thresholds=None):
    """Summarize whether a training run is ready to continue, stop, or debug."""
    if not isinstance(metrics, dict):
        raise ValueError("metrics must be a dict")
    thresholds = dict(thresholds or {})
    required = ["train_loss", "val_loss", "grad_norm", "tokens_per_second", "checkpoint_resume_ok"]
    missing = [name for name in required if name not in metrics]
    if missing:
        raise ValueError(f"missing required metrics: {', '.join(missing)}")

    train_loss = float(metrics["train_loss"])
    val_loss = float(metrics["val_loss"])
    grad_norm = float(metrics["grad_norm"])
    tokens_per_second = float(metrics["tokens_per_second"])
    if not all(math.isfinite(value) for value in [train_loss, val_loss, grad_norm, tokens_per_second]):
        raise ValueError("loss, grad_norm, and tokens_per_second must be finite")

    max_train_val_gap = float(thresholds.get("max_train_val_gap", 1.0))
    max_grad_norm = float(thresholds.get("max_grad_norm", 10.0))
    min_tokens_per_second = float(thresholds.get("min_tokens_per_second", 1.0))
    min_eval_pass_rate = float(thresholds.get("min_eval_pass_rate", 0.0))
    if max_train_val_gap < 0 or max_grad_norm <= 0 or min_tokens_per_second <= 0:
        raise ValueError("thresholds must be positive")
    if not 0.0 <= min_eval_pass_rate <= 1.0:
        raise ValueError("min_eval_pass_rate must be in [0, 1]")

    gates = {
        "optimization": {
            "pass": val_loss <= train_loss + max_train_val_gap and grad_norm <= max_grad_norm,
            "signals": {"train_loss": train_loss, "val_loss": val_loss, "grad_norm": grad_norm},
        },
        "throughput": {
            "pass": tokens_per_second >= min_tokens_per_second,
            "signals": {"tokens_per_second": tokens_per_second},
        },
        "state": {
            "pass": bool(metrics["checkpoint_resume_ok"]),
            "signals": {"checkpoint_resume_ok": bool(metrics["checkpoint_resume_ok"])},
        },
        "evaluation": {
            "pass": True,
            "signals": {},
        },
    }
    if "eval_pass_rate" in metrics:
        eval_pass_rate = float(metrics["eval_pass_rate"])
        if not 0.0 <= eval_pass_rate <= 1.0:
            raise ValueError("eval_pass_rate must be in [0, 1]")
        gates["evaluation"] = {
            "pass": eval_pass_rate >= min_eval_pass_rate,
            "signals": {"eval_pass_rate": eval_pass_rate},
        }

    action_items = []
    if not gates["optimization"]["pass"]:
        action_items.append("debug_loss_or_grad_norm")
    if not gates["throughput"]["pass"]:
        action_items.append("profile_dataloader_compute_communication_or_checkpoint")
    if not gates["state"]["pass"]:
        action_items.append("fix_checkpoint_optimizer_scheduler_rng_or_sampler_state")
    if not gates["evaluation"]["pass"]:
        action_items.append("inspect_eval_regression_baseline_or_data_leakage")

    return {
        "overall_pass": not action_items,
        "gates": gates,
        "action_items": action_items,
        "decision": "continue_or_scale" if not action_items else "debug_before_scale",
    }


@dataclass
class TrainConfig:
    num_epochs: int = 1
    max_grad_norm: float = 1.0
    log_interval: int = 10
    use_amp: bool = False
    dtype: str = "float32"
    device: str = "cpu"


def _resolve_dtype(dtype):
    if isinstance(dtype, torch.dtype):
        return dtype
    mapping = {
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
        "float32": torch.float32,
    }
    return mapping[dtype]


def train(model, dataloader, optimizer, scheduler, config, loss_history=None):
    device = torch.device(config.device)
    model.to(device)
    model.train()
    use_amp = bool(config.use_amp and device.type == "cuda")
    amp_dtype = _resolve_dtype(config.dtype)

    for _epoch in range(config.num_epochs):
        for _batch_idx, (x, y) in enumerate(dataloader):
            x = x.to(device)
            y = y.to(device)
            optimizer.zero_grad()

            with torch.autocast(device_type=device.type, dtype=amp_dtype, enabled=use_amp):
                logits = model(x)
                loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), y.reshape(-1))

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), config.max_grad_norm)
            optimizer.step()
            scheduler.step()
            if loss_history is not None:
                loss_history.append(float(loss.detach().cpu()))
    return model


def perplexity(loss):
    return math.exp(float(loss))


def expected_calibration_error(logits, targets, n_bins=10, ignore_index=None):
    if n_bins <= 0:
        raise ValueError("n_bins must be positive")
    if logits.dim() < 2:
        raise ValueError("logits must have a class dimension")
    if logits.shape[:-1] != targets.shape:
        raise ValueError("targets must match logits without the class dimension")

    flat_logits = logits.reshape(-1, logits.size(-1)).float()
    flat_targets = targets.reshape(-1)
    if ignore_index is not None:
        valid = flat_targets != ignore_index
        flat_logits = flat_logits[valid]
        flat_targets = flat_targets[valid]
    if flat_targets.numel() == 0:
        raise ValueError("at least one target position is required")

    probabilities = F.softmax(flat_logits, dim=-1)
    confidence, predictions = probabilities.max(dim=-1)
    correct = (predictions == flat_targets).float()

    bin_accuracy = torch.zeros(n_bins, device=logits.device)
    bin_confidence = torch.zeros(n_bins, device=logits.device)
    bin_counts = torch.zeros(n_bins, device=logits.device)
    ece = torch.zeros((), device=logits.device)
    total = float(flat_targets.numel())

    for bin_idx in range(n_bins):
        lower = bin_idx / n_bins
        upper = (bin_idx + 1) / n_bins
        if bin_idx == n_bins - 1:
            in_bin = (confidence >= lower) & (confidence <= upper)
        else:
            in_bin = (confidence >= lower) & (confidence < upper)
        count = in_bin.sum()
        bin_counts[bin_idx] = count
        if count.item() == 0:
            continue
        acc = correct[in_bin].mean()
        conf = confidence[in_bin].mean()
        bin_accuracy[bin_idx] = acc
        bin_confidence[bin_idx] = conf
        ece = ece + (count.float() / total) * torch.abs(acc - conf)

    return {
        "ece": ece.item(),
        "bin_accuracy": bin_accuracy,
        "bin_confidence": bin_confidence,
        "bin_counts": bin_counts,
    }
