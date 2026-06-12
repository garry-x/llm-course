# Python and PyTorch Review Session

本 handout 用于 Week 1 Python Review Session 和 Week 2 PyTorch Tutorial Session。它和 [数学与 PyTorch 先修复习](math-prerequisites.md)、[10 周 / 20 讲 Lecture Plan](lecture-plan.md) 配套，帮助学生把 Python、张量 shape、autograd 和测试定位能力直接接到 Transformer 代码练习。

本课程在 Week 1 安排 Python Review Session，在 Week 2 安排 PyTorch Tutorial Session，并把两次 review 合并为可移植 handout：学生先确认环境和 Python helper，再进入 PyTorch tensor、`nn.Module`、loss、autograd 和作业提交日志。

## Session 目标

| Session | 时长 | 面向对象 | 通过产出 |
|---------|:--:|----------|----------|
| Python Review Session | 80-90 分钟 | Python 基础 Borderline、跨语言转入、未完成 Ch01 helper 的学生 | 能实现 pair counting、non-overlapping merge、文件读取和异常边界 |
| PyTorch Tutorial Session | 80-90 分钟 | PyTorch 基础 Borderline、shape 推导不稳、未完成 Ch02 starter 的学生 | 能解释 `[B,T,D]` 到 logits，计算 next-token CE，并定位一个失败测试 |

## 课前准备

从仓库根目录运行：

```bash
.venv/bin/python -c "import sys, torch; print(sys.version.split()[0], torch.__version__, torch.cuda.is_available())"
.venv/bin/python run_assignment_tests.py
STUDENT_MODULE=starter .venv/bin/python assignments/ch01_bpe/tests.py
STUDENT_MODULE=starter .venv/bin/python assignments/ch02_embeddings/tests.py
```

如果 `.venv/bin/python run_assignment_tests.py` 失败，先按 Environment and Reproducibility Guide 记录 `Python executable`、`PyTorch version`、`CUDA available` 和第一个失败项。

## Python Review Session 议程

| 时间 | 主题 | 活动 | 产出 |
|------|------|------|------|
| 0-10 分钟 | 环境 smoke test | 运行 `.venv/bin/python -c "import sys, torch; ..."` | 记录解释器、PyTorch 版本和工作目录 |
| 10-25 分钟 | 函数与测试 | 阅读 `assignments/ch01_bpe/tests.py` 的 helper tests | 写出 `_get_stats` 的输入、输出和空边界 |
| 25-45 分钟 | 字典与 pair counting | 手写 `count_pairs(tokens)` | 能处理空列表、单元素和重复 pair |
| 45-65 分钟 | non-overlapping merge | 对 `[1,1,1]` 和 pair `(1,1)` 手算再实现 | 说明为什么不能重叠 merge |
| 65-80 分钟 | 文件、异常和日志 | 读非空行，保留第一个失败 traceback | 提交最小 run log |
| 80-90 分钟 | Exit ticket | 写一个仍不确定的问题 | 进入 office hours triage |

### Python Drill

学生应能在不看参考解的情况下解释：

- 为什么 `_get_stats([])` 和 `_get_stats([1])` 都返回空字典。
- 为什么 `list.append(x)` 会原地修改，而 `list + [x]` 会创建新列表。
- 为什么默认参数不写 `items=[]`。
- 什么时候应该抛出 `ValueError` 或 `KeyError`，而不是静默返回空结果。
- 为什么测试失败时要保留第一个 traceback，而不是只截最后一行。

## PyTorch Tutorial Session 议程

| 时间 | 主题 | 活动 | 产出 |
|------|------|------|------|
| 0-10 分钟 | Tensor shape contract | 写出 `[B,T] -> [B,T,D] -> [B,T,V]` | shape trace |
| 10-25 分钟 | Embedding lookup | 比较 `nn.Embedding` 和 `one_hot @ E` | 说明 lookup 等价关系 |
| 25-40 分钟 | Linear projection | 给定 `x @ W` 推导 logits shape | 参数量和输出 shape |
| 40-55 分钟 | next-token CE | flatten logits/labels 或使用等价实现 | loss 输入输出说明 |
| 55-70 分钟 | autograd | 执行 forward、loss、backward，检查 `.grad` | 梯度流向说明 |
| 70-85 分钟 | debug drill | 定位 dtype、device、contiguous、mask 或 shape 错误 | 第一个失败测试和修复假设 |
| 85-90 分钟 | Exit ticket | 写出一个 PyTorch bug pattern | FAQ 或 office hours 记录 |

### PyTorch Drill

必会检查项：

- Shape trace: [B,T,D] 到 logits 的路径必须能用文字和张量维度同时说明。
- `input_ids` dtype 应为 integer token ids；embedding 输出是 floating tensor。
- logits `[B,T,V]` 和 labels `[B,T]` 计算 CE 时，batch/time 维度必须对齐。
- `.reshape` 比 `.view` 更适合可能不连续的张量。
- `model.train()` / `model.eval()` 会影响 dropout 或部分 normalization 行为。
- `loss.backward()` 后应检查关键参数 `.grad is not None`，但不要把梯度值是否全相同当作正确性产出。

## 常见失败与处理

| 失败模式 | 典型症状 | 处理 |
|----------|----------|------|
| 工作目录错误 | `FileNotFoundError` 或找不到 assignments | 回到仓库根目录运行命令 |
| 模块选择错误 | 测试导入了错误文件 | 使用 `STUDENT_MODULE=starter` 或提交包要求的模块名 |
| dtype 错误 | embedding 报 token ids 类型错误 | token ids 使用 integer tensor，logits/loss 使用 floating tensor |
| shape 错误 | CE flatten 后 batch/time 错位 | 写出 `[B,T,V] -> [B*T,V]` 和 `[B,T] -> [B*T]` |
| device 错误 | CPU/GPU tensor 混用 | 本课程公开测试默认 CPU；GPU 只作为扩展 |
| 静默吞异常 | 测试失败但没有 traceback | 保留第一个失败 traceback 和命令 |

## 学生提交模板

```text
Session:
Command:
Working directory:
Python executable:
Python version:
PyTorch version:
CUDA available:
First failing test:
Shape trace:
Fix hypothesis:
Question for office hours:
```
