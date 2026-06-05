"""Reference solution for the classic NLP and evaluation assignment."""

from collections import Counter
import math
import re
import string


def attachment_scores(gold_heads, gold_labels, pred_heads, pred_labels):
    if not (
        len(gold_heads)
        == len(gold_labels)
        == len(pred_heads)
        == len(pred_labels)
    ):
        raise ValueError("gold and predicted heads/labels must have equal length")
    total = len(gold_heads)
    if total == 0:
        raise ValueError("at least one token is required")

    correct_heads = 0
    correct_labels = 0
    for gh, gl, ph, pl in zip(gold_heads, gold_labels, pred_heads, pred_labels):
        head_ok = gh == ph
        label_ok = head_ok and gl == pl
        correct_heads += int(head_ok)
        correct_labels += int(label_ok)

    return {
        "total": total,
        "correct_heads": correct_heads,
        "correct_labels": correct_labels,
        "uas": correct_heads / total,
        "las": correct_labels / total,
    }


def _ngrams(tokens, n):
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def sentence_bleu(candidate, references, max_n=4):
    if max_n <= 0:
        raise ValueError("max_n must be positive")
    if not references:
        raise ValueError("at least one reference is required")
    if len(candidate) == 0:
        return 0.0

    precisions = []
    for n in range(1, max_n + 1):
        cand_counts = Counter(_ngrams(candidate, n))
        if not cand_counts:
            precisions.append(0.0)
            continue

        max_ref_counts = Counter()
        for ref in references:
            ref_counts = Counter(_ngrams(ref, n))
            for gram, count in ref_counts.items():
                max_ref_counts[gram] = max(max_ref_counts[gram], count)

        clipped = sum(min(count, max_ref_counts[gram]) for gram, count in cand_counts.items())
        precisions.append(clipped / sum(cand_counts.values()))

    if any(p == 0.0 for p in precisions):
        return 0.0

    cand_len = len(candidate)
    ref_lens = [len(ref) for ref in references]
    closest_ref_len = min(ref_lens, key=lambda ref_len: (abs(ref_len - cand_len), ref_len))
    brevity_penalty = 1.0 if cand_len > closest_ref_len else math.exp(1 - closest_ref_len / cand_len)
    geo_mean = math.exp(sum(math.log(p) for p in precisions) / max_n)
    return brevity_penalty * geo_mean


def _lcs_length(left, right):
    rows = len(left) + 1
    cols = len(right) + 1
    dp = [[0] * cols for _ in range(rows)]
    for i, left_token in enumerate(left, start=1):
        for j, right_token in enumerate(right, start=1):
            if left_token == right_token:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]


def rouge_l_f1(candidate, reference):
    if not candidate or not reference:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0, "lcs": 0}

    lcs = _lcs_length(candidate, reference)
    precision = lcs / len(candidate)
    recall = lcs / len(reference)
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    return {"precision": precision, "recall": recall, "f1": f1, "lcs": lcs}


def normalize_answer(text):
    def remove_articles(value):
        return re.sub(r"\b(a|an|the)\b", " ", value)

    def remove_punc(value):
        return "".join(ch for ch in value if ch not in string.punctuation)

    return " ".join(remove_articles(remove_punc(text.lower())).split())


def _f1_score(prediction, gold):
    pred_tokens = normalize_answer(prediction).split()
    gold_tokens = normalize_answer(gold).split()
    if not pred_tokens and not gold_tokens:
        return 1.0
    if not pred_tokens or not gold_tokens:
        return 0.0
    overlap = Counter(pred_tokens) & Counter(gold_tokens)
    same = sum(overlap.values())
    if same == 0:
        return 0.0
    precision = same / len(pred_tokens)
    recall = same / len(gold_tokens)
    return 2 * precision * recall / (precision + recall)


def exact_match_and_f1(prediction, gold_answers):
    if not gold_answers:
        raise ValueError("at least one gold answer is required")
    exact = max(int(normalize_answer(prediction) == normalize_answer(gold)) for gold in gold_answers)
    f1 = max(_f1_score(prediction, gold) for gold in gold_answers)
    return {"exact_match": exact, "f1": f1}


def build_mlm_example(tokens, mask_positions, mask_token="[MASK]"):
    token_list = list(tokens)
    labels = [None] * len(token_list)
    seen = set()
    for position in mask_positions:
        if position in seen:
            raise ValueError("duplicate mask position")
        if position < 0 or position >= len(token_list):
            raise IndexError("mask position out of range")
        seen.add(position)
        labels[position] = token_list[position]
        token_list[position] = mask_token
    return token_list, labels
