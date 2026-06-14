# Math and PyTorch Prerequisite Review

This appendix summarizes the prerequisite knowledge of linear algebra, probability, backpropagation, and tensor differentiation commonly found in university courses. It is not an independent math course, but serves the implementation, derivation, and code analysis in each chapter; refer back to it when encountering shape, mask, loss, or gradient issues within chapters. The bridge from calculus, statistics, and machine learning foundations to the output of this course project can be found in [ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md).

## Full Course Notation and Shape Conventions

To avoid repeating symbol explanations in each chapter, this course uses the following conventions by default. If a particular chapter uses different symbols, it will be explained locally in that chapter.

| Symbol | Meaning | Common shape or unit |
|------|------|------------------|
| `B` | batch size | scalar |
| `T` | query sequence length or current input length | scalar |
| `S` | key/value sequence length, may differ from `T` | scalar |
| `V` | vocabulary size | scalar |
| `d_model` | residual stream hidden size | scalar |
| `H` | query attention heads | scalar |
| `H_kv` | KV heads, can be less than `H` in GQA/MQA | scalar |
| `D` / `d_head` | dimension per head | `d_model / H` |
| `N` | number of parameters or training samples, distinguished by context | count |
| `M` | number of MoE experts or matrix rows, distinguished by context | count |
| `input_ids` | token id sequence | `[B, T]` |
| `embedding_weight` | token embedding table | `[V, d_model]` |
| `hidden_states` | residual stream | `[B, T, d_model]` |
| `logits` | unnormalized vocabulary scores | `[B, T, V]` |
| `labels` | target token ids, may contain `ignore_index=-100` | `[B, T]` |
| `Q` | query states | `[B, H, T, D]` |
| `K, V_attn` | key/value states | `[B, H_kv, S, D]` or `[B, H, S, D]` after repetition |
| `attention_scores` | scaled dot-product logits | `[B, H, T, S]` |
| `attention_mask` | `True` means visible, `False` means masked | broadcastable to `[B, H, T, S]` |

Two easily confused letters:

- `V` usually means vocab size in embedding/LM head; in attention, `V_attn` means the value tensor. In code, avoid writing them as the same variable name.
- `D` often means `d_head` in attention formulas, but may also mean training token budget in training scaling laws. Written derivations must define it first.

## Core Tensor Flow

The minimal forward path for a decoder-only LLM is:

```text
input_ids [B,T]
  -> token embeddings [B,T,d_model]
  -> Transformer blocks [B,T,d_model]
  -> lm_head logits [B,T,V]
  -> shifted CE loss against labels [B,T]
```

The alignment relationship for next-token loss is:

```text
logits[:, t, :] predicts input_ids[:, t+1]
shift_logits = logits[:, :-1, :]
shift_labels = labels[:, 1:]
```

Therefore, if the sequence length of a batch is `T`, there are at most `T-1` next-token supervision positions. SFT, padding, and prompt masks will further remove invalid positions via `ignore_index=-100`, and the denominator for mean reduction should be the number of valid tokens, not `B*T`.

## Mask Semantics

In this course, masks are applied before softmax or loss by default:

| Scenario | Mask Function | Common Mistake |
|------|-----------|----------|
| Causal attention | Mask future keys | Applying mask after softmax, causing probabilities not to sum to 1 |
| Padding attention | Mask padding keys | Only masking padded queries, still allowing real tokens to attend to padding keys |
| SFT / causal LM labels | Positions with `-100` do not participate in loss | Using `-100` directly as an index before gathering |
| MLM labels | Compute CE only on masked positions | Including unmasked tokens in the averaging denominator |
| Constrained decoding | Set illegal token logits to `-inf` | Filtering after sampling, breaking probability semantics |

## Common Objective Functions and Evaluation Targets

| Name | Formula or Computation Target | Question Answered | Question Not Answered |
|------|----------------|------------|--------------|
| Causal LM CE | `-mean log p(x_t | x_<t)` | Does the model fit the next-token distribution? | Is the answer truthful, useful, safe? |
| Perplexity | `exp(CE)` | Average token prediction difficulty | Open-ended task quality |
| SFT loss | CE only on shifted labels of assistant response | Does the model learn answer format and example behavior? | Preference quality or safety boundaries |
| DPO loss | policy/reference chosen-rejected log-ratio | Does the policy improve chosen over reference? | Is the preference data unbiased? |
| PPO/GRPO surrogate | policy ratio, advantage, clip/KL | Is the policy update towards the reward direction and constrained? | Does the reward represent true quality? |
| Recall@k / MRR / nDCG | Retrieval ranking and relevance labels | Does RAG find relevant evidence? | Does the generation faithfully use the evidence? |
| BLEU / ROUGE | n-gram or LCS overlap | Lexical overlap between output and reference text | Factual consistency or semantic equivalence |
| EM / token F1 | Standardized answer or token overlap | Short answer matching for extractive QA | Multi-answer open-ended quality |
| Span F1 | Exact entity match `(type,start,end)` | NER/entity extraction boundaries and types | Token-level partial correctness |
| TTFT / TPOT / tokens/s | Service latency and throughput | User wait time, generation speed, and capacity cost | Semantic quality |

## Minimal Set of Linear Algebra

Learners need to be proficient in:

- Shape conventions for vectors, matrices, and tensors.
- Dimension conditions for matrix multiplication `A @ B`.
- Transpose, broadcasting, element-wise multiplication, and reduction.
- Dot product, norm, cosine similarity.
- Numerical stability of subtracting the maximum value before softmax.

### Checkpoint

Given `Q, K, V` with shapes `[B, H, T, D]`, `[B, H, S, D]`, `[B, H, S, D]` respectively:

- The shape of `Q @ K.transpose(-2, -1)` is `[B, H, T, S]`.
- Multiplying attention probabilities with `V` outputs `[B, H, T, D]`.
- The shape of a causal mask can be `[T, S]`, `[B, T, S]`, or `[B, H, T, S]`, but the semantics must be to mask future positions.

## Probability and Language Models

An autoregressive language model decomposes the sequence probability as:

```text
P(x_1, ..., x_T) = product_t P(x_t | x_<t)
```

Training typically maximizes the token conditional probability, which is equivalent to minimizing cross entropy:

```text
loss = -mean_t log P(target_t | context_t)
```

Perplexity is `exp(loss)`, representing the average number of equivalent candidates remaining at each step.

## Statistics and ML Foundations Entry Point

The statistical and machine learning foundations required for this course's project reports include:

- train / validation / test split.
- baseline, ablation, and held-out evaluation.
- sample mean, variance, seed sensitivity, and benchmark uncertainty.
- overfitting, data leakage, and benchmark contamination.
- The difference between objective, metric, and generalization boundary.

These topics are remediated according to [ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md) and serve as the basis for judging the reliability of conclusions in the training, inference, and evaluation chapters.

## Core Rules of Backpropagation

The following chain rule must be mastered:

```text
z = f(y), y = g(x)
dz/dx = dz/dy * dy/dx
```

For tensor implementations, the focus is not on writing Jacobians by hand, but on understanding how each parameter receives gradients from the loss:

- `Linear`: `y = x W^T + b`, gradients flow to `x`, `W`, `b`.
- `Embedding`: Only the rows of tokens that were indexed receive gradients.
- `LayerNorm`: Gradients must account for the coupling of mean and variance across all feature dimensions.
- `Attention`: `Q/K/V` all receive gradients through scores, softmax, and weighted sum.
- `Cross entropy`: The gradient for logits of valid tokens is `softmax(z)-one_hot(y)`; positions masked by `ignore_index` do not enter the average and do not pass gradients to logits.

## Cross Entropy Derivation Check

For a single sample logits `z` and target class `y`:

```text
p_i = exp(z_i) / sum_j exp(z_j)
loss = -log p_y
d loss / d z_i = p_i - 1[i = y]
```

The log-sum-exp trick should be used in implementation:

```text
logsumexp(z) = m + log(sum_i exp(z_i - m)), m = max_i z_i
```

## LayerNorm Derivation Check

Normalization over the last dimension:

```text
mu = mean(x)
var = mean((x - mu)^2)
x_hat = (x - mu) / sqrt(var + eps)
y = gamma * x_hat + beta
```

In backpropagation, `dx` cannot simply be written as `dy * gamma / sqrt(var + eps)`, because `mu` and `var` both depend on `x`. The correct implementation should pass gradcheck or align with the PyTorch reference implementation.

## DPO/GRPO Derivation Check

The core comparison in DPO is the log probability ratio of chosen vs. rejected under policy/reference:

```text
logit = beta * [(logp_pi(chosen)-logp_ref(chosen)) - (logp_pi(rejected)-logp_ref(rejected))]
loss = -log sigmoid(logit)
```

The key point of GRPO is not the single sample reward, but the group-normalized advantage composed of multiple responses for the same prompt:

```text
A_i = (r_i - mean_group(r)) / (std_group(r) + eps)
```

## PyTorch Implementation Discipline

- Write shape comments or tests for every core function.
- Test functions involving probabilities with extreme logits, masks, empty boundaries, and dtypes.
- Test functions involving gradients with `torch.autograd.gradcheck` or compare against PyTorch official modules.
- Use `.reshape` for tensors that may be non-contiguous, avoiding unintentional reliance on `.view`.
- Do not silently swallow NaN in the training loop; log step, loss, grad_norm, and input batch.