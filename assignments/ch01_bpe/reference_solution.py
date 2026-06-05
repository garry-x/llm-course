"""Reference solution for Chapter 1 BPE tokenizer assignment."""


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
