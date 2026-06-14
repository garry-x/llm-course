# Classic NLP Topics Handout

This handout is used to connect common topics in classic neural NLP that are easily compressed in the main LLM storyline back to the course chapters. It is recommended to schedule 1-2 discussion sessions during lectures, or use it as background reading for Ch11 and the final project.

## 1. Dependency Parsing

The goal of dependency parsing is to establish directed dependency edges between words in a sentence. For example, in `I saw her`, `saw` is the predicate head, `I` depends on `saw` as the subject, and `her` depends on `saw` as the object.

### Arc-Standard Transition System

The state consists of:

- **Stack**: Words that have been partially processed.
- **Buffer**: Words that have not yet been processed.
- **Arcs**: Dependency edges that have been established.

Operations:

- `SHIFT`: Move the first word from the buffer to the stack.
- `LEFT-ARC(label)`: Make the top word on the stack the head, connect it to the second-top dependent, and pop the dependent.
- `RIGHT-ARC(label)`: Make the second-top word on the stack the head, connect it to the top dependent, and pop the dependent.

### Worked Example: `I saw her`

Let the token IDs be `0=I, 1=saw, 2=her`, and the gold arcs be `saw -> I (nsubj)`, `saw -> her (obj)`, with `saw` as the root. A valid arc-standard transition sequence is as follows:

| Step | Stack | Buffer | Action | New arc |
|------|-------|--------|--------|---------|
| 0 | `[]` | `[I, saw, her]` | `SHIFT` | - |
| 1 | `[I]` | `[saw, her]` | `SHIFT` | - |
| 2 | `[I, saw]` | `[her]` | `LEFT-ARC(nsubj)` | `saw -> I` |
| 3 | `[saw]` | `[her]` | `SHIFT` | - |
| 4 | `[saw, her]` | `[]` | `RIGHT-ARC(obj)` | `saw -> her` |
| 5 | `[saw]` | `[]` | `ROOT` or end | `ROOT -> saw` |

Classroom Check:

- The head/dependent direction for `LEFT-ARC` and `RIGHT-ARC` cannot be guessed by the literal meaning of "left/right"; it depends on the system definition.
- The `run_arc_standard_transitions` function in Ch11 executes the actions from this table and returns heads, labels, arcs, and the stack/buffer trace; learners need to use code to check if each action satisfies the system constraints.
- If the predicted heads are `[1, -1, 1]` and labels are `["nsubj", "root", "obj"]`, both UAS and LAS are 1.0.
- If the head of `her` is predicted to be `I`, but the label is still `obj`, both UAS and LAS will decrease; LAS is only counted when both the head and the label are correct.

### Metrics

- **UAS**: Unlabeled Attachment Score, only checks if the head is correct.
- **LAS**: Labeled Attachment Score, requires both the head and the dependency label to be correct.

Course Purpose: Train learners to decompose a structure prediction problem into states, actions, loss, and evaluation, rather than only looking at generative LLMs.

## 2. RNN / LSTM: From Recurrent Language Models to Attention

Before Transformers, neural language models and sequence labeling commonly used RNNs, GRUs, or LSTMs. The core idea of an RNN is to use a hidden state to summarize the prefix that has been read:

```text
h_t = tanh(W_x x_t + W_h h_{t-1} + b)
p(x_{t+1} | x_{\le t}) = softmax(W_o h_t)
```

This formula models "predicting the next token given the prefix" just like a decoder-only LM, but the information path is completely different. In an RNN, for information at position 1 to influence position 100, it must pass through 99 state updates; in a Transformer, position 100 can directly read the representation of position 1 via self-attention.

### BPTT and Vanishing Gradients

Backpropagation Through Time (BPTT) unrolls the same RNN cell over time. For a scalar RNN:

```text
h_t = tanh(w_x x_t + w_h h_{t-1})
dh_t / dh_{t-1} = w_h * (1 - h_t^2)
```

Therefore, when propagating a loss from a later time step back to an earlier state, a product chain appears:

```text
dL / dh_1 = dL / dh_T * product_{t=2..T} w_h * (1 - h_t^2)
```

If the absolute values of these factors are consistently less than 1, the gradient will shrink rapidly; if they are consistently greater than 1, the gradient will explode. LSTMs mitigate this problem through input/forget/output gates and a cell state, but they still retain a sequential computation path.

### LSTM Gating Intuition

Simplified notation:

```text
f_t = sigmoid(W_f [h_{t-1}; x_t])
i_t = sigmoid(W_i [h_{t-1}; x_t])
o_t = sigmoid(W_o [h_{t-1}; x_t])
\tilde{c}_t = tanh(W_c [h_{t-1}; x_t])
c_t = f_t * c_{t-1} + i_t * \tilde{c}_t
h_t = o_t * tanh(c_t)
```

`f_t` controls the retention of old memory, `i_t` controls the writing of new information, and `o_t` controls how much of the state is exposed to the output. The key to LSTMs is not that they are "more complex and therefore stronger", but that the cell state provides a more stable gradient pathway.

### Systematic Differences from Transformers

| Dimension | RNN / LSTM | Transformer self-attention |
|------|------------|----------------------------|
| Training Parallelism | Sequential dependency on time steps, difficult to fully parallelize | All positions within the same layer can be computed in parallel |
| Long-range Path | Path length grows linearly with distance | A single layer can directly connect any two positions |
| State Bottleneck | Prefix compressed into a fixed-dimension hidden state | Each token retains its own representation |
| Inference Cache | Hidden state or cell state | K/V cache for each layer |
| Typical Strengths | Small models, streaming sequences, low-resource scenarios | Large-scale pre-training, long contexts, parallel training |

Course Purpose: RNNs are not an outdated term, but a foundation for understanding teacher forcing, BPTT, long-range dependencies, and the motivation for attention. Modern LLMs no longer use RNNs as their backbone, but many training concepts still originate from this historical path.

## 3. Seq2Seq / Neural Machine Translation

Seq2Seq models encode an input sequence into a context representation, and then a decoder autoregressively generates the target sequence. Attention allows the decoder to weight source tokens based on its current state at each step, rather than relying on a single fixed vector.

### Conditional Probability Decomposition

Given a source sentence `x = (x_1, ..., x_m)` and a target sentence `y = (y_1, ..., y_n)`, an encoder-decoder model learns the conditional distribution:

```text
p(y | x) = product_t p(y_t | y_<t, x)
```

During training, teacher forcing is commonly used, meaning the decoder sees the gold prefix `y_<t^gold` at step `t`:

```text
loss = - sum_t log p(y_t^gold | y_<t^gold, x)
```

During inference, the model can only see the prefix `y_<t^model` it has generated itself. The training condition and the inference condition are not exactly the same; this is one source of exposure bias.

### Cross-Attention Information Flow

Let the encoder output source representations `H = [h_1, ..., h_m]`, and the decoder hidden state at step `t` be `s_t`. A simplified additive attention is written as:

```text
score_{t,i} = v^T tanh(W_s s_t + W_h h_i)
alpha_{t,i} = softmax_i(score_{t,i})
c_t = sum_i alpha_{t,i} h_i
p(y_t | y_<t, x) = softmax(W_o [s_t; c_t])
```

Here, `alpha_{t,i}` is the attention weight of the decoder at step `t` on the `i`-th token of the source. It can help diagnose omissions, repetitions, or mistranslations, but it cannot be directly treated as a strict causal explanation.

The `additive_attention_context` function in Ch11 turns this set of formulas into a pure Python exercise: learners need to first calculate the score for each source position, then perform softmax normalization, and finally use `alpha` to compute a weighted sum of the encoder states to get `c_t`. The focus of this exercise is not to train a translation system, but to translate the information flow of encoder-decoder attention from a diagram into a numerically reproducible calculation.

### Core Issues

- **Exposure bias**: During training, the decoder sees the gold prefix; during inference, it sees the prefix it generated itself.
- **Beam search**: Keeps multiple candidate sequences, but tends to favor short sentences, so a length penalty is often added.
- **Alignment**: Attention weights can roughly explain the correspondence between source and target words, but they are not a strict causal explanation.

### BLEU

BLEU is based on n-gram precision and a brevity penalty. It is suitable for system-level comparison of machine translation, but it is unstable for single-sentence quality, semantically equivalent paraphrasing, and open-ended generation.

### Worked Example: Beam Search Length Bias

Assume the decoder gives two candidates at a certain step:

| Candidate | token log probs | sum log prob | length | normalized score `sum / length` |
|-----------|-----------------|--------------|--------|---------------------------------|
| `a` | `[-0.20]` | `-0.20` | 1 | `-0.20` |
| `a b c` | `[-0.20, -0.30, -0.30]` | `-0.80` | 3 | `-0.27` |

If only comparing the sum of log probabilities, the short candidate `a` is more likely to win because each additional generated token multiplies by a probability less than 1. Length normalization or a length penalty does not guarantee that a longer sentence is always better, but it can reduce the "too-short translation" bias. In open-ended generation, beam search can also lead to low diversity; sampling is more suitable for exploring diverse outputs, but requires temperature, top-k/top-p, and safety filtering.

Classroom Check:

- Beam search is a search strategy, not a training objective.
- Attention alignment can be used as a translation diagnostic, but it cannot automatically prove a model's causal explanation.
- BLEU's brevity penalty can only mitigate overly short outputs; it does not solve issues of semantically equivalent paraphrasing, factuality, or coreference errors.

Course Purpose: Help learners understand the encoder-decoder tradition before decoder-only LLMs, and why modern instruction models still use beam/search/rerank ideas.

## 4. Encoder-only / BERT

BERT uses a bidirectional Transformer encoder and is pre-trained using Masked Language Modeling (MLM) and Next Sentence Prediction. Unlike a causal LM, MLM can look at both left and right contexts, only predicting the masked positions.

### Differences from Causal LM

| Dimension | BERT / Encoder-only | GPT / Decoder-only |
|------|---------------------|--------------------|
| Attention | Bidirectional visibility | causal mask |
| Pre-training | MLM | next-token prediction |
| Output | token/CLS representation | next token logits |
| Typical Tasks | Classification, extraction, sequence labeling | Generation, dialogue, code |

Course Purpose: Connect the classic methods of representation learning and discriminative NLP to the task modeling in Ch11, allowing learners to understand that not all NLP tasks are inherently suited for autoregressive generation.

### Worked Example: BERT-style MLM Tensor

Input tokens:

```text
[CLS] the cat sat [SEP]
```

If the mask positions are `[2, 3]`, then:

| Field | Value |
|-------|-------|
| masked input | `[CLS] the [MASK] [MASK] [SEP]` |
| labels | `None, None, cat, sat, None` |
| attention | Bidirectional self-attention, can see left and right context |
| loss positions | Loss is only calculated at mask positions |

Comparison with causal LM:

- A causal LM trains on `the -> cat -> sat` for next-token prediction, only seeing the left context.
- MLM can simultaneously use the context around `the` and `[SEP]` to predict `cat/sat`, but it does not directly train for autoregressive generation.
- BERT fine-tuning commonly uses the `[CLS]` representation for classification, or can be used for token classification or span extraction; it is not a default decoder-only generative model.

### Worked Example: Extractive QA Span

Extractive QA assigns two scores to each token: `start_logit_i` and `end_logit_i`. The model selects a span that satisfies `start <= end` and does not exceed a maximum length, maximizing `start_logit_start + end_logit_end`. A no-answer option, like in SQuAD 2.0, is usually represented by the `[CLS]` start/end scores.

The `select_extractive_qa_span` function in Ch11 lets learners implement this step: enumerate valid spans, compare scores, and return an empty answer when the `[CLS]` score is higher. It emphasizes that encoder-only models can perform discriminative extraction, rather than generating a new piece of text.

## 4. Evaluation

University-level NLP courses must enable learners to distinguish between "optimization objectives" and "evaluation metrics".

| Metric | Applicable Task | Limitation |
|------|----------|------|
| Perplexity | Language model fit | Not directly equivalent to factual correctness or usefulness |
| Accuracy / F1 | Classification, extraction | Label definitions and class imbalance can affect interpretation |
| Exact Match | QA, code, math | Too strict for equivalent expressions |
| BLEU | Machine translation | Unstable for semantic paraphrasing and single-sentence evaluation |
| ROUGE | Summarization | Biased towards lexical overlap |
| Human Eval | Open-ended tasks | High cost, difficult to ensure consistency |
| LLM-as-judge | Large-scale preference evaluation | Potential position bias, model bias, and contamination risk |

Project reports should not only provide a single average score. They should at least include per-task results, failure cases, error types, and metric limitations.

### Computable Definitions of Common Metrics

**BLEU** uses clipped n-gram precision and a brevity penalty:

```text
BLEU = BP * exp(sum_n w_n log p_n)
BP = 1                  if candidate_len > reference_len
BP = exp(1 - reference_len / candidate_len) otherwise
```

Where `p_n` is the clipped precision of n-grams in the candidate translation that match the reference translation. BLEU is suitable for system-level machine translation comparison, but not for single-sentence semantic judgment.

**ROUGE-L** is based on the longest common subsequence `LCS(candidate, reference)`:

```text
precision = LCS / candidate_len
recall = LCS / reference_len
F1 = 2 * precision * recall / (precision + recall)
```

It is commonly used for summarization tasks because summaries may not require word-for-word exactness; however, a high ROUGE score might still only mean copying similar text, not factual correctness.

**Exact Match / token F1** is commonly used for extractive QA. Exact Match requires the normalized strings to be exactly identical; token F1 first calculates the token overlap between the predicted answer and the gold answer, then takes the harmonic mean of precision/recall. They are unstable for open-ended answers, synonymous paraphrasing, and multi-answer questions.

### Metric Failure Cases

| Case | Metric looks good | Human issue | Lesson |
|------|-------------------|-------------|--------|
| Translation synonym | BLEU low, because n-grams don't overlap | Semantics may be correct | BLEU cannot determine quality for a single sentence |
| Extractive QA punctuation | EM low, because of format difference | Answer entity is the same | EM is too strict, needs to be combined with normalized F1 |
| RAG copy overlap | ROUGE high, because it copies the retrieved snippet | The snippet may not answer the question | Lexical overlap does not equal factual correctness |
| Long answer latency | quality score high | P95 latency exceeds SLO | Quality metrics must be combined with system metrics |
| LLM judge preference | judge prefers longer answers | May be verbose or hallucinated | Requires blind pairwise, position swap, and manual spot-checking |

### Agent / Workflow Evaluation

An LLM course for training and inference engineers cannot only evaluate the "final text answer". Once the system includes tools, RAG, code execution, a browser, database writes, or multi-turn user interaction, the object of evaluation becomes a stateful workflow: the model must not only answer correctly, but also call the correct tool at the right time, adhere to policies, control costs, and avoid irreversible side effects.

Typical benchmarks reflect different workflow capabilities:

| Benchmark Type | Evaluation Object | Protocol to Abstract in the Course |
|----------------|----------|----------------------|
| SWE-bench-like code repair | Given a real issue and codebase, generate a patch and pass tests | Task success rate must be determined by hidden tests or regression tests, while recording repo version, tool environment, patch diff, and failure type |
| tau-bench-like tool-user interaction | Multi-turn user, domain policy, API tool, and final database state | Cannot only look at the reply text; must check action correctness, policy compliance, state delta, consistency across repeated trials, and unauthorized actions |
| BrowseComp-like browsing agent | Find a hard-to-find but verifiable short answer on a webpage | Need to record search strategy, cited evidence, browsing depth, time/call budget, and answer verifiability; a high score on a short answer does not mean the open-ended research is reliable |

The course evaluation protocol should be divided into at least four layers:

1. **Task success.** Whether the user's task is solved: tests passed, target state achieved, answer verifiable, or human acceptance passed.2. **Trajectory quality.** Whether tool selection, parameters, order, retries, loops, handoffs, retrieval, and citations are reasonable.
3. **Safety and side effects.** Whether it violates permissions, leaks data, executes irreversible actions, pollutes state, or bypasses policy.
4. **System cost.** wall time, LLM calls, tool calls, prompt/completion tokens, P95 latency, external API costs, and failure retry costs.

The pre-release agent eval gate should fix the environment and task version: tool registry, API schema, database snapshot, retrieval library, browser/network conditions, hidden tests, judge rubric, random seed, and temperature. Public benchmarks can only serve as regression signals and cannot replace private task sets, production canaries, and trace replay; otherwise, the model may simply adapt to the question bank, tool environment, or scorer.

Classroom check:

- Metrics are a compression of task assumptions, not a synonym for "true quality."
- When reporting averages, the sample size, split, confidence interval, or single_seed_limit must be stated.
- For open-ended LLM tasks, automatic metrics, human error analysis, and resource metrics should appear simultaneously.
- For agent/workflow tasks, final answer, trajectory, state changes, safety side effects, and system cost must be reported separately.

## 5. Ethics / Safety

LLM course engineering projects must cover the following risks:

- Data privacy: Whether the training or RAG corpus contains sensitive information.
- Bias and representation: Whether the data systematically ignores certain languages, regions, or groups.
- Hallucination: The model generates content unsupported by retrieval output.
- Evaluation contamination: Whether the benchmark or answers appear in the training/tuning data.
- Safety refusal: Whether the model gives inappropriate operational advice for high-risk requests.
- Copyright and citation: Whether generated content or training data requires source attribution.

It is recommended that project reports include a "Safety and Limitations" section, listing at least 3 risks, trigger examples, and mitigation strategies.

## Suggested Classroom Activities

1. Spend 10 minutes manually computing a dependency parsing transition sequence.
2. Spend 15 minutes comparing BLEU scores and human preference differences for the same translated sentence.
3. Spend 15 minutes designing a text classification task as both BERT fine-tuning and GPT prompting.
4. Spend 20 minutes analyzing a RAG failure case, identifying the responsibility boundaries of retrieval, generation, and evaluation.
5. Spend 20 minutes analyzing an agent trace, identifying the responsibility boundaries of tool schema, policy, state delta, side effect, latency, and final task success.

## Mini-Recitation Activities

| Topic | Board artifact | Learner action |
|-------|----------------|----------------|
| Dependency parsing | stack / buffer / arcs transition table | Write a valid action sequence and calculate UAS/LAS |
| Seq2Seq / NMT | beam table with sum and normalized score | Explain length bias and length penalty |
| BERT / MLM | masked input + labels table | Distinguish MLM loss positions from causal LM labels |
| Evaluation | metric failure-case table | Determine which metric supports the conclusion and which metric fails |
| Agent evaluation | trace + state delta + tool call table | Determine if final success, trajectory quality, safety side effects, and cost all pass the gate simultaneously |
| Ethics / Safety | risk / trigger / mitigation table | Connect the failure case to data, model, system, or evaluation causes |