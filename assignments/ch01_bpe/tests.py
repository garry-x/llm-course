"""Autograder-style tests for Chapter 1 BPE tokenizer.

By default these tests run against reference_solution.py so the course
repository can verify that the test suite itself is healthy. To test a
learner submission in the same directory:

    STUDENT_MODULE=student_solution .venv/bin/python assignments/ch01_bpe/tests.py
"""

import importlib
import os
import unittest


MODULE_NAME = os.environ.get("STUDENT_MODULE", "reference_solution")
submission = importlib.import_module(MODULE_NAME)


class TestBPEHelpers(unittest.TestCase):
    def test_get_stats_counts_adjacent_pairs(self):
        ids = [1, 2, 1, 2, 3]
        self.assertEqual(
            submission._get_stats(ids),
            {(1, 2): 2, (2, 1): 1, (2, 3): 1},
        )

    def test_get_stats_handles_short_inputs(self):
        self.assertEqual(submission._get_stats([]), {})
        self.assertEqual(submission._get_stats([42]), {})

    def test_merge_replaces_non_overlapping_pairs(self):
        self.assertEqual(
            submission._merge([1, 2, 1, 2], (1, 2), 99),
            [99, 99],
        )
        self.assertEqual(
            submission._merge([1, 1, 1], (1, 1), 9),
            [9, 1],
        )

    def test_merge_preserves_unmatched_tokens(self):
        self.assertEqual(
            submission._merge([4, 1, 2, 5, 1], (1, 2), 99),
            [4, 99, 5, 1],
        )


class TestBPETokenizer(unittest.TestCase):
    def test_train_adds_contiguous_merges_and_vocab_entries(self):
        tokenizer = submission.BPETokenizer()
        tokenizer.train("low lower lowest", vocab_size=260)
        self.assertLessEqual(len(tokenizer.vocab), 260)
        self.assertTrue(all(idx >= 256 for idx in tokenizer.merges.values()))
        if tokenizer.merges:
            merge_ids = sorted(tokenizer.merges.values())
            self.assertEqual(merge_ids, list(range(256, 256 + len(merge_ids))))
            for pair, idx in tokenizer.merges.items():
                self.assertEqual(
                    tokenizer.vocab[idx],
                    tokenizer.vocab[pair[0]] + tokenizer.vocab[pair[1]],
                )

    def test_train_rejects_too_small_vocab(self):
        tokenizer = submission.BPETokenizer()
        with self.assertRaises(ValueError):
            tokenizer.train("hello", vocab_size=128)

    def test_encode_decode_round_trip_ascii_and_cjk(self):
        tokenizer = submission.BPETokenizer()
        corpus = "hello hello world globe globe"
        tokenizer.train(corpus, vocab_size=280)

        for text in ["hello world", "globe hello", "new unseen text"]:
            encoded = tokenizer.encode(text)
            self.assertIsInstance(encoded, list)
            self.assertTrue(all(isinstance(idx, int) for idx in encoded))
            self.assertEqual(tokenizer.decode(encoded), text)

    def test_encode_uses_learned_merge_ids(self):
        tokenizer = submission.BPETokenizer()
        tokenizer.train("aaaaaaaa", vocab_size=259)
        encoded = tokenizer.encode("aaaaaaaa")
        self.assertLess(len(encoded), len("aaaaaaaa".encode("utf-8")))
        self.assertTrue(any(idx >= 256 for idx in encoded))

    def test_decode_rejects_unknown_ids_by_key_error(self):
        tokenizer = submission.BPETokenizer()
        with self.assertRaises(KeyError):
            tokenizer.decode([999999])


class TestTokenizerReport(unittest.TestCase):
    def test_tokenizer_report_counts_lengths_round_trip_and_embedding_budget(self):
        tokenizer = submission.BPETokenizer()
        texts = ["hello hello", "world", "emoji 😊", "x = a + b"]
        tokenizer.train(" ".join(texts), vocab_size=280)
        report = submission.tokenizer_report(tokenizer, texts, vocab_size=280, d_model=16)

        lengths = [len(tokenizer.encode(text)) for text in texts]
        self.assertEqual(report["num_texts"], 4)
        self.assertEqual(report["total_tokens"], sum(lengths))
        self.assertAlmostEqual(report["avg_tokens"], sum(lengths) / 4)
        self.assertEqual(report["p95_tokens"], sorted(lengths)[-1])
        self.assertAlmostEqual(report["tokens_per_character"], sum(lengths) / sum(len(text) for text in texts))
        self.assertEqual(report["round_trip_success_rate"], 1.0)
        self.assertEqual(report["embedding_params"], 280 * 16)

    def test_tokenizer_report_rejects_empty_texts(self):
        tokenizer = submission.BPETokenizer()
        with self.assertRaises(ValueError):
            submission.tokenizer_report(tokenizer, [])

    def test_tokenizer_group_report_compares_language_or_domain_costs(self):
        tokenizer = submission.BPETokenizer()
        groups = {
            "english": ["hello world", "lower cost"],
            "cjk": ["world hello", "language model"],
            "code": ["x = a + b", "def f(x): return x"],
        }
        tokenizer.train(" ".join(text for texts in groups.values() for text in texts), vocab_size=280)
        report = submission.tokenizer_group_report(tokenizer, groups, vocab_size=280, d_model=16)

        self.assertEqual(set(report["groups"]), set(groups))
        for name, texts in groups.items():
            expected = submission.tokenizer_report(tokenizer, texts, vocab_size=280, d_model=16)
            self.assertEqual(report["groups"][name]["total_tokens"], expected["total_tokens"])
            self.assertEqual(report["groups"][name]["embedding_params"], 280 * 16)

        rates = {
            name: group_report["tokens_per_character"]
            for name, group_report in report["groups"].items()
        }
        max_group = max(rates, key=rates.get)
        min_group = min(rates, key=rates.get)
        self.assertEqual(report["max_tokens_per_character_group"], max_group)
        self.assertEqual(report["min_tokens_per_character_group"], min_group)
        self.assertAlmostEqual(report["tokens_per_character_disparity"], rates[max_group] / rates[min_group])

    def test_tokenizer_group_report_rejects_empty_groups(self):
        tokenizer = submission.BPETokenizer()
        with self.assertRaises(ValueError):
            submission.tokenizer_group_report(tokenizer, {})
        with self.assertRaises(ValueError):
            submission.tokenizer_group_report(tokenizer, {"empty": []})


class TestBPETrainingTrace(unittest.TestCase):
    def test_bpe_training_trace_reports_pair_counts_and_token_savings(self):
        trace = submission.bpe_training_trace("abababa", vocab_size=258)
        self.assertEqual(trace["initial_length"], 7)
        self.assertEqual(trace["final_length"], 3)
        self.assertEqual(trace["total_tokens_saved"], 4)
        self.assertAlmostEqual(trace["compression_ratio"], 3 / 7)
        self.assertEqual(trace["final_ids"], [257, 256, ord("a")])

        first, second = trace["steps"]
        self.assertEqual(first["step"], 0)
        self.assertEqual(first["pair"], (ord("a"), ord("b")))
        self.assertEqual(first["count"], 3)
        self.assertEqual(first["new_id"], 256)
        self.assertEqual(first["token_bytes"], b"ab")
        self.assertEqual(first["token_text"], "ab")
        self.assertEqual(first["before_length"], 7)
        self.assertEqual(first["after_length"], 4)
        self.assertEqual(first["tokens_saved"], 3)

        self.assertEqual(second["pair"], (256, 256))
        self.assertEqual(second["count"], 2)
        self.assertEqual(second["new_id"], 257)
        self.assertEqual(second["token_bytes"], b"abab")
        self.assertEqual(second["before_length"], 4)
        self.assertEqual(second["after_length"], 3)
        self.assertEqual(second["tokens_saved"], 1)

    def test_bpe_training_trace_limits_steps_and_rejects_bad_inputs(self):
        trace = submission.bpe_training_trace("abababa", vocab_size=300, max_steps=1)
        self.assertEqual(len(trace["steps"]), 1)
        self.assertEqual(trace["final_length"], 4)

        with self.assertRaises(ValueError):
            submission.bpe_training_trace("abc", vocab_size=128)
        with self.assertRaises(ValueError):
            submission.bpe_training_trace("abc", vocab_size=260, max_steps=0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
