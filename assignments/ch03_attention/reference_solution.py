"""Reference solution for Chapter 3 attention assignment."""

import math

import torch
import torch.nn as nn


class QKVProjection(nn.Module):
    """Project input X into Query, Key and Value tensors."""

    def __init__(self, d_model, d_k):
        super().__init__()
        self.W_q = nn.Linear(d_model, d_k, bias=False)
        self.W_k = nn.Linear(d_model, d_k, bias=False)
        self.W_v = nn.Linear(d_model, d_k, bias=False)
        self.d_k = d_k

    def forward(self, x):
        return self.W_q(x), self.W_k(x), self.W_v(x)


def scaled_dot_product_attention(Q, K, V, mask=None):
    """Return (output, attention_weights)."""
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    if mask is not None:
        if mask.dim() == 2:
            mask = mask.unsqueeze(0)
        scores = scores.masked_fill(mask == 0, -1e9)
    attn_weights = torch.softmax(scores, dim=-1)
    output = torch.matmul(attn_weights, V)
    return output, attn_weights


def create_causal_mask(seq_len):
    """Return a boolean lower-triangular causal mask."""
    return torch.ones(seq_len, seq_len).tril().bool()


def causal_attention(Q, K, V):
    """Scaled dot-product attention with a causal mask."""
    mask = create_causal_mask(Q.size(1)).to(Q.device)
    return scaled_dot_product_attention(Q, K, V, mask=mask)


def plot_attention(attn_weights, tokens, title="Attention Weights"):
    """Return a matplotlib (fig, ax) heatmap for attention weights."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 6))
    image = ax.imshow(attn_weights.detach().cpu().numpy(), vmin=0, vmax=1, cmap="YlOrRd")
    ax.set_xticks(range(len(tokens)))
    ax.set_yticks(range(len(tokens)))
    ax.set_xticklabels(tokens)
    ax.set_yticklabels(tokens)
    ax.set_xlabel("Key Position")
    ax.set_ylabel("Query Position")
    ax.set_title(title)
    fig.colorbar(image, ax=ax)
    fig.tight_layout()
    return fig, ax
