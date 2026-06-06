"""Reference solution for Chapter 8 text-generation assignment."""

import torch


def _model_device(model):
    try:
        return next(model.parameters()).device
    except StopIteration:
        return torch.device("cpu")


def _eos_from_model(model, eos_token_id):
    if eos_token_id is not None:
        return eos_token_id
    tokenizer = getattr(model, "tokenizer", None)
    return getattr(tokenizer, "eos_token_id", None)


def top_p_filter(logits, p=0.9):
    if not 0 < p <= 1:
        raise ValueError("p must be in (0, 1]")
    sorted_logits, sorted_indices = torch.sort(logits, descending=True, dim=-1)
    sorted_probs = torch.softmax(sorted_logits, dim=-1)
    cumulative = torch.cumsum(sorted_probs, dim=-1)
    remove = cumulative >= p
    remove[..., 1:] = remove[..., :-1].clone()
    remove[..., 0] = False
    sorted_logits = sorted_logits.masked_fill(remove, -torch.inf)
    filtered = torch.full_like(logits, -torch.inf)
    return filtered.scatter(dim=-1, index=sorted_indices, src=sorted_logits)


def apply_repetition_penalty(logits, generated_ids, penalty=1.2):
    if penalty <= 0:
        raise ValueError("penalty must be positive")
    if logits.dim() != 2:
        raise ValueError("logits must have shape [batch, vocab]")
    if generated_ids.dim() != 2:
        raise ValueError("generated_ids must have shape [batch, seq]")
    if generated_ids.size(0) != logits.size(0):
        raise ValueError("generated_ids batch size must match logits batch size")
    if generated_ids.numel() and (
        int(generated_ids.min().item()) < 0 or int(generated_ids.max().item()) >= logits.size(-1)
    ):
        raise ValueError("generated_ids contains token ids outside the vocabulary")

    adjusted = logits.clone()
    for batch_idx in range(logits.size(0)):
        seen_ids = torch.unique(generated_ids[batch_idx])
        if seen_ids.numel() == 0:
            continue
        seen_scores = adjusted[batch_idx, seen_ids]
        adjusted[batch_idx, seen_ids] = torch.where(
            seen_scores < 0,
            seen_scores * penalty,
            seen_scores / penalty,
        )
    return adjusted


def apply_token_constraints(logits, allowed_token_ids):
    if logits.dim() != 2:
        raise ValueError("logits must have shape [batch, vocab]")
    batch_size, vocab_size = logits.shape
    mask = torch.zeros_like(logits, dtype=torch.bool)

    def validate_ids(ids):
        ids = torch.as_tensor(ids, device=logits.device, dtype=torch.long).flatten()
        if ids.numel() == 0:
            raise ValueError("each batch row must allow at least one token")
        if int(ids.min().item()) < 0 or int(ids.max().item()) >= vocab_size:
            raise ValueError("allowed_token_ids contains ids outside the vocabulary")
        return ids

    if torch.is_tensor(allowed_token_ids):
        if allowed_token_ids.dtype == torch.bool:
            if tuple(allowed_token_ids.shape) != tuple(logits.shape):
                raise ValueError("boolean constraint mask must match logits shape")
            mask = allowed_token_ids.to(device=logits.device)
        elif allowed_token_ids.dim() == 1:
            mask[:, validate_ids(allowed_token_ids)] = True
        elif allowed_token_ids.dim() == 2:
            if allowed_token_ids.size(0) != batch_size:
                raise ValueError("per-row allowed_token_ids must match batch size")
            for batch_idx in range(batch_size):
                mask[batch_idx, validate_ids(allowed_token_ids[batch_idx])] = True
        else:
            raise ValueError("allowed_token_ids tensor must be 1D, 2D, or a boolean mask")
    elif isinstance(allowed_token_ids, (list, tuple)):
        if not allowed_token_ids:
            raise ValueError("allowed_token_ids must be non-empty")
        if all(isinstance(item, int) for item in allowed_token_ids):
            mask[:, validate_ids(allowed_token_ids)] = True
        else:
            if len(allowed_token_ids) != batch_size:
                raise ValueError("per-row allowed_token_ids must match batch size")
            for batch_idx, row_ids in enumerate(allowed_token_ids):
                mask[batch_idx, validate_ids(row_ids)] = True
    else:
        raise TypeError("allowed_token_ids must be a tensor, list, or tuple")

    if not torch.all(mask.any(dim=-1)):
        raise ValueError("each batch row must allow at least one token")
    return logits.masked_fill(~mask, -torch.inf)


def sample_next_token(
    logits,
    strategy="greedy",
    temperature=1.0,
    k=40,
    p=0.9,
    generated_ids=None,
    repetition_penalty=1.0,
    allowed_token_ids=None,
):
    if logits.dim() == 3:
        logits = logits[:, -1, :]
    if logits.dim() != 2:
        raise ValueError("logits must have shape [batch, vocab] or [batch, seq, vocab]")
    if generated_ids is not None and repetition_penalty != 1.0:
        logits = apply_repetition_penalty(logits, generated_ids, repetition_penalty)
    if allowed_token_ids is not None:
        logits = apply_token_constraints(logits, allowed_token_ids)

    if strategy == "greedy" or temperature == 0:
        return logits.argmax(dim=-1, keepdim=True)
    if temperature < 0:
        raise ValueError("temperature must be non-negative")

    scaled = logits / temperature
    vocab_size = scaled.size(-1)
    if strategy == "temperature":
        probs = torch.softmax(scaled, dim=-1)
        return torch.multinomial(probs, num_samples=1)
    if strategy == "top-k":
        if k <= 0:
            raise ValueError("k must be positive")
        k = min(k, vocab_size)
        top_logits, top_indices = torch.topk(scaled, k, dim=-1)
        probs = torch.softmax(top_logits, dim=-1)
        sampled = torch.multinomial(probs, num_samples=1)
        return top_indices.gather(-1, sampled)
    if strategy == "top-p":
        filtered = top_p_filter(scaled, p=p)
        probs = torch.softmax(filtered, dim=-1)
        return torch.multinomial(probs, num_samples=1)
    raise ValueError(f"unknown strategy: {strategy}")


def decoding_distribution_report(
    logits,
    strategy="temperature",
    temperature=1.0,
    k=40,
    p=0.9,
    generated_ids=None,
    repetition_penalty=1.0,
    allowed_token_ids=None,
):
    if logits.dim() == 3:
        logits = logits[:, -1, :]
    if logits.dim() != 2:
        raise ValueError("logits must have shape [batch, vocab] or [batch, seq, vocab]")
    if temperature < 0:
        raise ValueError("temperature must be non-negative")

    processed = logits.clone()
    if generated_ids is not None and repetition_penalty != 1.0:
        processed = apply_repetition_penalty(processed, generated_ids, repetition_penalty)
    if allowed_token_ids is not None:
        processed = apply_token_constraints(processed, allowed_token_ids)

    if strategy == "greedy" or temperature == 0:
        filtered = processed
    else:
        scaled = processed / temperature
        vocab_size = scaled.size(-1)
        if strategy == "temperature":
            filtered = scaled
        elif strategy == "top-k":
            if k <= 0:
                raise ValueError("k must be positive")
            k = min(k, vocab_size)
            top_logits, top_indices = torch.topk(scaled, k, dim=-1)
            filtered = torch.full_like(scaled, -torch.inf)
            filtered.scatter_(dim=-1, index=top_indices, src=top_logits)
        elif strategy == "top-p":
            filtered = top_p_filter(scaled, p=p)
        else:
            raise ValueError(f"unknown strategy: {strategy}")

    probabilities = torch.softmax(filtered, dim=-1)
    finite_mask = torch.isfinite(filtered)
    kept_token_ids = []
    kept_probabilities = []
    entropy = []
    for batch_idx in range(filtered.size(0)):
        ids = torch.nonzero(finite_mask[batch_idx], as_tuple=False).flatten()
        probs = probabilities[batch_idx, ids]
        kept_token_ids.append([int(token_id.item()) for token_id in ids])
        kept_probabilities.append([float(prob.item()) for prob in probs])
        positive_probs = probs[probs > 0]
        entropy.append(float(-(positive_probs * torch.log(positive_probs)).sum().item()))

    return {
        "processed_logits": processed,
        "filtered_logits": filtered,
        "probabilities": probabilities,
        "kept_token_ids": kept_token_ids,
        "kept_probabilities": kept_probabilities,
        "entropy": entropy,
        "selected_token_ids": torch.argmax(probabilities, dim=-1).tolist(),
    }


def _generate(model, input_ids, max_new_tokens, strategy, eos_token_id=None, **kwargs):
    model.eval()
    device = _model_device(model)
    output = input_ids.to(device)
    eos_token_id = _eos_from_model(model, eos_token_id)

    for _ in range(max_new_tokens):
        with torch.no_grad():
            logits = model(output)
        next_token = sample_next_token(
            logits[:, -1, :],
            strategy=strategy,
            generated_ids=output,
            **kwargs,
        )
        output = torch.cat([output, next_token], dim=-1)
        if eos_token_id is not None and torch.all(next_token.squeeze(-1) == eos_token_id):
            break
    return output


def generate_greedy(model, input_ids, max_new_tokens=100, eos_token_id=None, repetition_penalty=1.0):
    return _generate(
        model,
        input_ids,
        max_new_tokens,
        "greedy",
        eos_token_id=eos_token_id,
        repetition_penalty=repetition_penalty,
    )


def generate_temperature(
    model,
    input_ids,
    max_new_tokens=100,
    temperature=1.0,
    eos_token_id=None,
    repetition_penalty=1.0,
):
    return _generate(
        model,
        input_ids,
        max_new_tokens,
        "temperature",
        eos_token_id=eos_token_id,
        temperature=temperature,
        repetition_penalty=repetition_penalty,
    )


def generate_topk(
    model,
    input_ids,
    max_new_tokens=100,
    k=40,
    temperature=1.0,
    eos_token_id=None,
    repetition_penalty=1.0,
):
    return _generate(
        model,
        input_ids,
        max_new_tokens,
        "top-k",
        eos_token_id=eos_token_id,
        temperature=temperature,
        k=k,
        repetition_penalty=repetition_penalty,
    )


def generate_topp(
    model,
    input_ids,
    max_new_tokens=100,
    p=0.9,
    temperature=1.0,
    eos_token_id=None,
    repetition_penalty=1.0,
):
    return _generate(
        model,
        input_ids,
        max_new_tokens,
        "top-p",
        eos_token_id=eos_token_id,
        temperature=temperature,
        p=p,
        repetition_penalty=repetition_penalty,
    )


def length_normalized_score(logprob_sum, length, alpha=1.0):
    if length <= 0:
        raise ValueError("length must be positive")
    if alpha < 0:
        raise ValueError("alpha must be non-negative")
    return float(logprob_sum) / (float(length) ** alpha)


def pass_at_k(num_samples, num_correct, k):
    if num_samples <= 0:
        raise ValueError("num_samples must be positive")
    if k <= 0 or k > num_samples:
        raise ValueError("k must be in [1, num_samples]")
    if num_correct < 0 or num_correct > num_samples:
        raise ValueError("num_correct must be in [0, num_samples]")
    if num_correct == 0:
        return 0.0
    incorrect = num_samples - num_correct
    if incorrect < k:
        return 1.0

    probability_all_k_fail = 1.0
    for offset in range(k):
        probability_all_k_fail *= (incorrect - offset) / (num_samples - offset)
    return 1.0 - probability_all_k_fail


def self_consistency_vote(outputs, answer_extractor=None, token_counts=None):
    if not outputs:
        raise ValueError("outputs must be non-empty")
    if token_counts is not None and len(token_counts) != len(outputs):
        raise ValueError("token_counts must have the same length as outputs")
    if token_counts is not None and any(count < 0 for count in token_counts):
        raise ValueError("token_counts must be non-negative")

    if answer_extractor is None:
        answer_extractor = lambda text: str(text).strip()

    counts = {}
    first_seen = {}
    answers = []
    for idx, output in enumerate(outputs):
        answer = str(answer_extractor(output)).strip()
        answers.append(answer)
        counts[answer] = counts.get(answer, 0) + 1
        first_seen.setdefault(answer, idx)

    vote_counts = sorted(
        counts.items(),
        key=lambda item: (-item[1], first_seen[item[0]]),
    )
    best_answer, best_count = vote_counts[0]
    total_tokens = sum(token_counts) if token_counts is not None else None
    mean_tokens = (total_tokens / len(outputs)) if token_counts is not None else None

    return {
        "answer": best_answer,
        "count": best_count,
        "vote_fraction": best_count / len(outputs),
        "num_samples": len(outputs),
        "answers": answers,
        "vote_counts": vote_counts,
        "total_tokens": total_tokens,
        "mean_tokens": mean_tokens,
    }


def speculative_decoding_speedup(accepted_counts, output_token_counts, gamma=4, draft_cost_ratio=0.2):
    if gamma <= 0:
        raise ValueError("gamma must be positive")
    if draft_cost_ratio < 0:
        raise ValueError("draft_cost_ratio must be non-negative")
    if not accepted_counts or not output_token_counts:
        raise ValueError("accepted_counts and output_token_counts must be non-empty")
    if len(accepted_counts) != len(output_token_counts):
        raise ValueError("accepted_counts and output_token_counts must have the same length")

    accepted_counts = [int(count) for count in accepted_counts]
    output_token_counts = [int(count) for count in output_token_counts]
    if any(count < 0 or count > gamma for count in accepted_counts):
        raise ValueError("each accepted count must be in [0, gamma]")
    if any(count <= 0 or count > gamma + 1 for count in output_token_counts):
        raise ValueError("each output token count must be in [1, gamma + 1]")

    rounds = len(accepted_counts)
    proposed = rounds * gamma
    accepted = sum(accepted_counts)
    generated_tokens = sum(output_token_counts)
    speculative_time_units = rounds + proposed * float(draft_cost_ratio)
    baseline_target_steps = generated_tokens
    speedup = baseline_target_steps / speculative_time_units

    return {
        "rounds": rounds,
        "proposed": proposed,
        "accepted": accepted,
        "generated_tokens": generated_tokens,
        "acceptance_rate": accepted / proposed if proposed else 0.0,
        "baseline_target_steps": baseline_target_steps,
        "target_verify_calls": rounds,
        "draft_steps": proposed,
        "draft_cost_ratio": float(draft_cost_ratio),
        "speculative_time_units": speculative_time_units,
        "speedup": speedup,
    }


def beam_search(model, input_ids, max_new_tokens=100, num_beams=4, eos_token_id=None, length_penalty_alpha=0.0):
    if input_ids.size(0) != 1:
        raise ValueError("beam_search currently supports batch size 1")
    if max_new_tokens <= 0:
        raise ValueError("max_new_tokens must be positive")
    if num_beams <= 0:
        raise ValueError("num_beams must be positive")
    if length_penalty_alpha < 0:
        raise ValueError("length_penalty_alpha must be non-negative")

    model.eval()
    device = _model_device(model)
    eos_token_id = _eos_from_model(model, eos_token_id)
    prompt_len = input_ids.size(1)
    beams = [(input_ids.to(device), 0.0, False)]

    for _ in range(max_new_tokens):
        candidates = []
        all_ended = True
        for sequence, score, ended in beams:
            if ended:
                candidates.append((sequence, score, True))
                continue
            all_ended = False
            with torch.no_grad():
                logits = model(sequence)[:, -1, :]
                log_probs = torch.log_softmax(logits, dim=-1)
            top_scores, top_tokens = torch.topk(log_probs, k=min(num_beams, log_probs.size(-1)), dim=-1)
            for token_score, token_id in zip(top_scores[0], top_tokens[0]):
                token = token_id.view(1, 1).to(sequence.device)
                new_sequence = torch.cat([sequence, token.to(sequence.dtype)], dim=-1)
                is_ended = eos_token_id is not None and int(token_id.item()) == eos_token_id
                candidates.append((new_sequence, score + float(token_score.item()), is_ended))

        if all_ended:
            break

        def rank_key(item):
            seq, score, _ended = item
            generated_len = max(1, seq.size(1) - prompt_len)
            return length_normalized_score(score, generated_len, length_penalty_alpha)

        beams = sorted(candidates, key=rank_key, reverse=True)[:num_beams]
        if all(ended for _seq, _score, ended in beams):
            break

    beam_table = []
    for sequence, score, ended in beams:
        generated_len = max(1, sequence.size(1) - prompt_len)
        beam_table.append(
            {
                "tokens": sequence[0].tolist(),
                "logprob_sum": score,
                "normalized_score": length_normalized_score(score, generated_len, length_penalty_alpha),
                "generated_len": generated_len,
                "ended": ended,
            }
        )
    beam_table.sort(key=lambda item: item["normalized_score"], reverse=True)
    return torch.tensor([beam_table[0]["tokens"]], device=device, dtype=input_ids.dtype), beam_table


class Generator:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    @torch.no_grad()
    def generate(
        self,
        prompt,
        strategy="top-p",
        max_new_tokens=100,
        temperature=0.8,
        k=40,
        p=0.9,
        repetition_penalty=1.0,
    ):
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        eos_token_id = getattr(self.tokenizer, "eos_token_id", None)
        output = _generate(
            self.model,
            input_ids,
            max_new_tokens,
            strategy,
            eos_token_id=eos_token_id,
            temperature=temperature,
            k=k,
            p=p,
            repetition_penalty=repetition_penalty,
        )
        return self.tokenizer.decode(output[0].tolist())

    def distinct_ngrams(self, text, n=2):
        tokens = text.split()
        if len(tokens) < n:
            return 0.0
        ngrams = [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]
        return len(set(ngrams)) / len(ngrams)


def speculative_decoding(target_model, draft_model, input_ids, gamma=4, max_new_tokens=100, eos_token_id=None):
    if gamma <= 0:
        raise ValueError("gamma must be positive")

    target_model.eval()
    draft_model.eval()
    device = _model_device(target_model)
    prefix = input_ids.to(device)
    eos_token_id = _eos_from_model(target_model, eos_token_id)
    generated = 0
    proposed = 0
    accepted_count = 0

    while generated < max_new_tokens:
        draft_ids = prefix
        draft_tokens = []
        with torch.no_grad():
            for _ in range(min(gamma, max_new_tokens - generated)):
                draft_logits = draft_model(draft_ids)
                token = sample_next_token(draft_logits[:, -1, :], strategy="temperature", temperature=1.0)
                draft_tokens.append(token)
                draft_ids = torch.cat([draft_ids, token.to(draft_ids.device)], dim=-1)

            target_logits = target_model(draft_ids)
            draft_logits = draft_model(draft_ids)

        accepted = []
        steps = len(draft_tokens)
        proposed += steps
        target_probs = torch.softmax(target_logits[:, -(steps + 1) : -1, :], dim=-1)
        draft_probs = torch.softmax(draft_logits[:, -(steps + 1) : -1, :], dim=-1)

        rejected = False
        for t, token_tensor in enumerate(draft_tokens):
            token = int(token_tensor.item())
            p = target_probs[0, t, token]
            q = draft_probs[0, t, token].clamp_min(1e-12)
            if p >= q or torch.rand((), device=device) < p / q:
                accepted.append(token)
                accepted_count += 1
            else:
                residual = (target_probs[0, t] - draft_probs[0, t]).clamp(min=0)
                if residual.sum() == 0:
                    corrected = sample_next_token(target_logits[:, t, :], strategy="temperature", temperature=1.0)
                    accepted.append(int(corrected.item()))
                else:
                    residual = residual / residual.sum()
                    accepted.append(int(torch.multinomial(residual, 1).item()))
                rejected = True
                break

        if not rejected and generated + len(accepted) < max_new_tokens:
            extra = sample_next_token(target_logits[:, -1, :], strategy="temperature", temperature=1.0)
            accepted.append(int(extra.item()))

        accepted = accepted[: max_new_tokens - generated]
        if not accepted:
            break
        prefix = torch.cat([prefix, torch.tensor([accepted], device=device, dtype=prefix.dtype)], dim=-1)
        generated += len(accepted)
        if eos_token_id is not None and accepted[-1] == eos_token_id:
            break

    stats = {
        "proposed": proposed,
        "accepted": accepted_count,
        "acceptance_rate": accepted_count / proposed if proposed else 0.0,
    }
    return prefix, stats
