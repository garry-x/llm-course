# 逐周阅读材料与复盘 Handout

本 handout 把 10 周课程的阅读材料组织成一条从基础 NLP 到现代 LLM 系统的学习路径。阅读分为三类：

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

## Week 0: 先修与 ML Foundations Bridge

对应材料：Prerequisite Diagnostic、[数学与 PyTorch 先修复习](math-prerequisites.md)、[ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md)。

本周阅读目标：确认学生能把基础 ML 语言转成 LLM 课程中反复使用的对象，包括 loss、gradient、generalization、held-out evaluation、tensor shape 和 PyTorch module。

必读：

- 本课程 [ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md)：重点看 calculus、probability/statistics、ML objectives、generalization 和 evaluation。
- Goodfellow, Bengio, Courville. [Deep Learning](https://www.deeplearningbook.org/), optimization 和 ML basics 相关章节。
- 本课程 [数学与 PyTorch 先修复习](math-prerequisites.md)：重点确认 Python、PyTorch、calculus、linear algebra、probability/statistics 和 ML foundations 的最低掌握边界。

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

本周阅读目标：从单步 loss 进入训练系统，理解 optimizer、scheduler、mixed precision、checkpoint、scaling law 和 distributed memory sharding 如何共同决定可训练规模。

必读：

- Loshchilov and Hutter. [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101). 重点看 AdamW 与 L2 正则的差别。
- Hoffmann et al. [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556). 重点看 Chinchilla scaling law 的数据/参数权衡。
- Rajbhandari et al. [ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](https://arxiv.org/abs/1910.02054). 重点看 optimizer/gradient/parameter state sharding。
- Shoeybi et al. [Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism](https://arxiv.org/abs/1909.08053). 重点看 tensor parallelism 如何切分 Transformer 层内矩阵。
- Jiang et al. [MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs](https://arxiv.org/abs/2402.15627). 重点看大规模训练中的 full-stack observability、straggler 诊断、容错和 MFU，而不是只记住 GPU 数。

选读：

- Huang et al. [GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism](https://arxiv.org/abs/1811.06965). 重点看 micro-batch、pipeline bubble 和 activation rematerialization。
- PyTorch documentation: `torch.amp`, `DistributedDataParallel`, FSDP2 和 Distributed Checkpoint。重点看 FSDP 如何分片参数、梯度和 optimizer state，以及 resume parity 如何验证。
- NVIDIA Megatron Core parallelism guide。重点看 DP、TP、PP、CP、EP 和 sequence parallelism 分别切什么维度，什么时候组合。
- DeepSeek-V3 Technical Report 中 FP8 mixed precision、DualPipe、MLA/MoE 和 MTP。重点看这些设计如何共同服务训练效率和稳定性。
- NVIDIA / PyTorch profiler 文档中 GPU utilization、kernel timeline、communication overlap 和 dataloader bottleneck 的诊断方法。

复盘问题：

- AdamW 的 weight decay 为什么不能简单等同于 Adam 里的 L2 penalty？
- 在固定算力下，为什么“更大的模型”不一定比“较小模型 + 更多训练 token”更合理？
- 训练日志里 loss 下降但开发集变差时，应该先查哪些产出？
- 参数、梯度、optimizer state、activation 和 communication buffer 分别如何进入显存预算？
- DDP、ZeRO/FSDP、tensor parallel 和 pipeline parallel 分别解决容量、通信还是吞吐中的哪一类瓶颈？
- MFU 低时，如何区分 batch 太小、通信等待、数据加载不足、checkpoint 写盘和 kernel 未融合？
- 一次训练 run 的 optimization、throughput、state/checkpoint 和 evaluation gate 分别需要哪些最低证据？
- FSDP2 / Distributed Checkpoint / Megatron Core 这类工具解决的是课程 tiny train 中哪一个被简化掉的问题？
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

选读：

- Hugging Face Transformers generation strategies documentation。
- DeepSeek-V3 Technical Report 中 multi-token prediction。

复盘问题：

- top-k、top-p、temperature 分别控制分布的哪个性质？
- speculative decoding 在什么情况下不能带来明显加速？
- self-consistency 或 best-of-N 的准确率提升应如何同时报告 token 成本和延迟？
- constrained decoding 是改变模型参数、logits、token mask 还是后处理？不同实现的失败模式是什么？
- test-time compute 提高准确率时，应该同时报告哪些系统指标？

## Week 7: SFT、LoRA、DPO、GRPO 与 RLVR/RFT

对应章节：Ch09。

本周阅读目标：区分 SFT、parameter-efficient fine-tuning、reward modeling、DPO、GRPO 和 RLVR/RFT 的训练信号，理解偏好数据和可验证 reward 如何进入目标函数。

必读：

- Hu et al. [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685). 重点看低秩增量和可训练参数比例。
- Rafailov et al. [Direct Preference Optimization](https://arxiv.org/abs/2305.18290). 重点看从 KL-constrained RL 到分类式 loss 的推导。
- DeepSeek-AI. [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948). 重点看 GRPO、推理行为和方法边界。
- Kimi Team. [Kimi k1.5: Scaling Reinforcement Learning with LLMs](https://arxiv.org/abs/2501.12599). 重点看 long-context RL、long2short、长度控制和多模态 reasoning 的工程取舍。

选读：

- Ouyang et al. [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155).
- Anthropic Constitutional AI paper。
- OpenAI. [Learning to reason with LLMs](https://openai.com/index/learning-to-reason-with-llms/) 与 [Reinforcement fine-tuning guide](https://developers.openai.com/api/docs/guides/reinforcement-fine-tuning)。重点看 train-time/test-time compute、programmable grader、validation split 和 grader 适用条件。

复盘问题：

- DPO 为什么需要 reference model？`beta` 调大或调小会怎样？
- 偏好数据中的长度偏差、风格偏差或标注者分歧会怎样进入 DPO/RLHF 的目标函数？
- GRPO 的组内 advantage 白化依赖什么采样假设？
- RLVR/RFT 的 grader 为什么需要 pass-rate、reward variance、completion length 和 hacking signal 四类检查？
- LoRA 的低秩增量限制了哪些更新方向？它节省的是训练参数、optimizer state 还是前向激活？
- 对齐后模型质量上升但能力回退时，应如何区分数据分布、KL 约束和评测指标的问题？

## Week 8: Inference Engineering、RAG、Quantization 与 Serving

对应章节：Ch10 与推理工程 capstone。

本周阅读目标：把模型输出接入真实服务，理解 KV cache、continuous batching、paged memory、FlashAttention、quantization、RAG 和多模态输入如何共同影响延迟、吞吐、成本和质量。

必读：

- Kwon et al. [Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180). 重点看 KV cache 分页。
- Dao et al. [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135). 重点看 IO-aware attention。
- Lewis et al. [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401). 重点看 retriever/generator 组合。
- Dettmers et al. [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314). 重点看 4-bit quantization 与 LoRA 结合。
- Yu et al. [Orca: A Distributed Serving System for Transformer-Based Generative Models](https://www.usenix.org/conference/osdi22/presentation/yu). 重点看 iteration-level scheduling 和 continuous batching 为什么能减少队列浪费。
- PyTorch and vLLM. [Disaggregated Inference at Scale with PyTorch & vLLM](https://pytorch.org/blog/disaggregated-inference-at-scale-with-pytorch-vllm/). 重点看 prefill/decode 分离如何同时影响 TTFT、TPOT、throughput 和 KV transfer。

选读：

- vLLM documentation on PagedAttention、continuous batching、prefix caching 和 disaggregated prefilling。
- SGLang v0.4 release note。重点看 zero-overhead batch scheduler、cache-aware load balancer、RadixAttention 和 structured outputs 如何把 CPU 调度、前缀缓存和格式约束揉进 serving engine。
- TensorRT-LLM disaggregated serving 文档。重点看 KV cache exchange、layout conversion、UCX/NIXL、KV transfer 与计算重叠。
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
- prefill/decode 解耦后，为什么必须把 KV transfer、decode queue 和 active KV tokens 单独报告？
- SGLang 的 cache-aware load balancing、vLLM 的 disaggregated prefilling 和 TensorRT-LLM 的 KV transfer overlap 分别在解决哪一层 bottleneck？

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

复盘问题：

- RNN 的 BPTT 梯度连乘为什么会导致长程依赖困难？LSTM 改变了哪条路径？
- dependency parsing 与 decoder-only LLM 在结构归纳偏置上有什么差异？
- encoder-decoder cross-attention 和 decoder-only causal self-attention 的 K/V 来源有什么不同？
- BERT MLM labels 中为什么未 mask token 要使用 ignore index？
- BLEU/ROUGE/F1/EM 为什么不能单独作为 LLM 质量指标？
- 什么时候 encoder-only token classification 或 span extraction 比开放式生成更合适？
- transition-based parsing 中的合法动作约束和 structured decoding 中的 token mask 有什么共同点？

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
