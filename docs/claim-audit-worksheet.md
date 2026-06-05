# Claim Audit Worksheet

本工作表用于逐章复核课程正文、作业、测验和项目材料中的关键 claim。它补充 [Chapter Source and Accuracy Map](chapter-source-map.md)、[Chapter Claim Audit Ledger](chapter-claim-audit-ledger.md)、[External Source Inventory](external-source-inventory.md)、[External Source Verification Guide](external-source-verification.md)、[Course Errata and Correction Ledger](course-errata-correction-ledger.md) 和 [前沿模型来源等级与复核记录](frontier-source-audit.md)。

目标不是把所有句子都写成引用表，而是让教师和助教能系统处理高风险表述：数学定理、复杂度、参数量、benchmark、API 行为、模型卡声明、价格、延迟、显存、对齐和安全结论。

## 使用场景

| 场景 | 何时使用 |
|------|----------|
| 章节大改 | 每次新增或重写正文小节 |
| 前沿模型更新 | 涉及 DeepSeek、新模型、API、benchmark、价格或上下文长度 |
| 作业/考试出题 | 某 claim 会进入评分题、隐藏测试或标准答案 |
| 项目报告评分 | 学生报告引用外部模型、数据集、leaderboard 或服务指标 |
| 争议复核 | 学生或助教指出正文、测试或答案可能过强或不准确 |

已经进入当前课程版本的逐章复核记录见 [Chapter Claim Audit Ledger](chapter-claim-audit-ledger.md)。本工作表用于新增、修改或争议复核时填写单条记录；ledger 用于发布前确认各章高风险 claim 覆盖。

## Claim 分类

| 类型 | 例子 | 最低来源要求 | 是否可进考试/作业事实 |
|------|------|--------------|--------------------------|
| Stable theory | attention scaling、LayerNorm、CE、AdamW、RoPE 相对位置性质 | A-stable 论文、教材或官方文档 | Yes |
| Implementation behavior | PyTorch API、vLLM/SGLang 参数、tokenizer 库行为 | 官方文档或代码版本 | Yes，但需标注版本/接口 |
| Frontier model card | DeepSeek-V4 参数量、context、mHC、Muon、reasoning modes | 官方模型卡/技术报告，带访问日期 | 可作案例，不宜作为基础定理 |
| Benchmark/performance | latency、tokens/s、FLOPs、KV cache 节省、pass rate | 官方报告或可复现实验，带配置 | 只在说明配置时可用 |
| Course inference | 由来源事实推导出的教学解释 | 必须明确“课程解释/推断” | 一般不作为唯一正确答案 |
| Unsupported / rumor | 社媒、论坛、二手博客、未署名转载 | 不足 | No |

## 复核表模板

| Field | 要求 |
|-------|------|
| Claim ID | 稳定编号，例如 `CH08-C03` |
| Location | 文件、章节、小节、题号或项目 rubric |
| Claim text | 最小可复核表述，不写整段 |
| Claim type | stable theory / implementation / frontier model card / benchmark / course inference / unsupported |
| Source | URL、论文、模型卡、官方文档或课程内实验 |
| Source level | A-stable / A-volatile / B-implementation / C-background / Runtime asset |
| Access date | 外部来源访问日期 |
| Evidence summary | 来源如何支持 claim，避免长段复制 |
| Boundary | 来源没有支持的更强结论 |
| Student-facing use | lecture / assignment / quiz / exam / capstone / reading only |
| Action | keep / qualify / downgrade / remove / replace |
| Owner | 复核人 |

## 示例记录

| Claim ID | Location | Claim text | Claim type | Source level | Boundary | Action |
|----------|----------|------------|------------|--------------|----------|--------|
| CH01-C01 | Ch01 BPE | BPE 每步选择高频 pair 是局部压缩启发式，不保证全局最优 | stable theory | A-stable | 不等同于语义最优或 PMI 最高 | qualify |
| CH02-C02 | Ch02 RoPE | RoPE 点积在理想旋转公式下依赖相对位移 | stable theory | A-stable | 长上下文外推仍依赖训练分布和缩放策略 | keep |
| CH05-C03 | Ch05 mHC | DeepSeek-V4 模型卡报告 mHC 使用 Birkhoff 约束 | frontier model card | A-volatile | 不能推出任意架构都稳定或不会梯度爆炸 | qualify |
| CH08-C04 | Ch08 speculative decoding | 在论文假设成立时，拒绝采样校正可保持目标采样分布 | stable theory | A-stable | 真实系统加速取决于 draft 质量和调度瓶颈 | keep |
| CH10-C05 | Ch10 serving | P95/P99 比平均延迟更能反映上线尾延迟风险 | implementation | B-implementation | 不给出通用 latency 数字 | keep |

## 逐章最低审查清单

| 章节 | 至少复核 |
|------|----------|
| Ch01 | BPE 最优性、byte-level 可逆性、token 成本 |
| Ch02 | word vector 类比、置换等变、RoPE 外推 |
| Ch03 | attention scaling、mask 位置、attention 可解释性 |
| Ch04 | MHA/GQA/MLA cache、RoPE 与 latent cache 边界 |
| Ch05 | Pre-Norm 稳定性、LayerNorm/RMSNorm、mHC/Birkhoff |
| Ch06 | GPT 训练目标、参数量、MoE 成本与负载均衡 |
| Ch07 | AdamW、scheduler、FP8/FP4、DualPipe、Muon |
| Ch08 | top-p、speculative decoding、TTFT/TPOT、结构化输出 |
| Ch09 | SFT mask、LoRA、DPO、GRPO、R1/RL 推理声明 |
| Ch10 | KV cache、RAG 指标、serving benchmark、量化、DSA/CSA/HCA |
| Ch11 | UAS/LAS、BLEU/ROUGE/EM/F1、BERT MLM、评测伦理 |

## 发布前 Checklist

| 检查项 | 通过标准 |
|--------|----------|
| 高风险 claim 已列入表 | 参数、benchmark、价格、API、模型卡和“最优/保证”表述都有记录 |
| 边界明确 | 每条记录都写出来源不支持的更强结论 |
| 学生用途明确 | 进入作业/考试的 claim 有 A/B 级来源或课程内可复现实验 |
| 改稿动作明确 | keep / qualify / downgrade / remove / replace 之一 |
| 门禁通过 | `.venv/bin/python verify_course.py` 和必要的 capstone 验收通过 |
