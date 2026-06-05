"""Starter code for Chapter 1 BPE tokenizer assignment.

Students should implement the TODO functions/classes and run:

    STUDENT_MODULE=student_solution .venv/bin/python assignments/ch01_bpe/tests.py
"""

import math


def _get_stats(ids):
    """Return a dict mapping adjacent token pairs to their frequency.

    Example:
        [1, 2, 1, 2, 3] -> {(1, 2): 2, (2, 1): 1, (2, 3): 1}
    """
    raise NotImplementedError


def _merge(ids, pair, new_id):
    """Replace non-overlapping occurrences of pair with new_id."""
    raise NotImplementedError


class BPETokenizer:
    """Minimal byte-level BPE tokenizer."""

    def __init__(self):
        self.vocab = {i: bytes([i]) for i in range(256)}
        self.merges = {}

    def train(self, text, vocab_size):
        """Train merges on text until vocab_size is reached or no pairs remain."""
        raise NotImplementedError

    def encode(self, text):
        """Encode text into token ids using learned merges."""
        raise NotImplementedError

    def decode(self, ids):
        """Decode token ids back into a UTF-8 string."""
        raise NotImplementedError


def tokenizer_report(tokenizer, texts, vocab_size=None, d_model=None):
    """Return token-count, round-trip, and embedding-budget statistics for texts."""
    raise NotImplementedError


def tokenizer_group_report(tokenizer, groups, vocab_size=None, d_model=None):
    """Return per-group token-cost statistics and cross-group disparity."""
    raise NotImplementedError
