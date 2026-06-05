"""Reference solution for Chapter 9 fine-tuning and alignment assignment."""

import torch
import torch.nn as nn
import torch.nn.functional as F


class SFTDataset(torch.utils.data.Dataset):
    def __init__(self, data, tokenizer, max_len=1024):
        self.input_ids = []
        self.labels = []
        self.pad_token_id = getattr(tokenizer, "pad_token_id", 0)
        eos = getattr(tokenizer, "eos_token", "")

        for item in data:
            prompt = tokenizer.apply_chat_template(
                [{"role": "user", "content": item["instruction"]}],
                tokenize=False,
            )
            full_text = prompt + item["response"] + eos
            input_ids = tokenizer.encode(full_text)[:max_len]
            prompt_len = min(len(tokenizer.encode(prompt)), len(input_ids))
            labels = torch.tensor(input_ids, dtype=torch.long)
            labels[:prompt_len] = -100
            labels[labels == self.pad_token_id] = -100
            self.input_ids.append(torch.tensor(input_ids, dtype=torch.long))
            self.labels.append(labels)

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return {"input_ids": self.input_ids[idx], "labels": self.labels[idx]}


def sft_collate_fn(batch, pad_id=0):
    input_ids = [item["input_ids"] for item in batch]
    labels = [item["labels"] for item in batch]
    input_ids = torch.nn.utils.rnn.pad_sequence(input_ids, batch_first=True, padding_value=pad_id)
    labels = torch.nn.utils.rnn.pad_sequence(labels, batch_first=True, padding_value=-100)
    return {
        "input_ids": input_ids,
        "labels": labels,
        "attention_mask": (input_ids != pad_id).long(),
    }


def sft_loss_from_logits(logits, labels):
    shift_logits = logits[:, :-1, :].contiguous()
    shift_labels = labels[:, 1:].contiguous()
    return F.cross_entropy(
        shift_logits.reshape(-1, shift_logits.size(-1)),
        shift_labels.reshape(-1),
        ignore_index=-100,
    )


class LoRALinear(nn.Module):
    def __init__(self, base_layer, r=8, alpha=16.0, dropout=0.0):
        super().__init__()
        if not isinstance(base_layer, nn.Linear):
            raise TypeError("base_layer must be nn.Linear")
        if r <= 0:
            raise ValueError("r must be positive")
        self.in_features = base_layer.in_features
        self.out_features = base_layer.out_features
        self.r = r
        self.scaling = alpha / r
        self.dropout = nn.Dropout(dropout)
        self.weight = nn.Parameter(base_layer.weight.detach().clone(), requires_grad=False)
        if base_layer.bias is None:
            self.bias = None
        else:
            self.bias = nn.Parameter(base_layer.bias.detach().clone(), requires_grad=False)
        self.A = nn.Parameter(torch.randn(r, self.in_features) * 0.01)
        self.B = nn.Parameter(torch.zeros(self.out_features, r))

    def forward(self, x):
        base = F.linear(x, self.weight, self.bias)
        lora = F.linear(F.linear(self.dropout(x), self.A), self.B) * self.scaling
        return base + lora

    def delta_weight(self):
        return (self.B @ self.A) * self.scaling


def _replace_child(parent, child_name, new_module):
    setattr(parent, child_name, new_module)


def apply_lora(model, r=8, alpha=16.0, target_modules=None):
    if target_modules is None:
        target_modules = ["q_proj", "v_proj"]
    target_modules = set(target_modules)

    for _name, param in model.named_parameters():
        param.requires_grad = False

    def convert(module):
        for child_name, child in list(module.named_children()):
            if child_name in target_modules and isinstance(child, nn.Linear):
                _replace_child(module, child_name, LoRALinear(child, r=r, alpha=alpha))
            else:
                convert(child)

    convert(model)
    for module in model.modules():
        if isinstance(module, LoRALinear):
            module.A.requires_grad = True
            module.B.requires_grad = True
    return model


def count_trainable_parameters(model):
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return {"total": total, "trainable": trainable}


def sequence_log_probs(model, input_ids, attention_mask, labels):
    outputs = model(input_ids=input_ids, attention_mask=attention_mask)
    logits = outputs.logits if hasattr(outputs, "logits") else outputs
    shift_logits = logits[:, :-1, :].contiguous()
    shift_labels = labels[:, 1:].contiguous()
    valid = shift_labels != -100
    safe_labels = shift_labels.masked_fill(~valid, 0)
    log_probs = F.log_softmax(shift_logits, dim=-1)
    token_logps = log_probs.gather(dim=-1, index=safe_labels.unsqueeze(-1)).squeeze(-1)
    return (token_logps * valid.float()).sum(dim=1)


def dpo_loss(policy_chosen_logps, policy_rejected_logps, ref_chosen_logps, ref_rejected_logps, beta=0.1):
    chosen_ratio = policy_chosen_logps - ref_chosen_logps
    rejected_ratio = policy_rejected_logps - ref_rejected_logps
    logits = beta * (chosen_ratio - rejected_ratio)
    loss = -F.logsigmoid(logits).mean()
    acc = (logits > 0).float().mean().item()
    return loss, acc


def approx_kl_from_logps(policy_logps, ref_logps, mask=None, reduction="mean"):
    if policy_logps.shape != ref_logps.shape:
        raise ValueError("policy_logps and ref_logps must have the same shape")
    if reduction not in {"mean", "sum", "none"}:
        raise ValueError("reduction must be 'mean', 'sum', or 'none'")
    if mask is not None and mask.shape != policy_logps.shape:
        raise ValueError("mask must have the same shape as log probabilities")

    log_ratio = ref_logps - policy_logps
    kl = torch.exp(log_ratio) - log_ratio - 1.0
    if mask is None:
        if reduction == "none":
            return kl
        if reduction == "sum":
            return kl.sum()
        return kl.mean()

    mask = mask.to(dtype=kl.dtype, device=kl.device)
    kl = kl * mask
    if reduction == "none":
        return kl
    if reduction == "sum":
        return kl.sum()
    valid = mask.sum()
    if valid <= 0:
        raise ValueError("mask must contain at least one valid token for mean reduction")
    return kl.sum() / valid


def pairwise_reward_loss(chosen_rewards, rejected_rewards):
    if chosen_rewards.shape != rejected_rewards.shape:
        raise ValueError("chosen_rewards and rejected_rewards must have the same shape")
    logits = chosen_rewards - rejected_rewards
    loss = -F.logsigmoid(logits).mean()
    acc = (logits > 0).float().mean().item()
    return loss, acc


def preference_length_bias(chosen_lengths, rejected_lengths):
    if chosen_lengths.shape != rejected_lengths.shape:
        raise ValueError("chosen_lengths and rejected_lengths must have the same shape")
    diff = chosen_lengths.float() - rejected_lengths.float()
    return {
        "mean_length_delta": diff.mean().item(),
        "chosen_longer_rate": (diff > 0).float().mean().item(),
        "rejected_longer_rate": (diff < 0).float().mean().item(),
        "tie_rate": (diff == 0).float().mean().item(),
    }


def ppo_clipped_policy_loss(new_logps, old_logps, advantages, mask=None, clip_range=0.2):
    if new_logps.shape != old_logps.shape or new_logps.shape != advantages.shape:
        raise ValueError("new_logps, old_logps and advantages must have the same shape")
    if clip_range <= 0:
        raise ValueError("clip_range must be positive")
    if mask is not None and mask.shape != new_logps.shape:
        raise ValueError("mask must have the same shape as log probabilities")

    log_ratio = new_logps - old_logps
    ratio = torch.exp(log_ratio)
    unclipped = ratio * advantages
    clipped_ratio = ratio.clamp(1.0 - clip_range, 1.0 + clip_range)
    clipped = clipped_ratio * advantages
    surrogate = torch.minimum(unclipped, clipped)
    clipped_mask = (torch.abs(ratio - 1.0) > clip_range).float()
    approx_kl = (ratio - 1.0) - log_ratio

    if mask is None:
        loss = -surrogate.mean()
        stats_mask = torch.ones_like(surrogate)
    else:
        stats_mask = mask.to(dtype=surrogate.dtype, device=surrogate.device)
        valid = stats_mask.sum()
        if valid <= 0:
            raise ValueError("mask must contain at least one valid token")
        loss = -(surrogate * stats_mask).sum() / valid

    denom = stats_mask.sum()
    stats = {
        "mean_ratio": ((ratio * stats_mask).sum() / denom).item(),
        "clip_fraction": ((clipped_mask * stats_mask).sum() / denom).item(),
        "approx_kl": ((approx_kl * stats_mask).sum() / denom).item(),
    }
    return loss, stats


def grpo_advantages(rewards, eps=1e-8):
    if rewards.dim() == 1:
        mean = rewards.mean()
        std = rewards.std(unbiased=False)
        return (rewards - mean) / (std + eps)
    if rewards.dim() == 2:
        mean = rewards.mean(dim=0, keepdim=True)
        std = rewards.std(dim=0, keepdim=True, unbiased=False)
        return (rewards - mean) / (std + eps)
    raise ValueError("rewards must be 1D or 2D")


def merge_lora(base_model, lora_weights):
    modules = dict(base_model.named_modules())
    for name, params in lora_weights.items():
        module = modules.get(name)
        if module is None or not hasattr(module, "weight"):
            continue
        A = params["A"].to(module.weight.device)
        B = params["B"].to(module.weight.device)
        scaling = params.get("scaling", 1.0)
        delta = (B @ A) * scaling
        if delta.shape != module.weight.shape:
            delta = delta.T
        module.weight.data.add_(delta.to(module.weight.dtype))
    return base_model
