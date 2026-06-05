# LLM 深度学习课程 Syllabus

本课程面向 10-12 周高校课程或系统自学使用。主线是从代码和数学出发，理解 decoder-only LLM 如何把文本表示为 token，如何通过 Transformer 计算下一个 token 分布，如何训练、生成、微调、对齐，并最终服务到真实应用中。

## 课程目标

完成课程后，学生应能：

- 从 tokenizer、embedding、attention、Transformer block 到 GPT model 解释 decoder-only LLM 的完整数据流。
- 用 PyTorch 实现并测试核心模块，而不是只调用现成 API。
- 推导或解释关键公式：BPE merge、RoPE 相对位置、attention scaling、LayerNorm/RMSNorm、cross entropy、DPO/GRPO、KV Cache 显存。
- 读懂 LLM 论文和模型报告中的核心技术选择，区分数学假设、实验结论和工程取舍。
- 设计训练与推理实验，解释 loss、PPL、latency、throughput、quality、safety 和 cost 指标。
- 理解经典 NLP 专题与现代 LLM 的关系：dependency parsing、seq2seq/NMT、BERT/encoder-only、BLEU/ROUGE/F1/EM 和安全评测。

## 先修要求

最低要求：

- Python 基础：函数、类、列表/字典、文件读写。
- PyTorch 基础：tensor shape、broadcast、`nn.Module`、autograd、optimizer。
- 数学基础：矩阵乘法、向量点积、概率分布、导数和链式法则。

建议课前完成：

- 复习 tensor indexing、broadcast、矩阵乘法和 cross entropy。
- 跑通 Ch01 BPE 作业，确认本地 Python 环境可用。
- 若 PyTorch 不熟，先完成 Python/PyTorch review session 中的 shape tracing 练习。

## 课程结构

| 模块 | 周次 | 内容 | 学习重点 |
|------|------|------|----------|
| 表示层 | Week 1 | Ch01-Ch02 | BPE、token id、embedding lookup、位置编码、RoPE |
| 注意力核心 | Week 2 | Ch03 | Q/K/V、scaled dot-product attention、causal mask、softmax 行为 |
| Transformer 组件 | Week 3 | Ch04-Ch05 | MHA、GQA、MLA、LayerNorm/RMSNorm、FFN、SwiGLU、residual path |
| GPT 组装 | Week 4 | Ch06 | GPTModel、LM head、weight tying、参数量估算、MoE router |
| 训练闭环 | Week 5 | Ch07 | MLE、cross entropy、PPL、AdamW、scheduler、checkpoint、分布式训练概念 |
| 生成方法 | Week 6 | Ch08 | greedy、temperature、top-k/top-p、speculative decoding、structured decoding |
| 微调与对齐 | Week 7 | Ch09 | SFT、LoRA、preference model、DPO、GRPO、alignment tax |
| 经典 NLP 与评测 | Week 8 | Classic NLP handout | dependency parsing、seq2seq、BERT、BLEU/ROUGE/F1/EM |
| 推理工程 | Week 9 | Ch10 | KV Cache、quantization、FlashAttention、RAG、vLLM/SGLang、Triton |
| 项目展示 | Week 10 | Capstone | 训练项目、推理项目、报告、演示和讨论 |

12 周版本建议把 Week 8 拆成两周，把 Week 10 拆成训练项目展示和推理项目展示两次。

## 作业与评分

| 项目 | 权重 | 交付内容 |
|------|:--:|----------|
| 章节编程作业 | 35% | Ch01-Ch10 starter 实现、测试输出、错误分析 |
| 书面推导与概念题 | 20% | 公式推导、复杂度分析、shape trace、概念辨析 |
| 训练工程 Capstone | 15% | 数据分析、训练日志、checkpoint/resume、成本估算 |
| 推理工程 Capstone | 20% | API、评测、压测、SLO、容量规划、错误分析 |
| 阅读复盘与课堂参与 | 10% | 论文摘要、技术细节、批判性问题、同伴反馈 |

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
| 5 | Training Loop | Ch07；reading-list Week 5 | A5：dataset/CE/AdamW/scheduler/train；训练项目提案 |
| 6 | Generation、Decoding 与 Reasoning | Ch08；reading-list Week 6 | A6：top-k/top-p/speculative decoding/reasoning；书面题 Ch08 |
| 7 | Fine-tuning 与 Alignment | Ch09；reading-list Week 7 | A7：SFT/LoRA/DPO/GRPO；训练 capstone 初版 |
| 8 | 经典 NLP 与评测专题 | classic-nlp-handout；reading-list Week 8 | A8：dependency/seq2seq/BERT/evaluation 书面题；同伴 review |
| 9 | Inference Engineering、RAG 与 Multimodal Serving | Ch10；reading-list Week 9 | A9：KV cache/RAG/benchmark/多模态评估；推理项目提案 |
| 10 | Capstone 展示与前沿 seminar | 两个 capstone README；reading-list Week 10 | 训练 capstone + 推理 capstone 报告、演示、复现包 |

## 项目

训练工程 Capstone：

| 时间 | 交付 |
|------|------|
| 第 5 周 | 项目提案：数据、模型规模、训练预算、风险 |
| 第 7 周 | 初版：数据分析、训练日志、checkpoint/resume |
| 第 10 周 | 最终报告：ablation、错误分析、成本估算、复现命令 |

推理工程 Capstone：

| 时间 | 交付 |
|------|------|
| 第 8 周 | 项目提案：API 设计、评测集、SLO、容量目标 |
| 第 9 周 | 初版：OpenAI-compatible API、评测、benchmark、SLO |
| 第 10 周 | 最终报告：P50/P95/P99、TTFT/TPOT、RAG/JSON/tool 回归、成本估算 |

## 协作与 AI 工具

- 可以讨论思路、论文、debug 假设和测试失败原因。
- 最终代码、推导和报告必须独立完成。
- 禁止复制他人提交、共享隐藏测试或伪造日志。
- AI 工具可以辅助学习和调试，但学生必须能解释提交内容，并在报告中披露使用环节。

## 引用与阅读

论文、官方文档、模型卡、博客和第三方库都需要引用。最低引用格式：

- 作者或机构。
- 标题。
- 链接。
- 访问日期。
- 使用位置。
