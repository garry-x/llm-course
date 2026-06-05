# Chapter 6 Assignment: GPT Model Assembly

本作业对应第 6 章的完整 GPT 组装练习。重点是实现 GPT-2 风格的稠密 Decoder-only 模型：token embedding、learned position embedding、causal self-attention、GELU MLP、LayerNorm、LM head 和 weight tying。

## Files

- `starter.py`: 学生起始代码。
- `reference_solution.py`: 参考实现。
- `tests.py`: 可运行测试。

## Run

```bash
.venv/bin/python assignments/ch06_gpt/tests.py
```

默认测试 `reference_solution.py`。测试学生代码时：

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch06_gpt/tests.py
```

## Requirements

- `GPTConfig()` 默认值应对应 GPT-2 small：`vocab_size=50257`、`max_seq_len=1024`、`d_model=768`、`n_heads=12`、`n_layers=12`。
- `GPTModel.forward(input_ids)` 返回形状为 `[batch, seq_len, vocab_size]` 的 logits。
- causal mask 必须阻止当前位置关注未来 token。
- `tie_weights=True` 时，`lm_head.weight` 和 `token_embedding.weight` 必须是同一个参数对象。
- 默认 GPT-2 small 参数量应为 `124,439,808`，这是 HuggingFace GPT-2 small 的常见总量；其中包含 tied embedding/LM head 只计一次。
- `MoERouter` 返回 top-k 专家索引和重新归一化后的 top-k 权重。

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 30 | 计算 GPT-2 small 参数量，解释 label shift、weight tying、causal leakage 测试、MoE 稀疏激活和负载均衡 |
| Programming parts | 60 | 实现 GPTConfig、causal attention、GPTModel、初始化/tying 和 MoE router |
| Analysis / style | 10 | 区分 total/activated parameters，报告参数分析、next-token logits 对齐和未来 token 泄漏检查 |
