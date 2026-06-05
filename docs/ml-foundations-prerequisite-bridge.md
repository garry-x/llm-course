# ML Foundations Prerequisite Bridge

本 handout 补齐 CS224N 风格先修中的 college calculus、probability/statistics 和 foundations of machine learning。它不是独立机器学习课程，而是把学生需要带入本课程的最小概念映射到 LLM 章节、作业、书面题和项目报告。它补充 [Prerequisite Diagnostic](prerequisite-diagnostic.md)、[数学与 PyTorch 先修复习](math-prerequisites.md)、[Python and PyTorch Review Session](python-pytorch-review-session.md)、[逐周阅读清单与复盘 Handout](reading-list.md)、[Course Outcome Map](course-outcome-map.md) 和 [Project Report Template and Reproducibility Checklist](project-report-template.md)。

## 覆盖范围

| 先修主题 | 本课程用途 | 最低掌握证据 |
|----------|------------|--------------|
| Calculus / gradients | loss、backprop、optimizer、LayerNorm、DPO/GRPO | 能解释 chain rule、partial derivative、gradient direction 和局部线性近似 |
| Probability | language model likelihood、softmax、sampling、perplexity、preference data | 能写出条件概率、联合分解、期望、方差和 log probability |
| Statistics | train/validation split、confidence、benchmark variance、error analysis | 能区分样本均值、方差、置信区间、随机 seed 和分布偏移 |
| ML objectives | maximum likelihood、cross entropy、regularization、preference loss | 能把公式连接到 Ch07/Ch09 的实现和测试 |
| Generalization | overfitting、data leakage、contamination、held-out evaluation | 能解释 val loss、test set、hidden tests 和项目评测集的边界 |
| Optimization | gradient descent、learning rate、weight decay、scheduler、early stopping | 能读训练曲线并提出可复现实验 |
| Evaluation | metric design、baseline、ablation、statistical uncertainty | 能说明一个指标支持什么结论、不支持什么结论 |

## Diagnostic Add-on

若学生未修过系统 ML 课程，应在 Week 0 / Week 1 完成以下短诊断。它可作为 [Prerequisite Diagnostic](prerequisite-diagnostic.md) 的补充分项。

| 模块 | 题目 | 通过标准 |
|------|------|----------|
| calculus | 对 `loss = (wx - y)^2` 写出 `d loss / d w`，并解释梯度下降更新方向 | 不只套公式，能说明 update 如何改变 prediction |
| probability | 把 `P(x_1, x_2, x_3)` 写成自回归条件概率乘积 | 条件对象和顺序正确 |
| statistics | 给定两个 benchmark run 的 P95 latency，说明为什么单次 run 不足以证明系统更快 | 提到方差、样本量、随机性或负载条件 |
| ML objective | 解释 cross entropy 为什么对应 maximum likelihood | 能连接 `-log p_y` 与提高正确 token 概率 |
| generalization | train loss 下降、val loss 上升时列出 3 个排查方向 | 提到 overfitting、data leakage、split、regularization 或 early stopping |
| evaluation | 为 RAG QA 项目选择至少 3 个指标，并说明每个指标的局限 | 同时覆盖 retrieval、generation 和 latency/safety 中至少两类 |

建议评分为完成/未完成。若 6 题中少于 4 题通过，学生应先完成本 handout 的补救任务，再提交第一个 graded programming assignment。

## Mini-Lecture: Calculus to Backprop

学生不需要手写大型 Jacobian，但必须理解梯度如何在计算图中传播：

```text
y_hat = model(x; theta)
loss = L(y_hat, y)
theta <- theta - lr * d loss / d theta
```

最低要求：

- chain rule：复合函数梯度逐层相乘。
- partial derivative：多参数函数中只看某个参数方向的局部变化。
- gradient vector：所有参数方向的偏导数组成更新方向。
- local linear approximation：小步更新近似由一阶导数解释。

课程连接：

| 课程位置 | 需要的 calculus 直觉 |
|----------|----------------------|
| Ch03 attention | score、softmax、weighted sum 都在同一计算图中 |
| Ch05 LayerNorm | mean 和 variance 依赖输入，反向传播不能只除以 std |
| Ch07 AdamW | gradient、momentum、weight decay 和 learning rate 分工不同 |
| Ch09 DPO | chosen/rejected log ratio 的方向决定偏好更新 |

## Mini-Lecture: Probability and Language Models

自回归语言模型使用条件概率分解：

```text
P(x_1, ..., x_T) = product_t P(x_t | x_<t)
log P(x_1, ..., x_T) = sum_t log P(x_t | x_<t)
```

课程中常见概率对象：

| 对象 | 解释 | 常见误区 |
|------|------|----------|
| softmax probability | logits 归一化后的类别分布 | logits 本身不是概率 |
| cross entropy | 对目标 token 的负 log probability 平均 | loss 低不等于事实正确 |
| perplexity | `exp(cross_entropy)` | PPL 不能单独评估开放式回答质量 |
| sampling temperature | 改变分布尖锐度 | temperature 不保证真实性 |
| top-p nucleus | 保留累计概率达到阈值的最小集合 | top-p 的候选数不是固定的 |

## Mini-Lecture: Statistics for Experiments

训练和推理项目必须避免把单次结果当成稳定结论。

| 统计概念 | 课程用法 | 报告要求 |
|----------|----------|----------|
| sample mean | 平均 loss、平均 latency、平均 score | 同时报告样本数和条件 |
| variance / std | 多次 run、不同 prompt、不同 batch 的波动 | 解释异常值和失败样例 |
| confidence interval | 小样本评测的不确定性 | 可用 bootstrap 或 repeated runs 估计 |
| distribution shift | train/dev/test 或线上流量不同 | 描述 split 和代表性 |
| data leakage | 训练数据、检索库或 prompt 泄漏答案 | 记录去重、污染检查和 held-out 集 |
| seed sensitivity | 不同初始化或采样导致指标变化 | 至少固定 seed，并说明仍可能不完全复现 |

## Mini-Lecture: ML Objectives and Generalization

| 概念 | 最小解释 | 本课程证据 |
|------|----------|------------|
| maximum likelihood | 提高数据中目标 token 或标签的概率 | Ch07 CE、Ch09 SFT |
| empirical risk | 在样本上的平均 loss | train/val loss table |
| regularization | 限制模型或更新以减少过拟合 | weight decay、dropout、early stopping |
| baseline | 证明新方法有价值的比较对象 | greedy vs top-p、no RAG vs RAG、mock engine vs serving engine |
| ablation | 移除一个组件看影响 | LoRA rank、chunk size、cache on/off |
| held-out evaluation | 不参与训练或调参的数据 | validation set、hidden tests、final eval set |

学生报告中不能只写“模型效果不错”。至少要写清：

- baseline 是什么。
- metric 衡量什么。
- split 如何产生。
- 是否调参使用了 eval set。
- 失败案例如何分类。
- 哪个结论只在当前数据、seed、模型或硬件条件下成立。

## Project Evidence Checklist

| evidence_id | 要求 |
|-------------|------|
| objective_mapping | loss、reward、metric 或 SLO 对应项目目标 |
| baseline_result | 至少一个简单 baseline 或 no-system baseline |
| split_statement | train/dev/test、retrieval corpus/eval queries 或 benchmark prompt 的来源 |
| leakage_check | 数据去重、prompt 泄漏、retrieval contamination 或 benchmark contamination / public benchmark 污染检查 |
| variance_note | repeated run、bootstrap、seed sensitivity 或负载波动说明 |
| ablation_plan | 至少一个组件、超参或数据处理的对比 |
| metric_limit | 每个关键 metric 的局限 |
| generalization_boundary | 结论不能推广的条件 |

## 补救任务

| 薄弱项 | 补救任务 | 验收 |
|--------|----------|------|
| calculus | 手推 CE 梯度或 DPO log-ratio 方向 | 能解释更新方向，而不是只写公式 |
| probability | 完成 language model likelihood 分解和 top-p/top-k 对比 | 能说明概率分布和采样候选集 |
| statistics | 对 3 次 benchmark 结果计算 mean/std 并解释不确定性 | 报告样本数、条件和局限 |
| ML objectives | 把 Ch07 training loss、Ch09 SFT/DPO loss 和项目 metric 分别解释 | 能区分训练目标和评价指标 |
| generalization | 为项目写 split、baseline、ablation 和 leakage check | 进入 proposal 或 milestone |

## Staff Checklist

- Week 0/1 对未修过 ML 基础课的学生发布本 handout。
- `Prerequisite Diagnostic` 对 calculus、statistics 和 ML foundations 低分学生给出补救任务。
- Week 5 前检查训练项目 proposal 是否写清 objective、split、baseline 和 leakage_check。
- Week 9 前检查推理项目 proposal 是否写清 benchmark variance、metric_limit 和 generalization_boundary。
- 期末报告 rubric 中 objective、baseline、ablation、variance 和 leakage 的扣分口径与本 handout 一致。

## 发布前 Checklist

- syllabus、prerequisite diagnostic、math prerequisites、reading list 和 CS224N crosswalk 均链接本 handout。
- `scripts/build_course_site_release.py` 把本文件列入学生安全文档。
- `.venv/bin/python verify_course.py` 通过。
