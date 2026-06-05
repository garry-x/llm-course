"""Reference solution for Chapter 5 Transformer block assignment."""

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class LayerNormFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x, gamma, beta, eps=1e-6):
        mean = x.mean(dim=-1, keepdim=True)
        var = x.var(dim=-1, keepdim=True, unbiased=False)
        inv_std = torch.rsqrt(var + eps)
        x_hat = (x - mean) * inv_std
        ctx.save_for_backward(x_hat, inv_std, gamma)
        return x_hat * gamma + beta

    @staticmethod
    def backward(ctx, grad_output):
        x_hat, inv_std, gamma = ctx.saved_tensors
        n = x_hat.shape[-1]
        grad_x_hat = grad_output * gamma
        grad_x = (
            inv_std
            / n
            * (
                n * grad_x_hat
                - grad_x_hat.sum(dim=-1, keepdim=True)
                - x_hat * (grad_x_hat * x_hat).sum(dim=-1, keepdim=True)
            )
        )
        reduce_dims = tuple(range(grad_output.dim() - 1))
        grad_gamma = (grad_output * x_hat).sum(dim=reduce_dims)
        grad_beta = grad_output.sum(dim=reduce_dims)
        return grad_x, grad_gamma, grad_beta, None


class LayerNorm(nn.Module):
    def __init__(self, dim, eps=1e-6):
        super().__init__()
        self.eps = eps
        self.gamma = nn.Parameter(torch.ones(dim))
        self.beta = nn.Parameter(torch.zeros(dim))

    def forward(self, x):
        return LayerNormFunction.apply(x, self.gamma, self.beta, self.eps)


class RMSNorm(nn.Module):
    def __init__(self, dim, eps=1e-6):
        super().__init__()
        self.eps = eps
        self.gamma = nn.Parameter(torch.ones(dim))

    def forward(self, x):
        rms = torch.sqrt(x.pow(2).mean(dim=-1, keepdim=True) + self.eps)
        return x / rms * self.gamma


class FFN(nn.Module):
    def __init__(self, d_model, d_ff=None):
        super().__init__()
        d_ff = d_ff or d_model * 4
        self.fc1 = nn.Linear(d_model, d_ff, bias=True)
        self.fc2 = nn.Linear(d_ff, d_model, bias=True)

    def forward(self, x):
        return self.fc2(F.gelu(self.fc1(x)))


class SwiGLU(nn.Module):
    def __init__(self, d_model, d_ff=None):
        super().__init__()
        d_ff = d_ff or int(d_model * 8 / 3)
        self.w1 = nn.Linear(d_model, d_ff, bias=False)
        self.w2 = nn.Linear(d_model, d_ff, bias=False)
        self.w3 = nn.Linear(d_ff, d_model, bias=False)

    def forward(self, x):
        gate = F.silu(self.w1(x))
        value = self.w2(x)
        return self.w3(gate * value)


def swiglu_hidden_size_for_param_budget(d_model, gelu_multiplier=4):
    """Return the SwiGLU hidden width that matches a GELU FFN parameter budget."""
    if d_model <= 0 or gelu_multiplier <= 0:
        raise ValueError("d_model and gelu_multiplier must be positive")
    return int(2 * gelu_multiplier * d_model / 3)


def ffn_parameter_counts(d_model, gelu_hidden=None, swiglu_hidden=None):
    """Compare bias-free GELU FFN and SwiGLU parameter counts.

    A GELU FFN has two matrices, d_model -> gelu_hidden -> d_model.
    SwiGLU has three matrices: gate, value, and output projection.
    """
    if d_model <= 0:
        raise ValueError("d_model must be positive")

    if gelu_hidden is None:
        gelu_hidden = 4 * d_model
    if swiglu_hidden is None:
        swiglu_hidden = swiglu_hidden_size_for_param_budget(d_model)
    if gelu_hidden <= 0 or swiglu_hidden <= 0:
        raise ValueError("gelu_hidden and swiglu_hidden must be positive")

    gelu_params = 2 * d_model * gelu_hidden
    swiglu_params = 3 * d_model * swiglu_hidden
    return {
        "gelu_hidden": gelu_hidden,
        "swiglu_hidden": swiglu_hidden,
        "gelu_params": gelu_params,
        "swiglu_params": swiglu_params,
        "ratio": swiglu_params / gelu_params,
    }


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_heads, dropout=0.0):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_head = d_model // n_heads
        self.W_qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.W_o = nn.Linear(d_model, d_model, bias=False)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        batch_size, seq_len, _ = x.shape
        qkv = self.W_qkv(x)
        qkv = qkv.view(batch_size, seq_len, 3, self.n_heads, self.d_head)
        qkv = qkv.permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]

        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.d_head)
        if mask is not None:
            if mask.dtype != torch.bool:
                mask = mask != 0
            while mask.dim() < scores.dim():
                mask = mask.unsqueeze(0)
            scores = scores.masked_fill(~mask, torch.finfo(scores.dtype).min)

        weights = F.softmax(scores, dim=-1)
        weights = self.dropout(weights)
        out = torch.matmul(weights, v)
        out = out.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
        return self.W_o(out), weights


class TransformerBlock(nn.Module):
    def __init__(self, d_model, n_heads, d_ff=None, dropout=0.0):
        super().__init__()
        self.attention = MultiHeadAttention(d_model=d_model, n_heads=n_heads, dropout=dropout)
        self.norm1 = RMSNorm(d_model)
        self.ffn = SwiGLU(d_model, d_ff)
        self.norm2 = RMSNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        identity = x
        x = self.norm1(x)
        x, _ = self.attention(x, mask=mask)
        x = self.dropout(x)
        x = x + identity

        identity = x
        x = self.norm2(x)
        x = self.ffn(x)
        x = self.dropout(x)
        x = x + identity
        return x


def count_params(model):
    return sum(p.numel() for p in model.parameters())


def estimate_block_resources(batch_size, seq_len, d_model, n_heads, d_ff=None, dtype_bytes=2):
    if batch_size <= 0 or seq_len <= 0 or d_model <= 0 or n_heads <= 0 or dtype_bytes <= 0:
        raise ValueError("batch_size, seq_len, d_model, n_heads, and dtype_bytes must be positive")
    if d_model % n_heads != 0:
        raise ValueError("d_model must be divisible by n_heads")
    d_ff = d_ff or int(d_model * 8 / 3)
    if d_ff <= 0:
        raise ValueError("d_ff must be positive")

    d_head = d_model // n_heads
    attention_params = 4 * d_model * d_model
    swiglu_params = 3 * d_model * d_ff
    norm_params = 2 * d_model
    total_params = attention_params + swiglu_params + norm_params

    tokens = batch_size * seq_len
    qkv_flops = 2 * tokens * d_model * (3 * d_model)
    attention_score_flops = 2 * batch_size * n_heads * seq_len * seq_len * d_head
    attention_value_flops = 2 * batch_size * n_heads * seq_len * seq_len * d_head
    output_proj_flops = 2 * tokens * d_model * d_model
    swiglu_flops = 2 * tokens * d_model * d_ff * 3
    total_flops = qkv_flops + attention_score_flops + attention_value_flops + output_proj_flops + swiglu_flops

    hidden_activation_bytes = tokens * d_model * dtype_bytes
    qkv_activation_bytes = tokens * 3 * d_model * dtype_bytes
    ffn_activation_bytes = tokens * 2 * d_ff * dtype_bytes
    attention_scores_bytes = batch_size * n_heads * seq_len * seq_len * dtype_bytes
    residual_stream_bytes = 2 * hidden_activation_bytes
    activation_bytes = qkv_activation_bytes + ffn_activation_bytes + attention_scores_bytes + residual_stream_bytes

    return {
        "d_head": d_head,
        "attention_params": attention_params,
        "swiglu_params": swiglu_params,
        "norm_params": norm_params,
        "total_params": total_params,
        "qkv_flops": qkv_flops,
        "attention_score_flops": attention_score_flops,
        "attention_value_flops": attention_value_flops,
        "output_proj_flops": output_proj_flops,
        "swiglu_flops": swiglu_flops,
        "total_flops": total_flops,
        "attention_scores_bytes": attention_scores_bytes,
        "activation_bytes": activation_bytes,
        "activation_mb": activation_bytes / (1024**2),
    }
