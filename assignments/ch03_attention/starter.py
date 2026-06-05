"""Starter code for Chapter 3 attention assignment."""

import torch
import torch.nn as nn


class QKVProjection(nn.Module):
    """Project input X into Query, Key and Value tensors."""

    def __init__(self, d_model, d_k):
        super().__init__()
        raise NotImplementedError

    def forward(self, x):
        raise NotImplementedError


def scaled_dot_product_attention(Q, K, V, mask=None):
    """Return (output, attention_weights)."""
    raise NotImplementedError


def create_causal_mask(seq_len):
    """Return a boolean lower-triangular causal mask."""
    raise NotImplementedError


def causal_attention(Q, K, V):
    """Scaled dot-product attention with a causal mask."""
    raise NotImplementedError


def plot_attention(attn_weights, tokens, title="Attention Weights"):
    """Return a matplotlib (fig, ax) heatmap for attention weights."""
    raise NotImplementedError
