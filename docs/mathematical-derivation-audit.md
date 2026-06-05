# Mathematical Derivation Audit

本文件把课程中进入 lecture、written assessment、assignment 或 capstone 的关键数学推导整理为可审计清单。它补充 [Board Derivation and Instructor Notes Pack](board-derivation-pack.md)、[Chapter Claim Audit Ledger](chapter-claim-audit-ledger.md)、[External Expert Review Dossier](external-expert-review-dossier.md)、[Notation and Shape Glossary](notation-shape-glossary.md)、[Worked Example Pack](worked-example-pack.md)、[书面推导与概念题题库](written-problem-set.md) 和 [Course Outcome Map](course-outcome-map.md)。

复核日期：2026-06-05
适用范围：Ch01-Ch10 正文章节、Ch11 经典 NLP 专题、章节作业、书面题和 capstone 报告。
维护原则：每条推导必须同时写出符号/shape、必要假设、可执行证据和边界；不能用单个公式支持来源没有证明的更强结论。

## Audit Schema

| Field | 要求 |
|-------|------|
| Derivation ID | `DER-xx`，稳定编号，可被 lecture notes、written problem 和 verifier 引用 |
| Chapter / use | 推导出现位置和评分使用场景 |
| Core statement | 学生需要能推导或解释的结论 |
| Assumptions | 推导成立所需的分布、shape、模型或工程条件 |
| Shape / units | 最小 shape 检查或单位检查 |
| Executable evidence | 对应公开测试、capstone acceptance、verifier 或 release gate |
| Boundary | 该推导不能推出的更强结论 |

## Audited Derivations

| Derivation ID | Chapter / use | Core statement | Assumptions | Shape / units | Executable evidence | Boundary |
|---------------|---------------|----------------|-------------|---------------|---------------------|----------|
| DER-01 | Ch01 BPE; written Ch01; `assignments/ch01_bpe/` | BPE 每轮选择当前最高频相邻 pair，是局部贪心 merge，不是全局最优压缩证明 | 语料已被离散化为字符、byte 或 token 序列；每轮 merge 后重新统计 pair | 输入为 token 序列列表；merge 后序列长度可降、词表大小增加 | Ch01 BPE tests；`check_unqualified_claim_phrasing()` optimality gate | 不能推出语义最优、PMI 最高或所有语言 token 成本公平 |
| DER-02 | Ch02 embedding; written Ch02; `assignments/ch02_embeddings/` | embedding lookup 等价于 one-hot 向量乘 embedding matrix | token id 合法且在 `[0,V)`；embedding matrix 可训练 | `E in R^{V x D}`；`input_ids [B,T] -> [B,T,D]` | Ch02 embedding tests；Ch06 weight tying tests | 类比结构是经验现象，不是训练目标保证的线性规则 |
| DER-03 | Ch02 RoPE; written Ch02; Ch04 MLA boundary | `q'_m^T k'_n = q^T R_{n-m} k`，RoPE attention score 只依赖相对位移 | 最后一维按 2D block 成对旋转；query/key 使用同一频率表；旋转矩阵正交 | `q,k [B,H,T,D_h]`，`D_h` 可按 pair 处理；score `[B,H,T,T]` | Ch02 RoPE Toeplitz tests；`check_key_derivation_consistency()` | norm 保持不等于语义保持；不保证任意长上下文稳定外推 |
| DER-04 | Ch03 attention scaling; written Ch03; `assignments/ch03_attention/` | 若 `q_i,k_i` 独立、零均值、单位方差，则 `Var(q^T k)=d_k`，除以 `sqrt(d_k)` 控制 score 尺度 | 独立性、零均值、单位方差是近似分析条件 | `Q [B,H,T,D_h]`、`K^T [B,H,D_h,T]`、score `[B,H,T,T]` | Ch03 scaled attention tests；written derivation gate | 不保证梯度总在有效范围；实际分布和层间相关性会偏离假设 |
| DER-05 | Ch03 causal mask; written Ch03; attention implementation | causal mask 应在 softmax 前加到 logits，阻断未来 token 概率质量 | 自回归 decoder-only 任务；mask 与 score broadcast 对齐 | mask `[T,T]` 或 `[B,1,T,T]`；score `[B,H,T,T]` | Ch03 causal mask tests；browser formula/render gate | softmax 后直接乘 mask 需要重归一，否则不是同一分布 |
| DER-06 | Ch04 MHA/GQA/MLA; written Ch04/Ch10 | KV cache 元素数与 `2 * B * T * H_kv * D_h` 成正比；GQA/MQA 主要减少 KV head cache | decoder incremental serving；每层缓存 K 和 V；dtype bytes 单独计入 | 每层元素数 `2BTH_kvD_h`；全模型再乘 layers 和 bytes | Ch04 GQA/MLA tests；Ch10 KV cache tests；inference capstone capacity plan | cache 降低不等于质量不变、端到端加速或 attention 计算免费 |
| DER-07 | Ch05 LayerNorm/RMSNorm; written Ch05; `assignments/ch05_block/` | LayerNorm 的均值/方差依赖输入，RMSNorm 只按 RMS 缩放；反向传播不能把统计量当常数 | normalization over last hidden dimension；`eps` 防止除零 | `x [B,T,D]`；`gamma,beta [D]`；输出 `[B,T,D]` | Ch05 LayerNorm gradcheck；RMSNorm tests | Pre-Norm 常改善稳定性，但不保证任意深度或任意 optimizer 成功 |
| DER-08 | Ch06 GPT assembly; written Ch06; `assignments/ch06_gpt/` | decoder-only GPT 参数量来自 token embedding、position embedding、每层 attention/FFN/norm 和 LM head；weight tying 可共享 token embedding 与 output head | config 固定 `V,T,D,H,L`；FFN hidden size 和 bias policy 明确；tied head 使用同一权重对象 | `input_ids [B,T] -> logits [B,T,V]`；tied head 减少约 `V*D` 个独立参数 | Ch06 GPT parameter and weight tying tests；course verifier assignment API gate | 参数量推导不等于训练显存或推理吞吐；MoE sparse activation 也不等于成本线性降低 |
| DER-09 | Ch07 next-token CE; training capstone | 自回归 MLE 等价于最小化 next-token negative log likelihood / cross entropy | labels 右移；padding 或 prompt token 可用 ignore policy 排除 | logits `[B,T,V]`；labels `[B,T]`；loss scalar 或 token average | Ch07 CE tests；training capstone acceptance | perplexity 是平均 NLL 的指数，不等于事实正确率或开放生成质量 |
| DER-10 | Ch07 AdamW; written Ch07; training plan | AdamW decouples weight decay from Adam gradient update，不等同于 Adam + L2 penalty | optimizer 使用 Adam moment estimates；weight decay 独立作用于参数 | parameter units unchanged；lr 和 decay 共同决定 shrinkage | Ch07 AdamW tests；training capstone plan evidence | learning-rate schedule、gradient clipping 和 weight decay 不能互相替代 |
| DER-11 | Ch08 sampling and speculative decoding; written Ch08; `assignments/ch08_generation/` | top-p 保留累计概率达到阈值的最小 nucleus；推测解码只有在接受/拒绝校正满足假设时才保持目标分布 | logits 已归一化为概率；temperature、top-k/top-p 顺序固定；draft/target 分布可计算 | probability mass sums to 1 after filtering；generated length and acceptance rate are reported scalars | Ch08 sampling tests；speculative decoding stats tests | 多样性指标不等于人工质量；推测解码加速取决于 draft 质量、batching 和系统瓶颈 |
| DER-12 | Ch09 DPO/GRPO; written Ch09; `assignments/ch09_alignment/` | DPO 优化 chosen/rejected log-ratio；GRPO 用组内相对 advantage whitening | chosen/rejected 序列 log prob 已按 response token 聚合；GRPO group 内有多个候选 | sequence log prob scalar；group advantage mean/scale 在同 prompt 组内计算 | Ch09 DPO/GRPO tests；alignment safety rubric | 不证明完整安全对齐，也不消除 reward noise、KL、采样覆盖问题 |
| DER-13 | Ch10 serving SLO and capacity; inference capstone | P95/P99 latency、TTFT、TPOT、tokens/s 和成本必须绑定模型、硬件、context、batching 与 workload | benchmark workload 固定；SLO 阈值预先声明；容量估算使用明确 dtype 和 memory budget | latency ms；throughput tokens/s；cost USD / 1M tokens；memory GB | inference capstone acceptance；SLO check；capacity plan | 平均延迟或单机 toy run 不能证明生产可用性 |
| DER-14 | Ch11 classic NLP evaluation; written Ch11; capstone reports | BLEU/ROUGE/EM/F1、UAS/LAS 各有任务假设，必须和人工错误分析或下游指标配合使用 | reference answers/parse labels 可用；文本规范化规则固定 | metric in `[0,1]` 或 percentage；paired comparison 需同输入集合 | Ch11 classic NLP tests；experimental rigor guide | 自动指标不能单独证明开放式 LLM 质量、安全或事实可靠性 |

## Executable Gate Coverage

| Gate | 覆盖 derivations | 命令或检查 |
|------|------------------|------------|
| Assignment tests | DER-01 到 DER-12、DER-14 | `.venv/bin/python run_assignment_tests.py` |
| Course verifier | 全部 | `.venv/bin/python verify_course.py` |
| Formula / formatting gate | DER-02 到 DER-11 | `check_text_and_formula_format()`、`check_python_code_blocks_compile()`、`check_key_derivation_consistency()` |
| Capstone release gate | DER-09、DER-13 | `.venv/bin/python verify_course.py --capstone --training` |
| Source / claim gate | 全部 | `check_chapter_claim_audit_ledger()`、`check_source_governance_docs()`、`check_mathematical_derivation_audit()` |

## Instructor Review Protocol

1. 每轮开课前抽查至少 4 条 derivation：一个 tokenization/embedding，一个 attention/normalization，一个 training/alignment，一个 serving/evaluation。
2. 对每条抽查项，核对章节正文、board derivation、written problem、assignment tests 和 boundary 是否一致。
3. 若新增公式进入作业或考试，先在本文件增加 `DER-xx`，再加入 [Chapter Claim Audit Ledger](chapter-claim-audit-ledger.md) 或 [Claim Audit Worksheet](claim-audit-worksheet.md)。
4. 若公式依赖易变模型卡、benchmark、API 或硬件性能，必须同步 [External Source Verification Guide](external-source-verification.md) 和 [前沿模型来源等级与复核记录](frontier-source-audit.md)。
5. 每次更新后运行 `.venv/bin/python verify_course.py`；若影响 capstone，额外运行 `.venv/bin/python verify_course.py --capstone --training`。

## 发布前 Checklist

- Ch01-Ch10 和 Ch11 至少各有一条可审计 derivation 或 evaluation statement。
- 每条 derivation 都有 assumptions、shape / units、executable evidence 和 boundary。
- 进入评分的 derivation 都能在 assignment tests、written assessment、capstone acceptance 或人工 rubric 中找到证据。
- 任何“最优”“保证”“无损”“免费”“实时”“生产可用”等强表述都必须有来源、配置或边界。
- 本文件与 board derivation pack、claim audit ledger、written problem set、source map 和 outcome map 互相链接。
