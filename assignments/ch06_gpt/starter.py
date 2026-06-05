"""Starter code for Chapter 6 GPT model assembly assignment."""

from dataclasses import dataclass
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class GPTConfig:
    vocab_size: int = 50257
    max_seq_len: int = 1024
    d_model: int = 768
    n_heads: int = 12
    n_layers: int = 12
    d_ff: Optional[int] = None
    dropout: float = 0.1
    bias: bool = True
    tie_weights: bool = True


class CausalSelfAttention(nn.Module):
    def __init__(self, config: GPTConfig):
        super().__init__()
        raise NotImplementedError

    def forward(self, x, mask=None):
        raise NotImplementedError


class GPT2MLP(nn.Module):
    def __init__(self, config: GPTConfig):
        super().__init__()
        raise NotImplementedError

    def forward(self, x):
        raise NotImplementedError


class GPT2Block(nn.Module):
    def __init__(self, config: GPTConfig):
        super().__init__()
        raise NotImplementedError

    def forward(self, x, mask=None):
        raise NotImplementedError


class GPTModel(nn.Module):
    def __init__(self, config: GPTConfig):
        super().__init__()
        raise NotImplementedError

    def _init_weights(self, module):
        raise NotImplementedError

    def forward(self, input_ids, mask=None):
        raise NotImplementedError


def count_parameters(model):
    raise NotImplementedError


def parameter_breakdown(model):
    raise NotImplementedError


class MoERouter(nn.Module):
    def __init__(self, d_model, n_experts=256, top_k=8):
        super().__init__()
        raise NotImplementedError

    def forward(self, x, bias=None):
        raise NotImplementedError


class AuxLossFreeBalancer:
    def __init__(self, n_experts, bias_update_rate=0.01, bias_clip=0.1):
        raise NotImplementedError

    def update(self, token_counts):
        raise NotImplementedError

    def apply_bias(self, gate_logits):
        raise NotImplementedError

    def get_load_stats(self, token_counts):
        raise NotImplementedError
