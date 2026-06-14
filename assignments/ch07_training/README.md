# Chapter 7 Assignment: Training Loop

This assignment corresponds to Chapter 7 on the training loop. The goal is to connect next-token data slicing, data repetition/leakage diagnostics, training data curation gate, training token budget estimation, stable cross-entropy, logits gradient, label smoothing, calibration metrics, global grad norm clipping, gradient accumulation step accounting, AdamW, warmup+cosine schedule trajectory, distributed training strategy ledger, checkpoint/resume integrity gate, training anomaly runbook, and a reproducible small training loop.

## Files

- `starter.py`: Starter code.
- `reference_solution.py`: Reference implementation.
- `tests.py`: Runnable tests.

## Run

```bash
.venv/bin/python assignments/ch07_training/tests.py
```

By default, tests `reference_solution.py`. To test your implementation:

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch07_training/tests.py
```

## Requirements

- `TextDataset[i]` must return equal-length `x` and `y`, where `y` is the next-token target shifted right by one from `x`.
- `ngram_repetition_rate` and `ngram_overlap_rate` must be able to detect repetition in the training corpus and train/eval n-gram overlap.
- `training_data_curation_report` must summarize the pre-training data source inventory into size, dedup, quality filter, eval contamination, domain mixture, and privacy gate, reporting weighted duplicate/quality/PII, domain token share, action items, and whether it can enter training rehearsal.
- `global_batch_tokens`, `training_steps_for_token_budget`, and `dense_lm_training_flops` must connect batch settings, token budget, and dense LM approximate training FLOPs.
- `optimizer_state_memory_bytes` must distinguish parameters, gradients, AdamW moments, and be able to roughly estimate per-GPU memory after ZeRO-style optimizer state sharding.
- `distributed_training_strategy_report` must compare DDP, ZeRO/FSDP-like strategies on per-card parameters/gradients/optimizer state, global batch tokens, communication pattern, memory gate, and optional MFU gate, indicating whether it can enter scale rehearsal.
- `checkpoint_resume_integrity_report` must check whether the checkpoint contains model, optimizer, scheduler, global_step, RNG, sampler/data cursor, low-precision scaler/scale history, and other training states, distinguish resume checkpoint from model-only export, and check atomic write, step monotonicity, resharding capability for distributed/sharded/DCP formats, save interval, and checkpoint overhead/async save.
- `cross_entropy_manual` must use the log-sum-exp trick and match `torch.nn.functional.cross_entropy`.
- `cross_entropy_logits_gradient` must return the gradient of mean CE with respect to logits, and support positions masked by `ignore_index` not contributing to the gradient.
- `label_smoothed_cross_entropy` must change the hard target distribution to a smoothed distribution, and ensure positions with `ignore_index` are not included in the average.
- `expected_calibration_error` must bin by confidence, compare accuracy and mean confidence within each bin, and support `ignore_index`.
- `clip_grad_norm` must uniformly scale gradients based on the global L2 norm of all parameter gradients, not clip per-parameter individually.
- `gradient_accumulation_step_accounting` must distinguish micro-batch backward loss, optimizer step, scheduler step, and consumed tokens.
- `AdamW` must implement first/second-order moments, bias correction, and decoupled weight decay.
- The scheduler must first warmup to 1, then cosine decay to `min_lr_ratio`; `lr_schedule_trace` must be able to return lr multiplier, actual lr, and cumulative consumed tokens per optimizer step.
- `train` must execute `zero_grad -> forward -> loss -> backward -> clip -> step -> scheduler.step`, and record loss history.
- The training anomaly analysis question must attribute loss spikes, NaN/Inf, resume discontinuity, and tokens/s drops to data, numerical precision, optimizer state, checkpoint integrity, or system throughput bottlenecks respectively.
- `training_system_gate_report` must break the training run into optimization, throughput, state/checkpoint, and evaluation gates, outputting `overall_pass`, signals for each gate, and action items requiring debugging.

## Grading Rubric

| Item | Points | Criteria |
|------|:--:|------|
| Written questions | 35 | Derive cross-entropy, CE gradient w.r.t. logits, label smoothing, perplexity, ECE/calibration, global grad norm clipping, gradient accumulation loss scaling, global batch tokens, training steps, dense LM training FLOPs, optimizer state memory, DDP/ZeRO/FSDP sharding differences, MFU, checkpoint resume state, DCP/sharded checkpoint and preemption loss, AdamW bias correction, warmup+cosine boundaries and token progress, n-gram leakage diagnosis, data curation gate, diagnostic significance of grad clipping, anomaly runbook, and training gate determination |
| Programming parts | 55 | Implement dataset/dataloader, n-gram repetition/overlap rate, `training_data_curation_report`, training budget calculation, optimizer state memory estimation, `distributed_training_strategy_report`, `checkpoint_resume_integrity_report`, stable cross entropy, CE logits gradient, label-smoothed CE, ECE/calibration bins, global grad norm clipping, gradient accumulation step accounting, AdamW, scheduler, lr schedule trace, training loop, and `training_system_gate_report` |
| Analysis / style | 10 | Explain how gradients flow back to LM head/embedding, and use training logs to explain loss spike, NaN, grad_norm, calibration bias, data repetition, train/val divergence, data quality/contamination gate, tokens/s, MFU, atomic checkpoint write, resharding, checkpoint overhead, resume parity, evaluation gate, and minimal fix experiments |