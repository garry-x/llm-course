"""Reference solution for Chapter 1 BPE tokenizer assignment."""

import math


def _get_stats(ids):
    stats = {}
    for pair in zip(ids, ids[1:]):
        stats[pair] = stats.get(pair, 0) + 1
    return stats


def _merge(ids, pair, new_id):
    new_ids = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and (ids[i], ids[i + 1]) == pair:
            new_ids.append(new_id)
            i += 2
        else:
            new_ids.append(ids[i])
            i += 1
    return new_ids


class BPETokenizer:
    """Minimal byte-level BPE tokenizer."""

    def __init__(self):
        self.vocab = {i: bytes([i]) for i in range(256)}
        self.merges = {}

    def train(self, text, vocab_size):
        if vocab_size < 256:
            raise ValueError("vocab_size must be >= 256")

        ids = list(text.encode("utf-8"))
        num_merges = vocab_size - 256

        for i in range(num_merges):
            stats = _get_stats(ids)
            if not stats:
                break
            pair = max(stats, key=stats.get)
            new_id = 256 + i
            self.merges[pair] = new_id
            self.vocab[new_id] = self.vocab[pair[0]] + self.vocab[pair[1]]
            ids = _merge(ids, pair, new_id)

        return ids

    def encode(self, text):
        ids = list(text.encode("utf-8"))
        while len(ids) >= 2:
            stats = _get_stats(ids)
            pair = min(stats, key=lambda p: self.merges.get(p, float("inf")))
            if pair not in self.merges:
                break
            ids = _merge(ids, pair, self.merges[pair])
        return ids

    def decode(self, ids):
        tokens = b"".join(self.vocab[idx] for idx in ids)
        return tokens.decode("utf-8", errors="replace")


def tokenizer_report(tokenizer, texts, vocab_size=None, d_model=None):
    if not texts:
        raise ValueError("texts must not be empty")

    token_lengths = []
    char_lengths = []
    round_trip_ok = 0
    for text in texts:
        encoded = tokenizer.encode(text)
        token_lengths.append(len(encoded))
        char_lengths.append(len(text))
        if tokenizer.decode(encoded) == text:
            round_trip_ok += 1

    sorted_lengths = sorted(token_lengths)
    p95_index = min(len(sorted_lengths) - 1, math.ceil(0.95 * len(sorted_lengths)) - 1)
    total_chars = sum(char_lengths)
    result = {
        "num_texts": len(texts),
        "total_tokens": sum(token_lengths),
        "avg_tokens": sum(token_lengths) / len(token_lengths),
        "p95_tokens": sorted_lengths[p95_index],
        "tokens_per_character": sum(token_lengths) / total_chars if total_chars else 0.0,
        "round_trip_success_rate": round_trip_ok / len(texts),
    }
    if vocab_size is not None and d_model is not None:
        result["embedding_params"] = int(vocab_size) * int(d_model)
    return result


def tokenizer_group_report(tokenizer, groups, vocab_size=None, d_model=None):
    if not groups:
        raise ValueError("groups must not be empty")

    group_reports = {}
    for name, texts in groups.items():
        if not texts:
            raise ValueError("each group must contain at least one text")
        group_reports[name] = tokenizer_report(tokenizer, texts, vocab_size=vocab_size, d_model=d_model)

    rates = {
        name: report["tokens_per_character"]
        for name, report in group_reports.items()
    }
    max_group = max(rates, key=rates.get)
    min_group = min(rates, key=rates.get)
    min_rate = rates[min_group]
    return {
        "groups": group_reports,
        "max_tokens_per_character_group": max_group,
        "min_tokens_per_character_group": min_group,
        "tokens_per_character_disparity": float("inf") if min_rate == 0 else rates[max_group] / min_rate,
    }


def bpe_training_trace(text, vocab_size, max_steps=None):
    if vocab_size < 256:
        raise ValueError("vocab_size must be >= 256")
    if max_steps is not None and max_steps <= 0:
        raise ValueError("max_steps must be positive when provided")

    ids = list(text.encode("utf-8"))
    vocab = {i: bytes([i]) for i in range(256)}
    steps = []
    num_merges = vocab_size - 256
    if max_steps is not None:
        num_merges = min(num_merges, int(max_steps))

    initial_length = len(ids)
    for step in range(num_merges):
        stats = _get_stats(ids)
        if not stats:
            break
        pair = max(stats, key=stats.get)
        new_id = 256 + step
        before_length = len(ids)
        before_count = stats[pair]
        vocab[new_id] = vocab[pair[0]] + vocab[pair[1]]
        ids = _merge(ids, pair, new_id)
        after_length = len(ids)
        steps.append(
            {
                "step": step,
                "pair": pair,
                "count": before_count,
                "new_id": new_id,
                "token_bytes": vocab[new_id],
                "token_text": vocab[new_id].decode("utf-8", errors="replace"),
                "before_length": before_length,
                "after_length": after_length,
                "tokens_saved": before_length - after_length,
            }
        )

    return {
        "initial_length": initial_length,
        "final_length": len(ids),
        "total_tokens_saved": initial_length - len(ids),
        "compression_ratio": len(ids) / initial_length if initial_length else 0.0,
        "final_ids": ids,
        "steps": steps,
    }
