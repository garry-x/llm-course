# Classic NLP Deep-Dive Teaching Module

This module is used to expand the [Classic NLP Topic Handout](classic-nlp-handout.md) from a discussion session material into a 2-4 lecture topic that can be taught independently. It supplements the [Weekly Reading Material Handout](reading-list.md), [Written Derivation and Conceptual Problem Set](written-problem-set.md), and `assignments/ch11_classic_nlp/`.

The goal is not to turn the course into a traditional full-coverage NLP course, but to ensure students can explain RNN/LSTM, structured prediction, encoder-decoder, and encoder-only representation learning within the classic neural NLP topics of this course.

## Module Outcomes

After completing this module, students should be able to:

| outcome_id | Learning Outcome | Learning Output |
|------------|----------|------------|
| CL-NLP-1 | Describe dependency parsing using a transition system and compute UAS/LAS | Handwritten stack/buffer/arcs trace; Ch11 `run_arc_standard_transitions` and `attachment_scores` tests |
| CL-NLP-2 | Compute scalar RNN hidden states and BPTT gradient chain products, explain why LSTM alleviates long-range dependencies | Ch11 `scalar_rnn_forward` and `recurrent_gradient_factors` tests; handwritten calculation problems |
| CL-NLP-3 | Write down the objectives, search states, and length bias for seq2seq teacher forcing and beam search | Written problems; beam table; metric failure case |
| CL-NLP-4 | Distinguish between encoder-decoder attention alignment and decoder-only causal self-attention | Information flow diagram; short answer on incorrect explanations |
| CL-NLP-5 | Construct BERT-style MLM inputs, labels, loss masks, extractive QA spans, and `[CLS]` no-answer outputs | Ch11 `build_mlm_example` and `select_extractive_qa_span` tests; written problems |
| CL-NLP-6 | Determine what claims BLEU/ROUGE/EM/F1 and human evaluation can each support | Metric counterexamples; short answer explanations |

Minimum passing standard: Students cannot just memorize terminology. For each topic, they must provide a computable example of a state/tensor/metric and explain what that example cannot prove.

## Suggested Lecture Split

| Version | Lecture | Content | Delivery |
|------|------|------|------|
| 10-week compressed version | L15 | RNN/LSTM, dependency parsing, seq2seq, BERT key differences | Ch11 written drill + tests |
| 12-week extended version A | L15 | Dependency parsing and structured prediction | UAS/LAS drill |
| 12-week extended version B | L16 | RNN/LSTM language modeling and BPTT | scalar recurrence + gradient path drill |
| 12-week extended version C | L17 | Seq2Seq/NMT, attention alignment, beam search | beam search / BLEU drill |
| 12-week extended version D | L18 | BERT/encoder-only and representation fine-tuning | MLM label mask drill |
| 12-week extended version E | L19 | Evaluation failure cases and ethics | metric failure examples |

If lecture time is limited, a comparison table of RNN/LSTM, dependency parsing, seq2seq, BERT, and decoder-only LM should still be retained; otherwise, students may easily misinterpret all NLP tasks as prompt-based generation.

## Dependency Parsing Deep Dive

### Formal Setup

Given a sentence token sequence `x_1, ..., x_n`, a dependency parser predicts the head `h_i` and label `l_i` for each token. A legal dependency tree typically requires:

- Each non-root token has exactly one head.
- There exists a root.
- Dependency edges do not form directed cycles.
- Projective parsing also requires edges not to cross; not all linguistic phenomena satisfy strict projectivity.

UAS and LAS:

```text
UAS = count(pred_head_i == gold_head_i) / n
LAS = count(pred_head_i == gold_head_i and pred_label_i == gold_label_i) / n
```

Classroom boundary: UAS/LAS measure whether syntactic edges align, not semantic adequacy, factuality, or generation quality.

### Arc-Standard Oracle Example

Sentence: `I saw her yesterday`

Gold arcs:

- `saw -> I (nsubj)`
- `saw -> her (obj)`
- `saw -> yesterday (advmod)`
- `ROOT -> saw (root)`

| step | stack | buffer | action | arc added | oracle reason |
|------|-------|--------|--------|-----------|---------------|
| 0 | `[]` | `[I, saw, her, yesterday]` | `SHIFT` | - | Need to put dependent and head onto stack |
| 1 | `[I]` | `[saw, her, yesterday]` | `SHIFT` | - | `saw` is the head of `I` |
| 2 | `[I, saw]` | `[her, yesterday]` | `LEFT-ARC(nsubj)` | `saw -> I` | Gold head of second-top `I` is stack-top `saw` |
| 3 | `[saw]` | `[her, yesterday]` | `SHIFT` | - | Read object |
| 4 | `[saw, her]` | `[yesterday]` | `RIGHT-ARC(obj)` | `saw -> her` | Gold head of stack-top `her` is second-top `saw` |
| 5 | `[saw]` | `[yesterday]` | `SHIFT` | - | Read adverbial |
| 6 | `[saw, yesterday]` | `[]` | `RIGHT-ARC(advmod)` | `saw -> yesterday` | Stack-top dependent has no unprocessed children |
| 7 | `[saw]` | `[]` | `ROOT` | `ROOT -> saw` | Root token remains on stack |

### Neural Parser Feature Template

Classic neural dependency parsers often convert the parser state into fixed-length features:

| source | example feature | intuition |
|--------|-----------------|-----------|
| stack top | `s_0`, `s_1`, `s_2` words/POS/labels | Current local structure |
| buffer front | `b_0`, `b_1`, `b_2` words/POS | Words available for shifting |
| left/right children | leftmost/rightmost child of `s_0`, `s_1` | Already built local subtrees |

The model output is a distribution over the next action:

```text
p(a_t | state_t) = softmax(W h(state_t) + b)
```

Misconception boundary:

- The local accuracy of the action classifier does not equal the legality of the final tree.
- Greedy parsing is fast but accumulates errors; beam or dynamic oracle can mitigate this but increases complexity.
- Attention heatmaps cannot automatically replace dependency trees.

Ch11's `run_arc_standard_transitions` implements the action definitions from this section as a runnable state machine. It requires students to handle action legality, that a dependent can only have one head, and that the final parse must exhaust the buffer and assign a head to each token. This is closer to the structured prediction fundamentals required by this course than simply computing UAS/LAS.

## RNN / LSTM Deep Dive

### Scalar RNN Recurrence

The class first uses a scalar version to prevent students from being overwhelmed by matrix notation:

```text
h_t = tanh(w_x x_t + w_h h_{t-1})
o_t = W_o h_t
p(x_{t+1} | x_{\le t}) = softmax(o_t)
```

Given `x=[1.0, 0.5, -1.0]`, `w_x=0.8`, `w_h=0.4`, `h_0=0`, students should be able to compute by hand:

```text
h_1 = tanh(0.8)
h_2 = tanh(0.8 * 0.5 + 0.4 * h_1)
h_3 = tanh(0.8 * -1.0 + 0.4 * h_2)
```

Ch11's `scalar_rnn_forward` corresponds to this recurrence. This small example emphasizes two points: the RNN hidden state is a prefix summary; the same parameters are shared at every time step.

### BPTT Gradient Path

For the same scalar RNN:

```text
dh_t / dh_{t-1} = w_h * (1 - h_t^2)
dL / dh_1 = dL / dh_T * product_{t=2..T} w_h * (1 - h_t^2)
```

Ch11's `recurrent_gradient_factors` returns the local factor for each step. If `|w_h * (1 - h_t^2)| < 1` persists, the gradient for early tokens decays rapidly; if the factor is consistently greater than 1, training can be unstable. This derivation explains why the course supplements gradient clipping, LSTM/GRU, and attention.

### LSTM Gate Interpretation

LSTM splits the hidden state into a cell state and an output state:

```text
c_t = f_t * c_{t-1} + i_t * \tilde{c}_t
h_t = o_t * tanh(c_t)
```

Where `f_t` determines how much old memory to retain, `i_t` determines how much new information to write, and `o_t` determines how much to output. The pedagogical value of LSTM is that it demonstrates the idea of "designing structure for gradient paths," while Transformer further uses attention to shorten cross-position paths and improve training parallelism.

## Seq2Seq / NMT Deep Dive

### Encoder-Decoder Factorization

Given source sentence `x` and target sentence `y`:

```text
p(y | x) = prod_t p(y_t | y_<t, x)
```

During training, teacher forcing uses the gold prefix:

```text
L = - sum_t log p(y_t^gold | y_<t^gold, x)
```

During inference, the model can only use its own generated prefix:

```text
y_t ~ p(y_t | y_<t^model, x)
```

This is the fundamental source of exposure bias: the training conditional distribution and the inference conditional distribution are not perfectly aligned.

### Attention Alignment

At decoder step `t`:

```text
e_{t,i} = score(s_t, h_i)
alpha_{t,i} = softmax_i(e_{t,i})
c_t = sum_i alpha_{t,i} h_i
p(y_t | y_<t, x) = softmax(W [s_t; c_t] + b)
```

Where `h_i` is the source encoder state, `s_t` is the decoder state, and `alpha_t` can serve as an alignment diagnostic.

Ch11's `additive_attention_context` corresponds to this numerical computation. It makes three things clear to students: scores are unnormalized alignment logits; `alpha_{t,i}` is a probability distribution over source positions; the context vector `c_t` has the same dimension as the encoder state and is obtained by a weighted sum of source representations.

Boundary:

- Attention alignment can help locate translation omissions, repetitions, or errors.
- Attention weights are not strict causal explanations, nor are they a substitute for human word alignment.
- The K/V in decoder-only causal attention both come from the same prefix; the K/V in encoder-decoder cross-attention come from the source.

### Beam Search Algorithm

```text
beam = [([BOS], score=0)]
for t in 1..T:
    candidates = []
    for prefix, score in beam:
        for token in top_k(p(token | prefix, x)):
            candidates.append((prefix + [token], score + log p(token)))
    beam = top_B(candidates by score + length_penalty)
return best finished hypothesis
```

Length penalty example:

```text
score_norm(y) = log p(y | x) / ((5 + len(y))^alpha / (5 + 1)^alpha)
```

Classroom checks:

- Beam search is decoding/search, not a training objective.
- Increasing beam size does not guarantee improved semantic quality; it may reduce diversity.
- BLEU is useful at the system level, but risky for individual sentences and open-ended generation.

## Encoder-only / BERT Deep Dive

### MLM Objective

BERT-style MLM first samples mask positions `M`, then computes the loss only at these positions:

```text
L_MLM = - sum_{i in M} log p(x_i | x_{\not M})
```

Input example:

```text
original: [CLS] the cat sat on mat [SEP]
masked:   [CLS] the [MASK] sat on [MASK] [SEP]
labels:   -100  -100 cat   -100 -100 mat    -100
```

`-100` indicates the ignore index; it is not the true classification target for unmasked tokens.

### Encoder Fine-tuning Patterns

| task | representation | head | typical loss |
|------|----------------|------|--------------|
| sentence classification | `[CLS]` final hidden state | linear classifier | cross entropy |
| token classification | each token hidden state | per-token classifier | masked CE |
| extractive QA | token hidden states | start/end classifiers | two CE losses |
| retrieval / embedding | pooled representation | contrastive head | contrastive / triplet loss |

The inference stage for extractive QA typically enumerates candidate spans:

```text
score(i,j) = start_logit_i + end_logit_j,  i <= j,  j-i+1 <= L_max
```

If `[CLS]`'s `start_logit + end_logit` is higher, return no-answer. Ch11's `select_extractive_qa_span` corresponds to this inference process; it advances encoder-only fine-tuning from "knowing there is a head" to "being able to explain how start/end logits produce an answer."

Key differences from decoder-only:

| dimension | encoder-only | encoder-decoder | decoder-only |
|-----------|--------------|-----------------|--------------|
| attention visibility | bidirectional | source bidirectional + target causal | causal |
| main objective | MLM / supervised discriminative | conditional generation | next-token prediction |
| best-fit tasks | classification, tagging, extraction | translation, summarization with source conditioning | generation, dialogue, code, tool use |
| generation ability | not native | native conditional generation | native autoregressive generation |

Misconception boundary:

- BERT is not a default autoregressive generator.
- MLM loss is not equivalent to perplexity in causal LM.
- The `[CLS]` embedding is not a natural "sentence semantic truth value"; it depends on pretraining and fine-tuning.

## Assessment Pack

### In-Class Checks

| check_id | prompt | expected learning output |
|----------|--------|-------------------|
| RNN-1 | Given scalar RNN parameters and 3 inputs, compute hidden states and BPTT gradient factors | Correctly use `tanh` recurrence and `w_h * (1 - h_t^2)` |
| DP-1 | Given a 4-token sentence and gold arcs, write a legal transition sequence | stack/buffer/arcs table, legal actions || DP-2 | Given pred/gold heads and labels, compute UAS/LAS | Denominator, head match, label match correct |
| S2S-1 | Draw encoder-decoder attention information flow | source encoder states, decoder state, cross-attention context |
| S2S-2 | Given beam candidates, compare raw score vs. length-normalized score | Can explain short-sentence bias |
| BERT-1 | Given mask positions, write masked input and labels | only mask positions have labels |
| BERT-2 | Select model families for classification, extraction, generation | Can explain encoder-only/encoder-decoder/decoder-only boundaries |

### Written Problem Templates

1. RNN/LSTM: Given scalar recurrence and hidden states, ask students to compute BPTT gradient product and explain the role of LSTM gates.
2. Dependency parsing: Given a sentence, gold arcs, and a transition system, ask students to write an action trace and explain an illegal action.
3. Seq2Seq/NMT: Given source/target and a decoder step, ask students to write the dependencies of `p(y_t | y_<t, x)`, attention context, and exposure bias.
4. Beam search: Given candidate log probabilities, ask to compare rankings after unnormalized, length-normalized, and length penalty.
5. BERT/MLM: Given tokens and mask positions, ask to write masked input, labels, loss mask, and compare with causal LM labels.
6. Evaluation: Given a high BLEU/low human quality or low BLEU/high human quality example, ask to judge claim strength.

### Programming Learning output

The minimum runnable output for this module is provided by `assignments/ch11_classic_nlp/`:

| function | concept learning output |
|----------|------------------|
| `scalar_rnn_forward` | Recurrent hidden state recursion |
| `recurrent_gradient_factors` | BPTT local gradient factors and long-range paths |
| `run_arc_standard_transitions` | Arc-standard stack/buffer/arcs state transitions |
| `attachment_scores` | UAS/LAS head and label alignment |
| `sentence_bleu` | Clipped precision and brevity penalty |
| `additive_attention_context` | Seq2seq alignment scores, softmax weights, and context vector |
| `rouge_l_f1` | LCS-based precision/recall/F1 |
| `exact_match_and_f1` | QA normalization and token overlap |
| `build_mlm_example` | MLM mask positions, labels, and ignore index |
| `select_extractive_qa_span` | Encoder-only extractive QA start/end span selection |

Optional extension: Have students implement a small beam search function that takes a step-level log probability table as input and outputs the top beam and length-normalized score. If the extension is added, hidden tests should cover EOS, empty beam, tie-breaking, and length penalty.

## Teaching Misconception Register

| misconception | correction | learning output to request |
|---------------|------------|---------------------|
| “Dependency parsing is just an attention heatmap” | Parsing outputs a discrete tree, attention is continuous weight diagnostics | Given heads/labels, compute UAS/LAS |
| “Beam search finds the global optimal translation” | Beam is an approximate search, affected by beam size, length penalty, and model score | Compare candidates for beam size 1/2/4 |
| “High BLEU means the translation is semantically correct” | BLEU measures n-gram overlap, cannot guarantee facts and semantics | Construct examples with lexical overlap but semantic errors |
| “BERT and GPT differ only by mask” | Objective, attention visibility, output usage, and fine-tuning head all differ | Write MLM labels vs. causal labels |
| “Encoder-only cannot be used in modern LLM projects” | Classification, reranking, retrieval embedding, span extraction are still common | Design a RAG reranker or classifier |

## Topic Boundary

The content of this module belongs to stable neural NLP foundations. If subsequent courses add new encoder-only models, NMT benchmarks, or parser papers, they should not replace the basic definitions of this module; they should be added as extension reading to [reading-list.md](reading-list.md), with the task setup and scope of application of the new paper clearly stated.