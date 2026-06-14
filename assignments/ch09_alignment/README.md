# Chapter 9 Assignment: Fine-tuning and Alignment

This assignment corresponds to Chapter 9 on fine-tuning and alignment. The goal is to implement SFT label mask, SFT chat template/mask/packing audit, LoRA low-rank adaptation, reward model pairwise loss, DPO preference loss and implicit reward, PPO clipped objective, approximate KL control, preference length bias statistics, post-training data audit, GRPO intra-group whitening, GRPO policy loss ledger, RLVR/RFT grader health report, and LoRA merge inference.

## Files

- `starter.py`: Starter code.
- `reference_solution.py`: Reference implementation.
- `tests.py`: Runnable tests.

## Run

```bash
.venv/bin/python assignments/ch09_alignment/tests.py
```

By default, tests `reference_solution.py`. To test your implementation:

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch09_alignment/tests.py
```

## Requirements

- In SFT labels, prompt and padding positions must be `-100`, and loss is only computed for the assistant response.
- `sft_chat_template_mask_report` must check multi-turn chat roles, assistant-only label mask, supervised token ratio, assistant token truncation, and whether packing has block-diagonal attention or safe sample boundaries.
- `sequence_log_probs` must first replace `-100` with a safe index before `gather`, then use a mask to remove invalid positions.
- LoRA initial output should equal the original linear layer output; only LoRA's `A/B` parameters should be trainable.
- The reward model pairwise loss must implement Bradley-Terry's `-log sigmoid(r_chosen - r_rejected)`.
- DPO loss must use the policy/reference chosen/rejected log-ratio.
- `dpo_implicit_rewards` must explicitly report `beta * (log pi_policy - log pi_ref)` as chosen/rejected implicit reward, margin, preference probability, and preference accuracy.
- `ppo_clipped_policy_loss` must compute the PPO surrogate using `min(ratio * advantage, clipped_ratio * advantage)`, and report mean ratio, clip fraction, and approximate KL.
- `approx_kl_from_logps` must implement approximate KL on sampled tokens: `exp(log_ref - log_policy) - (log_ref - log_policy) - 1`, and correctly ignore the padding mask.
- Preference length bias statistics must report the mean chosen/rejected length difference and three category proportions.
- `post_training_data_audit` must audit SFT, preference, and RLVR/RFT data sources for coverage, label quality, leakage, and safety gate, reporting task/safety slice coverage, length bias, same-prompt label conflicts, eval overlap, unsafe chosen rate, and whether post-training can proceed.
- GRPO advantages must be whitened within the same prompt group.
- `grpo_policy_loss` must extend intra-group whitened advantages to completion tokens, compute the PPO clipped surrogate, masked approximate KL, total loss after KL penalty, and report clip fraction, mean ratio, and mean advantage.
- `rlvr_grader_report` must report reward signal, cost, and integrity gate, determining if the verifiable grader is suitable for continued RL-style post-training.
- `merge_lora` must merge `B @ A * scaling` back into the base linear layer weights.

## Grading Rubric

| Item | Points | Criteria |
|------|:--:|------|
| Written questions | 35 | Derive SFT mask, chat template and assistant span, LoRA parameter count, Bradley-Terry RM loss, DPO log-ratio and implicit reward, PPO clipped objective, approximate KL, preference data bias, post-training data gate, GRPO intra-group whitening, RLVR/RFT grader applicability conditions, reward hacking boundaries, and alignment evaluation protocol |
| Programming parts | 55 | Implement SFT dataset/loss, `sft_chat_template_mask_report`, sequence log prob, LoRA, pairwise reward loss, DPO loss, DPO implicit rewards, PPO clipped objective, approximate KL, preference length bias statistics, `post_training_data_audit`, GRPO advantages, GRPO policy loss, and `rlvr_grader_report` |
| Analysis / style | 10 | Distinguish data format, chat template, assistant-only mask, packing boundaries, objective function, reference model, preference data bias, post-training coverage/leakage/safety gate, verifiable reward, grader coverage, helpfulness/honesty/harmlessness, excessive refusal, and capability regression |