"""Starter code for Chapter 5 Transformer block assignment."""

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class LayerNormFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x, gamma, beta, eps=1e-6):
        raise NotImplementedError

    @staticmethod
    def backward(ctx, grad_output):
        raise NotImplementedError


class LayerNorm(nn.Module):
    def __init__(self, dim, eps=1e-6):
        super().__init__()
        raise NotImplementedError

    def forward(self, x):
        raise NotImplementedError


class RMSNorm(nn.Module):
    def __init__(self, dim, eps=1e-6):
        super().__init__()
        raise NotImplementedError

    def forward(self, x):
        raise NotImplementedError


class FFN(nn.Module):
    def __init__(self, d_model, d_ff=None):
        super().__init__()
        raise NotImplementedError

    def forward(self, x):
        raise NotImplementedError


class SwiGLU(nn.Module):
    def __init__(self, d_model, d_ff=None):
        super().__init__()
        raise NotImplementedError

    def forward(self, x):
        raise NotImplementedError


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_heads, dropout=0.0):
        super().__init__()
        raise NotImplementedError

    def forward(self, x, mask=None):
        raise NotImplementedError


class TransformerBlock(nn.Module):
    def __init__(self, d_model, n_heads, d_ff=None, dropout=0.0):
        super().__init__()
        raise NotImplementedError

    def forward(self, x, mask=None):
        raise NotImplementedError


def count_params(model):
    raise NotImplementedError


def estimate_block_resources(batch_size, seq_len, d_model, n_heads, d_ff=None, dtype_bytes=2):
    """Estimate parameters, major FLOPs, and activation memory for one Transformer block."""
    raise NotImplementedError
