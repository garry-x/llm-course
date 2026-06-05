"""Autograder-style tests for Chapter 7 training-loop exercises."""

import importlib
import math
import os
import tempfile
import unittest

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ModuleNotFoundError:
    torch = None
    nn = None
    F = None


MODULE_NAME = os.environ.get("STUDENT_MODULE", "reference_solution")
submission = importlib.import_module(MODULE_NAME) if torch is not None else None


class CharTokenizer:
    def __init__(self, alphabet):
        self.stoi = {ch: i for i, ch in enumerate(alphabet)}

    def encode(self, text):
        return [self.stoi[ch] for ch in text]


@unittest.skipIf(torch is None, "PyTorch is required for Ch07 training tests")
class TestTextDataset(unittest.TestCase):
    def test_dataset_returns_shifted_equal_length_chunks(self):
        tokenizer = CharTokenizer("abcdefghijklmnopqrstuvwxyz")
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
            f.write("abcdefghij")
            path = f.name
        try:
            dataset = submission.TextDataset(path, tokenizer, block_size=4)
            self.assertEqual(len(dataset), 2)
            x0, y0 = dataset[0]
            x1, y1 = dataset[1]
            self.assertEqual(x0.tolist(), [0, 1, 2, 3])
            self.assertEqual(y0.tolist(), [1, 2, 3, 4])
            self.assertEqual(x1.tolist(), [4, 5, 6, 7])
            self.assertEqual(y1.tolist(), [5, 6, 7, 8])
            self.assertEqual(tuple(x0.shape), tuple(y0.shape))
        finally:
            os.unlink(path)

    def test_create_dataloader_batches(self):
        tokenizer = CharTokenizer("abcdefghijklmnopqrstuvwxyz")
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
            f.write("abcdefghijklmnopq")
            path = f.name
        try:
            loader = submission.create_dataloader(
                path, tokenizer, batch_size=2, block_size=4, shuffle=False, num_workers=0
            )
            x, y = next(iter(loader))
            self.assertEqual(tuple(x.shape), (2, 4))
            self.assertEqual(tuple(y.shape), (2, 4))
        finally:
            os.unlink(path)


@unittest.skipIf(torch is None, "PyTorch is required for Ch07 training tests")
class TestDataDiagnostics(unittest.TestCase):
    def test_ngram_repetition_rate_counts_repeated_occurrences(self):
        tokens = [1, 2, 3, 1, 2, 3, 1, 2]
        self.assertAlmostEqual(submission.ngram_repetition_rate(tokens, n=3), 3 / 6)
        self.assertEqual(submission.ngram_repetition_rate([1, 2], n=3), 0.0)

    def test_ngram_overlap_rate_measures_eval_leakage(self):
        train = [10, 11, 12, 13, 20, 21, 22]
        eval_tokens = [0, 10, 11, 12, 1, 20, 21, 22]
        self.assertAlmostEqual(submission.ngram_overlap_rate(train, eval_tokens, n=3), 2 / 6)
        self.assertEqual(submission.ngram_overlap_rate([], eval_tokens, n=3), 0.0)
        self.assertEqual(submission.ngram_overlap_rate(train, [1, 2], n=3), 0.0)

    def test_ngram_diagnostics_reject_invalid_n(self):
        with self.assertRaises(ValueError):
            submission.ngram_repetition_rate([1, 2, 3], n=0)
        with self.assertRaises(ValueError):
            submission.ngram_overlap_rate([1, 2, 3], [1, 2, 3], n=0)


@unittest.skipIf(torch is None, "PyTorch is required for Ch07 training tests")
class TestTrainingBudget(unittest.TestCase):
    def test_global_batch_tokens_and_steps_match_token_budget(self):
        global_tokens = submission.global_batch_tokens(
            micro_batch_size=4,
            seq_len=2048,
            grad_accum_steps=8,
            data_parallel_size=16,
        )
        self.assertEqual(global_tokens, 1_048_576)
        self.assertEqual(
            submission.training_steps_for_token_budget(20_000_000_000, global_tokens),
            19_074,
        )

    def test_dense_lm_training_flops_uses_six_nd_rule(self):
        self.assertEqual(
            submission.dense_lm_training_flops(num_params=1_000_000_000, train_tokens=20_000_000_000),
            120_000_000_000_000_000_000,
        )

    def test_training_budget_rejects_non_positive_values(self):
        with self.assertRaises(ValueError):
            submission.global_batch_tokens(0, 2048)
        with self.assertRaises(ValueError):
            submission.training_steps_for_token_budget(1000, 0)
        with self.assertRaises(ValueError):
            submission.dense_lm_training_flops(0, 1000)


@unittest.skipIf(torch is None, "PyTorch is required for Ch07 training tests")
class TestLossOptimizerScheduler(unittest.TestCase):
    def test_cross_entropy_matches_pytorch_for_large_logits(self):
        torch.manual_seed(0)
        logits = torch.randn(3, 5, 11) * 20.0
        targets = torch.randint(0, 11, (3, 5))
        manual = submission.cross_entropy_manual(logits, targets)
        reference = F.cross_entropy(logits.reshape(-1, 11), targets.reshape(-1))
        self.assertTrue(torch.allclose(manual, reference, atol=1e-5, rtol=1e-5))

    def test_cross_entropy_logits_gradient_matches_autograd(self):
        torch.manual_seed(3)
        logits = torch.randn(2, 4, 7, dtype=torch.float64, requires_grad=True)
        targets = torch.tensor([[1, 2, -100, 4], [0, -100, 3, 6]])
        loss = F.cross_entropy(logits.reshape(-1, 7), targets.reshape(-1), ignore_index=-100)
        loss.backward()

        manual = submission.cross_entropy_logits_gradient(logits.detach(), targets, ignore_index=-100)
        self.assertTrue(torch.allclose(manual, logits.grad, atol=1e-10, rtol=1e-10))
        self.assertTrue(torch.all(manual[targets == -100] == 0.0))

    def test_cross_entropy_logits_gradient_rejects_bad_inputs(self):
        with self.assertRaises(ValueError):
            submission.cross_entropy_logits_gradient(torch.randn(2, 3), torch.ones(2, dtype=torch.long))
        with self.assertRaises(ValueError):
            submission.cross_entropy_logits_gradient(torch.randn(2, 3, 4), torch.ones(2, 2, dtype=torch.long))
        with self.assertRaises(ValueError):
            submission.cross_entropy_logits_gradient(torch.randn(1, 1, 4), torch.tensor([[9]]))
        with self.assertRaises(ValueError):
            submission.cross_entropy_logits_gradient(torch.randn(1, 2, 4), torch.tensor([[-100, -100]]), ignore_index=-100)

    def test_adamw_single_step_matches_expected_update(self):
        p = torch.nn.Parameter(torch.tensor([1.0, -2.0]))
        p.grad = torch.tensor([0.1, -0.2])
        opt = submission.AdamW([p], lr=0.01, betas=(0.9, 0.99), eps=1e-8, weight_decay=0.1)
        opt.step()
        expected = torch.tensor([1.0, -2.0]) * (1 - 0.01 * 0.1)
        expected = expected - 0.01 * torch.tensor([1.0, -1.0])
        self.assertTrue(torch.allclose(p.detach(), expected, atol=1e-6))

    def test_scheduler_warmup_cosine_boundaries(self):
        param = torch.nn.Parameter(torch.tensor([1.0]))
        optimizer = torch.optim.SGD([param], lr=0.2)
        scheduler = submission.get_cosine_schedule_with_warmup(
            optimizer, num_warmup_steps=2, num_training_steps=6, min_lr_ratio=0.25
        )
        factors = [scheduler.lr_lambdas[0](step) for step in range(7)]
        self.assertAlmostEqual(factors[0], 0.0)
        self.assertAlmostEqual(factors[1], 0.5)
        self.assertAlmostEqual(factors[2], 1.0)
        self.assertAlmostEqual(factors[6], 0.25)
        self.assertTrue(all(0.25 <= value <= 1.0 for value in factors[2:]))


class TinyLanguageModel(nn.Module):
    def __init__(self, vocab_size=8, d_model=12):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.proj = nn.Linear(d_model, vocab_size)

    def forward(self, input_ids):
        return self.proj(self.embedding(input_ids))


@unittest.skipIf(torch is None, "PyTorch is required for Ch07 training tests")
class TestTrainLoop(unittest.TestCase):
    def test_train_records_losses_and_steps_scheduler(self):
        torch.manual_seed(1)
        x = torch.tensor([[0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]])
        y = torch.tensor([[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7]])
        dataset = torch.utils.data.TensorDataset(x, y)
        loader = torch.utils.data.DataLoader(dataset, batch_size=2, shuffle=False)
        model = TinyLanguageModel(vocab_size=8)
        optimizer = torch.optim.AdamW(model.parameters(), lr=0.05)
        scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lambda step: 1.0)
        config = submission.TrainConfig(num_epochs=2, max_grad_norm=1.0, log_interval=99, device="cpu")
        history = []

        initial_loss = F.cross_entropy(model(x).reshape(-1, 8), y.reshape(-1)).item()
        submission.train(model, loader, optimizer, scheduler, config, history)
        final_loss = F.cross_entropy(model(x).reshape(-1, 8), y.reshape(-1)).item()

        self.assertEqual(len(history), 4)
        self.assertLess(final_loss, initial_loss)
        self.assertEqual(scheduler.last_epoch, 4)

    def test_perplexity_is_exp_loss(self):
        self.assertAlmostEqual(submission.perplexity(2.0), math.exp(2.0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
