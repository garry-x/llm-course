# Concept Mastery and Misconception Map

本地图用于把章节内容、作业测试、quick check、office hours 和补救任务连接起来；术语定义和不要误讲成什么见 [Core Concept Glossary](core-concept-glossary.md)，先修依赖、章节 unlock path 和 spiral review 路径见 [Topic Dependency and Spiral Review Map](topic-dependency-map.md)，聚合信号如何触发 recap、worksheet、office hours 或项目 mentor check 见 [Learning Analytics and Remediation Plan](learning-analytics-remediation-plan.md)。它面向三类使用场景：

- 学生复习时确认自己是否真正掌握概念，而不是只记住公式。
- 助教答疑时快速定位错误类型，并给出对应章节、作业或书面题。
- 教师出 quiz、midterm 和 hidden tests 时覆盖常见误区，而不是只测 happy path。

使用规则：

- 每个模块至少检查一个 shape invariant、一个数学或概率边界、一个工程失败模式。
- 如果学生能跑通公开测试但答不出“为什么这样做”，应转到对应 quick check 或书面题。
- 如果同一误区在一周内出现 3 次以上，课程组应更新章节 FAQ、office-hour 记录或 hidden-test 反馈模板。

## 掌握等级

| 等级 | 判定标准 | 典型证据 | 补救动作 |
|------|----------|----------|----------|
| Ready | 能解释公式、shape、复杂度和失败模式，并能独立修复一个变体 bug | 作业公开测试通过；quick check ≥ 80%；能口头解释核心函数 | 进入下一模块 |
| Borderline | 能复现代码，但对边界条件、mask、归一化或指标解释不稳定 | 测试通过但书面题低分；debug 依赖提示 | 完成对应补救任务并在 office hours 复盘 |
| Not ready | 不能稳定写出核心 shape、公式方向或运行命令 | starter 失败不是 TODO；报告缺 seed/log；概念题无法定位错误 | 回到 prerequisite/math review，并重做最小作业 |

## 逐章误区与补救地图

| 模块 | 必须掌握 | 常见误区 | 快速检查 | 补救材料 | 评分证据 |
|------|----------|----------|----------|----------|----------|
| Ch01 Tokenization / BPE | byte-level BPE 的训练循环、merge rank、encode/decode、OOV 处理 | 把最高频 pair 当作全局最优压缩；把 BPE 编码说成普通最长匹配；忽略 Unicode byte 边界 | 给定 `["l","o","w"]` 合并规则，手算一次 merge 后 token 序列；解释为什么 byte-level 通常无 OOV | Ch01；`assignments/ch01_bpe/`；`written-problem-set.md` Ch01 | tokenizer 单元测试；词表大小实验；BPE 贪心局限短答 |
| Ch02 Embedding / Position Encoding / RoPE | embedding lookup、sinusoidal position、RoPE 旋转、相对位置内积形式 | 把 embedding 当成语义本身；认为 RoPE 保证距离越远分数单调下降；忘记 head dim 必须成对旋转 | 写出 `one_hot @ E` 的 shape；证明位置 0 的 RoPE 是 identity；解释 norm preservation 不等于语义不变 | Ch02；`assignments/ch02_embeddings/`；`math-prerequisites.md` | RoPE 数值验证；相对位置 Toeplitz 检查；外推失败报告 |
| Ch03 Scaled Dot-Product Attention | Q/K/V 投影、score shape、`1/sqrt(d_k)` 缩放、softmax 前 mask | mask 放在 softmax 后；把 attention 权重解释成因果解释；忽略 all-masked row 的数值风险 | 给定 `B,T,d,h` 写出 `QK^T` shape；说明为什么 mask 应作用在 logits；手算一个 3-token causal mask | Ch03；`assignments/ch03_attention/`；board derivation pack | attention 实现测试；mask 单元测试；缩放方差推导 |
| Ch04 MHA / GQA / MLA | head reshape、MHA/GQA/MLA 参数和 KV cache 差异、增量解码缓存 | 把 GQA 说成减少 query 参数；把 MLA matrix absorption 说成免费注意力；混淆训练时和解码时 cache | 比较 MHA 与 GQA 的 K/V head 数；估算 batch/context 对 KV cache 的影响；说明 latent cache 省在哪里 | Ch04；`assignments/ch04_multihead/`；`compute-resource-guide.md` | 参数量对比；cache 显存计算；MHA/GQA/MLA shape 测试 |
| Ch05 Transformer Block / Norm / FFN | Pre-Norm residual、LayerNorm/RMSNorm、FFN/SwiGLU、梯度流 | 声称 Pre-Norm 保证无限深稳定；把 RMSNorm 当成 LayerNorm 去均值版本；忘记 dropout/eval 模式差异 | 写出 LayerNorm 归一化维度；解释 RMSNorm 为什么不中心化；指出 residual path 如何绕过子层 | Ch05；`assignments/ch05_block/`；`math-prerequisites.md` | gradcheck；block 前向/反向测试；norm 公式短答 |
| Ch06 GPT Assembly / MoE | decoder-only 堆叠、weight tying、初始化、next-token loss、MoE routing | 把所有现代 LLM 绝对化为 decoder-only；忽略 context 长度检查；把 router top-k 当成可微硬选择 | 解释 logits 与 shifted labels 的对齐；估算 GPT-2 small 参数量；说明 expert imbalance 的观测指标 | Ch06；`assignments/ch06_gpt/` | forward shape；weight tying 检查；MoE router normalization 测试 |
| Ch07 Training Loop | dataset shift、cross entropy、AdamW、warmup/cosine、checkpoint/resume、perplexity | 混淆 AdamW 和 L2 regularization；把 PPL=1 解释成真实数据中可达的确定性；忽略 scheduler step 顺序 | 手算一条 next-token 样本；解释 `exp(loss)` 的条件；说明 resume 时 optimizer/scheduler 必须恢复 | Ch07；`assignments/ch07_training/`；training capstone | loss/scheduler 测试；checkpoint resume 证据；训练日志和 seed |
| Ch08 Generation / Decoding | greedy、temperature、top-k、top-p、repetition、speculative decoding | 把 top-p 当成固定 k；把 temperature=0 当成普通除零；把 speculative decoding 说成无条件无损加速 | 给定 logits 手算 top-p 保留集合；解释 draft rejection；比较 diversity 指标和人工质量 | Ch08；`assignments/ch08_generation/` | sampling 边界测试；distinct n-gram 报告；speculative stats |
| Ch09 SFT / LoRA / DPO / GRPO | prompt/label mask、LoRA delta、DPO log-ratio、GRPO group advantage | 让 loss 训练 prompt tokens；认为 LoRA merge 不改变 base 权重引用风险；把 GRPO whitening 说成完全解决 reward scale | 标出 SFT labels 中的 `-100`；写出 DPO chosen/rejected 方向；解释 group 内标准化限制 | Ch09；`assignments/ch09_alignment/`；data ethics review | SFT mask 测试；LoRA merge 测试；DPO/GRPO 数值题 |
| Ch10 Inference / RAG / Serving | KV cache、量化误差、RAG chunk/retrieve、SLO、capacity planning | 忽略 batch size 对 cache 的乘法影响；只看平均延迟不看 P95/P99；把 retrieval hit 当成 answer correctness | 计算 KV cache GB；解释 TTFT/TPOT 区别；给一个 RAG 失败案例分类 | Ch10；`assignments/ch10_inference/`；inference capstone | SLO 门禁；benchmark 报告；RAG retrieval/eval 测试 |
| Ch11 Classic NLP / Evaluation | dependency parsing、UAS/LAS、BLEU/ROUGE、EM/F1、MLM example | 把 BLEU 当成语义充分指标；混淆 UAS 和 LAS；忽略 normalization 对 EM/F1 的影响 | 给定 heads/labels 手算 UAS/LAS；计算一个短句 BLEU brevity penalty；解释 MLM label mask | classic NLP handout；`assignments/ch11_classic_nlp/` | UAS/LAS 测试；BLEU/ROUGE/EM/F1 测试；经典 NLP 书面题 |

## 跨章节高风险边界

| 边界 | 容易出错的说法 | 正确检查 |
|------|----------------|----------|
| Shape first | “公式看起来对，所以实现大概率对” | 先写 `B,T,C,H,D`，再检查 matmul、broadcast、mask 和 loss target |
| Mask before probability | “mask 后把概率乘 0 也一样” | 对 attention logits 加 `-inf` 或大负数，再 softmax；检查 all-masked row |
| Norm vs semantics | “RoPE/LayerNorm 保持 norm，所以语义不变” | norm preservation 是几何或数值性质，不等于语义或模型行为不变 |
| Metric vs quality | “BLEU/ROUGE/PPL/SLO 高就代表模型好” | 指标只能覆盖定义内的质量维度，必须配合错误分析和任务条件 |
| Public tests vs mastery | “公开测试通过就说明作业满分” | 公开测试只证明基础 API；hidden tests、书面题和报告解释覆盖边界条件 |
| Frontier claims | “某模型/方法已经证明最好” | 检查来源等级、发布时间、实验条件、任务范围和复核日期 |

## Quick Check 题型模板

| 类型 | 出题方式 | 合格答案应包含 |
|------|----------|----------------|
| Shape trace | 给定 `B,T,C,H` 和一段伪代码，要求写出每步 shape | 维度含义、广播位置、最终 logits/loss shape |
| Boundary fix | 给出一个通过普通输入但边界失败的函数 | 失败输入、原因、最小修复、回归测试 |
| Claim audit | 给出一句过强技术 claim | 来源等级、适用条件、应该改写的限定词 |
| Metric interpretation | 给出两组实验指标 | 哪个指标支持结论、哪个指标不能支持结论、还缺什么证据 |
| Reproducibility check | 给出不完整实验日志 | 缺少 seed、版本、数据、硬件、命令或失败案例 |

## 维护 Checklist

- 每个章节至少对应 3 个常见误区，并能映射到作业、书面题或 capstone。
- 每次新增隐藏测试或 quiz 题，应在本地图中标记对应误区。
- 如果 `verify_course.py` 的 overclaim 检查新增规则，应同步检查本地图是否已有解释。
- 学生 FAQ 和 office-hour 高频问题每两周与本地图对齐一次。
