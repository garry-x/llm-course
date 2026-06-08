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

    def test_optimizer_state_memory_counts_adamw_states_and_sharding(self):
        dense = submission.optimizer_state_memory_bytes(
            num_params=1_000,
            param_dtype_bytes=2,
            grad_dtype_bytes=2,
            optimizer_state_dtype_bytes=4,
            num_moments=2,
            data_parallel_size=4,
            shard_optimizer_states=False,
        )
        self.assertEqual(dense["param_bytes"], 2_000)
        self.assertEqual(dense["grad_bytes"], 2_000)
        self.assertEqual(dense["optimizer_state_bytes"], 8_000)
        self.assertEqual(dense["per_rank_optimizer_state_bytes"], 8_000)
        self.assertEqual(dense["total_bytes"], 12_000)

        sharded = submission.optimizer_state_memory_bytes(
            num_params=1_000,
            param_dtype_bytes=2,
            grad_dtype_bytes=2,
            optimizer_state_dtype_bytes=4,
            num_moments=2,
            data_parallel_size=4,
            shard_optimizer_states=True,
        )
        self.assertEqual(sharded["per_rank_optimizer_state_bytes"], 2_000)
        self.assertEqual(sharded["total_bytes"], 6_000)

    def test_training_budget_rejects_non_positive_values(self):
        with self.assertRaises(ValueError):
            submission.global_batch_tokens(0, 2048)
        with self.assertRaises(ValueError):
            submission.training_steps_for_token_budget(1000, 0)
        with self.assertRaises(ValueError):
            submission.dense_lm_training_flops(0, 1000)
        with self.assertRaises(ValueError):
            submission.optimizer_state_memory_bytes(0)
        with self.assertRaises(ValueError):
            submission.optimizer_state_memory_bytes(1000, num_moments=-1)


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

    def test_label_smoothed_cross_entropy_matches_manual_distribution(self):
        logits = torch.tensor(
            [
                [[2.0, 0.0, -1.0], [0.0, 1.0, 2.0]],
                [[1.0, -1.0, 0.0], [3.0, 0.0, -2.0]],
            ]
        )
        targets = torch.tensor([[0, 2], [1, -100]])
        epsilon = 0.2
        loss = submission.label_smoothed_cross_entropy(logits, targets, epsilon=epsilon, ignore_index=-100)

        log_probs = torch.log_softmax(logits, dim=-1)
        terms = []
        for b, t in [(0, 0), (0, 1), (1, 0)]:
            target = targets[b, t].item()
            distribution = torch.full((3,), epsilon / 2)
            distribution[target] = 1.0 - epsilon
            terms.append(-(distribution * log_probs[b, t]).sum())
        expected = torch.stack(terms).mean()
        self.assertTrue(torch.allclose(loss, expected, atol=1e-6))

    def test_label_smoothed_cross_entropy_rejects_bad_inputs(self):
        with self.assertRaises(ValueError):
            submission.label_smoothed_cross_entropy(torch.randn(2, 3), torch.ones(2, dtype=torch.long))
        with self.assertRaises(ValueError):
            submission.label_smoothed_cross_entropy(torch.randn(2, 3, 4), torch.ones(2, 2), epsilon=1.0)
        with self.assertRaises(ValueError):
            submission.label_smoothed_cross_entropy(torch.randn(1, 2, 1), torch.zeros(1, 2, dtype=torch.long))
        with self.assertRaises(ValueError):
            submission.label_smoothed_cross_entropy(torch.randn(1, 1, 3), torch.tensor([[4]]))
        with self.assertRaises(ValueError):
            submission.label_smoothed_cross_entropy(torch.randn(1, 2, 3), torch.tensor([[-100, -100]]), ignore_index=-100)

    def test_clip_grad_norm_scales_all_gradients_by_global_norm(self):
        p1 = torch.nn.Parameter(torch.tensor([1.0, 2.0]))
        p2 = torch.nn.Parameter(torch.tensor([3.0]))
        p3 = torch.nn.Parameter(torch.tensor([4.0]))
        p1.grad = torch.tensor([3.0, 0.0])
        p2.grad = torch.tensor([4.0])
        p3.grad = None

        result = submission.clip_grad_norm([p1, p2, p3], max_norm=2.0, eps=0.0 + 1e-6)
        expected_coef = 2.0 / (5.0 + 1e-6)
        self.assertAlmostEqual(result["total_norm"], 5.0)
        self.assertAlmostEqual(result["clip_coef"], expected_coef)
        self.assertTrue(torch.allclose(p1.grad, torch.tensor([3.0 * expected_coef, 0.0]), atol=1e-6))
        self.assertTrue(torch.allclose(p2.grad, torch.tensor([4.0 * expected_coef]), atol=1e-6))
        self.assertIsNone(p3.grad)

    def test_clip_grad_norm_leaves_small_gradients_and_rejects_bad_norms(self):
        p = torch.nn.Parameter(torch.tensor([1.0]))
        p.grad = torch.tensor([0.25])
        result = submission.clip_grad_norm([p], max_norm=1.0)
        self.assertAlmostEqual(result["clip_coef"], 1.0)
        self.assertTrue(torch.allclose(p.grad, torch.tensor([0.25])))
        self.assertEqual(submission.clip_grad_norm([], max_norm=1.0)["total_norm"], 0.0)
        with self.assertRaises(ValueError):
            submission.clip_grad_norm([p], max_norm=0.0)
        with self.assertRaises(ValueError):
            submission.clip_grad_norm([p], max_norm=1.0, eps=0.0)

    def test_gradient_accumulation_step_accounting_scales_loss_and_steps_once(self):
        result = submission.gradient_accumulation_step_accounting(
            micro_batch_losses=[2.4, 2.0, 1.8, 2.2],
            grad_accum_steps=4,
            tokens_per_micro_batch=8192,
        )
        self.assertEqual(result["scaled_losses"], [0.6, 0.5, 0.45, 0.55])
        self.assertEqual(result["group_raw_means"], [2.1])
        self.assertEqual(result["group_backward_loss_sums"], [2.1])
        self.assertEqual(result["optimizer_steps"], 1)
        self.assertEqual(result["scheduler_steps"], 1)
        self.assertEqual(result["consumed_tokens"], 32768)

    def test_gradient_accumulation_step_accounting_counts_optimizer_groups(self):
        result = submission.gradient_accumulation_step_accounting(
            micro_batch_losses=[1.0, 3.0, 2.0, 6.0],
            grad_accum_steps=2,
            tokens_per_micro_batch=10,
        )
        self.assertEqual(result["scaled_losses"], [0.5, 1.5, 1.0, 3.0])
        self.assertEqual(result["group_raw_means"], [2.0, 4.0])
        self.assertEqual(result["group_backward_loss_sums"], [2.0, 4.0])
        self.assertEqual(result["optimizer_steps"], 2)
        self.assertEqual(result["scheduler_steps"], 2)
        self.assertEqual(result["consumed_tokens"], 40)

    def test_gradient_accumulation_step_accounting_rejects_bad_inputs(self):
        with self.assertRaises(ValueError):
            submission.gradient_accumulation_step_accounting([], 4, 8192)
        with self.assertRaises(ValueError):
            submission.gradient_accumulation_step_accounting([1.0, 2.0], 0, 8192)
        with self.assertRaises(ValueError):
            submission.gradient_accumulation_step_accounting([1.0, 2.0], 2, 0)
        with self.assertRaises(ValueError):
            submission.gradient_accumulation_step_accounting([1.0, 2.0, 3.0], 2, 8192)
        with self.assertRaises(ValueError):
            submission.gradient_accumulation_step_accounting([1.0, float("nan")], 2, 8192)

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

    def test_lr_schedule_trace_reports_lr_and_consumed_tokens(self):
        trace = submission.lr_schedule_trace(
            base_lr=0.2,
            num_warmup_steps=2,
            num_training_steps=6,
            min_lr_ratio=0.25,
            tokens_per_step=1000,
        )
        rows = trace["steps"]
        self.assertEqual(len(rows), 7)
        self.assertEqual(rows[0]["phase"], "warmup")
        self.assertAlmostEqual(rows[0]["lr_multiplier"], 0.0)
        self.assertAlmostEqual(rows[0]["lr"], 0.0)
        self.assertEqual(rows[0]["consumed_tokens"], 0)
        self.assertAlmostEqual(rows[1]["lr_multiplier"], 0.5)
        self.assertAlmostEqual(rows[1]["lr"], 0.1)
        self.assertEqual(rows[1]["consumed_tokens"], 1000)
        self.assertEqual(rows[2]["phase"], "cosine")
        self.assertAlmostEqual(rows[2]["lr_multiplier"], 1.0)
        self.assertAlmostEqual(rows[2]["lr"], 0.2)
        self.assertAlmostEqual(rows[6]["lr_multiplier"], 0.25)
        self.assertAlmostEqual(rows[6]["lr"], 0.05)
        self.assertEqual(rows[6]["consumed_tokens"], 6000)

    def test_lr_schedule_trace_rejects_bad_inputs(self):
        with self.assertRaises(ValueError):
            submission.lr_schedule_trace(0.0, 2, 6)
        with self.assertRaises(ValueError):
            submission.lr_schedule_trace(0.2, -1, 6)
        with self.assertRaises(ValueError):
            submission.lr_schedule_trace(0.2, 7, 6)
        with self.assertRaises(ValueError):
            submission.lr_schedule_trace(0.2, 2, 6, min_lr_ratio=1.5)
        with self.assertRaises(ValueError):
            submission.lr_schedule_trace(0.2, 2, 6, tokens_per_step=0)


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


@unittest.skipIf(torch is None, "PyTorch is required for Ch07 training tests")
class TestCalibrationMetrics(unittest.TestCase):
    def test_expected_calibration_error_bins_confidence_and_accuracy(self):
        logits = torch.tensor(
            [
                [3.0, 0.0],
                [0.0, 3.0],
                [3.0, 0.0],
                [0.2, 0.0],
            ]
        )
        targets = torch.tensor([0, 1, 1, 0])
        result = submission.expected_calibration_error(logits, targets, n_bins=2)

        probs = torch.softmax(logits, dim=-1)
        confidence, predictions = probs.max(dim=-1)
        correct = (predictions == targets).float()
        low_bin = (confidence >= 0.0) & (confidence < 0.5)
        high_bin = (confidence >= 0.5) & (confidence <= 1.0)
        self.assertEqual(int(low_bin.sum()), 0)
        self.assertEqual(int(result["bin_counts"][1].item()), 4)

        expected_acc = correct[high_bin].mean()
        expected_conf = confidence[high_bin].mean()
        expected_ece = torch.abs(expected_acc - expected_conf).item()
        self.assertAlmostEqual(result["bin_accuracy"][1].item(), expected_acc.item())
        self.assertAlmostEqual(result["bin_confidence"][1].item(), expected_conf.item())
        self.assertAlmostEqual(result["ece"], expected_ece)

    def test_expected_calibration_error_respects_ignore_index_and_shapes(self):
        logits = torch.tensor([[[2.0, 0.0], [0.0, 2.0], [2.0, 0.0]]])
        targets = torch.tensor([[0, -100, 1]])
        result = submission.expected_calibration_error(logits, targets, n_bins=5, ignore_index=-100)
        self.assertEqual(int(result["bin_counts"].sum().item()), 2)

        with self.assertRaises(ValueError):
            submission.expected_calibration_error(logits, targets, n_bins=0)
        with self.assertRaises(ValueError):
            submission.expected_calibration_error(torch.randn(2, 3), torch.randn(2, 2).long())
        with self.assertRaises(ValueError):
            submission.expected_calibration_error(logits, torch.full((1, 3), -100), ignore_index=-100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
