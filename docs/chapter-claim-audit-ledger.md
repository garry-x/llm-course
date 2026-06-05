# Chapter Claim Audit Ledger

本台账记录当前课程正文、作业和项目材料中已经完成复核的关键 claim。它把 [Claim Audit Worksheet](claim-audit-worksheet.md) 的模板落到逐章证据上，并与 [Mathematical Derivation Audit](mathematical-derivation-audit.md)、[Worked Example Pack](worked-example-pack.md)、[Chapter Source and Accuracy Map](chapter-source-map.md)、[External Source Inventory](external-source-inventory.md)、[External Source Verification Guide](external-source-verification.md)、[External Expert Review Dossier](external-expert-review-dossier.md)、[Course Errata and Correction Ledger](course-errata-correction-ledger.md) 和 [前沿模型来源等级与复核记录](frontier-source-audit.md) 一起维护。

复核日期：2026-06-05
适用范围：Ch01-Ch10 正文章节、Ch11 经典 NLP 专题、章节作业、书面题和 capstone 指南。
维护原则：进入作业、测验或项目评分的 claim 必须有 A/B 级来源或课程内可复现实验证据；前沿模型、benchmark、API、价格、上下文长度和性能数字必须带来源等级、访问日期和边界。

## Ledger Schema

| Field | 要求 |
|-------|------|
| Claim ID | `CHxx-Cyy`，章节内稳定编号 |
| Location | 章节、作业、专题或项目材料位置 |
| Claim type | stable theory / implementation / frontier model card / benchmark / course inference |
| Source level | A-stable / A-volatile / B-implementation / C-background |
| Student-facing use | lecture / assignment / quiz / capstone / reading only |
| Boundary | 来源没有支持的更强结论 |
| Action | keep / qualify / downgrade / remove / replace |

## Audited Claims

| Claim ID | Location | Claim text | Claim type | Source level | Student-facing use | Boundary | Action |
|----------|----------|------------|------------|--------------|--------------------|----------|--------|
| CH01-C01 | Ch01 BPE; `assignments/ch01_bpe/` | BPE 每步选择高频相邻 pair 是局部压缩启发式，可缓解 OOV | stable theory | A-stable | lecture / assignment | 不保证全局最优、语义最优或 PMI 最高 | qualify |
| CH01-C02 | Ch01 tokenizer cost discussion | byte-level tokenizer 降低未知字符风险，但可能增加序列长度和成本 | implementation | B-implementation | lecture / quiz | vocab size、context length 和计费 token 不是同一概念 | keep |
| CH02-C01 | Ch02 word vectors | word2vec/GloVe 的类比现象是经验结构，不是训练目标保证 | stable theory | A-stable | lecture / assignment | 不写成“语义关系必然被线性编码” | qualify |
| CH02-C02 | Ch02 RoPE; `assignments/ch02_embeddings/` | RoPE 通过成对旋转使 Q/K 点积依赖相对位移 | stable theory | A-stable | lecture / assignment | norm preservation 不等于语义保持；长上下文外推另需证据 | keep |
| CH03-C01 | Ch03 attention scaling | 除以 `sqrt(d_k)` 控制点积分布尺度，缓解 softmax 饱和 | stable theory | A-stable | lecture / assignment | 方差推导依赖独立、零均值、单位方差等假设 | keep |
| CH03-C02 | Ch03 causal mask | causal mask 应在 softmax 前应用，阻断未来 token 概率质量 | stable theory | A-stable | lecture / assignment | softmax 后乘 mask 需要重归一，否则不是同一分布 | keep |
| CH04-C01 | Ch04 GQA/MQA | 减少 KV head 可降低 KV cache 参数和缓存占用 | implementation | A-stable | lecture / assignment | 节省 cache 不保证质量不变或端到端加速 | qualify |
| CH04-C02 | Ch04 MLA / DeepSeek reports | MLA 是 DeepSeek 技术报告中的 KV 压缩案例，本课程实现是教学简化 | frontier model card | A-volatile | lecture / assignment | 简化 latent cache 不能推出论文级性能或生产实现细节 | qualify |
| CH05-C01 | Ch05 Pre-Norm | Pre-Norm 通常改善深层 Transformer 优化稳定性 | stable theory | A-stable | lecture / assignment | 不是唯一正确结构，也不保证任意深度训练成功 | qualify |
| CH05-C02 | Ch05 LayerNorm/RMSNorm | LayerNorm 中心化并归一化，RMSNorm 只按 RMS 缩放 | stable theory | A-stable | lecture / assignment | backward 推导必须包含统计量依赖；不能只写逐元素缩放 | keep |
| CH06-C01 | Ch06 decoder-only LM | GPT 风格 decoder-only LM 用右移标签做 next-token prediction | stable theory | A-stable | lecture / assignment | 不等同于 encoder-only MLM 或 seq2seq teacher forcing 的全部设定 | keep |
| CH06-C02 | Ch06 MoE | MoE 激活参数少不等于训练或服务成本线性降低 | course inference | A-stable | lecture / quiz | routing、通信、capacity、负载均衡和实现都会影响成本 | qualify |
| CH07-C01 | Ch07 AdamW | AdamW 是 decoupled weight decay，不等同于 Adam 的 L2 penalty | stable theory | A-stable | lecture / assignment | weight decay、lr schedule、grad clipping 要分开解释 | keep |
| CH07-C02 | Ch07 training systems | FP8/FP4、DualPipe、Muon 是前沿训练系统案例 | frontier model card | A-volatile | lecture / capstone | 技术报告数字不能外推到所有模型、硬件或 workload | qualify |
| CH08-C01 | Ch08 top-p | top-p nucleus sampling 保留达到累计概率阈值的最小候选集合 | stable theory | A-stable | lecture / assignment | 采样质量仍依赖模型、prompt、temperature 和任务 | keep |
| CH08-C02 | Ch08 speculative decoding | 论文假设下拒绝采样校正可保持目标模型采样分布 | stable theory | A-stable | lecture / assignment | 真实加速取决于 draft 质量、接受率、batching 和系统瓶颈 | keep |
| CH09-C01 | Ch09 SFT | SFT 应 mask prompt 和 padding，只在回答 token 上训练 | implementation | A-stable | lecture / assignment | 不同任务可有不同 label policy，但必须写清 | keep |
| CH09-C02 | Ch09 DPO/GRPO | DPO 优化 chosen/rejected log-ratio；GRPO 使用组内相对优势 | stable theory | A-stable | lecture / assignment | 不能把 DPO/GRPO 描述成完整安全对齐保证 | qualify |
| CH10-C01 | Ch10 KV cache | KV cache 显存与 batch、layer、seq_len、KV head、head_dim 和 dtype 相关 | implementation | A-stable | lecture / assignment / capstone | 不要把权重显存当成 KV cache 显存 | keep |
| CH10-C02 | Ch10 serving benchmark | 推理 benchmark 只在给定模型、硬件、context、batching 和 workload 下成立 | benchmark | B-implementation | lecture / capstone | 平均延迟不足以支撑 SLO，需要 P95/P99 和配置 | qualify |
| CH10-C03 | Ch10 frontier V4/DSA/Engram | DeepSeek V4/DSA/Engram 相关内容只作前沿案例和来源边界训练 | frontier model card | A-volatile | lecture / reading only | 未逐条复核的 benchmark 数字不能进作业或考试事实 | downgrade |
| CH11-C01 | Ch11 dependency parsing | UAS/LAS 分别检查 head 和 label，适用于 dependency parsing 评测 | stable theory | A-stable | assignment / quiz | 指标不覆盖语义充分性或下游任务质量 | keep |
| CH11-C02 | Ch11 BLEU/ROUGE/EM/F1 | BLEU、ROUGE、EM/F1 各有任务假设和局限 | stable theory | A-stable | assignment / capstone | 不能单独证明开放式 LLM 真实质量或安全性 | qualify |

## High-Risk Claim Gates

| Gate | 覆盖 claim | 通过标准 |
|------|------------|----------|
| optimality_gate | CH01-C01、CH02-C01、CH05-C01 | 不使用“最优”“保证”“必然”等未限定表述 |
| formula_gate | CH02-C02、CH03-C01、CH03-C02、CH05-C02、CH07-C01 | 公式和 shape 有作业测试、书面题或推导脚本支撑 |
| systems_gate | CH04-C01、CH06-C02、CH07-C02、CH10-C01、CH10-C02 | 性能、成本和显存 claim 必须带配置、硬件或实现边界 |
| frontier_gate | CH04-C02、CH07-C02、CH10-C03 | 前沿模型卡 claim 只写成“报告值/案例”，不作为稳定定理 |
| evaluation_gate | CH08-C01、CH08-C02、CH09-C02、CH11-C01、CH11-C02 | 指标和算法 claim 必须说明适用条件和不支持的更强结论 |

## Maintenance Workflow

1. 新增或重写章节小节时，先在 [Chapter Source and Accuracy Map](chapter-source-map.md) 找到对应核心结论。
2. 若 claim 会进入作业、quiz、hidden test、项目 rubric 或标准答案，必须在本台账新增 `Claim ID`。
3. 若 claim 是可评分公式、复杂度、显存、优化目标或指标推导，必须同步 [Mathematical Derivation Audit](mathematical-derivation-audit.md) 的 `DER-xx` 条目。
4. 若 claim 涉及前沿模型、benchmark、API、价格、上下文长度、性能或显存数字，必须同步 [前沿模型来源等级与复核记录](frontier-source-audit.md) 或 [External Source Verification Guide](external-source-verification.md)。
5. 如果来源只支持案例或动机，`Action` 必须是 `qualify`、`downgrade`、`remove` 或 `replace`，不能直接 `keep`。
6. 每轮发布前运行 `.venv/bin/python verify_course.py`；涉及 capstone 或训练工程时运行 `.venv/bin/python verify_course.py --capstone --training`。

## 发布前 Checklist

- 每个 Ch01-Ch10 和 Ch11 至少有两个 audited claim。
- 每条 claim 都有 source level、student-facing use、boundary 和 action。
- 至少覆盖 stable theory、implementation、frontier model card、benchmark 和 course inference 五类。
- `downgrade` 的 claim 不进入作业或考试事实。
- 本台账、mathematical derivation audit、source map、claim worksheet、source inventory 和 frontier audit 互相链接。
