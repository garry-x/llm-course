# Grading Anchor Sample Feedback Pack

本包供教师、Head TA 和阅卷助教在批改前进行 anchor sample calibration。它补充 [Grading Calibration Guide](grading-calibration.md)、[Grading Drift Audit Ledger](grading-drift-audit-ledger.md)、[Instructor Solution Guide](instructor-solution-guide.md)、[Assignment Handout Pack](assignment-handout-pack.md)、[Autograder 与隐藏测试设计指南](autograder-hidden-tests.md)、[Capstone 项目报告 Rubric](project-report-rubric.md)、[项目展示与同伴 Review Rubric](presentation-peer-review.md) 和 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md)。

本文件不是学生发布材料。它可以保存 synthetic submission、匿名历史提交摘要和学生可见 feedback template，但不得包含 hidden test exact input、`reference_solution.py`、完整标准答案或可反推出隐藏测试的逐行输出。

## Use Rules

| 规则 | 要求 |
|------|------|
| anchor_id | 每个样例使用稳定 ID，例如 `WR-ROPE-FULL-01`、`CODE-ATTN-PARTIAL-01` |
| rubric_item | 必须指向 handout、rubric 或 instructor guide 中的具体评分项 |
| score | 写原始分和百分比，不只写等级 |
| evidence | 引用提交中的公式、shape、日志、图表或复现命令 |
| feedback_to_student | 使用学生可见语言；指出下一步，不泄露 hidden tests |
| calibration_note | 写给阅卷人看的边界说明和常见误判 |
| second_reader_delta | 记录二评差异；无二评时写 `N/A` |
| final_decision | 写清维持、上调、下调或教师裁定 |

所有 anchor 更新必须同步检查 `rubric_version`、`release_batch`、`regrade_decision_id` 和 gradebook/LMS 记录字段。若样例来自真实提交，应脱敏 student_id、文件名、日志路径和特殊个人信息。

## Written Anchor Samples

### WR-ROPE-FULL-01

| 字段 | 内容 |
|------|------|
| anchor_id | `WR-ROPE-FULL-01` |
| rubric_item | Ch02 written: RoPE 点积依赖相对位置 |
| score | 10/10, full_credit |
| evidence | 答案写出二维旋转矩阵，推导 `R_m^T R_n = R_{n-m}`，说明 query/key 点积只通过 `n-m` 引入位置差，并补充长上下文外推受训练分布和频率范围限制 |
| feedback_to_student | 推导完整，符号定义和限制条件清楚。继续保持这种“公式 + 维度 + 适用边界”的写法。 |
| calibration_note | 不要求学生使用完全相同记号；只要相对位移结论、成对旋转和限制条件都成立，应给满分。 |
| second_reader_delta | 0 |
| final_decision | 维持 10/10 |

### WR-ROPE-PARTIAL-01

| 字段 | 内容 |
|------|------|
| anchor_id | `WR-ROPE-PARTIAL-01` |
| rubric_item | Ch02 written: RoPE 点积依赖相对位置 |
| score | 6/10, partial_credit |
| evidence | 答案能说明 RoPE 是旋转位置编码，也写出部分 sin/cos 形式；但没有证明 `R_m^T R_n`，且把外推能力描述为“任意长度可靠” |
| feedback_to_student | 直觉方向正确，但缺少关键矩阵等式，且外推结论过强。请补上相对位置推导，并说明训练长度、频率缩放和数值范围限制。 |
| calibration_note | 只给“旋转产生相对位置”直觉不能超过 6/10；若还把外推说成无条件保证，应扣适用边界分。 |
| second_reader_delta | +1 before reconciliation |
| final_decision | 教师裁定 6/10 |

### WR-ATTN-NOTPASS-01

| 字段 | 内容 |
|------|------|
| anchor_id | `WR-ATTN-NOTPASS-01` |
| rubric_item | Ch03 written: scaling 与 causal mask |
| score | 2/10, not_passing |
| evidence | 答案把 mask 放在 softmax 后且不重新归一化；没有 `1/sqrt(d_k)` 方差理由；causal mask 方向允许未来 token |
| feedback_to_student | 目前关键机制方向错误。请重新推导 score 的方差、softmax 前 masking 的原因，并用一个 3-token causal matrix 检查未来 token 是否被屏蔽。 |
| calibration_note | 即使文字提到“防止看未来”，mask 矩阵方向错误仍属于核心错误；不应因术语出现而给高分。 |
| second_reader_delta | 0 |
| final_decision | 维持 2/10 |

## Programming Anchor Samples

### CODE-BPE-FULL-01

| 字段 | 内容 |
|------|------|
| anchor_id | `CODE-BPE-FULL-01` |
| rubric_item | Ch01 programming: `_get_stats`、`_merge`、round trip、edge cases |
| score | 60/60 programming, full_credit |
| evidence | 公开测试通过；隐藏类别反馈显示 empty input、emoji、多字节 UTF-8、overlapping pair 和 tie-breaking 均通过；代码未导入测试文件或参考答案 |
| feedback_to_student | 实现覆盖了核心路径和边界情况，round trip 证据充分。错误分析中关于重叠 pair 的说明很清楚。 |
| calibration_note | 不要求实现和 reference line-by-line 一致；性质测试和人工检查满足即可给满分。 |
| second_reader_delta | N/A |
| final_decision | 维持 60/60 |

### CODE-ATTN-PARTIAL-01

| 字段 | 内容 |
|------|------|
| anchor_id | `CODE-ATTN-PARTIAL-01` |
| rubric_item | Ch03 programming: scaled dot-product attention and mask broadcast |
| score | 39/55 programming, partial_credit |
| evidence | 主路径和梯度测试通过；4D broadcast mask 失败；全 mask 行产生 NaN；书面解释能定位 softmax 稳定性但没有修复 |
| feedback_to_student | 核心 attention 计算正确，但 mask 边界不稳定。请补充 2D/3D/4D mask broadcast 测试，并处理全 mask 行，避免概率为 NaN。 |
| calibration_note | 公开测试全过但隐藏性质失败时，不应给满分；若核心矩阵乘法和 scaling 正确，可保留主体分。 |
| second_reader_delta | -3 before reconciliation |
| final_decision | Head TA 对照 mask rubric 后定为 39/55 |

### CODE-GEN-BORDERLINE-01

| 字段 | 内容 |
|------|------|
| anchor_id | `CODE-GEN-BORDERLINE-01` |
| rubric_item | Ch08 programming: top-p filtering and generation loop |
| score | 33/55 programming, borderline |
| evidence | top-k、temperature 和 EOS stopping 正确；top-p 最小集合边界错误；过滤后未重新归一化；analysis 提供重复失败案例 |
| feedback_to_student | 生成 loop 主体可用，但 top-p 的定义和概率归一化会改变采样分布。请用排序后累积概率的最小集合重写 top-p，并在过滤后重新归一化。 |
| calibration_note | 若学生生成结果看似流畅但概率过滤定义错误，按算法正确性扣分；不要用主观样例质量替代 rubric。 |
| second_reader_delta | +5 before reconciliation |
| final_decision | 教师裁定 33/55，低于 B 边界 |

## Capstone Anchor Samples

### CAP-INF-FULL-01

| 字段 | 内容 |
|------|------|
| anchor_id | `CAP-INF-FULL-01` |
| rubric_item | 推理工程 capstone: latency/cost/quality/safety evidence |
| score | 92/100, full_credit |
| evidence | 报告包含 P50/P95/P99、TTFT、TPOT、tokens/s、cost per 1k requests、RAG 失败案例、seed/log、CPU fallback 和可复现命令；claim_audit 将结论限定到课程数据集 |
| feedback_to_student | 证据链完整，结论边界清楚。下一步可以扩大真实用户查询覆盖面，并把错误类别与检索 chunk 策略关联。 |
| calibration_note | 若报告数字能从日志复现且不夸大外推范围，可给 A 档；不因模型规模较小而扣核心严谨性分。 |
| second_reader_delta | -2 before reconciliation |
| final_decision | Head TA 复核后定为 92/100 |

### CAP-TRAIN-PARTIAL-01

| 字段 | 内容 |
|------|------|
| anchor_id | `CAP-TRAIN-PARTIAL-01` |
| rubric_item | 训练工程 capstone: training evidence and experimental rigor |
| score | 78/100, partial_credit |
| evidence | 训练 loop、checkpoint resume 和 loss curve 完整；但只报告单 seed 结果，ablation 缺少置信区间，数据 contamination 检查只写声明没有脚本证据 |
| feedback_to_student | 工程实现扎实，但实验结论证据不足。请补充至少一个 seed sensitivity 或 bootstrap confidence interval，并提交 contamination/leakage gate 的日志。 |
| calibration_note | 系统能跑通不等于 A 档；统计严谨性缺失应在实验设计和结论强度项扣分。 |
| second_reader_delta | +4 before reconciliation |
| final_decision | 教师裁定 78/100 |

### CAP-NOTPASS-01

| 字段 | 内容 |
|------|------|
| anchor_id | `CAP-NOTPASS-01` |
| rubric_item | Capstone 不通过条件 |
| score | 48/100, not_passing |
| evidence | 报告核心数字无法从日志复现；没有失败案例；引用前沿模型结果但无来源等级和访问日期；demo 只依赖本地缓存 |
| feedback_to_student | 当前提交不能支撑报告结论。请先提供可复现命令、原始日志、数据/模型版本和失败案例，再讨论性能结论。 |
| calibration_note | 可演示 demo 不能抵消不可复现的核心指标；若数字与日志矛盾，应触发二评和可能的 integrity_hold。 |
| second_reader_delta | -6 before reconciliation |
| final_decision | 教师裁定 48/100，并要求补交复现证据 |

## Reading And Peer Review Anchor Samples

### READ-FULL-01

| 字段 | 内容 |
|------|------|
| anchor_id | `READ-FULL-01` |
| rubric_item | reading recap: source, formula, course connection, testable question |
| score | 10/10, full_credit |
| evidence | 复盘解释论文要解决的问题、一个关键公式、与 Ch09 DPO 实现的连接、来源等级、链接、访问日期和可复现实验问题 |
| feedback_to_student | 复盘把阅读、公式和代码连接起来，问题也能转化为实验检查。 |
| calibration_note | 只要来源和课程连接清楚，不要求学生覆盖整篇论文。 |
| second_reader_delta | N/A |
| final_decision | 维持 10/10 |

### PEER-LOW-01

| 字段 | 内容 |
|------|------|
| anchor_id | `PEER-LOW-01` |
| rubric_item | presentation peer review: specificity and actionable evidence |
| score | 3/10, not_passing |
| evidence | Review 只写“很好，可以更详细”，没有引用命令、指标、图表、风险或一轮可完成的建议 |
| feedback_to_student | 反馈过于笼统。请至少指出一个具体证据、一个风险和一个可操作修改建议。 |
| calibration_note | 礼貌、正向但无证据的 review 不应超过低分档。 |
| second_reader_delta | 0 |
| final_decision | 维持 3/10 |

## Regrade Anchor Samples

### RG-MASK-UP-01

| 字段 | 内容 |
|------|------|
| anchor_id | `RG-MASK-UP-01` |
| rubric_item | Ch03 hidden category feedback: mask broadcast |
| score | original 35/55, revised 40/55 |
| evidence | 学生指出提交在 rubric 允许的 3D mask 上正确；原 grader 错把 4D-only 隐藏类别扣到 3D broadcast 项 |
| feedback_to_student | 复核确认原扣分项归类不准确，已把 3D broadcast 项恢复。4D broadcast 边界仍未通过，相关扣分维持。 |
| calibration_note | 复核说明只给类别级理由，不泄露 hidden test exact input；同批次若有相同误扣，应批量检查。 |
| second_reader_delta | +5 |
| final_decision | 上调 5 分；记录 `regrade_decision_id` |

### RG-CAP-DOWN-01

| 字段 | 内容 |
|------|------|
| anchor_id | `RG-CAP-DOWN-01` |
| rubric_item | Capstone reproducibility and claim strength |
| score | original 84/100, revised 80/100 |
| evidence | 复核中发现报告中一项 P99 latency 来自不同配置的日志；主结果仍可复现，但 claim strength 应降一级 |
| feedback_to_student | 复核确认主实验可复现，但 P99 延迟表格混入了不同配置日志。已调整结论强度项分数；请在最终归档中更正表格标签。 |
| calibration_note | regrade 可能上调或下调；复核后需保存原始提交、复核证据和最终学生可见说明。 |
| second_reader_delta | -4 |
| final_decision | 下调 4 分；记录 `regrade_decision_id` |

## Feedback Templates

### Written Feedback Template

```text
rubric_item:
score:
strength:
missing_evidence:
next_step:
student_visible_feedback:
calibration_note:
```

### Programming Feedback Template

```text
rubric_item:
score:
public_tests:
hidden_category_feedback:
manual_review:
next_step:
student_visible_feedback:
calibration_note:
```

### Capstone Feedback Template

```text
rubric_item:
score:
reproducibility_evidence:
metric_evidence:
claim_strength:
next_step:
student_visible_feedback:
calibration_note:
```

## Double-Grading Resolution

| 场景 | 处理 |
|------|------|
| second_reader_delta <= 3% | 原 grader 和二评 grader 对照 anchor 后自行统一 |
| 3% < second_reader_delta <= 8% | Head TA 复核边界项并写入 calibration_note |
| second_reader_delta > 8% | Instructor 裁定，并把争议加入下一轮校准 |
| 涉及 hidden-test bug | 冻结 release_batch，按 gradebook/LMS 指南批量修正 |
| 涉及诚信或来源争议 | 转入 academic integrity case，不在本包写私人细节 |

决议记录至少包含 `anchor_id`、`rubric_item`、`original_score`、`revised_score`、`second_reader_delta`、`final_decision`、`feedback_to_student` 和 `regrade_decision_id`。若复核暴露 rubric ambiguity，应同步更新 [Grading Calibration Guide](grading-calibration.md) 和 [Instructor Solution Guide](instructor-solution-guide.md)。

## Release Checklist

| 检查项 | 通过标准 |
|--------|----------|
| no hidden tests | 不含 hidden test exact input、seed、完整期望输出或测试源码 |
| no reference_solution.py | 不引用或复制 `reference_solution.py`、私有 starter diff 或标准答案全文 |
| public-safe feedback | `feedback_to_student` 可直接贴给学生，且不泄露其他学生信息 |
| rubric traceability | 每个 anchor 都能追溯到 assignment handout、rubric 或 instructor guide |
| gradebook traceability | 二评、复核和批量修正都能对应 `release_batch`、`rubric_version`、`regrade_decision_id` |
| update hooks | 争议样例会反馈到 grading calibration、assignment guide、hidden-test design 或 project rubric |
