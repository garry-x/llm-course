# Chapter 5 Assignment: Transformer Block

This assignment corresponds to the normalization, feed-forward network, and complete Decoder Block exercises in Chapter 5. The goal is to implement `LayerNorm`, `RMSNorm`, `FFN`, `SwiGLU`, and Pre-Norm `TransformerBlock` as testable modules, and to convert the RMSNorm input gradient, 4x GELU FFN and SwiGLU 8/3 width parameter budget, and Pre-Norm/Post-Norm gradient path derivations into computable functions.

## Files

- `starter.py`: Starter code.
- `reference_solution.py`: Reference implementation.
- `tests.py`: Runnable tests.

## Run

```bash
.venv/bin/python assignments/ch05_block/tests.py
```

By default, tests `reference_solution.py`. To test your implementation:

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch05_block/tests.py
```

## Requirements

- Calling `nn.LayerNorm` to implement `LayerNorm` is not allowed.
- `LayerNormFunction.backward` must return correct gradients for `x`, `gamma`, `beta`.
- `RMSNorm` only performs RMS scaling, no mean centering.
- `rms_norm_input_gradient` must write the gradient of RMSNorm with respect to the input and align with autograd.
- `swiglu_hidden_size_for_param_budget` and `ffn_parameter_counts` must explain the 8/3 width source based on bias-free matrix parameter counts.
- `residual_gradient_path_factors` must compare the per-layer gradient factors of Pre-Norm and Post-Norm in a linearized scalar residual model.
- `TransformerBlock` uses Pre-Norm: `RMSNorm -> MHA -> residual` and `RMSNorm -> SwiGLU -> residual`.
- `estimate_block_resources` estimates the parameter count, major FLOPs, attention score memory, and major activation memory for a single block.
- `activation_checkpointing_tradeoff` estimates the activation memory saved by activation checkpointing and the additional recomputation FLOPs.

## Grading Rubric

| Item | Points | Criteria |
|------|:--:|------|
| Written questions | 35 | Derive LayerNorm/RMSNorm forward and RMSNorm input gradient, compare Pre-Norm/Post-Norm gradient paths, compute FFN/SwiGLU parameter counts, FLOPs, activation memory, checkpointing recomputation cost and 8/3 width source, and explain the conclusion boundaries of probing/patching/ablation |
| Programming parts | 55 | Implement LayerNorm, RMSNorm, RMSNorm input gradient, FFN/SwiGLU, SwiGLU parameter budget function, Pre/Post-Norm gradient path diagnosis, Pre-Norm TransformerBlock, block resource estimator and checkpointing tradeoff estimator |
| Analysis / style | 10 | Explain numerical stability, gradient checking, residual paths, SwiGLU gating implications, resource estimation boundaries, component interpretability experiments, and speculative implementation risks of skipping sublayers |