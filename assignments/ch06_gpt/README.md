# Chapter 6 Assignment: GPT Model Assembly

This assignment corresponds to the complete GPT assembly exercise in Chapter 6. The focus is on implementing a GPT-2 style dense Decoder-only model: token embedding, learned position embedding, causal self-attention, GELU MLP, LayerNorm, LM head and weight tying, and understanding the difference between capacity and per-token computation through tied LM head gradients, MoE routing, load balancing, and parameter budgets.

## Files

- `starter.py`: Starter code.
- `reference_solution.py`: Reference implementation.
- `tests.py`: Runnable tests.

## Run

```bash
.venv/bin/python assignments/ch06_gpt/tests.py
```

By default, tests `reference_solution.py`. To test your implementation:

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch06_gpt/tests.py
```

## Requirements

- `GPTConfig()` defaults should correspond to GPT-2 small: `vocab_size=50257`, `max_seq_len=1024`, `d_model=768`, `n_heads=12`, `n_layers=12`.
- `GPTModel.forward(input_ids)` returns logits of shape `[batch, seq_len, vocab_size]`.
- `causal_lm_loss_from_logits` must use `logits[:, :-1, :]` to predict `input_ids[:, 1:]`, and correctly handle `ignore_index`.
- `tied_lm_head_gradients` requires manually writing the CE gradient under `logits = H E^T`, returning loss, `dH`, and `dE`.
- The causal mask must prevent the current position from attending to future tokens.
- When `tie_weights=True`, `lm_head.weight` and `token_embedding.weight` must be the same parameter object.
- The default GPT-2 small parameter count should be `124,439,808`, which is the common total for HuggingFace GPT-2 small; this includes the tied embedding/LM head counted only once.
- `MoERouter` returns re-normalized top-k weights and top-k expert indices.
- `moe_parameter_budget` uses the bias-free SwiGLU expert parameter count of `3 * d_model * expert_hidden`, calculating router parameters, total expert parameters, activated expert parameters per token, and the capacity/activation computation ratio.
- `moe_load_balance_loss` must report the load fraction from top-k assignment, the mean probability of the router softmax, and the Switch-style load-balancing loss.

## Grading Rubric

| Item | Points | Criteria |
|------|:--:|------|
| Written questions | 30 | Calculate GPT-2 small parameter count, explain label shift, next-token cross entropy, weight tying, tied LM head gradients, causal leakage test, MoE sparse activation, parameter budget, load-balancing loss and dynamic load balancing |
| Programming parts | 60 | Implement GPTConfig, causal attention, GPTModel, initialization/tying, causal LM loss, tied LM head gradient, MoE parameter budget, MoE load-balancing loss and MoE router |
| Analysis / style | 10 | Distinguish total/activated parameters, report parameter analysis, next-token logits alignment and future token leakage check |