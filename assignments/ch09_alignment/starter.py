"""Starter code for Chapter 9 fine-tuning and alignment assignment."""

import torch
import torch.nn as nn


class SFTDataset(torch.utils.data.Dataset):
    def __init__(self, data, tokenizer, max_len=1024):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, idx):
        raise NotImplementedError


def sft_collate_fn(batch, pad_id=0):
    raise NotImplementedError


def sft_loss_from_logits(logits, labels):
    raise NotImplementedError


class LoRALinear(nn.Module):
    def __init__(self, base_layer, r=8, alpha=16.0, dropout=0.0):
        super().__init__()
        raise NotImplementedError

    def forward(self, x):
        raise NotImplementedError

    def delta_weight(self):
        raise NotImplementedError


def apply_lora(model, r=8, alpha=16.0, target_modules=None):
    raise NotImplementedError


def count_trainable_parameters(model):
    raise NotImplementedError


def sequence_log_probs(model, input_ids, attention_mask, labels):
    raise NotImplementedError


def dpo_loss(policy_chosen_logps, policy_rejected_logps, ref_chosen_logps, ref_rejected_logps, beta=0.1):
    raise NotImplementedError


def grpo_advantages(rewards, eps=1e-8):
    raise NotImplementedError


def merge_lora(base_model, lora_weights):
    raise NotImplementedError
