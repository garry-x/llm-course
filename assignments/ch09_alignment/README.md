# Chapter 9 Assignment: Fine-tuning and Alignment

本作业对应第 9 章微调与对齐。目标是实现 SFT 的 label mask、LoRA 低秩适配、奖励模型 pairwise loss、DPO 偏好损失与隐式 reward、PPO clipped objective、近似 KL 控制、偏好长度偏差统计、GRPO 组内白化、GRPO policy loss 账本、RLVR/RFT grader 健康报告和 LoRA 合并推理。

## Files

- `starter.py`: 学生起始代码。
- `reference_solution.py`: 参考实现。
- `tests.py`: 可运行测试。

## Run

```bash
.venv/bin/python assignments/ch09_alignment/tests.py
```

默认测试 `reference_solution.py`。测试学生代码时：

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch09_alignment/tests.py
```

## Requirements

- SFT labels 中 prompt 和 padding 位置必须为 `-100`，只对 assistant response 计算损失。
- `sequence_log_probs` 必须先把 `-100` 替换成安全索引再 `gather`，再用 mask 去掉无效位置。
- LoRA 初始输出应等于原线性层输出；只有 LoRA 的 `A/B` 参数可训练。
- 奖励模型 pairwise loss 必须实现 Bradley-Terry 的 `-log sigmoid(r_chosen - r_rejected)`。
- DPO loss 必须使用 policy/reference 的 chosen/rejected log-ratio。
- `dpo_implicit_rewards` 必须把 `beta * (log pi_policy - log pi_ref)` 显式报告为 chosen/rejected 隐式 reward、margin、preference probability 和 preference accuracy。
- `ppo_clipped_policy_loss` 必须用 `min(ratio * advantage, clipped_ratio * advantage)` 计算 PPO surrogate，并报告 mean ratio、clip fraction 和近似 KL。
- `approx_kl_from_logps` 必须实现采样 token 上的近似 KL：`exp(log_ref - log_policy) - (log_ref - log_policy) - 1`，并正确忽略 padding mask。
- 偏好长度偏差统计必须报告 chosen/rejected 长度差均值和三类比例。
- GRPO advantages 必须在同 prompt 的组内白化。
- `grpo_policy_loss` 必须把组内白化 advantages 扩展到 completion tokens，计算 PPO clipped surrogate、masked approximate KL、KL penalty 后的 total loss，并报告 clip fraction、mean ratio 和 mean advantage。
- `rlvr_grader_report` 必须报告 reward signal、cost 和 integrity gate，判断可验证 grader 是否适合继续 RL-style post-training。
- `merge_lora` 必须把 `B @ A * scaling` 合并回基础线性层权重。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 推导 SFT mask、LoRA 参数量、Bradley-Terry RM loss、DPO log-ratio 与隐式 reward、PPO clipped objective、近似 KL、偏好数据偏差、GRPO 组内白化、RLVR/RFT grader 适用条件、奖励漏洞边界和对齐评估协议 |
| Programming parts | 55 | 实现 SFT dataset/loss、sequence log prob、LoRA、pairwise reward loss、DPO loss、DPO implicit rewards、PPO clipped objective、近似 KL、偏好长度偏差统计、GRPO advantages、GRPO policy loss 和 `rlvr_grader_report` |
| Analysis / style | 10 | 区分数据格式、目标函数、reference model、偏好数据偏差、可验证 reward、grader 覆盖率、helpfulness/honesty/harmlessness、过度拒答和能力回归 |
