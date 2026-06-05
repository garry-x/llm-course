"""Reference solution for Chapter 2 embedding and position encoding assignment."""

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class TokenEmbedding(nn.Module):
    """Map token ids to dense vectors."""

    def __init__(self, vocab_size, d_model):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)
        self.d_model = d_model

    def forward(self, x):
        return self.embed(x) * math.sqrt(self.d_model)


def build_cooccurrence_matrix(token_ids, vocab_size, window_size):
    if vocab_size <= 0:
        raise ValueError("vocab_size must be positive")
    if window_size <= 0:
        raise ValueError("window_size must be positive")
    ids = [int(token_id) for token_id in token_ids]
    counts = torch.zeros(vocab_size, vocab_size, dtype=torch.long)
    for center_pos, center_id in enumerate(ids):
        if center_id < 0 or center_id >= vocab_size:
            raise ValueError("token id out of vocabulary range")
        left = max(0, center_pos - window_size)
        right = min(len(ids), center_pos + window_size + 1)
        for context_pos in range(left, right):
            if context_pos == center_pos:
                continue
            context_id = ids[context_pos]
            if context_id < 0 or context_id >= vocab_size:
                raise ValueError("token id out of vocabulary range")
            counts[center_id, context_id] += 1
    return counts


def skipgram_negative_sampling_loss(center_vectors, positive_vectors, negative_vectors):
    if center_vectors.dim() != 2 or positive_vectors.dim() != 2:
        raise ValueError("center_vectors and positive_vectors must have shape [B, D]")
    if negative_vectors.dim() != 3:
        raise ValueError("negative_vectors must have shape [B, K, D]")
    if center_vectors.shape != positive_vectors.shape:
        raise ValueError("center_vectors and positive_vectors must have the same shape")
    if negative_vectors.size(0) != center_vectors.size(0) or negative_vectors.size(2) != center_vectors.size(1):
        raise ValueError("negative_vectors must align with batch size and embedding dimension")

    positive_logits = torch.sum(center_vectors * positive_vectors, dim=-1)
    negative_logits = torch.sum(negative_vectors * center_vectors.unsqueeze(1), dim=-1)
    positive_loss = -F.logsigmoid(positive_logits)
    negative_loss = -F.logsigmoid(-negative_logits).sum(dim=-1)
    return (positive_loss + negative_loss).mean()


def glove_weighted_loss(word_vectors, context_vectors, word_biases, context_biases, cooccurrence, x_max=100.0, alpha=0.75):
    if word_vectors.dim() != 2 or context_vectors.dim() != 2:
        raise ValueError("word_vectors and context_vectors must have shape [V, D]")
    if word_vectors.shape != context_vectors.shape:
        raise ValueError("word_vectors and context_vectors must have the same shape")
    vocab_size = word_vectors.size(0)
    if word_biases.shape != (vocab_size,) or context_biases.shape != (vocab_size,):
        raise ValueError("bias vectors must have shape [V]")
    if cooccurrence.shape != (vocab_size, vocab_size):
        raise ValueError("cooccurrence must have shape [V, V]")
    if x_max <= 0 or alpha <= 0:
        raise ValueError("x_max and alpha must be positive")

    counts = cooccurrence.to(word_vectors.device, dtype=word_vectors.dtype)
    nonzero = counts > 0
    if not torch.any(nonzero):
        raise ValueError("cooccurrence must contain at least one positive count")

    word_indices, context_indices = torch.nonzero(nonzero, as_tuple=True)
    x_ij = counts[word_indices, context_indices]
    weights = torch.clamp((x_ij / float(x_max)).pow(alpha), max=1.0)
    dot = torch.sum(word_vectors[word_indices] * context_vectors[context_indices], dim=-1)
    residual = dot + word_biases[word_indices] + context_biases[context_indices] - x_ij.log()
    return (weights * residual.pow(2)).mean()


def cosine_similarity_matrix(vectors):
    if vectors.dim() != 2:
        raise ValueError("vectors must have shape [V, D]")
    normalized = F.normalize(vectors.float(), p=2, dim=-1, eps=1e-12)
    return normalized @ normalized.T


def analogy_3cosadd(embeddings, word_to_idx, a, b, c, top_k=1):
    if embeddings.dim() != 2:
        raise ValueError("embeddings must have shape [V, D]")
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    for word in (a, b, c):
        if word not in word_to_idx:
            raise KeyError(word)

    idx_to_word = {idx: word for word, idx in word_to_idx.items()}
    query = embeddings[word_to_idx[b]] - embeddings[word_to_idx[a]] + embeddings[word_to_idx[c]]
    normalized_embeddings = F.normalize(embeddings.float(), p=2, dim=-1, eps=1e-12)
    normalized_query = F.normalize(query.float(), p=2, dim=0, eps=1e-12)
    scores = normalized_embeddings @ normalized_query
    for word in (a, b, c):
        scores[word_to_idx[word]] = -float("inf")

    k = min(top_k, embeddings.size(0) - len({a, b, c}))
    values, indices = torch.topk(scores, k=k)
    return [(idx_to_word[int(idx)], float(score)) for score, idx in zip(values, indices)]


class SinusoidalEncoding(nn.Module):
    """Fixed sinusoidal positional encoding."""

    def __init__(self, d_model, max_len=8192):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        pos = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        i = torch.arange(0, d_model, 2).float()
        div_term = torch.exp(i * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(pos * div_term)
        pe[:, 1::2] = torch.cos(pos * div_term)
        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x):
        return x + self.pe[:, : x.size(1), :]


class RoPE(nn.Module):
    """Rotary Position Embedding."""

    def __init__(self, d_model, max_len=8192, base=10000.0):
        super().__init__()
        if d_model % 2 != 0:
            raise ValueError("d_model must be even")
        theta = torch.pow(base, -torch.arange(0, d_model, 2).float() / d_model)
        pos = torch.arange(max_len).float().unsqueeze(1)
        angles = pos * theta.unsqueeze(0)
        self.register_buffer("cos", torch.cos(angles).unsqueeze(0).unsqueeze(0))
        self.register_buffer("sin", torch.sin(angles).unsqueeze(0).unsqueeze(0))

    def _rotate_half(self, x):
        x1, x2 = x.chunk(2, dim=-1)
        return torch.cat((-x2, x1), dim=-1)

    def _apply_rotary(self, x, cos, sin):
        x1, x2 = x.chunk(2, dim=-1)
        return torch.cat((x1 * cos - x2 * sin, x1 * sin + x2 * cos), dim=-1)

    def forward(self, q, k, pos_ids=None):
        _, _, seq_len, d_head = q.shape
        if d_head % 2 != 0:
            raise ValueError("last dimension must be even")

        if pos_ids is None:
            cos = self.cos[:, :, :seq_len, : d_head // 2]
            sin = self.sin[:, :, :seq_len, : d_head // 2]
        else:
            cos = self.cos[:, :, pos_ids, : d_head // 2]
            sin = self.sin[:, :, pos_ids, : d_head // 2]
        return self._apply_rotary(q, cos, sin), self._apply_rotary(k, cos, sin)


def verify_rope_relative_property(d_model=64, seq_len=8):
    """Return a score matrix whose diagonals are constant up to numerical error."""
    torch.manual_seed(0)
    rope = RoPE(d_model=d_model, max_len=seq_len)
    q = torch.randn(1, 1, 1, d_model)
    k = torch.randn(1, 1, 1, d_model)
    q_expanded = q.expand(1, 1, seq_len, -1)
    k_expanded = k.expand(1, 1, seq_len, -1)
    q_rot, k_rot = rope(q_expanded, k_expanded)
    return torch.matmul(q_rot, k_rot.transpose(-2, -1)).squeeze(0).squeeze(0)
