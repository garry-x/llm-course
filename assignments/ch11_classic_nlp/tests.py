import importlib
import math
import os
import unittest


MODULE_NAME = os.environ.get("STUDENT_MODULE", "reference_solution")
solution = importlib.import_module(MODULE_NAME)


class TestDependencyParsingMetrics(unittest.TestCase):
    def test_uas_las_counts_heads_and_labels(self):
        gold_heads = [1, -1, 1, 2]
        gold_labels = ["nsubj", "root", "obj", "advmod"]
        pred_heads = [1, -1, 2, 2]
        pred_labels = ["nsubj", "root", "obj", "case"]
        scores = solution.attachment_scores(gold_heads, gold_labels, pred_heads, pred_labels)
        self.assertEqual(scores["total"], 4)
        self.assertEqual(scores["correct_heads"], 3)
        self.assertEqual(scores["correct_labels"], 2)
        self.assertAlmostEqual(scores["uas"], 0.75)
        self.assertAlmostEqual(scores["las"], 0.5)

    def test_rejects_length_mismatch_and_empty_sentence(self):
        with self.assertRaises(ValueError):
            solution.attachment_scores([0], ["root"], [0, 1], ["root"])
        with self.assertRaises(ValueError):
            solution.attachment_scores([], [], [], [])


class TestRNNFoundations(unittest.TestCase):
    def test_scalar_rnn_forward_matches_manual_tanh_recurrence(self):
        states = solution.scalar_rnn_forward([1.0, 0.5, -1.0], w_xh=0.8, w_hh=0.4, h0=0.0)
        h1 = math.tanh(0.8)
        h2 = math.tanh(0.8 * 0.5 + 0.4 * h1)
        h3 = math.tanh(0.8 * -1.0 + 0.4 * h2)
        self.assertEqual(len(states), 3)
        self.assertAlmostEqual(states[0], h1)
        self.assertAlmostEqual(states[1], h2)
        self.assertAlmostEqual(states[2], h3)

    def test_recurrent_gradient_factors_show_vanishing_path(self):
        states = [0.0, 0.5, 0.9]
        factors = solution.recurrent_gradient_factors(states, w_hh=0.8)
        self.assertEqual(len(factors), 3)
        self.assertAlmostEqual(factors[0], 0.8)
        self.assertAlmostEqual(factors[1], 0.8 * (1 - 0.25))
        self.assertAlmostEqual(factors[2], 0.8 * (1 - 0.81))
        product = math.prod(factors)
        self.assertLess(product, factors[0])


class TestBleuRougeEvaluation(unittest.TestCase):
    def test_sentence_bleu_exact_match_is_one(self):
        candidate = "the cat sat on the mat".split()
        references = [candidate, "a cat is on the mat".split()]
        self.assertAlmostEqual(solution.sentence_bleu(candidate, references), 1.0)

    def test_sentence_bleu_uses_clipping_and_brevity_penalty(self):
        candidate = "the the the the".split()
        references = ["the cat is here".split()]
        score = solution.sentence_bleu(candidate, references, max_n=1)
        self.assertAlmostEqual(score, 0.25)

        short_candidate = "cat sat".split()
        reference = ["cat sat on mat".split()]
        short_score = solution.sentence_bleu(short_candidate, reference, max_n=1)
        self.assertAlmostEqual(short_score, math.exp(1 - 4 / 2))

    def test_sentence_bleu_returns_zero_for_missing_higher_order_ngrams(self):
        candidate = "the dog".split()
        references = ["the cat".split()]
        self.assertEqual(solution.sentence_bleu(candidate, references, max_n=2), 0.0)

    def test_rouge_l_f1_uses_lcs(self):
        candidate = "a b c d".split()
        reference = "a x b c".split()
        scores = solution.rouge_l_f1(candidate, reference)
        self.assertEqual(scores["lcs"], 3)
        self.assertAlmostEqual(scores["precision"], 0.75)
        self.assertAlmostEqual(scores["recall"], 0.75)
        self.assertAlmostEqual(scores["f1"], 0.75)

    def test_rouge_l_empty_inputs(self):
        self.assertEqual(solution.rouge_l_f1([], ["a"])["f1"], 0.0)
        self.assertEqual(solution.rouge_l_f1(["a"], [])["f1"], 0.0)


class TestQAMetricsAndMLM(unittest.TestCase):
    def test_normalize_answer(self):
        self.assertEqual(solution.normalize_answer("The, Quick!  Brown fox."), "quick brown fox")
        self.assertEqual(solution.normalize_answer("An answer"), "answer")

    def test_exact_match_and_f1_uses_best_gold_answer(self):
        scores = solution.exact_match_and_f1(
            "The quick brown fox",
            ["quick brown fox", "slow turtle"],
        )
        self.assertEqual(scores["exact_match"], 1)
        self.assertAlmostEqual(scores["f1"], 1.0)

        partial = solution.exact_match_and_f1("quick fox", ["quick brown fox"])
        self.assertEqual(partial["exact_match"], 0)
        self.assertAlmostEqual(partial["f1"], 0.8)

    def test_build_mlm_example_masks_positions_and_labels_original_tokens(self):
        tokens = ["[CLS]", "the", "cat", "sat", "[SEP]"]
        masked, labels = solution.build_mlm_example(tokens, [2, 3])
        self.assertEqual(masked, ["[CLS]", "the", "[MASK]", "[MASK]", "[SEP]"])
        self.assertEqual(labels, [None, None, "cat", "sat", None])
        self.assertEqual(tokens, ["[CLS]", "the", "cat", "sat", "[SEP]"])

    def test_build_mlm_example_rejects_invalid_positions(self):
        with self.assertRaises(IndexError):
            solution.build_mlm_example(["a"], [1])
        with self.assertRaises(ValueError):
            solution.build_mlm_example(["a", "b"], [1, 1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
