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


def self_attention_permutation_error(x, permutation):
    if x.dim() == 2:
        x_batch = x.unsqueeze(0)
        squeeze = True
    elif x.dim() == 3:
        x_batch = x
        squeeze = False
    else:
        raise ValueError("x must have shape [T, D] or [B, T, D]")

    perm = torch.as_tensor(permutation, device=x_batch.device, dtype=torch.long)
    seq_len = x_batch.size(1)
    if perm.dim() != 1 or perm.numel() != seq_len:
        raise ValueError("permutation must have shape [T]")
    if sorted(perm.detach().cpu().tolist()) != list(range(seq_len)):
        raise ValueError("permutation must contain each position exactly once")

    output, _ = scaled_dot_product_attention(x_batch, x_batch, x_batch)
    permuted_x = x_batch[:, perm, :]
    permuted_output, _ = scaled_dot_product_attention(permuted_x, permuted_x, permuted_x)
    expected = output[:, perm, :]
    error = (permuted_output - expected).abs().max()
    return float(error.item()) if squeeze else error.item()


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


def attention_qkv_gradients(Q, K, V, grad_output, mask=None):
    """Return manual (dQ, dK, dV) for scaled dot-product attention."""
    if Q.shape != K.shape or Q.shape != V.shape or Q.shape != grad_output.shape:
        raise ValueError("Q, K, V, and grad_output must have the same shape")
    if Q.dim() == 2:
        Q_batch = Q.unsqueeze(0)
        K_batch = K.unsqueeze(0)
        V_batch = V.unsqueeze(0)
        grad_batch = grad_output.unsqueeze(0)
        squeeze = True
    elif Q.dim() == 3:
        Q_batch, K_batch, V_batch, grad_batch = Q, K, V, grad_output
        squeeze = False
    else:
        raise ValueError("Q, K, V, and grad_output must have shape [T, D] or [B, T, D]")

    batch_size, seq_len, d_k = Q_batch.shape
    scale = math.sqrt(d_k)
    scores = torch.matmul(Q_batch, K_batch.transpose(-2, -1)) / scale

    expanded_mask = None
    if mask is not None:
        if mask.dim() == 2:
            if tuple(mask.shape) != (seq_len, seq_len):
                raise ValueError("2D mask must have shape [T, T]")
            expanded_mask = mask.to(device=Q_batch.device, dtype=torch.bool).unsqueeze(0)
        elif mask.dim() == 3:
            if tuple(mask.shape) != (batch_size, seq_len, seq_len):
                raise ValueError("3D mask must have shape [B, T, T]")
            expanded_mask = mask.to(device=Q_batch.device, dtype=torch.bool)
        else:
            raise ValueError("mask must have shape [T, T] or [B, T, T]")
        scores = scores.masked_fill(~expanded_mask, -1e9)

    attn = torch.softmax(scores, dim=-1)
    grad_v = torch.matmul(attn.transpose(-2, -1), grad_batch)
    grad_attn = torch.matmul(grad_batch, V_batch.transpose(-2, -1))
    row_mean = torch.sum(attn * grad_attn, dim=-1, keepdim=True)
    grad_scores = attn * (grad_attn - row_mean)
    if expanded_mask is not None:
        grad_scores = grad_scores.masked_fill(~expanded_mask, 0.0)

    grad_q = torch.matmul(grad_scores, K_batch) / scale
    grad_k = torch.matmul(grad_scores.transpose(-2, -1), Q_batch) / scale

    if squeeze:
        return grad_q.squeeze(0), grad_k.squeeze(0), grad_v.squeeze(0)
    return grad_q, grad_k, grad_v


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


def combine_causal_padding_mask(padding_mask):
    """Return a [B, T, T] mask that blocks future positions and padded keys."""
    if padding_mask.dim() != 2:
        raise ValueError("padding_mask must have shape [B, T]")
    if padding_mask.size(1) == 0:
        raise ValueError("sequence length must be positive")
    valid_keys = padding_mask.to(dtype=torch.bool)
    if not torch.all(valid_keys.any(dim=1)):
        raise ValueError("each sequence must contain at least one valid token")

    seq_len = valid_keys.size(1)
    causal = create_causal_mask(seq_len).to(valid_keys.device)
    return causal.unsqueeze(0) & valid_keys.unsqueeze(1)


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
