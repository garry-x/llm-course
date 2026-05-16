# LLM 深度学习课程 — 设计文档

## 概述

基于业界优秀课程（Karpathy Zero to Hero、Raschka Build LLM from Scratch、NJU LLM 课程、UPenn Stat 9911、Cornell LM-class）和 DeepSeek 开源技术体系（V2→R1→V3→V4），构建一个"从代码出发"的 LLM 深度学习 Web 课程。

## 文件结构

```
llm-learner/
├── index.html              # 功能首页：Hero + 进度仪表板 + 章节目录
├── css/style.css           # 统一样式（已创建，约350行）
├── js/app.js               # 共享逻辑（已创建，约170行）
├── chapters/
│   ├── ch01.html ~ ch10.html  # 10章，纯HTML
└── serve.sh                # 启动脚本
```

## 设计原则

- **内容即 HTML**：不使用 JS 模板字符串拼接内容，消除语法风险
- **练习用 data 属性**：答案存储在 `data-answer` 属性中，JS 只做校验
- **数学公式**：KaTeX CDN + `data-expr` 属性渲染
- **每章独立可用**：可单独打开阅读，共享 CSS/JS 通过相对路径引用

## 10 章大纲与代码产出

### 第 1 章：环境搭建与分词
- **产出**：BPE Tokenizer（~80行 Python）
- **小节**：1.1 课程概览 | 1.2 环境配置 | 1.3 Token 概念 | 1.4 BPE 算法原理 | 1.5 BPE 训练实现 | 1.6 编码与解码 | 1.7 中英文验证 | 1.8 主流分词器对比 | 1.9 特殊Token | 1.10 练习
- **延伸阅读**：OpenAI tiktoken、SentencePiece、Sennrich 2016

### 第 2 章：嵌入层与位置编码
- **产出**：TokenEmbedding + RoPE（~60行）
- **小节**：2.1 One-Hot→Dense | 2.2 nn.Embedding 实现 | 2.3 余弦相似度 | 2.4 位置信息必要性 | 2.5 正弦编码实现 | 2.6 RoPE 实现 | 2.7 序列外推 | 2.8 方案对比 | 2.9 练习
- **延伸阅读**：RoPE (Su 2023)、NTK-Aware、ALiBi (Press 2022)

### 第 3 章：单头自注意力
- **产出**：Scaled Dot-Product Attention（~40行）
- **小节**：3.1 注意力动机 | 3.2 注意力直觉 | 3.3 QKV 投影 | 3.4 实现 | 3.5 √dₖ 分析 | 3.6 Softmax 温度 | 3.7 Causal Mask | 3.8 权重可视化 | 3.9 O(n²) 挑战 + MLA 预告 | 3.10 练习
- **延伸阅读**：Attention Is All You Need、The Annotated Transformer

### 第 4 章：多头注意力 + DeepSeek MLA
- **产出**：MultiHeadAttention（~60行）
- **小节**：4.1 单头→多头 | 4.2 MHA 实现 | 4.3 MHA vs MQA vs GQA | 4.4 GQA 实现 | 4.5 DeepSeek MLA：潜在向量压缩 KV | 4.6 MLA 解耦 RoPE 设计 | 4.7 注意力头行为分析 | 4.8 参数量计算 | 4.9 练习
- **延伸阅读**：GQA (Ainslie 2023)、MQA (Shazeer 2019)、DeepSeek-V2 论文

### 第 5 章：Transformer Block + DeepSeek 优化
- **产出**：TransformerBlock（~50行）
- **小节**：5.1 Decoder-only 全景 | 5.2 LayerNorm | 5.3 RMSNorm (Llama/DeepSeek) | 5.4 Pre-Norm vs Post-Norm | 5.5 FFN (GELU→SwiGLU) | 5.6 FFN 作为键值存储器 | 5.7 组装 Block | 5.8 梯度检查 | 5.9 DeepSeek V4 mHC 超连接 | 5.10 练习
- **延伸阅读**：SwiGLU (Shazeer 2020)、RMSNorm (Zhang 2019)、DeepSeek-V4 mHC 论文

### 第 6 章：完整 GPT + DeepSeekMoE 架构
- **产出**：GPT-2 124M 模型（~100行）
- **小节**：6.1 GPT-2 架构全景 | 6.2 GPTConfig | 6.3 GPTModel 组装 | 6.4 Weight Tying | 6.5 124M 参数精算 | 6.6 前向传播测试 | 6.7 HuggingFace 权重验证 | 6.8 DeepSeekMoE：稀疏激活（671B→37B） | 6.9 Aux-Loss-Free 负载均衡 | 6.10 练习
- **延伸阅读**：GPT-2 论文、nanoGPT、DeepSeek-V3 论文

### 第 7 章：训练循环 + DeepSeek 训练优化
- **产出**：完整训练脚本（~120行）
- **小节**：7.1 LM 目标 | 7.2 DataLoader | 7.3 Cross-Entropy Loss | 7.4 Perplexity | 7.5 AdamW + Gradient Clipping | 7.6 学习率调度 | 7.7 混合精度 (FP16/BF16) | 7.8 完整训练循环 | 7.9 训练监控 | 7.10 微型 GPT 训练 | 7.11 DeepSeek Muon 优化器 | 7.12 FP8/FP4 QAT | 7.13 DualPipe 流水线概述 | 7.14 练习
- **延伸阅读**：AdamW、Chinchilla、DeepSeek-V3 FP8、Muon、DualPipe

### 第 8 章：文本生成 + DeepSeek MTP
- **产出**：文本生成器（~60行）
- **小节**：8.1 自回归生成 | 8.2 Greedy Decoding | 8.3 Temperature Sampling | 8.4 Top-K | 8.5 Top-P (Nucleus) | 8.6 采样对比实验 | 8.7 生成质量评估 | 8.8 上下文窗口 | 8.9 MTP：多 Token 预测 | 8.10 推测解码 | 8.11 练习
- **延伸阅读**：Holtzman 2020、DeepSeek-V3 MTP、Speculative Decoding

### 第 9 章：微调与对齐 + DeepSeek R1 推理
- **产出**：SFT（~80行）+ LoRA（~50行）+ DPO（~30行）+ GRPO（~60行）
- **小节**：9.1 对齐必要性 | 9.2 SFT 实现 | 9.3 Instruction Data 格式 | 9.4 RLHF (Reward Model + PPO) | 9.5 GRPO：无需 Critic 的群组优化 | 9.6 R1-Zero：纯 RL 涌现推理 | 9.7 LoRA 实现 | 9.8 DPO 实现 | 9.9 On-Policy Distillation (V4) | 9.10 QLoRA | 9.11 对齐税 | 9.12 练习
- **延伸阅读**：InstructGPT、LoRA、DPO、GRPO、DeepSeek-R1 (Nature 2025)、DeepSeek-V4 OPD

### 第 10 章：推理优化 + DeepSeek V4 前沿
- **产出**：KV Cache（~60行）+ 量化示例（~40行）
- **小节**：10.1 推理瓶颈分析 | 10.2 KV Cache 实现 | 10.3 KV Cache 内存分析 | 10.4 DeepSeek V4 CSA+HCA 混合注意力 | 10.5 量化 (INT8/INT4/FP4) | 10.6 MoE 推理优化 | 10.7 RAG | 10.8 Agent 模式 | 10.9 FlashAttention | 10.10 Batch Invariance (V4) | 10.11 安全与对齐评估 | 10.12 DeepSeek V2→V4 演进路线图 | 10.13 课程总结 | 10.14 练习
- **延伸阅读**：FlashAttention、GPTQ、vLLM、DeepSeek-V4 论文

## 设计验证

- 每章 HTML 写完用 `chromium --dump-dom` 验证渲染
- CSS 包含暗色/浅色主题变量
- JS app.js 管理主题切换、进度追踪、练习校验、键盘导航
- 练习答案用 `data-answer` 属性，校验逻辑无模板字符串
