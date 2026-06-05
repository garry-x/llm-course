# Quiz and Checkpoint Guide

本指南用于把 prerequisite diagnostic、课堂 quick check、recap quiz、期中 checkpoint 和期末复习组织成可评分、可补救、可复盘的阶段性评估。它补充 [Assessment Blueprint and Coverage Matrix](assessment-blueprint-coverage-matrix.md)、[Comprehensive Review Study Guide](comprehensive-review-study-guide.md)、[Prerequisite Diagnostic](prerequisite-diagnostic.md)、[10 周 / 20 讲 Lecture Plan](lecture-plan.md)、[Discussion Section and Office Hours Guide](discussion-office-hours-guide.md)、[书面推导与概念题题库](written-problem-set.md)、[Midterm and Final Review Pack](midterm-final-review-pack.md)、[Assessment Item Bank Ledger](assessment-item-bank-ledger.md)、[Assessment Administration and Exam Integrity Policy](assessment-administration-policy.md)、[Learning Analytics and Remediation Plan](learning-analytics-remediation-plan.md) 和 [Course Operations and Improvement Log](course-operations-log.md)。

## 评估类型

| 类型 | 时间 | 目标 | 是否计分 |
|------|------|------|----------|
| Prerequisite diagnostic | Week 0 / Week 1 前 | 识别 Python、PyTorch、数学和复现薄弱点 | 完成/未完成 |
| Recap quiz | 每周讨论课开头 | 检查上一周最核心 shape、公式或失败模式 | 可计入参与分 |
| Lecture quick check | 每讲中或结束前 | 立即发现概念误解 | 不建议单独计分 |
| Midterm checkpoint | Week 5 后 | 检查 Ch01-Ch07 主线是否可进入项目阶段 | 可计入书面/参与小分 |
| Capstone readiness check | Week 8-9 | 检查项目是否具备复现、评测和风险证据 | 计入 milestone |
| Final review quiz | Week 10 | 帮助学生复习公式、shape、工程指标和来源边界 | 不替代项目评分 |

## 出题原则

每个 quiz/checkpoint 题目应满足：

- 能在 5-12 分钟内完成。
- 至少检查一个可观察能力：shape、公式、边界、日志、来源、复现命令或失败分析。
- 不依赖隐藏测试、参考解或大型计算。
- 能明确映射到一个章节、作业、阅读或项目 rubric。
- 题目轮换时保持能力目标不变，避免学生背题。
- 计分或可能复用的题目必须在 [Assessment Item Bank Ledger](assessment-item-bank-ledger.md) 记录 item_bank_id、exposure_level、variant_policy 和 retirement_trigger。

## 题型池

| 题型 | 示例 | 适用周 |
|------|------|--------|
| Shape trace | 写出 `[B,H,T,D]` attention scores 和 context shape | Week 1-4 |
| Formula completion | 补全 RoPE 相对位置或 CE 梯度中的关键项 | Week 1-7 |
| Boundary case | 判断 `T=1` decode mask 或 top-p 最小 nucleus | Week 2, 6, 9 |
| Failure diagnosis | 给 traceback/log，判断是 dtype、mask、shape、NaN 还是环境 | Week 2-10 |
| Source boundary | 判断模型卡声明是否能支持更强结论 | Week 7-10 |
| Reproducibility check | 给项目报告片段，指出缺少 seed、环境、日志或指标 | Week 5-10 |

## 每周 Quick Check 蓝图

| 周 | 核心能力 | 示例题 | 补救材料 |
|----|----------|--------|----------|
| 1 | BPE/Embedding/RoPE shape | `one_hot @ E` 输出 shape；RoPE head dim 为什么要成对 | Ch01-Ch02; math prerequisites |
| 2 | attention/mask/backprop | score shape；mask 放 softmax 前还是后；CE 梯度 | Ch03; math prerequisites |
| 3 | MHA/GQA/MLA/Block | KV cache 元素数；pre-norm 梯度路径 | Ch04-Ch05 |
| 4 | GPT/MoE | next-token labels；tied weights；activated vs total parameters | Ch06 |
| 5 | training loop | logits/labels flatten；AdamW 与 L2；loss spike 排查 | Ch07 |
| 6 | generation | top-k/top-p/temperature；speculative decoding 接受率 | Ch08 |
| 7 | SFT/LoRA/DPO/GRPO | `-100` mask；chosen/rejected 方向；LoRA rank | Ch09 |
| 8 | classic NLP/evaluation | UAS/LAS；BLEU/ROUGE/EM/F1 局限；BERT MLM label | classic NLP handout |
| 9 | inference/RAG/serving | KV cache 公式；TTFT/TPOT/P95；RAG 失败分类 | Ch10 |
| 10 | capstone/source audit | 报告复现缺口；来源等级；项目失败案例 | capstone rubrics |

## Midterm Checkpoint

建议在 Week 5 后进行 45-60 分钟 checkpoint，覆盖 Ch01-Ch07。它的目标不是期中考试排名，而是判断学生是否具备进入 capstone 阶段的最低能力。

建议结构：

| 模块 | 分值 | 题目 |
|------|:--:|------|
| Token/Embedding/RoPE | 20 | embedding lookup shape + RoPE 相对位置解释 |
| Attention/Mask | 20 | attention score shape + causal mask 边界 |
| Transformer/GPT | 20 | block shape + next-token label + 参数量审计 |
| Training Loop | 25 | CE/AdamW/scheduler/log 排查 |
| Source/Reproducibility | 15 | 给一个模型卡或训练日志片段，指出证据边界 |

通过建议：

- 80-100：Ready for capstone。
- 60-79：允许进入 capstone，但必须完成 targeted remediation。
- 40-59：capstone proposal 需降级 scope，并安排 mentor check。
- 0-39：暂停自定义项目，优先完成默认项目最小闭环和补救任务。

## 补救路径

| 低分项 | 补救任务 | 验收 |
|--------|----------|------|
| shape trace | 重做对应 discussion shape drill | 助教口头抽查 2 个 shape |
| mask/attention | 完成 Ch03 causal mask 失败分析 | 能解释 softmax 前 mask |
| training stability | 提交 1 页 NaN/loss spike 排查记录 | 包含命令、日志、可能原因 |
| source audit | 复核 1 个模型卡/API 文档 claim | 填写 source type、access date、boundary |
| reproducibility | 跑通一个 capstone acceptance | 提交命令、环境和输出摘要 |

补救不应变成额外惩罚；它的目标是让学生在进入项目阶段前补齐关键能力。

## 评分与诚信边界

- Quick check 可作为参与证据，但不应占课程大分。
- Midterm checkpoint 可计入书面/参与的小比例，建议不超过 5%。
- 不公开完整答案库；可公开能力目标、样题和评分 rubric。
- 不使用隐藏作业测试作为 quiz 题目。
- allowed materials、makeup assessment、题目轮换、远程核验、诚信事件和成绩发布按 [Assessment Administration and Exam Integrity Policy](assessment-administration-policy.md) 执行。
- 若学生有正式便利安排，按 [Accessibility and Student Support Guide](accessibility-student-support.md) 调整时间或形式。

## 题目轮换记录

| 日期 | 周次 | 题目能力 | 使用题号/变体 | 平均通过率 | 后续动作 |
|------|------|----------|---------------|------------|----------|
| 2026-06-05 dry-run baseline | Week 2 | causal mask | mask-v1 | readiness proxy: Ch03 public attention tests pass; live pass rate pending | use WTR-2026-L03-MASK to add recap and recitation mask-shape drill before live offering |
| 2026-06-05 dry-run baseline | Week 5 | training loop debugging | train-debug-v1 | readiness proxy: Ch07 public training tests pass; live pass rate pending | prepare remediation item for device mismatch, missing `zero_grad`, validation mode, and label shift |

若同一题平均通过率低于 70%，下一讲或讨论课应安排 recap；若高于 95% 且无区分度，应替换为更有诊断价值的变体。

## 发布前 Checklist

| 检查项 | 通过标准 |
|--------|----------|
| 能力映射 | 每题能映射到章节、作业、阅读或项目 rubric |
| 时间控制 | quick check 5-12 分钟，midterm 45-60 分钟 |
| 隐藏边界 | 不泄露 reference solution 或 hidden tests |
| 补救路径 | 每个低分模块有对应任务和验收方式 |
| 运行记录 | quick check 通过率写入 operations log |
| 管理流程 | 计分 assessment 有 assessment_id、allowed materials、makeup 和 regrade window |
