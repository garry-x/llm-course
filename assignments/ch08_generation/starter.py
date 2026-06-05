"""Starter code for Chapter 8 text-generation assignment."""

import torch


def sample_next_token(logits, strategy="greedy", temperature=1.0, k=40, p=0.9):
    raise NotImplementedError


def top_p_filter(logits, p=0.9):
    raise NotImplementedError


def generate_greedy(model, input_ids, max_new_tokens=100, eos_token_id=None):
    raise NotImplementedError


def generate_temperature(model, input_ids, max_new_tokens=100, temperature=1.0, eos_token_id=None):
    raise NotImplementedError


def generate_topk(model, input_ids, max_new_tokens=100, k=40, temperature=1.0, eos_token_id=None):
    raise NotImplementedError


def generate_topp(model, input_ids, max_new_tokens=100, p=0.9, temperature=1.0, eos_token_id=None):
    raise NotImplementedError


class Generator:
    def __init__(self, model, tokenizer):
        raise NotImplementedError

    def generate(self, prompt, strategy="top-p", max_new_tokens=100, temperature=0.8, k=40, p=0.9):
        raise NotImplementedError

    def distinct_ngrams(self, text, n=2):
        raise NotImplementedError


def speculative_decoding(target_model, draft_model, input_ids, gamma=4, max_new_tokens=100, eos_token_id=None):
    raise NotImplementedError
