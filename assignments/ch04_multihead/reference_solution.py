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
        if self.n_rep > 1:
            k = k.repeat_interleave(self.n_rep, dim=1)
            v = v.repeat_interleave(self.n_rep, dim=1)
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


def count_params(model):
    return sum(p.numel() for p in model.parameters())


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
