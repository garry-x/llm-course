"""Autograder-style tests for Chapter 2 embedding and RoPE exercises."""

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


@unittest.skipIf(torch is None, "PyTorch is required for Ch02 embedding tests")
class TestTokenEmbedding(unittest.TestCase):
    def test_shape_parameter_count_and_scaling(self):
        torch.manual_seed(0)
        emb = submission.TokenEmbedding(vocab_size=11, d_model=6)
        self.assertIsInstance(emb, nn.Module)
        self.assertEqual(sum(p.numel() for p in emb.parameters()), 66)

        x = torch.tensor([[0, 1, 2], [3, 4, 5]])
        out = emb(x)
        self.assertEqual(tuple(out.shape), (2, 3, 6))

        weight = emb.embed.weight.detach()
        expected = weight[x] * math.sqrt(6)
        self.assertTrue(torch.allclose(out.detach(), expected, atol=1e-6))


@unittest.skipIf(torch is None, "PyTorch is required for Ch02 embedding tests")
class TestWordVectorObjectives(unittest.TestCase):
    def test_cooccurrence_matrix_counts_directed_window_context(self):
        ids = [0, 1, 2, 1]
        counts = submission.build_cooccurrence_matrix(ids, vocab_size=3, window_size=1)
        expected = torch.tensor(
            [
                [0, 1, 0],
                [1, 0, 2],
                [0, 2, 0],
            ],
            dtype=torch.long,
        )
        self.assertTrue(torch.equal(counts, expected))

    def test_cooccurrence_matrix_rejects_invalid_inputs(self):
        with self.assertRaises(ValueError):
            submission.build_cooccurrence_matrix([0], vocab_size=0, window_size=1)
        with self.assertRaises(ValueError):
            submission.build_cooccurrence_matrix([0], vocab_size=1, window_size=0)
        with self.assertRaises(ValueError):
            submission.build_cooccurrence_matrix([2], vocab_size=2, window_size=1)

    def test_skipgram_negative_sampling_loss_matches_manual_formula(self):
        center = torch.tensor([[1.0, 0.0], [0.5, 0.5]])
        positive = torch.tensor([[0.5, 0.0], [0.25, 0.75]])
        negative = torch.tensor(
            [
                [[-1.0, 0.0], [0.0, -1.0]],
                [[-0.5, 0.0], [0.0, -0.5]],
            ]
        )
        loss = submission.skipgram_negative_sampling_loss(center, positive, negative)
        positive_logits = torch.tensor([0.5, 0.5])
        negative_logits = torch.tensor([[-1.0, 0.0], [-0.25, -0.25]])
        expected = (
            -torch.nn.functional.logsigmoid(positive_logits)
            - torch.nn.functional.logsigmoid(-negative_logits).sum(dim=-1)
        ).mean()
        self.assertTrue(torch.allclose(loss, expected, atol=1e-6))

    def test_skipgram_negative_sampling_loss_rejects_bad_shapes(self):
        with self.assertRaises(ValueError):
            submission.skipgram_negative_sampling_loss(torch.randn(2), torch.randn(2), torch.randn(1, 1, 2))
        with self.assertRaises(ValueError):
            submission.skipgram_negative_sampling_loss(torch.randn(2, 3), torch.randn(2, 3), torch.randn(2, 4))


@unittest.skipIf(torch is None, "PyTorch is required for Ch02 embedding tests")
class TestSinusoidalEncoding(unittest.TestCase):
    def test_buffer_no_trainable_parameters_and_shape(self):
        pe = submission.SinusoidalEncoding(d_model=8, max_len=16)
        self.assertEqual(sum(p.numel() for p in pe.parameters()), 0)
        self.assertIn("pe", dict(pe.named_buffers()))
        self.assertEqual(tuple(pe.pe.shape), (1, 16, 8))

        x = torch.zeros(2, 5, 8)
        out = pe(x)
        self.assertEqual(tuple(out.shape), (2, 5, 8))
        self.assertTrue(torch.allclose(out[0], out[1]))

    def test_position_zero_and_known_frequency_values(self):
        pe = submission.SinusoidalEncoding(d_model=8, max_len=4)
        row0 = pe.pe[0, 0]
        self.assertTrue(torch.allclose(row0[0::2], torch.zeros(4), atol=1e-7))
        self.assertTrue(torch.allclose(row0[1::2], torch.ones(4), atol=1e-7))

        div_term = math.exp(2 * (-math.log(10000.0) / 8))
        self.assertAlmostEqual(pe.pe[0, 1, 2].item(), math.sin(div_term), places=6)
        self.assertAlmostEqual(pe.pe[0, 1, 3].item(), math.cos(div_term), places=6)


@unittest.skipIf(torch is None, "PyTorch is required for Ch02 embedding tests")
class TestRoPE(unittest.TestCase):
    def test_rotate_half(self):
        rope = submission.RoPE(d_model=4, max_len=4)
        x = torch.tensor([[[[1.0, 2.0, 3.0, 4.0]]]])
        expected = torch.tensor([[[[-3.0, -4.0, 1.0, 2.0]]]])
        self.assertTrue(torch.allclose(rope._rotate_half(x), expected))

    def test_shape_and_norm_preservation(self):
        torch.manual_seed(0)
        rope = submission.RoPE(d_model=8, max_len=16)
        q = torch.randn(2, 3, 5, 8)
        k = torch.randn(2, 3, 5, 8)
        q_rot, k_rot = rope(q, k)
        self.assertEqual(tuple(q_rot.shape), tuple(q.shape))
        self.assertEqual(tuple(k_rot.shape), tuple(k.shape))
        self.assertTrue(torch.allclose(q.norm(dim=-1), q_rot.norm(dim=-1), atol=1e-5))
        self.assertTrue(torch.allclose(k.norm(dim=-1), k_rot.norm(dim=-1), atol=1e-5))

    def test_position_zero_is_identity(self):
        rope = submission.RoPE(d_model=8, max_len=4)
        q = torch.randn(1, 1, 1, 8)
        q_rot, _ = rope(q, q)
        self.assertTrue(torch.allclose(q_rot, q, atol=1e-6))

    def test_relative_position_scores_are_toeplitz(self):
        scores = submission.verify_rope_relative_property(d_model=16, seq_len=6)
        self.assertEqual(tuple(scores.shape), (6, 6))
        for offset in range(-5, 6):
            diag = scores.diagonal(offset=offset)
            if diag.numel() > 1:
                self.assertTrue(torch.allclose(diag, diag[0].expand_as(diag), atol=1e-5))

    def test_rejects_odd_dimensions(self):
        with self.assertRaises(ValueError):
            submission.RoPE(d_model=7)


if __name__ == "__main__":
    unittest.main(verbosity=2)
