<p align="center">
  <img src="favicon.svg" width="64" alt="LLM 深度学习">
</p>

<h1 align="center">LLM 深度学习</h1>

<p align="center">
  <strong>从代码出发，10 章构建一个完整的大语言模型</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/chapters-10-orange" alt="10 chapters">
  <img src="https://img.shields.io/badge/exercises-102_(52编程+50概念)-blue" alt="102 exercises">
  <img src="https://img.shields.io/badge/DeepSeek-V2→R1→V3→V4-green" alt="DeepSeek">
  <img src="https://img.shields.io/badge/iPad_Pro-optimized-purple" alt="iPad Pro">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="license">
</p>

---

## 关于本课程

这是一门**从代码出发**的 LLM 实战课程。不做概念浏览，而是用 Python 和 PyTorch 逐行实现大语言模型的每一个核心组件。

**每章的学习循环：**
> 深度理论 → 理解"为什么" → 编程练习（你写代码）→ 对照参考解答 → 概念练习巩固

融入 **DeepSeek 开源技术体系**（V2 MLA → R1 GRPO → V3 FP8/MoE → V4 CSA+HCA/mHC），用真实的工业级设计来理解每一个组件。

## 快速开始

```bash
git clone <repo-url> && cd llm-learner
./serve.sh            # 默认 0.0.0.0:8080
./serve.sh -p 3000    # 指定端口
# 浏览器打开 http://localhost:8080
```

**环境要求：** Python 3.10+ / PyTorch / 现代浏览器（Safari / Chrome / Edge），推荐 iPad Pro 或桌面端阅读。

## 课程大纲

| # | 章节 | 编程产出 | 练习 |
|---|------|---------|:--:|
| 1 | **环境搭建与分词** — 实现 BPE Tokenizer | `BPETokenizer` ~80行 | 5+5 |
| 2 | **嵌入层与位置编码** — TokenEmbedding + RoPE | `TokenEmbedding` + `RoPE` ~60行 | 4+5 |
| 3 | **单头自注意力** — Scaled Dot-Product Attention | `ScaledDotProductAttention` ~40行 | 5+5 |
| 4 | **多头注意力与 MLA** — MHA → GQA → DeepSeek MLA | `MultiHeadAttention` ~60行 | 5+5 |
| 5 | **Transformer Block** — RMSNorm + FFN/SwiGLU + mHC | `TransformerBlock` ~50行 | 5+5 |
| 6 | **组装 GPT + DeepSeekMoE** — GPT-2 124M 完整模型 | `GPTModel` ~100行 | 5+5 |
| 7 | **训练循环** — AdamW/Muon + FP8/FP4 + DualPipe | 完整训练脚本 ~120行 | 6+5 |
| 8 | **文本生成** — 4 种采样策略 + MTP 推测解码 | 文本生成器 ~60行 | 6+5 |
| 9 | **微调与对齐** — SFT/LoRA/DPO/GRPO + R1 推理 | SFT + LoRA + GRPO ~190行 | 6+5 |
| 10 | **推理优化与前沿** — KV Cache/量化/RAG/Agent | KV Cache + 量化 ~100行 | 5+5 |

> **总计：52 道编程练习 + 50 道概念练习，约 9 小时学习时间**

## DeepSeek 技术融入

| 技术 | 来源 | 对应章节 | 要点 |
|------|------|---------|------|
| MLA (Multi-head Latent Attention) | V2 | Ch04 | KV Cache 压缩 93%，潜在向量解耦 RoPE |
| GRPO (Group Relative Policy Optimization) | R1 | Ch09 | 无需 Critic，组内白化优势，纯 RL 涌现推理 |
| DeepSeekMoE + Aux-Loss-Free | V3 | Ch06 | 671B→37B 稀疏激活，动态偏置负载均衡 |
| FP8 Mixed Precision + DualPipe | V3 | Ch07 | 首个大规模 FP8 验证，通信计算重叠 |
| MTP (Multi-Token Prediction) | V3 | Ch08 | 训练/推理双重增益，推测解码 ~1.8x 加速 |
| CSA + HCA Hybrid Attention | V4 | Ch10 | 4x/128x 压缩，1M 上下文仅 27% FLOPs |
| mHC (Manifold Hyper-Connections) | V4 | Ch05 | Birkhoff 约束，Sinkhorn-Knopp，谱范数保证 |
| Muon Optimizer | V4 | Ch07 | 矩阵正交化替代 AdamW，Newton-Schulz 迭代 |

## 项目结构

```
llm-learner/
├── index.html              # 课程首页：仪表板 + 章节目录
├── css/style.css            # 暖色 editorial 风格，暗色/浅色双主题
├── js/app.js                # 主题/字号/进度/搜索/练习/TOC/键盘导航
├── chapters/
│   ├── ch01.html ~ ch10.html         # 10 章，纯 HTML（6578 行）
├── images/                  # 7 张 SVG 概念示意图
│   ├── bpe-pipeline.svg     #   BPE 训练与编解码流程
│   ├── rope-rotation.svg    #   RoPE 旋转位置编码原理
│   ├── attention-flow.svg   #   Scaled Dot-Product Attention 数据流
│   ├── transformer-arch.svg #   GPT 架构全景
│   ├── mha-gqa-mla.svg      #   MHA/GQA/MLA KV Cache 压缩对比
│   ├── training-loop.svg    #   训练循环 + 优化器演进
│   └── rlhf-dpo-grpo.svg    #   RLHF/DPO/GRPO 对齐方法对比
├── serve.sh                 # 本地服务器启动脚本
├── favicon.ico              # ComfyUI + FLUX.1-dev 生成
└── README.md
```

## 页面特性

| 特性 | 说明 |
|------|------|
| 🎨 **暗色/浅色双主题** | CSS 变量驱动，一键切换，localStorage 持久化 |
| 📝 **编程练习驱动** | 每章 4-6 道编程题，参考解答可折叠 |
| 📐 **KaTeX 数学渲染** | 内联 + 块级公式，`throwOnError` + 红色降级显示 |
| 🔍 **全文搜索** | 侧边栏按章节标题/描述实时过滤 |
| 📑 **自动目录生成** | JS 读取 `section.card` 生成 TOC，scroll 高亮 |
| 📊 **阅读进度条** | 顶部 3px 渐变色，GPU 合成（transform，不触发 layout） |
| 📋 **代码复制** | Clipboard API + `execCommand` HTTP 回退 |
| ⌨️ **键盘导航** | ← → 切换章节，Esc 关闭侧边栏 |
| 📱 **响应式** | 桌面 / iPad Pro / 手机三级断点（960/640px），触控 ≥44px |
| 🔤 **可调字号** | 小(14px) / 中(16px) / 大(18px) 三档 |

## 延伸阅读

**基础论文：**
- Vaswani et al. (2017) — [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- Radford et al. (2019) — [Language Models are Unsupervised Multitask Learners (GPT-2)](https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)
- Hoffmann et al. (2022) — [Training Compute-Optimal Large Language Models (Chinchilla)](https://arxiv.org/abs/2203.15556)

**DeepSeek 系列：**
- DeepSeek-V2 — [MLA + DeepSeekMoE](https://arxiv.org/abs/2405.04434) · V3 — [FP8 + MTP + Aux-Loss-Free](https://arxiv.org/abs/2412.19437) · R1 — [GRPO 推理涌现 (Nature 2025)](https://www.nature.com/articles/s41586-025-09095-6) · V4 — [CSA+HCA + mHC](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)

**动手实践：**
- Andrej Karpathy — [Neural Networks: Zero to Hero](https://www.youtube.com/playlist?list=PLAqhIrjkxBUWIvTOCzB7XwZBt03h4H3kW) · [nanoGPT](https://github.com/karpathy/nanoGPT)
- Sebastian Raschka — [Build a Large Language Model (From Scratch)](https://www.manning.com/books/build-a-large-language-model-from-scratch)
- 南京大学 — [LLM 从零到一实现之路](https://github.com/NJUDeepEngine/llm-course-lecture)

**前沿技术：**
- Dao et al. (2022) — [FlashAttention: Fast and Memory-Efficient Exact Attention](https://arxiv.org/abs/2205.14135)
- Hu et al. (2021) — [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
- Rafailov et al. (2023) — [Direct Preference Optimization (DPO)](https://arxiv.org/abs/2305.18290)
- Ouyang et al. (2022) — [Training Language Models to Follow Instructions (InstructGPT)](https://arxiv.org/abs/2203.02155)
