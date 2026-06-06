"""Reference solution for Chapter 4 multi-head attention assignment."""

import torch
import torch.nn as nn
import torch.nn.functional as F


def _apply_mask(scores, mask):
    if mask is None:
        return scores
    if mask.dim() == 2:
        mask = mask.unsqueeze(0).unsqueeze(0)
    elif mask.dim() == 3:
        mask = mask.unsqueeze(1)
    return scores.masked_fill(mask == 0, float("-inf"))


def repeat_kv_heads(kv, n_rep):
    if kv.dim() != 4:
        raise ValueError("kv must have shape [B, H_kv, T, D]")
    if n_rep <= 0:
        raise ValueError("n_rep must be positive")
    if n_rep == 1:
        return kv
    return kv.repeat_interleave(n_rep, dim=1)


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_heads, dropout=0.1):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        self.W_qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.W_o = nn.Linear(d_model, d_model, bias=False)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        batch, seq_len, _ = x.shape
        qkv = self.W_qkv(x).reshape(batch, seq_len, 3, self.n_heads, self.d_k)
        q, k, v = qkv.unbind(dim=2)
        q = q.transpose(1, 2)
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)
        scores = torch.matmul(q, k.transpose(-2, -1)) / (self.d_k**0.5)
        scores = _apply_mask(scores, mask)
        attn = F.softmax(scores, dim=-1)
        attn = self.dropout(attn)
        out = torch.matmul(attn, v).transpose(1, 2).contiguous()
        out = out.reshape(batch, seq_len, self.d_model)
        return self.W_o(out), attn


class SingleHeadAttention(nn.Module):
    def __init__(self, d_model):
        super().__init__()
        self.W_qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.W_o = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x, mask=None):
        qkv = self.W_qkv(x)
        q, k, v = qkv.chunk(3, dim=-1)
        scores = torch.matmul(q, k.transpose(-2, -1)) / (q.size(-1) ** 0.5)
        scores = _apply_mask(scores, mask)
        attn = F.softmax(scores, dim=-1)
        return self.W_o(torch.matmul(attn, v))


class GroupedQueryAttention(nn.Module):
    def __init__(self, d_model, n_heads, n_kv_heads, dropout=0.1):
        super().__init__()
        assert d_model % n_heads == 0
        assert n_heads % n_kv_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.n_kv_heads = n_kv_heads
        self.d_k = d_model // n_heads
        self.n_rep = n_heads // n_kv_heads
        self.W_q = nn.Linear(d_model, n_heads * self.d_k, bias=False)
        self.W_k = nn.Linear(d_model, n_kv_heads * self.d_k, bias=False)
        self.W_v = nn.Linear(d_model, n_kv_heads * self.d_k, bias=False)
        self.W_o = nn.Linear(d_model, d_model, bias=False)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        batch, seq_len, _ = x.shape
        q = self.W_q(x).reshape(batch, seq_len, self.n_heads, self.d_k)
        k = self.W_k(x).reshape(batch, seq_len, self.n_kv_heads, self.d_k)
        v = self.W_v(x).reshape(batch, seq_len, self.n_kv_heads, self.d_k)
        q = q.transpose(1, 2)
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)
        k = repeat_kv_heads(k, self.n_rep)
        v = repeat_kv_heads(v, self.n_rep)
        scores = torch.matmul(q, k.transpose(-2, -1)) / (self.d_k**0.5)
        scores = _apply_mask(scores, mask)
        attn = F.softmax(scores, dim=-1)
        attn = self.dropout(attn)
        out = torch.matmul(attn, v).transpose(1, 2).contiguous()
        out = out.reshape(batch, seq_len, self.d_model)
        return self.W_o(out), attn


class MLA(nn.Module):
    def __init__(self, d_model, n_heads, d_latent, dropout=0.1):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        self.d_latent = d_latent
        self.W_q = nn.Linear(d_model, n_heads * self.d_k, bias=False)
        self.W_dkv = nn.Linear(d_model, d_latent, bias=False)
        self.W_uk = nn.Linear(d_latent, n_heads * self.d_k, bias=False)
        self.W_uv = nn.Linear(d_latent, n_heads * self.d_k, bias=False)
        self.W_o = nn.Linear(n_heads * self.d_k, d_model, bias=False)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        batch, seq_len, _ = x.shape
        q = self.W_q(x).reshape(batch, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        latent = self.W_dkv(x)
        k = self.W_uk(latent).reshape(batch, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        v = self.W_uv(latent).reshape(batch, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        scores = torch.matmul(q, k.transpose(-2, -1)) / (self.d_k**0.5)
        scores = _apply_mask(scores, mask)
        attn = F.softmax(scores, dim=-1)
        attn = self.dropout(attn)
        out = torch.matmul(attn, v).transpose(1, 2).contiguous()
        out = out.reshape(batch, seq_len, self.d_model)
        return self.W_o(out), attn, latent


def mla_absorbed_attention_scores(q, latent_kv, up_k_weight, scale=None):
    if q.dim() != 4:
        raise ValueError("q must have shape [B, H, T_q, D]")
    if latent_kv.dim() != 3:
        raise ValueError("latent_kv must have shape [B, T_k, D_latent]")
    if up_k_weight.dim() != 2:
        raise ValueError("up_k_weight must have shape [H * D, D_latent]")
    batch, n_heads, _t_q, d_head = q.shape
    if latent_kv.size(0) != batch:
        raise ValueError("q and latent_kv batch sizes must match")
    if up_k_weight.size(0) != n_heads * d_head:
        raise ValueError("up_k_weight output dimension must equal H * D")
    if up_k_weight.size(1) != latent_kv.size(-1):
        raise ValueError("up_k_weight input dimension must match latent_kv width")
    if scale is None:
        scale = d_head**0.5
    if scale <= 0:
        raise ValueError("scale must be positive")

    up_k_by_head = up_k_weight.reshape(n_heads, d_head, latent_kv.size(-1))
    absorbed_q = torch.einsum("bhtd,hdl->bhtl", q, up_k_by_head)
    return torch.matmul(absorbed_q, latent_kv.transpose(1, 2).unsqueeze(1)) / scale


def count_params(model):
    return sum(p.numel() for p in model.parameters())


def gqa_head_mapping(n_heads, n_kv_heads):
    if n_heads <= 0 or n_kv_heads <= 0:
        raise ValueError("n_heads and n_kv_heads must be positive")
    if n_heads % n_kv_heads != 0:
        raise ValueError("n_heads must be divisible by n_kv_heads")
    n_rep = n_heads // n_kv_heads
    return [query_head // n_rep for query_head in range(n_heads)]


def compute_kv_cache_size(d_model, n_heads, n_kv_heads, d_latent, seq_len):
    d_k = d_model // n_heads
    bytes_per_float = 4
    mha_per_token = 2 * n_heads * d_k
    gqa_per_token = 2 * n_kv_heads * d_k
    mla_per_token = d_latent
    return {
        "mha_per_token": mha_per_token,
        "gqa_per_token": gqa_per_token,
        "mla_per_token": mla_per_token,
        "mha_total_gb": mha_per_token * seq_len * bytes_per_float / (1024**3),
        "gqa_total_gb": gqa_per_token * seq_len * bytes_per_float / (1024**3),
        "mla_total_gb": mla_per_token * seq_len * bytes_per_float / (1024**3),
    }


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
    if d_model <= 0 or n_heads <= 0 or n_kv_heads <= 0 or d_latent <= 0:
        raise ValueError("model dimensions and head counts must be positive")
    if d_model % n_heads != 0:
        raise ValueError("d_model must be divisible by n_heads")
    if n_heads % n_kv_heads != 0:
        raise ValueError("n_heads must be divisible by n_kv_heads")
    if seq_len <= 0 or batch_size <= 0 or n_layers <= 0 or dtype_bytes <= 0:
        raise ValueError("seq_len, batch_size, n_layers, and dtype_bytes must be positive")

    d_k = d_model // n_heads
    per_token_elements = {
        "mha": 2 * n_heads * d_k,
        "gqa": 2 * n_kv_heads * d_k,
        "mla": d_latent,
    }
    total_bytes = {
        name: elements * seq_len * batch_size * n_layers * dtype_bytes
        for name, elements in per_token_elements.items()
    }
    total_gb = {name: bytes_value / (1024**3) for name, bytes_value in total_bytes.items()}
    return {
        "head_dim": d_k,
        "per_token_elements": per_token_elements,
        "total_bytes": total_bytes,
        "total_gb": total_gb,
        "compression_vs_mha": {
            "mha": 1.0,
            "gqa": total_bytes["mha"] / total_bytes["gqa"],
            "mla": total_bytes["mha"] / total_bytes["mla"],
        },
    }
