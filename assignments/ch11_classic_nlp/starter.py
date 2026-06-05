"""Starter code for the classic NLP and evaluation supplemental assignment."""

from collections import Counter
import math
import re
import string


def attachment_scores(gold_heads, gold_labels, pred_heads, pred_labels):
    """Return UAS/LAS metrics for one dependency-parsed sentence."""
    raise NotImplementedError


def sentence_bleu(candidate, references, max_n=4):
    """Compute sentence BLEU with clipped n-gram precision."""
    raise NotImplementedError


def rouge_l_f1(candidate, reference):
    """Compute ROUGE-L precision, recall, and F1 for token lists."""
    raise NotImplementedError


def normalize_answer(text):
    """Lowercase, remove punctuation/articles, and normalize whitespace."""
    raise NotImplementedError


def exact_match_and_f1(prediction, gold_answers):
    """Return best exact match and token F1 over multiple gold answers."""
    raise NotImplementedError


def build_mlm_example(tokens, mask_positions, mask_token="[MASK]"):
    """Build BERT-style MLM input tokens and labels.

    Labels should contain the original token at masked positions and None
    elsewhere.
    """
    raise NotImplementedError
