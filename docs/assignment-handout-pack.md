# Assignment Handout Pack

本文件把 11 个章节作业整理成正式 handout 摘要，补充各 `assignments/ch*/README.md`、[Assessment Blueprint and Coverage Matrix](assessment-blueprint-coverage-matrix.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md)、[Programming Assignment Code Quality Rubric](programming-assignment-code-quality-rubric.md)、[Workload and Pacing Calibration](workload-pacing-calibration.md)、[Notation and Shape Glossary](notation-shape-glossary.md)、[Worked Example Pack](worked-example-pack.md)、[Autograder 与隐藏测试设计指南](autograder-hidden-tests.md)、[书面推导与概念题题库](written-problem-set.md) 和 [Instructor Solution Guide](instructor-solution-guide.md)。

目标是让每个作业都像高校课程作业一样同时包含 written questions、programming parts、提交物、评分权重和隐藏测试边界，而不是只提供一个可运行测试目录。

## 统一提交结构

| 文件 | 必需 | 内容 |
|------|------|------|
| `student_solution.py` | Yes | 保持 starter API，不改函数签名 |
| `written_answers.md` 或 `.pdf` | Yes | 推导题、shape、复杂度、错误分析和引用 |
| `run_log.txt` | Yes | 公开测试命令、环境、通过/失败摘要 |
| `honor_statement.txt` | Yes | 协作、AI 工具、外部资源和参考代码披露 |
| `extra_experiments.md` | Optional | ablation、边界测试或项目扩展 |

公开测试不等于满分。正式评分应由公开测试、隐藏测试、书面题和代码质量共同决定。

## Assignment 1: Tokenization and BPE

| 部分 | 权重 | 要求 |
|------|:--:|------|
| Written questions | 30 | 解释 byte-level BPE 可逆性、频率合并的压缩启发式、tie-breaking 对词表的影响、词表大小与序列长度/嵌入参数量的权衡 |
| Programming parts | 60 | 实现 `_get_stats`、`_merge`、`train`、`encode`、`decode`，通过中英文、emoji、多字节 UTF-8 round trip |
| Analysis / style | 10 | 报告至少 2 个 tokenizer 失败或边界案例，不硬编码测试文本 |

隐藏测试关注空输入、多字节字符、重叠 pair、tie-breaking、非法 vocab size 和未见文本 round trip。

## Assignment 2: Embeddings and Position Encoding

| 部分 | 权重 | 要求 |
|------|:--:|------|
| Written questions | 35 | 推导 embedding 参数量，解释 one-hot 与 lookup 等价性，证明 self-attention 的置换等变性，推导 RoPE 点积依赖相对位置 |
| Programming parts | 55 | 实现 `TokenEmbedding`、`SinusoidalEncoding`、`RoPE` 和相对位置数值验证 |
| Analysis / style | 10 | 说明 RoPE 外推失败模式、odd head dimension 拒绝策略和 dtype/device 迁移 |

隐藏测试关注 batch/seq 边界、buffer 是否训练、RoPE 范数保持、Toeplitz 分数矩阵和非法维度处理。

## Assignment 3: Scaled Dot-Product Attention

| 部分 | 权重 | 要求 |
|------|:--:|------|
| Written questions | 35 | 推导 `1/sqrt(d_k)` scaling、mask 加在 softmax 前的原因、causal mask 的形状广播和复杂度 |
| Programming parts | 55 | 实现 Q/K/V 投影、scaled dot-product attention、causal mask 和 attention 可视化接口 |
| Analysis / style | 10 | 解释全 mask 行、数值稳定性和 softmax 后 mask 的错误模式 |

隐藏测试关注 2D/3D/4D mask broadcast、大 logits、全 mask 行、decode query 非方阵场景和梯度传播。

## Assignment 4: Multi-Head Attention, GQA, and MLA

| 部分 | 权重 | 要求 |
|------|:--:|------|
| Written questions | 35 | 计算 MHA 参数量，比较 MHA/MQA/GQA/MLA 的 KV cache，解释 RoPE 与 latent cache 的边界 |
| Programming parts | 55 | 实现 MHA、GQA、MLA shape、KV cache size ratio 和参数量检查 |
| Analysis / style | 10 | 报告不同 `n_heads/n_kv_heads` 下的显存变化和非法配置处理 |

隐藏测试关注不可整除 head、mask 广播、GQA 分组、latent cache shape 和不能退化为完整 MHA cache。

## Assignment 5: Transformer Block, Norm, and FFN

| 部分 | 权重 | 要求 |
|------|:--:|------|
| Written questions | 35 | 推导 LayerNorm/RMSNorm，比较 Pre-Norm/Post-Norm 梯度路径，计算 FFN/SwiGLU 参数量 |
| Programming parts | 55 | 实现 LayerNorm、RMSNorm、FFN/SwiGLU、Pre-Norm TransformerBlock 和 gradcheck |
| Analysis / style | 10 | 说明 `eps`、dropout/eval、残差缩放和深层稳定性的边界 |

隐藏测试关注零方差输入、LayerNorm backward、SwiGLU hidden width、block 梯度流和跳过子层的投机实现。

## Assignment 6: GPT Assembly and MoE

| 部分 | 权重 | 要求 |
|------|:--:|------|
| Written questions | 30 | 计算 GPT-2 small 参数量，解释 weight tying、causal leakage 测试、MoE 稀疏激活和负载均衡 |
| Programming parts | 60 | 实现 GPTConfig、GPTModel forward、初始化、权重共享、MoERouter top-k 和动态偏置 |
| Analysis / style | 10 | 报告一次参数/显存审计，并说明超长序列拒绝原因 |

隐藏测试关注自定义小模型、future-token leakage、参数对象关系、初始化、非法 top-k 和负载偏置方向。

## Assignment 7: Training Loop

| 部分 | 权重 | 要求 |
|------|:--:|------|
| Written questions | 35 | 推导交叉熵、perplexity、AdamW 偏置修正、warmup+cosine 边界和 grad clipping 的诊断意义 |
| Programming parts | 55 | 实现 TextDataset、稳定 CE、AdamW、scheduler、训练循环、loss/lr/grad_norm/tokens/s 日志 |
| Analysis / style | 10 | 提交一段 loss 曲线解释、一次失败案例和 checkpoint/resume 计划 |

隐藏测试关注短文本边界、大 logits、AdamW 单步手算、scheduler 边界、optimizer state 和 resume 一致性。

## Assignment 8: Generation and Constrained Decoding

| 部分 | 权重 | 要求 |
|------|:--:|------|
| Written questions | 35 | 比较 greedy、temperature、top-k、top-p、repetition penalty、speculative decoding 和约束解码的适用边界 |
| Programming parts | 55 | 实现采样过滤、generation loop、distinct-n、speculative decoding 统计和结构化输出约束 |
| Analysis / style | 10 | 用固定 prompt 报告重复、幻觉、格式错误和指标局限 |

隐藏测试关注非法采样参数、top-p 最小集合、EOS/max tokens、空 prompt、接受率统计和过滤后重新归一化。

## Assignment 9: SFT, LoRA, DPO, and GRPO

| 部分 | 权重 | 要求 |
|------|:--:|------|
| Written questions | 35 | 推导 SFT mask、LoRA 参数量、DPO log-ratio、GRPO 组内白化和奖励漏洞边界 |
| Programming parts | 55 | 实现 SFT dataset/loss、LoRA apply/merge、DPO loss、GRPO advantage 和 sequence log-prob |
| Analysis / style | 10 | 报告 chosen/rejected 长度偏差、beta 敏感性或单样本 group 风险 |

隐藏测试关注 `-100` ignore index、LoRA 初始等价、冻结参数、DPO 方向、GRPO NaN 和 prompt group 边界。

## Assignment 10: Inference Engineering

| 部分 | 权重 | 要求 |
|------|:--:|------|
| Written questions | 35 | 推导 KV cache 显存、量化误差、RAG chunk/overlap、TTFT/TPOT/tokens/s 和 SLO 的上线意义 |
| Programming parts | 55 | 实现增量 KV attention、显存估算、INT8 per-channel quantization、RAG、benchmark summary 和 LSH |
| Analysis / style | 10 | 提交 latency/cost/quality/safety 取舍说明和至少一个容量规划例子 |

隐藏测试关注 batch/layer/K/V 两倍显存、全零量化、非法 overlap、P50/P95/P99、error rate 和 LSH 空桶策略。

## Assignment 11: Classic NLP and Evaluation

| 部分 | 权重 | 要求 |
|------|:--:|------|
| Written questions | 40 | 解释 dependency parsing、BLEU、ROUGE-L、QA EM/F1、BERT MLM mask 和 LLM 评测之间的关系 |
| Programming parts | 50 | 实现 UAS/LAS、BLEU、ROUGE-L、QA EM/F1 和 BERT-style MLM example |
| Analysis / style | 10 | 构造至少 2 个指标高但人工质量差的例子，并说明指标局限 |

隐藏测试关注长度错误、root、brevity penalty、多 reference、空输入、标准化和非法 mask position。

## 发布前 Checklist

| 检查项 | 通过标准 |
|--------|----------|
| written/programming 双轨 | 每个作业都能指出 written questions 和 programming parts |
| rubric 可追溯 | 每个测试类别映射到分值和手工评分项 |
| 提交包完整 | 学生知道代码、书面题、日志和诚信声明如何提交 |
| 隐藏测试边界透明 | 公开类别和性质，不公开精确输入 |
| 复核可操作 | 失败日志能对应 rubric 项、seed、shape、dtype 和期望性质 |
