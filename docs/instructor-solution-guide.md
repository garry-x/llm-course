# Instructor Solution Guide

本文件供教师和助教评分使用，不建议直接发给学生。它不是完整标准答案，而是每章书面题的答案要点、常见错误和扣分边界，用于保证不同助教评分一致。

## 使用规则

- 正式作业可从 `written-problem-set.md` 每章抽 2-3 题。
- 批改时优先看推导链条、shape、边界条件和解释质量，而不是只看最终数字。
- 学生可以使用不同符号；只要假设清楚、维度一致、结论正确，应给分。
- 若学生引用前沿模型数字，必须检查来源等级、日期和评测设置。

## 书面题选择与证据矩阵

下表给出每章正式作业的建议抽题组合。教师可以替换题目，但每章至少应保留一个数学/shape 题和一个边界/工程判断题，避免书面部分只考记忆性概念。

| 章节 | 正式作业建议题 | 满分证据下限 | 人工复核重点 |
|------|----------------|--------------|--------------|
| Ch01 Tokenization / BPE | Q1 + Q2，Q3 可作讨论课 | 能说明非重叠 merge、贪心非全局最优、byte/word/char 取舍 | 是否把 BPE 误讲成语义最优分词 |
| Ch02 Embedding / RoPE | Q1 + Q3 | 能写出 lookup 等价和 `R_m^T R_n = R_{n-m}`，并说明外推限制 | 是否把相对位置性质误讲成无限上下文保证 |
| Ch03 Attention | Q1 + Q2，Q3 可作期中题 | 能推导 `Var(q^T k)=d_k`，正确放置 mask，并写清 shape | 是否 softmax 后 mask 且不归一化 |
| Ch04 MHA / GQA / MLA | Q1 + Q2 + Q3 | 能计算 KV cache 元素数，说明 GQA 只减少 K/V 头，MLA 仍有重建/解压成本 | 是否把 latent cache 说成免费注意力 |
| Ch05 Block / Norm / FFN | Q1 + Q2 | 能说明 LayerNorm 反向的均值/方差依赖，比较 Pre-Norm/Post-Norm 梯度路径 | 是否把 RMSNorm 与 LayerNorm 等同 |
| Ch06 GPT / MoE | Q1 + Q3 | 能逐项审计 GPT-2 small 参数，区分 total 与 activated parameters | 是否重复计算 tied LM head 或忽略 MoE 负载 |
| Ch07 Training | Q1 + Q2 + Q4 | 能从自回归分解到 CE 梯度，并用日志诊断 NaN/loss spike/tokens/s 下降 | 是否把 PPL 当准确率或忽略右移目标 |
| Ch08 Generation | Q1 + Q2 + Q4 | 能手算 top-p nucleus，比较解码策略，并解释 speculative decoding 接受率/成本 | 是否把 beam/search/sampling 优劣绝对化 |
| Ch09 Alignment | Q1 + Q2 + Q3 | 能标出 `-100` mask，解释 DPO reference log-ratio 和 GRPO 组内白化边界 | 是否说 DPO 不需要 reference 或 GRPO 解决安全 |
| Ch10 Inference | Q1 + Q2 + Q5 | KV cache 公式完整，延迟指标含 P95/P99，benchmark claim 有来源/日期/设置 | 是否只报均值或把参数显存当 KV cache |
| 经典 NLP 专题 | Dependency + BERT + Evaluation 至少各 1 题 | 能区分 UAS/LAS、MLM/causal LM、BLEU/ROUGE/F1/LLM judge 局限 | 是否用单一自动指标替代人工质量判断 |

评分时每个正式书面题建议采用 10 分制：数学/算法核心 4 分，shape/边界 2 分，工程解释 2 分，来源或实验判断 1 分，表达清晰度 1 分。若题目不涉及来源，则把该 1 分并入工程解释；若题目是前沿模型或 benchmark 判断，来源/日期/设置缺失时该项不得分。

## Ch01 Tokenization / BPE

答案要点：

- 一次 BPE merge 会把被选 pair 的每次非重叠出现合并成一个新 token，序列长度减少量等于该 pair 的非重叠出现次数。
- 贪心最大频次合并只优化当前步，不保证未来所有 merge 后的全局最短序列。
- Byte-level BPE 基本消除 OOV，但序列可能更长；word-level 序列短但 OOV 和多语言覆盖差；character-level 词表小但上下文长。

常见扣分：

- 把 pair 的重叠出现次数直接当作长度减少量。
- 忽略 tie-breaking 对 merge 顺序和最终词表的影响。
- 只讨论英文，不讨论多语言或 byte fallback。

## Ch02 Embedding / Position Encoding / RoPE

答案要点：

- `one_hot @ E` 选出 embedding matrix 的一行；实际实现用 index lookup 避免构造稀疏 one-hot。
- Sinusoidal 的每个频率维度是二维旋转 block，`pos+k` 可由 `pos` 经过角度为 `omega k` 的旋转得到。
- RoPE 关键等式是 `R_m^T R_n = R_{n-m}`，因此点积依赖相对位移而非绝对位置。

常见扣分：

- 把 RoPE 说成“无限长上下文必然泛化”，没有说明训练分布、频率设计和数值外推限制。
- 忘记偶数维成对旋转。
- 混淆 sinusoidal 加法编码和 RoPE 乘法旋转。

## Ch03 Scaled Dot-Product Attention

答案要点：

- 若 `q_i,k_i` 独立且方差为 1，`Var(sum_i q_i k_i)=d_k`；除以 `sqrt(d_k)` 后方差回到约 1。
- Causal mask 应在 softmax 前加大负数或 `-inf`，使被 mask 的位置概率为 0。
- 训练 attention 的 score/probability activation 通常是 `O(BHT^2)`；推理 KV Cache 是 `O(BLHTD)` 级别，瓶颈不同。

常见扣分：

- 在 softmax 后 mask 但不重新归一化。
- 把计算复杂度和显存复杂度混为一谈。
- 忽略 mask shape 的广播规则。

## Ch04 MHA / GQA / MLA

答案要点：

- 标准 MHA 的 Q/K/V/O 投影仍是四个 `d_model x d_model` 矩阵；多头改变的是表示分块和 attention 子空间。
- MHA 每 token KV 元素为 `2 * n_heads * head_dim`；GQA 为 `2 * n_kv_heads * head_dim`。给定 32/8/128，MHA 为 8192，GQA 为 2048，压缩 4 倍。
- MLA 把 KV 内容压到 latent cache，推理时仍需要投影/矩阵吸收/额外 RoPE 分支等工程处理。

常见扣分：

- 把 GQA 的 Q 头数也减少。
- 把 MLA 说成完全不需要 K/V 重建或注意力计算。
- 忽略质量、实现复杂度和框架支持的 trade-off。

## Ch05 Transformer Block / Norm / FFN

答案要点：

- LayerNorm 中 `mu` 和 `var` 都由 `x` 计算得到，反向传播包含跨 feature 的耦合项。
- Pre-Norm 让 residual 分支提供更直接的梯度路径，深层训练更稳定；Post-Norm 表达可行但深层更难训。
- SwiGLU 通常比 GELU FFN 多门控分支；MoE 增加 total parameters，但每 token 只激活少数专家。

常见扣分：

- 把 RMSNorm 说成等价于 LayerNorm。
- LayerNorm 反向只写 `dy * gamma / std`。
- 只比较参数量，不讨论激活参数、通信和负载均衡。

## Ch06 GPT Assembly / MoE

答案要点：

- GPT-2 small 参数审计应包含 token embedding、position embedding、每层 attention/MLP/LayerNorm、final LayerNorm；tied LM head 不重复计数。
- Weight tying 共享输入 embedding 和输出 projection 权重，减少参数并让词向量空间保持一致约束。
- MoE total parameters 是所有专家总和；activated parameters 是每 token 被路由到的 top-k 专家加 shared expert。

常见扣分：

- tied embedding 下重复计算 LM head 参数。
- 忘记 attention/MLP bias 或 LayerNorm 参数。
- 认为 top-k 稀疏激活会自动保证负载均衡。

## Ch07 Training Loop

答案要点：

- 自回归分解为 `p(x)=prod_t p(x_t|x_<t)`；NLL 是 `-sum log p_theta(target|context)`，实现为 cross entropy。
- Cross entropy 对 logits 的梯度为 `softmax(z)-one_hot(y)`。
- AdamW 将 weight decay 作为参数更新项与梯度矩估计解耦；warmup 降低早期不稳定，cosine decay 让后期细化收敛。
- Loss spike/NaN 常见原因包括学习率过大、数据异常、混合精度溢出、梯度爆炸；tokens/s 下降可能来自 dataloader、显存碎片、长样本或硬件争用。

常见扣分：

- 把 perplexity 当作事实正确率。
- 忘记 target 是 input 右移一位。
- 不区分 L2 regularization 与 decoupled weight decay。

## Ch08 Generation / Decoding

答案要点：

- Greedy 可复现但易退化；temperature 调节分布尖锐度；top-k 限制候选数量；top-p 保留累计概率达到阈值的最小集合。
- 给定 `[0.40,0.25,0.20,0.10,0.05]`：`p=0.7` 保留前三个 token，因为 0.40+0.25=0.65 不足，+0.20=0.85；`p=0.9` 保留前四个 token。
- Beam search 适合翻译等目标较确定任务；开放式对话常更适合 sampling。
- Speculative decoding 吞吐取决于 draft 成本、接受率和 target 验证批量；draft 太弱接受率低，太强成本高。

常见扣分：

- Top-p 少保留导致累计概率低于阈值。
- 忘记采样后重新归一化。
- 把 beam search 等同于总是质量更高。

## Ch09 Fine-tuning / Alignment

答案要点：

- SFT label 中 prompt 和 padding 位置应为 `-100`，只让 assistant response 贡献 loss。
- DPO 比较 chosen/rejected 在 policy 相对 reference 的 log probability 改变量。
- GRPO 组内白化消除不同 prompt reward 尺度差异，但不能解决 reward model 错误、奖励稀疏、分布外泛化或安全漏洞。
- LoRA rank 增加表达能力和参数量；alpha 改变缩放；target modules 决定适配能力和训练成本；merge 后推理无需额外 adapter 分支。

常见扣分：

- 对 `-100` 直接 gather 导致非法索引。
- 认为 DPO 不需要 reference model。
- 把 GRPO 组内标准化当作完整安全对齐方案。

## Ch10 Inference / RAG / Serving

答案要点：

- KV Cache bytes 为 `2 * batch * layers * seq_len * kv_heads * head_dim * dtype_bytes`，其中 2 表示 K 和 V。
- TTFT 对应首 token 等待，TPOT 对应 decode 单 token 成本，tokens/s 对应吞吐/成本，P95 latency 对应尾部用户体验。
- RAG 失败要按 chunking、embedding、retrieval、reranking、prompt assembly、generation 分类，不能只归咎于模型。
- INT8 weight-only 主要降权重带宽；KV quant 降 cache 显存/带宽；FP8/FP4 mixed precision 常用于训练或推理整体吞吐，但需要校准和误差验证。
- 前沿 benchmark 必须带来源、日期、任务、shot 数、评测版本和硬件/上下文条件。

常见扣分：

- KV Cache 公式漏掉 batch size 或 K/V 的 2 倍。
- 只报告平均延迟，不报告 P95/P99。
- 用新闻或社区帖子作为唯一模型规格来源。

## 经典 NLP 专题

答案要点：

- Dependency parsing：UAS 只看 head，LAS 同时看 head 和 label；transition 序列必须保持 stack/buffer 合法。
- Seq2Seq/NMT：encoder 表示源句，decoder 自回归生成；attention 每步对源端加权；beam length bias 需要 length penalty 或 normalized score。
- BERT：MLM 双向看上下文，适合分类/抽取/序列标注；causal LM 只能看左侧上下文，适合生成。
- Evaluation：BLEU/ROUGE 是词面重合指标，F1/EM 适合有标准答案任务，LLM-as-judge 需要控制位置偏置、模型偏置和污染。
- Ethics/Safety：答案应覆盖隐私、偏见、幻觉、评测污染、安全拒答和版权/引用中的至少三个，并给出具体缓解策略。

常见扣分：

- 把 LAS/UAS 混同。
- 把 BERT 描述成 decoder-only 生成模型。
- 只列风险名词，没有触发样例或缓解方案。
