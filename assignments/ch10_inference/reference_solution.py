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


def contrastive_inbatch_loss(query_embeddings, doc_embeddings, temperature=1.0):
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    if query_embeddings.dim() != 2 or doc_embeddings.dim() != 2:
        raise ValueError("embeddings must be 2D tensors")
    if query_embeddings.shape != doc_embeddings.shape:
        raise ValueError("query and document embeddings must have the same shape")
    if query_embeddings.size(0) == 0:
        raise ValueError("batch size must be positive")

    query_norm = F.normalize(query_embeddings.float(), p=2, dim=1)
    doc_norm = F.normalize(doc_embeddings.float(), p=2, dim=1)
    logits = query_norm @ doc_norm.t() / float(temperature)
    labels = torch.arange(logits.size(0), device=logits.device)
    loss = F.cross_entropy(logits, labels)
    accuracy = (logits.argmax(dim=1) == labels).float().mean().item()
    return {"loss": loss, "logits": logits, "accuracy": accuracy}


def pairwise_reranker_loss(chosen_scores, rejected_scores, margin=0.0):
    if margin < 0:
        raise ValueError("margin must be non-negative")
    if chosen_scores.shape != rejected_scores.shape:
        raise ValueError("chosen and rejected scores must have the same shape")
    if chosen_scores.numel() == 0:
        raise ValueError("score tensors must not be empty")

    chosen = chosen_scores.float()
    rejected = rejected_scores.float()
    score_margins = chosen - rejected
    logits = score_margins - float(margin)
    loss = F.softplus(-logits).mean()
    accuracy = (score_margins > 0).float().mean().item()
    return {"loss": loss, "margins": score_margins, "accuracy": accuracy}


def recall_at_k(retrieved_ids, relevant_ids, k):
    if k <= 0:
        raise ValueError("k must be positive")
    relevant = set(relevant_ids)
    if not relevant:
        raise ValueError("relevant_ids must not be empty")
    retrieved_top_k = set(retrieved_ids[:k])
    return len(retrieved_top_k & relevant) / len(relevant)


def reciprocal_rank_at_k(retrieved_ids, relevant_ids, k):
    if k <= 0:
        raise ValueError("k must be positive")
    relevant = set(relevant_ids)
    if not relevant:
        raise ValueError("relevant_ids must not be empty")
    for rank, doc_id in enumerate(retrieved_ids[:k], start=1):
        if doc_id in relevant:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(retrieved_ids, relevance_scores, k):
    if k <= 0:
        raise ValueError("k must be positive")
    if not relevance_scores:
        raise ValueError("relevance_scores must not be empty")

    labels = {doc_id: float(score) for doc_id, score in relevance_scores.items()}
    if any(score < 0 for score in labels.values()):
        raise ValueError("relevance scores must be non-negative")

    def gain(score):
        return (2.0**score - 1.0)

    dcg = 0.0
    for rank, doc_id in enumerate(retrieved_ids[:k], start=1):
        score = labels.get(doc_id, 0.0)
        dcg += gain(score) / np.log2(rank + 1)

    ideal_scores = sorted(labels.values(), reverse=True)[:k]
    ideal_dcg = sum(gain(score) / np.log2(rank + 1) for rank, score in enumerate(ideal_scores, start=1))
    if ideal_dcg == 0.0:
        return 0.0
    return dcg / ideal_dcg


def reciprocal_rank_fusion(rankings, k=60):
    if k <= 0:
        raise ValueError("k must be positive")
    if not rankings:
        raise ValueError("rankings must not be empty")

    scores = defaultdict(float)
    first_seen = {}
    order = 0
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            if doc_id not in first_seen:
                first_seen[doc_id] = order
                order += 1
            scores[doc_id] += 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda item: (-item[1], first_seen[item[0]]))


def rerank_documents(query, candidates, scorer, top_k=None):
    if not candidates:
        return []
    if top_k is not None and top_k <= 0:
        raise ValueError("top_k must be positive")

    reranked = []
    for position, candidate in enumerate(candidates):
        if len(candidate) != 2:
            raise ValueError("candidates must contain (doc_id, text) pairs")
        doc_id, text = candidate
        score = float(scorer(query, text))
        reranked.append({"doc_id": doc_id, "text": text, "score": score, "original_rank": position + 1})
    reranked.sort(key=lambda item: (-item["score"], item["original_rank"]))
    return reranked[:top_k] if top_k is not None else reranked


def maximal_marginal_relevance(query_embedding, doc_embeddings, doc_ids=None, top_k=3, lambda_mult=0.5):
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    if not 0.0 <= lambda_mult <= 1.0:
        raise ValueError("lambda_mult must be in [0, 1]")
    if query_embedding.dim() != 1:
        raise ValueError("query_embedding must be a 1D tensor")
    if doc_embeddings.dim() != 2:
        raise ValueError("doc_embeddings must be a 2D tensor")
    if doc_embeddings.size(0) == 0:
        raise ValueError("doc_embeddings must contain at least one document")
    if doc_embeddings.size(1) != query_embedding.numel():
        raise ValueError("document embedding width must match query embedding length")
    if doc_ids is not None and len(doc_ids) != doc_embeddings.size(0):
        raise ValueError("doc_ids length must match number of documents")

    ids = list(range(doc_embeddings.size(0))) if doc_ids is None else list(doc_ids)
    query = F.normalize(query_embedding.float().unsqueeze(0), p=2, dim=1).squeeze(0)
    docs = F.normalize(doc_embeddings.float(), p=2, dim=1)
    query_sims = docs @ query
    doc_sims = docs @ docs.t()

    selected = []
    selected_indices = []
    remaining = list(range(doc_embeddings.size(0)))
    top_k = min(top_k, len(remaining))

    while remaining and len(selected) < top_k:
        best = None
        for idx in remaining:
            redundancy = 0.0
            if selected_indices:
                redundancy = float(doc_sims[idx, selected_indices].max().item())
            score = lambda_mult * float(query_sims[idx].item()) - (1.0 - lambda_mult) * redundancy
            candidate = (score, -idx, idx, redundancy)
            if best is None or candidate > best:
                best = candidate
        score, _neg_idx, idx, redundancy = best
        selected.append(
            {
                "doc_id": ids[idx],
                "index": idx,
                "score": score,
                "query_similarity": float(query_sims[idx].item()),
                "diversity_penalty": redundancy,
            }
        )
        selected_indices.append(idx)
        remaining.remove(idx)
    return selected


def build_rag_context(retrieved_chunks, max_context_tokens, reserved_output_tokens=0, token_counter=None):
    if max_context_tokens <= 0:
        raise ValueError("max_context_tokens must be positive")
    if reserved_output_tokens < 0:
        raise ValueError("reserved_output_tokens must be non-negative")
    context_budget = max_context_tokens - reserved_output_tokens
    if context_budget <= 0:
        raise ValueError("reserved_output_tokens must be smaller than max_context_tokens")
    if token_counter is None:
        token_counter = lambda text: len(str(text).split())

    selected = []
    used_tokens = 0
    skipped = 0
    for chunk in retrieved_chunks:
        if not isinstance(chunk, dict):
            raise ValueError("retrieved_chunks must contain dictionaries")
        if "doc_id" not in chunk or "text" not in chunk:
            raise ValueError("each chunk must contain doc_id and text")
        text = str(chunk["text"]).strip()
        if not text:
            skipped += 1
            continue
        block = f"[{chunk['doc_id']}] {text}"
        cost = int(token_counter(block))
        if cost <= 0:
            raise ValueError("token_counter must return a positive integer for non-empty chunks")
        if used_tokens + cost > context_budget:
            skipped += 1
            continue
        selected.append(
            {
                "doc_id": chunk["doc_id"],
                "text": text,
                "score": chunk.get("score"),
                "tokens": cost,
            }
        )
        used_tokens += cost

    context = "\n\n".join(f"[{item['doc_id']}] {item['text']}" for item in selected)
    return {
        "context": context,
        "selected": selected,
        "citations": [item["doc_id"] for item in selected],
        "used_tokens": used_tokens,
        "context_budget": context_budget,
        "skipped": skipped,
    }


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


def build_metric_card(task, metrics, baseline, sample_size, risks=None, uncertainty=None, conclusion=None):
    if not isinstance(task, str) or not task.strip():
        raise ValueError("task must be a non-empty string")
    if not isinstance(metrics, dict) or not metrics:
        raise ValueError("metrics must be a non-empty dict")
    if not isinstance(baseline, str) or not baseline.strip():
        raise ValueError("baseline must be a non-empty string")
    if sample_size <= 0:
        raise ValueError("sample_size must be positive")

    normalized_metrics = {}
    for name, value in metrics.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("metric names must be non-empty strings")
        if isinstance(value, (int, float)):
            normalized_metrics[name] = float(value)
        else:
            normalized_metrics[name] = value

    risk_items = list(risks or [])
    return {
        "task": task.strip(),
        "sample_size": int(sample_size),
        "baseline": baseline.strip(),
        "metrics": normalized_metrics,
        "risks": risk_items,
        "uncertainty": uncertainty or "single_run_limit",
        "conclusion": conclusion or "metric_card_describes_results_but_does_not_prove_general_capability",
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
