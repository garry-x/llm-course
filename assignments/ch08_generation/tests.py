"""Autograder-style tests for Chapter 8 text-generation exercises."""

import importlib
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


class ScriptedModel(nn.Module):
    def __init__(self, vocab_size=6, eos_token_id=None):
        super().__init__()
        self.anchor = nn.Parameter(torch.zeros(()))
        self.vocab_size = vocab_size
        self.tokenizer = type("Tok", (), {"eos_token_id": eos_token_id})() if eos_token_id is not None else None

    def forward(self, input_ids):
        batch, seq = input_ids.shape
        logits = torch.full((batch, seq, self.vocab_size), -10.0, device=input_ids.device)
        next_id = min(seq, self.vocab_size - 1)
        logits[:, -1, next_id] = 10.0
        return logits + self.anchor


class TinyTokenizer:
    eos_token_id = None

    def __init__(self):
        self.stoi = {"a": 0, "b": 1, "c": 2, "d": 3}
        self.itos = {v: k for k, v in self.stoi.items()}

    def encode(self, text, return_tensors=None):
        ids = [self.stoi[ch] for ch in text]
        if return_tensors == "pt":
            return torch.tensor([ids], dtype=torch.long)
        return ids

    def decode(self, ids):
        return "".join(self.itos.get(int(i), "?") for i in ids)


@unittest.skipIf(torch is None, "PyTorch is required for Ch08 generation tests")
class TestSampling(unittest.TestCase):
    def test_greedy_uses_last_position_argmax(self):
        model = ScriptedModel(vocab_size=6)
        prompt = torch.tensor([[0, 1]])
        out = submission.generate_greedy(model, prompt, max_new_tokens=3)
        self.assertEqual(out.tolist(), [[0, 1, 2, 3, 4]])

    def test_temperature_zero_degenerates_to_argmax(self):
        logits = torch.tensor([[0.0, 4.0, 2.0]])
        token = submission.sample_next_token(logits, strategy="temperature", temperature=0)
        self.assertEqual(token.item(), 1)

    def test_topk_never_samples_outside_k_and_clamps_large_k(self):
        torch.manual_seed(0)
        logits = torch.tensor([[10.0, 9.0, -100.0, -100.0]])
        seen = set()
        for _ in range(50):
            token = submission.sample_next_token(logits, strategy="top-k", temperature=1.0, k=2)
            seen.add(token.item())
        self.assertTrue(seen.issubset({0, 1}))
        token = submission.sample_next_token(logits, strategy="top-k", temperature=1.0, k=99)
        self.assertIn(token.item(), {0, 1})

    def test_top_p_filter_keeps_minimal_nucleus(self):
        logits = torch.log(torch.tensor([[0.50, 0.30, 0.20]]))
        filtered = submission.top_p_filter(logits, p=0.5)
        kept = torch.isfinite(filtered)
        self.assertEqual(kept.tolist(), [[True, False, False]])

        filtered = submission.top_p_filter(logits, p=0.51)
        kept = torch.isfinite(filtered)
        self.assertEqual(kept.tolist(), [[True, True, False]])

    def test_invalid_sampling_hyperparameters_raise(self):
        logits = torch.tensor([[1.0, 2.0]])
        with self.assertRaises(ValueError):
            submission.sample_next_token(logits, strategy="temperature", temperature=-1.0)
        with self.assertRaises(ValueError):
            submission.sample_next_token(logits, strategy="top-k", k=0)
        with self.assertRaises(ValueError):
            submission.sample_next_token(logits, strategy="top-p", p=0.0)


@unittest.skipIf(torch is None, "PyTorch is required for Ch08 generation tests")
class TestGenerator(unittest.TestCase):
    def test_generator_decodes_and_distinct_ngrams(self):
        model = ScriptedModel(vocab_size=4)
        tokenizer = TinyTokenizer()
        generator = submission.Generator(model, tokenizer)
        text = generator.generate("ab", strategy="greedy", max_new_tokens=2)
        self.assertEqual(text, "abcd")
        self.assertAlmostEqual(generator.distinct_ngrams("a b a b", n=2), 2 / 3)
        self.assertEqual(generator.distinct_ngrams("a", n=2), 0.0)


@unittest.skipIf(torch is None, "PyTorch is required for Ch08 generation tests")
class TestSpeculativeDecoding(unittest.TestCase):
    def test_speculative_decoding_returns_stats_and_respects_budget(self):
        torch.manual_seed(1)
        target = ScriptedModel(vocab_size=8)
        draft = ScriptedModel(vocab_size=8)
        prompt = torch.tensor([[0, 1]])
        out, stats = submission.speculative_decoding(
            target, draft, prompt, gamma=3, max_new_tokens=5
        )
        self.assertEqual(tuple(out.shape), (1, 7))
        self.assertLessEqual(stats["accepted"], stats["proposed"])
        self.assertGreater(stats["proposed"], 0)
        self.assertGreaterEqual(stats["acceptance_rate"], 0.0)
        self.assertLessEqual(stats["acceptance_rate"], 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
