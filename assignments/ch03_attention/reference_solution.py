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


def softmax_jacobian(logits):
    if logits.dim() != 1:
        raise ValueError("logits must be a 1D tensor")
    probs = torch.softmax(logits, dim=-1)
    return torch.diag(probs) - torch.outer(probs, probs)


def attention_logits_gradient(attn_weights, values, grad_output):
    if attn_weights.dim() != 1:
        raise ValueError("attn_weights must have shape [T]")
    if values.dim() != 2:
        raise ValueError("values must have shape [T, D]")
    if grad_output.dim() != 1:
        raise ValueError("grad_output must have shape [D]")
    if values.size(0) != attn_weights.size(0) or values.size(1) != grad_output.size(0):
        raise ValueError("values must align with attention length and output dimension")

    grad_attn = values @ grad_output
    expected_grad = torch.sum(attn_weights * grad_attn)
    return attn_weights * (grad_attn - expected_grad)


def attention_entropy(attn_weights, eps=1e-12):
    if attn_weights.dim() < 1:
        raise ValueError("attn_weights must have at least one dimension")
    probs = attn_weights.clamp_min(eps)
    return -(attn_weights * probs.log()).sum(dim=-1)


def attention_score_memory_bytes(batch_size, n_heads, seq_len, dtype_bytes=2):
    values = [batch_size, n_heads, seq_len, dtype_bytes]
    if any(value <= 0 for value in values):
        raise ValueError("batch_size, n_heads, seq_len, and dtype_bytes must be positive")
    return int(batch_size * n_heads * seq_len * seq_len * dtype_bytes)


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
