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


if __name__ == "__main__":
    unittest.main(verbosity=2)
