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


class TinyLogitModel(nn.Module):
    def __init__(self, logits):
        super().__init__()
        self.anchor = nn.Parameter(torch.zeros(()))
        self.register_buffer("fixed_logits", logits)

    def forward(self, input_ids=None, attention_mask=None):
        batch, seq = input_ids.shape
        logits = self.fixed_logits[:batch, :seq].clone() + self.anchor
        return SimpleNamespace(logits=logits)


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


class TinyModule(nn.Module):
    def __init__(self):
        super().__init__()
        self.q_proj = nn.Linear(4, 3, bias=True)
        self.v_proj = nn.Linear(4, 3, bias=False)
        self.other = nn.Linear(4, 3, bias=False)

    def forward(self, x):
        return self.q_proj(x) + self.v_proj(x) + self.other(x)


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

    def test_grpo_advantages_whiten_within_group(self):
        rewards = torch.tensor([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]])
        adv = submission.grpo_advantages(rewards)
        self.assertTrue(torch.allclose(adv.mean(dim=0), torch.zeros(2), atol=1e-6))
        self.assertTrue(torch.allclose(adv.std(dim=0, unbiased=False), torch.ones(2), atol=1e-5))


if __name__ == "__main__":
    unittest.main(verbosity=2)
