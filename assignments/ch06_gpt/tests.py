"""Autograder-style tests for Chapter 6 GPT model assembly exercises."""

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


@unittest.skipIf(torch is None, "PyTorch is required for Ch06 GPT tests")
class TestGPTConfig(unittest.TestCase):
    def test_default_config_matches_gpt2_small(self):
        config = submission.GPTConfig()
        self.assertEqual(config.vocab_size, 50257)
        self.assertEqual(config.max_seq_len, 1024)
        self.assertEqual(config.d_model, 768)
        self.assertEqual(config.n_heads, 12)
        self.assertEqual(config.n_layers, 12)
        self.assertTrue(config.tie_weights)


@unittest.skipIf(torch is None, "PyTorch is required for Ch06 GPT tests")
class TestGPTModel(unittest.TestCase):
    def small_config(self, **kwargs):
        defaults = dict(
            vocab_size=31,
            max_seq_len=8,
            d_model=16,
            n_heads=4,
            n_layers=2,
            dropout=0.0,
            bias=True,
            tie_weights=True,
        )
        defaults.update(kwargs)
        return submission.GPTConfig(**defaults)

    def test_forward_shape_and_weight_tying(self):
        torch.manual_seed(0)
        config = self.small_config()
        model = submission.GPTModel(config)
        input_ids = torch.randint(0, config.vocab_size, (3, 5))
        logits = model(input_ids)
        self.assertEqual(tuple(logits.shape), (3, 5, config.vocab_size))
        self.assertIs(model.lm_head.weight, model.token_embedding.weight)

    def test_can_disable_weight_tying(self):
        config = self.small_config(tie_weights=False)
        model = submission.GPTModel(config)
        self.assertIsNot(model.lm_head.weight, model.token_embedding.weight)
        groups = submission.parameter_breakdown(model)
        self.assertGreater(groups["lm_head"], 0)

    def test_gradient_flows_to_all_parameters(self):
        torch.manual_seed(1)
        config = self.small_config(vocab_size=23)
        model = submission.GPTModel(config)
        input_ids = torch.randint(0, config.vocab_size, (2, 6))
        logits = model(input_ids)
        loss = logits.pow(2).mean()
        loss.backward()
        params = [p for p in model.parameters() if p.requires_grad]
        self.assertTrue(all(p.grad is not None for p in params))

    def test_rejects_sequence_longer_than_context(self):
        config = self.small_config(max_seq_len=4)
        model = submission.GPTModel(config)
        input_ids = torch.randint(0, config.vocab_size, (1, 5))
        with self.assertRaises(ValueError):
            model(input_ids)

    def test_initialization_scale_and_zero_biases(self):
        torch.manual_seed(2)
        config = self.small_config()
        model = submission.GPTModel(config)
        linear_weights = []
        linear_biases = []
        for module in model.modules():
            if isinstance(module, nn.Linear):
                linear_weights.append(module.weight.detach().flatten())
                if module.bias is not None:
                    linear_biases.append(module.bias.detach().flatten())
        weights = torch.cat(linear_weights)
        self.assertLess(abs(weights.mean().item()), 0.01)
        self.assertLess(abs(weights.std().item() - 0.02), 0.01)
        if linear_biases:
            self.assertTrue(torch.allclose(torch.cat(linear_biases), torch.zeros_like(torch.cat(linear_biases))))

    def test_default_gpt2_small_parameter_count_without_forward(self):
        config = submission.GPTConfig(dropout=0.0)
        model = submission.GPTModel(config)
        self.assertEqual(submission.count_parameters(model), 124_439_808)
        groups = submission.parameter_breakdown(model)
        self.assertEqual(groups["token_embedding"], 50_257 * 768)
        self.assertEqual(groups["position_embedding"], 1_024 * 768)
        self.assertEqual(groups["lm_head"], 0)
        self.assertEqual(groups["total"], 124_439_808)


@unittest.skipIf(torch is None, "PyTorch is required for Ch06 GPT tests")
class TestCausalAttention(unittest.TestCase):
    def test_attention_is_causal(self):
        torch.manual_seed(3)
        config = submission.GPTConfig(
            vocab_size=19,
            max_seq_len=6,
            d_model=12,
            n_heads=3,
            n_layers=1,
            dropout=0.0,
        )
        attn = submission.CausalSelfAttention(config)
        x = torch.randn(2, 5, config.d_model)
        out, weights = attn(x)
        self.assertEqual(tuple(out.shape), (2, 5, config.d_model))
        self.assertEqual(tuple(weights.shape), (2, config.n_heads, 5, 5))
        future = torch.triu(torch.ones(5, 5, dtype=torch.bool), diagonal=1)
        self.assertTrue(torch.all(weights[:, :, future] < 1e-6))
        self.assertTrue(torch.allclose(weights.sum(dim=-1), torch.ones(2, config.n_heads, 5), atol=1e-6))


@unittest.skipIf(torch is None, "PyTorch is required for Ch06 GPT tests")
class TestMoERouter(unittest.TestCase):
    def test_moe_parameter_budget_distinguishes_total_and_activated(self):
        budget = submission.moe_parameter_budget(
            d_model=16,
            expert_hidden=32,
            n_routed_experts=8,
            top_k=2,
            shared_experts=1,
        )
        expert_params = 3 * 16 * 32
        self.assertEqual(budget["expert_params"], expert_params)
        self.assertEqual(budget["router_params"], 16 * 8)
        self.assertEqual(budget["total_expert_params"], 9 * expert_params)
        self.assertEqual(budget["total_params"], 9 * expert_params + 16 * 8)
        self.assertEqual(budget["activated_expert_params_per_token"], 3 * expert_params)
        self.assertAlmostEqual(budget["activated_fraction_of_experts"], 3 / 9)
        self.assertLess(budget["activated_fraction_of_total_params"], 1.0)
        self.assertAlmostEqual(budget["capacity_to_compute_ratio"], 3.0)

    def test_moe_parameter_budget_validates_inputs(self):
        bad_kwargs = [
            dict(d_model=0, expert_hidden=32, n_routed_experts=8, top_k=2),
            dict(d_model=16, expert_hidden=0, n_routed_experts=8, top_k=2),
            dict(d_model=16, expert_hidden=32, n_routed_experts=8, top_k=0),
            dict(d_model=16, expert_hidden=32, n_routed_experts=8, top_k=9),
            dict(d_model=16, expert_hidden=32, n_routed_experts=8, top_k=2, shared_experts=-1),
        ]
        for kwargs in bad_kwargs:
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    submission.moe_parameter_budget(**kwargs)

    def test_router_topk_shapes_and_normalization(self):
        torch.manual_seed(4)
        router = submission.MoERouter(d_model=10, n_experts=7, top_k=3)
        x = torch.randn(2, 4, 10)
        weights, indices = router(x)
        self.assertEqual(tuple(weights.shape), (2, 4, 3))
        self.assertEqual(tuple(indices.shape), (2, 4, 3))
        self.assertTrue(torch.allclose(weights.sum(dim=-1), torch.ones(2, 4), atol=1e-6))
        self.assertTrue(torch.all((indices >= 0) & (indices < 7)))

    def test_balancer_moves_bias_against_overloaded_expert(self):
        balancer = submission.AuxLossFreeBalancer(n_experts=4, bias_update_rate=0.04, bias_clip=0.1)
        counts = torch.tensor([80, 10, 5, 5])
        balancer.update(counts)
        self.assertLess(balancer.bias[0].item(), 0.0)
        self.assertGreater(balancer.bias[2].item(), 0.0)
        stats = balancer.get_load_stats(counts)
        self.assertAlmostEqual(stats["ideal_load"], 0.25)
        self.assertGreater(stats["max_load"], stats["min_load"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
