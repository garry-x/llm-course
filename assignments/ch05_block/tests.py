"""Autograder-style tests for Chapter 5 Transformer block exercises."""

import importlib
import os
import unittest

try:
    import torch
    import torch.nn as nn
    from torch.autograd import gradcheck
except ModuleNotFoundError:
    torch = None
    nn = None
    gradcheck = None


MODULE_NAME = os.environ.get("STUDENT_MODULE", "reference_solution")
submission = importlib.import_module(MODULE_NAME) if torch is not None else None


@unittest.skipIf(torch is None, "PyTorch is required for Ch05 block tests")
class TestLayerNorm(unittest.TestCase):
    def test_layer_norm_matches_pytorch(self):
        torch.manual_seed(0)
        layer_norm = submission.LayerNorm(6, eps=1e-6)
        reference = nn.LayerNorm(6, eps=1e-6)
        with torch.no_grad():
            reference.weight.copy_(layer_norm.gamma)
            reference.bias.copy_(layer_norm.beta)

        x = torch.randn(3, 4, 6)
        y = layer_norm(x)
        y_ref = reference(x)
        self.assertTrue(torch.allclose(y, y_ref, atol=1e-5))
        self.assertTrue(torch.allclose(y.mean(dim=-1), torch.zeros(3, 4), atol=1e-5))
        self.assertTrue(torch.allclose(y.var(dim=-1, unbiased=False), torch.ones(3, 4), atol=1e-4))

    def test_layer_norm_function_gradcheck(self):
        torch.manual_seed(1)
        x = torch.randn(2, 3, 4, dtype=torch.float64, requires_grad=True)
        gamma = torch.randn(4, dtype=torch.float64, requires_grad=True)
        beta = torch.randn(4, dtype=torch.float64, requires_grad=True)
        self.assertTrue(
            gradcheck(
                submission.LayerNormFunction.apply,
                (x, gamma, beta, 1e-6),
                eps=1e-6,
                atol=1e-4,
                rtol=1e-3,
            )
        )


@unittest.skipIf(torch is None, "PyTorch is required for Ch05 block tests")
class TestRMSNorm(unittest.TestCase):
    def test_rms_norm_scales_rms_without_centering(self):
        torch.manual_seed(2)
        rms_norm = submission.RMSNorm(8, eps=1e-6)
        x = torch.randn(2, 5, 8) + 3.0
        y = rms_norm(x)
        rms = torch.sqrt(y.pow(2).mean(dim=-1))
        self.assertTrue(torch.allclose(rms, torch.ones_like(rms), atol=1e-5))
        self.assertFalse(torch.allclose(y.mean(dim=-1), torch.zeros(2, 5), atol=1e-2))
        self.assertFalse(hasattr(rms_norm, "beta"))


@unittest.skipIf(torch is None, "PyTorch is required for Ch05 block tests")
class TestFeedForward(unittest.TestCase):
    def test_ffn_shape_and_default_width(self):
        torch.manual_seed(3)
        ffn = submission.FFN(d_model=12)
        x = torch.randn(2, 7, 12)
        y = ffn(x)
        self.assertEqual(tuple(y.shape), (2, 7, 12))
        self.assertEqual(ffn.fc1.out_features, 48)
        self.assertEqual(ffn.fc2.in_features, 48)

    def test_swiglu_shape_width_and_parameter_budget(self):
        torch.manual_seed(4)
        d_model = 24
        ffn = submission.FFN(d_model=d_model)
        swiglu = submission.SwiGLU(d_model=d_model)
        x = torch.randn(2, 5, d_model)
        y = swiglu(x)
        self.assertEqual(tuple(y.shape), (2, 5, d_model))
        self.assertEqual(swiglu.w1.out_features, int(d_model * 8 / 3))
        ffn_params = submission.count_params(ffn)
        swiglu_params = submission.count_params(swiglu)
        self.assertLess(abs(ffn_params - swiglu_params) / ffn_params, 0.08)

    def test_swiglu_hidden_size_matches_gelu_budget(self):
        d_model = 24
        self.assertEqual(submission.swiglu_hidden_size_for_param_budget(d_model), 64)

        counts = submission.ffn_parameter_counts(d_model)
        self.assertEqual(counts["gelu_hidden"], 96)
        self.assertEqual(counts["swiglu_hidden"], 64)
        self.assertEqual(counts["gelu_params"], 2 * 24 * 96)
        self.assertEqual(counts["swiglu_params"], 3 * 24 * 64)
        self.assertAlmostEqual(counts["ratio"], 1.0)

    def test_ffn_parameter_counts_reject_invalid_values(self):
        with self.assertRaises(ValueError):
            submission.swiglu_hidden_size_for_param_budget(0)
        with self.assertRaises(ValueError):
            submission.ffn_parameter_counts(8, gelu_hidden=-1)
        with self.assertRaises(ValueError):
            submission.ffn_parameter_counts(8, swiglu_hidden=0)


@unittest.skipIf(torch is None, "PyTorch is required for Ch05 block tests")
class TestTransformerBlock(unittest.TestCase):
    def test_block_shape_mask_and_gradient_flow(self):
        torch.manual_seed(5)
        block = submission.TransformerBlock(d_model=16, n_heads=4, d_ff=32, dropout=0.0)
        x = torch.randn(2, 6, 16, requires_grad=True)
        mask = torch.tril(torch.ones(6, 6, dtype=torch.bool))
        out = block(x, mask=mask)
        self.assertEqual(tuple(out.shape), (2, 6, 16))
        self.assertFalse(torch.allclose(out, x))

        loss = out.pow(2).mean()
        loss.backward()
        params = [p for p in block.parameters() if p.requires_grad]
        self.assertGreater(len(params), 0)
        self.assertTrue(all(p.grad is not None for p in params))
        self.assertIsNotNone(x.grad)

    def test_block_uses_pre_norm_components(self):
        block = submission.TransformerBlock(d_model=20, n_heads=5, d_ff=40, dropout=0.0)
        self.assertIsInstance(block.norm1, submission.RMSNorm)
        self.assertIsInstance(block.norm2, submission.RMSNorm)
        self.assertIsInstance(block.ffn, submission.SwiGLU)
        self.assertEqual(block.attention.n_heads, 5)


class TestBlockResourceEstimates(unittest.TestCase):
    def test_estimates_params_flops_and_activation_memory(self):
        result = submission.estimate_block_resources(
            batch_size=2,
            seq_len=4,
            d_model=8,
            n_heads=2,
            d_ff=16,
            dtype_bytes=2,
        )
        self.assertEqual(result["d_head"], 4)
        self.assertEqual(result["attention_params"], 4 * 8 * 8)
        self.assertEqual(result["swiglu_params"], 3 * 8 * 16)
        self.assertEqual(result["norm_params"], 16)
        self.assertEqual(result["total_params"], 256 + 384 + 16)
        self.assertEqual(result["qkv_flops"], 2 * 8 * 8 * 24)
        self.assertEqual(result["attention_score_flops"], 2 * 2 * 2 * 4 * 4 * 4)
        self.assertEqual(result["attention_value_flops"], 2 * 2 * 2 * 4 * 4 * 4)
        self.assertEqual(result["output_proj_flops"], 2 * 8 * 8 * 8)
        self.assertEqual(result["swiglu_flops"], 2 * 8 * 8 * 16 * 3)
        expected_scores_bytes = 2 * 2 * 4 * 4 * 2
        self.assertEqual(result["attention_scores_bytes"], expected_scores_bytes)
        self.assertGreater(result["activation_bytes"], expected_scores_bytes)

    def test_estimates_reject_invalid_shapes(self):
        with self.assertRaises(ValueError):
            submission.estimate_block_resources(1, 4, 7, 2)
        with self.assertRaises(ValueError):
            submission.estimate_block_resources(0, 4, 8, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
