# Ch01 BPE Tokenizer 作业测试

本目录把第 1 章的 5 个编程练习整理成可自动验收的作业入口。目标不是替代章节讲解，而是给学生一个类似高校课程作业的提交标准。

## 文件说明

| 文件 | 用途 |
|------|------|
| `starter.py` | 学生起始代码，包含需要实现的 TODO |
| `reference_solution.py` | 教师参考实现，用于验证测试本身 |
| `tests.py` | `unittest` 测试，覆盖 `_get_stats`、`_merge`、`train`、`encode`、`decode`、tokenizer 统计报告和分组 token 成本比较 |

## 学生运行方式

```bash
cp assignments/ch01_bpe/starter.py assignments/ch01_bpe/student_solution.py
# 编辑 student_solution.py 完成 TODO
STUDENT_MODULE=student_solution .venv/bin/python assignments/ch01_bpe/tests.py
```

也可以直接让测试加载 `starter.py`：

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch01_bpe/tests.py
```

也可以直接验证课程内置参考实现：

```bash
.venv/bin/python assignments/ch01_bpe/tests.py
```

## 评分 Rubric

| 项目 | 分值 | 标准 |
|------|:--:|------|
| Written questions | 30 | 解释 byte-level BPE 可逆性、频率合并的压缩启发式、tie-breaking 对词表的影响、词表大小与序列长度/嵌入参数量/多语言和领域文本成本的权衡 |
| Programming parts | 60 | 实现 `_get_stats`、`_merge`、`train`、`encode`、`decode`、`tokenizer_report` 和 `tokenizer_group_report`，通过中英文、emoji、多字节 UTF-8 round trip 与分组 token 成本统计 |
| Analysis / style | 10 | 报告至少 2 个 tokenizer 失败或边界案例，并比较压缩率、可逆性、特殊 token 和领域文本切分 |
