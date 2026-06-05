# Worked Example Pack


本包把章节正文、讨论课、书面题和编程作业中的核心概念落成可复算例子。它的作用是帮助学生把公式、shape、代码和常见错误连接起来；配套题目见 [书面推导与概念题题库](written-problem-set.md)。

使用规则：

- 每个 worked example 必须能被学生用纸笔或少量 PyTorch 张量复算。
- 每个例子必须说明输入、shape、关键公式、预期中间量、常见错误和关联作业。
- 前沿模型、benchmark、API、价格或硬件性能不能从 worked example 外推为通用事实；需要回到论文、官方文档或模型卡阅读实验条件。
- 例子可以进入 student site release；不得包含隐藏测试输入、reference_solution.py、评分私有样例或真实学生提交。

## Example Schema

| field | requirement |
| --- | --- |
| example_id | Stable `WE-CHxx-NAME` identifier. |
| chapter | Chapter, module, or classic NLP topic. |
| learning target | One observable student action, such as compute, derive, debug, compare, or justify. |
| inputs and shapes | Concrete tensors, token sequences, dimensions, masks, or metric tables. |
| worked trace | Intermediate values sufficient to reproduce the result. |
| common failure | A plausible wrong answer and the diagnostic signal. |
| learning link | Assignment, written problem, recitation worksheet, quiz, or capstone task. |
| scope note | Stable theory, implementation detail, course inference, or volatile external fact. |

## Core Worked Examples

| example_id | chapter | learning target | inputs and shapes | worked trace | common failure | learning link | scope note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WE-CH01-BPE | Ch01 Tokenization / BPE | Compute two BPE merge steps and explain why merges are corpus-dependent. | Corpus tokens `low`, `lower`, `newer`; byte/character pairs counted over word-end markers. | Count adjacent pairs, pick highest frequency, merge once, recount before the next merge; show that `l o` and `e r` can change rank after the first merge. | Reusing the original pair counts after a merge; diagnostic is a merge order that no longer matches current tokenization. | `assignments/ch01_bpe/`, `written-problem-set.md` Ch01, `recitation-worksheet-pack.md` W1 | stable algorithmic procedure |
| WE-CH01-REPORT | Ch01 Tokenization / Evaluation | Compute tokenizer token counts, round-trip success, and embedding parameter budget. | Texts `hello hello`, `世界`, `emoji 😊`; vocab size `280`, `d_model=16`. | Encode each text, average token lengths, take P95 by sorted nearest rank, verify decode(encode(x)) equals x, and compute `280*16` embedding params. | Claiming a tokenizer is good because it round-trips only; diagnostic is no token-cost or embedding-budget comparison. | `assignments/ch01_bpe/`, written Ch01 tokenizer experiment | stable tokenizer metric |
| WE-CH02-SGNS | Ch02 Embedding / Word Vectors | Build a co-occurrence matrix and compute skip-gram negative sampling loss. | Token ids `[0,1,2,1]`, window size `1`, center/positive/negative vectors. | Window counts directed center-context pairs; SGNS uses `-logsigmoid(pos_dot) - sum(logsigmoid(-neg_dot))`. | Treating negative samples as extra positive contexts; diagnostic is using `logsigmoid(neg_dot)` instead of `logsigmoid(-neg_dot)`. | `assignments/ch02_embeddings/`, written Ch02 SGNS problem | stable word-vector objective |
| WE-CH02-ANALOGY | Ch02 Embedding / Word Vectors | Compute cosine similarity and solve a 3CosAdd analogy. | Vectors for `man=[0,1]`, `king=[1,1]`, `woman=[0,2]`, `queen=[1,2]`, `apple=[-1,-1]`. | Query is `king - man + woman = [1,2]`; after cosine normalization and excluding input words, `queen` ranks first. | Returning one of the query words or using raw dot product without normalization; diagnostic is wrong top result on scale-changed vectors. | `assignments/ch02_embeddings/`, written Ch02 analogy problem | empirical static-vector diagnostic |
| WE-CH02-ROPE | Ch02 Embedding / Position Encoding / RoPE | Show that RoPE preserves vector norm while changing relative dot products by position difference. | Two 2D query/key vectors `q=[1,0]`, `k=[0,1]`; positions `m=0`, `n=1`; angle `theta`. | Rotate with `R_m` and `R_n`; show `norm(R_m q)=norm(q)`, `norm(R_n k)=norm(k)`, and `(R_m q)^T(R_n k)` depends on `n-m`. | Treating RoPE as adding a position vector; diagnostic is norm drift or loss of relative-position dependence. | `assignments/ch02_embeddings/`, Ch02 written problem | stable theory with notation boundary |
| WE-CH03-ATTN | Ch03 Scaled Dot-Product Attention | Compute masked attention weights for a three-token causal sequence. | `Q,K,V` shape `(T=3,d=2)`; mask blocks future columns above the diagonal. | Compute `QK^T/sqrt(2)`, replace masked logits with large negative value, apply row-wise softmax, multiply by `V`. | Applying softmax before masking; diagnostic is nonzero attention mass on future tokens. | `assignments/ch03_attention/`, DER-04, W2 shape drill | stable theory and implementation detail |
| WE-CH03-BWD | Ch03 Attention Backward | Compute softmax Jacobian and the gradient from attention output back to logits. | One query with `p` shape `(T,)`, `V` shape `(T,D)`, upstream gradient `g` shape `(D,)`. | First compute `dL/dp_i=g^T v_i`, then `dL/dz_j=p_j(dL/dp_j-sum_i p_i dL/dp_i)`. | Treating softmax as elementwise independent; diagnostic is gradient rows not summing to zero or mismatch with autograd. | `assignments/ch03_attention/`, written Ch03 softmax problem | stable backward math |
| WE-CH03-ENTROPY | Ch03 Attention / Complexity | Compute attention entropy and dense score memory. | Weights `[1,0,0]`, `[1/3,1/3,1/3]`; `B=2,H=4,T=8,fp16`. | Entropies are `0` and `log(3)`; score memory is `2*4*8*8*2` bytes. | Treating a sharp heatmap as causal explanation or forgetting the `T^2` score tensor. | `assignments/ch03_attention/`, Ch03 entropy/complexity written problem | diagnostic metric and memory estimate |
| WE-CH04-GQA | Ch04 MHA / GQA / MLA | Compare KV-cache memory for MHA and GQA with the same query heads. | `n_q=8`, `n_kv=2`, `d_head=64`, `T=1024`, fp16 KV cache. | MHA stores `2*T*n_q*d_head*2` bytes; GQA stores `2*T*n_kv*d_head*2` bytes; ratio is `n_kv/n_q=0.25`. | Counting query heads for KV cache in GQA; diagnostic is no memory reduction despite fewer KV heads. | `assignments/ch04_multihead/`, Ch04 KV-cache analysis | implementation detail tied to architecture |
| WE-CH05-NORM | Ch05 Transformer Block / Norm / FFN | Distinguish LayerNorm centering from RMSNorm scaling. | Vector `x=[1,2,5]`; compare mean-centered variance against root-mean-square. | LayerNorm subtracts mean then divides by standard deviation; RMSNorm divides by `sqrt(mean(x^2)+eps)` without centering. | Claiming RMSNorm output has zero mean; diagnostic is output mean not equal to zero. | `assignments/ch05_block/`, DER-07, written norm question | stable normalization math |
| WE-CH05-RESOURCE | Ch05 Transformer Block / Resource Estimate | Estimate one block's parameter count, FLOPs, and activation memory. | `B=2`, `T=4`, `d_model=8`, `n_heads=2`, `d_ff=16`, fp16. | MHA params `4d^2`; SwiGLU params `3*d*d_ff`; attention score memory `B*H*T*T*dtype_bytes`; major FLOPs sum QKV, scores, value mixing, output projection, and SwiGLU linears. | Confusing parameter memory with activation memory; diagnostic is no `T^2` term for attention scores. | `assignments/ch05_block/`, Ch05 resource written problem | coarse systems estimate |
| WE-CH06-PARAMS | Ch06 GPT Assembly / MoE | Estimate GPT block parameter count and identify tied embedding effect. | `vocab=1000`, `d_model=128`, `n_layers=2`, FFN width `4*d_model`. | Count token embedding, position embedding, attention projections, FFN matrices, norms, and LM head; if weights are tied, LM head reuses token embedding. | Double-counting tied LM head; diagnostic is parameter estimate larger by `vocab*d_model`. | `assignments/ch06_gpt/`, project capacity planning | stable implementation accounting |
| WE-CH07-DATA | Ch07 Training Loop / Data Quality | Compute n-gram repetition and train/eval overlap rates. | Train tokens `[10,11,12,13,20,21,22]`, eval tokens `[0,10,11,12,1,20,21,22]`, `n=3`. | Eval has 6 trigrams; `(10,11,12)` and `(20,21,22)` overlap with train, so overlap rate is `2/6`. | Treating low val loss as proof of generalization without checking overlap; diagnostic is high overlap rate. | `assignments/ch07_training/`, Ch07 written data problem | coarse data-leakage diagnostic |
| WE-CH07-ADAMW | Ch07 Training Loop | Execute one AdamW update and separate gradient update from decoupled weight decay. | Scalar weight `w=1.0`, gradient `g=0.1`, learning rate, betas, epsilon, weight decay. | Update first and second moments, bias-correct, apply adaptive step, then decoupled decay term. | Implementing L2 penalty inside the gradient and calling it AdamW; diagnostic is mismatch on a one-step hand calculation. | `assignments/ch07_training/`, DER-10, optimizer written problem | stable optimizer algorithm |
| WE-CH07-BUDGET | Ch07 Training Loop / Scaling | Compute global batch tokens, optimizer steps, and dense LM training FLOPs. | `micro_batch=4`, `seq_len=2048`, `grad_accum=8`, `data_parallel=16`, `D=20B`, `N=1B`. | Global batch tokens are `1,048,576`; step count is `ceil(20B / 1,048,576)=19,074`; dense LM training FLOPs are approximately `6ND=1.2e20`. | Reporting epochs without token budget or treating parameter count alone as training cost; diagnostic is missing step/FLOP calculation. | `assignments/ch07_training/`, Ch07 written budget problem | coarse scaling estimate |
| WE-CH08-TOPP | Ch08 Generation / Decoding | Compute a nucleus sampling candidate set and explain temperature effect. | Sorted probabilities `[0.40,0.25,0.20,0.10,0.05]`, `top_p=0.80`. | Accumulate until mass reaches threshold: keep first three tokens with mass `0.85`, renormalize before sampling. | Keeping tokens whose individual probability is below `p`; diagnostic is candidate set changes incorrectly when probabilities are sorted. | `assignments/ch08_generation/`, decoding quiz item | stable decoding procedure |
| WE-CH08-BEAM | Ch08 Generation / Search | Rank beam candidates with raw and length-normalized scores. | Candidates `a` with logprob `-0.2`, `a b c` with logprob `-0.8`, alpha `1.0`. | Raw score prefers `a`; normalized scores are `-0.2` and `-0.27`, showing why length penalty changes but does not solve quality. | Treating beam search as a quality metric; diagnostic is no discussion of task type or model probability bias. | `assignments/ch08_generation/`, written Ch08 beam problem | stable decoding search |
| WE-CH09-RM | Ch09 Fine-tuning / Alignment | Compute Bradley-Terry reward-model loss and response-length bias statistics. | Chosen rewards `[3,1]`, rejected rewards `[1,2]`; chosen lengths `[10,8,5,7]`, rejected lengths `[6,8,9,4]`. | Reward margins are `[2,-1]`, so pairwise loss is mean `-logsigmoid`; preference accuracy is `1/2`. Length delta mean is `0.75`; chosen_longer_rate is `1/2`. | Treating higher reward accuracy as proof of better alignment; diagnostic is missing length-bias calculation. | `assignments/ch09_alignment/`, written Ch09 RM/bias problems | stable preference-model objective |
| WE-CH09-DPO | Ch09 Fine-tuning / Alignment | Compute the sign of a DPO preference update from chosen/rejected log-prob ratios. | Chosen log-ratio `0.3`, rejected log-ratio `-0.1`, beta positive. | Preference margin is `0.4`; loss decreases as chosen improves relative to rejected, with reference model anchoring the ratio. | Comparing raw policy log-probs without reference ratios; diagnostic is reward hacking explanation missing the reference term. | `assignments/ch09_alignment/`, DER-12, paper recap DPO anchor | stable algorithmic objective |
| WE-CH10-KVCACHE | Ch10 Inference / RAG / Serving | Show why incremental decoding with KV cache avoids recomputing old keys/values. | Prompt length `T=4`, one new token, `n_layers`, `n_heads`, `d_head`. | Prefill computes KV for 4 tokens; decode step appends one KV row and attends one query over cached 5 positions. | Recomputing all KV tensors at every decode token; diagnostic is per-token latency growing like full-prefix forward cost. | `assignments/ch10_inference/`, inference capstone benchmark/SLO | systems implementation detail |
| WE-CH10-RAG | Ch10 Inference / RAG / Serving | Compute Recall@k and reciprocal rank for a retrieved document list. | Retrieved ids `[doc9, doc2, doc5, doc1]`, relevant ids `{doc1, doc2, doc7}`, `k=3`. | Top-3 contains one of three relevant docs, so Recall@3 is `1/3`; first relevant doc is rank 2, so reciprocal rank is `1/2`. | Judging RAG only from generated answer text; diagnostic is no separate retrieval metric. | `assignments/ch10_inference/`, Ch10 RAG written problem | stable retrieval metric |
| WE-CH11-RNN | Ch11 Classic NLP / RNN Foundations | Compute scalar RNN states and BPTT gradient factors. | `x=[1.0,0.5,-1.0]`, `w_x=0.8`, `w_h=0.4`, `h0=0`. | Recurrence is `h_t=tanh(w_x*x_t+w_h*h_{t-1})`; local gradient factor is `w_h*(1-h_t^2)`. | Treating the final hidden state as if it directly stores all early tokens equally; diagnostic is missing the product of recurrent factors. | `assignments/ch11_classic_nlp/`, classic NLP handout, written problem set | stable sequence-model math |
| WE-CH11-METRICS | Ch11 Classic NLP / Evaluation | Compute dependency UAS/LAS and explain why metric choice changes conclusions. | Three-token sentence with gold heads/labels and predicted heads/labels. | UAS counts matching heads; LAS counts both head and dependency label; one wrong label can keep UAS correct but lower LAS. | Reporting only one metric as overall quality; diagnostic is hidden label errors in high-UAS output. | `assignments/ch11_classic_nlp/`, classic NLP handout, written problem set | stable evaluation definition |

## Recitation Use

| recitation_id | examples | activity | exit learning output |
| --- | --- | --- | --- |
| WE-R1-SHAPE | WE-CH02-ROPE, WE-CH03-ATTN | Students fill shape tables and identify where the mask or rotation enters. | one corrected shape trace |
| WE-R2-SYSTEMS | WE-CH04-GQA, WE-CH10-KVCACHE | Students compute memory ratios and explain latency consequences. | one memory/latency calculation with units |
| WE-R3-OBJECTIVES | WE-CH07-ADAMW, WE-CH09-DPO | Students compare optimizer and preference-objective failure modes. | one signed update explanation |
| WE-R4-EVAL | WE-CH08-TOPP, WE-CH11-METRICS | Students explain why generation and evaluation choices change observed quality. | one metric or sampling boundary note |

## Assessment Coverage

| channel | required use |
| --- | --- |
| programming assignments | Each example links to at least one public assignment suite or capstone task. |
| written assessment | Ch01-Ch10 and Ch11 examples map to written derivation or concept questions. |
| recitation | Recitation rows require students to produce a visible trace, not just a final answer. |
| quiz/checkpoint | Instructors may convert any common failure into a quick check or distractor item. |
| paper recap | Examples with external facts should point students back to the relevant paper, official documentation, or model card. |

## Maintenance Workflow

1. When a chapter formula, starter API, assignment test, or scope note changes, update the corresponding `WE-*` row in this pack.
2. If a worked trace becomes too long for a table, move the expanded trace into lecture notes and keep the `WE-*` row as the index record.
3. If an example depends on a volatile external model or benchmark number, cite the paper or official documentation in the relevant reading notes.
4. Run `.venv/bin/python run_assignment_tests.py` after editing this pack or any linked chapter/assignment.
