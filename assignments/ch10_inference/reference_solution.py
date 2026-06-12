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


def rag_answer_diagnostics(retrieved_ids, relevant_ids, cited_ids, answer_correct, k):
    if k <= 0:
        raise ValueError("k must be positive")
    relevant = set(relevant_ids)
    if not relevant:
        raise ValueError("relevant_ids must not be empty")
    cited = list(cited_ids or [])
    retrieved_top_k = list(retrieved_ids[:k])
    retrieved_relevant = set(retrieved_top_k) & relevant
    cited_set = set(cited)
    cited_relevant = cited_set & relevant

    retrieval_recall = len(retrieved_relevant) / len(relevant)
    retrieval_hit = bool(retrieved_relevant)
    citation_precision = len(cited_relevant) / len(cited_set) if cited_set else 0.0
    citation_recall = len(cited_relevant) / len(relevant)

    if answer_correct:
        failure_mode = "success"
    elif not retrieval_hit:
        failure_mode = "retrieval_miss"
    elif not cited_relevant:
        failure_mode = "context_or_citation_miss"
    else:
        failure_mode = "generation_error"

    return {
        "answer_correct": bool(answer_correct),
        "retrieval_recall_at_k": retrieval_recall,
        "retrieval_mrr_at_k": reciprocal_rank_at_k(retrieved_ids, relevant, k),
        "retrieval_hit": retrieval_hit,
        "citation_precision": citation_precision,
        "citation_recall": citation_recall,
        "cited_relevant_ids": sorted(cited_relevant),
        "missing_relevant_ids": sorted(relevant - set(retrieved_top_k)),
        "failure_mode": failure_mode,
    }


def validate_tool_call_plan(tool_registry, proposed_calls, budgets=None):
    if not proposed_calls:
        raise ValueError("proposed_calls must not be empty")
    budgets = dict(budgets or {})

    if isinstance(tool_registry, dict):
        registry = tool_registry
    else:
        registry = {}
        for spec in tool_registry:
            if not isinstance(spec, dict) or "name" not in spec:
                raise ValueError("each tool spec must contain a name")
            registry[spec["name"]] = spec
    if not registry:
        raise ValueError("tool_registry must not be empty")

    max_calls = int(budgets.get("max_calls", len(proposed_calls)))
    max_consecutive_same_tool = int(budgets.get("max_consecutive_same_tool", len(proposed_calls)))
    allowed_risks = set(budgets.get("allowed_risks", ["read_only"]))
    if max_calls <= 0 or max_consecutive_same_tool <= 0:
        raise ValueError("budget limits must be positive")

    calls = []
    invalid_call_count = 0
    denied_call_count = 0
    action_items = []
    consecutive_tool = None
    consecutive_count = 0
    loop_violation = False

    def validate_value(value, schema, path):
        errors = []
        expected_type = schema.get("type")
        if expected_type == "object":
            if not isinstance(value, dict):
                return [f"{path}: expected object"]
            properties = schema.get("properties", {})
            for field in schema.get("required", []):
                if field not in value:
                    errors.append(f"{path}.{field}: missing required")
            additional = schema.get("additionalProperties", True)
            if additional is False:
                extra = sorted(set(value) - set(properties))
                errors.extend(f"{path}.{field}: unexpected field" for field in extra)
            for field, field_schema in properties.items():
                if field in value:
                    errors.extend(validate_value(value[field], field_schema, f"{path}.{field}"))
            return errors
        if expected_type == "string":
            if not isinstance(value, str):
                return [f"{path}: expected string"]
            if "minLength" in schema and len(value) < int(schema["minLength"]):
                errors.append(f"{path}: shorter than minLength")
            if "maxLength" in schema and len(value) > int(schema["maxLength"]):
                errors.append(f"{path}: longer than maxLength")
            if "enum" in schema and value not in set(schema["enum"]):
                errors.append(f"{path}: not in enum")
            return errors
        if expected_type == "integer":
            if not isinstance(value, int) or isinstance(value, bool):
                return [f"{path}: expected integer"]
            if "minimum" in schema and value < int(schema["minimum"]):
                errors.append(f"{path}: below minimum")
            if "maximum" in schema and value > int(schema["maximum"]):
                errors.append(f"{path}: above maximum")
            if "enum" in schema and value not in set(schema["enum"]):
                errors.append(f"{path}: not in enum")
            return errors
        if expected_type == "number":
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                return [f"{path}: expected number"]
            if "minimum" in schema and float(value) < float(schema["minimum"]):
                errors.append(f"{path}: below minimum")
            if "maximum" in schema and float(value) > float(schema["maximum"]):
                errors.append(f"{path}: above maximum")
            return errors
        if expected_type == "boolean":
            if not isinstance(value, bool):
                return [f"{path}: expected boolean"]
        return errors

    for idx, call in enumerate(proposed_calls):
        if not isinstance(call, dict):
            raise ValueError("each proposed call must be a dict")
        name = call.get("name") or call.get("tool_name")
        arguments = call.get("arguments", call.get("args", {}))
        errors = []
        allowed = True
        risk = None
        if not isinstance(arguments, dict):
            errors.append("arguments: expected object")
        if not name or name not in registry:
            errors.append("tool_name: unknown tool")
            spec = {}
        else:
            spec = registry[name]
            parameters = spec.get("parameters", {})
            if parameters:
                errors.extend(validate_value(arguments, parameters, "arguments"))
            risk = spec.get("risk", "read_only")
            if risk not in allowed_risks:
                allowed = False

        if name == consecutive_tool:
            consecutive_count += 1
        else:
            consecutive_tool = name
            consecutive_count = 1
        if consecutive_count > max_consecutive_same_tool:
            loop_violation = True
            errors.append("loop: repeated same tool beyond budget")

        valid = not errors
        if not valid:
            invalid_call_count += 1
        if not allowed:
            denied_call_count += 1
        calls.append(
            {
                "index": idx,
                "name": name,
                "valid": valid,
                "allowed": allowed,
                "risk": risk,
                "errors": errors,
            }
        )

    if invalid_call_count:
        action_items.append("repair_or_constrain_tool_arguments")
    if denied_call_count:
        action_items.append("request_permission_or_remove_high_risk_tool")
    if len(proposed_calls) > max_calls or loop_violation:
        action_items.append("stop_or_summarize_agent_loop_before_more_tool_calls")

    gates = {
        "schema": {
            "pass": invalid_call_count == 0,
            "signals": {"invalid_call_count": invalid_call_count},
        },
        "permission": {
            "pass": denied_call_count == 0,
            "signals": {"denied_call_count": denied_call_count, "allowed_risks": sorted(allowed_risks)},
        },
        "budget": {
            "pass": len(proposed_calls) <= max_calls and not loop_violation,
            "signals": {
                "call_count": len(proposed_calls),
                "max_calls": max_calls,
                "max_consecutive_same_tool": max_consecutive_same_tool,
                "loop_violation": loop_violation,
            },
        },
    }
    return {
        "overall_pass": not action_items,
        "gates": gates,
        "calls": calls,
        "action_items": action_items,
        "decision": "execute_tool_calls" if not action_items else "reject_or_repair_before_execution",
    }


def prefix_cache_savings(tokenized_prompts):
    if not tokenized_prompts:
        raise ValueError("tokenized_prompts must not be empty")

    cached_prompts = []
    per_request = []
    total_tokens = 0
    saved_tokens = 0

    def normalize(prompt):
        if torch.is_tensor(prompt):
            ids = prompt.detach().cpu().flatten().tolist()
        else:
            ids = list(prompt)
        if not ids:
            raise ValueError("each prompt must contain at least one token")
        return [int(token_id) for token_id in ids]

    def common_prefix_len(left, right):
        limit = min(len(left), len(right))
        idx = 0
        while idx < limit and left[idx] == right[idx]:
            idx += 1
        return idx

    for request_id, prompt in enumerate(tokenized_prompts):
        ids = normalize(prompt)
        best_cached = 0
        best_source = None
        for source_id, cached in cached_prompts:
            prefix_len = common_prefix_len(ids, cached)
            if prefix_len > best_cached:
                best_cached = prefix_len
                best_source = source_id

        prompt_tokens = len(ids)
        new_prefill_tokens = prompt_tokens - best_cached
        total_tokens += prompt_tokens
        saved_tokens += best_cached
        per_request.append(
            {
                "request_id": request_id,
                "prompt_tokens": prompt_tokens,
                "cached_prefix_tokens": best_cached,
                "new_prefill_tokens": new_prefill_tokens,
                "cache_source_request_id": best_source,
            }
        )
        cached_prompts.append((request_id, ids))

    return {
        "requests": per_request,
        "total_prompt_tokens": total_tokens,
        "saved_prefill_tokens": saved_tokens,
        "effective_prefill_tokens": total_tokens - saved_tokens,
        "prefix_cache_hit_rate": saved_tokens / total_tokens,
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


def build_benchmark_summary(task, metrics, baseline, sample_size, risks=None, uncertainty=None, conclusion=None):
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
        "conclusion": conclusion or "summary_describes_results_but_does_not_prove_general_capability",
    }


def prefill_decode_disaggregation_report(requests, slo=None):
    if not requests:
        raise ValueError("requests must not be empty")
    slo = dict(slo or {})
    rows = []
    for idx, req in enumerate(requests):
        if not isinstance(req, dict):
            raise ValueError("each request must be a dict")
        required = ["prefill_ms", "kv_transfer_ms", "decode_queue_ms", "decode_token_ms", "prompt_tokens", "output_tokens", "active_kv_tokens"]
        missing = [name for name in required if name not in req]
        if missing:
            raise ValueError(f"request {idx} missing fields: {', '.join(missing)}")
        decode_token_ms = list(req["decode_token_ms"])
        if not decode_token_ms:
            raise ValueError("decode_token_ms must not be empty")
        numeric = [req["prefill_ms"], req["kv_transfer_ms"], req["decode_queue_ms"], req["prompt_tokens"], req["output_tokens"], req["active_kv_tokens"], *decode_token_ms]
        if any(float(value) < 0 for value in numeric):
            raise ValueError("request metrics must be non-negative")
        if int(req["output_tokens"]) <= 0:
            raise ValueError("output_tokens must be positive")
        first_decode = float(decode_token_ms[0])
        tpot = float(np.mean(np.asarray(decode_token_ms, dtype=np.float64)))
        rows.append(
            {
                "request_id": req.get("request_id", idx),
                "ttft_ms": float(req["prefill_ms"]) + float(req["kv_transfer_ms"]) + float(req["decode_queue_ms"]) + first_decode,
                "prefill_ms": float(req["prefill_ms"]),
                "kv_transfer_ms": float(req["kv_transfer_ms"]),
                "decode_queue_ms": float(req["decode_queue_ms"]),
                "tpot_ms": tpot,
                "prompt_tokens": int(req["prompt_tokens"]),
                "output_tokens": int(req["output_tokens"]),
                "active_kv_tokens": int(req["active_kv_tokens"]),
            }
        )

    def p95(field):
        return float(np.percentile(np.asarray([row[field] for row in rows], dtype=np.float64), 95))

    p95s = {
        "prefill_ms": p95("prefill_ms"),
        "kv_transfer_ms": p95("kv_transfer_ms"),
        "decode_queue_ms": p95("decode_queue_ms"),
        "tpot_ms": p95("tpot_ms"),
        "ttft_ms": p95("ttft_ms"),
    }
    bottleneck = max(["prefill_ms", "kv_transfer_ms", "decode_queue_ms", "tpot_ms"], key=lambda name: p95s[name])
    slo_pass = True
    violations = []
    checks = {
        "max_p95_ttft_ms": ("ttft_ms", "<="),
        "max_p95_tpot_ms": ("tpot_ms", "<="),
        "max_p95_kv_transfer_ms": ("kv_transfer_ms", "<="),
    }
    for key, (field, _op) in checks.items():
        if key in slo and p95s[field] > float(slo[key]):
            slo_pass = False
            violations.append(key)
    if "max_active_kv_tokens" in slo:
        max_active = max(row["active_kv_tokens"] for row in rows)
        if max_active > int(slo["max_active_kv_tokens"]):
            slo_pass = False
            violations.append("max_active_kv_tokens")

    return {
        "requests": rows,
        "p95": p95s,
        "total_prompt_tokens": sum(row["prompt_tokens"] for row in rows),
        "total_output_tokens": sum(row["output_tokens"] for row in rows),
        "max_active_kv_tokens": max(row["active_kv_tokens"] for row in rows),
        "likely_bottleneck": bottleneck,
        "slo_pass": slo_pass,
        "slo_violations": violations,
    }


def pd_pool_capacity_plan(workload, capacity):
    """Plan prefill/decode pools and KV-transfer capacity for disaggregated serving."""
    if not isinstance(workload, dict) or not isinstance(capacity, dict):
        raise ValueError("workload and capacity must be dictionaries")

    required_workload = ["qps", "mean_prompt_tokens", "mean_output_tokens"]
    required_capacity = [
        "prefill_tokens_per_s_per_worker",
        "decode_tokens_per_s_per_worker",
        "kv_transfer_tokens_per_s_per_link",
        "prefill_workers",
        "decode_workers",
    ]
    missing_workload = [name for name in required_workload if name not in workload]
    missing_capacity = [name for name in required_capacity if name not in capacity]
    if missing_workload or missing_capacity:
        raise ValueError(f"missing fields: {', '.join(missing_workload + missing_capacity)}")

    qps = float(workload["qps"])
    mean_prompt_tokens = float(workload["mean_prompt_tokens"])
    mean_output_tokens = float(workload["mean_output_tokens"])
    prefix_cache_hit_rate = float(workload.get("prefix_cache_hit_rate", 0.0))
    active_requests = float(workload.get("active_requests", qps))
    if qps <= 0 or mean_prompt_tokens <= 0 or mean_output_tokens <= 0 or active_requests < 0:
        raise ValueError("qps, prompt tokens, and output tokens must be positive; active_requests must be non-negative")
    if not 0.0 <= prefix_cache_hit_rate < 1.0:
        raise ValueError("prefix_cache_hit_rate must be in [0, 1)")

    target_utilization = float(capacity.get("target_utilization", 0.8))
    prefill_per_worker = float(capacity["prefill_tokens_per_s_per_worker"])
    decode_per_worker = float(capacity["decode_tokens_per_s_per_worker"])
    transfer_per_link = float(capacity["kv_transfer_tokens_per_s_per_link"])
    prefill_workers = int(capacity["prefill_workers"])
    decode_workers = int(capacity["decode_workers"])
    kv_transfer_links = int(capacity.get("kv_transfer_links", 1))
    if not 0.0 < target_utilization <= 1.0:
        raise ValueError("target_utilization must be in (0, 1]")
    if min(prefill_per_worker, decode_per_worker, transfer_per_link) <= 0:
        raise ValueError("per-worker/link capacities must be positive")
    if min(prefill_workers, decode_workers, kv_transfer_links) <= 0:
        raise ValueError("worker and link counts must be positive")

    effective_prefill_tokens_per_s = qps * mean_prompt_tokens * (1.0 - prefix_cache_hit_rate)
    decode_tokens_per_s = qps * mean_output_tokens
    kv_transfer_tokens_per_s = effective_prefill_tokens_per_s

    def pool(load, per_unit, units, unit_name):
        raw_capacity = per_unit * units
        budgeted_capacity = raw_capacity * target_utilization
        required_units = max(1, int(np.ceil(load / (per_unit * target_utilization)))) if load > 0 else 1
        utilization = load / raw_capacity
        return {
            f"{unit_name}s": units,
            f"required_{unit_name}s": required_units,
            "load_tokens_per_s": load,
            "raw_capacity_tokens_per_s": raw_capacity,
            "budgeted_capacity_tokens_per_s": budgeted_capacity,
            "utilization": utilization,
            "pass": utilization <= target_utilization,
        }

    prefill = pool(effective_prefill_tokens_per_s, prefill_per_worker, prefill_workers, "worker")
    decode = pool(decode_tokens_per_s, decode_per_worker, decode_workers, "worker")
    kv_transfer = pool(kv_transfer_tokens_per_s, transfer_per_link, kv_transfer_links, "link")

    active_kv_tokens = active_requests * (mean_prompt_tokens + 0.5 * mean_output_tokens)
    kv_capacity_tokens = capacity.get("kv_cache_tokens_per_decode_worker")
    if kv_capacity_tokens is None:
        kv_cache_gb_per_decode_worker = capacity.get("kv_cache_gb_per_decode_worker")
        kv_bytes_per_token = capacity.get("kv_bytes_per_token")
        if kv_cache_gb_per_decode_worker is not None and kv_bytes_per_token is not None:
            if float(kv_bytes_per_token) <= 0:
                raise ValueError("kv_bytes_per_token must be positive")
            kv_capacity_tokens = float(kv_cache_gb_per_decode_worker) * (1024**3) / float(kv_bytes_per_token)
    memory = {
        "active_kv_tokens": active_kv_tokens,
        "capacity_tokens": None,
        "utilization": None,
        "pass": True,
    }
    if kv_capacity_tokens is not None:
        kv_capacity_total = float(kv_capacity_tokens) * decode_workers
        if kv_capacity_total <= 0:
            raise ValueError("KV cache token capacity must be positive")
        memory = {
            "active_kv_tokens": active_kv_tokens,
            "capacity_tokens": kv_capacity_total,
            "utilization": active_kv_tokens / kv_capacity_total,
            "pass": active_kv_tokens <= kv_capacity_total * target_utilization,
        }

    components = {
        "prefill": prefill,
        "decode": decode,
        "kv_transfer": kv_transfer,
        "kv_memory": memory,
    }
    action_items = []
    if not prefill["pass"]:
        action_items.append("add_prefill_workers_or_raise_prefix_cache_hit_rate")
    if not decode["pass"]:
        action_items.append("add_decode_workers_or_reduce_output_tokens")
    if not kv_transfer["pass"]:
        action_items.append("increase_kv_transfer_bandwidth_or_avoid_disaggregation_for_this_workload")
    if not memory["pass"]:
        action_items.append("lower_active_kv_tokens_or_add_decode_memory_capacity")

    comparable = {
        name: comp["utilization"]
        for name, comp in components.items()
        if comp["utilization"] is not None
    }
    likely_bottleneck = max(comparable, key=comparable.get)
    overall_pass = not action_items
    return {
        "loads": {
            "effective_prefill_tokens_per_s": effective_prefill_tokens_per_s,
            "decode_tokens_per_s": decode_tokens_per_s,
            "kv_transfer_tokens_per_s": kv_transfer_tokens_per_s,
            "active_kv_tokens": active_kv_tokens,
        },
        "components": components,
        "target_utilization": target_utilization,
        "likely_bottleneck": likely_bottleneck,
        "overall_pass": overall_pass,
        "action_items": action_items,
        "decision": "pd_pool_plan_within_budget" if overall_pass else "revise_pool_sizing_or_serving_mode",
    }


def speculative_serving_gate_report(records, thresholds=None):
    """Decide whether speculative decoding is worth enabling for a measured workload."""
    if not records:
        raise ValueError("records must not be empty")
    thresholds = dict(thresholds or {})
    min_output_tokens = int(thresholds.get("min_output_tokens", 1))
    min_acceptance_rate = float(thresholds.get("min_acceptance_rate", 0.5))
    min_speedup = float(thresholds.get("min_speedup", 1.1))
    max_draft_overhead_fraction = thresholds.get("max_draft_overhead_fraction", 0.5)
    max_quality_regression = float(thresholds.get("max_quality_regression", 0.0))
    max_memory_overhead_gb = thresholds.get("max_memory_overhead_gb")
    max_qps_for_latency_mode = thresholds.get("max_qps_for_latency_mode")
    if min_output_tokens <= 0:
        raise ValueError("min_output_tokens must be positive")
    for name, value in [
        ("min_acceptance_rate", min_acceptance_rate),
        ("max_quality_regression", max_quality_regression),
    ]:
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be in [0, 1]")
    if min_speedup <= 0:
        raise ValueError("min_speedup must be positive")
    if max_draft_overhead_fraction is not None:
        max_draft_overhead_fraction = float(max_draft_overhead_fraction)
        if not 0.0 <= max_draft_overhead_fraction <= 1.0:
            raise ValueError("max_draft_overhead_fraction must be in [0, 1]")
    if max_memory_overhead_gb is not None and float(max_memory_overhead_gb) < 0:
        raise ValueError("max_memory_overhead_gb must be non-negative")
    if max_qps_for_latency_mode is not None and float(max_qps_for_latency_mode) <= 0:
        raise ValueError("max_qps_for_latency_mode must be positive")

    rows = []
    for idx, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError("each record must be a dict")
        required = ["baseline_ms", "speculative_ms", "output_tokens", "draft_tokens", "accepted_tokens", "target_verify_steps"]
        missing = [name for name in required if name not in record]
        if missing:
            raise ValueError(f"record {idx} missing fields: {', '.join(missing)}")

        baseline_ms = float(record["baseline_ms"])
        speculative_ms = float(record["speculative_ms"])
        output_tokens = int(record["output_tokens"])
        draft_tokens = int(record["draft_tokens"])
        accepted_tokens = int(record["accepted_tokens"])
        target_verify_steps = int(record["target_verify_steps"])
        draft_ms = record.get("draft_ms")
        draft_ms = None if draft_ms is None else float(draft_ms)
        quality_regression = float(record.get("quality_regression", 0.0))
        memory_overhead_gb = float(record.get("memory_overhead_gb", 0.0))
        qps = record.get("qps")
        qps = None if qps is None else float(qps)
        if min(baseline_ms, speculative_ms) <= 0:
            raise ValueError("baseline_ms and speculative_ms must be positive")
        if min(output_tokens, draft_tokens, target_verify_steps) <= 0:
            raise ValueError("output_tokens, draft_tokens, and target_verify_steps must be positive")
        if not 0 <= accepted_tokens <= draft_tokens:
            raise ValueError("accepted_tokens must be between 0 and draft_tokens")
        if draft_ms is not None and draft_ms < 0:
            raise ValueError("draft_ms must be non-negative")
        if not 0.0 <= quality_regression <= 1.0:
            raise ValueError("quality_regression must be in [0, 1]")
        if memory_overhead_gb < 0:
            raise ValueError("memory_overhead_gb must be non-negative")
        if qps is not None and qps <= 0:
            raise ValueError("qps must be positive")

        rows.append(
            {
                "record_id": record.get("record_id", idx),
                "baseline_ms": baseline_ms,
                "speculative_ms": speculative_ms,
                "output_tokens": output_tokens,
                "draft_tokens": draft_tokens,
                "accepted_tokens": accepted_tokens,
                "target_verify_steps": target_verify_steps,
                "draft_ms": draft_ms,
                "quality_regression": quality_regression,
                "memory_overhead_gb": memory_overhead_gb,
                "qps": qps,
                "lossless_validation_passed": bool(record.get("lossless_validation_passed", True)),
            }
        )

    total_output_tokens = sum(row["output_tokens"] for row in rows)
    total_draft_tokens = sum(row["draft_tokens"] for row in rows)
    total_accepted_tokens = sum(row["accepted_tokens"] for row in rows)
    total_baseline_ms = sum(row["baseline_ms"] for row in rows)
    total_speculative_ms = sum(row["speculative_ms"] for row in rows)
    total_verify_steps = sum(row["target_verify_steps"] for row in rows)
    draft_ms_values = [row["draft_ms"] for row in rows if row["draft_ms"] is not None]
    total_draft_ms = sum(draft_ms_values) if draft_ms_values else None
    draft_overhead_fraction = None if total_draft_ms is None else total_draft_ms / total_speculative_ms
    acceptance_rate = total_accepted_tokens / total_draft_tokens
    speedup = total_baseline_ms / total_speculative_ms
    max_quality_regression_observed = max(row["quality_regression"] for row in rows)
    max_memory_overhead_observed = max(row["memory_overhead_gb"] for row in rows)
    max_qps_observed = max((row["qps"] for row in rows if row["qps"] is not None), default=None)

    gates = {
        "sample_size": total_output_tokens >= min_output_tokens,
        "acceptance_rate": acceptance_rate >= min_acceptance_rate,
        "speedup": speedup >= min_speedup,
        "quality": max_quality_regression_observed <= max_quality_regression and all(row["lossless_validation_passed"] for row in rows),
    }
    if max_draft_overhead_fraction is not None and draft_overhead_fraction is not None:
        gates["draft_overhead"] = draft_overhead_fraction <= max_draft_overhead_fraction
    if max_memory_overhead_gb is not None:
        gates["memory_overhead"] = max_memory_overhead_observed <= float(max_memory_overhead_gb)
    if max_qps_for_latency_mode is not None and max_qps_observed is not None:
        gates["latency_workload_fit"] = max_qps_observed <= float(max_qps_for_latency_mode)

    action_items = []
    if not gates["sample_size"]:
        action_items.append("collect_more_speculative_decode_samples")
    if not gates["acceptance_rate"]:
        action_items.append("improve_draft_model_or_reduce_speculation_depth")
    if not gates["speedup"]:
        action_items.append("keep_speculation_disabled_until_speedup_reproduces")
    if not gates["quality"]:
        action_items.append("run_lossless_or_quality_regression_validation")
    if gates.get("draft_overhead") is False:
        action_items.append("reduce_draft_cost_or_use_ngram_suffix_method")
    if gates.get("memory_overhead") is False:
        action_items.append("reduce_extra_memory_or_choose_lighter_speculator")
    if gates.get("latency_workload_fit") is False:
        action_items.append("benchmark_under_target_qps_and_batching")

    overall_pass = not action_items
    return {
        "records": rows,
        "totals": {
            "output_tokens": total_output_tokens,
            "draft_tokens": total_draft_tokens,
            "accepted_tokens": total_accepted_tokens,
            "target_verify_steps": total_verify_steps,
            "baseline_ms": total_baseline_ms,
            "speculative_ms": total_speculative_ms,
            "draft_ms": total_draft_ms,
        },
        "metrics": {
            "acceptance_rate": acceptance_rate,
            "speedup": speedup,
            "baseline_tpot_ms": total_baseline_ms / total_output_tokens,
            "speculative_tpot_ms": total_speculative_ms / total_output_tokens,
            "tokens_per_verify_step": total_output_tokens / total_verify_steps,
            "draft_overhead_fraction": draft_overhead_fraction,
            "max_quality_regression": max_quality_regression_observed,
            "max_memory_overhead_gb": max_memory_overhead_observed,
            "max_qps": max_qps_observed,
        },
        "gates": gates,
        "overall_pass": overall_pass,
        "action_items": action_items,
        "decision": "enable_speculative_decoding_for_this_workload" if overall_pass else "keep_baseline_or_rebenchmark_speculation",
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
