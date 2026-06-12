# LLM 深度学习课程 Syllabus

本课程面向 10-12 周高校课程或系统自学使用。主线是从代码和数学出发，理解 decoder-only LLM 如何把文本表示为 token，如何通过 Transformer 计算下一个 token 分布，如何训练、生成、微调、对齐，并最终服务到真实应用中。课程定位不是传统 NLP 概论，而是面向 LLM 训练工程师和推理工程师的系统课程；经典 NLP 作为模型范式和评测专题补充主线。

## 课程目标

完成课程后，学生应能：

- 从 tokenizer、embedding、attention、Transformer block 到 GPT model 解释 decoder-only LLM 的完整数据流。
- 用 PyTorch 实现并测试核心模块，而不是只调用现成 API。
- 推导或解释关键公式：BPE merge、RoPE 相对位置、attention scaling、LayerNorm/RMSNorm、cross entropy、DPO/GRPO、KV Cache 显存。
- 读懂 LLM 论文和模型报告中的核心技术选择，区分数学假设、实验结论和工程取舍。
- 设计训练与推理实验，解释 loss、PPL、latency、throughput、quality、safety 和 cost 指标。
- 理解经典 NLP 专题与现代 LLM 的关系：RNN/LSTM、dependency parsing、seq2seq/NMT、BERT/encoder-only、BLEU/ROUGE/F1/EM 和安全评测。

## 先修要求

最低要求：

- Python 基础：函数、类、列表/字典、文件读写。
- PyTorch 基础：tensor shape、broadcast、`nn.Module`、autograd、optimizer。
- 数学基础：矩阵乘法、向量点积、概率分布、导数和链式法则。

建议课前完成：

- 复习 tensor indexing、broadcast、矩阵乘法和 cross entropy。
- 跑通 Ch01 BPE 作业，确认本地 Python 环境可用。
- 若 PyTorch 不熟，先完成 Python/PyTorch 复习 handout 中的 shape tracing 练习。

## 课程结构

| 模块 | 周次 | 内容 | 学习重点 |
|------|------|------|----------|
| 表示层 | Week 1 | Ch01-Ch02 | BPE、token id、embedding lookup、位置编码、RoPE |
| 注意力核心 | Week 2 | Ch03 | Q/K/V、scaled dot-product attention、causal mask、softmax 行为 |
| Transformer 组件 | Week 3 | Ch04-Ch05 | MHA、GQA、MLA、LayerNorm/RMSNorm、FFN、SwiGLU、residual path、block 资源估算 |
| GPT 组装 | Week 4 | Ch06 | GPTModel、LM head、weight tying、参数量估算、MoE router |
| 训练闭环 | Week 5 | Ch07 | MLE、cross entropy、PPL、AdamW、scheduler、checkpoint、分布式训练概念 |
| 生成方法 | Week 6 | Ch08 | greedy、temperature、top-k/top-p、speculative decoding、structured decoding |
| 微调与对齐 | Week 7 | Ch09 | SFT/偏好数据 gate、LoRA、preference model、DPO、GRPO、alignment tax |
| 推理工程 | Week 8 | Ch10 | KV Cache、quantization、FlashAttention、RAG、vLLM/SGLang、Triton、服务指标 |
| 经典 NLP 与评测专题 | Week 9 | Ch11 + Classic NLP handout | RNN/LSTM、dependency parsing、seq2seq、BERT、BLEU/ROUGE/F1/EM、安全评测 |
| 项目展示 | Week 10 | Capstone | 训练项目、推理项目、报告、演示和讨论 |

10 周版本优先保证“模型实现 -> 训练 -> 生成/对齐 -> 推理服务 -> 项目”的工程链路完整；经典 NLP 放在 Week 9，用来补齐 encoder-only、seq2seq、结构化预测和评价指标。12 周版本建议把 Week 9 的经典 NLP 与评测拆成两周，把 Week 10 拆成训练项目展示和推理项目展示两次。

## 作业与评分

| 项目 | 权重 | 交付内容 |
|------|:--:|----------|
| 章节编程作业 | 35% | Ch01-Ch11 starter 实现、测试输出、错误分析 |
| 书面推导与概念题 | 20% | 公式推导、复杂度分析、shape trace、概念辨析 |
| 训练工程 Capstone | 15% | 数据分析、训练日志、checkpoint/resume、成本估算 |
| 推理工程 Capstone | 20% | API、评测、压测、SLO、容量规划、错误分析 |
| 阅读复盘与课堂参与 | 10% | 论文摘要、技术细节、批判性问题、课堂讨论 |

## 学习成果矩阵

本课程的评分不是只检查“能否跑通代码”。每个模块都同时考查四类能力：数学定义、可运行实现、实验评测和工程判断。学生应能把同一个概念从公式、张量 shape、测试用例和系统取舍四个角度讲清楚。

| 能力 | 课程中的具体要求 | 主要对应材料 |
|------|------------------|--------------|
| 数学建模 | 写出目标函数、概率分解、mask 语义、动态规划递推或复杂度公式，并说明变量含义和边界条件 | 书面题、lecture derivations、worked examples |
| PyTorch 实现 | 用 tensor 操作实现核心模块，处理 batch、sequence、head、vocab、padding、ignore index 和 dtype 等边界 | Ch01-Ch11 programming assignments |
| 实验评测 | 区分训练 loss、任务指标、系统指标和人工质量；能解释指标适用范围和失败模式 | Ch07-Ch11、capstone、benchmark summary |
| 工程判断 | 估算显存、FLOPs、token budget、latency、throughput、context packing 和对齐风险 | Ch04-Ch10、training/inference capstone |
| 论文阅读 | 抽取论文中的问题设定、核心算法、实验设置和方法边界，并映射到课程代码 | reading-list、课堂讨论、阅读复盘 |

## 编程作业路线图

章节作业按“从 token 到服务”的顺序递进。每次作业都应保留简短错误分析：哪些 shape、mask、dtype、边界条件或评价指标最容易出错，以及你如何用测试定位问题。

| 作业 | 核心实现 | 关键概念 | 学生完成后应能回答 |
|------|----------|----------|--------------------|
| A1 Ch01-Ch02 | BPE、tokenizer report、embedding lookup、RoPE、word-vector objectives | 表示学习、子词压缩、分布式语义、位置编码 | tokenization 如何影响 context、训练成本和 embedding 参数量？ |
| A2 Ch03 | scaled attention、causal/padding mask、softmax Jacobian、attention entropy | Q/K/V、mask 语义、attention 反向传播 | 为什么 mask 必须在 softmax 前应用？attention score 的 shape 为什么是四维？ |
| A3 Ch04-Ch05 | MHA/GQA/MLA、repeat KV heads、LayerNorm/RMSNorm、SwiGLU、block resource estimates | 多头结构、KV cache、残差路径、激活显存 | GQA 为什么能省推理显存？Pre-Norm 为什么更利于深层训练？ |
| A4 Ch06 | GPT config/model、weight tying、causal LM label shift、MoE router 和参数预算 | decoder-only LM、LM head、MoE 稀疏激活 | 为什么 logits 位置 `t` 预测 label `t+1`？MoE 的总参数和激活参数为什么不同？ |
| A5 Ch07 | dataset/dataloader、data curation gate、CE gradient、label smoothing、AdamW、scheduler、calibration、training budget、optimizer memory、`distributed_training_strategy_report`、`training_system_gate_report` | 训练闭环、数据过滤/去重/混合、优化器、校准、训练成本、DDP/ZeRO/FSDP、MFU、resume parity、工业训练 gate | AdamW 与 L2 penalty 有何差异？训练显存为什么不能只数参数？DDP、ZeRO/FSDP 和 TP/PP 分别解决什么瓶颈？数据质量或污染 gate 失败时为什么不能直接扩容？什么时候应该继续扩容，什么时候必须先 debug？ |
| A6 Ch08 | greedy/top-k/top-p、repetition penalty、beam、pass@k、self-consistency、`test_time_compute_budget_report`、token constraints、speculative decoding | 解码策略、搜索、多样性、reasoning/test-time compute 预算、结构化生成 | top-p 为什么是自适应截断？多样本 reasoning 何时值得上线？约束解码如何改变采样分布？ |
| A7 Ch09 | SFT mask、LoRA、sequence log-probs、post-training data audit、RM/DPO/PPO/GRPO、implicit reward、KL、length bias、`rlvr_grader_report` | 指令微调、偏好优化、reference model、可验证 reward、对齐风险 | DPO 为什么比较 policy 相对 reference 的变化，而不是只比较 raw log-prob？偏好数据 gate 失败时为什么不能直接进入 DPO/GRPO？什么时候 RLVR/RFT 的 grader 信号足够可靠？ |
| A8 Ch10 | KV cache、prefix cache、quantization、InfoNCE、reranker loss、retrieval metrics、MMR、context packing、`validate_tool_call_plan`、benchmark summary、`prefill_decode_disaggregation_report`、`pd_pool_capacity_plan`、`speculative_serving_gate_report`、指标结论边界 | 推理工程、RAG、tool/agent 协议、服务指标、容量规划、prefill/decode 解耦、KV transfer、P/D worker pool sizing、speculative decoding 上线 gate | TTFT、TPOT、tokens/s、P95 和显存分别约束什么产品问题？如何在执行前拦截无效或越权 tool call？如何把端到端延迟拆成 prefill、KV transfer、decode queue 和 TPOT？P/D 解耦后如何判断 worker、link 和 KV memory 哪个先饱和？为什么高接受率不必然支持启用推测解码？ |
| A9 Ch11 | RNN recurrence、dependency parsing、seq2seq attention、MLM、BIO/span F1、Viterbi/CRF、QA span、BLEU/ROUGE/EM/F1、`judge_reliability_audit` | 经典 NLP、encoder-only、结构化预测、评测指标、LLM-as-judge 可靠性 | 什么时候应选择 span extraction、token classification 或 structured decoding，而不是开放式生成？为什么一次 judge win rate 不能直接支持上线结论？ |

## 书面题能力层级

书面题按难度分为三层。基础题检查定义和 shape；推导题要求从公式到数值例子；设计题要求学生提出可复现实验并说明结论边界。

| 层级 | 要求 | 示例 |
|------|------|------|
| Level 1: Definition / Shape | 写清输入输出、mask、标签、有效 token、batch/head/sequence 维度 | attention score shape、SFT label mask、KV cache bytes |
| Level 2: Derivation / Calculation | 展开公式并完成小数值例子，说明每一步分母、归一化或动态规划状态 | softmax CE gradient、top-p nucleus、CRF log-partition、pass@k |
| Level 3: Experiment / Critique | 设计实验、选择指标、列出失败模式，并说明结果不能推出哪些更强结论 | RAG ablation、DPO vs SFT evaluation、training gate、prefill/decode benchmark summary |

## Capstone 学术要求

两个 capstone 分别训练学生做“受约束的建模实验”和“受约束的系统实验”。最终报告应像课程 project paper，而不是产品介绍。

最终报告建议按课程论文结构组织：

| 部分 | 必须回答的问题 |
|------|----------------|
| Abstract | 一句话说明问题、方法、最重要结果和结论边界 |
| Introduction | 为什么这个训练或推理问题值得研究，目标 workload 是什么 |
| Related work | 至少连接 2 篇论文、技术报告或官方文档，说明项目继承和简化了什么 |
| Method / System | 数据、模型、训练目标、服务架构、RAG/工具/评测流程或容量假设 |
| Experiments | baseline、ablation、固定评测集、系统指标、硬件、随机种子或负载设置 |
| Analysis | 错误类型、失败案例、资源瓶颈、安全/过度拒答或成本变化 |
| Limitations | 哪些结论不能外推到更大模型、真实 GPU、真实用户流量或其他领域 |
| Reproducibility | 运行命令、配置、数据版本、checkpoint 或服务启动方式 |

训练工程 Capstone 必须回答：

- 数据：训练/验证拆分、去重或泄漏风险、token 统计、样本质量问题。
- 模型：架构规模、参数量、训练 token budget、batch tokens、optimizer state 和 checkpoint 策略。
- 优化：loss/PPL 曲线、learning rate schedule、gradient clipping、resume、失败 run 处理。
- 系统 gate：把 optimization、throughput、state/checkpoint 和 evaluation 分开判定，说明继续训练、扩容、回退或 debug 的依据。
- 评测：至少一个 held-out 指标、一个人工错误分析维度和一个能力退化或偏差风险。
- 结论：哪些发现只适用于当前数据、规模、预算和随机种子。

推理工程 Capstone 必须回答：

- 服务：模型、硬件、batching、context length、generation 参数和 API 行为。
- 检索/上下文：chunking、embedding、retrieval、reranking、MMR、context packing 和 citation 策略。
- 性能：TTFT、TPOT、tokens/s、P50/P95/P99、显存、并发和错误率。
- 解耦分析：若 workload 有长 prompt、RAG、多模态或 agent 请求，必须拆分 prefill、KV transfer、decode queue、TPOT 和 active KV tokens。
- 质量：任务指标、失败案例、结构化输出或 tool/JSON 回归。
- 结论：哪些结果依赖当前负载、评测集、缓存命中率、硬件和实现。

每次编程作业必须包含：

- 核心代码实现。
- 至少一组正常输入和一组边界输入。
- 测试输出或失败分析。
- 对关键 tensor shape 的说明。

每次书面作业必须包含：

- 推导步骤，而不是只给最终公式。
- 变量定义、shape 和边界条件。
- 必要的论文或官方文档引用。

## 周安排

| 周 | 主题 | 阅读 | 作业/交付 |
|----|------|------|-----------|
| 1 | Tokenization 与 Embedding | Ch01-Ch02；reading-list Week 1 | A1：BPE + embedding/RoPE；书面题 Ch01-Ch02 |
| 2 | Attention 与反向传播复习 | Ch03；reading-list Week 2；math prerequisites | A2：scaled attention + causal mask；书面题 Ch03 |
| 3 | MHA/GQA/MLA、Transformer Block 与机制可解释性 | Ch04-Ch05；reading-list Week 3 | A3：MHA/GQA/MLA + block；书面题 Ch04-Ch05 |
| 4 | GPT 组装与 MoE | Ch06；reading-list Week 4 | A4：GPTModel + MoE router；书面题 Ch06 |
| 5 | Training Loop | Ch07；reading-list Week 5 | A5：dataset/data curation/CE/AdamW/scheduler/train；训练项目提案 |
| 6 | Generation、Decoding 与 Reasoning | Ch08；reading-list Week 6 | A6：top-k/top-p/speculative decoding/reasoning；书面题 Ch08 |
| 7 | Fine-tuning 与 Alignment | Ch09；reading-list Week 7 | A7：SFT/post-training data audit/LoRA/DPO/GRPO/RLVR grader；训练 capstone 初版 |
| 8 | Inference Engineering、RAG 与 Multimodal Serving | Ch10；reading-list Week 8 | A8：KV cache/RAG/speculative gate/benchmark summary/多模态评估；推理项目提案 |
| 9 | 经典 NLP、结构化预测与评测专题 | Ch11；classic-nlp-handout；reading-list Week 9 | A9：RNN/dependency/seq2seq/BERT/evaluation 作业与书面题；推理 capstone 初版 |
| 10 | Capstone 综合与前沿 seminar | 两个 capstone 方向；reading-list Week 10 | 训练 capstone + 推理 capstone 总结、前沿方法复盘 |

## 项目

训练工程 Capstone：

| 时间 | 交付 |
|------|------|
| 第 5 周 | 项目提案：研究问题、baseline、数据、模型规模、训练预算、风险 |
| 第 7 周 | Milestone：数据分析、训练日志、checkpoint/resume、初步失败案例 |
| 第 10 周 | 最终报告：ablation、错误分析、成本估算、结论边界、复现命令 |

推理工程 Capstone：

| 时间 | 交付 |
|------|------|
| 第 8 周 | 项目提案：服务场景、research question、baseline、评测集、SLO、容量目标 |
| 第 9 周 | Milestone：OpenAI-compatible API、评测、benchmark、SLO、初步失败案例 |
| 第 10 周 | 最终报告：P50/P95/P99、TTFT/TPOT、RAG/JSON/tool 回归、成本估算和结论边界 |

## 协作与 AI 工具

- 可以讨论思路、论文、debug 假设和测试失败原因。
- 最终代码、推导和报告必须独立完成。
- 禁止复制他人提交、共享隐藏测试或伪造日志。
- AI 工具可以辅助学习和调试，但学生必须能解释提交内容，并在报告中披露使用环节。

## 引用与阅读

论文、官方文档、模型卡、博客和第三方库都需要引用。引用的重点是让读者知道概念、公式、实验设置或工程接口来自哪里，并能回到原文继续阅读。
