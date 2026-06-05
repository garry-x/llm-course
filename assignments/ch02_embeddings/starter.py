"""Starter code for Chapter 2 embedding and position encoding assignment."""

import torch
import torch.nn as nn


class TokenEmbedding(nn.Module):
    """Map token ids to dense vectors."""

    def __init__(self, vocab_size, d_model):
        super().__init__()
        raise NotImplementedError

    def forward(self, x):
        raise NotImplementedError


def build_cooccurrence_matrix(token_ids, vocab_size, window_size):
    """Count directed center->context co-occurrences inside a fixed window."""
    raise NotImplementedError


def skipgram_negative_sampling_loss(center_vectors, positive_vectors, negative_vectors):
    """Return mean SGNS loss for center, positive context, and negative vectors."""
    raise NotImplementedError


class SinusoidalEncoding(nn.Module):
    """Fixed sinusoidal positional encoding."""

    def __init__(self, d_model, max_len=8192):
        super().__init__()
        raise NotImplementedError

    def forward(self, x):
        raise NotImplementedError


class RoPE(nn.Module):
    """Rotary Position Embedding."""

    def __init__(self, d_model, max_len=8192, base=10000.0):
        super().__init__()
        raise NotImplementedError

    def _rotate_half(self, x):
        raise NotImplementedError

    def _apply_rotary(self, x, cos, sin):
        raise NotImplementedError

    def forward(self, q, k, pos_ids=None):
        raise NotImplementedError


def verify_rope_relative_property(d_model=64, seq_len=8):
    """Return a score matrix whose diagonals should be constant."""
    raise NotImplementedError
