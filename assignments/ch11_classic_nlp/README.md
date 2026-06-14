# Supplemental Assignment: Classic NLP and Evaluation

This supplemental assignment corresponds to the classic NLP topic handout and Week 9 discussion session. The goal is to advance conceptual questions on RNN long-range dependencies, dependency parsing transition system, seq2seq cross-attention, BERT/MLM mask and loss, BIO sequence labeling and span-level F1, Viterbi structured decoding, linear-chain CRF forward algorithm and CRF NLL, BLEU, ROUGE, Exact Match/F1, LLM-as-judge reliability audit and safety evaluation into runnable implementations.

## Files

- `starter.py`: Starter code.
- `reference_solution.py`: Reference implementation.
- `tests.py`: Runnable tests.

## Run

```bash
.venv/bin/python assignments/ch11_classic_nlp/tests.py
```

Default tests `reference_solution.py`. To test your implementation:

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch11_classic_nlp/tests.py
```

## Requirements

- `attachment_scores` computes UAS/LAS, must check that heads and labels have consistent lengths.
- `run_arc_standard_transitions` executes `SHIFT`, `LEFT_ARC(label)`, `RIGHT_ARC(label)` and `ROOT(label)`, returns heads, labels, arcs and stack/buffer trace.
- `scalar_rnn_forward` and `recurrent_gradient_factors` demonstrate tanh RNN state recurrence and BPTT gradient products.
- `additive_attention_context` computes alignment scores, softmax weights and context vector via `v^T tanh(W_s s_t + W_h h_i)`.
- `sentence_bleu` uses clipped n-gram precision and brevity penalty.
- `rouge_l_f1` computes precision, recall and F1 using the longest common subsequence.
- `exact_match_and_f1` normalizes QA strings, then computes exact match and token F1.
- `build_mlm_example` generates BERT-style masked input and labels based on mask positions.
- `masked_lm_loss_from_logits` computes MLM cross entropy and masked-token accuracy only at non-ignored label positions.
- `bio_tags_to_spans` decodes token classification / NER entity spans from BIO tags, must distinguish `B-`, `I-` and `O`.
- `span_f1` must exactly match entity spans using `(type, start, end)`, reports precision, recall, F1, TP, FP and FN.
- `viterbi_decode` decodes the optimal tag path for a linear-chain sequence model using emission, transition, start/end scores.
- `linear_chain_log_partition` computes the CRF normalization term over all tag paths using the logsumexp forward algorithm.
- `linear_chain_crf_nll` must compute the gold path score and return the structured negative log-likelihood `log_partition - gold_score`.
- `select_extractive_qa_span` selects a valid answer span based on encoder-only QA head start/end logits, and supports `[CLS]` no-answer.
- `summarize_pairwise_judgments` aggregates blind pairwise LLM-as-judge results, computes raw win rate, tie-adjusted win rate, and per-task win rates.
- `judge_reliability_audit` must check LLM-as-judge records for sample size, A/B position bias, long answer bias, swapped-order consistency and agreement with human gold labels; when checks fail, should provide action items for re-randomizing order, controlling length, changing judge prompt/model, or supplementing human annotations.
- `safety_evaluation_metrics` computes attack success, harmful refusal, over-refusal and task utility across harmful, benign sensitive and ordinary sample categories.
- `benchmark_result_summary` organizes task, sample size, metrics, prompt/temperature/model, failure types and non-extrapolatable scope into a structured benchmark conclusion.

## Written Drill Expectations

- Following the `I saw her` worked example from `classic-nlp-handout.md`, write out the stack / buffer / arcs transition table.
- Given scalar RNN parameters, manually compute 3-step hidden states and `prod_t w_hh * (1 - h_t^2)`, explaining gradient vanishing or explosion.
- Write out the conditional probability decomposition `p(y | x)` for seq2seq, teacher forcing loss, and explain the meaning of `alpha_{t,i}` and `c_t` in cross-attention.
- Given a set of beam candidates, compare ranking by sum log prob, length-normalized score, and length penalty.
- Given BERT tokens, mask positions, vocab logits and labels, write out the masked input, loss positions, MLM cross entropy and masked-token accuracy; given start/end logits, write out the best answer span for extractive QA.
- Given BIO tags, decode entity spans; given gold/pred spans, compute span-level precision, recall, F1, and explain why an illegal `I-` start or type switch is typically treated as a new span or flagged as an error in strict evaluation.
- Given emission and transition score tables, manually compute the Viterbi DP table, CRF forward alpha table, gold path score and CRF NLL, explaining the difference between max-path decoding, logsumexp normalization and the training objective.
- Given a candidate/reference, explain what BLEU clipped precision, ROUGE-L, EM/F1 would reward or penalize.
- Construct a metric failure case where BLEU, ROUGE, EM/F1 or LLM-as-judge gives a high score but human quality is poor.
- Given pairwise judge records, compute the tie-adjusted win rate, and explain why A/B order must be randomized, model names hidden, results stratified by task, and judge trustworthiness audited via swapped-order consistency and human-label agreement.
- Given output counts for harmful, benign sensitive and ordinary groups, compute attack success rate, over-refusal rate and task utility respectively, explaining why a high refusal rate alone does not represent safety.

## Scoring Rubric

| Item | Points | Criteria |
|------|:--:|------|
| Written questions | 40 | Explain relationships among RNN long-range dependencies, dependency parsing, seq2seq/cross-attention, beam search length bias, BIO sequence labeling, span-level F1, Viterbi/CRF forward/CRF NLL, BLEU, ROUGE-L, QA EM/F1, BERT MLM mask/loss, LLM-as-judge bias and LLM evaluation |
| Programming parts | 50 | Implement arc-standard transition parsing, RNN recurrence, BPTT gradient factors, UAS/LAS, seq2seq additive attention, BIO span decoding, span-level F1, Viterbi decoding, CRF log-partition, CRF NLL, BLEU, ROUGE-L, QA EM/F1, MLM mask example, MLM loss, extractive QA span selection, pairwise judge aggregation, judge reliability audit and safety metrics |
| Analysis / style | 10 | Construct at least 2 examples where metrics are high but human quality is poor, and explain metric limitations; benchmark conclusions must include task, sample size, inference settings, judge bias audit, failure types and non-extrapolatable scope |