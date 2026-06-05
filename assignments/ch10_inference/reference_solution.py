"""Reference solution for Chapter 10 inference-engineering assignment."""

from collections import defaultdict

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class AttentionWithCache(nn.Module):
    def __init__(self, d_model, n_heads, dropout=0.0):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_head = d_model // n_heads
        self.q_proj = nn.Linear(d_model, d_model, bias=False)
        self.k_proj = nn.Linear(d_model, d_model, bias=False)
        self.v_proj = nn.Linear(d_model, d_model, bias=False)
        self.o_proj = nn.Linear(d_model, d_model, bias=False)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, cache=None):
        batch, seq_len, _ = x.shape
        q = self.q_proj(x).view(batch, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        k = self.k_proj(x).view(batch, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        v = self.v_proj(x).view(batch, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        if cache is not None:
            k = torch.cat([cache["k"], k], dim=2)
            v = torch.cat([cache["v"], v], dim=2)
        new_cache = {"k": k, "v": v}

        scores = torch.matmul(q, k.transpose(-2, -1)) / (self.d_head**0.5)
        mask = self._causal_mask(k.size(2), q.size(2), x.device)
        scores = scores.masked_fill(~mask.view(1, 1, q.size(2), k.size(2)), torch.finfo(scores.dtype).min)
        weights = F.softmax(scores, dim=-1)
        weights = self.dropout(weights)
        out = torch.matmul(weights, v)
        out = out.transpose(1, 2).contiguous().view(batch, seq_len, self.d_model)
        return self.o_proj(out), new_cache

    def _causal_mask(self, l_kv, l_q, device):
        query_start = l_kv - l_q
        query_positions = torch.arange(query_start, query_start + l_q, device=device).unsqueeze(1)
        key_positions = torch.arange(l_kv, device=device).unsqueeze(0)
        return key_positions <= query_positions


def kv_cache_memory_analysis(n_layers, n_kv_heads, d_head, seq_len, batch_size=1, dtype_bytes=2, model_params_gb=None):
    cache_per_layer_bytes = batch_size * 2 * seq_len * n_kv_heads * d_head * dtype_bytes
    total_cache_bytes = cache_per_layer_bytes * n_layers
    result = {
        "cache_per_layer_mb": cache_per_layer_bytes / (1024**2),
        "total_cache_gb": total_cache_bytes / (1024**3),
        "bytes": total_cache_bytes,
    }
    if model_params_gb is not None:
        result["cache_to_params_ratio"] = result["total_cache_gb"] / model_params_gb
    return result


def quantize_per_channel(tensor):
    if tensor.dim() != 2:
        raise ValueError("tensor must be a 2D weight matrix")
    abs_max = tensor.abs().max(dim=1, keepdim=True).values
    scales = (abs_max / 127.0).clamp(min=1e-8)
    quantized = torch.round(tensor / scales).clamp(-127, 127).to(torch.int8)
    return quantized, scales.squeeze(1)


def dequantize(quantized, scales):
    return quantized.float() * scales.to(quantized.device).unsqueeze(1)


def nrmse(original, reconstructed):
    rmse = torch.sqrt(torch.mean((original - reconstructed) ** 2))
    denom = original.max() - original.min()
    if denom.abs() < 1e-12:
        return 0.0 if rmse.item() == 0.0 else float("inf")
    return (rmse / denom).item()


class SimpleRAG:
    def __init__(self, embed_model, llm, chunk_size=512, overlap=64):
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")
        self.embed_model = embed_model
        self.llm = llm
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.documents = []
        self.embeddings = None

    def add_document(self, text):
        tokens = text.split()
        chunks = []
        start = 0
        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            chunk = " ".join(tokens[start:end])
            if chunk:
                chunks.append(chunk)
            if end == len(tokens):
                break
            start += self.chunk_size - self.overlap
        self.documents.extend(chunks)
        embs = np.asarray([self.embed_model.encode(chunk) for chunk in chunks], dtype=np.float64)
        if self.embeddings is None:
            self.embeddings = embs
        else:
            self.embeddings = np.concatenate([self.embeddings, embs], axis=0)

    def retrieve(self, query, top_k=3):
        if self.embeddings is None or not self.documents:
            return []
        query_emb = np.asarray(self.embed_model.encode(query), dtype=np.float64)
        denom = np.linalg.norm(self.embeddings, axis=1) * max(np.linalg.norm(query_emb), 1e-12)
        scores = (self.embeddings @ query_emb) / np.maximum(denom, 1e-12)
        top_k = min(top_k, len(self.documents))
        top_indices = np.argsort(scores)[-top_k:][::-1]
        return [(self.documents[i], float(scores[i])) for i in top_indices]

    def query(self, question):
        context_chunks = self.retrieve(question, top_k=3)
        context = "\n\n".join(f"[文档 {i + 1}]: {chunk}" for i, (chunk, _score) in enumerate(context_chunks))
        prompt = f"基于以下文档内容回答问题。\n\n文档内容：\n{context}\n\n问题：{question}\n回答："
        return self.llm.generate(prompt)


def summarize_benchmark(latencies, generated_tokens, memory_gb):
    if not latencies:
        raise ValueError("latencies must not be empty")
    if generated_tokens <= 0:
        raise ValueError("generated_tokens must be positive")
    ttft_ms = float(latencies[0])
    decode_latencies = latencies[1:] if len(latencies) > 1 else latencies
    tpot_ms = float(sum(decode_latencies) / len(decode_latencies))
    total_seconds = sum(latencies) / 1000.0
    return {
        "ttft_ms": ttft_ms,
        "ms_per_token": tpot_ms,
        "tokens_per_second": generated_tokens / total_seconds,
        "memory_gb": float(memory_gb),
        "p95_ms": float(np.percentile(np.asarray(latencies, dtype=np.float64), 95)),
    }


class LSHMemory:
    def __init__(self, dim, n_bits=8, seed=0):
        generator = torch.Generator().manual_seed(seed)
        self.planes = torch.randn(n_bits, dim, generator=generator)
        self.buckets = defaultdict(list)

    def _hash(self, x):
        x = x.detach().float()
        bits = (self.planes.to(x.device) @ x > 0).long()
        weights = 2 ** torch.arange(len(bits), device=x.device)
        return int((bits * weights).sum().item())

    def add(self, vec, value):
        vec = vec.detach().float()
        self.buckets[self._hash(vec)].append((vec, value))

    def query(self, vec):
        vec = vec.detach().float()
        candidates = self.buckets.get(self._hash(vec), [])
        if not candidates:
            return None
        sims = [torch.dot(vec, stored) / (vec.norm() * stored.norm() + 1e-9) for stored, _value in candidates]
        return candidates[int(torch.stack(sims).argmax().item())][1]
