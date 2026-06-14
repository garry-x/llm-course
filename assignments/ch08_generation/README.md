# Chapter 8 Assignment: Text Generation

This assignment corresponds to Chapter 8 on Text Generation. The goal is to implement core decoding strategies from logits to tokens, including probability truncation, repetition penalty, constrained decoding, sampling distribution ledger, search, diversity metrics, reasoning multi-sample aggregation, test-time compute budget gate, and speculative decoding speedup ledger, and to verify sampling boundaries and generation behavior with small models.

## Files

- `starter.py`: Starter code.
- `reference_solution.py`: Reference implementation.
- `tests.py`: Runnable tests.

## Run

```bash
.venv/bin/python assignments/ch08_generation/tests.py
```

By default, tests `reference_solution.py`. To test your implementation:

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch08_generation/tests.py
```

## Requirements

- Greedy decoding only uses the logits at the last position and selects `argmax`.
- `temperature=0` must degenerate to greedy, `temperature>0` must divide by temperature.
- Top-K must only sample from the top K tokens, and handle `k > vocab_size`.
- Top-P must retain the smallest nucleus whose cumulative probability reaches the threshold, and renormalize.
- `apply_repetition_penalty` must adjust the logits of already appeared tokens before sampling: divide positive logits by penalty, multiply negative logits by penalty, and must not modify the input in place.
- `apply_token_constraints` must set the logits of tokens invalid under the current grammar/schema state to `-inf`, support different valid token sets per row within a batch, and ensure at least one token remains per row.
- `decoding_distribution_report` must apply repetition penalty, constraint mask, temperature, and top-k/top-p truncation in order, returning the processed logits, final candidate set, normalized probabilities, entropy, and the current highest probability token.
- Beam search must retain multiple candidates, accumulate log probabilities, and support length-normalized scoring.
- `pass_at_k` should use the sampling success rate estimate `1 - C(n-c,k)/C(n,k)`, connecting multi-sample evaluation in code/math tasks.
- `self_consistency_vote` should extract final answers from multiple reasoning outputs, aggregate by majority vote, and report sample count, vote proportion, and token cost.
- `test_time_compute_budget_report` should compare the accuracy, samples, output tokens, latency, cost, and marginal benefit of greedy, self-consistency, best-of-N, verifier reranking, or reasoning model tiers, and output a budget gate indicating whether it is suitable for deployment.
- `speculative_decoding_speedup` should report proposed, accepted, and generated tokens, number of target model verifications, number of draft model steps, approximate time, and speedup based on the number of accepted draft tokens per round, actual written output tokens, `gamma`, and the draft/target cost ratio.
- `Generator` should provide a unified generation interface and be able to compute distinct-n diversity metrics.
- Simplified speculative decoding should return the generated sequence and acceptance rate statistics, facilitating comparison of draft/target consistency.

## Grading Rubric

| Item | Points | Criteria |
|------|:--:|------|
| Written questions | 35 | Compare the applicability boundaries of greedy, beam, temperature, top-k, top-p, repetition penalty, CoT/self-consistency/best-of-N, verifier reranking, speculative decoding, generation evaluation metrics, and constrained decoding |
| Programming parts | 55 | Implement greedy/beam/temperature, top-k, top-p, repetition penalty, token constraints, decoding distribution report, pass@k, self-consistency vote, `test_time_compute_budget_report`, speculative decoding speedup accounting, Generator metrics, and speculative decoding |
| Analysis / style | 10 | Quality of explanation, diversity, factuality, reasoning correctness, test-time compute, latency, cost, marginal benefit, degeneration risk, parameter sweep, and sampling parameter boundaries |