# Grading Calibration Guide

本指南用于教师和助教在正式批改前统一评分口径。它补充 `written-problem-set.md`、`instructor-solution-guide.md`、assignment rubrics、capstone rubrics、[Programming Assignment Code Quality Rubric](programming-assignment-code-quality-rubric.md)、[Grading Anchor Sample Feedback Pack](grading-anchor-sample-feedback-pack.md)、[Grading Drift Audit Ledger](grading-drift-audit-ledger.md)、[TA Training and Certification Dossier](ta-training-certification.md) 和 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md)，重点解决同一份答案在不同助教之间分数不一致的问题；成绩册字段、权重复算、late-day ledger 和 regrade workflow 由 gradebook/LMS 指南维护。

## 校准流程

每次作业发布前：

1. 教师选择正式题目和隐藏测试范围。
2. 助教共同批改 3-5 份样例答案、教师准备的 synthetic answer，或 [Grading Anchor Sample Feedback Pack](grading-anchor-sample-feedback-pack.md) 中的 anchor sample。
3. 对每题明确“满分证据”“部分分证据”“不通过证据”。
4. 记录容易误判的合理替代表达。
5. 更新本指南或 `instructor-solution-guide.md` 中的常见扣分点。

每次作业批改中：

- 先跑公开测试和隐藏测试，再看书面解释。
- 编程题不要只按测试给分；要抽查 shape、边界处理和硬编码风险。
- 书面题不要只看最终公式；要看符号定义、维度、条件和解释。
- 对分数边界样例进行二次评阅。

每次作业批改后：

- 汇总隐藏测试失败率。
- 汇总学生最常见的 3 个误解。
- 记录需要在下一讲 recap 或 office hours 中澄清的问题。

## 双评一致性规则

建议对以下提交进行双评：

- 分数落在等级边界附近，例如 89/90、79/80、59/60。
- 自动测试全过但书面解释明显薄弱。
- 自动测试失败但代码思路接近正确。
- 涉及学术诚信、AI 工具披露或引用争议。
- Capstone 报告数字与日志不一致。

若两名助教分差超过 8%，处理流程：

1. 各自指出具体 rubric 项。
2. 对照本指南中的满分/部分分/不通过证据。
3. 若仍无法一致，由教师给最终裁定。
4. 把争议点写入下一版校准记录；若分歧可复用为锚点，则补充到 [Grading Anchor Sample Feedback Pack](grading-anchor-sample-feedback-pack.md)。

## 书面题校准样例

### BPE Merge

满分证据：

- 说明一次 merge 只合并非重叠 pair。
- 正确区分 pair 出现次数和序列长度减少量。
- 解释 tie-breaking 影响最终词表。
- 至少提到 byte-level BPE 对 OOV 的影响。

部分分证据：

- 能手算 merge，但没有解释非重叠。
- 能比较 word/char/BPE，但忽略多语言或 byte fallback。
- 只说贪心不最优，但没有给反例思路。

不通过证据：

- 把所有重叠 pair 都合并。
- 认为 BPE 学到语义最优分词。
- 把 vocab size 和序列长度变化混为一谈。

### RoPE 相对位置

满分证据：

- 写出二维旋转 block。
- 推出 `R_m^T R_n = R_{n-m}`。
- 说明点积依赖相对位移。
- 说明长上下文外推还受训练分布、频率和数值范围影响。

部分分证据：

- 能解释旋转位置编码，但没有完整矩阵推导。
- 能说相对位置，但没有说明点积形式。
- 只提长上下文优点，未提限制。

不通过证据：

- 把 RoPE 说成 learned absolute embedding。
- 忘记 head dim 成对旋转。
- 认为 RoPE 保证任意长度无损泛化。

### Attention Scaling 与 Mask

满分证据：

- 推导 `Var(q^T k)=d_k`。
- 解释除以 `sqrt(d_k)` 避免 softmax 饱和。
- 说明 mask 应在 softmax 前应用。
- 写清 score/probability/context 的 shape。

部分分证据：

- 只给直觉，未给方差推导。
- mask 矩阵方向正确，但广播 shape 不清楚。
- 能说 causal mask 防未来，但没有说明 softmax 前后差异。

不通过证据：

- 在 softmax 后乘 mask 且不重新归一化。
- 把 causal mask 写成允许未来 token。
- 把训练 activation 显存和推理 KV cache 混为一谈。

### DPO / GRPO

满分证据：

- DPO 中 chosen/rejected log-ratio 方向正确。
- 解释 reference model 和 `beta` 的作用。
- GRPO 中 advantage 在 prompt group 内白化。
- 能列出 reward hacking、分布外泛化或安全局限。

部分分证据：

- 能写 DPO loss，但没有解释 reference model。
- 能说 GRPO 不用 critic，但没有说明组内标准化。
- 只讲优势，不讲局限。

不通过证据：

- chosen/rejected 方向写反。
- 认为 DPO 不需要 reference model。
- 把 GRPO 描述成完整安全对齐方案。

### KV Cache 显存

满分证据：

- 公式包含 `2 * batch * layers * seq_len * kv_heads * head_dim * dtype_bytes`。
- 解释 2 表示 K/V。
- 能区分 MHA/GQA/MLA 对 kv heads 或 latent cache 的影响。
- 能把显存估算联系到 batch、context 和 SLO。

部分分证据：

- 公式漏掉 batch 或 dtype，但其他维度正确。
- 能解释 KV cache 作用，但没有连接到服务容量。
- 只报告平均延迟，未报告 P95/P99。

不通过证据：

- 把参数显存当作 KV cache 显存。
- 漏掉 K/V 两份。
- 认为 cache 会降低 prefill 计算复杂度。

## 编程作业校准

### 满分代码特征

- 通过公开测试和隐藏测试。
- API 与 starter 保持一致。
- shape、dtype、device、非法参数处理清楚。
- 没有硬编码公开样例。
- 能在错误分析中解释至少一个失败或边界情况。

### 部分分代码特征

- 主路径正确，但边界条件失败。
- 数值上接近 reference，但容差或 dtype 处理不稳定。
- 代码可读性一般，但核心算法正确。
- 公开测试通过，隐藏性质测试失败。

### 不通过代码特征

- 不能 import 或编译。
- 修改测试或依赖参考答案。
- 只返回固定 shape 或硬编码输出。
- 跳过核心计算但用 residual 或默认值掩盖错误。

### 代码评分常见争议

| 情况 | 建议处理 |
|------|----------|
| 学生实现与 reference 不同但数学等价 | 若测试性质和人工检查都通过，应给分 |
| 浮点结果微小差异 | 按 `autograder-hidden-tests.md` 的容差，不要求逐 bit 相等 |
| 只在 GPU 上失败 | 若作业要求 CPU 可运行，按复现性扣分 |
| 公开测试全过但隐藏测试失败 | 按隐藏测试 rubric 扣分，并要求错误分析 |
| 代码很短但正确 | 不因短而扣分；只看 API、正确性、边界和解释 |

## Capstone 报告校准

### A 档报告

- 问题定义具体，成功标准可测。
- 提供完整复现命令、环境、seed、日志和数据版本。
- 有 baseline、ablation 或对照实验。
- 指标覆盖质量、延迟/吞吐、成本和失败案例。
- 报告数字能从提交文件或日志复现。
- 能说明结论的适用范围和不确定性。

### B 档报告

- 系统能跑通，核心指标齐全。
- 有失败案例，但归因不够深入。
- 有复现命令，但环境或数据版本说明不完整。
- 有引用，但来源等级或访问日期不全。

### C 档报告

- demo 能跑，但报告更像操作日志。
- 只有成功案例，失败分析薄弱。
- 指标只报告平均值，缺少 P95/P99 或错误率。
- 成本、显存或数据质量分析不完整。

### 不通过报告

- 无法复现核心结果。
- 报告数字与日志矛盾。
- 没有失败案例。
- 使用前沿模型数据但没有来源。
- 无法解释核心代码或关键公式。

## 阅读复盘校准

满分复盘：

- 说明论文或文档解决的问题。
- 解释一个公式、算法或实验设计。
- 连接到课程章节、作业函数或 capstone 模块。
- 标注来源等级、链接和访问日期。
- 提出一个可验证问题或复现实验。

部分分复盘：

- 摘要准确，但缺少代码连接。
- 有来源链接，但未说明来源等级。
- 有问题意识，但不能转化为实验或检查。

不通过复盘：

- 只复述摘要。
- 没有引用。
- 把博客、新闻或社区传闻当作稳定事实。

## 同伴 Review 校准

高质量 review：

- 指向具体命令、日志、图表、指标或文件。
- 明确最强证据和最大风险。
- 建议能在一轮修改中完成。
- 至少检查一个引用或模型 claim。

低质量 review：

- 只说“很好”“可以更详细”。
- 没有复现尝试。
- 不区分个人偏好和技术问题。
- 没有指出风险或证据。

## 复核请求处理

学生复核请求必须包含：

- 作业或项目名称。
- 具体 rubric 项。
- 当前得分和期望复核的理由。
- 对应提交文件、日志或题号。

助教处理原则：

- 只复核学生指出的具体项，除非发现系统性错误。
- 复核可能上调或下调分数。
- 若复核暴露 rubric 含糊，应更新校准指南。
- 涉及学术诚信或 AI 工具披露时交由教师处理。
- 复核状态、`regrade_decision_id`、批量修正范围和学生可见决定说明按 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md) 记录。

## 校准记录模板

```text
Assignment:
Date:
Graders:
Sample size:

Disagreement case:
Rubric item:
Reason for disagreement:
Final decision:
Rule added or clarified:
```
