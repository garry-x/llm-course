# ML Foundations Prerequisite Bridge

This handout summarizes the college calculus, probability/statistics, and foundations of machine learning that will be used repeatedly throughout this course. It is not a standalone machine learning course, but rather maps the minimum concepts learners need to bring into this course to LLM chapters, assignments, and written problems. Related review materials can be found in [Math and PyTorch Prerequisite Review](math-prerequisites.md), [Python and PyTorch Review Session](python-pytorch-review-session.md), and the [Weekly Reading List Handout](reading-list.md).

## Coverage

| Prerequisite Topic | Use in This Course | Minimum Mastery Output |
|----------|------------|--------------|
| Calculus / gradients | loss, backprop, optimizer, LayerNorm, DPO/GRPO | Can explain chain rule, partial derivative, gradient direction, and local linear approximation |
| Probability | language model likelihood, softmax, sampling, perplexity, preference data | Can write conditional probability, joint decomposition, expectation, variance, and log probability |
| Statistics | train/validation split, confidence, benchmark variance, error analysis | Can distinguish sample mean, variance, confidence interval, random seed, and distribution shift |
| ML objectives | maximum likelihood, cross entropy, regularization, preference loss | Can connect formulas to implementations and tests in Ch07/Ch09 |
| Generalization | overfitting, data leakage, contamination, held-out evaluation | Can explain val loss, test set, hidden tests, and the boundaries of the project evaluation set |
| Optimization | gradient descent, learning rate, weight decay, scheduler, early stopping | Can read training curves and propose reproducible experiments |
| Evaluation | metric design, baseline, ablation, statistical uncertainty | Can state what conclusions a metric supports and does not support |

## Diagnostic Add-on

If a learner has not taken a systematic ML course, they should complete the following short diagnostic in Week 0 / Week 1. It can serve as a supplementary sub-section of the Prerequisite Diagnostic.

| Module | Question | Passing Criteria |
|------|------|----------|
| calculus | For `loss = (wx - y)^2`, write `d loss / d w` and explain the gradient descent update direction | Not just applying the formula; can explain how the update changes the prediction |
| probability | Write `P(x_1, x_2, x_3)` as a product of autoregressive conditional probabilities | The conditional objects and order are correct |
| statistics | Given the P95 latency of two benchmark runs, explain why a single run is insufficient to prove one system is faster | Mention variance, sample size, randomness, or load conditions |
| ML objective | Explain why cross entropy corresponds to maximum likelihood | Can connect `-log p_y` to increasing the probability of the correct token |
| generalization | When train loss decreases and val loss increases, list 3 directions for investigation | Mention overfitting, data leakage, split, regularization, or early stopping |
| evaluation | Select at least 3 metrics for a RAG QA project and explain the limitation of each metric | Covers at least two categories among retrieval, generation, and latency/safety |

It is recommended to score as complete/incomplete. If a learner passes fewer than 4 out of 6 questions, they should complete the remedial tasks in this handout before submitting the first graded programming assignment.

## Mini-Lecture: Calculus to Backprop

Learners do not need to hand-write large Jacobians, but they must understand how gradients propagate through a computation graph:

```text
y_hat = model(x; theta)
loss = L(y_hat, y)
theta <- theta - lr * d loss / d theta
```

Minimum requirements:

- chain rule: Gradients of composite functions multiply layer by layer.
- partial derivative: The local change in only one parameter direction for a multi-parameter function.
- gradient vector: The partial derivatives for all parameter directions form the update direction.
- local linear approximation: Small-step updates are approximately explained by the first derivative.

Course connections:

| Course Location | Required Calculus Intuition |
|----------|----------------------|
| Ch03 attention | score, softmax, weighted sum are all in the same computation graph |
| Ch05 LayerNorm | mean and variance depend on the input; backpropagation cannot simply divide by std |
| Ch07 AdamW | gradient, momentum, weight decay, and learning rate have different roles |
| Ch09 DPO | The direction of the chosen/rejected log ratio determines the preference update |

## Mini-Lecture: Probability and Language Models

Autoregressive language models use conditional probability decomposition:

```text
P(x_1, ..., x_T) = product_t P(x_t | x_<t)
log P(x_1, ..., x_T) = sum_t log P(x_t | x_<t)
```

Common probability objects in the course:

| Object | Explanation | Common Misconception |
|------|------|----------|
| softmax probability | Class distribution after logits normalization | Logits themselves are not probabilities |
| cross entropy | Average negative log probability of the target token | Low loss does not mean factually correct |
| perplexity | `exp(cross_entropy)` | PPL alone cannot evaluate open-ended response quality |
| sampling temperature | Changes the sharpness of the distribution | Temperature does not guarantee factuality |
| top-p nucleus | The smallest set whose cumulative probability reaches a threshold | The number of candidates for top-p is not fixed |

## Mini-Lecture: Statistics for Experiments

Training and inference projects must avoid treating a single result as a stable conclusion.

| Statistical Concept | Course Usage | Reporting Requirement |
|----------|----------|----------|
| sample mean | average loss, average latency, average score | Report sample size and conditions simultaneously |
| variance / std | Fluctuation across multiple runs, different prompts, different batches | Explain outliers and failure cases |
| confidence interval | Uncertainty of small-sample evaluations | Can be estimated using bootstrap or repeated runs |
| distribution shift | Differences between train/dev/test or online traffic | Describe the split and representativeness |
| data leakage | Training data, retrieval corpus, or prompt leaking answers | Record deduplication, contamination checks, and held-out sets |
| seed sensitivity | Metric changes due to different initialization or sampling | At least fix the seed, and explain that full reproducibility may still not be possible |

## Mini-Lecture: ML Objectives and Generalization

| Concept | Minimal Explanation | Output for This Course |
|------|----------|------------|
| maximum likelihood | Increase the probability of target tokens or labels in the data | Ch07 CE, Ch09 SFT |
| empirical risk | Average loss over the sample | train/val loss table |
| regularization | Constrain the model or update to reduce overfitting | weight decay, dropout, early stopping |
| baseline | A comparison object that proves the value of the new method | greedy vs top-p, no RAG vs RAG, mock engine vs serving engine |
| ablation | Remove one component to see its effect | LoRA rank, chunk size, cache on/off |
| held-out evaluation | Data not used for training or hyperparameter tuning | validation set, hidden tests, final eval set |

Reports cannot simply state "the model works well." They must at least clearly state:

- What the baseline is.
- What the metric measures.
- How the split was generated.
- Whether the eval set was used for hyperparameter tuning.
- How failure cases are categorized.
- Which conclusions are only valid under the current data, seed, model, or hardware conditions.

## Project Learning Outputs

| learning output_id | Requirement |
|-------------|------|
| objective_mapping | loss, reward, metric, or SLO corresponds to the project objective |
| baseline_result | At least one simple baseline or no-system baseline |
| split_statement | Source of train/dev/test, retrieval corpus/eval queries, or benchmark prompts |
| leakage_check | Data deduplication, prompt leakage, retrieval contamination, or benchmark contamination check |
| variance_note | Explanation of repeated runs, bootstrap, seed sensitivity, or load fluctuation |
| ablation_plan | Comparison of at least one component, hyperparameter, or data processing step |
| metric_limit | Limitation of each key metric |
| generalization_boundary | Conditions under which conclusions cannot be generalized |

## Remedial Tasks

| Weak Area | Remedial Task | Check |
|--------|----------|------|
| calculus | Hand-derive the CE gradient or the DPO log-ratio direction | Can explain the update direction, not just write the formula |
| probability | Complete language model likelihood decomposition and top-p/top-k comparison | Can explain the probability distribution and the sampling candidate set |
| statistics | Calculate mean/std for 3 benchmark results and explain the uncertainty | Report sample size, conditions, and limitations |
| ML objectives | Explain Ch07 training loss, Ch09 SFT/DPO loss, and project metrics separately | Can distinguish between training objectives and evaluation metrics |
| generalization | Write the split, baseline, ablation, and leakage check for the project | Included in the proposal or milestone |
