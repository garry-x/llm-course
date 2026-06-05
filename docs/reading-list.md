# 逐周阅读清单与复盘 Handout

本 handout 把 10 周课程的阅读材料集中为可布置、可评分、可引用的清单。阅读分为三类：

- 必读：课堂讨论和作业默认依赖。
- 选读：用于项目、报告或加深理解。
- 来源辨析：用于训练学生区分论文、官方文档、模型卡、博客和社区材料。

每次阅读复盘必须写明：阅读对象、核心结论、一个公式或实验设计、一个局限、与本课程代码或项目的连接、引用链接和访问日期。

## Week 0: 先修与 ML Foundations Bridge

对应材料：Prerequisite Diagnostic、[数学与 PyTorch 先修复习](math-prerequisites.md)、[ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md)。

必读：

- 本课程 [ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md)：重点看 calculus、probability/statistics、ML objectives、generalization 和 evaluation。
- Goodfellow, Bengio, Courville. [Deep Learning](https://www.deeplearningbook.org/), optimization 和 ML basics 相关章节。
- Stanford CS224N 公开页 Prerequisites 和 Reference Texts：重点看 Python、PyTorch、calculus、linear algebra、probability/statistics 和 ML foundations 的预期边界。

复盘问题：

- 训练目标、验证指标和最终项目结论之间是什么关系？
- 一个 benchmark 或 hidden test 结果在什么条件下不能推广？

## 阅读复盘评分

| 维度 | 分值 | 通过标准 |
|------|:--:|----------|
| 核心结论 | 25 | 能用自己的话说明论文或文档解决的问题、方法和结论 |
| 技术细节 | 25 | 至少解释一个公式、结构图、算法步骤或实验设置 |
| 代码连接 | 20 | 明确指出对应章节代码、作业函数或 capstone 模块 |
| 来源辨析 | 20 | 标注来源等级、发布日期或访问日期，并说明不确定性 |
| 批判性问题 | 10 | 提出一个可讨论的问题、反例、失败模式或复现实验 |

## Week 1: Tokenization 与 Word Vectors

对应章节：Ch01-Ch02。

必读：

- Sennrich, Haddow, Birch. [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909). 重点看 BPE 如何缓解 OOV。
- Mikolov et al. [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781). 重点看 skip-gram 目标。
- Pennington, Socher, Manning. [GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/pubs/glove.pdf). 重点看共现矩阵与加权最小二乘目标。

选读：

- Stanford CS224N 2026 schedule 中的 Word Vectors 主题和 suggested readings。
- Jurafsky and Martin, Speech and Language Processing, word embeddings 相关章节。

复盘问题：

- BPE merge 规则为什么是贪心的？它在哪些语料上会产生不符合语义直觉的 token？
- word2vec 的类比现象是训练目标直接保证的吗？还是空间结构中的经验现象？

## Week 2: Attention 与 Tensor Derivatives

对应章节：Ch03 与数学先修复习。

必读：

- Vaswani et al. [Attention Is All You Need](https://arxiv.org/abs/1706.03762). 重点看 scaled dot-product attention、mask 和 multi-head 结构。
- Stanford CS224N Assignment 2 主题：neural network foundations、tensor derivatives、dependency parsing。

选读：

- Goodfellow, Bengio, Courville. [Deep Learning](https://www.deeplearningbook.org/), optimization 和 backpropagation 相关章节。
- The Matrix Cookbook 中 softmax/cross entropy 与矩阵求导条目。

复盘问题：

- 为什么 attention score 要除以 `sqrt(d_k)`？
- causal mask 的加法实现为什么通常使用一个很大的负数，而不是直接乘 0？

## Week 3: Multi-Head Attention、GQA、MLA 与 Block

对应章节：Ch04-Ch05。

必读：

- Vaswani et al. [Attention Is All You Need](https://arxiv.org/abs/1706.03762). 复读 multi-head attention 与 positional encoding。
- Ainslie et al. [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](https://arxiv.org/abs/2305.13245). 重点看 KV head 数与推理效率。
- DeepSeek-AI. [DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model](https://arxiv.org/abs/2405.04434). 重点看 MLA 的 KV cache 压缩动机。

选读：

- Zhang and Sennrich. [Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467).
- Shazeer. [GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202).

复盘问题：

- GQA 节省 KV cache 的同时损失了什么表达能力？
- MLA 的 latent cache 与 RoPE 解耦为什么会改变工程实现？

## Week 4: GPT 组装、预训练目标与 MoE

对应章节：Ch06。

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

## Week 5: Training Loop、Scaling 与 Distributed Training

对应章节：Ch07。

必读：

- Loshchilov and Hutter. [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101). 重点看 AdamW 与 L2 正则的差别。
- Hoffmann et al. [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556). 重点看 Chinchilla scaling law 的数据/参数权衡。
- Rajbhandari et al. [ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](https://arxiv.org/abs/1910.02054). 重点看 optimizer/gradient/parameter state sharding。

选读：

- PyTorch documentation: `torch.amp`, `DistributedDataParallel`, FSDP。
- DeepSeek-V3 Technical Report 中 FP8 mixed precision 与 DualPipe。

复盘问题：

- AdamW 的 weight decay 为什么不能简单等同于 Adam 里的 L2 penalty？
- 在固定算力下，为什么“更大的模型”不一定比“较小模型 + 更多训练 token”更合理？
- 训练日志里 loss 下降但开发集变差时，应该先查哪些产出？

## Week 6: Generation、Search 与 Speculative Decoding

对应章节：Ch08。

必读：

- Holtzman et al. [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751). 重点看 nucleus sampling。
- Leviathan, Kalman, Matias. [Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192). 重点看 draft/target 接受机制。
- Stern et al. [Blockwise Parallel Decoding for Deep Autoregressive Models](https://arxiv.org/abs/1811.03115). 重点看一次预测多个 token 的动机。

选读：

- Hugging Face Transformers generation strategies documentation。
- DeepSeek-V3 Technical Report 中 multi-token prediction。

复盘问题：

- top-k、top-p、temperature 分别控制分布的哪个性质？
- speculative decoding 在什么情况下不能带来明显加速？

## Week 7: SFT、LoRA、DPO 与 GRPO

对应章节：Ch09。

必读：

- Hu et al. [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685). 重点看低秩增量和可训练参数比例。
- Rafailov et al. [Direct Preference Optimization](https://arxiv.org/abs/2305.18290). 重点看从 KL-constrained RL 到分类式 loss 的推导。
- DeepSeek-AI. [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948). 重点看 GRPO、推理行为和来源边界。

选读：

- Ouyang et al. [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155).
- Anthropic Constitutional AI paper。

复盘问题：

- DPO 为什么需要 reference model？`beta` 调大或调小会怎样？
- GRPO 的组内 advantage 白化依赖什么采样假设？

## Week 8: 经典 NLP、Encoder-only、Evaluation 与 Ethics

对应材料：经典 NLP 专题 Handout、Classic NLP Deep-Dive Teaching Module、经典 NLP 与评测覆盖说明。

必读：

- Chen and Manning. [A Fast and Accurate Dependency Parser using Neural Networks](https://aclanthology.org/D14-1082/). 重点看 transition-based parsing。
- Sutskever, Vinyals, Le. [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215). 重点看 encoder-decoder 和 teacher forcing。
- Devlin et al. [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805). 重点看 MLM/NSP 与 encoder-only 表示。
- Bommasani et al. [On the Opportunities and Risks of Foundation Models](https://arxiv.org/abs/2108.07258). 重点看风险分类。

选读：

- Papineni et al. [BLEU: a Method for Automatic Evaluation of Machine Translation](https://aclanthology.org/P02-1040/).
- Lin. [ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/).

复盘问题：

- dependency parsing 与 decoder-only LLM 在结构归纳偏置上有什么差异？
- encoder-decoder cross-attention 和 decoder-only causal self-attention 的 K/V 来源有什么不同？
- BERT MLM labels 中为什么未 mask token 要使用 ignore index？
- BLEU/ROUGE/F1/EM 为什么不能单独作为 LLM 质量指标？

## Week 9: Inference Engineering、RAG、Quantization 与 Serving

对应章节：Ch10 与推理工程 capstone。

必读：

- Kwon et al. [Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180). 重点看 KV cache 分页。
- Dao et al. [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135). 重点看 IO-aware attention。
- Lewis et al. [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401). 重点看 retriever/generator 组合。
- Dettmers et al. [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314). 重点看 4-bit quantization 与 LoRA 结合。

选读：

- vLLM documentation on PagedAttention and continuous batching。
- SGLang, TensorRT-LLM, llama.cpp 官方文档中 serving、quantization 或 batching 部分。

复盘问题：

- TTFT、TPOT、TPS 分别受哪些系统瓶颈影响？
- RAG 评测为什么必须同时看检索质量和生成质量？

## Week 10: Capstone 报告、复现与前沿来源辨析

对应材料：两个 capstone README、项目报告 rubric 和前沿主题阅读。

必读：

- Stanford CS224N coursework/final project 页面：重点看 assignment、project proposal、milestone、poster/report 的分工。
- 本课程 [Capstone 项目报告 Rubric](project-report-rubric.md)。
- 目标方向的官方论文、课程讲义或模型卡：interpretability、multimodality、social impact、agents 或 reasoning。

选读：

- 目标模型、框架或数据集的官方 model card / technical report / API documentation。
- 近一年同主题论文的 related work 和 evaluation section。
- interpretability、多模态、agent、reasoning 或安全治理方向的官方论文、课程讲义或模型卡。

复盘问题：

- 你的项目最强产出是什么？最弱产出是什么？
- 报告中哪些结论只能说“本实验条件下成立”，不能推广为一般事实？

## 来源等级速查

| 等级 | 来源 | 适用方式 |
|------|------|----------|
| A | 论文、官方技术报告、官方文档、模型卡、课程官网 | 可作为正文事实，但仍需标注日期和适用范围 |
| B | 研究团队博客、会议演讲、工程博客 | 可作为解释或案例，不能替代论文中的实验条件 |
| C | 第三方 benchmark、媒体报道、社区整理 | 只能作为线索，必须交叉验证 |
| D | 未给出实验设置的截图、社交媒体、传闻 | 不作为课程事实 |

## 提交模板

```text
阅读对象：
链接：
访问日期：
来源等级：

1. 核心问题：
2. 方法或公式：
3. 实验或产出：
4. 局限或失败模式：
5. 对应课程代码/作业：
6. 我的问题：
```
