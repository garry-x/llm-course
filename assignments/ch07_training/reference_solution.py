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


def cross_entropy_manual(logits, targets):
    batch, seq_len, vocab_size = logits.shape
    logits_flat = logits.reshape(batch * seq_len, vocab_size)
    targets_flat = targets.reshape(batch * seq_len)
    logits_max = logits_flat.max(dim=-1, keepdim=True).values
    logits_stable = logits_flat - logits_max
    log_probs = logits_stable - logits_stable.exp().sum(dim=-1, keepdim=True).log()
    nll = -log_probs.gather(dim=-1, index=targets_flat.unsqueeze(-1)).squeeze(-1)
    return nll.mean()


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
