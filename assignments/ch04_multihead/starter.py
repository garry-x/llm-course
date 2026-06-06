"""Starter code for Chapter 4 multi-head attention assignment."""

import torch
import torch.nn as nn


def repeat_kv_heads(kv, n_rep):
    """Repeat [B, H_kv, T, D] K/V heads to [B, H_kv*n_rep, T, D] for GQA."""
    raise NotImplementedError


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_heads, dropout=0.1):
        super().__init__()
        raise NotImplementedError

    def forward(self, x, mask=None):
        raise NotImplementedError


class SingleHeadAttention(nn.Module):
    def __init__(self, d_model):
        super().__init__()
        raise NotImplementedError

    def forward(self, x, mask=None):
        raise NotImplementedError


class GroupedQueryAttention(nn.Module):
    def __init__(self, d_model, n_heads, n_kv_heads, dropout=0.1):
        super().__init__()
        raise NotImplementedError

    def forward(self, x, mask=None):
        raise NotImplementedError


class MLA(nn.Module):
    def __init__(self, d_model, n_heads, d_latent, dropout=0.1):
        super().__init__()
        raise NotImplementedError

    def forward(self, x, mask=None):
        raise NotImplementedError


def mla_absorbed_attention_scores(q, latent_kv, up_k_weight, scale=None):
    """Compute MLA content attention scores without explicitly decompressing K."""
    raise NotImplementedError


def count_params(model):
    raise NotImplementedError


def gqa_head_mapping(n_heads, n_kv_heads):
    raise NotImplementedError


def compute_kv_cache_size(d_model, n_heads, n_kv_heads, d_latent, seq_len):
    raise NotImplementedError


def compare_kv_cache_budget(
    d_model,
    n_heads,
    n_kv_heads,
    d_latent,
    seq_len,
    batch_size=1,
    n_layers=1,
    dtype_bytes=2,
):
    """Compare total KV-cache memory for MHA, GQA, and MLA."""
    raise NotImplementedError
