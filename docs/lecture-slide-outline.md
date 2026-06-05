# Lecture Slide Outline

本文件提供 20 讲课件大纲，用于把 HTML 章节、reading list、written problems、assignments 和 capstone 组织成可直接制作 slides 的授课材料。它不是已发布的 PDF slides；正式开课时，教师应按 [Course Materials Index](course-materials-index.md) 记录 slides 的发布日期、版本和可访问性替代材料。代表性 deck 的 slide-by-slide 样例见 [Lecture Slide Sample Pack](lecture-slide-sample-pack.md)。每讲 notes、板书推导和复盘问题见 [Lecture Notes Index](lecture-notes-index.md)，每讲 notes 的 notation、derivation、shape、code binding、source boundary 和 correction path 按 [Lecture Notes Quality and Review Standard](lecture-notes-quality-review.md) 审查，可直接板书的推导脚本见 [Board Derivation and Instructor Notes Pack](board-derivation-pack.md)，课堂演示的可运行命令见 [Classroom Demo Runbook](demo-runbook.md)。

## 使用规则

- 每讲建议 35-45 张 slides，80 分钟课堂留出 10-15 分钟 quick check 或 demo。
- 每讲 slides 必须包含：学习目标、核心公式或代码、1 个课堂 demo、1 个 quick check、课后证据。
- 公式符号必须与章节正文一致；若 slide 为了空间省略推导，必须指向章节或 handout。
- slides 中的核心公式、shape 和前沿 claim 必须能映射到 reviewed notes 或 review_record。
- 前沿模型 claim 必须标注来源等级和复核日期；不把模型卡声明写成普遍事实。
- 若使用图片、录屏或复杂图表，应提供文字替代说明，按 [Accessibility and Student Support Guide](accessibility-student-support.md) 执行。

## Slide Deck 模板

| Slide 组 | 内容 | 证据 |
|----------|------|------|
| Opening | 本讲目标、前置知识、与上一讲连接 | syllabus outcome 或 lecture plan |
| Concept | 核心概念、动机、失败案例 | 章节正文、reading list |
| Math | 关键公式、shape、复杂度、边界条件 | written problem 或 math prerequisites |
| Code | 伪代码、PyTorch API、测试目标 | assignment starter/tests |
| Demo | 课堂运行或白板推导 | demo 命令、预期输出、失败排查 |
| Check | quick check / exit ticket | quiz-checkpoint guide |
| Evidence | 课后提交、rubric、下一讲准备 | assignment / project / reading recap |

## 20 讲课件大纲

| 讲次 | Slide 标题 | 核心 slides | Demo / 板书 | Quick check | 课后证据 |
|------|------------|-------------|-------------|-------------|----------|
| L1 | Course Setup, PyTorch, BPE | 课程目标；评分结构；BPE merge 直觉；byte-level tokenizer；复杂度 | 手算 3 轮 BPE merge；运行 Ch01 tokenizer test | 贪心 merge 为什么不保证全局最优 | Ch01 starter、reading recap |
| L2 | Embeddings, Word Vectors, RoPE | embedding lookup；word2vec/GloVe 经验结构；sinusoidal PE；RoPE 旋转 | 画 RoPE 2D block；验证相对位置点积 | 类比现象是否由训练目标保证 | Ch02 RoPE 数值验证 |
| L3 | Scaled Dot-Product Attention | Q/K/V；方差缩放；softmax；mask 前后差异；attention 复杂度 | 手算 3-token attention；错误 mask 对比 | 为什么 mask 应在 softmax 前应用 | Ch03 attention tests |
| L4 | Causal Mask, Backprop, Parsing Preview | causal LM 数据流；attention backward 形状；dependency parsing 预告 | 白板推导 causal mask；transition parser 小例子 | attention heatmap 能否直接解释模型理由 | Ch03 written problem |
| L5 | Multi-Head Attention and GQA | MHA reshape；head 子空间；MQA/GQA cache；参数量等价 | MHA/GQA 参数量和 KV cache 表格 | head 更多是否必然更好 | Ch04 starter |
| L6 | MLA, Norm, FFN, Block | latent cache；RoPE 解耦；LayerNorm/RMSNorm；SwiGLU；pre-norm block | 修正 RoPE/MLA 可交换性板书；block grad flow | RoPE 为什么不是“非线性操作” | Ch05 starter |
| L7 | GPT Model Assembly | decoder-only stack；weight tying；GPT-2 config；参数审计 | 从 config 估算 GPT-2 small 参数量 | vocab/tied weights 如何影响参数量 | Ch06 GPTModel tests |
| L8 | MoE, Routing, Memory Audit | top-k routing；capacity；load balancing；DeepSeekMoE 边界 | router bias update 可视化；显存组成表 | 激活参数少是否等于服务成本线性降低 | Ch06 written problem |
| L9 | Dataset, CE, AdamW, Scheduler | next-token dataset；cross entropy；ignore index；AdamW；warmup/cosine | 手算 CE；AdamW 单步更新 | AdamW 与 L2 penalty 的差别 | Ch07 starter |
| L10 | Training Loop, Checkpoint, Scaling | train/eval loop；checkpoint/resume；loss/PPL；训练成本估算 | 运行训练 capstone acceptance；读 loss log | PPL 是否等于事实正确率 | training proposal |
| L11 | Generation and Sampling | prefill/decode；greedy；temperature；top-k；top-p；degeneration | 比较 top-k/top-p 样本；重复率和 distinct-n | top-p 如何保留最小 nucleus | Ch08 starter |
| L12 | Speculative and Structured Decoding | draft/target；接受率；MTP；约束解码；schema 校验 | 简化 speculative decoding；JSON schema 失败案例 | 无损采样条件与系统加速条件区别 | Ch08 written problem |
| L13 | SFT and LoRA | instruction format；prompt mask；LoRA rank/scaling；merge | LoRA 参数量计算；mask prompt loss | prompt token 计入 loss 会改变什么 | Ch09 starter |
| L14 | DPO, GRPO, Alignment Boundaries | preference pairs；reference model；DPO log-ratio；GRPO whitening；安全边界 | 手算 DPO 方向；GRPO group advantage | chosen/rejected 方向写反会怎样 | Ch09 written problem |
| L15 | Classic NLP and Evaluation | dependency parsing；seq2seq/NMT；BERT/MLM；BLEU/ROUGE/EM/F1；encoder/decoder 对比 | UAS/LAS 例题；beam length bias；MLM labels；QA normalization | BLEU 能否证明开放式回答质量 | Ch11 supplement + [classic-nlp-deep-dive-module.md](classic-nlp-deep-dive-module.md) |
| L16 | Ethics, Safety, Data Review | 数据来源；许可证；PII；bias；benchmark contamination；模型卡边界 | 填写 data/ethics review 表；污染案例 | benchmark 数字必须带哪些字段 | data/ethics review |
| L17 | KV Cache, Quantization, RAG | KV cache 公式；batch/seq/layer/dtype；INT8；RAG retrieval | 计算 KV 显存；RAG prompt construction | 相似文档命中是否保证事实正确 | Ch10 starter |
| L18 | Serving, Benchmark, SLO, Capacity | OpenAI-compatible API；TTFT/TPOT；P95/P99；capacity plan | 跑 inference benchmark；读 SLO 报告 | 平均延迟为什么不够 | inference proposal |
| L19 | Capstone Reproducibility Rehearsal | 复现包；seed；日志；错误分析；report rubric | acceptance dry run；同伴复现实验 | 最强证据和最大风险分别是什么 | project draft + peer review |
| L20 | Final Presentation and Course Review | outcome map 回顾；项目展示；来源审计；未来学习路线 | final report checklist；课程复盘表 | 哪个结论仍需更强证据 | final report + presentation |

## 教师备注模板

每讲备课前填写：

```text
Lecture:
Date:
Slides version:
Required reading checked:
External claims rechecked:
Demo command:
Expected output:
Known failure modes:
Accessibility notes:
Post-lecture action items:
```

## 发布前 Checklist

- 每讲 slide outline 能映射到 [Course Materials Index](course-materials-index.md) 的 20 讲。
- 每讲至少有一个可评分证据：assignment、written problem、reading recap、checkpoint 或 capstone。
- 每讲 quick check 能在 [Quiz and Checkpoint Guide](quiz-checkpoint-guide.md) 中找到题型或补救路径。
- 使用的外部来源已在 [reading-list.md](reading-list.md)、[chapter-source-map.md](chapter-source-map.md) 或 [frontier-source-audit.md](frontier-source-audit.md) 中登记。
- 发布 slides 或录屏后更新 materials index 和 operations log。
