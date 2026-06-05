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
