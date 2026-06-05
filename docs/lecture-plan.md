# 10 周 / 20 讲 Lecture Plan

本计划把 syllabus 的周安排展开为每周两讲。每讲包含目标、核心推导、课堂 demo、quick check 和课后产出，供教师备课、助教带讨论课和学生复盘使用。讲后产出可以转成下一讲 recap、worksheet、FAQ、handout 或 source patch。

默认节奏：每讲 80-90 分钟。若采用 12 周版本，可把 Week 8 的经典 NLP 与 Week 10 的项目展示拆成更多讲次。

## 授课结构

| 环节 | 建议时间 | 目标 |
|------|:--:|------|
| Recap / diagnostic quiz | 5-10 分钟 | 检查上节课核心 shape、公式或代码 |
| Concept lecture | 25-35 分钟 | 建立数学和系统图景 |
| Derivation / board work | 15-25 分钟 | 推导关键公式或复杂度 |
| Code demo / live debugging | 15-25 分钟 | 把公式落到 PyTorch 实现 |
| Exit ticket | 5 分钟 | 记录一个仍不清楚的问题和一个可验证结论 |

## Week 1 Lecture 1: 课程导论、Python/PyTorch 复习与 BPE

对应材料：Ch01、math prerequisites、reading-list Week 1。

目标：

- 解释课程交付物：章节作业、书面题、阅读复盘、两个 capstone。
- 复习 tensor shape、indexing、broadcast 和 `nn.Module`。
- 从 OOV 问题引出 byte-level BPE。
- 用 tokenizer report 比较平均 token 数、P95 token 数和 round-trip 成功率。

核心推导：

- BPE 每次 merge 对序列长度和 vocab size 的影响。
- 贪心 merge 与全局最优压缩之间的差距。
- tokenizer 成本指标：tokens/character、P95 token count、embedding params。

课堂 demo：

- 在小语料上手算 3 次 merge。
- 对中英/代码/emoji 样本运行 tokenizer report。
- 运行 `assignments/ch01_bpe/tests.py`，定位 `_get_stats` 与 `_merge` 的失败原因。

Quick check：

- 给定 `[1, 1, 1]` 和 pair `(1, 1)`，非重叠 merge 后长度是多少？
- byte-level BPE 为什么通常没有 OOV？

课后产出：

- A1 Ch01 starter 初版。
- 阅读复盘：BPE 论文中的 rare word 处理假设。

## Week 1 Lecture 2: Embedding、Word Vectors 与 RoPE

对应材料：Ch02、reading-list Week 1。

目标：

- 从 one-hot 矩阵乘法推导 embedding lookup。
- 解释 word2vec/GloVe 空间结构、窗口共现和类比推理的经验性质。
- 计算 cosine similarity matrix 与 3CosAdd 类比。
- 推导 sinusoidal 和 RoPE 的相对位置性质。

核心推导：

- `one_hot @ E = E[token_id]`。
- directed co-occurrence matrix、SGNS loss 与 GloVe weighted least-squares residual。
- 3CosAdd 查询向量：`v_b - v_a + v_c`，并排除输入词。
- `R_m^T R_n = R_{n-m}`。

课堂 demo：

- 比较 learned embedding 与 one-hot matmul 的 shape 和内存。
- 手算 `[0,1,2,1]` 在 window size 1 下的共现矩阵，再计算一个 SGNS loss。
- 手造 `man/king/woman/queen` 向量，跑 3CosAdd。
- 检查 RoPE 是否保持向量范数。

Quick check：

- RoPE 为什么要求 head dim 成对旋转？
- 类比推理是否由训练目标直接保证？

课后产出：

- Ch02 embedding/RoPE 测试通过。
- 书面题：RoPE 点积相对位置推导。

## Week 2 Lecture 3: Scaled Dot-Product Attention

对应材料：Ch03、reading-list Week 2。

目标：

- 建立 Q/K/V 的 shape 约定。
- 解释 scaling、softmax 和 weighted sum 的作用。
- 区分 score、probability、context 的张量形状。

核心推导：

- 若 `q_i,k_i` 方差为 1，则 `Var(q^T k)=d_k`。
- softmax Jacobian `J_ij=p_i(delta_ij-p_j)`。
- attention entropy `-sum p log p` 衡量分布尖锐程度。
- self-attention 时间复杂度 `O(BHT^2D)`。
- dense attention score memory `B * H * T^2 * dtype_bytes`。

课堂 demo：

- 手写一个小矩阵 attention，并与 PyTorch 输出对齐。
- 改变 `d_k`，观察未 scaling logits 的 softmax 饱和。
- 计算 one-hot 与 uniform attention 的 entropy。
- 对单个 query 比较手算 `attention_logits_gradient` 与 autograd。

Quick check：

- score shape 为什么是 `[B, H, T_q, T_k]`？
- scaling 放在 softmax 前还是后？
- attention entropy 低是否一定说明模型解释更可靠？
- softmax 的 Jacobian 为什么不是对角矩阵？

课后产出：

- Ch03 scaled attention 与 backward helper 测试通过。
- 书面题：attention scaling 与 softmax Jacobian 推导。

## Week 2 Lecture 4: Causal Mask、反向传播与 Dependency Parsing 预告

对应材料：Ch03、math prerequisites、classic NLP handout dependency parsing 部分。

目标：

- 解释 causal mask 的语义和广播规则。
- 复习 softmax/cross entropy 的反向传播。
- 用 dependency parsing 预告“结构化预测”与 decoder-only LM 的差异。

核心推导：

- mask 应在 softmax 前加 `-inf` 或大负数。
- cross entropy 对 logits 的梯度 `softmax(z)-one_hot(y)`。

课堂 demo：

- 构造错误的 softmax 后 mask，展示概率和不再为 1。
- 用一个 transition parsing 状态说明合法 action 约束。

Quick check：

- 为什么 softmax 后乘 mask 通常是错误实现？
- UAS 和 LAS 差别是什么？

课后产出：

- A2 causal mask 失败案例分析。
- 阅读复盘：Attention Is All You Need 的 mask 设计。

## Week 3 Lecture 5: Multi-Head Attention 与 GQA

对应材料：Ch04、reading-list Week 3。

目标：

- 比较单头、MHA、MQA/GQA 的参数量和 KV cache。
- 解释为什么减少 KV heads 能降低推理显存。
- 明确 Q heads 与 KV heads 的分组关系。

核心推导：

- 标准 MHA 投影参数量与同宽度单头相同。
- GQA head mapping：`query_head // (n_heads / n_kv_heads)`。
- KV cache 元素数 `2 * n_kv_heads * head_dim`。

课堂 demo：

- 用小模型打印 Q/K/V reshape 后的 shape。
- 计算 MHA 与 GQA 在 32/8 heads 下的 cache ratio。
- 写出 8 个 Q heads、2 个 KV heads 的映射列表。

Quick check：

- GQA 是否减少 Q heads？
- MQA 和 MHA 在 GQA mapping 中分别是什么边界情况？
- 参数量节省和 KV cache 节省是不是同一件事？

课后产出：

- Ch04 MHA/GQA 测试通过。
- 书面题：GQA cache 压缩比。

## Week 3 Lecture 6: MLA、Norm、FFN 与 Transformer Block

对应材料：Ch04-Ch05、reading-list Week 3。

目标：

- 解释 MLA latent cache 的工程动机和限制。
- 比较 LayerNorm、RMSNorm、Pre-Norm 与 Post-Norm。
- 组装 attention、FFN、residual 和 norm 成 Transformer block。

核心推导：

- LayerNorm 的 mean/variance 依赖输入，反向传播存在跨 feature 耦合。
- Pre-Norm residual 为深层模型提供更直接的梯度路径。
- 4x GELU FFN 的 bias-free 参数量为 `8*d_model^2`；SwiGLU 三矩阵参数量为 `3*d_model*d_ff`，同预算得到 `d_ff = 8/3*d_model`。
- 单个 block 的参数、FLOPs 和激活显存主项。

课堂 demo：

- 对接近零方差输入测试 LayerNorm/RMSNorm 的 `eps`。
- 用 `d_model=24` 手算并运行 GELU FFN 与 SwiGLU 的参数预算。
- 单步 forward 一个 Transformer block，检查梯度是否流到所有子模块。
- 用 `estimate_block_resources` 比较 `T=512` 与 `T=4096` 时 attention score 显存的变化。

Quick check：

- RMSNorm 是否会减去均值？
- 参数量、activation memory 和 optimizer state 是同一件事吗？
- MLA cache 低维是否意味着 attention 计算免费？

课后产出：

- A3 block 测试通过。
- 阅读复盘：MLA 或 RMSNorm 的一个 trade-off。

## Week 4 Lecture 7: GPT Model Assembly

对应材料：Ch06、reading-list Week 4。

目标：

- 串联 token embedding、position embedding、blocks、final norm 和 LM head。
- 解释 decoder-only next-token objective。
- 分析 GPT-2 small 参数量。

核心推导：

- 自回归分解 `p(x)=prod_t p(x_t|x_<t)`。
- tied LM head 下 embedding 权重只计一次。

课堂 demo：

- 实例化 tiny GPT，打印每个模块参数量。
- 改变未来 token，验证当前位置 logits 不应变化。

Quick check：

- labels 为什么右移一位？
- tied embedding 为什么影响参数量统计？

课后产出：

- Ch06 GPTModel forward 和参数量测试通过。
- 书面题：GPT-2 small 参数分析。

## Week 4 Lecture 8: MoE、Routing 与 Load Balancing

对应材料：Ch06、DeepSeekMoE/Switch Transformer 阅读。

目标：

- 区分 dense FFN、MoE total parameters 和 activated parameters。
- 解释 top-k routing、capacity、load balancing 和 routing bias。
- 讨论 MoE 的训练/推理工程代价。

核心推导：

- 每 token 激活参数只包含被选专家和共享专家。
- load imbalance 会导致 token drop、专家过载或吞吐下降。

课堂 demo：

- 用 `MoERouter` 观察 top-k 权重归一化。
- 人为增加负载偏置，观察 routing 倾向变化。

Quick check：

- 稀疏激活是否自动保证负载均衡？
- total parameters 和 activated parameters 分别对应什么成本？

课后产出：

- A4 MoE router 测试通过。
- 阅读复盘：Switch/DeepSeekMoE 的负载均衡策略。

## Week 5 Lecture 9: Dataset、Loss、AdamW 与 Scheduler

对应材料：Ch07、reading-list Week 5。

目标：

- 把连续文本切成 input/target block。
- 计算 n-gram 重复率和 train/eval overlap rate。
- 推导 next-token cross entropy。
- 区分 AdamW 与 L2 regularization。

核心推导：

- CE gradient `p_i - 1[i=y]`。
- `ignore_index` 位置不进入 mean CE 的分母，logits 梯度整行为 0。
- ECE：按 confidence 分桶比较 accuracy 与 mean confidence。
- n-gram repetition / overlap 的分母和结论边界。
- AdamW 的 decoupled weight decay 更新项。

课堂 demo：

- 打印 dataset 样本，确认 input 和 target 右移。
- 对一段 toy token 序列计算重复率和 train/eval 重叠率。
- 给定 logits 和 labels，计算 confidence、accuracy bucket 与 ECE。
- 手算 AdamW 单步更新并与测试对齐。

Quick check：

- perplexity 是正确率吗？
- softmax probability 可以直接当作答案可信度吗？
- warmup 解决什么早期训练问题？

课后产出：

- Ch07 dataset/CE/AdamW/scheduler 测试通过。
- 训练 capstone 提案。

## Week 5 Lecture 10: Training Stability、Checkpoint 与 Scaling

对应材料：Ch07、training capstone。

目标：

- 解释 grad clipping、AMP、checkpoint/resume、tokens/s。
- 读训练日志，定位 loss spike、NaN 和吞吐下降。
- 用简单 scaling law 讨论数据/参数/算力预算。

核心推导：

- global batch tokens、steps、tokens/s、GPU hours 的关系。
- dense LM 近似训练 FLOPs：`6 * params * train_tokens`。
- checkpoint storage 与保存频率的成本。

课堂 demo：

- 跑 training capstone 的 tiny train + resume。
- 手算 20B token 预算下的 step count 与 dense LM FLOPs。
- 修改 learning rate 观察 loss 异常。

Quick check：

- resume 时只恢复 model 权重够不够？
- token budget 翻倍时，step count、FLOPs 和 GPU hours 分别怎样变化？
- tokens/s 下降可能来自哪些非模型原因？

课后产出：

- 训练日志、checkpoint、resume 证明。
- 阅读复盘：Chinchilla 或 ZeRO 的一个工程假设。

## Week 6 Lecture 11: Decoding、Sampling 与 Search

对应材料：Ch08、reading-list Week 6。

目标：

- 比较 greedy、beam、temperature、top-k、top-p。
- 解释开放式生成中的 degeneration。
- 明确 sampling 的概率过滤和重新归一化。

核心推导：

- top-p nucleus 保留累计概率达到阈值的最小集合。
- beam score 与 length penalty 的关系。

课堂 demo：

- 对固定 logits 手算 top-k/top-p。
- 构造 beam table，比较 raw logprob 与 length-normalized 排序。
- 调整 temperature，观察分布 entropy。

Quick check：

- top-p 是否可能保留 0 个 token？
- beam search 是否总比 sampling 好？
- length penalty 解决的是短输出偏置还是事实性？

课后产出：

- Ch08 sampling 与 beam search 测试通过。
- 书面题：top-p 和 beam table 手算。

## Week 6 Lecture 12: Speculative Decoding 与 Constrained Generation

对应材料：Ch08、reading-list Week 6。

目标：

- 解释 draft/target 模型的接受机制。
- 分析接受率、draft 成本和 target batch verify 的权衡。
- 区分普通 sampling 与 reasoning/test-time compute。
- 引入结构化输出、JSON schema 和约束生成。

核心推导：

- speculative decoding 加速受 `draft_cost`、`accept_rate`、verify batch size 共同影响。
- self-consistency、best-of-N 和 verifier reranking 的准确率/成本权衡。
- pass@k：从 `n` 个样本中有 `c` 个正确时，估计抽取 `k` 个至少命中一次的概率。
- 约束生成把无效 token mask 到候选集之外。

课堂 demo：

- 运行 speculative decoding toy model，记录接受率。
- 对同一数学题采样多条推理路径，比较 single-sample、majority vote 和 best-of-N。
- 给定 `n,c,k` 手算 pass@k，并讨论它和单样本准确率的差异。
- 构造 JSON 输出失败和修复策略。

Quick check：

- draft model 越强是否一定越划算？
- reasoning 输出更长是否一定代表推理更正确？
- 约束生成会改变模型概率分布吗？

课后产出：

- A6 speculative decoding 输出统计。
- 阅读复盘：speculative decoding 或 self-consistency 的失败条件。

## Week 7 Lecture 13: SFT、LoRA 与 Parameter-Efficient Tuning

对应材料：Ch09、reading-list Week 7。

目标：

- 解释 instruction tuning 数据格式和 label mask。
- 推导 LoRA 的低秩权重增量。
- 区分 trainable parameters、merged weights 和推理成本。

核心推导：

- prompt/padding labels 为 `-100`，只让 assistant response 贡献 loss。
- LoRA 增量 `Delta W = B A * alpha / r`。

课堂 demo：

- 打印 SFT dataset labels，确认 prompt 被 mask。
- 对 Linear 层应用 LoRA，检查初始输出等于 base。

Quick check：

- 为什么不能对 `-100` 直接 gather？
- merge LoRA 后推理还需要 adapter 分支吗？

课后产出：

- Ch09 SFT/LoRA 测试通过。
- 训练 capstone 初版。

## Week 7 Lecture 14: Preference Optimization、DPO 与 GRPO

对应材料：Ch09、reading-list Week 7。

目标：

- 从偏好数据解释 chosen/rejected。
- 从 Bradley-Terry 模型写出奖励模型 pairwise loss。
- 推导 DPO log-ratio 的方向。
- 用长度统计判断偏好数据是否鼓励冗长输出。
- 解释 GRPO 组内 advantage 白化和局限。

核心推导：

- RM 训练最大化 `sigmoid(r_chosen - r_rejected)`，对应 `-logsigmoid` 损失。
- DPO 比较 policy 相对 reference 的 chosen/rejected log probability 改变量。
- GRPO 在同 prompt group 内标准化 reward。

课堂 demo：

- 手算 chosen/rejected reward 的 pairwise loss 和 preference accuracy。
- 手造 chosen/rejected logits，观察 DPO loss 方向。
- 对 chosen/rejected response length 计算 length bias 统计。
- 对不同 reward scale 的 group 做 whitening。

Quick check：

- RM accuracy 高是否足以说明偏好数据质量好？
- DPO 为什么需要 reference model？
- GRPO 是否解决 reward hacking？

课后产出：

- A7 RM/DPO/GRPO 测试通过。
- 阅读复盘：R1/GRPO 的方法边界。

## Week 8 Lecture 15: RNN/LSTM、Dependency Parsing、Seq2Seq 与 BERT

对应材料：classic NLP handout、Classic NLP Deep-Dive Teaching Module、reading-list Week 8。

目标：

- 补齐 CS224N 式经典神经 NLP 主线：RNN/LSTM、dependency parsing、seq2seq/NMT、BERT。
- 比较 structured prediction、encoder-decoder 和 encoder-only 表示。
- 说明这些主题与 decoder-only LLM 的关系和边界。

核心推导：

- 标量 RNN recurrence 与 BPTT 梯度连乘。
- LSTM gate 如何改变长期信息路径。
- UAS/LAS 指标。
- seq2seq teacher forcing 与 exposure bias。
- MLM 与 causal LM 的 mask 方向差异。
- BIO tagging 如何把 token classification 转成 entity spans。
- Viterbi DP：emission + transition scores 下的最优 tag path。
- CRF forward algorithm：用 logsumexp 计算所有 tag paths 的 log-partition。
- encoder-decoder cross-attention 与 decoder-only causal self-attention 的信息流差异。

课堂 demo：

- 手写一个 transition parsing 状态序列。
- 手算 3 步标量 RNN hidden state 和 recurrent gradient factors。
- 给定 BIO tags，解码 NER spans，并讨论非法 `I-` 标签的处理策略。
- 给定小型 emission/transition table，手算 Viterbi scores、backpointers 和 CRF forward alpha。
- 对比 BERT MLM 输入和 GPT causal LM 输入。
- 用 beam candidate table 展示 length-normalized score 如何改变排序。

Quick check：

- RNN 为什么难以直接学习很远的依赖？LSTM 缓解了什么但没有解决什么？
- BERT 是 decoder-only 模型吗？
- BLEU 高是否代表事实正确？

课后产出：

- 经典 NLP 专题书面题。
- 阅读复盘：RNN/LSTM、BERT 或 seq2seq 的一个 inductive bias。
- Deep-dive in-class check：RNN-1、DP-1、S2S-2 或 BERT-1 至少完成一项。

## Week 8 Lecture 16: Evaluation、Ethics、Safety 与同伴 Review

对应材料：classic NLP handout、presentation peer review、项目报告要求。

目标：

- 比较 perplexity、BLEU、ROUGE、F1、EM、LLM-as-judge。
- 讨论隐私、偏见、幻觉、评测污染和安全拒答。
- 训练同伴 review 的评价标准和反馈质量。

核心推导：

- precision/recall/F1 与 exact match。
- benchmark contamination 与 data leakage 的区别。

课堂 demo：

- 对同一输出分别用 ROUGE、EM 和人工判断打分。
- 现场 review 一段项目摘要，标出最强产出和最大风险。

Quick check：

- 为什么单一指标不能覆盖 LLM 质量？
- review 里“建议更好”为什么不是可执行反馈？

课后产出：

- 第 8 周同伴 review。
- 经典 NLP/evaluation 书面题。

## Week 9 Lecture 17: KV Cache、FlashAttention 与 Serving Metrics

对应材料：Ch10、reading-list Week 9。

目标：

- 推导 KV cache 显存公式。
- 区分 prefill/decode、TTFT、TPOT、tokens/s、P95/P99。
- 解释 FlashAttention 的 IO-aware 动机。

核心推导：

- KV cache bytes `2 * batch * layers * seq_len * kv_heads * head_dim * dtype_bytes`。
- tail latency 与并发队列的关系。

课堂 demo：

- 用 Ch10 代码验证 incremental attention 与 full causal attention 等价。
- 运行 inference capstone benchmark，读 P95 和 tokens/s。
- 把一次 benchmark 结果改写成 metric card，区分任务、baseline、指标和结论边界。

Quick check：

- KV cache 公式里的 2 表示什么？
- 平均延迟为什么不能替代 P95？
- 为什么固定开发集上的 pass rate 不能证明开放域能力？

课后产出：

- Ch10 KV cache 与 metric card 测试通过。
- 推理项目提案。

## Week 9 Lecture 18: RAG、Quantization、多模态输入与 Production Readiness

对应材料：Ch10、inference capstone。

目标：

- 解释 RAG 的 chunking、embedding、retrieval、rerank、prompt assembly。
- 计算 Recall@k 和 MRR，区分召回失败与排序失败。
- 比较 weight-only quantization、KV quantization、FP8/FP4。
- 区分 VQA、OCR、图表理解、视觉定位和视频理解的评价方式。
- 建立上线前的 latency、cost、quality 和 safety 判断框架。

核心推导：

- cosine similarity 与 normalized dot product。
- InfoNCE / in-batch negatives：`Q D^T / temperature` 后用对角线正样本做 cross entropy。
- Cross-encoder pairwise reranker loss：`-log sigmoid(s_chosen - s_rejected)`。
- quantization scale、dequantization error 和 ranking 误差。
- RAG retrieval metrics：Recall@k、reciprocal rank 与 nDCG@k。
- RRF 融合 dense/BM25 排序；rerank 改善前排相关性但会增加延迟。
- 视觉 token 数如何影响 prefill latency 和 KV cache 成本。

课堂 demo：

- 运行 RAG toy retriever，制造 chunk overlap 错误。
- 给定 query/document embedding batch，手算 contrastive logits 和对角线 labels。
- 给定 chosen/rejected reranker scores，手算 pairwise loss 和排序准确率。
- 给定 retrieved/relevant ids 与 graded relevance，手算 Recall@k、reciprocal rank 和 nDCG@k。
- 给定 dense/BM25 排序，手算 RRF 分数，再用 reranker 分数调整 top-k。
- 对 per-channel INT8 权重做 roundtrip。
- 对同一张图设计 VQA、OCR、图表和定位四类问题，比较指标差异。

Quick check：

- RAG 失败一定是模型生成错了吗？
- INT8 降低的是权重显存、KV cache 还是两者？
- 一个多模态模型 VQA 分数高，是否能推出 OCR 或视觉定位可靠？

课后产出：

- A9 RAG/quantization/benchmark 测试通过。
- 推理 capstone 初版，包含 RAG 或多模态输入的失败模式分析。

## Week 10 Lecture 19: Capstone Reproducibility Workshop

对应材料：两个 capstone README、frontier reading notes。

目标：

- 检查项目报告是否包含 seed、环境、日志、评测集和失败案例。
- 区分实验结论、模型卡声明和推断性说法。
- 修复复现包中的命令、依赖和路径问题。

核心推导：

- capacity/cost 估算随 batch、context、dtype、GPU memory 变化。
- ablation 应只改变一个关键变量。

课堂 demo：

- 互换项目复现命令，记录首个失败点。
- 分析一个前沿模型 claim 的任务设置、评测版本和适用范围。

Quick check：

- “本实验条件下成立”和“一般成立”有什么区别？
- 没有失败案例的项目报告可信度如何？

课后产出：

- capstone 最终报告草稿。
- reading notes 表格。

## Week 10 Lecture 20: Final Presentation、Poster Session 与课程回顾

对应材料：presentation peer review、syllabus。

目标：

- 完成项目展示、问答和同伴 review。
- 回顾从 tokenizer 到 serving 的端到端数据流。
- 明确学生最终应能独立复现和解释的产出。

核心推导：

- 从输入 token 到输出 token 的完整 shape trace。
- 从训练成本到推理成本的指标链路。

课堂 demo：

- 每组 5-8 分钟展示，2-3 分钟问答。
- 助教现场核对最小复现命令和报告要求。

Quick check：

- 你的项目中最强产出和最大风险各是什么？
- 哪个结论需要更多数据或更强 benchmark 才能支撑？

课后产出：

- 最终报告、复现包、展示材料、同伴 review 修改说明。

## Discussion Section 模板

每周讨论课建议围绕三件事：

1. Shape drill：给一个核心模块，学生写出输入、输出和中间张量 shape。
2. Failure drill：给一个失败测试或错误日志，学生判断是数学、mask、dtype、device、数据还是评测问题。
3. Paper-to-code drill：从本周论文中选一个公式或结构，指向课程代码中的对应函数。

## Office Hours 模板

助教答疑时优先使用以下顺序：

1. 复现学生命令和错误。
2. 让学生说明期望 shape 和实际 shape。
3. 检查是否违反作业公开 API。
4. 只讨论调试思路，不代写隐藏测试覆盖的核心实现。
5. 记录高频问题，下一讲 recap 中集中澄清。

## Exit Ticket 模板

```text
Lecture:
One concept I can explain:
One tensor shape I verified:
One test or experiment I ran:
One point I still find unclear:
```
