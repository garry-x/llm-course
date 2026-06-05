# Recitation Worksheet Pack

复核日期：2026-06-05

本包提供学生可见的讨论课 worksheet 样例，用于把 [Discussion Section and Office Hours Guide](discussion-office-hours-guide.md)、[Concept Mastery and Misconception Map](concept-misconception-map.md)、[Topic Dependency and Spiral Review Map](topic-dependency-map.md)、[Reading Discussion Question Bank](reading-discussion-question-bank.md)、[Learning Analytics and Remediation Plan](learning-analytics-remediation-plan.md)、[Workload and Pacing Calibration](workload-pacing-calibration.md)、[Notation and Shape Glossary](notation-shape-glossary.md)、[Worked Example Pack](worked-example-pack.md)、[Paper-to-Code Traceability Matrix](paper-to-code-traceability-matrix.md)、[Mathematical Derivation Audit](mathematical-derivation-audit.md)、[Assignment Handout Pack](assignment-handout-pack.md) 和 [Participation and Feedback Guide](participation-feedback-guide.md) 落成可布置、可提交、可反馈的课堂活动。每张 worksheet 都避免给出参考实现，只要求学生写出 shape、错误定位、论文到代码连接和仍不确定的问题。

## 使用规则

- 每次讨论课选择 1 张 worksheet 或拆分其中 2-3 个活动，目标是让学生在 30-60 分钟内完成。
- 学生提交的是 reasoning trace、shape table、failure hypothesis、source boundary 和 exit ticket，不提交隐藏测试答案。
- 助教反馈只指出首个错误假设、缺失证据或过度外推；不代写作业核心函数。
- 若同一 worksheet 中 30% 以上学生卡在同一概念，下一讲应增加 recap，并把问题汇总到 [Course Operations and Improvement Log](course-operations-log.md)。

## Worksheet Schema

| Field | Student output | Staff check |
|-------|----------------|-------------|
| learning_goal | 本次讨论课要证明自己会做什么 | 是否对应 syllabus outcome 或 assignment objective |
| shape_table | 输入、中间张量、输出和 axis 含义 | shape 是否完整且没有 batch/time/head 混淆 |
| failure_hypothesis | 从错误现象推断 1-2 个可能原因 | 是否能用最小反例验证 |
| paper_to_code_link | 一个来源 claim 对应的代码、测试或推导 | 是否匹配 source tier 和边界 |
| source_boundary | 该论文或报告不支持的更强结论 | 是否避免把经验结果写成定理 |
| exit_ticket | 仍不确定的问题和下一步命令 | 是否可用于下次 recap |

## Worksheet W1: BPE, Embedding, RoPE

Mapped materials: Ch01-Ch02, `assignments/ch01_bpe/`, `assignments/ch02_embeddings/`, DER-01, DER-02, DER-03, [Reading List Week 1](reading-list.md).

Learning goal: 手算一次 BPE pair 统计，解释 embedding lookup 的 shape，并把 RoPE 的相对位置性质连接到测试。

Shape table:

| Object | Shape or value | Axis meaning |
|--------|----------------|--------------|
| byte id sequence | `[T]` | token position |
| embedding ids | `[B,T]` | batch, token |
| embedding output | `[B,T,D]` | batch, token, feature |
| RoPE head vector | `[D]` where `D` is even | paired feature dimensions |

Activity:

1. 给定 sequence `[101, 101, 32, 228, 184, 173]`，写出相邻 pair 计数最高的 pair，并说明 tie 时你的规则。
2. 给定 ids `[B,T]` 和 embedding matrix `[V,D]`，写出 lookup 后 shape，并说明它为什么等价于 one-hot 矩阵乘法。
3. 用一句话解释 `R_m^T R_n = R_{n-m}` 为什么是相对位置性质。

Failure drill:

| Symptom | First hypothesis | Minimal check |
|---------|------------------|---------------|
| `_merge([1,1,1], (1,1), 256)` returns `[256,256]` | overlapping merge | Try length-3 repeated pair |
| RoPE norm changes | sin/cos pairing or odd dimension | Compare vector norm before and after rotation |

Paper-to-code link: Sennrich BPE supports rare-word motivation; RoPE paper supports relative rotation structure. These sources do not prove semantic segmentation or unlimited long-context extrapolation.

Exit ticket:

```text
One shape I can now justify:
One implementation bug I can now test:
One source boundary I should remember:
```

## Worksheet W2: Attention and Masking

Mapped materials: Ch03, `assignments/ch03_attention/`, DER-04, DER-05, [Reading List Week 2](reading-list.md).

Learning goal: 推导 scaled dot-product attention 的 score/probability/context shape，并区分 pre-softmax mask 与 post-softmax mask。

Shape table:

| Object | Shape | Axis meaning |
|--------|-------|--------------|
| `q` | `[B,H,T,D]` | batch, head, query time, head dim |
| `k` | `[B,H,S,D]` | batch, head, key time, head dim |
| score | `[B,H,T,S]` | query-key compatibility |
| mask | `[T,S]` or broadcastable | allowed attention positions |
| attention probability | `[B,H,T,S]` | normalized over key positions |
| context | `[B,H,T,D]` | weighted value vectors |

Activity:

1. 对 `T=3,S=3` 写出 causal mask 中哪些位置允许被看见。
2. 解释为什么 score 要除以 `sqrt(d_k)`，写出需要的方差假设。
3. 给一个全 mask 行可能导致 NaN 的例子，并说明如何在测试中暴露。

Failure drill:

| Symptom | First hypothesis | Minimal check |
|---------|------------------|---------------|
| future token changes current output | causal mask leak | Change only future token and compare current logits |
| masked key still has probability | mask applied after softmax or wrong broadcast | Inspect probability row sum over masked positions |

Paper-to-code link: Vaswani et al. supports scaled dot-product attention and decoder masking. It does not prove that an attention heatmap is a faithful explanation of the model decision.

Exit ticket:

```text
The score axis normalized by softmax:
The most likely bug if masked tokens still receive probability:
One attention claim I should not overstate:
```

## Worksheet W3: MHA, GQA, Norm, FFN

Mapped materials: Ch04-Ch05, `assignments/ch04_multihead/`, `assignments/ch05_block/`, DER-06, DER-07, [Reading List Week 3](reading-list.md).

Learning goal: 比较 MHA/GQA 的 KV cache shape，说明 LayerNorm/RMSNorm 的差异，并把 FFN/SwiGLU 看作 token-wise 容量。

Shape table:

| Object | Shape | Axis meaning |
|--------|-------|--------------|
| MHA query heads | `[B,n_heads,T,head_dim]` | every query head has separate projection |
| GQA key/value heads | `[B,n_kv_heads,S,head_dim]` | several query heads share one KV head |
| LayerNorm input/output | `[B,T,D]` | normalize over feature axis |
| FFN input/output | `[B,T,D]` | token-wise transformation |

Activity:

1. 设 `n_heads=16,n_kv_heads=4,head_dim=64`，写出每个 token 的 K cache 元素数量变化。
2. 解释 RMSNorm 为什么不需要减去 mean。
3. 写出 pre-norm block 中 residual 分支的 shape invariant。

Failure drill:

| Symptom | First hypothesis | Minimal check |
|---------|------------------|---------------|
| GQA cache 没有节省 | reduced Q heads instead of KV heads | Count K/V projection output heads |
| LayerNorm gradcheck fails | mean/variance dependency omitted | Compare with PyTorch LayerNorm on small tensor |

Paper-to-code link: GQA paper supports KV head reduction as an efficiency strategy; RMSNorm paper supports non-centering normalization. These sources do not make one head-sharing or norm choice universally optimal.

Exit ticket:

```text
The cache formula term I was missing:
The norm detail I can now explain:
One quality/cost tradeoff I should qualify:
```

## Worksheet W4: GPT, Training, Decoding, Alignment

Mapped materials: Ch06-Ch09, `assignments/ch06_gpt/`, `assignments/ch07_training/`, `assignments/ch08_generation/`, `assignments/ch09_alignment/`, DER-08, DER-09, DER-10, DER-11, DER-12, DER-14, [Reading List Week 4-7](reading-list.md).

Learning goal: 连接 next-token objective、MoE routing、CE/AdamW、top-p/speculative decoding、SFT label mask、LoRA 和 DPO/GRPO 的最小可测证据。

Shape table:

| Object | Shape | Axis meaning |
|--------|-------|--------------|
| logits | `[B,T,V]` | batch, time, vocabulary |
| labels | `[B,T]` | target token or ignore index |
| MoE router weights | `[B,T,k]` | token-level selected experts |
| LoRA A/B | depends on in/out features and rank | low-rank update |
| chosen/rejected logprob | `[B]` | sequence-level preference comparison |

Activity:

1. 解释 decoder-only LM 的 label 为什么右移一位。
2. 写出 logits 与 labels flatten 计算 CE 时哪些 axis 合并。
3. 给定一个 top-p 阈值，说明为什么要保留达到累计概率阈值的最小集合。
4. 标出 prompt、response、padding 中哪些 label 应是 `-100`。
5. 用一句话解释 DPO 为什么需要 reference model。

Failure drill:

| Symptom | First hypothesis | Minimal check |
|---------|------------------|---------------|
| AdamW update equals Adam + L2 | weight decay not decoupled | Hand-calc one scalar update |
| router weights do not sum to one | softmax or top-k gather dimension bug | Check selected expert probability sum |
| top-p removes every token | threshold/sort/cumulative bug | Assert at least one token remains |
| DPO prefers rejected | chosen/rejected direction flipped | Swap inputs and compare loss |

Paper-to-code link: GPT-2, Switch Transformer, AdamW, Holtzman nucleus sampling, LoRA, DPO and DeepSeek-R1/GRPO each support a specific mechanism. They do not prove universal training stability, sampling quality or complete safety alignment.

Exit ticket:

```text
The label position I am most likely to mask incorrectly:
The decoding parameter I can now test:
One alignment claim I should qualify:
```

## Worksheet W5: Inference, RAG, Evaluation

Mapped materials: Ch10 and classic NLP module, `assignments/ch10_inference/`, `assignments/ch11_classic_nlp/`, DER-13, DER-14, [Reading List Week 8-9](reading-list.md).

Learning goal: 估算 KV cache memory，区分 retrieval 与 generation 评测，并说明 BLEU/ROUGE/EM/F1 的边界。

Shape table:

| Object | Shape or scalar | Axis meaning |
|--------|-----------------|--------------|
| K cache | `[B,L,S,n_kv_heads,head_dim]` or implementation equivalent | batch, layer, sequence, head, feature |
| V cache | same as K cache | separate value storage |
| document embeddings | `[N,D]` | document, embedding feature |
| query embedding | `[D]` | embedding feature |
| top-k docs | `[K]` | retrieved candidates |

Activity:

1. 写出 KV cache memory formula 中 batch、layer、sequence、KV head、head dim、dtype bytes 和 K/V factor。
2. 给一个 RAG 检索命中但答案错误的场景，并说明该看哪个 metric。
3. 计算一个短答案的 EM/F1 前，列出 normalization 步骤。

Failure drill:

| Symptom | First hypothesis | Minimal check |
|---------|------------------|---------------|
| cache estimate is half expected | forgot K/V factor | Multiply by 2 and compare units |
| retrieval hit but answer unsupported | generator hallucination or context assembly | Inspect retrieved text and prompt |
| BLEU exact match not one | tokenization or brevity penalty bug | Use identical token lists |

Paper-to-code link: PagedAttention supports KV memory management motivation; RAG supports retriever/generator decomposition; BLEU/ROUGE papers support automatic metric definitions. These sources do not prove factuality or user-level quality for open-ended LLM outputs.

Exit ticket:

```text
The serving metric I would report besides average latency:
The RAG failure type I can now distinguish:
One metric limitation I should state in a report:
```

## Worksheet W6: Capstone Rehearsal and Source Audit

Mapped materials: training capstone, inference capstone, [Project Report Template](project-report-template.md), [Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md), [Frontier Seminar Handout](frontier-seminar-handout.md), [Paper-to-Code Traceability Matrix](paper-to-code-traceability-matrix.md).

Learning goal: 把项目结论拆成可复现命令、数据 split、metric、失败案例、来源等级和边界。

Shape table:

| Object | Shape or value | Axis meaning |
|--------|----------------|--------------|
| evaluation split | `[N]` examples | fixed examples for comparison |
| metric vector | `[M]` metrics | quality, latency, cost, error rate |
| source record | one row per citation | title, tier, date, boundary |

Project evidence table:

| Claim | Evidence required | Current status |
|-------|-------------------|----------------|
| quality improved | fixed evaluation set, baseline, metric, uncertainty | missing / partial / ready |
| training is stable | loss curve, validation metric, seed, checkpoint | missing / partial / ready |
| serving meets SLO | TTFT, TPOT, P50/P95/P99, error rate, hardware | missing / partial / ready |
| source supports design | paper/model card/API doc, date, tier, boundary | missing / partial / ready |

Activity:

1. 写出项目最强 claim 和最弱 claim。
2. 找到一个引用来源，说明它支持哪个设计选择，不支持哪个更强结论。
3. 写出别人复现你项目时应运行的第一条命令。
4. 列出 3 个失败案例类别：数据、模型、评测、服务、成本或来源。

Failure drill:

| Symptom | First hypothesis | Minimal check |
|---------|------------------|---------------|
| report number cannot be reproduced | missing seed, command, split, or checkpoint | Re-run first command and compare log path |
| only average latency reported | insufficient SLO evidence | Add P95/P99, TTFT, TPOT, error rate |
| source is a model card but written as theorem | source tier overclaim | Downgrade claim and add access date |

Paper-to-code link: Every project citation should map to a row in the traceability matrix or a project-specific source audit. A paper, model card or API doc does not support claims outside its stated setting.

Exit ticket:

```text
My project's strongest reproducible evidence:
My project's weakest source or metric boundary:
The next artifact I need to produce:
```

## Staff Feedback Rubric

| Dimension | Complete | Needs revision |
|-----------|----------|----------------|
| Shape reasoning | all axes named and compatible | shape written without axis meaning |
| Failure reasoning | hypothesis can be tested with minimal input | symptom copied without test plan |
| Paper-to-code link | source claim maps to code/test/DER and boundary | source is summarized but not connected |
| Evidence quality | command, metric, or table can be checked | answer relies on impression |
| Exit ticket | next step is actionable | question is too broad to route |

## Release Checklist

| Check | Passing evidence |
|-------|------------------|
| Worksheet coverage | W1-W6 cover tokenization, attention, MHA/norm, training/decoding/alignment, inference/evaluation and capstone |
| Assignment coverage | `assignments/ch01_bpe` through `assignments/ch11_classic_nlp` appear across worksheets |
| DER coverage | DER-01 through DER-14 appear across mapped materials |
| Activity coverage | shape table, failure drill, paper-to-code link and exit ticket appear in every worksheet |
| Boundary coverage | every worksheet has at least one explicit "does not" or "do not" source boundary |
| Student safety | no reference implementation, hidden-test details or private grading rubric appears |
