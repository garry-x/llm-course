# Default Final Project Guide

本文件把本课程的默认最终项目整理成一条可授课、可评分、可复现的路径。它对标 CS224N default final project 的公开结构：学生先实现 GPT-2 风格模型，再把模型用于下游 NLP/LLM 任务，并用 proposal、milestone、poster 和 final report 证明技术判断。

本指南补充 [Capstone Proposal and Milestone Guide](capstone-proposal-milestone.md)、[Capstone Project Gallery and Idea Bank](capstone-project-gallery.md)、[Project Report Template and Reproducibility Checklist](project-report-template.md)、[Capstone 项目报告 Rubric](project-report-rubric.md)、[Data and Ethics Review](data-ethics-review.md)、[Compute Resource and Cost Guide](compute-resource-guide.md)、训练工程 capstone 和推理工程 capstone。

## 项目目标

默认项目适合没有自定义数据或研究题目的学生。目标不是训练大模型，而是证明学生能把课程主线串起来：

1. 实现并解释 GPT-2 风格 decoder-only 模型的核心组件。
2. 在小规模可复现设置下完成训练、验证、checkpoint 和 resume。
3. 把模型或服务用于至少三个下游任务或评测场景。
4. 提交可追溯的指标、失败案例、成本估算和贡献声明。

## 默认任务包

| 任务 | 最小交付 | 主要指标 | 关联材料 |
|------|----------|----------|----------|
| Task A: Tiny GPT 语言建模 | 用 `projects/training-engineering-capstone/train.py` 或等价代码训练小型 decoder-only LM，并记录 checkpoint/resume | train/val loss、perplexity、tokens/s、resume step | Ch01-Ch07、训练 capstone |
| Task B: 生成质量与采样对比 | 在固定 prompt 集上比较 greedy、temperature、top-k/top-p 或 repetition penalty | distinct-n、人工失败分类、长度/重复率 | Ch08、`assignments/ch08_generation/` |
| Task C: 固定评测与服务化 | 用 OpenAI-compatible API 或等价 CLI 输出固定评测集结果，包含 JSON/工具/RAG 中至少一种约束场景 | pass rate、P95 latency、TTFT、TPOT、error rate | Ch08-Ch10、推理 capstone |
| Task D: 经典 NLP / 评测专题选做 | BLEU/ROUGE/F1、dependency parsing 或 BERT MLM mask 中任选一个专题，用于展示评价指标局限 | 指标值、错误案例、指标局限说明 | `assignments/ch11_classic_nlp/`、classic NLP handout |

最低通过需要完成 Task A、Task B、Task C。Task D 可作为自定义扩展或报告加分证据。

## 项目时间线

| 阶段 | 交付 | 评分用途 |
|------|------|----------|
| Proposal | 1-2 页项目计划，包含任务选择、数据来源、baseline、资源预算、风险登记 | 确认范围可控、数据合规、指标可复现 |
| Milestone | 可运行最小闭环、初步指标、至少 2 个失败案例、下一步计划 | 检查训练/评测是否已经跑通 |
| Poster / Presentation | 8-10 分钟展示，突出系统图、核心结果、失败案例和下一步 | 训练学生解释技术取舍，而不是只展示结果 |
| Final Report | 完整报告、复现命令、日志、贡献声明、数据伦理审查 | 按项目报告 rubric 评分 |

## Proposal 必填字段

- 团队成员和贡献预期。
- 是否采用默认三任务包，或替换其中一个任务。
- 数据来源、许可证、访问日期和数据风险。
- 模型配置：层数、hidden size、head 数、context length、参数量估计。
- 训练预算：token 数、global batch tokens、step、预计耗时和成本。
- 评测集：固定 prompt、期望行为、失败判定和指标局限。
- 最小成功标准和降级路径。

## Milestone 必交证据

| 证据 | 通过标准 |
|------|----------|
| 训练日志 | 至少一次 train + validation，指标写入机器可读日志 |
| checkpoint/resume | resume 后 step 单调增加，并说明恢复了哪些状态 |
| 生成样例 | 至少 5 个固定 prompt，包含成功和失败输出 |
| 评测结果 | pass/fail 或指标表能由命令复现 |
| 风险处理 | 至少 2 个具体失败案例和对应修复计划 |

## Final Report 结构

正式提交建议直接使用 [Project Report Template and Reproducibility Checklist](project-report-template.md)。最低结构如下：

1. Abstract：一句话问题、方法和最重要结论。
2. Model and Implementation：GPT-2 组件、shape、参数量和关键实现。
3. Data and Ethics：数据来源、许可证、PII、污染、偏见和残余风险。
4. Experiments：baseline、变量控制、ablation、训练/推理命令。
5. Results：loss、PPL、生成质量、服务指标和固定评测结果。
6. Error Analysis：至少 3 个失败案例，按原因分类。
7. Cost and Reproducibility：硬件、耗时、成本、seed、依赖版本、日志路径。
8. Contributions：团队贡献、外部代码/AI 工具/协作者披露。

## 评分细则

| 维度 | 分值 | 满分证据 |
|------|:--:|----------|
| GPT-2 实现理解 | 15 | 能解释 tokenizer、embedding、attention、block、LM head 和 loss 的数据流 |
| 训练复现 | 15 | 数据审计、训练日志、checkpoint/resume、seed 和成本估算完整 |
| 下游任务覆盖 | 20 | 至少三个任务/场景有固定输入、指标和失败判定 |
| 实验设计 | 15 | 有 baseline、至少一个 ablation、指标局限说明 |
| 错误分析 | 15 | 至少 3 个失败案例，分析具体且连接到模型/数据/系统原因 |
| 工程判断 | 10 | 解释延迟、显存、吞吐、成本或数据质量取舍 |
| 报告与引用 | 10 | 引用论文/文档/模型卡，图表清晰，贡献声明完整 |

## 不通过条件

- 只调用现成 API 或开源模型，没有实现、评测或贡献边界说明。
- 报告数字无法从日志、命令或机器可读文件复现。
- 只展示成功样例，没有失败案例。
- 缺少数据和伦理审查。
- 团队贡献、外部协作者、AI 工具或参考代码未披露。
- 项目范围与 proposal 明显不一致且未在 milestone 中说明。

## 发布前 Checklist

| 检查项 | 通过标准 |
|--------|----------|
| 默认项目入口清楚 | README、syllabus 和 capstone guide 均链接本文件 |
| 下游任务可评分 | 三个必做任务均有输入、指标、失败判定和复现命令 |
| 项目过程可管理 | proposal、milestone、poster/report 均有交付物 |
| 贡献边界清楚 | 团队、外部协作者、AI 工具和开源代码必须披露 |
| 与资源政策一致 | CPU baseline、GPU/API 额度和成本记录遵循 compute guide |
