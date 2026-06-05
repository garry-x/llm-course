# Chapter 8 Assignment: Text Generation

本作业对应第 8 章文本生成。目标是实现从 logits 到 token 的核心解码策略，包括概率截断、重复惩罚、搜索、多样性指标和 reasoning 多样本聚合，并用小模型验证采样边界和生成行为。

## Files

- `starter.py`: 学生起始代码。
- `reference_solution.py`: 参考实现。
- `tests.py`: 可运行测试。

## Run

```bash
.venv/bin/python assignments/ch08_generation/tests.py
```

默认测试 `reference_solution.py`。测试学生代码时：

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch08_generation/tests.py
```

## Requirements

- 贪心解码只使用最后一个位置的 logits，并选择 `argmax`。
- `temperature=0` 必须退化为贪心，`temperature>0` 才能除以温度。
- Top-K 必须只在最高 K 个 token 内采样，并处理 `k > vocab_size`。
- Top-P 必须保留累计概率达到阈值的最小 nucleus，并重新归一化。
- `apply_repetition_penalty` 必须在采样前调整已出现 token 的 logits：正 logit 除以 penalty，负 logit 乘以 penalty，且不能原地修改输入。
- Beam search 必须保留多个候选，累加 log probability，并支持长度归一化评分。
- `pass_at_k` 应使用 `1 - C(n-c,k)/C(n,k)` 的采样成功率估计，连接代码/数学任务中的多样本评测。
- `self_consistency_vote` 应从多条 reasoning 输出中抽取最终答案，按多数投票聚合，并报告样本数、票数占比和 token 成本。
- `Generator` 应提供统一生成接口，并能计算 distinct-n 多样性指标。
- 简化推测解码应返回生成序列和接受率统计，便于比较 draft/target 一致性。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 比较 greedy、beam、temperature、top-k、top-p、repetition penalty、CoT/self-consistency/best-of-N、speculative decoding、生成评估指标和约束解码的适用边界 |
| Programming parts | 55 | 实现 greedy/beam/temperature、top-k、top-p、repetition penalty、pass@k、self-consistency vote、Generator 指标和 speculative decoding |
| Analysis / style | 10 | 解释质量、多样性、事实性、推理正确率、test-time compute、延迟、退化风险、参数 sweep 和采样参数边界 |
