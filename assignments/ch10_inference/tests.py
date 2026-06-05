"""Autograder-style tests for Chapter 10 inference-engineering exercises."""

import importlib
import os
import unittest

try:
    import numpy as np
    import torch
except ModuleNotFoundError:
    np = None
    torch = None


MODULE_NAME = os.environ.get("STUDENT_MODULE", "reference_solution")
submission = importlib.import_module(MODULE_NAME) if torch is not None and np is not None else None


@unittest.skipIf(torch is None or np is None, "PyTorch and NumPy are required for Ch10 inference tests")
class TestKVCache(unittest.TestCase):
    def test_incremental_attention_matches_full_causal_attention(self):
        torch.manual_seed(0)
        attn = submission.AttentionWithCache(d_model=8, n_heads=2, dropout=0.0)
        x = torch.randn(2, 5, 8)
        full_out, _ = attn(x, cache=None)

        cache = None
        pieces = []
        for t in range(x.size(1)):
            out, cache = attn(x[:, t : t + 1, :], cache=cache)
            pieces.append(out)
            self.assertEqual(tuple(cache["k"].shape), (2, 2, t + 1, 4))
            self.assertEqual(tuple(cache["v"].shape), (2, 2, t + 1, 4))
        inc_out = torch.cat(pieces, dim=1)
        self.assertTrue(torch.allclose(inc_out, full_out, atol=1e-5))

    def test_causal_mask_allows_all_past_tokens_for_single_decode_query(self):
        attn = submission.AttentionWithCache(d_model=8, n_heads=2, dropout=0.0)
        mask = attn._causal_mask(l_kv=4, l_q=1, device=torch.device("cpu"))
        self.assertEqual(mask.tolist(), [[True, True, True, True]])


@unittest.skipIf(torch is None or np is None, "PyTorch and NumPy are required for Ch10 inference tests")
class TestMemoryQuantization(unittest.TestCase):
    def test_kv_cache_memory_includes_batch_size(self):
        result = submission.kv_cache_memory_analysis(
            n_layers=2,
            n_kv_heads=3,
            d_head=4,
            seq_len=5,
            batch_size=7,
            dtype_bytes=2,
            model_params_gb=1.0,
        )
        expected_bytes = 7 * 2 * 5 * 3 * 4 * 2 * 2
        self.assertEqual(result["bytes"], expected_bytes)
        self.assertAlmostEqual(result["total_cache_gb"], expected_bytes / (1024**3))
        self.assertAlmostEqual(result["cache_to_params_ratio"], result["total_cache_gb"])

    def test_int8_per_channel_quantization_roundtrip(self):
        weight = torch.tensor([[0.0, 1.0, -1.0], [2.0, -4.0, 0.5], [0.0, 0.0, 0.0]])
        q, scales = submission.quantize_per_channel(weight)
        self.assertEqual(q.dtype, torch.int8)
        self.assertEqual(tuple(scales.shape), (3,))
        deq = submission.dequantize(q, scales)
        self.assertFalse(torch.isnan(deq).any())
        self.assertLess(submission.nrmse(weight, deq), 0.01)
        self.assertTrue(torch.all(q[2] == 0))


@unittest.skipIf(torch is None or np is None, "PyTorch and NumPy are required for Ch10 inference tests")
class TestContrastiveRetrievalTraining(unittest.TestCase):
    def test_contrastive_inbatch_loss_uses_diagonal_positives(self):
        query_embeddings = torch.tensor(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        )
        doc_embeddings = torch.tensor(
            [
                [0.9, 0.1, 0.0],
                [0.1, 0.8, 0.0],
                [0.0, 0.1, 0.9],
            ]
        )
        result = submission.contrastive_inbatch_loss(query_embeddings, doc_embeddings, temperature=0.5)
        self.assertEqual(tuple(result["logits"].shape), (3, 3))
        self.assertGreater(result["logits"][0, 0], result["logits"][0, 1])
        self.assertGreater(result["logits"][1, 1], result["logits"][1, 0])
        self.assertAlmostEqual(result["accuracy"], 1.0)

        labels = torch.arange(3)
        expected_loss = torch.nn.functional.cross_entropy(result["logits"], labels)
        self.assertTrue(torch.allclose(result["loss"], expected_loss))

    def test_contrastive_inbatch_loss_rejects_bad_shapes(self):
        with self.assertRaises(ValueError):
            submission.contrastive_inbatch_loss(torch.randn(2, 3), torch.randn(2, 3), temperature=0.0)
        with self.assertRaises(ValueError):
            submission.contrastive_inbatch_loss(torch.randn(2, 3), torch.randn(3, 3))
        with self.assertRaises(ValueError):
            submission.contrastive_inbatch_loss(torch.randn(2, 3, 1), torch.randn(2, 3, 1))


@unittest.skipIf(torch is None or np is None, "PyTorch and NumPy are required for Ch10 inference tests")
class TestRerankerTraining(unittest.TestCase):
    def test_pairwise_reranker_loss_uses_chosen_rejected_preferences(self):
        chosen = torch.tensor([3.0, 1.0, 2.5])
        rejected = torch.tensor([1.0, 1.5, 0.5])
        result = submission.pairwise_reranker_loss(chosen, rejected, margin=0.2)

        margins = chosen - rejected
        expected_loss = torch.nn.functional.softplus(-(margins - 0.2)).mean()
        self.assertTrue(torch.allclose(result["loss"], expected_loss))
        self.assertTrue(torch.allclose(result["margins"], margins))
        self.assertAlmostEqual(result["accuracy"], 2 / 3)

    def test_pairwise_reranker_loss_rejects_bad_inputs(self):
        with self.assertRaises(ValueError):
            submission.pairwise_reranker_loss(torch.tensor([]), torch.tensor([]))
        with self.assertRaises(ValueError):
            submission.pairwise_reranker_loss(torch.ones(2), torch.ones(3))
        with self.assertRaises(ValueError):
            submission.pairwise_reranker_loss(torch.ones(2), torch.ones(2), margin=-0.1)


@unittest.skipIf(torch is None or np is None, "PyTorch and NumPy are required for Ch10 inference tests")
class TestRetrievalMetrics(unittest.TestCase):
    def test_recall_and_reciprocal_rank_at_k(self):
        retrieved = ["doc9", "doc2", "doc5", "doc1"]
        relevant = {"doc1", "doc2", "doc7"}
        self.assertAlmostEqual(submission.recall_at_k(retrieved, relevant, k=3), 1 / 3)
        self.assertAlmostEqual(submission.reciprocal_rank_at_k(retrieved, relevant, k=3), 1 / 2)
        self.assertEqual(submission.reciprocal_rank_at_k(["doc9", "doc8"], relevant, k=2), 0.0)

    def test_ndcg_at_k_rewards_better_ordering_with_graded_relevance(self):
        relevance = {"doc1": 3.0, "doc2": 2.0, "doc3": 1.0}
        ideal = ["doc1", "doc2", "doc3"]
        poor = ["doc3", "doc2", "doc1"]
        self.assertAlmostEqual(submission.ndcg_at_k(ideal, relevance, k=3), 1.0)
        self.assertLess(submission.ndcg_at_k(poor, relevance, k=3), 1.0)

        expected = (
            (2**1 - 1) / np.log2(2)
            + (2**2 - 1) / np.log2(3)
            + (2**3 - 1) / np.log2(4)
        ) / (
            (2**3 - 1) / np.log2(2)
            + (2**2 - 1) / np.log2(3)
            + (2**1 - 1) / np.log2(4)
        )
        self.assertAlmostEqual(submission.ndcg_at_k(poor, relevance, k=3), expected)

    def test_retrieval_metrics_reject_invalid_inputs(self):
        with self.assertRaises(ValueError):
            submission.recall_at_k(["doc1"], {"doc1"}, k=0)
        with self.assertRaises(ValueError):
            submission.recall_at_k(["doc1"], set(), k=1)
        with self.assertRaises(ValueError):
            submission.reciprocal_rank_at_k(["doc1"], set(), k=1)
        with self.assertRaises(ValueError):
            submission.ndcg_at_k(["doc1"], {}, k=1)
        with self.assertRaises(ValueError):
            submission.ndcg_at_k(["doc1"], {"doc1": -1.0}, k=1)
        with self.assertRaises(ValueError):
            submission.ndcg_at_k(["doc1"], {"doc1": 1.0}, k=0)

    def test_reciprocal_rank_fusion_combines_ranked_lists(self):
        dense = ["docA", "docB", "docC"]
        sparse = ["docB", "docD", "docA"]
        fused = submission.reciprocal_rank_fusion([dense, sparse], k=60)
        fused_ids = [doc_id for doc_id, _score in fused]
        self.assertEqual(fused_ids[0], "docB")
        self.assertIn("docA", fused_ids[:2])
        self.assertGreater(dict(fused)["docB"], dict(fused)["docD"])

    def test_rerank_documents_uses_query_document_scorer(self):
        candidates = [
            ("doc1", "apple car"),
            ("doc2", "apple banana fruit"),
            ("doc3", "engine car"),
        ]

        def scorer(query, text):
            return len(set(query.split()) & set(text.split()))

        reranked = submission.rerank_documents("apple fruit", candidates, scorer, top_k=2)
        self.assertEqual([item["doc_id"] for item in reranked], ["doc2", "doc1"])
        self.assertEqual(reranked[0]["original_rank"], 2)
        self.assertEqual(reranked[0]["score"], 2.0)

    def test_mmr_trades_query_similarity_against_redundancy(self):
        query = torch.tensor([1.0, 0.0])
        docs = torch.tensor(
            [
                [1.0, 0.0],
                [0.9, 0.1],
                [0.4, 0.8],
            ]
        )
        selected = submission.maximal_marginal_relevance(
            query,
            docs,
            doc_ids=["exact", "near_duplicate", "diverse"],
            top_k=2,
            lambda_mult=0.4,
        )
        self.assertEqual([item["doc_id"] for item in selected], ["exact", "diverse"])
        self.assertGreater(selected[1]["diversity_penalty"], 0.0)

    def test_build_rag_context_packs_citations_under_budget(self):
        chunks = [
            {"doc_id": "A", "text": "alpha beta", "score": 0.9},
            {"doc_id": "B", "text": "gamma delta epsilon", "score": 0.8},
            {"doc_id": "C", "text": "zeta eta theta iota", "score": 0.7},
        ]
        packed = submission.build_rag_context(
            chunks,
            max_context_tokens=9,
            reserved_output_tokens=2,
            token_counter=lambda text: len(text.split()),
        )
        self.assertEqual(packed["context_budget"], 7)
        self.assertLessEqual(packed["used_tokens"], packed["context_budget"])
        self.assertEqual(packed["citations"], ["A", "B"])
        self.assertIn("[A] alpha beta", packed["context"])
        self.assertIn("[B] gamma delta epsilon", packed["context"])
        self.assertNotIn("[C]", packed["context"])
        self.assertEqual(packed["skipped"], 1)
        self.assertEqual([item["tokens"] for item in packed["selected"]], [3, 4])

    def test_build_rag_context_rejects_bad_budget_and_chunks(self):
        chunks = [{"doc_id": "A", "text": "alpha"}]
        with self.assertRaises(ValueError):
            submission.build_rag_context(chunks, max_context_tokens=0)
        with self.assertRaises(ValueError):
            submission.build_rag_context(chunks, max_context_tokens=4, reserved_output_tokens=4)
        with self.assertRaises(ValueError):
            submission.build_rag_context([("A", "alpha")], max_context_tokens=4)
        with self.assertRaises(ValueError):
            submission.build_rag_context([{"doc_id": "A"}], max_context_tokens=4)
        with self.assertRaises(ValueError):
            submission.build_rag_context(chunks, max_context_tokens=4, token_counter=lambda _text: 0)

    def test_reranking_helpers_reject_invalid_inputs(self):
        with self.assertRaises(ValueError):
            submission.reciprocal_rank_fusion([], k=60)
        with self.assertRaises(ValueError):
            submission.reciprocal_rank_fusion([["doc"]], k=0)
        with self.assertRaises(ValueError):
            submission.rerank_documents("q", [("doc", "text")], lambda _q, _d: 1.0, top_k=0)
        with self.assertRaises(ValueError):
            submission.maximal_marginal_relevance(torch.ones(2), torch.ones(2, 2), top_k=0)
        with self.assertRaises(ValueError):
            submission.maximal_marginal_relevance(torch.ones(2), torch.ones(2, 2), lambda_mult=1.5)
        with self.assertRaises(ValueError):
            submission.maximal_marginal_relevance(torch.ones(2), torch.ones(2, 3))


class BagOfWordsEmbedder:
    def __init__(self):
        self.vocab = {"apple": 0, "banana": 1, "car": 2, "engine": 3, "fruit": 4}

    def encode(self, text):
        vec = np.zeros(len(self.vocab), dtype=np.float64)
        for token in text.lower().split():
            if token in self.vocab:
                vec[self.vocab[token]] += 1.0
        return vec


class EchoLLM:
    def generate(self, prompt):
        return prompt


@unittest.skipIf(torch is None or np is None, "PyTorch and NumPy are required for Ch10 inference tests")
class TestRAGBenchmarkLSH(unittest.TestCase):
    def test_rag_retrieves_by_cosine_similarity_and_builds_prompt(self):
        rag = submission.SimpleRAG(BagOfWordsEmbedder(), EchoLLM(), chunk_size=4, overlap=1)
        rag.add_document("apple banana fruit car engine car")
        results = rag.retrieve("apple fruit", top_k=2)
        self.assertEqual(len(results), 2)
        self.assertGreaterEqual(results[0][1], results[1][1])
        self.assertIn("apple banana fruit", results[0][0])
        answer = rag.query("apple fruit")
        self.assertIn("文档内容", answer)
        self.assertIn("apple", answer)

    def test_rag_rejects_invalid_overlap(self):
        with self.assertRaises(ValueError):
            submission.SimpleRAG(BagOfWordsEmbedder(), EchoLLM(), chunk_size=4, overlap=4)

    def test_benchmark_summary_reports_core_slo_metrics(self):
        result = submission.summarize_benchmark([100.0, 20.0, 30.0, 40.0], generated_tokens=3, memory_gb=1.5)
        self.assertEqual(result["ttft_ms"], 100.0)
        self.assertAlmostEqual(result["ms_per_token"], 30.0)
        self.assertAlmostEqual(result["tokens_per_second"], 3 / 0.19)
        self.assertEqual(result["memory_gb"], 1.5)
        self.assertGreaterEqual(result["p95_ms"], result["ms_per_token"])

    def test_metric_card_preserves_benchmark_context_and_limits(self):
        card = submission.build_metric_card(
            task="rag qa",
            metrics={"pass_rate": 0.8, "p95_ms": 320.0},
            baseline="bm25-only",
            sample_size=25,
            risks=["retrieval_contamination", "judge_bias"],
            uncertainty="bootstrap_ci_or_repeated_runs_needed",
            conclusion="hybrid improves this fixed dev set only",
        )
        self.assertEqual(card["task"], "rag qa")
        self.assertEqual(card["sample_size"], 25)
        self.assertEqual(card["baseline"], "bm25-only")
        self.assertAlmostEqual(card["metrics"]["pass_rate"], 0.8)
        self.assertIn("retrieval_contamination", card["risks"])
        self.assertIn("fixed dev set", card["conclusion"])

    def test_metric_card_rejects_missing_core_fields(self):
        with self.assertRaises(ValueError):
            submission.build_metric_card("", {"acc": 1.0}, "baseline", 10)
        with self.assertRaises(ValueError):
            submission.build_metric_card("qa", {}, "baseline", 10)
        with self.assertRaises(ValueError):
            submission.build_metric_card("qa", {"acc": 1.0}, "", 10)
        with self.assertRaises(ValueError):
            submission.build_metric_card("qa", {"acc": 1.0}, "baseline", 0)

    def test_lsh_returns_best_same_bucket_candidate(self):
        memory = submission.LSHMemory(dim=2, n_bits=1, seed=0)
        memory.planes = torch.tensor([[1.0, 0.0]])
        memory.add(torch.tensor([1.0, 0.0]), "near")
        memory.add(torch.tensor([0.2, 1.0]), "far")
        memory.add(torch.tensor([-1.0, 0.0]), "other_bucket")
        self.assertEqual(memory.query(torch.tensor([0.9, 0.1])), "near")
        self.assertEqual(memory.query(torch.tensor([-0.9, 0.1])), "other_bucket")


if __name__ == "__main__":
    unittest.main(verbosity=2)
