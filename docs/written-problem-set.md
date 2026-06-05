# 书面推导与概念题题库

本题库对应 README 中 20% 的“书面推导与概念题”。它补充自动编程测试无法覆盖的数学、复杂度、实验解释和工程判断。每章建议选 2-3 题作为正式作业，剩余题作为讨论课或期末复习；逐章可复算小例子见 [Worked Example Pack](worked-example-pack.md)。

## 评分规则

| 维度 | 分值 | 标准 |
|------|:--:|------|
| 数学正确性 | 35 | 符号、条件概率、矩阵维度、梯度或复杂度推导正确 |
| Shape 与边界 | 20 | 写清 batch、sequence、head、vocab、mask 等 shape，并覆盖边界条件 |
| 工程解释 | 20 | 能把公式和 PyTorch 实现、显存、延迟、稳定性联系起来 |
| 实验判断 | 15 | 能解释测试输出、失败案例、ablation 或指标局限 |
| 表达与引用 | 10 | 答案结构清晰，必要时引用论文/官方文档/模型卡 |

## Ch01 Tokenization / BPE

1. 设语料 token 序列长度为 `N`，词表大小从 `V0` 增加到 `V`。说明 BPE 每次合并如何改变序列长度，并给出贪心合并不能保证全局最优压缩的反例思路。
2. 比较 word-level、character-level、byte-level BPE 在 OOV、多语言、序列长度和 embedding 参数量上的取舍。
3. 设计一个 tokenizer 评价实验：比较英文、中文、代码、数学公式和 emoji 混合文本的平均 token 数、P95 token 数、round-trip 成功率和 embedding 参数量，并说明这些结果如何影响 context、训练 FLOPs 和 KV Cache 成本。
4. 给定一个小语料，手算前 3 次 BPE merge，并说明 tie-breaking 会怎样影响最终词表。

## Ch02 Embedding / Position Encoding / RoPE

1. 从 one-hot 矩阵乘法推导 embedding lookup，说明为什么 `E[token_id]` 等价于 `one_hot @ E`。
2. 给定 token 序列 `[0,1,2,1]` 和 window size 1，手算 directed co-occurrence matrix；再给定 center/positive/negative 向量，写出 SGNS loss。
3. 比较 skip-gram negative sampling 与 GloVe：它们分别从局部上下文样本和全局共现矩阵中学习什么统计信号？为什么类比推理不是训练目标直接保证的性质？
4. 证明 sinusoidal position encoding 的相对位移可以由线性变换表示，即 `PE(pos+k)` 可以由 `PE(pos)` 的 sin/cos block 旋转得到。
5. 证明 RoPE 点积只依赖相对位置：`(R_m q)^T (R_n k) = q^T R_{n-m} k`，并解释为什么这对长上下文外推有帮助但不是充分条件。

## Ch03 Scaled Dot-Product Attention

1. 若 `q_i, k_i` 独立且均值 0、方差 1，推导 `q^T k` 的方差，并说明为什么 attention scores 要除以 `sqrt(d_k)`。
2. 写出 causal mask 在 `T=4` 时的矩阵，并说明 mask 值应该在 softmax 前还是 softmax 后应用。
3. 推导 softmax Jacobian `J_ij = p_i(delta_ij - p_j)`，并说明 attention 输出梯度如何通过 `p @ V` 传回 logits。
4. 分析 self-attention 的时间复杂度和显存复杂度，区分训练时保存 activation 与推理时 KV Cache 的差异。
5. 给定一张 attention heatmap，说明它能支持哪些路由诊断、不能单独支持哪些因果解释；设计一个 ablation 或 counterfactual prompt 比较模型行为变化。

## Ch04 MHA / GQA / MLA

1. 证明标准 MHA 与一个同宽度单头 attention 在 Q/K/V/O 投影参数量上相同，但表达方式不同。
2. 给定 `n_heads=32`、`n_kv_heads=8`、`head_dim=128`，计算 MHA 与 GQA 每 token KV Cache 的元素数和压缩比。
3. 用低秩近似解释 MLA 为什么能减少缓存；同时说明“缓存低维 latent”不等价于“完全免费解压”。
4. 解释 head redundancy 为什么会出现；比较 head pruning、GQA 和 MLA 分别压缩了什么，以及它们可能损失哪些表示能力。

## Ch05 Transformer Block / Norm / FFN

1. 推导 LayerNorm 的 `mu`、`var`、`x_hat`，说明反向传播中为什么不能把 `mu` 和 `var` 当常数。
2. 比较 Pre-Norm 与 Post-Norm 的梯度路径，解释为什么深层 decoder-only 模型常用 Pre-Norm。
3. 比较 GELU FFN、SwiGLU 和 MoE FFN 的参数量、激活参数量和训练稳定性取舍。
4. 推导 SwiGLU 中 `d_ff = 8/3 * d_model` 与 4x GELU FFN 参数量近似相等，并解释门控乘法能表达哪些 token 条件化交互。
5. 给定 `B,T,d_model,n_heads,d_ff,dtype_bytes`，估算单个 Transformer block 的 attention 参数量、SwiGLU 参数量、主要 FLOPs、attention score 显存和主要激活显存，并说明哪些项会被 FlashAttention 或 activation checkpointing 改变。
6. 设计一个主语-动词一致性的机制可解释性实验：写出 clean/corrupted prompt、目标 logit difference、activation patching 位置、ablation 对象，并说明 probing、patching 和 ablation 各自能支持什么结论。

## Ch06 GPT Assembly / MoE

1. 按 embedding、position embedding、12 个 block、final LayerNorm 和 tied LM head 逐项计算 GPT-2 small 的参数量。
2. 解释 weight tying 为什么既减少参数又可能改善输入/输出词向量的一致性。
3. 给定 `256` 个专家、`top_k=8` 和 1 个 shared expert，解释 MoE 的 total parameters 与 activated parameters 为什么不同，并说明负载不均衡的风险。
4. 给定 token 序列 `[BOS, a, b, c, EOS]`，写出 GPT 训练时的 `inputs`、`labels` 和每个 `logits[:, t, :]` 对应的预测目标；说明 causal leakage 会如何让训练 loss 虚高地好看。

## Ch07 Training Loop

1. 从自回归分解推导 next-token negative log likelihood，并说明它与 cross entropy 的关系。
2. 推导单样本 cross entropy 对 logits 的梯度 `p_i - 1[i=y]`。
3. 设 tied LM head 为 `z_t = h_t E^T`，说明 CE 梯度如何更新正确 token、错误 token 的 output embedding 行，以及它如何继续传回 Transformer hidden state。
4. 解释 AdamW 中“解耦权重衰减”和 L2 regularization 的区别，并说明 warmup + cosine decay 的作用。
5. 给定 `micro_batch=4`、`seq_len=2048`、`grad_accum=8`、`data_parallel=16`、训练预算 `D=20B tokens` 和 dense LM 参数量 `N=1B`，计算 global batch tokens、训练 step 数和近似训练 FLOPs，并说明这会如何影响 learning rate schedule、checkpoint 间隔与 GPU hours。
6. 给定 train token 序列和 eval token 序列，计算 n-gram repetition rate 与 train/eval overlap rate，并说明它们如何影响 val loss 和泛化判断。
7. 解释 Chinchilla-style scaling law 的核心启示：为什么固定算力下需要同时考虑模型参数量、训练 token 数和数据质量，而不是只扩大参数量。
8. 给出训练日志中 loss spike、NaN、grad_norm 突增、tokens/s 下降各自可能的原因和排查顺序。
9. 给定 train loss 下降但 val loss 上升的曲线，判断它更可能是过拟合、数据切分问题还是训练目标错误；说明你会先检查哪些数据和日志字段。

## Ch08 Generation / Decoding

1. 比较 greedy、temperature、top-k、top-p 的质量/多样性/可复现性/延迟取舍。
2. 手算一个 5 token 词表的 top-p nucleus：给定概率 `[0.40, 0.25, 0.20, 0.10, 0.05]`，当 `p=0.7` 和 `p=0.9` 时各保留哪些 token。
3. 说明 beam search 为什么常需要长度惩罚，并比较它与 sampling 在开放式生成任务中的适用场景。
4. 给定一个 beam table，分别用 raw logprob 和 length-normalized score 排序，说明排序改变是否一定意味着质量更好。
5. 解释 speculative decoding 的接受率如何影响吞吐，为什么 draft model 过弱或过强都可能不划算。
6. 设计一个比较 greedy、top-p 和 temperature sampling 的小实验：写出 prompt 集、随机种子、输出长度、distinct-n、重复率、任务正确率或人工偏好指标，并说明每个指标的局限。
7. 对数学或代码题设计一个 reasoning 生成实验：比较 single-sample、self-consistency、best-of-N 和 verifier reranking，报告准确率、pass@k、平均输出 token 数、延迟和单位正确答案成本。

## Ch09 Fine-tuning / Alignment

1. 给定 prompt/response token 序列，标出 SFT labels 中应为 `-100` 的位置，并解释原因。
2. 从 Bradley-Terry 偏好模型写出 DPO loss 中 chosen/rejected log-ratio 的含义。
3. 给定一组 chosen/rejected reward，计算 Bradley-Terry pairwise reward loss 和 preference accuracy，并解释这个 loss 与奖励模型训练的关系。
4. 给定一组 chosen/rejected 回答长度，计算 mean length delta、chosen_longer_rate、rejected_longer_rate 和 tie_rate，并说明长度偏差如何影响 DPO 或 RLHF。
5. 给定一组 chosen/rejected 回答，指出可能的风格偏差或标注者分歧，并说明这些偏差如何影响 DPO 或 RLHF。
6. 说明 GRPO 组内白化如何减少不同 prompt reward scale 的影响，以及它不能解决哪些 reward hacking 问题。
7. 比较 LoRA rank、alpha、target modules 对训练参数量、表达能力和合并推理的影响。
8. 设计一个评估 DPO 模型是否优于 SFT/reference 的方案：至少包含 helpfulness、事实性、安全拒答、过度拒答和数学/代码能力保留，并解释为什么 preference win rate 不能单独作为结论。

## Ch10 Inference / RAG / Serving

1. 推导 KV Cache 显存公式，必须包含 batch size、layers、kv heads、head dim、context length 和 dtype bytes。
2. 区分 TTFT、TPOT、tokens/s、吞吐、并发和 P95 latency；说明它们分别对应哪个用户体验或成本问题。
3. 给定 retrieved document ids、relevant document ids 和 `k`，计算 Recall@k 与 reciprocal rank，并说明它们分别衡量 RAG 检索的哪一类问题。
4. 给定一个 RAG 失败案例，判断可能是 chunking、embedding、retrieval、reranking、prompt assembly 还是 generation 的问题。
5. 比较 INT8 weight-only quantization、KV Cache quantization 和 FP8/FP4 mixed precision 的目标、风险和验证指标。
6. 说明为什么前沿模型 benchmark 数字必须标注来源、日期、任务设置和评测版本。
7. 设计一个 RAG 消融实验：比较 dense-only、BM25-only、hybrid、hybrid+rerank 和两组 chunk size/overlap，说明应分别报告哪些检索指标、生成质量指标、延迟和 token 成本。
8. 设计一个多模态 LLM 评估：分别覆盖图像问答、OCR/文档理解、图表数值推理和视觉定位，说明输入分辨率、视觉 token 数、延迟、KV Cache 成本和每类任务的失败模式。
9. 为一个 LLM benchmark 写 metric card：包括 task、sample_size、baseline、metrics、risks、uncertainty 和 conclusion，并说明哪些结论不能从这组数据推出。

## 经典 NLP 专题题

1. RNN/LSTM：给定标量 RNN 参数，手算 hidden state、BPTT 梯度连乘，并说明 LSTM 的 forget/input/output gate 如何改变长期信息路径。
2. Dependency Parsing：给定句子和 gold arcs，用 arc-standard transition system 写出一条合法 shift/reduce 序列，并计算 UAS/LAS。
3. Seq2Seq/NMT：画出 encoder-decoder attention 的信息流，解释 exposure bias 和 beam search length bias。
4. BERT/Encoder-only：比较 MLM 与 causal LM 的 mask 方式、训练目标和下游 fine-tuning 输入格式。
5. Evaluation：比较 perplexity、BLEU、ROUGE、F1、exact match 和 LLM-as-judge 的适用范围与失效模式。
6. Ethics/Safety：列出一个 RAG 医疗问答系统的隐私、幻觉、偏见和评测污染风险，并给出缓解方案。
