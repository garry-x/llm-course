# Discussion Section and Office Hours Guide

本指南用于助教每周带讨论课、答疑和复盘。它补充 [10 周 / 20 讲 Lecture Plan](lecture-plan.md)、[Weekly Teaching Reflection and Adjustment Log](weekly-teaching-reflection-adjustment-log.md)、[Course Staff and Office Hours Directory](course-staff-office-hours-directory.md)、[Recitation Worksheet Pack](recitation-worksheet-pack.md) 和 [Staff Assistance and Code Review Boundary Policy](staff-assistance-code-review-policy.md)，把模板落成可直接使用的 shape drill、failure drill、paper-to-code drill 和 office-hour triage 记录。

## 讨论课结构

每次 50-75 分钟讨论课建议按以下节奏：

| 环节 | 时间 | 目标 |
|------|:--:|------|
| Recap quiz | 5-10 分钟 | 检查上周最核心的 shape、公式或测试失败 |
| Shape drill | 15 分钟 | 学生独立写出输入、中间张量和输出 shape |
| Failure drill | 15-20 分钟 | 从错误日志判断问题属于数学、mask、dtype、device、数据还是评测 |
| Paper-to-code drill | 15-20 分钟 | 把论文公式或结构定位到 starter/reference/API |
| Exit ticket | 5 分钟 | 收集仍不清楚的问题和下一讲 recap 主题 |

讨论课不应代写作业核心实现。助教可以讲调试路径、shape 推导、最小反例和测试思想。Ch01-Ch02 可以有限查看局部代码片段帮助建立 debug_trace；Ch03-Ch11 默认使用 pseudocode_review、shape guidance 和 public test 解释。

## Week 1: BPE / Embedding / RoPE

Shape drill:

- 给定 byte ids `[101, 101, 32, 228, 184, 173]`，手算一次 pair 统计。
- 给定 token ids shape `[B,T]` 和 embedding matrix `[V,D]`，写出 lookup 输出 shape。
- 给定 RoPE head dim `D=8`，写出需要多少个二维旋转 block。

Failure drill:

- `_merge([1,1,1], (1,1), 256)` 输出 `[256,256]` 是什么错误？
- RoPE 测试显示 norm 不保持，优先检查 sin/cos shape、成对维度还是 position index？

Paper-to-code drill:

- 从 BPE 论文的 rare word 动机定位到 Ch01 `train/encode/decode`。
- 从 `R_m^T R_n = R_{n-m}` 定位到 Ch02 RoPE 相对位置测试。

## Week 2: Attention

Shape drill:

- `q,k,v` 为 `[B,H,T,D]` 时，写出 scores、mask、probabilities、context 的 shape。
- 非方阵 decode：query 长度 `T=1`，cache 长度 `S=8`，causal mask 应允许哪些位置？

Failure drill:

- attention 输出含 NaN：检查全 mask 行、softmax overflow、dtype 还是除以 0？
- masked token 仍有非零概率：判断 mask 是 softmax 前还是 softmax 后应用。

Paper-to-code drill:

- 从 Attention Is All You Need 的 scaled dot-product 公式定位到 `scaled_dot_product_attention`。

## Week 3: MHA / GQA / MLA / Block

Shape drill:

- `d_model=768,n_heads=12` 时每个 head dim 是多少？
- GQA 中 `n_heads=16,n_kv_heads=4`，每组 query head 对应几个 KV head？
- Pre-norm block 中 residual、norm、attention、FFN 的输入输出 shape 是否一致？

Failure drill:

- MHA 换 batch size 后失败：检查 hard-coded shape、view/reshape、mask broadcast。
- GQA KV cache 没有节省：检查是否错误减少 Q head，而不是 KV head。
- LayerNorm gradcheck 失败：检查 mean/variance 依赖和 eps。

Paper-to-code drill:

- 从 GQA 论文的 KV head 减少动机定位到 cache size 计算。
- 从 RMSNorm 论文定位到 RMS 不中心化的实现差异。

## Week 4: GPT / MoE

Shape drill:

- 输入 ids `[B,T]` 到 logits `[B,T,V]` 的完整路径。
- tied embedding 和 LM head 时，参数对象关系应如何检查？
- top-k MoE router 输出 expert ids 和 weights 的 shape。

Failure drill:

- 改变未来 token 后当前 logits 变化：定位 causal mask 泄漏。
- 参数量只在默认 GPT-2 small 下正确：检查是否硬编码常数。
- router 权重和不为 1：检查 softmax 维度和 top-k gather。

Paper-to-code drill:

- 从 GPT-2 next-token training 定位到右移标签。
- 从 Switch Transformer capacity/load balancing 定位到 MoE router 测试。

## Week 5: Training Loop

Shape drill:

- `TextDataset[i]` 返回的 `x,y` 长度为什么相同？
- logits `[B,T,V]` 和 labels `[B,T]` 如何 flatten 计算 CE？

Failure drill:

- loss 变 NaN：检查 logits 数值、mask/ignore index、lr、grad norm、数据异常。
- resume 后 step 没变：检查 checkpoint 是否保存 optimizer/scheduler/global_step。
- 每步 loss 下降但 val loss 上升：区分过拟合、数据泄漏和评估集太小。

Paper-to-code drill:

- 从 AdamW 论文定位到解耦 weight decay。
- 从 Chinchilla scaling law 定位到训练预算和 token/parameter 讨论。

## Week 6: Generation

Shape drill:

- generation loop 中每一步模型输入和新增 token 的 shape。
- top-p 过滤后概率为什么要重新归一化？

Failure drill:

- top-p 没保留任何 token：检查阈值、排序、累计概率和至少保留一个 token。
- temperature=0 仍随机：检查是否退化为 greedy。
- speculative decoding 没加速：区分 draft 质量、target 调用次数和系统瓶颈。

Paper-to-code drill:

- 从 nucleus sampling 论文定位到 top-p 最小集合。
- 从 speculative decoding 论文定位到 draft/target 接受统计。

## Week 7: SFT / LoRA / DPO / GRPO

Shape drill:

- prompt、answer、padding 对应 label 中哪些位置应是 `-100`？
- LoRA `A/B` 矩阵的 shape 如何决定 rank 和参数量？
- chosen/rejected logprob 的 batch shape。

Failure drill:

- SFT loss 包含 prompt：检查 label mask。
- LoRA 初始输出不等于 base：检查 B 初始化和 scaling。
- DPO 越训越偏向 rejected：检查 chosen/rejected 方向。
- GRPO 单样本 group NaN：检查 std 和 eps。

Paper-to-code drill:

- 从 DPO loss 公式定位到 sequence logprob 和 reference ratio。
- 从 DeepSeek-R1 GRPO 描述定位到 group-relative advantage。

## Week 8: Classic NLP / Evaluation / Safety

Shape drill:

- dependency parsing 中 head 和 label 序列长度如何与 token 对齐？
- BLEU n-gram precision、ROUGE-L LCS、QA EM/F1 的输入输出是什么？
- BERT MLM labels 中未 mask token 应如何处理？

Failure drill:

- BLEU exact match 不是 1：检查 clipping、brevity penalty 和 tokenization。
- QA F1 对标点敏感：检查 normalize answer。
- MLM 把 mask token 当 label：检查 label 应为原始 token。

Paper-to-code drill:

- 从 BERT MLM 目标定位到 Ch11 MLM mask 练习。
- 从 BLEU/ROUGE 论文定位到自动评测局限。

## Week 9: Inference / RAG / Serving

Shape drill:

- KV cache memory 公式中每一项的含义。
- incremental decode 的 query 长度和 cache 长度。
- RAG chunk、embedding matrix、query vector、top-k docs 的 shape。

Failure drill:

- KV cache 估算少一半：检查 K/V 两份。
- incremental attention 与 full attention 不一致：检查 causal mask、position index、cache append。
- RAG 检索命中文档但答案错：区分 retrieval quality 和 generation quality。

Paper-to-code drill:

- 从 PagedAttention 定位到 KV cache 内存管理动机。
- 从 RAG 论文定位到 retriever/generator 分工。

## Week 10: Capstone Rehearsal

Shape drill:

- 每组画出项目中一条核心数据流：input -> model/service -> metric -> report。

Failure drill:

- 报告数字无法复现：检查命令、seed、日志路径、数据版本。
- latency 只有平均值：要求 P50/P95/P99、TTFT、TPOT、错误率。
- 训练项目无失败案例：要求至少 3 个按原因分类的失败样例。

Paper-to-code drill:

- 每组选择一个项目引用来源，说明它支持哪个设计选择，不支持哪个更强结论。

## Office Hours Triage

助教答疑时按以下顺序记录并处理；学生可见 queue 字段、Office Hours 类型和 escalation matrix 见 [Course Staff and Office Hours Directory](course-staff-office-hours-directory.md)：

| 步骤 | 问题 | 证据 |
|------|------|------|
| 1 | 学生运行了什么命令？ | 原始命令、cwd、环境 |
| 2 | 失败是 import、shape、数值、测试还是理解问题？ | traceback、assert message、log |
| 3 | 学生期望的 shape/输出是什么？ | 学生手写推导 |
| 4 | 是否违反公开 API 或提交规范？ | diff、函数签名、文件名 |
| 5 | 能否构造更小反例？ | 1-2 行输入或小 tensor |
| 6 | 需要课堂 recap 吗？ | 是否多人重复出现 |

禁止：

- 直接给出隐藏测试答案。
- 替学生写核心函数。
- 查看或传播其他学生提交。
- 在没有复现命令的情况下凭印象判断成绩。

允许的 staff assistance level、limited_code_view、pseudocode_review、artifact_review 和 rubric_explanation 边界见 [Staff Assistance and Code Review Boundary Policy](staff-assistance-code-review-policy.md)。

## 高频问题记录模板

```text
Week:
Assignment:
Question category: shape / math / PyTorch / data / serving / report / policy
Symptom:
Minimal reproduction:
Likely cause:
Suggested hint:
Needs lecture recap: yes/no
Needs autograder update: yes/no
Needs handout clarification: yes/no
```

## Exit Ticket 汇总

每周结束后助教应汇总：

- 3 个最多学生仍不清楚的问题。
- 2 个最常见测试失败。
- 1 个需要更新到讲义、作业 README 或 autograder hint 的地方。
- 1 个下周 discussion section 的开场 recap 题。

这些记录应反馈到 [Course Outcome Map](course-outcome-map.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md) 和 [Grading Calibration Guide](grading-calibration.md)。
