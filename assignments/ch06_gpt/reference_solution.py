"""Reference solution for Chapter 6 GPT model assembly assignment."""

import math
from dataclasses import dataclass
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class GPTConfig:
    vocab_size: int = 50257
    max_seq_len: int = 1024
    d_model: int = 768
    n_heads: int = 12
    n_layers: int = 12
    d_ff: Optional[int] = None
    dropout: float = 0.1
    bias: bool = True
    tie_weights: bool = True


class CausalSelfAttention(nn.Module):
    def __init__(self, config: GPTConfig):
        super().__init__()
        assert config.d_model % config.n_heads == 0
        self.n_heads = config.n_heads
        self.d_head = config.d_model // config.n_heads
        self.c_attn = nn.Linear(config.d_model, 3 * config.d_model, bias=config.bias)
        self.c_proj = nn.Linear(config.d_model, config.d_model, bias=config.bias)
        self.attn_dropout = nn.Dropout(config.dropout)
        self.resid_dropout = nn.Dropout(config.dropout)

    def forward(self, x, mask=None):
        batch_size, seq_len, d_model = x.shape
        qkv = self.c_attn(x)
        q, k, v = qkv.split(d_model, dim=-1)
        q = q.view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        k = k.view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        v = v.view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)

        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.d_head)
        causal_mask = torch.ones(seq_len, seq_len, dtype=torch.bool, device=x.device).tril()
        scores = scores.masked_fill(~causal_mask.view(1, 1, seq_len, seq_len), torch.finfo(scores.dtype).min)
        if mask is not None:
            if mask.dtype != torch.bool:
                mask = mask != 0
            while mask.dim() < scores.dim():
                mask = mask.unsqueeze(0)
            scores = scores.masked_fill(~mask, torch.finfo(scores.dtype).min)

        weights = F.softmax(scores, dim=-1)
        weights = self.attn_dropout(weights)
        out = torch.matmul(weights, v)
        out = out.transpose(1, 2).contiguous().view(batch_size, seq_len, d_model)
        out = self.resid_dropout(self.c_proj(out))
        return out, weights


class GPT2MLP(nn.Module):
    def __init__(self, config: GPTConfig):
        super().__init__()
        d_ff = config.d_ff or 4 * config.d_model
        self.c_fc = nn.Linear(config.d_model, d_ff, bias=config.bias)
        self.c_proj = nn.Linear(d_ff, config.d_model, bias=config.bias)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x):
        return self.dropout(self.c_proj(F.gelu(self.c_fc(x), approximate="tanh")))


class GPT2Block(nn.Module):
    def __init__(self, config: GPTConfig):
        super().__init__()
        self.ln_1 = nn.LayerNorm(config.d_model, bias=config.bias)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = nn.LayerNorm(config.d_model, bias=config.bias)
        self.mlp = GPT2MLP(config)

    def forward(self, x, mask=None):
        attn_out, _ = self.attn(self.ln_1(x), mask=mask)
        x = x + attn_out
        x = x + self.mlp(self.ln_2(x))
        return x


class GPTModel(nn.Module):
    def __init__(self, config: GPTConfig):
        super().__init__()
        self.config = config
        self.token_embedding = nn.Embedding(config.vocab_size, config.d_model)
        self.pos_embedding = nn.Embedding(config.max_seq_len, config.d_model)
        self.dropout = nn.Dropout(config.dropout)
        self.blocks = nn.ModuleList([GPT2Block(config) for _ in range(config.n_layers)])
        self.norm = nn.LayerNorm(config.d_model, bias=config.bias)
        self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)

        self.apply(self._init_weights)
        if config.tie_weights:
            self.lm_head.weight = self.token_embedding.weight

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, input_ids, mask=None):
        batch_size, seq_len = input_ids.shape
        if seq_len > self.config.max_seq_len:
            raise ValueError(f"sequence length {seq_len} exceeds max_seq_len={self.config.max_seq_len}")

        pos_ids = torch.arange(seq_len, device=input_ids.device).unsqueeze(0)
        x = self.token_embedding(input_ids) + self.pos_embedding(pos_ids)
        x = self.dropout(x)
        for block in self.blocks:
            x = block(x, mask=mask)
        x = self.norm(x)
        return self.lm_head(x)


def count_parameters(model):
    return sum(p.numel() for p in model.parameters())


def parameter_breakdown(model):
    groups = {
        "token_embedding": 0,
        "position_embedding": 0,
        "blocks": 0,
        "final_norm": 0,
        "lm_head": 0,
    }
    for name, param in model.named_parameters():
        if name.startswith("token_embedding"):
            groups["token_embedding"] += param.numel()
        elif name.startswith("pos_embedding"):
            groups["position_embedding"] += param.numel()
        elif name.startswith("blocks"):
            groups["blocks"] += param.numel()
        elif name.startswith("norm"):
            groups["final_norm"] += param.numel()
        elif name.startswith("lm_head"):
            groups["lm_head"] += param.numel()
    groups["total"] = sum(groups.values())
    return groups


def causal_lm_loss_from_logits(logits, input_ids, ignore_index=-100):
    if logits.dim() != 3:
        raise ValueError("logits must have shape [B, T, V]")
    if input_ids.dim() != 2:
        raise ValueError("input_ids must have shape [B, T]")
    if logits.shape[:2] != input_ids.shape:
        raise ValueError("logits and input_ids must agree on batch and sequence dimensions")
    if logits.size(1) < 2:
        raise ValueError("sequence length must be at least 2")

    vocab_size = logits.size(-1)
    labels = input_ids[:, 1:].contiguous()
    if not torch.any(labels != ignore_index):
        raise ValueError("at least one next-token label must be valid")
    shift_logits = logits[:, :-1, :].contiguous()
    return F.cross_entropy(
        shift_logits.view(-1, vocab_size),
        labels.view(-1),
        ignore_index=ignore_index,
    )


def tied_lm_head_gradients(hidden_states, embedding_weight, target_ids, ignore_index=-100):
    """Return (loss, d_hidden, d_embedding) for logits = hidden_states @ embedding_weight.T."""
    if hidden_states.dim() != 2:
        raise ValueError("hidden_states must have shape [N, D]")
    if embedding_weight.dim() != 2:
        raise ValueError("embedding_weight must have shape [V, D]")
    if target_ids.dim() != 1:
        raise ValueError("target_ids must have shape [N]")
    if hidden_states.size(0) != target_ids.size(0) or hidden_states.size(1) != embedding_weight.size(1):
        raise ValueError("hidden_states, embedding_weight, and target_ids shapes are incompatible")

    valid = target_ids != ignore_index
    if not torch.any(valid):
        raise ValueError("at least one target id must be valid")
    if torch.any((target_ids[valid] < 0) | (target_ids[valid] >= embedding_weight.size(0))):
        raise ValueError("target id out of vocabulary range")

    logits = hidden_states @ embedding_weight.T
    loss = F.cross_entropy(logits, target_ids, ignore_index=ignore_index)

    probs = F.softmax(logits, dim=-1)
    grad_logits = probs
    grad_logits[valid, target_ids[valid]] -= 1.0
    grad_logits[~valid] = 0.0
    grad_logits = grad_logits / valid.sum()

    grad_hidden = grad_logits @ embedding_weight
    grad_embedding = grad_logits.T @ hidden_states
    return loss, grad_hidden, grad_embedding


def moe_parameter_budget(
    d_model,
    expert_hidden,
    n_routed_experts,
    top_k,
    shared_experts=0,
    router_bias=False,
):
    if d_model <= 0 or expert_hidden <= 0 or n_routed_experts <= 0:
        raise ValueError("d_model, expert_hidden and n_routed_experts must be positive")
    if not 1 <= top_k <= n_routed_experts:
        raise ValueError("top_k must satisfy 1 <= top_k <= n_routed_experts")
    if shared_experts < 0:
        raise ValueError("shared_experts must be non-negative")

    expert_params = 3 * d_model * expert_hidden
    router_params = d_model * n_routed_experts
    if router_bias:
        router_params += n_routed_experts

    total_experts = n_routed_experts + shared_experts
    activated_experts = top_k + shared_experts
    total_expert_params = total_experts * expert_params
    activated_expert_params_per_token = activated_experts * expert_params
    total_params = total_expert_params + router_params

    return {
        "expert_params": expert_params,
        "router_params": router_params,
        "total_expert_params": total_expert_params,
        "total_params": total_params,
        "activated_expert_params_per_token": activated_expert_params_per_token,
        "activated_fraction_of_experts": activated_experts / total_experts,
        "activated_fraction_of_total_params": activated_expert_params_per_token / total_params,
        "capacity_to_compute_ratio": total_expert_params / activated_expert_params_per_token,
    }


def moe_load_balance_loss(router_probs, expert_indices, n_experts=None):
    if router_probs.dim() < 2:
        raise ValueError("router_probs must have an expert dimension")
    if expert_indices.shape[:-1] != router_probs.shape[:-1]:
        raise ValueError("expert_indices must match router_probs except for the top-k dimension")
    if n_experts is None:
        n_experts = router_probs.size(-1)
    if n_experts <= 0 or n_experts != router_probs.size(-1):
        raise ValueError("n_experts must match router_probs.size(-1)")
    if expert_indices.numel() == 0:
        raise ValueError("expert_indices must be non-empty")
    if torch.any((expert_indices < 0) | (expert_indices >= n_experts)):
        raise ValueError("expert_indices contains invalid expert ids")
    prob_sums = router_probs.sum(dim=-1)
    if not torch.allclose(prob_sums, torch.ones_like(prob_sums), atol=1e-5):
        raise ValueError("router_probs must sum to 1 over experts")

    flat_probs = router_probs.reshape(-1, n_experts).float()
    flat_indices = expert_indices.reshape(-1).long()
    token_count = flat_probs.size(0)
    assignment_count = flat_indices.numel()
    assignment_counts = torch.bincount(flat_indices, minlength=n_experts).to(flat_probs.dtype)
    load_fraction = assignment_counts / float(assignment_count)
    mean_router_prob = flat_probs.mean(dim=0)
    loss = n_experts * torch.sum(load_fraction * mean_router_prob)
    return {
        "loss": loss,
        "load_fraction": load_fraction,
        "mean_router_prob": mean_router_prob,
        "assignment_counts": assignment_counts,
        "token_count": token_count,
        "assignment_count": assignment_count,
    }


class MoERouter(nn.Module):
    def __init__(self, d_model, n_experts=256, top_k=8):
        super().__init__()
        assert 1 <= top_k <= n_experts
        self.n_experts = n_experts
        self.top_k = top_k
        self.gate = nn.Linear(d_model, n_experts, bias=False)

    def forward(self, x, bias=None):
        logits = self.gate(x)
        if bias is not None:
            logits = logits + bias.to(logits.device).view(1, 1, -1)
        weights = F.softmax(logits, dim=-1)
        top_weights, top_indices = torch.topk(weights, self.top_k, dim=-1)
        top_weights = top_weights / top_weights.sum(dim=-1, keepdim=True)
        return top_weights, top_indices


class AuxLossFreeBalancer:
    def __init__(self, n_experts, bias_update_rate=0.01, bias_clip=0.1):
        self.n_experts = n_experts
        self.bias_update_rate = bias_update_rate
        self.bias_clip = bias_clip
        self.bias = torch.zeros(n_experts)

    def update(self, token_counts):
        total = token_counts.sum().float()
        if total == 0:
            return
        load_ratio = token_counts.float() / total
        target_load = 1.0 / self.n_experts
        self.bias += self.bias_update_rate * (target_load - load_ratio)
        self.bias.clamp_(-self.bias_clip, self.bias_clip)

    def apply_bias(self, gate_logits):
        return gate_logits + self.bias.to(gate_logits.device)

    def get_load_stats(self, token_counts):
        total = token_counts.sum().float()
        load_ratio = token_counts.float() / total if total > 0 else token_counts.float()
        return {
            "max_load": load_ratio.max().item(),
            "min_load": load_ratio.min().item(),
            "std_load": load_ratio.std().item(),
            "ideal_load": 1.0 / self.n_experts,
        }
