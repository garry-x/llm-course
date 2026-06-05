# Ch04 多头注意力 / GQA / MLA 作业测试

本目录把第 4 章的 5 个编程练习整理成可自动验收的作业入口，覆盖 MHA、单头参数等价性、GQA、简化版 MLA 和 KV Cache 大小计算。

## 文件说明

| 文件 | 用途 |
|------|------|
| `starter.py` | 学生起始代码，包含需要实现的 TODO |
| `reference_solution.py` | 教师参考实现，用于验证测试本身 |
| `tests.py` | `unittest` 测试，覆盖 shape、mask、参数量、KV 头重复和 cache 压缩比 |

## 学生运行方式

```bash
cp assignments/ch04_multihead/starter.py assignments/ch04_multihead/student_solution.py
# 编辑 student_solution.py 完成 TODO
STUDENT_MODULE=student_solution .venv/bin/python assignments/ch04_multihead/tests.py
```

也可以直接让测试加载 `starter.py`：

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch04_multihead/tests.py
```

也可以直接验证课程内置参考实现：

```bash
.venv/bin/python assignments/ch04_multihead/tests.py
```

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 计算 MHA 参数量，比较 MHA/MQA/GQA/MLA 的 KV cache，解释 RoPE 与 latent cache 的边界 |
| Programming parts | 55 | 实现 MHA、单头对照、GQA、简化 MLA 和 KV cache 分析 |
| Analysis / style | 10 | 说明 head grouping、latent cache、mask broadcast 和实现复杂度取舍 |
