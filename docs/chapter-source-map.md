# Chapter Source and Accuracy Map

本文档把每章的核心知识点映射到权威来源、课程内验证证据和常见误讲边界。它用于教师备课、助教答疑、内容改版和前沿事实复核；课程内术语定义见 [Core Concept Glossary](core-concept-glossary.md)，阅读安排仍以 [逐周阅读清单与复盘 Handout](reading-list.md) 为准，阅读讨论、paper-to-code drill 和 source-boundary 问题见 [Reading Discussion Question Bank](reading-discussion-question-bank.md)，核心论文到章节、推导、作业测试和项目证据的横向映射见 [Paper-to-Code Traceability Matrix](paper-to-code-traceability-matrix.md)，符号、shape、mask 和 metric 单位按 [Notation and Shape Glossary](notation-shape-glossary.md) 统一，外部链接和易变来源先按 [External Source Inventory](external-source-inventory.md) 分层，模型卡、API 文档、leaderboard 和 benchmark claim 按 [Model and Benchmark Card Guide](model-benchmark-card-guide.md) 填卡，再按 [External Source Verification Guide](external-source-verification.md) 复核。逐条改稿时使用 [Claim Audit Worksheet](claim-audit-worksheet.md) 记录 claim、来源、边界和处理动作；当前已审计 claim 见 [Chapter Claim Audit Ledger](chapter-claim-audit-ledger.md)；学生或 staff 报告的内容错误、修订、公告和验证闭环见 [Course Errata and Correction Ledger](course-errata-correction-ledger.md)。

## 使用规则

- 基础理论优先引用论文、教材、课程官网或官方文档。
- 前沿模型规格只能写成“论文/模型卡/官方文档报告”，不能写成普遍事实。
- 若正文、作业或项目使用具体 benchmark 数字，必须能在来源中定位任务、日期、评测设置和版本。
- 若来源只支持“动机”或“案例”，不得把它升级成算法定理。
- 每次修改章节后，至少运行 `.venv/bin/python verify_course.py`；涉及 capstone 或训练代码时运行 `.venv/bin/python verify_course.py --capstone --training`。

## Ch01 Tokenization / BPE

| 核心结论 | 主要来源 | 课程验证证据 | 常见边界 |
|----------|----------|--------------|----------|
| BPE 通过高频相邻符号 merge 缓解 OOV，但不是语义最优分词 | Sennrich et al., Neural Machine Translation of Rare Words with Subword Units | `assignments/ch01_bpe/tests.py` 检查 merge、round trip 和 vocab 连续性 | 不要声称 BPE 直接学习语义边界 |
| byte-level tokenizer 能降低未知字符风险，但可能增加序列长度 | GPT-2 tokenizer 设计说明、Hugging Face tokenizers 文档 | Ch01 作业要求 ASCII/CJK round trip | 不要把 vocab size 与上下文长度混为一谈 |
| tokenizer 是 LLM 成本和上下文利用率的一部分 | GPT-2、tiktoken/tokenizers 工程文档 | Ch01 练习和 README 岗位能力矩阵 | 成本估算需要结合模型、服务和计费单位 |

## Ch02 Embedding / Position Encoding / RoPE

| 核心结论 | 主要来源 | 课程验证证据 | 常见边界 |
|----------|----------|--------------|----------|
| word2vec/GloVe 类比现象是向量空间经验结构，不是训练目标的数学保证 | Mikolov et al.; Pennington et al.; CS224N word vectors material | Ch02 书面题要求区分训练目标与类比现象 | 不要写成“语义关系必然被线性编码” |
| sinusoidal position encoding 提供确定性位置特征 | Vaswani et al., Attention Is All You Need | `assignments/ch02_embeddings/tests.py` 检查位置 0 和频率项 | 不要把 sinusoidal encoding 说成 learned absolute embedding |
| RoPE 通过成对旋转让点积依赖相对位移 | RoFormer / RoPE paper | Ch02 测试检查 `R_m^T R_n = R_{n-m}` 性质和 norm preservation | 长上下文外推仍受训练分布、频率和数值范围限制 |

## Ch03 Scaled Dot-Product Attention

| 核心结论 | 主要来源 | 课程验证证据 | 常见边界 |
|----------|----------|--------------|----------|
| score 除以 `sqrt(d_k)` 是为了控制点积方差和 softmax 饱和 | Vaswani et al.; Deep Learning 教材中的方差传播 | 书面题和 `assignments/ch03_attention/tests.py` 手算 attention | 不要只给口号，需说明 shape 和方差假设 |
| causal mask 应在 softmax 前应用 | Transformer decoder attention 定义 | Ch03 测试检查未来 token 被屏蔽 | softmax 后乘 mask 且不重归一会改变概率分布 |
| attention 权重可解释性有限 | attention visualization 相关讨论和课程讲义 | Ch03 热力图练习只作为诊断工具 | 不要把单个 attention head 直接解释成完整模型理由 |

## Ch04 MHA / GQA / MLA

| 核心结论 | 主要来源 | 课程验证证据 | 常见边界 |
|----------|----------|--------------|----------|
| Multi-head attention 用多个子空间并行建模关系 | Vaswani et al. | Ch04 tests 检查投影形状、mask 和归一化 | head 数增加不必然提升质量 |
| GQA/MQA 通过减少 KV head 降低推理 KV cache | Ainslie et al., GQA | Ch04 tests 检查 KV 参数和 cache 比例 | 节省 cache 可能带来表达能力或质量折衷 |
| MLA 作为 DeepSeek-V2/V3 报告中的 KV 压缩方案 | DeepSeek-V2/V3 technical reports | Ch04 简化 MLA 作业检查 latent cache | 简化实现不是完整生产 MLA，不应用它推出论文级性能；RoPE 旋转是位置相关线性正交变换，不要误讲成非线性 |

## Ch05 Transformer Block / Norm / FFN

| 核心结论 | 主要来源 | 课程验证证据 | 常见边界 |
|----------|----------|--------------|----------|
| Pre-norm block 更利于深层 Transformer 训练稳定 | Transformer/LayerNorm 相关论文和实践文档 | Ch05 tests 检查 pre-norm 组件与梯度流 | 不要把 pre-norm 写成唯一正确结构 |
| LayerNorm 对最后一维归一化；RMSNorm 不中心化 | Ba et al. LayerNorm; Zhang and Sennrich RMSNorm | gradcheck 和 PyTorch 对齐测试 | backward 推导需包含 mean/variance 依赖 |
| FFN/SwiGLU 是 token-wise 非线性容量来源 | Transformer FFN; GLU variants paper | Ch05 tests 检查宽度、shape 和参数量 | FFN 不是 attention 的替代品，两者负责不同计算 |

## Ch06 GPT Assembly / MoE

| 核心结论 | 主要来源 | 课程验证证据 | 常见边界 |
|----------|----------|--------------|----------|
| decoder-only LM 用右移标签做 next-token prediction | GPT-2 report; Transformer decoder 定义 | Ch06 tests 检查 causal attention、forward shape 和 weight tying | 不要把 encoder-only MLM 目标混入 GPT 训练目标 |
| GPT-2 small 默认配置可作为教学规模参照 | GPT-2 report / implementation configs | Ch06 tests 检查默认配置和参数量 | 参数量取决于 vocab、tie weights 和实现细节 |
| MoE routing 需要 capacity、负载均衡和稳定性处理 | Switch Transformer; DeepSeek-V3 report | Ch06 tests 检查 router top-k 和 bias balancing | “激活参数少”不等于训练/服务成本线性降低 |

## Ch07 Training Loop

| 核心结论 | 主要来源 | 课程验证证据 | 常见边界 |
|----------|----------|--------------|----------|
| Cross entropy 是 next-token LM 的核心损失 | Deep Learning 教材；PyTorch `cross_entropy` 文档 | Ch07 tests 对齐 PyTorch CE | ignore index 必须在 gather 前处理 |
| AdamW 是 decoupled weight decay，不等同于 Adam 里的 L2 penalty | Loshchilov and Hutter, AdamW | Ch07 tests 手算单步更新 | weight decay、lr schedule 和 grad clipping 要分开解释 |
| 训练报告需要数据审计、日志、checkpoint/resume 和成本估算 | CS224N final project 实践；PyTorch/工程文档 | training capstone acceptance | 小模型 CPU 验收不代表大模型训练可直接外推 |
| FP8/FP4、DualPipe 和 Muon 属于前沿训练系统案例 | DeepSeek 技术报告/模型卡；优化器与低精度训练文献 | Ch07 正文和 compute guide 要求记录硬件、dtype、成本和 fallback | 不要把报告中的吞吐、显存或 bubble 数字外推成所有硬件的固定收益 |

## Ch08 Generation / Decoding

| 核心结论 | 主要来源 | 课程验证证据 | 常见边界 |
|----------|----------|--------------|----------|
| temperature、top-k、top-p 分别改变采样分布形状和候选集合 | Holtzman et al.; generation docs | Ch08 tests 检查 top-k/top-p 和非法参数 | top-p 应保留达到累计概率阈值的最小 nucleus |
| TTFT、TPOT、TPS 受模型、上下文、并发、排队、网络和 serving engine 共同影响 | serving framework docs; systems benchmark practice | inference capstone benchmark/SLO 要求学生实测 | 不要把某个产品或某次 benchmark 的延迟数字写成通用事实 |
| speculative decoding 通过 draft/target 验证减少目标模型调用成本 | Leviathan et al.; blockwise decoding | Ch08 tests 检查预算和统计输出 | draft 质量差或系统瓶颈不在 decode 时，加速会有限 |
| distinct n-gram 等多样性指标只能诊断局部退化 | text generation evaluation 文献 | Ch08 generator 测试 | 不能用单一多样性指标替代人工质量评估 |
| structured output / constrained decoding 能提高格式稳定性 | OpenAI/Outlines/vLLM/SGLang/llama.cpp 等官方文档 | Ch08 约束解码讲解与推理 capstone JSON 回归 | 即使服务端支持结构化输出，应用侧仍应做 schema 校验 |

## Ch09 Fine-tuning / Alignment

| 核心结论 | 主要来源 | 课程验证证据 | 常见边界 |
|----------|----------|--------------|----------|
| SFT 需要 mask prompt/padding，只在回答 token 上训练 | instruction tuning/RLHF 实践文档 | Ch09 tests 检查 label mask 和 loss | 把 prompt token 计入 loss 会改变训练目标 |
| LoRA 用低秩增量减少可训练参数 | Hu et al., LoRA | Ch09 tests 检查 apply/merge 和 trainable count | rank、target module 和 scaling 会影响质量与稳定性 |
| DPO 使用 chosen/rejected log-ratio 和 reference model | Rafailov et al., DPO | Ch09 tests 检查 preference 方向 | chosen/rejected 方向写反会优化相反目标 |
| GRPO 是 DeepSeek-R1 报告中的 group-relative 强化学习方案 | DeepSeek-R1 paper / Nature entry | Ch09 tests 检查 group whitening | 不要把 GRPO 描述成完整安全对齐方案 |

## Ch10 Inference / RAG / Serving

| 核心结论 | 主要来源 | 课程验证证据 | 常见边界 |
|----------|----------|--------------|----------|
| KV cache 显存与 batch、layer、seq_len、KV head、head_dim 和 dtype 相关 | Transformer serving papers; vLLM/PagedAttention | Ch10 tests 检查 batch 和 K/V 两份 | 不要把权重显存当成 KV cache 显存 |
| RAG 需要同时评估检索质量和生成质量 | Lewis et al., RAG; retrieval evaluation literature | Ch10 tests 检查 retrieval 和 prompt construction | 命中相似文档不代表答案事实正确 |
| serving 指标应包含 latency、TTFT、TPOT、tokens/s、错误率和容量规划 | vLLM/SGLang/TensorRT-LLM docs; systems papers | inference capstone acceptance 和 benchmark | 平均延迟不足以支撑 SLO，需要 P95/P99 |
| 推理引擎 benchmark 只在给定模型、硬件、context、batching 和 workload 下成立 | vLLM/SGLang/TensorRT-LLM docs; benchmark reports | capstone 要求输出固定配置和机器可读报告 | 不要把 vLLM/PagedAttention 的示例吞吐或显存利用率写成无条件承诺 |
| 量化降低显存和带宽压力，但可能影响质量、吞吐和兼容性 | QLoRA / quantization 文献与框架文档 | Ch10 int8 roundtrip 作业 | 教学 int8 例子不能代表所有生产量化策略 |

## 经典 NLP 与评测专题

| 核心结论 | 主要来源 | 课程验证证据 | 常见边界 |
|----------|----------|--------------|----------|
| dependency parsing、seq2seq/NMT、BERT 是神经 NLP 主线的一部分 | CS224N schedule; Jurafsky and Martin; Chen and Manning; Sutskever et al.; Devlin et al. | `docs/classic-nlp-handout.md` 与 `assignments/ch11_classic_nlp/tests.py` | 它们作为专题覆盖，不等同于 10 章 decoder-only 主线 |
| BLEU/ROUGE/EM/F1 各有任务假设和局限 | BLEU、ROUGE、SQuAD evaluation 文献 | Ch11 tests 检查 BLEU、ROUGE-L、EM/F1 | 不能用这些指标单独证明开放式 LLM 的真实质量 |
| ethics/safety 评估需要来源、场景和失败案例 | Foundation model risk reports; course policies | reading review 与 project peer review | 不要用抽象“安全”替代可审查的风险类别 |

## 维护检查清单

每次修改章节正文、作业或 capstone 时：

1. 对照 [External Source Inventory](external-source-inventory.md) 确认来源层级，再对照本表确认该知识点至少有一个 A/B 级来源。
2. 在 [Claim Audit Worksheet](claim-audit-worksheet.md) 中记录高风险 claim、来源、边界、学生用途和处理动作，并把进入作业、quiz、项目 rubric 或标准答案的 claim 加入 [Chapter Claim Audit Ledger](chapter-claim-audit-ledger.md)。
3. 检查是否需要在 [书面推导与概念题题库](written-problem-set.md) 或作业测试中增加证据。
4. 若涉及 DeepSeek、新模型、API、benchmark 或价格，更新 [前沿模型来源等级与复核记录](frontier-source-audit.md)。
5. 若涉及外部链接、模型卡、API 文档、benchmark 或价格，按 [External Source Verification Guide](external-source-verification.md) 记录访问日期、来源类型和处理动作。
6. 运行 `.venv/bin/python verify_course.py`。
7. 若涉及训练或推理工程，运行 `.venv/bin/python verify_course.py --capstone --training`。
