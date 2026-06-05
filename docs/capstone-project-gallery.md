# Capstone Project Gallery and Idea Bank

本文件用于支持课程最终项目选题、导师匹配、项目范围控制和优秀报告归档。它补充 [Capstone Proposal and Milestone Guide](capstone-proposal-milestone.md)、[Project Team and Mentor Policy](project-team-mentor-policy.md)、[Default Final Project Guide](default-final-project-guide.md)、[Project Report Exemplar Pack](project-report-exemplar-pack.md)、[Capstone 项目报告 Rubric](project-report-rubric.md)、[项目展示与同伴 Review Rubric](presentation-peer-review.md)、[Final Project Showcase and Archive Policy](final-project-showcase-archive-policy.md) 和两个 capstone README。

## 使用目标

高校课程中的 final project 不应只靠学生临时想题。课程团队应提供默认项目、自定义项目边界、选题样例、导师匹配规则和报告归档口径，让学生能在有限时间内做出可复现、可评价、有技术深度的项目。

## 项目类型

| 类型 | 适合学生 | 必须交付 | 风险 |
|------|----------|----------|------|
| 默认最终项目任务包 | 希望按统一项目路径完成 GPT-2 + 下游评测的学生 | Tiny GPT 训练、生成质量对比、固定评测/服务化、报告与贡献声明 | 容易只跑通脚本，缺少下游错误分析 |
| 默认训练工程项目 | 第一次做训练闭环或资源有限的学生 | 数据审计、tiny LM 训练、checkpoint/resume、metrics、成本估算 | 容易只跑通脚本，缺少错误分析 |
| 默认推理工程项目 | 希望做服务、评测和系统指标的学生 | OpenAI-compatible API、eval、benchmark、SLO、capacity plan | 容易只做 demo，缺少固定回归和容量解释 |
| 自定义训练项目 | 有数据或特定任务兴趣的学生 | 自定义数据、baseline、ablation、训练日志、失败案例 | 数据风险、资源超预算、指标不稳定 |
| 自定义推理项目 | 有 RAG/Agent/serving 场景的学生 | API/检索/工具调用、评测集、SLO、压测、上线风险 | 评测集过窄、系统复杂度过高 |

所有项目必须满足 [Data and Ethics Review](data-ethics-review.md)、复现要求和报告 rubric。自定义项目不因“更复杂”自动加分；评分依据是目标清晰、证据可靠、实现可复现和分析可信。

默认最终项目任务包见 [Default Final Project Guide](default-final-project-guide.md)。它把训练工程 capstone、推理工程 capstone 和至少三个下游任务/评测场景组合成统一路径，适合作为正式开课时的 default project。

报告结构、证据强度和 A/B/C/not_passing 分档样例见 [Project Report Exemplar Pack](project-report-exemplar-pack.md)。这些样例是教学用 synthetic/anonymized material，不是可复制答案。

## 选题库

### 训练工程方向

| 题目 | 最小目标 | 可扩展方向 | 推荐章节 |
|------|----------|------------|----------|
| Tiny GPT 数据质量审计 | 比较去重前后 val loss 和样例质量 | 加入长度分桶、异常字符过滤、污染检查 | Ch01, Ch07 |
| Tokenizer 对训练稳定性的影响 | 比较字符级、BPE 或不同 vocab 大小对 loss 的影响 | 分析 token 长度分布和 OOV 行为 | Ch01, Ch02, Ch07 |
| LoRA 小模型微调 | 在固定小数据上比较 full fine-tune 与 LoRA | 加入 rank/alpha ablation 和过拟合分析 | Ch07, Ch09 |
| DPO 偏好优化最小实验 | 构造小型 preference 数据并解释 loss 变化 | 比较 DPO beta、chosen/rejected 长度偏差 | Ch09 |
| 训练监控与恢复报告 | 设计 checkpoint/resume、grad norm 和 loss spike 排查 | 增加 NaN 注入与恢复策略 | Ch07 |

### 推理工程方向

| 题目 | 最小目标 | 可扩展方向 | 推荐章节 |
|------|----------|------------|----------|
| KV Cache 容量规划 | 计算 context/batch/dtype 对显存的影响 | 加入 MQA/GQA/MLA cache 对比 | Ch04, Ch10 |
| RAG 固定回归集 | 构建检索语料、固定 query 和失败判定 | 加入 rerank、chunk overlap ablation | Ch08, Ch10 |
| JSON/工具调用可靠性 | 测试结构化输出、错误格式和回退策略 | 加入 schema repair 与安全边界 | Ch08, Ch10 |
| Streaming 延迟分解 | 报告 TTFT、TPOT、P95/P99 和 tokens/s | 加入并发、batching、限流策略 | Ch08, Ch10 |
| 服务上线 Checklist | health、metrics、eval、benchmark、SLO 全流程 | 加入灰度、回滚和成本预算 | Ch10 |

### 经典 NLP 与评测方向

| 题目 | 最小目标 | 可扩展方向 | 推荐材料 |
|------|----------|------------|----------|
| BLEU/ROUGE/F1 指标误差分析 | 构造指标高但人工差的样例 | 增加人工标注协议和一致性检查 | classic NLP handout |
| Dependency parsing 错误分类 | 分析 UAS/LAS 与标签错误 | 连接到 attention 可解释性边界 | Ch03, Ch11 |
| BERT MLM mask 策略实验 | 比较 mask 位置和 label 构造 | 讨论 encoder-only 与 decoder-only 差异 | Ch11 |

## 自定义项目边界

允许：

- 使用公开数据集、开源模型、第三方库或外部 API，但必须引用和说明贡献边界。
- 与另一门课共享项目，但必须在 proposal 中说明共享范围，并交付本课程要求的 LLM/NLP 证据。
- 与外部协作者讨论问题或共享非课程资源，但报告中必须明确哪些部分不是学生贡献。

不允许：

- 只调用商业 API 得到输出而没有评测、错误分析、复现命令或工程判断。
- 用未授权数据、私有文档、密钥或含敏感信息的样本做公开展示。
- 把往届项目、开源 repo 或 AI 生成代码改名提交而不说明来源。
- 选择无法在课程时间内复现的超大训练或不可控线上系统作为核心证据。

## 导师匹配

每个自定义项目在 proposal 后应分配一名教师或助教作为项目 mentor。匹配依据：

| 项目主题 | 推荐 mentor 背景 |
|----------|------------------|
| tokenizer、训练、优化器、checkpoint | 训练工程或 PyTorch 经验 |
| RAG、serving、benchmark、SLO | 推理系统或后端经验 |
| alignment、preference learning、安全 | 对齐、评测或安全经验 |
| 经典 NLP、指标、标注协议 | NLP 任务与评测经验 |
| 数据/伦理高风险项目 | 数据治理、安全或课程负责人 |

导师反馈只提供方向、风险和复现建议，不代写代码、不调试隐藏测试、不替学生完成实验设计。

## 贡献声明

团队项目最终报告必须包含贡献声明：

| 成员 | 主要贡献 | 证据 | 是否使用外部协助 |
|------|----------|------|------------------|
| 姓名 | 数据/训练/服务/评测/报告/展示 | commit、日志、实验表、文档 | 同伴、AI 工具、外部库 |

若贡献严重不均衡，教师可要求一对一问答、补充日志或单独评分。贡献声明不替代协作政策和 AI 工具披露。

## 项目报告归档

课程运行后可按 [Final Project Showcase and Archive Policy](final-project-showcase-archive-policy.md) 归档优秀项目作为下一轮样例，但必须满足：

- 学生或团队同意公开。
- 删除个人信息、密钥、私有路径和未授权数据。
- 报告保留数据来源、许可证、访问日期和模型卡/API 文档引用。
- 归档页面说明该报告来自哪一轮课程、使用了哪些依赖和硬件条件。
- 不把归档报告作为可复制答案；学生不得直接复用往届代码或文字作为提交。

归档记录样例：

| 年份/轮次 | 项目标题 | 类型 | 公开材料 | 关键证据 | 已脱敏 | 备注 |
|-----------|----------|------|----------|----------|--------|------|
| 2026 dry-run baseline | LLM Training Engineering Capstone reference path | 训练 | project README, acceptance command, report rubric | training acceptance, checkpoint resume evidence, cost estimate, sample corpus audit | Yes | instructor-created reference path only; not a real student archive |
| 2026 dry-run baseline | LLM Inference Engineering Capstone reference path | 推理 | project README, acceptance command, benchmark/SLO report rubric | eval pass rate, TTFT/TPOT/P95 latency, tokens/s, capacity plan | Yes | instructor-created reference path only; replace with consented student work after first live offering |

## 发布前 Checklist

| 检查项 | 通过标准 |
|--------|----------|
| 默认项目路径清楚 | 学生能在两个 capstone README 中找到可运行起点 |
| 自定义项目边界清楚 | proposal 明确数据、贡献、资源、指标和非目标 |
| 选题不过大 | mentor 能指出最小成功标准和降级路径 |
| 评测可复现 | 报告数字能追溯到命令、日志或机器可读文件 |
| 归档合规 | 公开样例无敏感数据、密钥、私有路径或未授权材料 |
