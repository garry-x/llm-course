# 前沿模型来源等级与复核记录

复核日期：2026-06-05

本表用于约束 DeepSeek、长上下文、稀疏注意力、对齐和推理系统等快速变化内容。课程正文可以讲前沿案例，但必须区分“稳定基础理论”和“模型卡/技术报告中的当前声明”。外部链接失效、模型卡变更、API 价格和 benchmark 更新按 [External Source Verification Guide](external-source-verification.md) 处理；逐条 claim 复核记录按 [Claim Audit Worksheet](claim-audit-worksheet.md) 维护；本轮外部抽查证据卡见 [Frontier Source Evidence Cards](frontier-source-evidence-cards.md)；独立审阅流程按 [External Expert Review Dossier](external-expert-review-dossier.md) 归档。

## 来源等级

| 等级 | 说明 | 可用于 |
|------|------|--------|
| A | 论文、官方技术报告、官方模型卡、官方 API 文档、官方代码仓库 | 正文事实、作业题、项目要求 |
| B | 主流框架官方文档、Transformers/vLLM/SGLang 等实现文档 | 工程实现说明、兼容性说明 |
| C | 新闻报道、第三方博客、社区总结 | 背景材料，不单独作为课程事实依据 |
| D | 社交媒体、论坛、未署名搬运 | 只能作为待验证线索 |

## DeepSeek 技术声明复核表

| 声明 | 课程位置 | 当前来源等级 | 复核结论 |
|------|----------|--------------|----------|
| DeepSeek-V2/V3 使用 MLA 和 DeepSeekMoE；V3 为 671B total / 37B activated，并使用 auxiliary-loss-free load balancing 和 MTP | Ch04、Ch06、Ch08、README | A | DeepSeek-V3 技术报告摘要明确写到 MLA、DeepSeekMoE、671B/37B、auxiliary-loss-free 和 MTP，可作为正文事实 |
| DeepSeek-V3 预训练 14.8T tokens，训练约 2.788M H800 GPU hours，训练过程稳定 | Ch07/扩展阅读 | A | 技术报告摘要给出这些数字；正文若使用必须标注为 DeepSeek 报告值 |
| DeepSeek-R1 通过 RL 激励推理能力，出现自我反思/验证等推理模式；论文有 Nature 2025 版本 | Ch09 | A | arXiv 页面显示 v2、Nature volume 645，并摘要描述 pure RL 激励推理能力 |
| DeepSeek-V3.2-Exp 引入 DeepSeek Sparse Attention (DSA)，目标是长上下文训练/推理效率 | Ch10、README | A | DeepSeek API 新闻页明确说明 V3.2-Exp、DSA、长上下文效率和开源发布；正文只按该发布说明讲工程案例，不把未再次复核的 benchmark 外推 |
| DeepSeek-V4-Pro/Flash 支持 1M context；V4-Pro 为 1.6T total / 49B activated，V4-Flash 为 284B / 13B activated | Ch09、Ch10、README | A | DeepSeek-V4-Pro 模型卡给出 preview release、参数量、激活参数和 1M context |
| DeepSeek-V4 的 CSA+HCA 在 1M context 下相对 V3.2 使用 27% single-token inference FLOPs 和 10% KV cache | Ch10、README | A | DeepSeek-V4-Pro 模型卡介绍中给出该相对数字；正文必须写成“模型卡报告” |
| DeepSeek-V4 包含 mHC、Muon optimizer、on-policy distillation 和三档 reasoning effort modes | Ch05、Ch07、Ch09、README | A | DeepSeek-V4-Pro 模型卡列出 mHC、Muon、post-training/on-policy distillation 和三种 reasoning modes |
| DeepSeek-V4 与 MTP/推测解码的更深集成 | Ch08 | D | 无当前 A 级来源支撑；Ch08 只保留为 monitor-only 复核规则，必须有后续模型卡或技术报告才可升级，不作为当前课程事实 |
| Engram 外部记忆、NIAH 84.2% 到 97.0% | Ch10、README | D | 具体 NIAH 数字已从正文和 README 移除；Engram 仅保留为 monitor-only 前沿案例，不作为当前课程事实，也不进入作业或考试事实 |
| DeepSeek-V4 已统一 R1 推理线，不再需要独立 R1 系列 | Ch09 | D | 已降级为 monitor-only 课程解释边界：V4 模型卡可支持多档 reasoning effort 和 on-policy distillation，不支持“不再需要独立 R1 系列”作为事实；该推断不作为当前课程事实 |

## 写作规则

1. 基础算法如 softmax、attention、LayerNorm、KV Cache、cross entropy 不依赖具体厂商模型，正文按稳定理论讲。
2. DeepSeek/V4/新模型规格必须写成“某技术报告/模型卡报告”，避免写成普遍事实。
3. 任何 benchmark 数字必须带来源、日期、任务名、shot 数或评测设置。
4. 第三方新闻和博客可以帮助发现新内容，但不能单独支撑作业题或考试题。
5. 外部来源复核必须记录 claim、source URL、source type、access date、action 和 owner。
6. 每次更新前沿章节后，至少运行：

```bash
.venv/bin/python verify_course.py
```

并重新打开相关章节确认 KaTeX、链接和来源说明可读。

## 下一轮准确性任务

| 优先级 | 任务 | 验收 |
|--------|------|------|
| Done | 把 Ch09 中 “V4 统一 R1 推理线” 改写为模型卡事实 + 课程推断 | 正文明确区分事实与解释 |
| Done | 复核 Ch10 Engram/NIAH 数字是否出现在 V4 技术报告或官方模型卡 | 未保留未复核数字，正文降级为前沿案例 |
| Done | 给 DeepSeek 技术融入表增加“来源/复核日期”列 | README 表格已包含来源等级、2026-06-05 复核日期和 D 级 monitor-only 降级项 |
| Done | 为每个前沿专题增加 1 个“来源可靠性”概念题 | [书面推导与概念题题库](written-problem-set.md) 的 Ch10 第 5 题要求学生标注来源、日期、任务设置和评测版本 |
| Done | 修正 Ch04 关于 RoPE/MLA 可交换性的错误表述 | Ch04 已改为“位置相关线性正交变换，与固定解压矩阵一般不能交换或统一吸收” |
