"""Starter code for Chapter 10 inference-engineering assignment."""

import torch
import torch.nn as nn


class AttentionWithCache(nn.Module):
    def __init__(self, d_model, n_heads, dropout=0.0):
        super().__init__()
        raise NotImplementedError

    def forward(self, x, cache=None):
        raise NotImplementedError

    def _causal_mask(self, l_kv, l_q, device):
        raise NotImplementedError


def kv_cache_memory_analysis(n_layers, n_kv_heads, d_head, seq_len, batch_size=1, dtype_bytes=2, model_params_gb=None):
    raise NotImplementedError


def quantize_per_channel(tensor):
    raise NotImplementedError


def dequantize(quantized, scales):
    raise NotImplementedError


def nrmse(original, reconstructed):
    raise NotImplementedError


def recall_at_k(retrieved_ids, relevant_ids, k):
    raise NotImplementedError


def reciprocal_rank_at_k(retrieved_ids, relevant_ids, k):
    raise NotImplementedError


def reciprocal_rank_fusion(rankings, k=60):
    """Fuse multiple ranked document-id lists with reciprocal rank fusion."""
    raise NotImplementedError


def rerank_documents(query, candidates, scorer, top_k=None):
    """Rerank candidate (doc_id, text) pairs with a query-document scorer."""
    raise NotImplementedError


class SimpleRAG:
    def __init__(self, embed_model, llm, chunk_size=512, overlap=64):
        raise NotImplementedError

    def add_document(self, text):
        raise NotImplementedError

    def retrieve(self, query, top_k=3):
        raise NotImplementedError

    def query(self, question):
        raise NotImplementedError


def summarize_benchmark(latencies, generated_tokens, memory_gb):
    raise NotImplementedError


def build_metric_card(task, metrics, baseline, sample_size, risks=None, uncertainty=None, conclusion=None):
    raise NotImplementedError


class LSHMemory:
    def __init__(self, dim, n_bits=8, seed=0):
        raise NotImplementedError

    def _hash(self, x):
        raise NotImplementedError

    def add(self, vec, value):
        raise NotImplementedError

    def query(self, vec):
        raise NotImplementedError
