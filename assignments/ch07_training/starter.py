"""Starter code for Chapter 7 training-loop assignment."""

from dataclasses import dataclass

import torch
from torch.utils.data import DataLoader, Dataset


class TextDataset(Dataset):
    def __init__(self, data_path, tokenizer, block_size=1024):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, idx):
        raise NotImplementedError


def create_dataloader(data_path, tokenizer, batch_size=8, block_size=1024, shuffle=True, num_workers=0):
    raise NotImplementedError


def cross_entropy_manual(logits, targets):
    raise NotImplementedError


class AdamW:
    def __init__(self, params, lr=3e-4, betas=(0.9, 0.95), eps=1e-8, weight_decay=0.1):
        raise NotImplementedError

    def zero_grad(self):
        raise NotImplementedError

    def step(self, grads=None):
        raise NotImplementedError


def get_cosine_schedule_with_warmup(optimizer, num_warmup_steps, num_training_steps, min_lr_ratio=0.1):
    raise NotImplementedError


@dataclass
class TrainConfig:
    num_epochs: int = 1
    max_grad_norm: float = 1.0
    log_interval: int = 10
    use_amp: bool = False
    dtype: str = "float32"
    device: str = "cpu"


def train(model, dataloader, optimizer, scheduler, config, loss_history=None):
    raise NotImplementedError


def perplexity(loss):
    raise NotImplementedError
