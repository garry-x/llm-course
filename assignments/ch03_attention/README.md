# Ch03 Scaled Dot-Product Attention 作业测试

本目录把第 3 章的编程练习整理成可自动验收的作业入口，覆盖 QKV 投影、Scaled Dot-Product Attention、self-attention permutation equivariance、softmax/attention 反向传播、Q/K/V 手写梯度、attention entropy、attention score 显存估算、Causal Mask、causal+padding mask 合成、因果注意力和注意力热力图函数。

## 文件说明

| 文件 | 用途 |
|------|------|
| `starter.py` | 学生起始代码，包含需要实现的 TODO |
| `reference_solution.py` | 教师参考实现，用于验证测试本身 |
| `tests.py` | `unittest` 测试，覆盖 shape、缩放、mask、置换等变性、softmax Jacobian、attention logits gradient、Q/K/V gradients、attention entropy、attention score 显存、因果约束、padding key 屏蔽和可视化返回值 |

## 学生运行方式

```bash
cp assignments/ch03_attention/starter.py assignments/ch03_attention/student_solution.py
# 编辑 student_solution.py 完成 TODO
STUDENT_MODULE=student_solution .venv/bin/python assignments/ch03_attention/tests.py
```

也可以直接让测试加载 `starter.py`：

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch03_attention/tests.py
```

也可以直接验证课程内置参考实现：

```bash
.venv/bin/python assignments/ch03_attention/tests.py
```

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 推导 `1/sqrt(d_k)` scaling、self-attention 置换等变性、softmax Jacobian、attention logits 到 Q/K/V 的链式法则、attention entropy、mask 加在 softmax 前的原因、causal mask 与 padding mask 的形状广播、all-masked row 的 NaN 风险、复杂度和 heatmap 解释边界 |
| Programming parts | 55 | 实现 QKV projection、scaled dot-product attention、置换等变性数值验证、softmax/attention backward helpers、Q/K/V gradient helper、attention entropy、attention score 显存估算、causal mask、causal+padding mask 合成和 attention visualization |
| Analysis / style | 10 | 解释 mask 数值稳定性、padding key 与 padding query 的区别、attention heatmap 的适用范围和常见 shape bug |
