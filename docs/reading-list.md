# 逐周阅读材料与复盘 Handout

本 handout 把 10 周课程的阅读材料按章节任务组织起来。它不是独立补课路径；每篇阅读都必须回到章节代码、书面题或 capstone 决策中。阅读分为三类：

- 必读：课堂讨论和作业默认依赖。
- 选读：用于项目、报告或加深理解。
- 课程连接：用于把阅读中的目标函数、架构细节或实验设计落到本课程代码。

每次阅读后重点回答三个问题：这篇材料解决什么技术问题，核心方法如何写成公式或算法步骤，和本课程哪一章的代码、书面题或系统设计直接相关。

## 阅读方法：从论文到课程能力

本课程不要求学生记住论文列表，而要求把论文中的技术选择转成可推导、可实现、可评测的能力。阅读每篇材料时，应至少完成四步：

1. 问题设定：写出输入、输出、训练数据、模型假设和目标任务。
2. 数学对象：定位一个目标函数、概率分解、矩阵运算、mask 规则、复杂度公式或评测指标，并解释每个变量。
3. 代码落点：指出它对应本课程中的哪个函数、张量 shape、测试用例或 capstone 系统组件。
4. 结论边界：说明实验结论依赖的数据、规模、指标、硬件、prompt、解码策略或人工标注假设。

阅读深度按三层递进：

| 层级 | 学生应能做到 | 例子 |
|------|--------------|------|
| 概念层 | 用自己的话复述问题、方法、结果和限制 | BPE 为什么缓解 OOV；DPO 为什么需要 reference model |
| 数学层 | 展开关键公式并完成一个小数值例子 | SGNS loss、attention scaling、next-token CE、DPO log-ratio |
| 系统层 | 把论文方法连接到资源、延迟、质量或安全取舍 | GQA 的 KV cache、PagedAttention 的显存分页、RAG 的检索/生成双指标 |

## Week 0: 章节内置先修诊断

对应材料：Prerequisite Diagnostic、[数学与 PyTorch 先修复习](math-prerequisites.md)、[ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md)。

本周阅读目标：确认学生能把基础 ML 语言转成 LLM 课程中反复使用的对象，包括 loss、gradient、generalization、held-out evaluation、tensor shape 和 PyTorch module。若诊断暴露短板，直接回到相关章节的“先修能力/本章内化/验收信号”补强，而不是另走一条独立课程。

必读：

- 本课程 [ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md)：重点看 calculus、probability/statistics、ML objectives、generalization 和 evaluation 如何进入 Ch07-Ch11 的训练、评测和上线结论。
- Goodfellow, Bengio, Courville. [Deep Learning](https://www.deeplearningbook.org/), optimization 和 ML basics 相关章节。
- 本课程 [数学与 PyTorch 先修复习](math-prerequisites.md)：重点确认 Python、PyTorch、calculus、linear algebra、probability/statistics 和 ML foundations 在 Ch01-Ch06 的 shape、mask、loss 和梯度实现中如何出现。

复盘问题：

- 训练目标、验证指标和最终项目结论之间是什么关系？
- 一个 benchmark 或 hidden test 结果在什么条件下不能推广？
- 为什么 cross entropy 可以作为概率模型的负对数似然？它和 accuracy/F1 的关系是什么？
- PyTorch 中 shape 正确但语义错误的实现通常会在哪些地方出现？

## 阅读重点

- 核心结论：用自己的话说明论文或文档解决的问题、方法和结论。
- 技术细节：至少解释一个公式、结构图、算法步骤或实验设置。
- 代码连接：明确指出对应章节代码、作业函数或 capstone 模块。
- 边界条件：写出一个失败模式、反例或适用范围。
- 延伸问题：提出一个可在课堂讨论或作业中继续追问的问题。

## Week 1: Tokenization 与 Word Vectors

对应章节：Ch01-Ch02。

本周阅读目标：理解从离散文本到连续向量的两条路线：子词 tokenization 解决符号覆盖和压缩问题，word vectors 用分布式语义把共现关系投影到向量空间。

必读：

- Sennrich, Haddow, Birch. [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909). 重点看 BPE 如何缓解 OOV。
- Mikolov et al. [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781). 重点看 skip-gram 目标。
- Pennington, Socher, Manning. [GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/pubs/glove.pdf). 重点看共现矩阵与加权最小二乘目标。

选读：

- 本课程 Ch02 的 word vectors 与 embedding 相关小节。
- Jurafsky and Martin, Speech and Language Processing, word embeddings 相关章节。

复盘问题：

- BPE merge 规则为什么是贪心的？它在哪些语料上会产生不符合语义直觉的 token？
- skip-gram 的窗口共现样本如何变成 positive/negative 二分类目标？
- word2vec 的类比现象是训练目标直接保证的吗？还是空间结构中的经验现象？
- SGNS、PMI 和 GloVe 都在利用共现统计，它们的归一化和权重处理有什么不同？
- token 粒度如何影响 context length、embedding 参数量、训练 token budget 和推理成本？

## Week 2: Attention 与 Tensor Derivatives

对应章节：Ch03 与数学先修复习。

本周阅读目标：把 Transformer 的 attention 写成完整张量计算，并能解释 scaling、mask、softmax、weighted sum 和反向传播中的每个维度。

必读：

- Vaswani et al. [Attention Is All You Need](https://arxiv.org/abs/1706.03762). 重点看 scaled dot-product attention、mask 和 multi-head 结构。
- 本课程 Ch03 attention 作业与书面题：重点看 neural network foundations、tensor derivatives 和 masked attention。

选读：

- Goodfellow, Bengio, Courville. [Deep Learning](https://www.deeplearningbook.org/), optimization 和 backpropagation 相关章节。
- The Matrix Cookbook 中 softmax/cross entropy 与矩阵求导条目。

复盘问题：

- 为什么 attention score 要除以 `sqrt(d_k)`？
- causal mask 的加法实现为什么通常使用一个很大的负数，而不是直接乘 0？
- padding mask 和 causal mask 分别约束 query 还是 key？合成后 shape 应该如何广播？
- attention 权重能否直接作为模型解释？它最多支持哪类诊断结论？

## Week 3: Multi-Head Attention、GQA、MLA 与 Block

对应章节：Ch04-Ch05。

本周阅读目标：从标准 multi-head attention 扩展到 GQA、MLA、norm、FFN 和完整 block，理解现代 LLM 架构如何围绕显存、吞吐、训练稳定性和表达能力做取舍。

必读：

- Vaswani et al. [Attention Is All You Need](https://arxiv.org/abs/1706.03762). 复读 multi-head attention 与 positional encoding。
- Ainslie et al. [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](https://arxiv.org/abs/2305.13245). 重点看 KV head 数与推理效率。
- DeepSeek-AI. [DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model](https://arxiv.org/abs/2405.04434). 重点看 MLA 的 KV cache 压缩动机。

选读：

- Zhang and Sennrich. [Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467).
- Shazeer. [GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202).
- Geva et al. [Transformer Feed-Forward Layers Are Key-Value Memories](https://arxiv.org/abs/2012.14913). 重点看 FFN neuron 的键值存储解释。
- Meng et al. [Locating and Editing Factual Associations in GPT](https://arxiv.org/abs/2202.05262). 重点看 causal tracing、activation patching 和模型编辑边界。

复盘问题：

- GQA 节省 KV cache 的同时损失了什么表达能力？
- MLA 的 latent cache 与 RoPE 解耦为什么会改变工程实现？
- Probing、activation patching 和 ablation 分别能支持什么结论，不能支持什么结论？
- Pre-Norm、RMSNorm、SwiGLU 和 residual path 分别解决训练中的哪类数值或优化问题？
- 只看参数量为什么不足以预测训练显存和推理显存？

## Week 4: GPT 组装、预训练目标与 MoE

对应章节：Ch06。

本周阅读目标：把 decoder-only LM 的概率分解、PyTorch forward、label shift、LM head 和 MoE 稀疏激活组织成一个完整模型。

必读：

- Radford et al. [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf). 重点看 GPT-2 的 decoder-only 预训练范式。
- Fedus, Zoph, Shazeer. [Switch Transformers](https://arxiv.org/abs/2101.03961). 重点看 top-1 routing、capacity 和 load balancing。
- DeepSeek-AI. [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437). 重点看 DeepSeekMoE 与 auxiliary-loss-free load balancing。

选读：

- Brown et al. [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165).
- Hugging Face Transformers GPT-2 model documentation。

复盘问题：

- decoder-only LM 的训练标签为什么是右移一位？
- MoE 的 capacity factor 太低或太高分别会造成什么问题？
- tied embedding、final norm、position encoding 和 causal mask 分别在 GPT forward 中处于什么位置？
- MoE 的“总参数量”和“每 token 激活参数量”为什么必须分开报告？

## Week 5: Training Loop、Scaling 与 Distributed Training

对应章节：Ch07。

本周阅读目标：从单步 loss 进入训练系统，理解数据策展、optimizer、scheduler、mixed precision、checkpoint、scaling law 和 distributed memory sharding 如何共同决定可训练规模。

必读：

- Loshchilov and Hutter. [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101). 重点看 AdamW 与 L2 正则的差别。
- Hoffmann et al. [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556). 重点看 Chinchilla scaling law 的数据/参数权衡。
- Li et al. [DataComp-LM: In search of the next generation of training sets for language models](https://arxiv.org/abs/2406.11794). 重点看 data curation strategies：deduplication、filtering、data mixing 和多尺度评估。
- Penedo et al. [The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale](https://arxiv.org/abs/2406.17557). 重点看 pretraining data 的 filtering、deduplication、ablation 和 FineWeb-Edu 的教育文本过滤。
- Rajbhandari et al. [ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](https://arxiv.org/abs/1910.02054). 重点看 optimizer/gradient/parameter state sharding。
- Shoeybi et al. [Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism](https://arxiv.org/abs/1909.08053). 重点看 tensor parallelism 如何切分 Transformer 层内矩阵。
- Jiang et al. [MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs](https://arxiv.org/abs/2402.15627). 重点看大规模训练中的 full-stack observability、straggler 诊断、容错和 MFU，而不是只记住 GPU 数。

选读：

- Huang et al. [GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism](https://arxiv.org/abs/1811.06965). 重点看 micro-batch、pipeline bubble 和 activation rematerialization。
- PyTorch documentation: `torch.amp`, `DistributedDataParallel`, [FSDP2](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html)、[DTensor](https://docs.pytorch.org/docs/stable/distributed.tensor.html) 和 [Distributed Checkpoint](https://docs.pytorch.org/docs/stable/distributed.checkpoint.html)。重点看 FSDP2 如何用 DTensor 风格分片参数、梯度和 optimizer state，DCP 如何做多 rank checkpoint 与 load-time resharding，以及 resume parity 如何验证。
- PyTorch [TorchTitan checkpoint guide](https://github.com/pytorch/torchtitan/blob/main/docs/checkpoint.md)。重点看 model-only save 与完整训练状态保存的差异，以及 checkpoint interval/async/keep-latest 这类工程参数如何进入训练可靠性。
- NVIDIA Transformer Engine documentation on [FP8/MXFP8/NVFP4](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/index.html)。重点看低精度训练不仅是 dtype 选择，还包括 scaling、amax history、kernel 支持和 checkpoint state。
- NVIDIA Megatron Core parallelism guide。重点看 DP、TP、PP、CP、EP 和 sequence parallelism 分别切什么维度，什么时候组合。
- DeepSeek-V3 Technical Report 中 FP8 mixed precision、DualPipe、MLA/MoE 和 MTP。重点看这些设计如何共同服务训练效率和稳定性。
- Meta. [The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783). 重点看 pre-training data cleaning、deduplication、PII/adult-content filtering 和 contamination analysis 如何影响评测解释。
- Jordan et al. [Muon is Scalable for LLM Training](https://arxiv.org/abs/2502.16982)。重点看 Muon 从小模型实验扩展到 LLM 时需要 weight decay 和 update scale，不能只背“正交化”口号。
- NVIDIA / PyTorch profiler 文档中 GPU utilization、kernel timeline、communication overlap 和 dataloader bottleneck 的诊断方法。

复盘问题：

- AdamW 的 weight decay 为什么不能简单等同于 Adam 里的 L2 penalty？
- 在固定算力下，为什么“更大的模型”不一定比“较小模型 + 更多训练 token”更合理？
- `training_data_curation_report` 的 size、dedup、quality、eval contamination、domain mixture 和 privacy gate 分别阻止哪类错误训练结论？
- 训练日志里 loss 下降但开发集变差时，应该先查哪些产出？
- 参数、梯度、optimizer state、activation 和 communication buffer 分别如何进入显存预算？
- DDP、ZeRO/FSDP、tensor parallel 和 pipeline parallel 分别解决容量、通信还是吞吐中的哪一类瓶颈？
- `distributed_training_strategy_report` 中每卡模型状态、global batch tokens、MFU 和 action item 分别对应训练系统的哪个风险？
- `checkpoint_resume_integrity_report` 中 state completeness、write integrity、distributed reshard、interval 和 overhead gate 分别阻止哪类恢复失败？
- MFU 低时，如何区分 batch 太小、通信等待、数据加载不足、checkpoint 写盘和 kernel 未融合？
- FP8/MXFP8 带来吞吐收益时，为什么仍要单独检查 loss spike、scale/amax history、梯度范围和 checkpoint resume？
- 一次训练 run 的 optimization、throughput、state/checkpoint 和 evaluation gate 分别需要哪些最低证据？
- FSDP2 / Distributed Checkpoint / Megatron Core 这类工具解决的是课程 tiny train 中哪一个被简化掉的问题？
- 为什么 model-only export 不能替代可恢复训练 checkpoint？FSDP/ZeRO 下为什么还要检查 sharded/DCP 格式和 shard metadata？
- Chinchilla scaling law 的结论在数据质量、token 重复率或领域迁移变化时有什么边界？

## Week 6: Generation、Search 与 Speculative Decoding

对应章节：Ch08。

本周阅读目标：把同一个 next-token 分布转成不同解码行为，理解 greedy、sampling、beam、self-consistency、constrained decoding 和 speculative decoding 的质量/成本关系。

必读：

- Holtzman et al. [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751). 重点看 nucleus sampling。
- Leviathan, Kalman, Matias. [Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192). 重点看 draft/target 接受机制。
- Stern et al. [Blockwise Parallel Decoding for Deep Autoregressive Models](https://arxiv.org/abs/1811.03115). 重点看一次预测多个 token 的动机。
- Wei et al. [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903). 重点看中间推理 token 如何改变任务成功率。
- Wang et al. [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171). 重点看多路径采样与投票。
- Snell et al. [Scaling LLM Test-Time Compute Optimally Can be More Effective than Scaling Model Parameters](https://arxiv.org/abs/2408.03314). 重点看 verifier search、test-time compute 与边际收益，不要把多采样等同于免费提升。

选读：

- Hugging Face Transformers generation strategies documentation。
- DeepSeek-V3 Technical Report 中 multi-token prediction。
- OpenAI. [Learning to reason with LLMs](https://openai.com/index/learning-to-reason-with-llms/). 重点看 train-time compute 与 test-time compute 的区别，以及为什么 reasoning 模型的系统指标要单独报告。

复盘问题：

- top-k、top-p、temperature 分别控制分布的哪个性质？
- speculative decoding 在什么情况下不能带来明显加速？
- self-consistency 或 best-of-N 的准确率提升应如何同时报告 token 成本和延迟？
- `test_time_compute_budget_report` 的 quality、token、latency、cost 和 efficiency gate 分别阻止哪类错误上线结论？
- constrained decoding 是改变模型参数、logits、token mask 还是后处理？不同实现的失败模式是什么？
- test-time compute 提高准确率时，应该同时报告哪些系统指标？

## Week 7: SFT、LoRA、DPO、GRPO 与 RLVR/RFT

对应章节：Ch09。

本周阅读目标：区分 SFT、parameter-efficient fine-tuning、合成数据/蒸馏、reward modeling、DPO、GRPO 和 RLVR/RFT 的训练信号，理解偏好数据、AI/人工反馈、安全切片、rejection sampling 和可验证 reward 如何进入目标函数。

必读：

- Hugging Face. [Chat templates](https://huggingface.co/docs/transformers/chat_templating). 重点看 role/message 如何被序列化成模型真实输入，以及为什么训练和推理必须使用一致模板。
- Hugging Face TRL. [SFT Trainer](https://huggingface.co/docs/trl/sft_trainer). 重点看 assistant/completion-only loss、packing 和训练数据格式如何影响 SFT label mask。
- OpenAI. [Fine-tuning guide](https://platform.openai.com/docs/guides/fine-tuning). 重点看 chat 格式训练样本、训练/验证切分和生产微调数据协议。
- Hu et al. [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685). 重点看低秩增量和可训练参数比例。
- Bai et al. [Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback](https://arxiv.org/abs/2204.05862). 重点看 chosen/rejected 偏好数据、helpful/harmless 目标和在线反馈数据迭代。
- Rafailov et al. [Direct Preference Optimization](https://arxiv.org/abs/2305.18290). 重点看从 KL-constrained RL 到分类式 loss 的推导。
- DeepSeek-AI. [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948). 重点看 GRPO、冷启动数据、rejection sampling、蒸馏模型和方法边界。
- Kimi Team. [Kimi k1.5: Scaling Reinforcement Learning with LLMs](https://arxiv.org/abs/2501.12599). 重点看 long-context RL、long2short、长度控制、采样策略和多模态 reasoning 的工程取舍。
- Yu et al. [DAPO: An Open-Source LLM Reinforcement Learning System at Scale](https://arxiv.org/abs/2503.14476). 重点看 dynamic sampling、decoupled clipping、token-level policy gradient loss、overlong reward shaping 和开源 RL recipe 如何服务可复现训练。
- Zheng et al. [Group Sequence Policy Optimization](https://arxiv.org/abs/2507.18071). 重点看 sequence-level importance ratio、length normalization、MoE RL 稳定性和为什么 token-level ratio 噪声会影响长训练。

选读：

- Ouyang et al. [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155).
- Bai et al. [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073). 重点看 AI feedback 如何生成 harmlessness preference data，以及为什么仍要审计数据混合和安全边界。
- Meta. [The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783). 重点看 post-training 数据、rejection sampling、reward model、human annotation、安全数据和评测切片如何共同支撑发布结论。
- OpenAI. [Learning to reason with LLMs](https://openai.com/index/learning-to-reason-with-llms/) 与 [Reinforcement fine-tuning guide](https://developers.openai.com/api/docs/guides/reinforcement-fine-tuning)。重点看 train-time/test-time compute、programmable grader、validation split 和 grader 适用条件。

复盘问题：

- DPO 为什么需要 reference model？`beta` 调大或调小会怎样？
- SFT 数据从 messages 变成 token 序列后，哪些信息必须保留下来才能检查 assistant-only loss、truncation 和 packing 边界？
- 合成/蒸馏数据进入 SFT 或偏好优化前，为什么必须记录 teacher 版本、采样参数、verifier 准确性、人工抽检、去重和 eval overlap？
- 偏好数据中的长度偏差、风格偏差或标注者分歧会怎样进入 DPO/RLHF 的目标函数？
- `post_training_data_audit` 的 coverage、label quality、leakage 和 safety gate 分别对应 post-training 的哪类失败结论？
- 如果 SFT/偏好数据的任务覆盖不足或 eval overlap 不为零，为什么不能用 DPO/GRPO 训练 loss 下降作为上线证据？
- GRPO 的组内 advantage 白化依赖什么采样假设？
- DAPO/GSPO 式 reasoning RL 报告为什么必须同时看 rollout 命中率、completion length、entropy、clip fraction、sequence ratio 和 held-out prompt 切片？
- RLVR/RFT 的 grader 为什么需要 pass-rate、reward variance、completion length 和 hacking signal 四类检查？
- LoRA 的低秩增量限制了哪些更新方向？它节省的是训练参数、optimizer state 还是前向激活？
- 对齐后模型质量上升但能力回退时，应如何区分数据分布、KL 约束和评测指标的问题？

## Week 8: Inference Engineering、RAG、Quantization 与 Serving

对应章节：Ch10 与推理工程 capstone。

本周阅读目标：把模型输出接入真实服务，理解 KV cache、continuous batching、paged memory、FlashAttention、quantization、RAG、speculative decoding 和多模态输入如何共同影响延迟、吞吐、成本和质量。

必读：

- Kwon et al. [Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180). 重点看 KV cache 分页。
- Dao et al. [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135). 重点看 IO-aware attention。
- Lewis et al. [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401). 重点看 retriever/generator 组合。
- Dettmers et al. [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314). 重点看 4-bit quantization 与 LoRA 结合。
- Yu et al. [Orca: A Distributed Serving System for Transformer-Based Generative Models](https://www.usenix.org/conference/osdi22/presentation/yu). 重点看 iteration-level scheduling 和 continuous batching 为什么能减少队列浪费。
- vLLM documentation: [Optimization and Tuning](https://docs.vllm.ai/en/stable/configuration/optimization/) 与 [serve scheduler arguments](https://docs.vllm.ai/en/stable/cli/serve/). 重点看 `max_num_seqs`、`max_num_batched_tokens`、chunked prefill、KV cache capacity 和 queue/SLO 之间的关系。
- PyTorch and vLLM. [Disaggregated Inference at Scale with PyTorch & vLLM](https://pytorch.org/blog/disaggregated-inference-at-scale-with-pytorch-vllm/). 重点看 prefill/decode 分离如何同时影响 TTFT、TPOT、throughput 和 KV transfer。
- OpenAI. [Function calling](https://developers.openai.com/api/docs/guides/function-calling) 与 [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs). 重点看 function tools、JSON schema、strict structured output 和 tool call output 如何构成服务端协议。
- vLLM. [Structured Outputs](https://docs.vllm.ai/en/latest/features/structured_outputs/) 与 SGLang. [Structured Outputs](https://docs.sglang.ai/advanced_features/structured_outputs.html). 重点看 OpenAI-compatible serving 中的 JSON schema、choice、regex、grammar/EBNF constrained decoding，以及为什么仍要做 parse/schema/retry/safety 回归。
- vLLM. [Quantization](https://docs.vllm.ai/en/latest/features/quantization/) 与 [Quantized KV Cache](https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/). 重点看 FP8/INT8/INT4、weight-only 与 KV cache quantization 分别作用在什么资源上，以及为什么 KV cache 量化要用长上下文质量 gate 验证。
- NVIDIA TensorRT-LLM. [Quantization](https://nvidia.github.io/TensorRT-LLM/latest/features/quantization.html) 与 Transformer Engine [FP8/FP4 primer](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/examples/fp8_primer.html). 重点看 SmoothQuant、AWQ、FP8 KV cache、FP8/FP4 scale metadata、硬件代际和 kernel 支持如何决定真实收益。
- Xiao et al. [SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models](https://arxiv.org/abs/2211.10438)、Frantar et al. [GPTQ](https://arxiv.org/abs/2210.17323)、Lin et al. [AWQ](https://arxiv.org/abs/2306.00978). 重点看 W8A8 激活 outlier、近似二阶 weight quantization 和 activation-aware weight-only quantization 的不同假设。
- Model Context Protocol. [Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) 与 [What is MCP?](https://modelcontextprotocol.io/docs/getting-started/intro). 重点看 host/client/server、resources/prompts/tools、sampling/roots/elicitation、authorization、用户同意、数据隐私和 tool safety。
- Anthropic. [Code execution with MCP: Building more efficient agents](https://www.anthropic.com/engineering/code-execution-with-mcp). 重点看工具定义和中间结果如何消耗上下文，以及为什么大型 agent 系统需要延迟加载工具、执行环境处理和结果摘要。
- Anthropic. [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) 与 Claude Cookbook [Context engineering: memory, compaction, and tool clearing](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools). 重点看 active context、context rot、compaction、tool-result clearing、memory 和为什么 agent/RAG 不能只靠扩大 context window。
- OWASP. [Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) 与 [LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/). 重点看 prompt injection、insecure output handling、insecure plugin design、excessive agency 和外部内容隔离。
- OpenAI. [Production best practices](https://developers.openai.com/api/docs/guides/production-best-practices) 与 [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices). 重点看 prototype 到 production 时的可靠性、监控、评测和成本控制如何进入上线判断。
- Google SRE. [Canarying Releases](https://sre.google/workbook/canarying-releases/) 与 [Implementing SLOs](https://sre.google/workbook/implementing-slos/). 重点看 canary/control、流量分阶段、SLO/SLI 和 error budget 如何转成发布 gate。
- Google SRE. [Handling Overload](https://sre.google/sre-book/handling-overload/) 与 [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/). 重点看 degraded responses、load shedding、动态超时和防止过载级联。
- OpenTelemetry. [Generative AI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) 与 [GenAI attributes](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/). 重点看 model、operation、token usage、finish reason、prompt/completion/tool event 和 trace span 如何变成跨平台遥测字段。
- OpenAI Agents SDK [Tracing](https://openai.github.io/openai-agents-python/tracing/). 重点看 agent run 中 LLM generation、tool calls、handoffs、guardrails 和 custom spans 如何帮助调试生产 workflow。
- Chen, Zaharia, Zou. [FrugalGPT](https://arxiv.org/abs/2305.05176) 与 Ong et al. [RouteLLM](https://arxiv.org/abs/2406.18665). 重点看 LLM cascade、强/弱模型 query routing、成本-质量边界和为什么 router 需要偏好/质量数据验证。
- LiteLLM [Router / Load Balancing](https://docs.litellm.ai/docs/routing) 与 [Fallbacks](https://docs.litellm.ai/docs/proxy/reliability). 重点看 load balancing、cooldowns、timeouts、retries、fallbacks 和 provider/model group 管理如何进入可靠性 gate。
- vLLM documentation: [Production Metrics](https://docs.vllm.ai/en/latest/usage/metrics/) 与 [V1 Metrics design](https://docs.vllm.ai/en/latest/design/v1/metrics.html). 重点看推理引擎的 request/engine metrics 如何服务生产监控、capacity planning 和 incident triage。
- Google Gemini API [Long context](https://ai.google.dev/gemini-api/docs/long-context) 与 Anthropic Claude API [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows). 重点看 1M+ context 带来的产品形态、context rot、context management、token counting 和长上下文并不自动等于稳定召回。
- vLLM [Automatic Prefix Caching](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/) 与 [serve scheduler arguments](https://docs.vllm.ai/en/stable/cli/serve/). 重点看长文档重复查询、prefix cache、chunked prefill、long-prefill scheduling 和 full input sequence length KV admission。

选读：

- vLLM documentation on PagedAttention、continuous batching、prefix caching 和 disaggregated prefilling。
- TensorRT-LLM documentation on [in-flight batching and request scheduling](https://nvidia.github.io/TensorRT-LLM/). 重点看 in-flight batching 如何在 generation loop 中动态加入/退出请求。
- vLLM [Speculative Decoding](https://docs.vllm.ai/en/latest/features/speculative_decoding/) documentation。重点看 medium-to-low QPS、memory-bound workload、draft/EAGLE/MTP/n-gram/suffix 方法选择和 lossless validation 边界。
- SGLang [Speculative Decoding](https://docs.sglang.ai/advanced_features/speculative_decoding.html) documentation。重点看 EAGLE-2/EAGLE-3、MTP、standalone draft model、NGRAM 和 OOM/benchmark 注意事项。
- SGLang v0.4 release note。重点看 zero-overhead batch scheduler、cache-aware load balancer、RadixAttention 和 structured outputs 如何把 CPU 调度、前缀缓存和格式约束揉进 serving engine。
- TensorRT-LLM disaggregated serving 文档。重点看 KV cache exchange、layout conversion、UCX/NIXL、KV transfer 与计算重叠。
- Model Context Protocol tools specification。重点看工具名、metadata、input schema、tool result 与跨服务工具发现如何标准化。
- OpenAI Agents SDK guardrails 与 tracing。重点看 input/output/tool guardrails 在 agent workflow 中运行的不同位置，以及 tracing 如何记录 LLM generation、tool calls、handoffs、guardrail events 和 custom spans。
- Google SRE Book. [Release Engineering](https://sre.google/sre-book/release-engineering/) 与 [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/). 重点看发布工程、回滚、SLO 与业务风险之间的连接。
- llama.cpp 官方文档中 quantization、CPU/GPU offload 和本地部署边界。
- Sarathi-Serve 或 chunked prefill 相关论文/文档：重点看长 prompt prefill 如何影响短请求 TTFT。
- Liu et al. [Visual Instruction Tuning](https://arxiv.org/abs/2304.08485). 重点看 vision encoder、projection 和 LLM instruction tuning 的两阶段流程。
- OpenAI, Anthropic 或 Google DeepMind 的多模态 model card / system card：重点看输入分辨率、任务设置、延迟和安全边界如何描述。

复盘问题：

- TTFT、TPOT、TPS 分别受哪些系统瓶颈影响？
- RAG 评测为什么必须同时看检索质量和生成质量？
- 多模态评估为什么要分开看 VQA、OCR、图表理解和视觉定位？
- 一个 benchmark summary 应怎样限制结论的适用范围？
- prefill 和 decode 阶段的计算/访存瓶颈为什么不同？
- quantization 的误差会优先影响哪些任务、层或 token 分布？
- 为什么 serving admission control 不能只按并发请求数，而要看 active KV tokens、prompt/output token 分布和 SLO 队列？
- 长 prompt 进入 continuous batching 时，chunked prefill 和 prefix cache 分别缓解哪类 TTFT 问题？
- tool/function calling 为什么不能只依赖 prompt 约束？schema、权限和循环预算分别拦截哪类失败？
- 结构化输出上线时，为什么要同时报告 JSON parse rate、schema valid rate、repair retry、fallback/refusal、P95 latency 和 safety violation，而不是只看一次示例输出？
- MCP/remote tool 接入后，为什么还要单独审计 server trust、用户同意、roots/elicitation、敏感数据外发、observation isolation 和 recursive sampling？
- agent trace 为什么要记录 guardrail events、tool spans、context budget 和 side-effect log？这些字段分别帮助定位哪类生产事故？
- context engineering gate 为什么要同时报告 active context、retrieved context、summary、memory、tool observation 和 cleared results 的 token 占比、引用保留、summary fidelity、权限和 P95 TTFT？
- 生产发布时，为什么候选模型即使离线 pass rate 更高，也必须经过 canary/control、per-version quality/safety/SLO/cost monitoring 和 rollback readiness gate？
- 模型路由或级联上线时，为什么平均成本下降不能替代 route branch 的质量、安全、schema、RAG 和高风险任务切片回归？
- 服务运行中 queue backlog、KV cache nearing full、swapped requests、TPOT 变差、timeout 上升和单租户超配额分别指向哪些不同的 overload response？
- prefill/decode 解耦后，为什么必须把 KV transfer、decode queue 和 active KV tokens 单独报告？
- SGLang 的 cache-aware load balancing、vLLM 的 disaggregated prefilling 和 TensorRT-LLM 的 KV transfer overlap 分别在解决哪一层 bottleneck？
- speculative decoding 的 acceptance rate、draft overhead、QPS 和 quality regression 如何共同决定是否启用，而不是只看 `num_speculative_tokens`？
- 长上下文上线时，为什么不能只报告 max context length？`long_context_serving_gate_report` 的 context fit、quality、position robustness 和 serving cost 分别挡住哪类失败？

## Week 9: RNN、经典 NLP、Encoder-only、Evaluation 与 Ethics

对应材料：经典 NLP 专题 Handout、Classic NLP Deep-Dive Teaching Module、书面推导与概念题题库。

本周阅读目标：把现代 LLM 放回 NLP 课程脉络中，理解 RNN/LSTM、dependency parsing、seq2seq、BERT 和传统指标为什么仍然是理解结构预测、表示学习和评测局限的基础。

必读：

- Elman. [Finding Structure in Time](https://crl.ucsd.edu/~elman/Papers/fsit.pdf). 重点看 recurrent hidden state 如何表示前缀。
- Hochreiter and Schmidhuber. [Long Short-Term Memory](https://www.bioinf.jku.at/publications/older/2604.pdf). 重点看 gate 与 cell state 如何缓解长程梯度问题。
- Chen and Manning. [A Fast and Accurate Dependency Parser using Neural Networks](https://aclanthology.org/D14-1082/). 重点看 transition-based parsing。
- Sutskever, Vinyals, Le. [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215). 重点看 encoder-decoder 和 teacher forcing。
- Devlin et al. [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805). 重点看 MLM/NSP 与 encoder-only 表示。
- Bommasani et al. [On the Opportunities and Risks of Foundation Models](https://arxiv.org/abs/2108.07258). 重点看风险分类。

选读：

- Papineni et al. [BLEU: a Method for Automatic Evaluation of Machine Translation](https://aclanthology.org/P02-1040/).
- Lin. [ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/).
- Zheng et al. [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://papers.nips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html). 重点看 position、verbosity、self-enhancement bias 和与人工偏好的一致性验证。
- OpenAI. [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices). 重点看 model graders 需要先和 human labels 验证一致性，再用于优化。

复盘问题：

- RNN 的 BPTT 梯度连乘为什么会导致长程依赖困难？LSTM 改变了哪条路径？
- dependency parsing 与 decoder-only LLM 在结构归纳偏置上有什么差异？
- encoder-decoder cross-attention 和 decoder-only causal self-attention 的 K/V 来源有什么不同？
- BERT MLM labels 中为什么未 mask token 要使用 ignore index？
- BLEU/ROUGE/F1/EM 为什么不能单独作为 LLM 质量指标？
- 什么时候 encoder-only token classification 或 span extraction 比开放式生成更合适？
- transition-based parsing 中的合法动作约束和 structured decoding 中的 token mask 有什么共同点？
- LLM-as-judge 的 position bias、verbosity bias、swapped-order inconsistency 和 human-label disagreement 分别会让什么结论失真？

## Week 10: 前沿方法、Benchmark 边界与课程综合

对应材料：两个 capstone 方向、Ch10 前沿推理部分和前沿主题阅读。

本周阅读目标：综合前面九周的表示、架构、训练、生成、对齐、评测和服务知识，分析一个前沿方法到底改变了哪一层技术栈，以及它的 claim 需要哪些实验才能支撑。

必读：

- 本课程两个 Capstone README：重点看 project 如何把问题设定、方法、实验和结论组织成课程级工程产出。
- 目标方向的官方论文、课程讲义或模型卡：interpretability、multimodality、social impact、agents 或 reasoning。
- 本课程 worked-example-pack：重点复盘每个模块的可计算定义和常见误解。

选读：

- 目标模型、框架或数据集的官方 model card / technical report / API documentation。
- 近一年同主题论文的 related work 和 evaluation section。
- interpretability、多模态、agent、reasoning 或安全治理方向的官方论文、课程讲义或模型卡。

项目论文阅读任务：

每个 capstone 小组需要选 2 篇最接近自己项目问题的材料：一篇方法论文或系统论文，一篇模型卡、benchmark paper 或官方技术报告。阅读目标不是堆引用，而是把自己的项目放进一个明确技术坐标中：

| 论文部分 | 你需要抽取什么 | 如何映射到 capstone |
|----------|----------------|---------------------|
| Problem setup | 输入、输出、约束、目标用户或系统 workload | 写清你的 research question 和不研究什么 |
| Method | 核心算法、模型结构、训练目标或系统机制 | 对应你的 baseline、改动点和实现边界 |
| Experiments | 数据集、样本量、指标、baseline、消融和硬件 | 对应你的评测集、压测、ablation 和成本估算 |
| Analysis | 失败样例、误差分类、资源瓶颈或安全边界 | 对应你的 error analysis 和上线风险 |
| Limitations | 作者承认的限制和未覆盖场景 | 对应你的 conclusion boundary |

最终报告应包含一个短的 related work 段落，说明你的项目继承了什么思路、简化了什么条件、没有覆盖哪些论文中的实验范围。对于训练 capstone，这通常是 optimizer、scaling、LoRA/对齐或数据质量相关工作；对于推理 capstone，这通常是 serving、RAG、quantization、structured output 或 evaluation 相关工作。

复盘问题：

- 目标方向的 benchmark 衡量什么能力？没有衡量什么能力？
- 论文或模型卡中的哪个 claim 依赖特定数据集、推理设置或评测器？
- 如果把该方法接入本课程的训练或推理系统，最先受影响的是显存、延迟、质量、安全性还是成本？
- 一个新方法如果只在单一 benchmark、单一模型规模或单一 prompt 模板上有效，结论应如何表述？
- 如何把 interpretability、multimodality、agents、reasoning 或 safety 的论文 claim 映射到本课程已有的公式、代码和系统指标？
- final project report 中的 abstract、method、experiments、analysis 和 limitations 应分别回答什么问题？
