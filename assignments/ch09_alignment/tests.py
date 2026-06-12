"""Autograder-style tests for Chapter 9 fine-tuning and alignment exercises."""

import importlib
import os
import unittest
from types import SimpleNamespace

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


class TinyChatTokenizer:
    pad_token_id = 0
    eos_token = "<eos>"

    def __init__(self):
        alphabet = list("abcdefghijklmnopqrstuvwxyz <>/_:") + ["\n"]
        self.stoi = {ch: i + 1 for i, ch in enumerate(alphabet)}
        self.stoi["<pad>"] = self.pad_token_id

    def apply_chat_template(self, messages, tokenize=False):
        assert not tokenize
        return "".join(f"<user>{m['content']}</user>\n<assistant>" for m in messages)

    def encode(self, text):
        return [self.stoi.get(ch, 1) for ch in text]


if nn is not None:
    class TinyLogitModel(nn.Module):
        def __init__(self, logits):
            super().__init__()
            self.anchor = nn.Parameter(torch.zeros(()))
            self.register_buffer("fixed_logits", logits)

        def forward(self, input_ids=None, attention_mask=None):
            batch, seq = input_ids.shape
            logits = self.fixed_logits[:batch, :seq].clone() + self.anchor
            return SimpleNamespace(logits=logits)
else:
    class TinyLogitModel:
        pass


@unittest.skipIf(torch is None, "PyTorch is required for Ch09 alignment tests")
class TestSFT(unittest.TestCase):
    def test_sft_dataset_masks_prompt_and_padding(self):
        tokenizer = TinyChatTokenizer()
        data = [{"instruction": "abc", "response": "de"}]
        dataset = submission.SFTDataset(data, tokenizer, max_len=128)
        item = dataset[0]
        prompt = tokenizer.apply_chat_template([{"role": "user", "content": "abc"}], tokenize=False)
        prompt_len = len(tokenizer.encode(prompt))
        self.assertTrue(torch.all(item["labels"][:prompt_len] == -100))
        self.assertTrue(torch.any(item["labels"][prompt_len:] != -100))

    def test_sft_loss_ignores_masked_labels(self):
        logits = torch.tensor([[[10.0, 0.0, 0.0], [0.0, 8.0, 0.0], [0.0, 0.0, 6.0]]])
        labels = torch.tensor([[-100, 1, -100]])
        loss = submission.sft_loss_from_logits(logits, labels)
        expected = F.cross_entropy(logits[:, :-1, :].reshape(-1, 3), labels[:, 1:].reshape(-1), ignore_index=-100)
        self.assertTrue(torch.allclose(loss, expected))


if nn is not None:
    class TinyModule(nn.Module):
        def __init__(self):
            super().__init__()
            self.q_proj = nn.Linear(4, 3, bias=True)
            self.v_proj = nn.Linear(4, 3, bias=False)
            self.other = nn.Linear(4, 3, bias=False)

        def forward(self, x):
            return self.q_proj(x) + self.v_proj(x) + self.other(x)
else:
    class TinyModule:
        pass


@unittest.skipIf(torch is None, "PyTorch is required for Ch09 alignment tests")
class TestLoRA(unittest.TestCase):
    def test_lora_initial_output_matches_base_and_trainable_count(self):
        torch.manual_seed(0)
        base = nn.Linear(4, 3, bias=True)
        lora = submission.LoRALinear(base, r=2, alpha=4.0, dropout=0.0)
        x = torch.randn(5, 4)
        self.assertTrue(torch.allclose(lora(x), base(x), atol=1e-6))
        self.assertTrue(lora.A.requires_grad)
        self.assertTrue(lora.B.requires_grad)
        self.assertFalse(lora.weight.requires_grad)
        self.assertIsNotNone(lora.bias)
        self.assertFalse(lora.bias.requires_grad)

    def test_apply_lora_replaces_targets_and_freezes_base(self):
        model = TinyModule()
        submission.apply_lora(model, r=2, alpha=4.0, target_modules=["q_proj", "v_proj"])
        self.assertIsInstance(model.q_proj, submission.LoRALinear)
        self.assertIsInstance(model.v_proj, submission.LoRALinear)
        self.assertIsInstance(model.other, nn.Linear)
        trainable_names = [name for name, p in model.named_parameters() if p.requires_grad]
        self.assertEqual(set(trainable_names), {"q_proj.A", "q_proj.B", "v_proj.A", "v_proj.B"})
        counts = submission.count_trainable_parameters(model)
        self.assertEqual(counts["trainable"], 2 * (2 * 4 + 3 * 2))

    def test_merge_lora_adds_delta_weight(self):
        model = TinyModule()
        before = model.q_proj.weight.detach().clone()
        A = torch.ones(2, 4)
        B = torch.ones(3, 2) * 0.5
        submission.merge_lora(model, {"q_proj": {"A": A, "B": B, "scaling": 2.0}})
        expected_delta = B @ A * 2.0
        self.assertTrue(torch.allclose(model.q_proj.weight, before + expected_delta))


@unittest.skipIf(torch is None, "PyTorch is required for Ch09 alignment tests")
class TestDPOGRPO(unittest.TestCase):
    def test_sequence_log_probs_ignores_negative_100_before_gather(self):
        logits = torch.zeros(1, 4, 5)
        logits[0, 0, 2] = 3.0
        logits[0, 1, 4] = 2.0
        logits[0, 2, 1] = 1.0
        model = TinyLogitModel(logits)
        input_ids = torch.tensor([[1, 2, 3, 4]])
        labels = torch.tensor([[-100, 2, -100, 1]])
        logp = submission.sequence_log_probs(model, input_ids, torch.ones_like(input_ids), labels)
        log_probs = F.log_softmax(logits[:, :-1, :], dim=-1)
        expected = log_probs[0, 0, 2] + log_probs[0, 2, 1]
        self.assertTrue(torch.allclose(logp, expected.unsqueeze(0)))

    def test_dpo_loss_prefers_chosen_ratio(self):
        policy_chosen = torch.tensor([3.0, 1.0])
        policy_rejected = torch.tensor([1.0, 2.0])
        ref_chosen = torch.tensor([1.0, 1.0])
        ref_rejected = torch.tensor([1.0, 1.0])
        loss, acc = submission.dpo_loss(policy_chosen, policy_rejected, ref_chosen, ref_rejected, beta=0.5)
        expected_logits = torch.tensor([1.0, -0.5])
        expected = -F.logsigmoid(expected_logits).mean()
        self.assertTrue(torch.allclose(loss, expected))
        self.assertEqual(acc, 0.5)

    def test_dpo_implicit_rewards_report_reference_relative_margins(self):
        policy_chosen = torch.tensor([3.0, 1.0])
        policy_rejected = torch.tensor([1.0, 2.0])
        ref_chosen = torch.tensor([1.0, 1.0])
        ref_rejected = torch.tensor([1.0, 1.0])
        report = submission.dpo_implicit_rewards(
            policy_chosen,
            policy_rejected,
            ref_chosen,
            ref_rejected,
            beta=0.5,
        )
        self.assertTrue(torch.allclose(report["chosen_rewards"], torch.tensor([1.0, 0.0])))
        self.assertTrue(torch.allclose(report["rejected_rewards"], torch.tensor([0.0, 0.5])))
        self.assertTrue(torch.allclose(report["reward_margin"], torch.tensor([1.0, -0.5])))
        self.assertTrue(torch.allclose(report["preference_prob"], torch.sigmoid(torch.tensor([1.0, -0.5]))))
        self.assertEqual(report["preference_accuracy"], 0.5)
        self.assertAlmostEqual(report["mean_margin"], 0.25)

    def test_dpo_implicit_rewards_rejects_bad_inputs(self):
        values = torch.zeros(2)
        with self.assertRaises(ValueError):
            submission.dpo_implicit_rewards(values, torch.zeros(3), values, values)
        with self.assertRaises(ValueError):
            submission.dpo_implicit_rewards(values, values, values, values, beta=0.0)

    def test_approx_kl_from_logps_masks_padding_tokens(self):
        policy_logps = torch.tensor([[-0.2, -1.0, -3.0]])
        ref_logps = torch.tensor([[-0.4, -0.7, -3.5]])
        mask = torch.tensor([[1, 1, 0]])
        kl = submission.approx_kl_from_logps(policy_logps, ref_logps, mask=mask)
        log_ratio = ref_logps[:, :2] - policy_logps[:, :2]
        expected = (torch.exp(log_ratio) - log_ratio - 1.0).mean()
        self.assertTrue(torch.allclose(kl, expected))
        none = submission.approx_kl_from_logps(policy_logps, ref_logps, mask=mask, reduction="none")
        self.assertEqual(none[0, 2].item(), 0.0)

    def test_approx_kl_from_logps_rejects_bad_inputs(self):
        policy_logps = torch.zeros(2, 3)
        ref_logps = torch.zeros(2, 3)
        with self.assertRaises(ValueError):
            submission.approx_kl_from_logps(policy_logps, torch.zeros(2, 2))
        with self.assertRaises(ValueError):
            submission.approx_kl_from_logps(policy_logps, ref_logps, mask=torch.ones(2, 2))
        with self.assertRaises(ValueError):
            submission.approx_kl_from_logps(policy_logps, ref_logps, reduction="median")
        with self.assertRaises(ValueError):
            submission.approx_kl_from_logps(policy_logps, ref_logps, mask=torch.zeros(2, 3))

    def test_pairwise_reward_loss_matches_bradley_terry(self):
        chosen = torch.tensor([3.0, 1.0])
        rejected = torch.tensor([1.0, 2.0])
        loss, acc = submission.pairwise_reward_loss(chosen, rejected)
        expected = -F.logsigmoid(torch.tensor([2.0, -1.0])).mean()
        self.assertTrue(torch.allclose(loss, expected))
        self.assertEqual(acc, 0.5)

    def test_preference_length_bias_reports_direction(self):
        chosen_lengths = torch.tensor([10, 8, 5, 7])
        rejected_lengths = torch.tensor([6, 8, 9, 4])
        stats = submission.preference_length_bias(chosen_lengths, rejected_lengths)
        self.assertAlmostEqual(stats["mean_length_delta"], 0.75)
        self.assertAlmostEqual(stats["chosen_longer_rate"], 0.5)
        self.assertAlmostEqual(stats["rejected_longer_rate"], 0.25)
        self.assertAlmostEqual(stats["tie_rate"], 0.25)

    def test_post_training_data_audit_passes_balanced_records(self):
        records = [
            {
                "kind": "sft",
                "prompt_id": "p1",
                "task": "qa",
                "safety_slice": "ordinary",
                "response_tokens": 80,
            },
            {
                "kind": "sft",
                "prompt_id": "p2",
                "task": "coding",
                "safety_slice": "ordinary",
                "response_tokens": 120,
            },
            {
                "kind": "preference",
                "prompt_id": "p3",
                "task": "qa",
                "safety_slice": "benign_sensitive",
                "chosen_tokens": 90,
                "rejected_tokens": 86,
                "winner_id": "a",
            },
            {
                "kind": "preference",
                "prompt_id": "p4",
                "task": "coding",
                "safety_slice": "ordinary",
                "chosen_tokens": 75,
                "rejected_tokens": 80,
                "winner_id": "b",
            },
            {
                "kind": "rlvr",
                "prompt_id": "p5",
                "task": "math",
                "safety_slice": "ordinary",
                "chosen_tokens": 60,
                "rejected_tokens": 62,
                "winner_id": "solver_a",
            },
        ]
        report = submission.post_training_data_audit(
            records,
            thresholds={
                "min_samples": 5,
                "min_sft_examples": 2,
                "min_preference_pairs": 3,
                "min_task_count": 3,
                "min_safety_slice_count": 2,
                "max_task_share": 0.4,
                "max_mean_length_delta_ratio": 0.1,
                "max_chosen_longer_rate": 0.5,
            },
        )
        self.assertTrue(report["overall_pass"])
        self.assertEqual(report["decision"], "post_training_data_ready")
        self.assertTrue(report["gates"]["coverage"]["pass"])
        self.assertTrue(report["gates"]["label_quality"]["pass"])
        self.assertEqual(report["counts"]["by_kind"]["sft"], 2)
        self.assertEqual(report["counts"]["by_kind"]["preference_or_rlvr"], 3)
        self.assertAlmostEqual(report["metrics"]["max_task_share"], 0.4)

    def test_post_training_data_audit_flags_data_quality_failures(self):
        records = [
            {
                "kind": "preference",
                "prompt_id": "p1",
                "task": "qa",
                "safety_slice": "ordinary",
                "chosen_tokens": 240,
                "rejected_tokens": 80,
                "winner_id": "a",
                "eval_overlap": True,
            },
            {
                "kind": "preference",
                "prompt_id": "p1",
                "task": "qa",
                "safety_slice": "ordinary",
                "chosen_tokens": 220,
                "rejected_tokens": 70,
                "winner_id": "b",
                "chosen_safety_violation": True,
            },
            {
                "kind": "preference",
                "prompt_id": "p2",
                "task": "qa",
                "safety_slice": "ordinary",
                "chosen_tokens": 200,
                "rejected_tokens": 60,
                "winner_id": "c",
            },
        ]
        report = submission.post_training_data_audit(
            records,
            thresholds={
                "min_samples": 4,
                "min_task_count": 2,
                "min_safety_slice_count": 2,
                "max_task_share": 0.8,
                "max_eval_overlap_rate": 0.0,
                "max_label_conflict_rate": 0.0,
                "max_unsafe_chosen_rate": 0.0,
                "max_mean_length_delta_ratio": 0.25,
                "max_chosen_longer_rate": 0.8,
            },
        )
        self.assertFalse(report["overall_pass"])
        self.assertEqual(report["decision"], "fix_post_training_data_before_optimization")
        self.assertFalse(report["gates"]["coverage"]["pass"])
        self.assertFalse(report["gates"]["label_quality"]["pass"])
        self.assertFalse(report["gates"]["leakage"]["pass"])
        self.assertFalse(report["gates"]["safety"]["pass"])
        self.assertIn("collect_or_rebalance_post_training_slices", report["action_items"])
        self.assertIn("audit_preference_labels_length_bias_and_prompt_conflicts", report["action_items"])
        self.assertIn("remove_eval_overlap_before_post_training", report["action_items"])
        self.assertIn("fix_or_filter_unsafe_chosen_responses", report["action_items"])

    def test_post_training_data_audit_rejects_bad_records(self):
        with self.assertRaises(ValueError):
            submission.post_training_data_audit([])
        with self.assertRaises(ValueError):
            submission.post_training_data_audit([{"kind": "bad", "prompt_id": "p", "task": "qa"}])
        with self.assertRaises(ValueError):
            submission.post_training_data_audit([{"kind": "sft", "prompt_id": "p", "task": "qa", "response_tokens": 0}])
        with self.assertRaises(ValueError):
            submission.post_training_data_audit(
                [{"kind": "preference", "prompt_id": "p", "task": "qa", "chosen_tokens": 1, "rejected_tokens": 1}],
                thresholds={"max_task_share": 1.2},
            )

    def test_ppo_clipped_policy_loss_matches_manual_surrogate(self):
        old_logps = torch.zeros(3)
        ratios = torch.tensor([1.0, 1.5, 0.5])
        new_logps = torch.log(ratios)
        advantages = torch.tensor([1.0, 1.0, -1.0])
        loss, stats = submission.ppo_clipped_policy_loss(
            new_logps,
            old_logps,
            advantages,
            clip_range=0.2,
        )
        expected_surrogate = torch.tensor([1.0, 1.2, -0.8])
        self.assertTrue(torch.allclose(loss, -expected_surrogate.mean()))
        expected_kl = ((ratios - 1.0) - torch.log(ratios)).mean().item()
        self.assertAlmostEqual(stats["mean_ratio"], ratios.mean().item())
        self.assertAlmostEqual(stats["clip_fraction"], 2 / 3)
        self.assertAlmostEqual(stats["approx_kl"], expected_kl)

    def test_ppo_clipped_policy_loss_masks_padding_tokens(self):
        old_logps = torch.zeros(3)
        ratios = torch.tensor([1.0, 1.5, 0.5])
        new_logps = torch.log(ratios)
        advantages = torch.tensor([1.0, 1.0, -1.0])
        mask = torch.tensor([1, 1, 0])
        loss, stats = submission.ppo_clipped_policy_loss(
            new_logps,
            old_logps,
            advantages,
            mask=mask,
            clip_range=0.2,
        )
        expected_surrogate = torch.tensor([1.0, 1.2])
        self.assertTrue(torch.allclose(loss, -expected_surrogate.mean()))
        self.assertAlmostEqual(stats["clip_fraction"], 0.5)
        self.assertAlmostEqual(stats["mean_ratio"], 1.25)

    def test_ppo_clipped_policy_loss_rejects_bad_inputs(self):
        logps = torch.zeros(2, 3)
        advantages = torch.ones(2, 3)
        with self.assertRaises(ValueError):
            submission.ppo_clipped_policy_loss(logps, torch.zeros(2, 2), advantages)
        with self.assertRaises(ValueError):
            submission.ppo_clipped_policy_loss(logps, logps, torch.ones(2, 2))
        with self.assertRaises(ValueError):
            submission.ppo_clipped_policy_loss(logps, logps, advantages, mask=torch.ones(2, 2))
        with self.assertRaises(ValueError):
            submission.ppo_clipped_policy_loss(logps, logps, advantages, mask=torch.zeros(2, 3))
        with self.assertRaises(ValueError):
            submission.ppo_clipped_policy_loss(logps, logps, advantages, clip_range=0.0)

    def test_grpo_advantages_whiten_within_group(self):
        rewards = torch.tensor([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]])
        adv = submission.grpo_advantages(rewards)
        self.assertTrue(torch.allclose(adv.mean(dim=0), torch.zeros(2), atol=1e-6))
        self.assertTrue(torch.allclose(adv.std(dim=0, unbiased=False), torch.ones(2), atol=1e-5))

    def test_grpo_policy_loss_combines_clipped_surrogate_and_kl(self):
        rewards = torch.tensor([[1.0], [2.0], [3.0]])
        old_logps = torch.zeros(3, 1, 2)
        ratios = torch.tensor([[[1.0, 1.5]], [[1.0, 1.0]], [[0.5, 1.0]]])
        new_logps = torch.log(ratios)
        ref_logps = torch.zeros_like(new_logps)
        mask = torch.tensor([[[1, 1]], [[1, 0]], [[1, 1]]])

        report = submission.grpo_policy_loss(
            new_logps,
            old_logps,
            ref_logps,
            rewards,
            completion_mask=mask,
            clip_range=0.2,
            kl_beta=0.04,
        )

        expected_adv = (rewards - rewards.mean(dim=0, keepdim=True)) / rewards.std(
            dim=0,
            keepdim=True,
            unbiased=False,
        )
        expected_adv_tokens = expected_adv.unsqueeze(-1).expand_as(new_logps)
        clipped_ratios = ratios.clamp(0.8, 1.2)
        expected_surrogate = torch.minimum(ratios * expected_adv_tokens, clipped_ratios * expected_adv_tokens)
        valid = mask.float()
        expected_policy_loss = -(expected_surrogate * valid).sum() / valid.sum()
        log_ratio = ref_logps - new_logps
        expected_kl = ((torch.exp(log_ratio) - log_ratio - 1.0) * valid).sum() / valid.sum()

        self.assertTrue(torch.allclose(report["advantages"], expected_adv, atol=1e-6))
        self.assertTrue(torch.allclose(report["policy_loss"], expected_policy_loss, atol=1e-6))
        self.assertTrue(torch.allclose(report["kl_loss"], expected_kl, atol=1e-6))
        self.assertTrue(torch.allclose(report["loss"], expected_policy_loss + 0.04 * expected_kl, atol=1e-6))
        self.assertAlmostEqual(report["clip_fraction"], 2 / 5)
        self.assertAlmostEqual(report["mean_ratio"], ((ratios * valid).sum() / valid.sum()).item())

    def test_grpo_policy_loss_rejects_bad_inputs(self):
        logps = torch.zeros(3, 1, 2)
        rewards = torch.ones(3, 1)
        with self.assertRaises(ValueError):
            submission.grpo_policy_loss(logps, torch.zeros(3, 1), logps, rewards)
        with self.assertRaises(ValueError):
            submission.grpo_policy_loss(logps, logps, logps, torch.ones(3, 1, 1))
        with self.assertRaises(ValueError):
            submission.grpo_policy_loss(logps, logps, logps, torch.ones(2, 1))
        with self.assertRaises(ValueError):
            submission.grpo_policy_loss(logps, logps, logps, rewards, completion_mask=torch.zeros(3, 1, 2))
        with self.assertRaises(ValueError):
            submission.grpo_policy_loss(logps, logps, logps, rewards, clip_range=0.0)
        with self.assertRaises(ValueError):
            submission.grpo_policy_loss(logps, logps, logps, rewards, kl_beta=-0.1)

    def test_rlvr_grader_report_passes_usable_signal(self):
        rewards = torch.tensor([0.0, 1.0, 0.5, 1.0])
        grader_pass = torch.tensor([False, True, False, True])
        report = submission.rlvr_grader_report(
            rewards,
            grader_pass,
            completion_lengths=torch.tensor([80, 120, 90, 110]),
            hacking_flags=torch.tensor([False, False, False, False]),
            thresholds={
                "min_pass_rate": 0.25,
                "max_pass_rate": 0.8,
                "min_reward_std": 0.1,
                "max_avg_completion_tokens": 128,
                "max_hacking_rate": 0.0,
            },
        )
        self.assertTrue(report["overall_pass"])
        self.assertEqual(report["decision"], "train_or_continue_rl")
        self.assertEqual(report["sample_count"], 4)
        self.assertAlmostEqual(report["pass_rate"], 0.5)
        self.assertTrue(report["gates"]["reward_signal"]["pass"])
        self.assertTrue(report["gates"]["cost"]["pass"])
        self.assertTrue(report["gates"]["integrity"]["pass"])

    def test_rlvr_grader_report_attributes_grader_cost_and_hacking_failures(self):
        report = submission.rlvr_grader_report(
            torch.tensor([1.0, 1.0, 1.0, 1.0]),
            torch.tensor([True, True, True, True]),
            completion_lengths=torch.tensor([400, 500, 450, 550]),
            hacking_flags=torch.tensor([False, True, False, False]),
            thresholds={
                "min_pass_rate": 0.1,
                "max_pass_rate": 0.9,
                "min_reward_std": 0.01,
                "max_avg_completion_tokens": 256,
                "max_hacking_rate": 0.0,
            },
        )
        self.assertFalse(report["overall_pass"])
        self.assertEqual(report["decision"], "fix_grader_or_data_before_rl")
        self.assertIn("rebalance_prompts_grader_thresholds_or_reward_scale", report["action_items"])
        self.assertIn("reduce_reasoning_budget_or_add_length_penalty", report["action_items"])
        self.assertIn("tighten_grader_with_adversarial_or_process_checks", report["action_items"])

    def test_rlvr_grader_report_rejects_bad_inputs(self):
        with self.assertRaises(ValueError):
            submission.rlvr_grader_report([], [])
        with self.assertRaises(ValueError):
            submission.rlvr_grader_report(torch.ones(2), torch.ones(3, dtype=torch.bool))
        with self.assertRaises(ValueError):
            submission.rlvr_grader_report(torch.ones(2), torch.ones(2, dtype=torch.bool), thresholds={"min_pass_rate": 0.9, "max_pass_rate": 0.1})
        with self.assertRaises(ValueError):
            submission.rlvr_grader_report(torch.ones(2), torch.ones(2, dtype=torch.bool), completion_lengths=torch.tensor([1.0, -1.0]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
