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

1. 设语料 token 序列长度为 `N`，词表大小从 `V0` 增加到 `V`。说明 BPE 每次合并如何改变序列长度；对字符串 `abababa` 手算前两次 merge 的 pair、count、new id、before/after length、tokens saved、final ids 和 compression ratio，并给出贪心合并不能保证全局最优压缩的反例思路。
2. 比较 word-level、character-level、byte-level BPE 在 OOV、多语言、序列长度和 embedding 参数量上的取舍。
3. 设计一个 tokenizer 评价实验：按英文、中文、代码、数学公式和 emoji/混合文本分组，比较每组平均 token 数、P95 token 数、tokens/character、round-trip 成功率和 embedding 参数量；计算最高/最低 tokens/character 的 disparity，并说明这些结果如何影响 context、训练 FLOPs、KV Cache 成本和多语言使用体验。
4. 给定一个小语料，手算前 3 次 BPE merge，并说明 tie-breaking 会怎样影响最终词表。

## Ch02 Embedding / Position Encoding / RoPE

1. 从 one-hot 矩阵乘法推导 embedding lookup，说明为什么 `E[token_id]` 等价于 `one_hot @ E`；再用一个形状为 `[B,T]` 的 token id 张量说明 `one_hot(token_ids)`、`E` 和输出张量的形状分别是什么。
2. 给定 token 序列 `[0,1,2,1]` 和 window size 1，手算 directed co-occurrence matrix；再给定 center/positive/negative 向量，写出 SGNS loss，并推导 mean reduction 下中心向量梯度 `dL/dv_c`；从共现矩阵计算 PMI 与 shifted PMI；给定非零共现计数、word/context 向量和 bias，计算一项 GloVe weighted least-squares residual。
3. 给定 5 个二维词向量，计算 cosine similarity matrix，并用 3CosAdd 解 `man:king :: woman:?`；说明为什么必须排除输入词。
4. 比较 skip-gram negative sampling 与 GloVe：它们分别从局部上下文样本和全局共现矩阵中学习什么统计信号？SGNS 与 shifted PMI 的关系说明了什么？为什么类比推理不是训练目标直接保证的性质？
5. 证明 sinusoidal position encoding 的相对位移可以由线性变换表示，即 `PE(pos+k)` 可以由 `PE(pos)` 的 sin/cos block 旋转得到。
6. 证明 RoPE 点积只依赖相对位置：`(R_m q)^T (R_n k) = q^T R_{n-m} k`，并解释为什么这对长上下文外推有帮助但不是充分条件。

## Ch03 Scaled Dot-Product Attention

1. 若 `q_i, k_i` 独立且均值 0、方差 1，推导 `q^T k` 的方差，并说明为什么 attention scores 要除以 `sqrt(d_k)`。
2. 证明或数值验证无位置编码、无遮挡 self-attention 满足 `Attn(PX)=P Attn(X)`；说明为什么 causal mask 或位置编码会打破完整置换等变性。
3. 写出 causal mask 在 `T=4` 时的矩阵；给定 padding mask `[[1,1,0,0],[1,1,1,0]]`，写出合成后的 `[B,T,T]` attention mask，并说明 mask 值应该在 softmax 前还是 softmax 后应用。
4. 推导 softmax Jacobian `J_ij = p_i(delta_ij - p_j)`，并说明 attention 输出梯度如何通过 `p @ V` 传回 logits；进一步对 `S = QK^T/sqrt(d_k)` 推导 `dQ = dS K / sqrt(d_k)`、`dK = dS^T Q / sqrt(d_k)` 和 `dV = P^T dO`，写清每个张量的 shape。
5. 给定 attention weights `[1,0,0]` 和 `[1/3,1/3,1/3]`，计算 attention entropy，并说明它如何反映 softmax 分布尖锐程度。
6. 分析 self-attention 的时间复杂度和显存复杂度；给定 `B,H,T,dtype_bytes`，计算 dense attention score 矩阵的显存，并区分训练时保存 activation 与推理时 KV Cache 的差异。
7. 给定一张 attention heatmap，说明它能支持哪些路由诊断、不能单独支持哪些因果解释；设计一个 ablation 或 counterfactual prompt 比较模型行为变化。

## Ch04 MHA / GQA / MLA

1. 证明标准 MHA 与一个同宽度单头 attention 在 Q/K/V/O 投影参数量上相同，但表达方式不同。
2. 给定 `n_heads=8`、`n_kv_heads=2`，写出每个 Q head 对应的 KV head 映射；若 K/V 张量形状为 `[B,2,T,D]`，说明重复后如何得到 `[B,8,T,D]`，并说明 `n_kv_heads=1` 和 `n_kv_heads=n_heads` 分别对应什么特例。
3. 给定 `n_layers=24`、`batch=4`、`seq_len=2048`、`n_heads=32`、`n_kv_heads=8`、`head_dim=128`、`d_latent=512` 和 fp16，计算 MHA、GQA 与 MLA 的每 token KV Cache 元素数、总显存和相对 MHA 的压缩比。
4. 用低秩近似解释 MLA 为什么能减少缓存；给定 `q_h`、latent `c_s` 和 K 解压矩阵 `W_UK,h`，推导 `q_h^T (W_UK,h c_s) = (q_h W_UK,h)^T c_s`，说明如何不显式解压 K 就在 latent 空间计算 attention score；同时说明“缓存低维 latent”不等价于“完全免费解压”。
5. 解释 head redundancy 为什么会出现；比较 head pruning、GQA 和 MLA 分别压缩了什么，以及它们可能损失哪些表示能力。

## Ch05 Transformer Block / Norm / FFN

1. 推导 LayerNorm 的 `mu`、`var`、`x_hat`，说明反向传播中为什么不能把 `mu` 和 `var` 当常数；再对 `RMSNorm(x)=gamma*x/sqrt(mean(x^2)+eps)` 推导 `dL/dx`，指出梯度中为什么会出现跨特征维度的 coupling term。
2. 比较 Pre-Norm 与 Post-Norm 的梯度路径；给定若干层的子层局部斜率和 norm 局部斜率，在线性化标量模型中计算逐层梯度因子，并解释为什么深层 decoder-only 模型常用 Pre-Norm。
3. 比较 GELU FFN、SwiGLU 和 MoE FFN 的参数量、激活参数量和训练稳定性取舍。
4. 推导 SwiGLU 中 `d_ff = 8/3 * d_model` 与 4x GELU FFN 参数量近似相等；令 `d_model=24`，计算 bias-free GELU FFN 与 SwiGLU 的隐藏宽度和参数量，并解释门控乘法能表达哪些 token 条件化交互。
5. 给定 `B,T,d_model,n_heads,d_ff,dtype_bytes`，估算单个 Transformer block 的 attention 参数量、SwiGLU 参数量、主要 FLOPs、attention score 显存和主要激活显存；再给定 checkpointed fraction，计算 activation checkpointing 省下的激活显存、额外重算 FLOPs 和训练 FLOPs 倍数，并说明哪些项会被 FlashAttention 改变。
6. 设计一个主语-动词一致性的机制可解释性实验：写出 clean/corrupted prompt、目标 logit difference、activation patching 位置、ablation 对象，并说明 probing、patching 和 ablation 各自能支持什么结论。

## Ch06 GPT Assembly / MoE

1. 按 embedding、position embedding、12 个 block、final LayerNorm 和 tied LM head 逐项计算 GPT-2 small 的参数量。
2. 解释 weight tying 为什么既减少参数又可能改善输入/输出词向量的一致性；给定 `logits = H E^T`、target ids 和 CE mean reduction，推导 `dH = G E` 与 `dE = G^T H`，并说明 `ignore_index` 如何改变有效分母。
3. 给定 bias-free SwiGLU expert 的 `d_model=16`、`expert_hidden=32`、`256` 个路由专家、`top_k=8` 和 1 个 shared expert，计算单个 expert 参数量、router 参数量、total expert parameters、每 token activated expert parameters 和 capacity-to-compute ratio；再给定某个 batch 的 expert token counts 和每 expert capacity，计算 overflow 与 drop rate，并解释负载不均衡为什么会导致吞吐下降或 token drop。
4. 给定 4 个 token 对 3 个 experts 的 router probabilities `[[0.7,0.2,0.1],[0.6,0.3,0.1],[0.1,0.8,0.1],[0.2,0.2,0.6]]`，top-1 expert ids `[0,0,1,2]`，计算每个 expert 的 load fraction、mean router probability 和 `3 * sum_i load_i * prob_i` load-balancing loss；说明为什么只看 router probability 或只看 top-k counts 都不够。
5. 给定 token 序列 `[BOS, a, b, c, EOS]`，写出 GPT 训练时的 `inputs`、`labels` 和每个 `logits[:, t, :]` 对应的预测目标；给定一组小 vocab logits，按 `logits[:, :-1, :]` 与 `input_ids[:, 1:]` 手算 next-token cross entropy，并说明 causal leakage 会如何让训练 loss 虚高地好看。

## Ch07 Training Loop

1. 从自回归分解推导 next-token negative log likelihood，并说明它与 cross entropy 的关系。
2. 推导单样本 cross entropy 对 logits 的梯度 `p_i - 1[i=y]`；若 batch 中有 `ignore_index` 位置，说明 mean reduction 的分母为什么应是有效 token 数，且被忽略位置的 logits 梯度应为 0。
3. 给定 vocab size、目标 token、`epsilon` 和 logits，构造 label-smoothed target distribution，计算 label-smoothed cross entropy，并说明它和 hard one-hot CE、蒸馏 soft targets 的关系。
4. 设 tied LM head 为 `z_t = h_t E^T`，说明 CE 梯度如何更新正确 token、错误 token 的 output embedding 行，以及它如何继续传回 Transformer hidden state。
5. 解释 AdamW 中“解耦权重衰减”和 L2 regularization 的区别，并说明 warmup + cosine decay 的作用；给定 `base_lr=0.2`、`num_warmup_steps=2`、`num_training_steps=6`、`min_lr_ratio=0.25`、每个 optimizer step 消耗 `1000` tokens，手算 step `0,1,2,6` 的 lr multiplier、实际 lr、phase 和累计 consumed tokens。
6. 给定 `micro_batch=4`、`seq_len=2048`、`grad_accum=8`、`data_parallel=16`、训练预算 `D=20B tokens` 和 dense LM 参数量 `N=1B`，计算 global batch tokens、训练 step 数和近似训练 FLOPs；再按 bf16 参数/梯度、fp32 AdamW 两个 moment states 计算训练显存，并说明 optimizer-state sharding 会改变哪些项。
7. 给定 train token 序列和 eval token 序列，计算 n-gram repetition rate 与 train/eval overlap rate，并说明它们如何影响 val loss 和泛化判断。
8. 给定两个数据源：web `600k` tokens、`600` documents、duplicate `0.03`、eval overlap `0.001`、quality pass `0.92`；code `400k` tokens、`400` documents、duplicate `0.02`、eval overlap `0`、quality pass `0.90`。在阈值 `min_total_tokens=900k`、`max_duplicate_rate=0.05`、`max_eval_overlap_rate=0.005`、`min_quality_pass_rate=0.88`、`min_domain_count=2`、`max_domain_token_share=0.7` 下，计算 weighted duplicate rate、weighted quality pass rate、domain shares，并判断 `training_data_curation_report` 是否通过。再说明如果 PII rate 或 eval overlap 失败，为什么不能直接用低 val loss 支持扩容。
9. 解释 Chinchilla-style scaling law 的核心启示：为什么固定算力下需要同时考虑模型参数量、训练 token 数和数据质量，而不是只扩大参数量。
10. 给定一组 logits、targets 和 confidence bins，计算每个桶的 accuracy、mean confidence 与 ECE，并说明模型过度自信会如何影响拒答阈值或风险控制。
11. 给定两个参数张量的梯度，计算 global grad norm、clip coefficient 和裁剪后的梯度；说明它与逐参数裁剪的区别。
12. 给定 `grad_accum_steps=4`、四个 micro-batch mean losses、每个 micro-batch 的 token 数和 warmup scheduler，计算每次 backward 使用的 scaled loss、一次 optimizer step 消耗的 token 数、scheduler 应推进几次，以及如果忘记除以 `grad_accum_steps` 会等价于怎样改变学习率。
13. 给出训练日志中 loss spike、NaN、grad_norm 突增、tokens/s 下降各自可能的原因和排查顺序。
14. 给定 train loss 下降但 val loss 上升的曲线，判断它更可能是过拟合、数据切分问题还是训练目标错误；说明你会先检查哪些数据和日志字段。
15. 给定 7B 参数模型、8 张 GPU、bf16 参数/梯度、fp32 AdamW `m/v` states，分别计算 DDP、ZeRO-1、ZeRO-2、ZeRO-3/FSDP 的每卡模型状态显存；再按 `distributed_training_strategy_report` 的格式写出 strategy、global batch tokens、memory gate 和 action item，并说明这些估算没有包含 activation、通信 buffer、临时张量和 allocator fragmentation，因此不能单独证明训练可行。
16. 给定模型参数量 `N=7B`、吞吐 `tokens/s=20000`、GPU 数 `8`、单卡峰值 `300 TFLOP/s`，按 `6N` FLOPs/token 粗估 MFU；若 MFU 只有 18%，列出至少 4 个可能原因，并说明如何用 profiler 或日志区分 batch 太小、通信等待、数据加载不足、checkpoint 写盘和 kernel 未融合。若策略使用 FP8/MXFP8，还要写出 scale/amax history、loss spike、梯度范围和 checkpoint state 的验证证据。

## Ch08 Generation / Decoding

1. 比较 greedy、temperature、top-k、top-p 和 repetition penalty 的质量/多样性/可复现性/延迟取舍。
2. 手算一个 5 token 词表的 top-p nucleus：给定概率 `[0.40, 0.25, 0.20, 0.10, 0.05]`，当 `p=0.7` 和 `p=0.9` 时各保留哪些 token。
3. 给定 logits `[4.0, 3.0, -1.0]`、已生成 token ids `[0,2]` 和 repetition penalty `2.0`，手算采样前 logits 如何变化；再用 `top_p=0.8` 计算保留的候选 token、重新归一化后的概率、entropy 和 greedy token，并说明为什么正负 logit 的处理方向不同。
4. 说明 beam search 为什么常需要长度惩罚，并比较它与 sampling 在开放式生成任务中的适用场景。
5. 给定一个 beam table，分别用 raw logprob 和 length-normalized score 排序，说明排序改变是否一定意味着质量更好。
6. 给定 speculative decoding 的三轮记录：`gamma=4`，每轮接受草稿 token 数 `[4,2,3]`，实际写入输出 token 数 `[5,3,4]`，draft 单步成本是 target 单步成本的 `0.2`。计算 proposed、accepted、acceptance rate、baseline target steps、target verify calls、draft steps、粗略耗时和 speedup，并解释为什么 draft model 过弱或过强都可能不划算。
7. 给定两行 logits `[[5,4,3],[1,2,9]]` 和合法 token 集 `[[1,2],[0,1]]`，写出约束 mask 后哪些位置为 `-inf`，并给出 greedy 解码结果；说明为什么约束解码需要重新归一化。
8. 设计一个比较 greedy、top-p 和 temperature sampling 的小实验：写出 prompt 集、随机种子、输出长度、distinct-n、重复率、任务正确率或人工偏好指标，并说明每个指标的局限。
9. 对数学或代码题设计一个 reasoning 生成实验：比较 single-sample、self-consistency、best-of-N 和 verifier reranking；给定 5 条候选输出，写出 final-answer extractor、majority vote 的票数分布和 tie-breaking 规则；给定 `n` 个样本中 `c` 个正确，计算 `pass@k = 1 - C(n-c,k)/C(n,k)`，并报告平均输出 token 数、延迟和单位正确答案成本。

## Ch09 Fine-tuning / Alignment

1. 给定 prompt/response token 序列，标出 SFT labels 中应为 `-100` 的位置，并解释原因。
2. 从 Bradley-Terry 偏好模型写出 DPO loss 中 chosen/rejected log-ratio 的含义。
3. 给定 policy chosen/rejected log-probs `[3,1]`、`[1,2]`，reference chosen/rejected log-probs `[1,1]`、`[1,1]`，`beta=0.5`，计算 DPO 隐式 chosen/rejected reward、reward margin、preference probability 和 preference accuracy。
4. 给定一组 chosen/rejected reward，计算 Bradley-Terry pairwise reward loss 和 preference accuracy，并解释这个 loss 与奖励模型训练的关系。
5. 给定一组 chosen/rejected 回答长度，计算 mean length delta、chosen_longer_rate、rejected_longer_rate 和 tie_rate，并说明长度偏差如何影响 DPO 或 RLHF。
6. 给定一组 chosen/rejected 回答，指出可能的风格偏差或标注者分歧，并说明这些偏差如何影响 DPO 或 RLHF。
7. 给定 policy/ref 在 sampled tokens 上的 log probability，计算近似 KL `exp(log_ref-log_policy) - (log_ref-log_policy) - 1`，并说明 padding mask 为什么不能进入均值分母。
8. 给定 old/new policy log-probs、advantages 和 `clip_range=0.2`，计算 PPO unclipped surrogate、clipped surrogate、最终 policy loss、clip fraction 和 approximate KL；说明 PPO clipping 与 KL penalty 分别约束什么。
9. 给定 GRPO rewards `[[1],[2],[3]]`、old log-probs 全 0、new/old ratios `[[[1.0,1.5]],[[1.0,1.0]],[[0.5,1.0]]]`、completion mask `[[[1,1]],[[1,0]],[[1,1]]]`、reference log-probs 全 0、`clip_range=0.2`、`kl_beta=0.04`，计算组内白化 advantages、PPO clipped surrogate、masked policy loss、masked approximate KL 和总 loss；说明 GRPO 组内白化不能解决哪些 reward hacking 问题。
10. 比较 LoRA rank、alpha、target modules 对训练参数量、表达能力和合并推理的影响。
11. 设计一个评估 DPO 模型是否优于 SFT/reference 的方案：至少包含 helpfulness、事实性、安全拒答、过度拒答和数学/代码能力保留，并解释为什么 preference win rate 不能单独作为结论。

## Ch10 Inference / RAG / Serving

1. 推导 KV Cache 显存公式，必须包含 batch size、layers、kv heads、head dim、context length 和 dtype bytes。
2. 区分 TTFT、TPOT、tokens/s、吞吐、并发和 P95 latency；说明它们分别对应哪个用户体验或成本问题。
3. 给定 tokenized prompts `[[1,2,3,4],[1,2,3,9,10],[1,2,8],[7,8]]`，按请求顺序计算每条请求可复用的最长历史前缀、new prefill tokens、总 saved prefill tokens、effective prefill tokens 和 prefix cache hit rate；说明为什么随机时间戳会破坏 prefix cache。
4. 给定 query/document embedding batch，写出 in-batch negatives 的 InfoNCE logits、label 和 loss；给定 chosen/rejected reranker scores，计算 pairwise reranker loss；给定 dense 检索排序、BM25 排序、retrieved document ids、relevant document ids、graded relevance scores、MMR 相似度表和 `k`，计算 RRF 融合排序、Recall@k、reciprocal rank、nDCG@k 与 MMR 选择结果，并说明它们分别衡量 RAG 检索的哪一类问题。
5. 给定一个 RAG 失败案例：retrieved ids `[doc9,doc2,doc5,doc1]`、relevant ids `{doc1,doc2,doc7}`、cited ids `[doc2,doc9]`、`k=3`、答案错误。计算 retrieval recall@k、MRR@k、citation precision、citation recall、missing relevant ids，并判断 failure mode 是 retrieval miss、context/citation miss 还是 generation error；若同时给出候选 chunk、citation id、token 数、context budget 和 reserved output budget，写出最终进入 prompt 的 citation 列表、used tokens 和 skipped chunks。
6. 比较 INT8 weight-only quantization、KV Cache quantization 和 FP8/FP4 mixed precision 的目标、风险和验证指标。
7. 说明为什么前沿模型 benchmark 数字必须同时给出任务、数据集、推理设置和评测版本。
8. 设计一个 RAG 消融实验：比较 dense-only、BM25-only、hybrid、hybrid+rerank、hybrid+MMR 和两组 chunk size/overlap，说明应分别报告哪些检索指标、生成质量指标、延迟和 token 成本。
9. 设计一个多模态 LLM 评估：分别覆盖图像问答、OCR/文档理解、图表数值推理和视觉定位，说明输入分辨率、视觉 token 数、延迟、KV Cache 成本和每类任务的失败模式。
10. 为一个 LLM benchmark 写结构化结论摘要：包括 task、sample_size、baseline、metrics、risks、uncertainty 和 conclusion，并说明哪些结论不能从这组数据推出。
11. 给定服务 workload：`QPS=10`、平均 prompt tokens `800`、平均 output tokens `200`、单卡 prefill capacity `120k prompt tokens/s`、decode capacity `2.5k output tokens/s`，计算 prefill/decode token rate，并判断主要瓶颈；说明为什么 QPS 继续上升时 TPOT、排队时长和 TTFT 可能以不同顺序恶化。
12. 给定 32 层 GQA 模型、`n_kv_heads=8`、`head_dim=128`、fp16 KV Cache、平均活跃上下文 `6000` tokens、可用于 KV 的显存 `48 GiB`，计算每 token KV bytes、每请求 KV Cache 和理论最大活跃请求数；再考虑 20% 安全余量，给出 admission limit，并解释为什么只按并发请求数限流会误伤短请求或放过长请求。
13. 给定 speculative decoding 服务 trace：baseline `2000 ms`、speculative `940 ms`、输出 `200` tokens、draft `200` tokens、accepted `152` tokens、target verify steps `50`、draft cost `200 ms`、quality regression `0`、额外显存 `1.5 GiB`、QPS `5`。在 gate `acceptance>=0.7`、`speedup>=1.8`、`draft_overhead<=0.25`、额外显存 `<=2 GiB` 下，计算 acceptance rate、speedup、draft overhead、tokens per verify step，并判断是否启用；再说明为什么 high QPS、compute-bound workload 或质量回归会改变结论。

## 经典 NLP 专题题

1. RNN/LSTM：给定标量 RNN 参数，手算 hidden state、BPTT 梯度连乘，并说明 LSTM 的 forget/input/output gate 如何改变长期信息路径。
2. Dependency Parsing：给定句子和 gold arcs，用 arc-standard transition system 写出一条合法 shift/reduce 序列，并计算 UAS/LAS。
3. Seq2Seq/NMT：画出 encoder-decoder attention 的信息流；给定一组 decoder state、encoder states 和 additive attention 参数，手算 scores、softmax alignment 与 context vector；解释 exposure bias 和 beam search length bias。
4. BERT/Encoder-only：比较 MLM 与 causal LM 的 mask 方式、训练目标和下游 fine-tuning 输入格式；给定 masked positions、vocab logits 和 labels，计算只在 mask 位置上的 MLM cross entropy 与 accuracy；给定 BIO tags 解码 NER/entity spans；给定 gold/pred spans，计算 span-level precision、recall、F1、TP、FP 和 FN；给定 emission/transition scores 手算 Viterbi 最优 tag path、CRF forward log-partition、gold path score 与 CRF NLL；给定 `[CLS] question [SEP] passage [SEP]` 的 start/end logits，选择抽取式 QA 的最佳 span，并说明 `[CLS]` no-answer 的含义。
5. Evaluation：比较 perplexity、BLEU、ROUGE、F1、exact match 和 LLM-as-judge 的适用范围与失效模式。
6. Ethics/Safety：列出一个 RAG 医疗问答系统的隐私、幻觉、偏见和评测污染风险，并给出缓解方案。
7. 现代 LLM 评测协议：给定 pairwise judge 结果 `W=42, L=35, T=23`，计算 tie-adjusted win rate；说明位置偏置、长度偏置、judge 模型同源偏置和小样本方差如何影响结论。再把“模型 A 比模型 B 好 8%”改写成包含样本量、任务、prompt、temperature、失败类别、延迟/成本和不可外推范围的严谨结论。
8. Safety evaluation：给定 harmful set、benign sensitive set 和普通任务集上的拒答/通过/错误计数，分别计算 attack success rate、refusal rate、over-refusal rate 和 task utility；解释为什么高拒答率不等于高安全性，以及如何同时报告 helpfulness、harmlessness 和能力保留。

## 跨章节综合题

这些题用于期末复习或课程综合讨论。答案必须同时写出公式、shape、计算步骤和结论边界。

1. End-to-end decoder-only trace：给定 `input_ids` shape `[B=2,T=5]`、`vocab_size=8`、`d_model=4`、`n_heads=2`，写出 embedding、Q/K/V、attention scores、hidden states、logits 和 shifted labels 的 shape；若 labels 中有 3 个 `-100`，说明 CE mean reduction 的有效分母是多少。
2. Token cost to serving cost：给定两个 tokenizer 对同一组英文、中文、代码 prompt 的 token counts、一个 24 层 GQA 模型配置和 fp16 KV cache，计算每组平均 prompt tokens、KV cache bytes、prefill token work 和多语言 token cost disparity；说明 tokenizer 选择如何同时影响 embedding 参数、context budget、TTFT 和服务成本。
3. Training-to-alignment objective chain：从 causal LM CE 写到 SFT mask，再到 DPO chosen/rejected reference log-ratio。给定一组 policy/ref sequence log-probs，计算 SFT 有效 token loss、DPO implicit rewards、preference probability 和近似 KL；说明这些数值分别支持什么结论、不支持什么结论。
4. Retrieval-to-generation failure analysis：给定 dense/BM25 排序、reranker scores、MMR 相似度表、context token budget、生成答案和 gold answer，计算 RRF、rerank top-k、MMR selection、最终 citations、Recall@k、MRR、answer EM/F1 和 used tokens；判断失败更可能来自 retrieval、reranking、context packing 还是 generation。
5. Decoding and evaluation tradeoff：给定同一 prompt 的 greedy、top-p、self-consistency 和 constrained decoding 输出，计算 distinct-n、pass@k、vote distribution、token cost 和格式合法率；说明在开放式写作、代码生成、JSON 工具调用和数学题中应如何选择不同策略。
6. Model family selection：对同一信息抽取任务，比较 decoder-only generation、encoder-only token classification、BERT span QA、RAG + constrained decoding 四种方案。写出每种方案的输入输出形式、训练或推理目标、可用指标、主要失败模式和服务成本。
