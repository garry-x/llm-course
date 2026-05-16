# LLM 深度学习

从代码出发，10 章构建一个完整的大语言模型。每一行代码都值得自己敲一遍。

## 课程结构

| 章 | 标题 | 编程练习 | 概念练习 |
|---|------|---------|---------|
| 1 | 环境搭建与分词 — 实现 BPE Tokenizer | 5 | 5 |
| 2 | 嵌入层与位置编码 — TokenEmbedding + RoPE | 4 | 5 |
| 3 | 单头自注意力 — Scaled Dot-Product Attention | 5 | 5 |
| 4 | 多头注意力与 MLA — MHA→GQA→DeepSeek MLA | 5 | 5 |
| 5 | Transformer Block — RMSNorm+FFN+SwiGLU+mHC | 5 | 5 |
| 6 | 组装完整 GPT 模型 — GPT-2 124M + DeepSeekMoE | 5 | 5 |
| 7 | 训练循环 — AdamW/Muon+FP8+DualPipe | 6 | 5 |
| 8 | 文本生成 — 采样策略 + MTP 推测解码 | 6 | 5 |
| 9 | 微调与对齐 — SFT/LoRA/DPO/GRPO | 6 | 5 |
| 10 | 推理优化与前沿 — KV Cache/量化/RAG/Agent | 5 | 5 |

**总计：52 道编程练习 + 50 道概念练习**

## 快速开始

```bash
# 启动本地服务器
./serve.sh

# 或指定端口
./serve.sh -p 3000

# 浏览器打开
# http://localhost:8080
```

## 技术栈

- 纯 HTML/CSS/JS，零依赖构建工具
- KaTeX 数学公式渲染
- 7 张 SVG 概念示意图（支持暗色/浅色双主题）
- CSS 变量驱动的暗色模式
- 响应式：桌面 / iPad Pro / 手机三级适配

## 特性

- **编程驱动**：每章要求读者动手写代码，参考解答可折叠
- **深度理论**：信息论、方差分析、梯度行为、Bradley-Terry 模型等
- **现代 LLM 覆盖**：DeepSeek V2(MLA)→R1(GRPO)→V3(FP8/MoE)→V4(CSA+HCA/mHC)
- **iPad Pro 优化**：触控目标 ≥44px，三级响应式断点
- **可调字号**：小/中/大三档，localStorage 持久化
- **学习进度追踪**：章节完成状态跨页面保存
- **全文搜索**：侧边栏按章节标题搜索
- **键盘导航**：← → 切换章节，Esc 关闭侧边栏

## 延伸阅读

- Vaswani et al. (2017) — [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- DeepSeek-V2 — [MLA 原始论文](https://arxiv.org/abs/2405.04434)
- DeepSeek-V3 — [技术报告](https://arxiv.org/abs/2412.19437)
- DeepSeek-R1 — [Nature 2025](https://www.nature.com/articles/s41586-025-09095-6)
- Sebastian Raschka — [Build a Large Language Model (From Scratch)](https://www.manning.com/books/build-a-large-language-model-from-scratch)
- Andrej Karpathy — [Neural Networks: Zero to Hero](https://www.youtube.com/playlist?list=PLAqhIrjkxBUWIvTOCzB7XwZBt03h4H3kW)
- 南京大学 — [LLM 从零到一实现之路](https://github.com/NJUDeepEngine/llm-course-lecture)
