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
| WE-CH02-ROPE | Ch02 Embedding / Position Encoding / RoPE | Show that RoPE preserves vector norm while changing relative dot products by position difference. | Two 2D query/key vectors `q=[1,0]`, `k=[0,1]`; positions `m=0`, `n=1`; angle `theta`. | Rotate with `R_m` and `R_n`; show `norm(R_m q)=norm(q)`, `norm(R_n k)=norm(k)`, and `(R_m q)^T(R_n k)` depends on `n-m`. | Treating RoPE as adding a position vector; diagnostic is norm drift or loss of relative-position dependence. | `assignments/ch02_embeddings/`, Ch02 written problem | stable theory with notation boundary |
| WE-CH03-ATTN | Ch03 Scaled Dot-Product Attention | Compute masked attention weights for a three-token causal sequence. | `Q,K,V` shape `(T=3,d=2)`; mask blocks future columns above the diagonal. | Compute `QK^T/sqrt(2)`, replace masked logits with large negative value, apply row-wise softmax, multiply by `V`. | Applying softmax before masking; diagnostic is nonzero attention mass on future tokens. | `assignments/ch03_attention/`, DER-04, W2 shape drill | stable theory and implementation detail |
| WE-CH04-GQA | Ch04 MHA / GQA / MLA | Compare KV-cache memory for MHA and GQA with the same query heads. | `n_q=8`, `n_kv=2`, `d_head=64`, `T=1024`, fp16 KV cache. | MHA stores `2*T*n_q*d_head*2` bytes; GQA stores `2*T*n_kv*d_head*2` bytes; ratio is `n_kv/n_q=0.25`. | Counting query heads for KV cache in GQA; diagnostic is no memory reduction despite fewer KV heads. | `assignments/ch04_multihead/`, Ch04 KV-cache analysis | implementation detail tied to architecture |
| WE-CH05-NORM | Ch05 Transformer Block / Norm / FFN | Distinguish LayerNorm centering from RMSNorm scaling. | Vector `x=[1,2,5]`; compare mean-centered variance against root-mean-square. | LayerNorm subtracts mean then divides by standard deviation; RMSNorm divides by `sqrt(mean(x^2)+eps)` without centering. | Claiming RMSNorm output has zero mean; diagnostic is output mean not equal to zero. | `assignments/ch05_block/`, DER-07, written norm question | stable normalization math |
| WE-CH06-PARAMS | Ch06 GPT Assembly / MoE | Estimate GPT block parameter count and identify tied embedding effect. | `vocab=1000`, `d_model=128`, `n_layers=2`, FFN width `4*d_model`. | Count token embedding, position embedding, attention projections, FFN matrices, norms, and LM head; if weights are tied, LM head reuses token embedding. | Double-counting tied LM head; diagnostic is parameter estimate larger by `vocab*d_model`. | `assignments/ch06_gpt/`, project capacity planning | stable implementation accounting |
| WE-CH07-ADAMW | Ch07 Training Loop | Execute one AdamW update and separate gradient update from decoupled weight decay. | Scalar weight `w=1.0`, gradient `g=0.1`, learning rate, betas, epsilon, weight decay. | Update first and second moments, bias-correct, apply adaptive step, then decoupled decay term. | Implementing L2 penalty inside the gradient and calling it AdamW; diagnostic is mismatch on a one-step hand calculation. | `assignments/ch07_training/`, DER-10, optimizer written problem | stable optimizer algorithm |
| WE-CH08-TOPP | Ch08 Generation / Decoding | Compute a nucleus sampling candidate set and explain temperature effect. | Sorted probabilities `[0.40,0.25,0.20,0.10,0.05]`, `top_p=0.80`. | Accumulate until mass reaches threshold: keep first three tokens with mass `0.85`, renormalize before sampling. | Keeping tokens whose individual probability is below `p`; diagnostic is candidate set changes incorrectly when probabilities are sorted. | `assignments/ch08_generation/`, decoding quiz item | stable decoding procedure |
| WE-CH09-DPO | Ch09 Fine-tuning / Alignment | Compute the sign of a DPO preference update from chosen/rejected log-prob ratios. | Chosen log-ratio `0.3`, rejected log-ratio `-0.1`, beta positive. | Preference margin is `0.4`; loss decreases as chosen improves relative to rejected, with reference model anchoring the ratio. | Comparing raw policy log-probs without reference ratios; diagnostic is reward hacking explanation missing the reference term. | `assignments/ch09_alignment/`, DER-12, paper recap DPO anchor | stable algorithmic objective |
| WE-CH10-KVCACHE | Ch10 Inference / RAG / Serving | Show why incremental decoding with KV cache avoids recomputing old keys/values. | Prompt length `T=4`, one new token, `n_layers`, `n_heads`, `d_head`. | Prefill computes KV for 4 tokens; decode step appends one KV row and attends one query over cached 5 positions. | Recomputing all KV tensors at every decode token; diagnostic is per-token latency growing like full-prefix forward cost. | `assignments/ch10_inference/`, inference capstone benchmark/SLO | systems implementation detail |
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
