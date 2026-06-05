# Paper Recap Calibration Pack

本文件用于校准阅读复盘评分，补充 [逐周阅读清单与复盘 Handout](reading-list.md)、[Reading Discussion Question Bank](reading-discussion-question-bank.md)、[Participation and Feedback Guide](participation-feedback-guide.md)、[Chapter Claim Audit Ledger](chapter-claim-audit-ledger.md)、[Mathematical Derivation Audit](mathematical-derivation-audit.md) 和 [External Source Verification Guide](external-source-verification.md)。

复核日期：2026-06-05
适用范围：每周阅读复盘、student-led paper report、frontier seminar reflection、capstone related work 和项目报告引用表。
评分原则：阅读复盘不是论文摘要摘抄；满分证据必须把论文/官方文档的核心结论、至少一个技术细节、课程代码连接、来源等级、局限边界和可讨论问题放在同一份记录中。

## Recap Rubric

| 维度 | 分值 | 满分证据 | 常见扣分 |
|------|:--:|----------|----------|
| Core claim | 20 | 用自己的话说明论文或文档解决什么问题、方法为何有效、结论支持到什么范围 | 只复制 abstract，或把动机写成已证明事实 |
| Technical detail | 20 | 解释一个公式、算法步骤、架构部件、实验设置或 metric 定义 | 只有口号，没有可检查细节 |
| Course connection | 20 | 明确连接到章节、assignment function、capstone module 或 derivation ID | 只说“和 Transformer 有关” |
| Source audit | 20 | 写出来源等级、发布日期/访问日期、实验条件和不确定性 | 没有日期、没有来源等级、把二手材料当一手证据 |
| Critical question | 10 | 提出可复现、可反驳或可用于讨论的问题 | 问题无法验证，或只是“这篇论文很好吗” |
| Citation hygiene | 10 | 包含作者/机构、标题、链接、访问日期、使用位置 | 链接缺失，引用无法定位 |

## Anchor Samples

| Anchor ID | Level | Topic / source | Evidence summary | Score | Feedback |
|-----------|-------|----------------|------------------|:--:|----------|
| PR-A1 | A | Vaswani et al. Attention Is All You Need | 说明 scaled dot-product attention 解决长程依赖和并行化；推导 `1/sqrt(d_k)` 的方差动机；连接 Ch03 `ScaledDotProductAttention` 和 DER-04；指出方差假设依赖独立、零均值、单位方差；引用 arXiv 链接和访问日期 | 95 | 满分级别；若再补一个 mask 失败反例，可用于 discussion exemplar |
| PR-A2 | A | Kwon et al. PagedAttention / vLLM | 解释 KV cache 分页减少碎片；连接 Ch10 KV cache、inference capstone benchmark 和 DER-13；区分论文实验硬件、batching、context length；提出“prefix cache 与 continuous batching 如何互相影响”的讨论问题 | 93 | 工程边界清楚；注意不要把论文吞吐数字外推到不同 GPU |
| PR-B1 | B | Holtzman et al. Nucleus Sampling | 正确说明 top-p nucleus 的最小累计概率集合，并连接 Ch08 sampling tests；但没有说明 temperature/top-k 顺序，也没有构造重复/多样性指标反例 | 82 | 技术主线正确；扣分来自边界和反例不足 |
| PR-B2 | B | DeepSeek-R1 / GRPO | 能说明 GRPO 使用组内相对优势并连接 Ch09 tests；标了 A-volatile 和访问日期；但把“出现自我反思行为”写得接近通用能力结论，缺少任务和训练设定边界 | 78 | 需要把模型报告观察降级为“在报告设定下观察到” |
| PR-C1 | C | GQA paper | 只写“GQA 比 MHA 快且质量差不多”，有论文链接，但没有 KV head/cache shape、没有课程代码连接、没有实验条件 | 62 | 可通过但不适合课堂展示；补 DER-06 和 Ch04 tests 才能升到 B |
| PR-C2 | C | BERT paper | 能区分 MLM 和 causal LM，但没有解释 ignore index / masked labels，也没有连接 Ch11 MLM example 或 encoder-only evaluation | 58 | 技术细节不足；需要至少一个 label policy 或 metric 细节 |
| PR-NP1 | Not passing | Blog post on “latest LLM benchmark” | 只贴第三方排行榜截图，没有访问日期、benchmark 设置、模型版本、数据污染风险或课程连接 | 35 | 不能作为课程事实；必须回到官方报告或 benchmark 文档 |
| PR-NP2 | Not passing | “LoRA makes fine-tuning free” | 使用绝对表述，未说明 rank、target modules、optimizer states、base model memory 或质量边界 | 40 | 违反 source audit 和 boundary 要求；需要重写为条件化 claim |

## Required Evidence Fields

学生每次提交必须包含下列字段；助教评分时按字段定位证据，不按篇幅给分。

| Field | Required content | Failing pattern |
|-------|------------------|-----------------|
| `source_record` | 作者/机构、标题、链接、发布日期或访问日期、来源等级 | 只有论文名或截图 |
| `core_claim` | 论文或文档真正支持的主张 | 把背景动机当结论 |
| `technical_detail` | 公式、算法、架构、实验或 metric 中至少一项 | 泛泛说“提升性能” |
| `course_link` | 章节、assignment、capstone、DER ID 或 claim ID | 没有课程连接 |
| `boundary` | 不支持的更强结论、适用条件或失败模式 | 使用“保证、最优、免费、实时、必然”而无条件 |
| `discussion_question` | 可复现、可检验或可辩论的问题 | 主观偏好问题 |

## TA Calibration Procedure

1. 每轮开课前，TA 先独立评分 PR-A1、PR-B1、PR-C1 和 PR-NP1，分差超过 8 分必须讨论 rubric 解释。
2. 每周抽取 5-8 份阅读复盘，标注 `source_record`、`technical_detail`、`course_link` 和 `boundary` 是否可定位。
3. 若某周 30% 以上学生缺同一字段，下一次讨论课增加 paper-to-code drill，并更新 [Course Operations and Improvement Log](course-operations-log.md)。
4. 前沿模型、API、benchmark、价格、上下文长度或性能数字必须与 [External Source Inventory](external-source-inventory.md) 和 [External Source Verification Guide](external-source-verification.md) 一致。
5. 优秀样例进入下轮课程前必须脱敏，不能公开学生个人身份、未发布项目 idea 或私有数据来源。

## Student Submission Template

```text
source_record:
  authors_or_org:
  title:
  url:
  publication_or_access_date:
  source_level:

core_claim:
technical_detail:
course_link:
boundary:
discussion_question:
citation_use:
```

## Release Checklist

- 至少有 A、B、C、Not passing 四档 anchor sample。
- 每个 anchor sample 都说明 topic/source、score 和 actionable feedback。
- Required evidence fields 覆盖 source_record、core_claim、technical_detail、course_link、boundary 和 discussion_question。
- TA calibration procedure 包含分差阈值、抽样检查、operations log 和前沿来源一致性。
- 本文件与 reading list、participation guide、claim audit、derivation audit 和 external source verification 互相链接。
