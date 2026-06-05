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


def sample_next_token(logits, strategy="greedy", temperature=1.0, k=40, p=0.9):
    if logits.dim() == 3:
        logits = logits[:, -1, :]
    if logits.dim() != 2:
        raise ValueError("logits must have shape [batch, vocab] or [batch, seq, vocab]")

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


def _generate(model, input_ids, max_new_tokens, strategy, eos_token_id=None, **kwargs):
    model.eval()
    device = _model_device(model)
    output = input_ids.to(device)
    eos_token_id = _eos_from_model(model, eos_token_id)

    for _ in range(max_new_tokens):
        with torch.no_grad():
            logits = model(output)
        next_token = sample_next_token(logits[:, -1, :], strategy=strategy, **kwargs)
        output = torch.cat([output, next_token], dim=-1)
        if eos_token_id is not None and torch.all(next_token.squeeze(-1) == eos_token_id):
            break
    return output


def generate_greedy(model, input_ids, max_new_tokens=100, eos_token_id=None):
    return _generate(model, input_ids, max_new_tokens, "greedy", eos_token_id=eos_token_id)


def generate_temperature(model, input_ids, max_new_tokens=100, temperature=1.0, eos_token_id=None):
    return _generate(
        model,
        input_ids,
        max_new_tokens,
        "temperature",
        eos_token_id=eos_token_id,
        temperature=temperature,
    )


def generate_topk(model, input_ids, max_new_tokens=100, k=40, temperature=1.0, eos_token_id=None):
    return _generate(
        model,
        input_ids,
        max_new_tokens,
        "top-k",
        eos_token_id=eos_token_id,
        temperature=temperature,
        k=k,
    )


def generate_topp(model, input_ids, max_new_tokens=100, p=0.9, temperature=1.0, eos_token_id=None):
    return _generate(
        model,
        input_ids,
        max_new_tokens,
        "top-p",
        eos_token_id=eos_token_id,
        temperature=temperature,
        p=p,
    )


class Generator:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    @torch.no_grad()
    def generate(self, prompt, strategy="top-p", max_new_tokens=100, temperature=0.8, k=40, p=0.9):
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
