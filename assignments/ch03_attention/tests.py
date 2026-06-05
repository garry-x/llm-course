"""Autograder-style tests for Chapter 3 attention exercises."""

import importlib
import math
import os
import unittest

try:
    import torch
    import torch.nn as nn
except ModuleNotFoundError:
    torch = None
    nn = None


MODULE_NAME = os.environ.get("STUDENT_MODULE", "reference_solution")
submission = importlib.import_module(MODULE_NAME) if torch is not None else None


@unittest.skipIf(torch is None, "PyTorch is required for Ch03 attention tests")
class TestQKVProjection(unittest.TestCase):
    def test_projection_shapes_and_parameters(self):
        torch.manual_seed(0)
        proj = submission.QKVProjection(d_model=12, d_k=5)
        self.assertIsInstance(proj, nn.Module)
        self.assertFalse(proj.W_q.bias is not None)
        self.assertEqual(sum(p.numel() for p in proj.parameters()), 3 * 12 * 5)

        x = torch.randn(2, 7, 12)
        Q, K, V = proj(x)
        self.assertEqual(tuple(Q.shape), (2, 7, 5))
        self.assertEqual(tuple(K.shape), (2, 7, 5))
        self.assertEqual(tuple(V.shape), (2, 7, 5))


@unittest.skipIf(torch is None, "PyTorch is required for Ch03 attention tests")
class TestScaledDotProductAttention(unittest.TestCase):
    def test_attention_matches_manual_computation(self):
        torch.manual_seed(1)
        Q = torch.randn(2, 4, 6)
        K = torch.randn(2, 4, 6)
        V = torch.randn(2, 4, 6)

        output, attn = submission.scaled_dot_product_attention(Q, K, V)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(6)
        expected_attn = torch.softmax(scores, dim=-1)
        expected_output = torch.matmul(expected_attn, V)

        self.assertTrue(torch.allclose(attn, expected_attn, atol=1e-6))
        self.assertTrue(torch.allclose(output, expected_output, atol=1e-6))
        self.assertTrue(torch.allclose(attn.sum(dim=-1), torch.ones(2, 4), atol=1e-6))

    def test_mask_blocks_positions_for_2d_and_3d_masks(self):
        torch.manual_seed(2)
        Q = torch.randn(2, 3, 4)
        K = torch.randn(2, 3, 4)
        V = torch.randn(2, 3, 4)
        mask_2d = torch.tensor(
            [[1, 0, 0], [1, 1, 0], [1, 1, 1]],
            dtype=torch.bool,
        )
        _, attn_2d = submission.scaled_dot_product_attention(Q, K, V, mask=mask_2d)
        self.assertTrue(torch.all(attn_2d[:, 0, 1:] < 1e-6))
        self.assertTrue(torch.all(attn_2d[:, 1, 2] < 1e-6))

        mask_3d = mask_2d.unsqueeze(0).expand(2, -1, -1).clone()
        mask_3d[1, 2, 0] = False
        _, attn_3d = submission.scaled_dot_product_attention(Q, K, V, mask=mask_3d)
        self.assertLess(attn_3d[1, 2, 0].item(), 1e-6)
        self.assertGreater(attn_3d[0, 2, 0].item(), 0.0)


@unittest.skipIf(torch is None, "PyTorch is required for Ch03 attention tests")
class TestCausalAttention(unittest.TestCase):
    def test_create_causal_mask(self):
        expected = torch.tensor(
            [
                [True, False, False, False],
                [True, True, False, False],
                [True, True, True, False],
                [True, True, True, True],
            ]
        )
        mask = submission.create_causal_mask(4)
        self.assertEqual(mask.dtype, torch.bool)
        self.assertTrue(torch.equal(mask, expected))

    def test_causal_attention_prevents_future_attention(self):
        torch.manual_seed(3)
        Q = torch.randn(1, 5, 8)
        K = torch.randn(1, 5, 8)
        V = torch.randn(1, 5, 8)
        output, attn = submission.causal_attention(Q, K, V)
        self.assertEqual(tuple(output.shape), (1, 5, 8))
        self.assertEqual(tuple(attn.shape), (1, 5, 5))

        future_mask = torch.triu(torch.ones(5, 5, dtype=torch.bool), diagonal=1)
        self.assertTrue(torch.all(attn[0][future_mask] < 1e-6))
        self.assertTrue(torch.allclose(attn.sum(dim=-1), torch.ones(1, 5), atol=1e-6))
        self.assertAlmostEqual(attn[0, 0, 0].item(), 1.0, places=6)


@unittest.skipIf(torch is None, "PyTorch is required for Ch03 attention tests")
class TestPlotAttention(unittest.TestCase):
    def test_plot_attention_returns_figure_and_axis(self):
        try:
            import matplotlib
        except ModuleNotFoundError:
            self.skipTest("matplotlib is required for plot_attention")

        matplotlib.use("Agg")
        tokens = ["<s>", "cat", "sat"]
        attn = torch.eye(3)
        fig, ax = submission.plot_attention(attn, tokens, title="Unit Test")
        self.assertEqual(ax.get_title(), "Unit Test")
        self.assertEqual(ax.get_xlabel(), "Key Position")
        self.assertEqual(ax.get_ylabel(), "Query Position")
        self.assertEqual([t.get_text() for t in ax.get_xticklabels()], tokens)
        fig.canvas.draw()


if __name__ == "__main__":
    unittest.main(verbosity=2)
