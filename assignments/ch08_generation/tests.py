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


class BeamToyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.anchor = nn.Parameter(torch.zeros(()))
        self.vocab_size = 4
        self.tokenizer = type("Tok", (), {"eos_token_id": 3})()

    def forward(self, input_ids):
        batch, seq = input_ids.shape
        logits = torch.full((batch, seq, self.vocab_size), -20.0, device=input_ids.device)
        last = int(input_ids[0, -1].item())
        if seq == 1:
            logits[:, -1, 1] = 3.0
            logits[:, -1, 3] = 2.8
        elif last == 1:
            logits[:, -1, 2] = 3.0
            logits[:, -1, 3] = 1.0
        elif last == 2:
            logits[:, -1, 3] = 3.0
        else:
            logits[:, -1, 3] = 3.0
        return logits + self.anchor


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

    def test_repetition_penalty_adjusts_seen_logits_by_sign(self):
        logits = torch.tensor([[2.0, -1.0, 0.5, 3.0]])
        original = logits.clone()
        generated_ids = torch.tensor([[0, 1, 1]])
        adjusted = submission.apply_repetition_penalty(logits, generated_ids, penalty=2.0)
        expected = torch.tensor([[1.0, -2.0, 0.5, 3.0]])
        self.assertTrue(torch.allclose(adjusted, expected))
        self.assertTrue(torch.allclose(logits, original))

    def test_sample_next_token_applies_repetition_penalty_before_greedy(self):
        logits = torch.tensor([[4.0, 3.5, 1.0]])
        generated_ids = torch.tensor([[0]])
        token = submission.sample_next_token(
            logits,
            strategy="greedy",
            generated_ids=generated_ids,
            repetition_penalty=2.0,
        )
        self.assertEqual(token.item(), 1)

    def test_invalid_sampling_hyperparameters_raise(self):
        logits = torch.tensor([[1.0, 2.0]])
        with self.assertRaises(ValueError):
            submission.sample_next_token(logits, strategy="temperature", temperature=-1.0)
        with self.assertRaises(ValueError):
            submission.sample_next_token(logits, strategy="top-k", k=0)
        with self.assertRaises(ValueError):
            submission.sample_next_token(logits, strategy="top-p", p=0.0)
        with self.assertRaises(ValueError):
            submission.apply_repetition_penalty(logits, torch.tensor([[0]]), penalty=0.0)
        with self.assertRaises(ValueError):
            submission.apply_repetition_penalty(logits, torch.tensor([[0], [1]]), penalty=1.2)
        with self.assertRaises(ValueError):
            submission.apply_repetition_penalty(logits, torch.tensor([[2]]), penalty=1.2)


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
class TestBeamSearch(unittest.TestCase):
    def test_length_normalized_score_penalizes_shorter_or_longer_outputs_by_alpha(self):
        self.assertAlmostEqual(submission.length_normalized_score(-3.0, length=3, alpha=1.0), -1.0)
        self.assertAlmostEqual(submission.length_normalized_score(-3.0, length=3, alpha=0.0), -3.0)
        with self.assertRaises(ValueError):
            submission.length_normalized_score(-1.0, length=0)
        with self.assertRaises(ValueError):
            submission.length_normalized_score(-1.0, length=1, alpha=-0.5)

    def test_pass_at_k_estimates_success_probability(self):
        self.assertEqual(submission.pass_at_k(num_samples=10, num_correct=0, k=3), 0.0)
        self.assertEqual(submission.pass_at_k(num_samples=10, num_correct=8, k=3), 1.0)
        expected = 1.0 - (8 / 10) * (7 / 9) * (6 / 8)
        self.assertAlmostEqual(submission.pass_at_k(num_samples=10, num_correct=2, k=3), expected)
        self.assertAlmostEqual(submission.pass_at_k(num_samples=10, num_correct=2, k=1), 0.2)

    def test_pass_at_k_rejects_invalid_counts(self):
        with self.assertRaises(ValueError):
            submission.pass_at_k(0, 0, 1)
        with self.assertRaises(ValueError):
            submission.pass_at_k(5, 6, 1)
        with self.assertRaises(ValueError):
            submission.pass_at_k(5, 1, 0)
        with self.assertRaises(ValueError):
            submission.pass_at_k(5, 1, 6)

    def test_self_consistency_vote_aggregates_extracted_answers_and_cost(self):
        outputs = [
            "path one\nanswer=42",
            "path two\nanswer=41",
            "path three\nanswer=42",
        ]

        def extract_answer(text):
            return text.rsplit("=", 1)[-1]

        report = submission.self_consistency_vote(
            outputs,
            answer_extractor=extract_answer,
            token_counts=[12, 15, 18],
        )
        self.assertEqual(report["answer"], "42")
        self.assertEqual(report["count"], 2)
        self.assertEqual(report["num_samples"], 3)
        self.assertAlmostEqual(report["vote_fraction"], 2 / 3)
        self.assertEqual(report["answers"], ["42", "41", "42"])
        self.assertEqual(report["vote_counts"], [("42", 2), ("41", 1)])
        self.assertEqual(report["total_tokens"], 45)
        self.assertEqual(report["mean_tokens"], 15)

    def test_self_consistency_vote_ties_use_first_seen_answer(self):
        report = submission.self_consistency_vote(["A", "B", "B", "A"])
        self.assertEqual(report["answer"], "A")
        self.assertEqual(report["vote_counts"], [("A", 2), ("B", 2)])

    def test_self_consistency_vote_rejects_bad_inputs(self):
        with self.assertRaises(ValueError):
            submission.self_consistency_vote([])
        with self.assertRaises(ValueError):
            submission.self_consistency_vote(["A"], token_counts=[1, 2])
        with self.assertRaises(ValueError):
            submission.self_consistency_vote(["A"], token_counts=[-1])

    def test_beam_search_keeps_multiple_candidates_and_reports_scores(self):
        model = BeamToyModel()
        prompt = torch.tensor([[0]])
        best, table = submission.beam_search(
            model,
            prompt,
            max_new_tokens=3,
            num_beams=2,
            eos_token_id=3,
            length_penalty_alpha=0.0,
        )
        self.assertEqual(best.tolist(), [[0, 1, 2, 3]])
        self.assertEqual(len(table), 2)
        self.assertTrue(all("normalized_score" in item for item in table))
        self.assertTrue(any(item["tokens"] == [0, 3] for item in table))

    def test_beam_search_rejects_unsupported_shapes(self):
        model = BeamToyModel()
        with self.assertRaises(ValueError):
            submission.beam_search(model, torch.tensor([[0], [0]]))
        with self.assertRaises(ValueError):
            submission.beam_search(model, torch.tensor([[0]]), num_beams=0)


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
