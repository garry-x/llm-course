<p align="center">
  <img src="images/favicon.svg" width="64" alt="LLM 深度学习">
</p>

<h1 align="center">LLM 深度学习</h1>

<p align="center">
  <strong>从代码出发，11 章构建一个完整的大语言模型工程体系</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/chapters-11-orange" alt="11 chapters">
  <img src="https://img.shields.io/badge/exercises-programming_+_written-blue" alt="programming and written exercises">
  <img src="https://img.shields.io/badge/sections-127-yellow" alt="127 sections">
  <img src="https://img.shields.io/badge/frontier-architecture_cases-green" alt="frontier architecture cases">
  <img src="https://img.shields.io/badge/iPad_Pro-optimized-purple" alt="iPad Pro">
  <img src="https://img.shields.io/badge/db-IndexedDB-red" alt="IndexedDB">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="license">
</p>

---

## 关于本课程

这是一门**从代码出发**的 LLM 实战课程。不做概念浏览，而是用 Python 和 PyTorch 逐行实现大语言模型的每一个核心组件。必要的数学、PyTorch、ML 和系统基础不会被拆成旁路，而是揉进每章开头的先修能力、章节内实现和验收信号里。

**每章的学习循环：**
> 深度理论 → 理解"为什么" → 编程练习（你写代码）→ 对照参考解答 → 概念练习巩固

融入 MLA、MoE、GRPO、FP8、稀疏/压缩注意力、可学习残差连接等工业级架构案例，用它们理解每个组件背后的工程瓶颈，而不是追逐单个模型版本规格。

## 初学者怎么学

这门课覆盖从基础组件到工业前沿的完整链路。第一次学习时不要把所有高级专题都当成必修，可以按三遍阅读节奏推进：

| 阶段 | 章节 | 目标 | 建议 |
|------|------|------|------|
| 第一遍：主线必学 | Ch01-Ch06 | 把文本变成 token，搭出能前向传播的 GPT | 代码练习必须动手写；DeepSeek 扩展先理解动机即可 |
| 第二遍：跑起来 | Ch07-Ch08 | 训练小模型，并让模型生成文本 | 重点看 loss、optimizer、sampling 的输入输出形状 |
| 第三遍：进阶选读 | Ch09-Ch10 | 微调、对齐、RAG、推理优化和前沿架构 | 先掌握概念地图，再回头补公式和工程细节 |

**最低前置要求：**会 Python 函数、列表/字典、基础矩阵乘法，知道 PyTorch 张量的 `shape`。如果数学推导暂时吃力，先抓住每节的“输入是什么、输出是什么、形状怎么变”。数学、PyTorch、统计和系统知识只在被章节任务用到时展开；附录用于查阅，不要求先单独学完。

## LLM 知识体系

本课程按“大模型如何被表示、计算、训练、生成、对齐和部署”组织，而不是按零散工具组织：

| 模块 | 对应章节 | 核心问题 |
|------|----------|----------|
| 表示层 | Ch01-Ch02 | 文本如何变成 token，token 如何变成向量，模型如何获得位置信息 |
| Transformer 核心 | Ch03-Ch06 | 注意力、mask、多头、GQA/MLA、Norm、FFN、MoE 和 GPT 前向传播如何组合 |
| 训练闭环 | Ch07 | next-token prediction 为什么等价于最大似然，loss、PPL、优化器、checkpoint/resume integrity 和分布式训练 gate 如何工作 |
| 生成与推理 | Ch08-Ch10 | prefill/decode、采样、推测解码、KV Cache、FlashAttention、RAG 和推理服务如何取舍 |
| 微调与对齐 | Ch09 | SFT chat template/mask/packing gate、偏好数据 gate、LoRA、偏好建模、DPO、GRPO、RLVR/RFT 如何改变模型行为 |
| 经典 NLP 与评测 | Week 8 专题 / Ch11 作业 | RNN/LSTM、dependency parsing、seq2seq、BERT/MLM、BLEU/ROUGE/F1/EM 如何连接现代 LLM |
| 前沿工程案例 | Ch04-Ch10 | MLA、MoE、FP8、GRPO、稀疏/压缩注意力等设计解决了哪些工程瓶颈 |

高校课程水准的关键不在材料数量，而在每个知识点都能回答三件事：

- 数学上它解决什么问题，公式里的每个量是什么。
- 代码上它怎样落到 PyTorch 张量、shape、mask、dtype 和梯度。
- 工程上它带来什么成本、速度、质量或稳定性的取舍。

## 章节内置基础

基础知识按章节任务就地出现。每章开头都给出“先修能力、本章内化、验收信号”，作业和书面题再把这些基础落到可运行代码或可复算推导。

| 章节 | 章节内化的基础 | 直接服务的工程判断 |
|------|----------------|--------------------|
| Ch01-Ch02 | Python 数据结构、矩阵查表、向量点积、位置旋转和 shape trace | token 成本、embedding 参数、context 利用率和 prefix cache 前提 |
| Ch03-Ch05 | softmax、mask、广播、矩阵乘法、归一化、残差路径和资源估算 | attention 正确性、GQA/MLA 显存收益、block 稳定性和 FLOPs 预算 |
| Ch06-Ch07 | 自回归概率分解、cross entropy、optimizer state、随机性和实验统计 | GPT 组装、训练曲线解释、checkpoint/resume integrity、数据 gate 和扩容判断 |
| Ch08-Ch09 | logits 分布、采样方差、KL/reference model、chat template、assistant mask、偏好数据和 reward 假设 | 生成策略上线、reasoning 预算、SFT/DPO/GRPO 质量与安全边界 |
| Ch10 | 排队、显存/带宽、KV cache、压测指标、RAG 检索指标、准入控制、发布 gate 和过载响应 | TTFT/TPOT/P95、continuous batching admission、P/D 解耦、容量规划、canary/control、load shedding 和回退 |
| Ch11 | 序列建模、结构化预测、encoder-only、传统指标和 judge 可靠性 | 选择生成/抽取/排序/结构化解码，判断评测结果能否支持上线结论 |

配套学习材料：

- [课程 Syllabus](docs/syllabus.html)：课程目标、周安排、作业节奏和项目安排。
- [10 周 / 20 讲 Lecture Plan](docs/lecture-plan.html)：每讲目标、推导、课堂 demo 和 quick check。
- [逐周阅读材料与复盘 Handout](docs/reading-list.html)：论文阅读、关键问题和复盘要求。
- [书面推导与概念题题库](docs/written-problem-set.html)：公式推导、复杂度分析和概念辨析。
- [Worked Example Pack](docs/worked-example-pack.html)：BPE、RoPE、attention、GQA、Norm、AdamW、SFT mask/packing、DPO、KV cache 等可复算小例子。
- [经典 NLP 专题 Handout](docs/classic-nlp-handout.html)：RNN/LSTM、dependency parsing、seq2seq/NMT、BERT、BLEU/ROUGE/F1/EM 与现代 LLM 的关系。

章节作业入口：[assignments/ch01_bpe/](assignments/ch01_bpe/) · [assignments/ch02_embeddings/](assignments/ch02_embeddings/) · [assignments/ch03_attention/](assignments/ch03_attention/) · [assignments/ch04_multihead/](assignments/ch04_multihead/) · [assignments/ch05_block/](assignments/ch05_block/) · [assignments/ch06_gpt/](assignments/ch06_gpt/) · [assignments/ch07_training/](assignments/ch07_training/) · [assignments/ch08_generation/](assignments/ch08_generation/) · [assignments/ch09_alignment/](assignments/ch09_alignment/) · [assignments/ch10_inference/](assignments/ch10_inference/) · [assignments/ch11_classic_nlp/](assignments/ch11_classic_nlp/)。

## 面向 LLM 推理工程师的能力路线

如果你的目标是成为 LLM 推理工程师，学习目标不只是“懂 Transformer”，而是能把模型稳定、低成本、可观测地服务给真实用户。课程按以下能力组织：

| 能力 | 对应章节 | 你需要能做什么 |
|------|----------|----------------|
| 模型结构读懂 | Ch01-Ch06 | 看懂 tokenizer、attention、KV Cache 来源、logits 输出和参数规模 |
| 生成与延迟拆解 | Ch08 | 区分 prefill/decode，解释 TTFT、TPOT、TPS、吞吐、采样质量和 reasoning 预算 |
| 显存与带宽优化 | Ch04, Ch10 | 计算 KV Cache、理解 MQA/GQA/MLA、量化、FlashAttention 和显存瓶颈 |
| 推理服务架构 | Ch10 | 选择 vLLM/SGLang/TensorRT-LLM/llama.cpp，理解 continuous batching admission、prefix cache、并发调度、load shedding、speculative decoding gate、tool-call gate 和 MCP runtime security |
| 检索与工具调用 | Ch08-Ch10 | 设计结构化输出、RAG、Agent 工具链和失败兜底 |
| 评测与上线 | Ch09-Ch10 | 设计质量/安全/延迟/成本指标，做压测、回归评估、canary/control 发布和回滚检查 |

**课程最终项目：**[LLM Inference Engineering Capstone](projects/inference-engineering-capstone/) 会带你部署一个 OpenAI-compatible Chat API：支持流式输出、结构化 JSON、工具调用、RAG、基础指标、压测报告、P50/P95/P99 延迟和 tokens/s 成本估算。先用 mock engine 跑通服务骨架，再替换为 vLLM / SGLang / TensorRT-LLM / llama.cpp。

**能力视图：**如果你想按岗位能力检查覆盖面，参考 [LLM 推理工程师能力视图](inference-engineer-curriculum.html)（详细版在 [docs/inference-engineer-curriculum.html](docs/inference-engineer-curriculum.html)）。它只重排章节产出、练习、Capstone、压测、评测和上线复盘，不替代章节学习。

## 面向 LLM 训练工程师的能力路线

如果你的目标是成为 LLM 训练工程师，学习目标要从“能跑一个 loss”推进到“能交付可复现、可恢复、可观测、成本可解释的训练系统”。课程按以下能力组织：

| 能力 | 对应章节 | 你需要能做什么 |
|------|----------|----------------|
| 数据与 Token 预算 | Ch01, Ch07 | 分析样本、重复、质量过滤、eval contamination、领域混合、长度分布和 token 规模，估算训练 step |
| 训练循环工程 | Ch06-Ch07 | 组织 PyTorch Dataset/DataLoader、forward、loss、backward、optimizer、scheduler |
| 稳定性与恢复 | Ch07 | 使用 seed、grad clipping、checkpoint integrity、distributed resume 和异常排查保护训练 |
| 监控与评测 | Ch07-Ch09 | 记录 train_loss、val_loss、ppl、lr、grad_norm、tokens/s，并解释曲线 |
| 微调与对齐 | Ch09 | 区分 SFT/偏好数据 gate、LoRA、DPO、GRPO、RLVR/RFT 的数据格式、损失和适用场景 |
| 分布式与成本 | Ch07, Ch10 | 理解 AMP、FSDP/ZeRO、global batch tokens、MFU、GPU hours、distributed checkpoint、checkpoint 存储和 scale rehearsal |

**训练最终项目：**[LLM Training Engineering Capstone](projects/training-engineering-capstone/) 会带你实现一个 PyTorch 字符级语言模型训练闭环：数据分析、data curation gate、训练、开发集监控、checkpoint/resume integrity、metrics、训练规划和分布式策略账本。默认模型很小，CPU 可跑通；报告仍需解释目标规模下数据过滤/去重/混合、DDP/ZeRO/FSDP、低精度、MFU、checkpoint state 和 reshard 的工程边界。

**能力视图：**按 [LLM 训练工程师能力视图](training-engineer-curriculum.html)（详细版在 [docs/training-engineer-curriculum.html](docs/training-engineer-curriculum.html)）检查训练报告、指标日志、checkpoint 恢复说明和成本规划是否覆盖完整。

## 快速开始

### 本地开发

```bash
git clone https://github.com/garry-x/llm-course.git && cd llm-course

./serve.sh                    # 默认 0.0.0.0:8080
./serve.sh serve -p 3000      # 指定端口
```

### 运行作业测试

本仓库推荐使用根目录下的 `.venv` 运行本地代码；如果你已经激活等价虚拟环境，也可以把 `.venv/bin/python` 替换为 `python`。先确认 PyTorch 可导入：

```bash
.venv/bin/python -c "import sys, torch; print(sys.version.split()[0], torch.__version__)"
.venv/bin/python run_assignment_tests.py
```

### CLI 命令一览

| 命令 | 说明 | 支持 `-p` |
|------|------|:---------:|
| `serve` | 本地 Python HTTP 服务器 | ✓ |

**环境要求：** Python 3.10+ / 现代浏览器（Safari / Chrome / Edge）；推荐 iPad Pro 或桌面端阅读。

## 课程大纲

| # | 章节 | 编程产出 | 练习 |
|---|------|---------|:--:|
| 1 | **环境搭建与分词** — 实现 BPE Tokenizer | `BPETokenizer` ~80行 | 5+5 |
| 2 | **嵌入层与位置编码** — TokenEmbedding + RoPE + 上下文学习导论 | `TokenEmbedding` + `RoPE` ~60行 | 4+5 |
| 3 | **单头自注意力** — Scaled Dot-Product Attention | `ScaledDotProductAttention` ~40行 | 5+5 |
| 4 | **多头注意力与 MLA** — MHA → GQA → DeepSeek MLA | `MultiHeadAttention` ~60行 | 5+5 |
| 5 | **Transformer Block** — RMSNorm + FFN/SwiGLU + mHC | `TransformerBlock` ~50行 | 5+5 |
| 6 | **组装 GPT + DeepSeekMoE** — GPT-2 124M 完整模型 | `GPTModel` ~100行 | 5+5 |
| 7 | **训练循环** — AdamW/Muon + FP8/MXFP8 + 分布式策略账本 | 完整训练脚本 + strategy/gate report | 7+5 |
| 8 | **文本生成** — 采样策略 + reasoning budget + MTP 推测解码 + 约束生成 | 文本生成器 + test-time compute gate | 7+5 |
| 9 | **微调与对齐** — SFT/偏好数据 Gate/LoRA/DPO/GRPO/RLVR + R1 推理 | SFT + post-training data audit + LoRA + GRPO/RLVR ~240行 | 8+5 |
| 10 | **推理优化与前沿** — KV Cache/量化/RAG/Structured Output/Tool/MCP Gate/vLLM/Triton/生产发布/长上下文/多模态 | KV Cache + 量化 + RAG + structured output gate + Tool/MCP Gate + rollout gate + overload response + continuous batching admission + P/D pool plan + speculative gate + long-context gate + LSH + 服务蓝图 | 11+5 |
| 专题 | **经典 NLP 与评测** — RNN/LSTM / dependency parsing / seq2seq / BERT / metrics | RNN gradient path + UAS/LAS + BLEU/ROUGE/EM/F1 + judge audit + MLM mask | Ch11 |

> **总计：覆盖 11 章编程作业、书面推导题、经典 NLP 专题作业和两个工程 Capstone。**

## DeepSeek 技术融入

下表用于建立技术地图。具体论文和模型卡请在学习对应章节时打开原文阅读。

| 技术 | 对应章节 | 学习重点 |
|------|---------|----------|
| MLA (Multi-head Latent Attention) | Ch04 | KV Cache 压缩，潜在向量解耦 RoPE |
| GRPO (Group Relative Policy Optimization) | Ch09 | 无需 Critic，组内白化优势，RL 激励推理能力 |
| RLVR / RFT | Ch09 | 用可验证 grader 训练 reasoning，并检查 reward signal、成本和 hacking 风险 |
| DeepSeekMoE + Aux-Loss-Free | Ch06 | 稀疏激活、专家路由和动态偏置负载均衡 |
| FP8 Mixed Precision + DualPipe | Ch07 | 低精度训练、缩放策略、通信计算重叠 |
| MTP (Multi-Token Prediction) | Ch08 | 训练辅助目标和推测解码草稿信号 |
| DSA / CSA / HCA | Ch10 | 长上下文稀疏注意力与 KV/计算成本压缩 |
| Engram 外部记忆 | Ch10 | 模型外部记忆、LSH 检索和 RAG 的差异 |
| mHC (Manifold-Constrained Hyper-Connections) | Ch05 | Birkhoff 约束、Sinkhorn-Knopp 和残差连接扩展 |
| Muon Optimizer | Ch07 | 动量矩阵正交化和大规模优化器设计 |

## 项目结构

```
llm-course/
├── index.html                # 课程首页：Hero + 仪表板 + 章节目录
├── inference-engineer-curriculum.html # 推理工程师能力视图
├── training-engineer-curriculum.html  # 训练工程师能力视图
├── css/style.css              # 暖色 editorial 风格，暗色/浅色双主题
├── js/
│   ├── db.js                  # IndexedDB 持久化存储层
│   └── app.js                 # 搜索/主题/字号/进度/笔记/TOC/键盘导航
├── chapters/                  # 11 章，纯 HTML
│   └── ch01.html ~ ch11.html
├── docs/
│   ├── syllabus.md              # 课程目标、周安排、作业和项目结构
│   ├── lecture-plan.md          # 10 周 / 20 讲授课计划
│   ├── reading-list.md          # 逐周论文与技术报告阅读
│   ├── written-problem-set.md   # 书面推导与概念题
│   ├── worked-example-pack.md   # 可复算小例子
│   ├── math-prerequisites.md    # 数学先修
│   ├── classic-nlp-handout.md   # 经典 NLP 专题
│   ├── inference-engineer-curriculum.md  # 推理工程师能力视图
│   └── training-engineer-curriculum.md   # 训练工程师能力视图
├── projects/
│   ├── inference-engineering-capstone/
│   │   ├── acceptance.py      # 项目脚本：health + 评测 + 压测 + SLO + 容量估算
│   │   ├── app.py             # OpenAI-compatible Chat API + SSE + RAG stub + metrics
│   │   ├── benchmark.py       # 并发压测，输出 P50/P95/P99、TTFT/TPOT、tokens/s
│   │   ├── capacity_plan.py   # 显存、最大 batch 和每 1M tokens 成本估算
│   │   ├── evaluate.py        # 固定评测集回归检查
│   │   ├── slo_check.py       # 读取压测 JSON，检查延迟/吞吐/错误率 SLO
│   │   └── eval_cases.jsonl
│   └── training-engineering-capstone/
│       ├── acceptance.py      # 项目脚本：数据分析 + 训练 + resume + 规划
│       ├── data_profile.py      # 语料行数、重复、长度和字符规模分析
│       ├── plan_training.py   # step、GPU hours、成本和 checkpoint 存储估算
│       ├── train.py           # PyTorch tiny LM 训练循环 + checkpoint/resume
│       └── sample_corpus.txt
├── images/                    # 11 张 SVG 概念示意图 + favicon（支持暗色模式）
│   ├── bpe-pipeline.svg       # BPE 训练与编解码流程
│   ├── rope-rotation.svg      # RoPE 旋转位置编码原理
│   ├── attention-flow.svg     # Scaled Dot-Product Attention 数据流
│   ├── transformer-arch.svg   # GPT 架构全景
│   ├── mha-gqa-mla.svg        # MHA / GQA / MLA KV Cache 压缩对比
│   ├── transformer-block.svg  # Transformer Block 内部结构
│   ├── gpt-params.svg         # GPT-2 124M 参数分解
│   ├── training-loop.svg      # 训练循环 + 优化器演进
│   ├── sampling-strategies.svg# 4 种采样策略对比
│   ├── rlhf-dpo-grpo.svg      # RLHF / DPO / GRPO 对齐方法对比
│   ├── gpu-memory.svg         # GPU 内存层次 — A100 架构
│   └── favicon.svg/.png/.ico  # ComfyUI + FLUX.1-dev 生成
├── serve.sh                   # CLI: 本地静态服务器
└── README.md
```

## 页面特性

| 特性 | 说明 |
|------|------|
| 👤 **用户账户** | 多账户切换，随机头像颜色，localStorage + IndexedDB 持久化 |
| 📝 **章节笔记** | 右下角滑出面板，自动关联当前阅读小节，按用户隔离 |
| 💾 **IndexedDB 存储** | 双写策略：localStorage 缓存(即时) + IDB 持久化(备份)，不丢数据 |
| 🎨 **暗色/浅色双主题** | CSS 变量驱动，一键切换，localStorage 持久化 |
| 📝 **编程练习驱动** | 每章 4-6 道编程题，参考解答可折叠（`LLM.toggleSolution`） |
| 📐 **KaTeX 数学渲染** | 内联 + 块级公式，渲染失败红色降级显示 LaTeX 源码 |
| 🔍 **章节搜索** | 侧边栏按章节标题/描述实时过滤 |
| 📑 **自动目录生成** | JS 读取 `section.card` 生成 TOC，scroll 高亮当前小节 |
| 📊 **阅读进度条** | 顶部 3px 渐变，GPU 合成（`transform: scaleX` + rAF 节流） |
| 📋 **代码复制** | Clipboard API + `execCommand` HTTP 回退，📋→✓ 反馈 |
| ⌨️ **键盘导航** | ← → 切换章节，Esc 关闭侧边栏 |
| 📱 **响应式** | 桌面 / iPad Pro / 手机三级断点（960/640px），触控 ≥44px |
| 🔤 **可调字号** | 小(14px) / 中(16px) / 大(18px)，localStorage 持久化 |
| 🖼️ **11 张 SVG 图表** | CSS filter 暗色适配（`invert + hue-rotate`） |
| 🏷️ **矢量 favicon** | SVG/PNG/ICO + apple-touch-icon (ComfyUI + FLUX.1-dev 生成) |

## 延伸阅读

**基础论文：**
- Vaswani et al. (2017) — [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- Radford et al. (2019) — [Language Models are Unsupervised Multitask Learners (GPT-2)](https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)
- Hoffmann et al. (2022) — [Training Compute-Optimal Large Language Models (Chinchilla)](https://arxiv.org/abs/2203.15556)

**前沿架构案例：**
- DeepSeek-V2 — [MLA + DeepSeekMoE](https://arxiv.org/abs/2405.04434) · DeepSeek-V3 — [FP8 + MTP + Aux-Loss-Free](https://arxiv.org/abs/2412.19437) · DeepSeek-R1 — [GRPO 与推理行为](https://arxiv.org/abs/2501.12948) · Kimi k1.5 — [Scaling RL with LLMs](https://arxiv.org/abs/2501.12599)

**动手实践：**
- Andrej Karpathy — [Neural Networks: Zero to Hero](https://www.youtube.com/playlist?list=PLAqhIrjkxBUWIvTOCzB7XwZBt03h4H3kW) · [nanoGPT](https://github.com/karpathy/nanoGPT)
- Sebastian Raschka — [Build a Large Language Model (From Scratch)](https://www.manning.com/books/build-a-large-language-model-from-scratch)
- 南京大学 — [LLM 从零到一实现之路](https://github.com/NJUDeepEngine/llm-course-lecture)

**推理与部署：**
- Kwon et al. (2023) — [vLLM: Efficient Memory Management for Large Language Model Serving](https://arxiv.org/abs/2309.06180)
- Tillet et al. (2019) — [Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations](https://dl.acm.org/doi/10.1145/3315508.3329973)
- Dao et al. (2022) — [FlashAttention: Fast and Memory-Efficient Exact Attention](https://arxiv.org/abs/2205.14135)
- Frantar et al. (2023) — [GPTQ: Accurate Post-Training Quantization for GPT](https://arxiv.org/abs/2210.17323)

**对齐与微调：**
- Hu et al. (2021) — [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
- Rafailov et al. (2023) — [Direct Preference Optimization (DPO)](https://arxiv.org/abs/2305.18290)
- Ouyang et al. (2022) — [Training Language Models to Follow Instructions (InstructGPT)](https://arxiv.org/abs/2203.02155)
