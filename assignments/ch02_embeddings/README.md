# Ch02 Embedding 与位置编码作业测试

本目录把第 2 章的编程练习整理成可自动验收的作业入口，覆盖 TokenEmbedding、word vector 共现统计、skip-gram negative sampling、SinusoidalEncoding、RoPE 以及 RoPE 相对位置性质验证。

## 文件说明

| 文件 | 用途 |
|------|------|
| `starter.py` | 学生起始代码，包含需要实现的 TODO |
| `reference_solution.py` | 教师参考实现，用于验证测试本身 |
| `tests.py` | `unittest` 测试，覆盖 shape、共现计数、SGNS loss、buffer、范数保持和相对位置性质 |

## 学生运行方式

```bash
cp assignments/ch02_embeddings/starter.py assignments/ch02_embeddings/student_solution.py
# 编辑 student_solution.py 完成 TODO
STUDENT_MODULE=student_solution .venv/bin/python assignments/ch02_embeddings/tests.py
```

也可以直接让测试加载 `starter.py`：

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch02_embeddings/tests.py
```

也可以直接验证课程内置参考实现：

```bash
.venv/bin/python assignments/ch02_embeddings/tests.py
```

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 35 | 推导 embedding 参数量，解释 one-hot 与 lookup 等价性，比较 word2vec/GloVe 的统计目标，证明 self-attention 的置换等变性，推导 RoPE 点积依赖相对位置 |
| Programming parts | 55 | 实现 `TokenEmbedding`、共现矩阵、SGNS loss、`SinusoidalEncoding`、`RoPE` 和相对位置数值验证 |
| Analysis / style | 10 | 说明 RoPE 外推失败模式、odd head dimension 拒绝策略和 dtype/device 迁移 |
