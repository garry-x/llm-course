"""Autograder-style tests for Chapter 4 multi-head attention exercises."""

import importlib
import os
import unittest

try:
    import torch
except ModuleNotFoundError:
    torch = None


MODULE_NAME = os.environ.get("STUDENT_MODULE", "reference_solution")
submission = importlib.import_module(MODULE_NAME) if torch is not None else None


@unittest.skipIf(torch is None, "PyTorch is required for Ch04 multi-head tests")
class TestMultiHeadAttention(unittest.TestCase):
    def test_mha_shapes_mask_and_normalization(self):
        torch.manual_seed(0)
        mha = submission.MultiHeadAttention(d_model=16, n_heads=4, dropout=0.0)
        x = torch.randn(2, 5, 16)
        mask = torch.ones(5, 5, dtype=torch.bool).tril()
        out, weights = mha(x, mask)
        self.assertEqual(tuple(out.shape), (2, 5, 16))
        self.assertEqual(tuple(weights.shape), (2, 4, 5, 5))
        self.assertTrue(torch.allclose(weights.sum(dim=-1), torch.ones(2, 4, 5), atol=1e-6))
        future = torch.triu(torch.ones(5, 5, dtype=torch.bool), diagonal=1)
        self.assertTrue(torch.all(weights[:, :, future] < 1e-6))

    def test_mha_parameter_shapes(self):
        mha = submission.MultiHeadAttention(d_model=24, n_heads=6, dropout=0.0)
        self.assertEqual(tuple(mha.W_qkv.weight.shape), (72, 24))
        self.assertEqual(tuple(mha.W_o.weight.shape), (24, 24))
        self.assertEqual(submission.count_params(mha), 4 * 24 * 24)


@unittest.skipIf(torch is None, "PyTorch is required for Ch04 multi-head tests")
class TestSingleHeadEquivalence(unittest.TestCase):
    def test_single_head_and_mha_parameter_count_match(self):
        d_model = 32
        mha = submission.MultiHeadAttention(d_model=d_model, n_heads=4, dropout=0.0)
        sha = submission.SingleHeadAttention(d_model=d_model)
        self.assertEqual(submission.count_params(mha), submission.count_params(sha))
        self.assertEqual(mha.W_qkv.weight.numel(), sha.W_qkv.weight.numel())


@unittest.skipIf(torch is None, "PyTorch is required for Ch04 multi-head tests")
class TestGroupedQueryAttention(unittest.TestCase):
    def test_repeat_kv_heads_expands_grouped_kv_heads(self):
        kv = torch.tensor(
            [
                [
                    [[1.0, 10.0], [2.0, 20.0]],
                    [[3.0, 30.0], [4.0, 40.0]],
                ]
            ]
        )
        repeated = submission.repeat_kv_heads(kv, n_rep=3)
        self.assertEqual(tuple(repeated.shape), (1, 6, 2, 2))
        self.assertTrue(torch.equal(repeated[:, 0], kv[:, 0]))
        self.assertTrue(torch.equal(repeated[:, 1], kv[:, 0]))
        self.assertTrue(torch.equal(repeated[:, 2], kv[:, 0]))
        self.assertTrue(torch.equal(repeated[:, 3], kv[:, 1]))
        self.assertTrue(torch.equal(repeated[:, 4], kv[:, 1]))
        self.assertTrue(torch.equal(repeated[:, 5], kv[:, 1]))

    def test_repeat_kv_heads_rejects_bad_inputs(self):
        with self.assertRaises(ValueError):
            submission.repeat_kv_heads(torch.randn(2, 3, 4), n_rep=2)
        with self.assertRaises(ValueError):
            submission.repeat_kv_heads(torch.randn(1, 2, 3, 4), n_rep=0)

    def test_gqa_shapes_and_kv_parameter_savings(self):
        torch.manual_seed(1)
        gqa = submission.GroupedQueryAttention(
            d_model=32,
            n_heads=8,
            n_kv_heads=2,
            dropout=0.0,
        )
        x = torch.randn(2, 6, 32)
        out, weights = gqa(x)
        self.assertEqual(tuple(out.shape), (2, 6, 32))
        self.assertEqual(tuple(weights.shape), (2, 8, 6, 6))
        self.assertTrue(torch.allclose(weights.sum(dim=-1), torch.ones(2, 8, 6), atol=1e-6))
        self.assertEqual(gqa.n_rep, 4)
        self.assertEqual(gqa.W_k.weight.numel(), 32 * (2 * 4))
        self.assertLess(gqa.W_k.weight.numel() + gqa.W_v.weight.numel(), 2 * 32 * 32)

    def test_gqa_rejects_invalid_grouping(self):
        with self.assertRaises(AssertionError):
            submission.GroupedQueryAttention(d_model=32, n_heads=6, n_kv_heads=4)

    def test_gqa_head_mapping_assigns_query_groups_to_kv_heads(self):
        self.assertEqual(submission.gqa_head_mapping(n_heads=8, n_kv_heads=2), [0, 0, 0, 0, 1, 1, 1, 1])
        self.assertEqual(submission.gqa_head_mapping(n_heads=4, n_kv_heads=1), [0, 0, 0, 0])
        self.assertEqual(submission.gqa_head_mapping(n_heads=4, n_kv_heads=4), [0, 1, 2, 3])
        with self.assertRaises(ValueError):
            submission.gqa_head_mapping(n_heads=6, n_kv_heads=4)
        with self.assertRaises(ValueError):
            submission.gqa_head_mapping(n_heads=0, n_kv_heads=1)


@unittest.skipIf(torch is None, "PyTorch is required for Ch04 multi-head tests")
class TestMLA(unittest.TestCase):
    def test_mla_shapes_and_latent_cache(self):
        torch.manual_seed(2)
        mla = submission.MLA(d_model=32, n_heads=4, d_latent=6, dropout=0.0)
        x = torch.randn(2, 5, 32)
        out, weights, latent = mla(x)
        self.assertEqual(tuple(out.shape), (2, 5, 32))
        self.assertEqual(tuple(weights.shape), (2, 4, 5, 5))
        self.assertEqual(tuple(latent.shape), (2, 5, 6))
        self.assertTrue(torch.allclose(weights.sum(dim=-1), torch.ones(2, 4, 5), atol=1e-6))
        self.assertEqual(mla.W_dkv.weight.numel(), 32 * 6)

    def test_mla_absorbed_scores_match_explicit_k_decompression(self):
        torch.manual_seed(3)
        batch, n_heads, t_q, t_k, d_head, d_latent = 2, 3, 4, 5, 2, 7
        q = torch.randn(batch, n_heads, t_q, d_head)
        latent = torch.randn(batch, t_k, d_latent)
        up_k_weight = torch.randn(n_heads * d_head, d_latent)

        explicit_k = torch.nn.functional.linear(latent, up_k_weight)
        explicit_k = explicit_k.reshape(batch, t_k, n_heads, d_head).transpose(1, 2)
        explicit_scores = torch.matmul(q, explicit_k.transpose(-2, -1)) / (d_head**0.5)
        absorbed_scores = submission.mla_absorbed_attention_scores(q, latent, up_k_weight)

        self.assertTrue(torch.allclose(absorbed_scores, explicit_scores, atol=1e-5))
        self.assertEqual(tuple(absorbed_scores.shape), (batch, n_heads, t_q, t_k))

    def test_mla_absorbed_scores_reject_bad_shapes(self):
        q = torch.randn(2, 3, 4, 2)
        latent = torch.randn(2, 5, 7)
        up_k_weight = torch.randn(6, 7)
        with self.assertRaises(ValueError):
            submission.mla_absorbed_attention_scores(torch.randn(2, 4, 2), latent, up_k_weight)
        with self.assertRaises(ValueError):
            submission.mla_absorbed_attention_scores(q, torch.randn(2, 7), up_k_weight)
        with self.assertRaises(ValueError):
            submission.mla_absorbed_attention_scores(q, latent, torch.randn(5, 7))
        with self.assertRaises(ValueError):
            submission.mla_absorbed_attention_scores(q, latent, torch.randn(6, 8))
        with self.assertRaises(ValueError):
            submission.mla_absorbed_attention_scores(q, latent, up_k_weight, scale=0.0)


@unittest.skipIf(torch is None, "PyTorch is required for Ch04 multi-head tests")
class TestKVCacheAnalysis(unittest.TestCase):
    def test_kv_cache_size_ratios(self):
        result = submission.compute_kv_cache_size(
            d_model=7168,
            n_heads=64,
            n_kv_heads=8,
            d_latent=512,
            seq_len=131072,
        )
        self.assertEqual(result["mha_per_token"], 14336)
        self.assertEqual(result["gqa_per_token"], 1792)
        self.assertEqual(result["mla_per_token"], 512)
        self.assertAlmostEqual(result["mha_per_token"] / result["gqa_per_token"], 8.0)
        self.assertAlmostEqual(result["mha_per_token"] / result["mla_per_token"], 28.0)
        self.assertGreater(result["mha_total_gb"], result["gqa_total_gb"])
        self.assertGreater(result["gqa_total_gb"], result["mla_total_gb"])

    def test_kv_cache_budget_includes_batch_layers_and_dtype(self):
        result = submission.compare_kv_cache_budget(
            d_model=4096,
            n_heads=32,
            n_kv_heads=8,
            d_latent=512,
            seq_len=2048,
            batch_size=4,
            n_layers=24,
            dtype_bytes=2,
        )
        self.assertEqual(result["head_dim"], 128)
        self.assertEqual(result["per_token_elements"]["mha"], 8192)
        self.assertEqual(result["per_token_elements"]["gqa"], 2048)
        self.assertEqual(result["per_token_elements"]["mla"], 512)
        expected_mha_bytes = 8192 * 2048 * 4 * 24 * 2
        self.assertEqual(result["total_bytes"]["mha"], expected_mha_bytes)
        self.assertAlmostEqual(result["compression_vs_mha"]["gqa"], 4.0)
        self.assertAlmostEqual(result["compression_vs_mha"]["mla"], 16.0)

    def test_kv_cache_budget_rejects_invalid_configs(self):
        with self.assertRaises(ValueError):
            submission.compare_kv_cache_budget(10, 3, 1, 4, 128)
        with self.assertRaises(ValueError):
            submission.compare_kv_cache_budget(12, 6, 4, 4, 128)
        with self.assertRaises(ValueError):
            submission.compare_kv_cache_budget(12, 6, 3, 4, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
