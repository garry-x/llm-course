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


def _parse_action(action):
    if isinstance(action, str):
        if ":" in action:
            name, label = action.split(":", 1)
        elif "(" in action and action.endswith(")"):
            name, label = action[:-1].split("(", 1)
        else:
            name, label = action, None
    else:
        if len(action) == 1:
            name, label = action[0], None
        elif len(action) == 2:
            name, label = action
        else:
            raise ValueError("action tuples must have one or two items")
    name = str(name).upper().replace("-", "_")
    return name, label


def run_arc_standard_transitions(tokens, actions):
    """Run arc-standard dependency parsing actions and return heads, labels, and trace."""
    if not tokens:
        raise ValueError("tokens must not be empty")

    stack = []
    buffer = list(range(len(tokens)))
    heads = [None] * len(tokens)
    labels = [None] * len(tokens)
    arcs = []
    trace = []

    def snapshot(action_name, label, arc):
        trace.append(
            {
                "stack": [tokens[index] for index in stack],
                "buffer": [tokens[index] for index in buffer],
                "action": action_name if label is None else f"{action_name}({label})",
                "arc": None if arc is None else (arc[0], tokens[arc[1]], arc[2]),
            }
        )

    for action in actions:
        name, label = _parse_action(action)
        arc = None
        if name == "SHIFT":
            if not buffer:
                raise ValueError("SHIFT requires a non-empty buffer")
            stack.append(buffer.pop(0))
        elif name == "LEFT_ARC":
            if label is None:
                raise ValueError("LEFT_ARC requires a label")
            if len(stack) < 2:
                raise ValueError("LEFT_ARC requires at least two stack items")
            head = stack[-1]
            dep = stack[-2]
            if heads[dep] is not None:
                raise ValueError("dependent already has a head")
            heads[dep] = head
            labels[dep] = label
            stack.pop(-2)
            arc = (tokens[head], dep, label)
            arcs.append(arc)
        elif name == "RIGHT_ARC":
            if label is None:
                raise ValueError("RIGHT_ARC requires a label")
            if len(stack) < 2:
                raise ValueError("RIGHT_ARC requires at least two stack items")
            head = stack[-2]
            dep = stack[-1]
            if heads[dep] is not None:
                raise ValueError("dependent already has a head")
            heads[dep] = head
            labels[dep] = label
            stack.pop()
            arc = (tokens[head], dep, label)
            arcs.append(arc)
        elif name == "ROOT":
            root_label = label or "root"
            if buffer or len(stack) != 1:
                raise ValueError("ROOT requires an empty buffer and exactly one stack item")
            dep = stack[-1]
            if heads[dep] is not None:
                raise ValueError("root token already has a head")
            heads[dep] = -1
            labels[dep] = root_label
            stack.pop()
            arc = ("ROOT", dep, root_label)
            arcs.append(arc)
        else:
            raise ValueError(f"unknown action: {action}")
        snapshot(name, label, arc)

    if stack or buffer or any(head is None for head in heads):
        raise ValueError("transition sequence did not finish a complete parse")

    return {"heads": heads, "labels": labels, "arcs": arcs, "trace": trace}


def scalar_rnn_forward(inputs, w_xh, w_hh, h0=0.0):
    hidden_states = []
    h_prev = float(h0)
    for x_t in inputs:
        h_prev = math.tanh(float(w_xh) * float(x_t) + float(w_hh) * h_prev)
        hidden_states.append(h_prev)
    return hidden_states


def recurrent_gradient_factors(hidden_states, w_hh):
    return [float(w_hh) * (1.0 - float(h_t) ** 2) for h_t in hidden_states]


def _matvec(matrix, vector):
    return [sum(float(weight) * float(value) for weight, value in zip(row, vector)) for row in matrix]


def _dot(left, right):
    return sum(float(x) * float(y) for x, y in zip(left, right))


def _validate_rectangular_matrix(name, matrix):
    if not matrix:
        raise ValueError(f"{name} must not be empty")
    width = len(matrix[0])
    if width == 0:
        raise ValueError(f"{name} rows must not be empty")
    if any(len(row) != width for row in matrix):
        raise ValueError(f"{name} must be rectangular")
    return width


def additive_attention_context(decoder_state, encoder_states, w_s, w_h, v):
    """Compute seq2seq additive-attention scores, weights, and context vector."""
    if not decoder_state:
        raise ValueError("decoder_state must not be empty")
    source_dim = _validate_rectangular_matrix("encoder_states", encoder_states)
    decoder_dim = _validate_rectangular_matrix("w_s", w_s)
    hidden_dim = len(w_s)
    if decoder_dim != len(decoder_state):
        raise ValueError("w_s width must match decoder_state length")
    if len(w_h) != hidden_dim:
        raise ValueError("w_h must have the same row count as w_s")
    encoder_dim = _validate_rectangular_matrix("w_h", w_h)
    if encoder_dim != source_dim:
        raise ValueError("w_h width must match encoder state length")
    if len(v) != hidden_dim:
        raise ValueError("v length must match attention hidden size")

    projected_decoder = _matvec(w_s, decoder_state)
    scores = []
    for encoder_state in encoder_states:
        projected_encoder = _matvec(w_h, encoder_state)
        hidden = [
            math.tanh(dec_part + enc_part)
            for dec_part, enc_part in zip(projected_decoder, projected_encoder)
        ]
        scores.append(_dot(v, hidden))

    max_score = max(scores)
    exp_scores = [math.exp(score - max_score) for score in scores]
    normalizer = sum(exp_scores)
    weights = [score / normalizer for score in exp_scores]
    context = [
        sum(weight * encoder_state[dim] for weight, encoder_state in zip(weights, encoder_states))
        for dim in range(source_dim)
    ]
    return {"scores": scores, "weights": weights, "context": context}


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


def masked_lm_loss_from_logits(logits, labels, ignore_index=None):
    if not logits:
        raise ValueError("logits must not be empty")
    vocab_size = len(logits[0])
    if vocab_size == 0:
        raise ValueError("logit rows must not be empty")
    if any(len(row) != vocab_size for row in logits):
        raise ValueError("logits must be rectangular")
    if len(labels) != len(logits):
        raise ValueError("labels length must match logits length")

    losses = []
    correct = 0
    positions = []
    for position, (row, label) in enumerate(zip(logits, labels)):
        if label is None or label == ignore_index:
            continue
        if label < 0 or label >= vocab_size:
            raise ValueError("label ids must be inside the vocabulary")
        max_logit = max(float(value) for value in row)
        normalizer = sum(math.exp(float(value) - max_logit) for value in row)
        log_z = max_logit + math.log(normalizer)
        losses.append(log_z - float(row[label]))
        pred = max(range(vocab_size), key=lambda idx: float(row[idx]))
        correct += int(pred == label)
        positions.append(position)

    if not losses:
        raise ValueError("at least one non-ignored MLM label is required")
    return {
        "loss": sum(losses) / len(losses),
        "accuracy": correct / len(losses),
        "num_masked": len(losses),
        "positions": positions,
    }


def bio_tags_to_spans(tokens, tags):
    if len(tokens) != len(tags):
        raise ValueError("tokens and tags must have equal length")

    spans = []
    current_type = None
    start = None

    def close(end):
        if current_type is None:
            return
        span_tokens = list(tokens[start:end])
        spans.append(
            {
                "type": current_type,
                "start": start,
                "end": end,
                "tokens": span_tokens,
                "text": " ".join(span_tokens),
            }
        )

    for index, tag in enumerate(tags):
        if tag == "O":
            close(index)
            current_type = None
            start = None
            continue
        if "-" not in tag:
            raise ValueError("BIO tags must be O or PREFIX-TYPE")
        prefix, entity_type = tag.split("-", 1)
        if prefix not in {"B", "I"} or not entity_type:
            raise ValueError("BIO tags must use B-TYPE or I-TYPE")

        starts_new_entity = (
            prefix == "B"
            or current_type is None
            or entity_type != current_type
        )
        if starts_new_entity:
            close(index)
            current_type = entity_type
            start = index

    close(len(tokens))
    return spans


def span_f1(gold_spans, pred_spans):
    def span_key(span):
        if isinstance(span, dict):
            if not {"type", "start", "end"}.issubset(span):
                raise ValueError("span dictionaries must contain type, start, and end")
            entity_type = span["type"]
            start = span["start"]
            end = span["end"]
        elif isinstance(span, (tuple, list)) and len(span) == 3:
            entity_type, start, end = span
        else:
            raise ValueError("spans must be dicts or (type, start, end) triples")
        start = int(start)
        end = int(end)
        if start < 0 or end <= start:
            raise ValueError("span boundaries must satisfy 0 <= start < end")
        return str(entity_type), start, end

    gold = {span_key(span) for span in gold_spans}
    pred = {span_key(span) for span in pred_spans}
    true_positive = len(gold & pred)
    false_positive = len(pred - gold)
    false_negative = len(gold - pred)
    precision = 0.0 if not pred else true_positive / len(pred)
    recall = 0.0 if not gold else true_positive / len(gold)
    f1 = 0.0 if precision + recall == 0.0 else 2 * precision * recall / (precision + recall)
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "gold_count": len(gold),
        "pred_count": len(pred),
    }


def viterbi_decode(emissions, transitions, start_scores=None, end_scores=None):
    if not emissions:
        raise ValueError("emissions must not be empty")
    num_tags = len(emissions[0])
    if num_tags == 0:
        raise ValueError("emission rows must not be empty")
    if any(len(row) != num_tags for row in emissions):
        raise ValueError("emissions must be rectangular")
    if len(transitions) != num_tags or any(len(row) != num_tags for row in transitions):
        raise ValueError("transitions must have shape num_tags x num_tags")
    if start_scores is not None and len(start_scores) != num_tags:
        raise ValueError("start_scores length must match num_tags")
    if end_scores is not None and len(end_scores) != num_tags:
        raise ValueError("end_scores length must match num_tags")

    starts = [0.0] * num_tags if start_scores is None else [float(score) for score in start_scores]
    ends = [0.0] * num_tags if end_scores is None else [float(score) for score in end_scores]
    transition_scores = [[float(score) for score in row] for row in transitions]

    scores = [[starts[tag] + float(emissions[0][tag]) for tag in range(num_tags)]]
    backpointers = [[None] * num_tags]

    for position in range(1, len(emissions)):
        row_scores = []
        row_backpointers = []
        for current_tag in range(num_tags):
            candidates = [
                scores[position - 1][previous_tag]
                + transition_scores[previous_tag][current_tag]
                + float(emissions[position][current_tag])
                for previous_tag in range(num_tags)
            ]
            best_previous = max(range(num_tags), key=lambda tag: candidates[tag])
            row_scores.append(candidates[best_previous])
            row_backpointers.append(best_previous)
        scores.append(row_scores)
        backpointers.append(row_backpointers)

    final_candidates = [score + ends[tag] for tag, score in enumerate(scores[-1])]
    best_last_tag = max(range(num_tags), key=lambda tag: final_candidates[tag])
    best_path = [best_last_tag]
    for position in range(len(emissions) - 1, 0, -1):
        best_path.append(backpointers[position][best_path[-1]])
    best_path.reverse()

    return {
        "tags": best_path,
        "score": final_candidates[best_last_tag],
        "scores": scores,
        "backpointers": backpointers,
    }


def _validate_linear_chain_inputs(emissions, transitions, start_scores=None, end_scores=None):
    if not emissions:
        raise ValueError("emissions must not be empty")
    num_tags = len(emissions[0])
    if num_tags == 0:
        raise ValueError("emission rows must not be empty")
    if any(len(row) != num_tags for row in emissions):
        raise ValueError("emissions must be rectangular")
    if len(transitions) != num_tags or any(len(row) != num_tags for row in transitions):
        raise ValueError("transitions must have shape num_tags x num_tags")
    if start_scores is not None and len(start_scores) != num_tags:
        raise ValueError("start_scores length must match num_tags")
    if end_scores is not None and len(end_scores) != num_tags:
        raise ValueError("end_scores length must match num_tags")
    return num_tags


def _logsumexp(values):
    maximum = max(values)
    return maximum + math.log(sum(math.exp(value - maximum) for value in values))


def linear_chain_log_partition(emissions, transitions, start_scores=None, end_scores=None):
    num_tags = _validate_linear_chain_inputs(emissions, transitions, start_scores, end_scores)
    starts = [0.0] * num_tags if start_scores is None else [float(score) for score in start_scores]
    ends = [0.0] * num_tags if end_scores is None else [float(score) for score in end_scores]
    transition_scores = [[float(score) for score in row] for row in transitions]

    alpha = [starts[tag] + float(emissions[0][tag]) for tag in range(num_tags)]
    alpha_table = [list(alpha)]
    for position in range(1, len(emissions)):
        next_alpha = []
        for current_tag in range(num_tags):
            candidates = [
                alpha[previous_tag]
                + transition_scores[previous_tag][current_tag]
                + float(emissions[position][current_tag])
                for previous_tag in range(num_tags)
            ]
            next_alpha.append(_logsumexp(candidates))
        alpha = next_alpha
        alpha_table.append(list(alpha))

    log_partition = _logsumexp([alpha[tag] + ends[tag] for tag in range(num_tags)])
    return {"log_partition": log_partition, "alpha": alpha_table}


def linear_chain_crf_nll(emissions, transitions, gold_tags, start_scores=None, end_scores=None):
    num_tags = _validate_linear_chain_inputs(emissions, transitions, start_scores, end_scores)
    if len(gold_tags) != len(emissions):
        raise ValueError("gold_tags length must match emissions length")
    if any(tag < 0 or tag >= num_tags for tag in gold_tags):
        raise ValueError("gold_tags contain tag ids outside the tag set")

    starts = [0.0] * num_tags if start_scores is None else [float(score) for score in start_scores]
    ends = [0.0] * num_tags if end_scores is None else [float(score) for score in end_scores]
    transition_scores = [[float(score) for score in row] for row in transitions]

    gold_score = starts[gold_tags[0]] + float(emissions[0][gold_tags[0]])
    for position in range(1, len(gold_tags)):
        previous_tag = gold_tags[position - 1]
        current_tag = gold_tags[position]
        gold_score += transition_scores[previous_tag][current_tag]
        gold_score += float(emissions[position][current_tag])
    gold_score += ends[gold_tags[-1]]

    partition = linear_chain_log_partition(emissions, transitions, start_scores, end_scores)
    log_partition = partition["log_partition"]
    return {
        "gold_score": gold_score,
        "log_partition": log_partition,
        "nll": log_partition - gold_score,
        "alpha": partition["alpha"],
    }


def select_extractive_qa_span(tokens, start_logits, end_logits, max_answer_len=30, cls_index=0):
    if not tokens:
        raise ValueError("tokens must not be empty")
    if len(tokens) != len(start_logits) or len(tokens) != len(end_logits):
        raise ValueError("tokens, start_logits, and end_logits must have equal length")
    if max_answer_len <= 0:
        raise ValueError("max_answer_len must be positive")
    if cls_index < 0 or cls_index >= len(tokens):
        raise ValueError("cls_index out of range")

    best = None
    for start in range(len(tokens)):
        if start == cls_index:
            continue
        max_end = min(len(tokens), start + max_answer_len)
        for end in range(start, max_end):
            if end == cls_index:
                continue
            score = float(start_logits[start]) + float(end_logits[end])
            if best is None or score > best["score"]:
                best = {
                    "start": start,
                    "end": end,
                    "tokens": list(tokens[start : end + 1]),
                    "text": " ".join(tokens[start : end + 1]),
                    "score": score,
                    "no_answer": False,
                }

    no_answer_score = float(start_logits[cls_index]) + float(end_logits[cls_index])
    if best is None or no_answer_score >= best["score"]:
        return {
            "start": cls_index,
            "end": cls_index,
            "tokens": [tokens[cls_index]],
            "text": "",
            "score": no_answer_score,
            "no_answer": True,
        }
    return best


def summarize_pairwise_judgments(judgments):
    """Summarize blind pairwise LLM-as-judge results."""
    if not judgments:
        raise ValueError("at least one judgment is required")

    wins = losses = ties = 0
    by_task = {}
    valid_winners = {"A", "B", "tie"}
    for judgment in judgments:
        if not isinstance(judgment, dict) or "winner" not in judgment:
            raise ValueError("each judgment must be a dict with a winner field")
        winner = judgment["winner"]
        if isinstance(winner, str):
            winner = winner.strip()
        if winner not in valid_winners:
            raise ValueError("winner must be A, B, or tie")

        if winner == "A":
            wins += 1
        elif winner == "B":
            losses += 1
        else:
            ties += 1

        task = judgment.get("task")
        if task is not None:
            task = str(task)
            task_stats = by_task.setdefault(task, {"wins": 0, "losses": 0, "ties": 0, "total": 0})
            task_stats["total"] += 1
            if winner == "A":
                task_stats["wins"] += 1
            elif winner == "B":
                task_stats["losses"] += 1
            else:
                task_stats["ties"] += 1

    total = wins + losses + ties
    tie_adjusted_win_rate = (wins + 0.5 * ties) / total
    for task_stats in by_task.values():
        task_total = task_stats["total"]
        task_stats["tie_adjusted_win_rate"] = (
            task_stats["wins"] + 0.5 * task_stats["ties"]
        ) / task_total

    return {
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "total": total,
        "win_rate": wins / total,
        "tie_adjusted_win_rate": tie_adjusted_win_rate,
        "by_task": by_task,
    }


def safety_evaluation_metrics(buckets):
    """Compute safety and usefulness rates from stratified evaluation buckets."""
    required = {"harmful", "benign_sensitive", "ordinary"}
    if not required.issubset(buckets):
        missing = ", ".join(sorted(required - set(buckets)))
        raise ValueError(f"missing required bucket(s): {missing}")

    def validate_counts(bucket_name):
        counts = buckets[bucket_name]
        if not isinstance(counts, dict):
            raise ValueError("bucket counts must be dictionaries")
        normalized = {}
        for key, value in counts.items():
            if int(value) != value or value < 0:
                raise ValueError("bucket counts must be non-negative integers")
            normalized[str(key)] = int(value)
        total = sum(normalized.values())
        if total == 0:
            raise ValueError("bucket total must be positive")
        normalized["total"] = total
        return normalized

    harmful = validate_counts("harmful")
    benign = validate_counts("benign_sensitive")
    ordinary = validate_counts("ordinary")

    harmful_unsafe = harmful.get("unsafe", 0)
    harmful_refused = harmful.get("refused", 0)
    benign_refused = benign.get("refused", 0)
    ordinary_correct = ordinary.get("correct", 0)
    ordinary_passed = ordinary.get("passed", 0)

    task_success = ordinary_correct if "correct" in ordinary else ordinary_passed
    return {
        "harmful_total": harmful["total"],
        "benign_sensitive_total": benign["total"],
        "ordinary_total": ordinary["total"],
        "attack_success_rate": harmful_unsafe / harmful["total"],
        "harmful_refusal_rate": harmful_refused / harmful["total"],
        "over_refusal_rate": benign_refused / benign["total"],
        "task_utility": task_success / ordinary["total"],
    }


def benchmark_result_summary(task, sample_size, metrics, inference_settings, failure_counts=None):
    """Build a structured benchmark conclusion with scope and uncertainty fields."""
    if not task:
        raise ValueError("task must be non-empty")
    if int(sample_size) != sample_size or sample_size <= 0:
        raise ValueError("sample_size must be a positive integer")
    if not isinstance(metrics, dict) or not metrics:
        raise ValueError("metrics must be a non-empty dictionary")
    if not isinstance(inference_settings, dict) or not inference_settings:
        raise ValueError("inference_settings must be a non-empty dictionary")
    failures = {} if failure_counts is None else dict(failure_counts)
    if any(int(value) != value or value < 0 for value in failures.values()):
        raise ValueError("failure counts must be non-negative integers")

    required_settings = ["model", "prompt", "temperature"]
    missing_settings = [key for key in required_settings if key not in inference_settings]
    if missing_settings:
        raise ValueError("inference_settings must include model, prompt, and temperature")

    sorted_failures = sorted(failures.items(), key=lambda item: (-item[1], item[0]))
    largest_failure = None if not sorted_failures else sorted_failures[0][0]
    uncertainty = "high" if sample_size < 30 else "medium" if sample_size < 100 else "lower"
    scope = (
        f"Results apply to {task} with n={sample_size}, model={inference_settings['model']}, "
        f"prompt={inference_settings['prompt']}, temperature={inference_settings['temperature']}."
    )
    limits = [
        "Does not prove general model quality outside this task distribution.",
        "Does not replace latency, cost, safety, and human review when those matter.",
        "May change with prompt, decoding settings, judge rubric, data version, or cache state.",
    ]

    return {
        "task": str(task),
        "sample_size": int(sample_size),
        "metrics": dict(metrics),
        "inference_settings": dict(inference_settings),
        "failure_counts": failures,
        "largest_failure_type": largest_failure,
        "uncertainty": uncertainty,
        "scope": scope,
        "limits": limits,
    }
