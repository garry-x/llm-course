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
3. 给定一个小语料，手算前 3 次 BPE merge，并说明 tie-breaking 会怎样影响最终词表。

## Ch02 Embedding / Position Encoding / RoPE

1. 从 one-hot 矩阵乘法推导 embedding lookup，说明为什么 `E[token_id]` 等价于 `one_hot @ E`。
2. 比较 skip-gram negative sampling 与 GloVe：它们分别从局部上下文样本和全局共现矩阵中学习什么统计信号？为什么类比推理不是训练目标直接保证的性质？
3. 证明 sinusoidal position encoding 的相对位移可以由线性变换表示，即 `PE(pos+k)` 可以由 `PE(pos)` 的 sin/cos block 旋转得到。
4. 证明 RoPE 点积只依赖相对位置：`(R_m q)^T (R_n k) = q^T R_{n-m} k`，并解释为什么这对长上下文外推有帮助但不是充分条件。

## Ch03 Scaled Dot-Product Attention

1. 若 `q_i, k_i` 独立且均值 0、方差 1，推导 `q^T k` 的方差，并说明为什么 attention scores 要除以 `sqrt(d_k)`。
2. 写出 causal mask 在 `T=4` 时的矩阵，并说明 mask 值应该在 softmax 前还是 softmax 后应用。
3. 分析 self-attention 的时间复杂度和显存复杂度，区分训练时保存 activation 与推理时 KV Cache 的差异。

## Ch04 MHA / GQA / MLA

1. 证明标准 MHA 与一个同宽度单头 attention 在 Q/K/V/O 投影参数量上相同，但表达方式不同。
2. 给定 `n_heads=32`、`n_kv_heads=8`、`head_dim=128`，计算 MHA 与 GQA 每 token KV Cache 的元素数和压缩比。
3. 用低秩近似解释 MLA 为什么能减少缓存；同时说明“缓存低维 latent”不等价于“完全免费解压”。

## Ch05 Transformer Block / Norm / FFN

1. 推导 LayerNorm 的 `mu`、`var`、`x_hat`，说明反向传播中为什么不能把 `mu` 和 `var` 当常数。
2. 比较 Pre-Norm 与 Post-Norm 的梯度路径，解释为什么深层 decoder-only 模型常用 Pre-Norm。
3. 比较 GELU FFN、SwiGLU 和 MoE FFN 的参数量、激活参数量和训练稳定性取舍。

## Ch06 GPT Assembly / MoE

1. 按 embedding、position embedding、12 个 block、final LayerNorm 和 tied LM head 逐项计算 GPT-2 small 的参数量。
2. 解释 weight tying 为什么既减少参数又可能改善输入/输出词向量的一致性。
3. 给定 `256` 个专家、`top_k=8` 和 1 个 shared expert，解释 MoE 的 total parameters 与 activated parameters 为什么不同，并说明负载不均衡的风险。

## Ch07 Training Loop

1. 从自回归分解推导 next-token negative log likelihood，并说明它与 cross entropy 的关系。
2. 推导单样本 cross entropy 对 logits 的梯度 `p_i - 1[i=y]`。
3. 解释 AdamW 中“解耦权重衰减”和 L2 regularization 的区别，并说明 warmup + cosine decay 的作用。
4. 给定 `micro_batch=4`、`seq_len=2048`、`grad_accum=8`、`data_parallel=16` 和训练预算 `D=20B tokens`，计算 global batch tokens 与训练 step 数，并说明这会如何影响 learning rate schedule 与 checkpoint 间隔。
5. 解释 Chinchilla-style scaling law 的核心启示：为什么固定算力下需要同时考虑模型参数量、训练 token 数和数据质量，而不是只扩大参数量。
6. 给出训练日志中 loss spike、NaN、grad_norm 突增、tokens/s 下降各自可能的原因和排查顺序。

## Ch08 Generation / Decoding

1. 比较 greedy、temperature、top-k、top-p 的质量/多样性/可复现性/延迟取舍。
2. 手算一个 5 token 词表的 top-p nucleus：给定概率 `[0.40, 0.25, 0.20, 0.10, 0.05]`，当 `p=0.7` 和 `p=0.9` 时各保留哪些 token。
3. 说明 beam search 为什么常需要长度惩罚，并比较它与 sampling 在开放式生成任务中的适用场景。
4. 解释 speculative decoding 的接受率如何影响吞吐，为什么 draft model 过弱或过强都可能不划算。

## Ch09 Fine-tuning / Alignment

1. 给定 prompt/response token 序列，标出 SFT labels 中应为 `-100` 的位置，并解释原因。
2. 从 Bradley-Terry 偏好模型写出 DPO loss 中 chosen/rejected log-ratio 的含义。
3. 给定一组 chosen/rejected 回答，指出可能的长度偏差、风格偏差或标注者分歧，并说明这些偏差如何影响 DPO 或 RLHF。
4. 说明 GRPO 组内白化如何减少不同 prompt reward scale 的影响，以及它不能解决哪些 reward hacking 问题。
5. 比较 LoRA rank、alpha、target modules 对训练参数量、表达能力和合并推理的影响。

## Ch10 Inference / RAG / Serving

1. 推导 KV Cache 显存公式，必须包含 batch size、layers、kv heads、head dim、context length 和 dtype bytes。
2. 区分 TTFT、TPOT、tokens/s、吞吐、并发和 P95 latency；说明它们分别对应哪个用户体验或成本问题。
3. 给定一个 RAG 失败案例，判断可能是 chunking、embedding、retrieval、reranking、prompt assembly 还是 generation 的问题。
4. 比较 INT8 weight-only quantization、KV Cache quantization 和 FP8/FP4 mixed precision 的目标、风险和验证指标。
5. 说明为什么前沿模型 benchmark 数字必须标注来源、日期、任务设置和评测版本。

## 经典 NLP 专题题

1. Dependency Parsing：给定句子和 gold arcs，用 arc-standard transition system 写出一条合法 shift/reduce 序列，并计算 UAS/LAS。
2. Seq2Seq/NMT：画出 encoder-decoder attention 的信息流，解释 exposure bias 和 beam search length bias。
3. BERT/Encoder-only：比较 MLM 与 causal LM 的 mask 方式、训练目标和下游 fine-tuning 输入格式。
4. Evaluation：比较 perplexity、BLEU、ROUGE、F1、exact match 和 LLM-as-judge 的适用范围与失效模式。
5. Ethics/Safety：列出一个 RAG 医疗问答系统的隐私、幻觉、偏见和评测污染风险，并给出缓解方案。
