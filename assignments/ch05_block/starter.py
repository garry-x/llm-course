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


def swiglu_hidden_size_for_param_budget(d_model, gelu_multiplier=4):
    """Return the SwiGLU hidden width that matches a GELU FFN parameter budget."""
    raise NotImplementedError


def ffn_parameter_counts(d_model, gelu_hidden=None, swiglu_hidden=None):
    """Compare bias-free GELU FFN and SwiGLU parameter counts."""
    raise NotImplementedError


def residual_gradient_path_factors(sublayer_slopes, norm_slopes, mode="pre"):
    """Return per-layer and total gradient factors in a scalar residual block model."""
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


def activation_checkpointing_tradeoff(activation_bytes, forward_flops, checkpointed_fraction=1.0):
    """Estimate activation memory saved and extra recompute FLOPs from checkpointing."""
    raise NotImplementedError
