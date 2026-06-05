# Prerequisite Diagnostic

本诊断用于开课前确认学生是否具备进入课程的最低准备。它不是淘汰测试，而是帮助学生和教师判断需要补哪一块：Python、PyTorch、线性代数、概率统计、反向传播、ML foundations 或工程复现。微积分、统计和机器学习基础补救见 [ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md)。

建议在第 1 周第一次课前完成，限时 60-90 分钟。允许查阅 Python/PyTorch 官方文档，但不允许直接使用他人答案。

## 通过标准

| 等级 | 分数 | 建议 |
|------|:--:|------|
| Ready | 80-100 | 可直接进入 Ch01-Ch02，同时完成常规阅读复盘 |
| Borderline | 60-79 | 可以选课，但第 1 周必须完成补救任务和 office hours 检查 |
| At Risk | 40-59 | 建议先完成 Python/PyTorch 和数学补课，再开始正式作业 |
| Not Ready | 0-39 | 不建议直接进入本课程；先完成基础编程、线代和 ML 入门 |

教师可根据班级背景调整阈值。若学生在 PyTorch 或线代任一项低于 50%，即使总分超过 60，也应完成对应补救任务。

## 诊断结构

| 模块 | 分值 | 目标 |
|------|:--:|------|
| Python 基础 | 15 | 能读写函数、列表/字典、文件和异常 |
| PyTorch 基础 | 25 | 能正确处理 tensor shape、broadcast、module、loss 和 autograd |
| 线性代数、概率与统计 | 20 | 能推导矩阵乘法 shape、softmax、cross entropy、简单概率和 benchmark variance |
| 反向传播与数值稳定性 | 20 | 能解释梯度流、log-sum-exp、LayerNorm 依赖 |
| 复现与调试纪律 | 20 | 能固定 seed、记录命令、解释测试失败和环境版本 |

## Python 基础

1. 写一个函数 `count_pairs(tokens)`，返回相邻 pair 的计数字典。
2. 给定一个文本文件路径，读取非空行并去掉首尾空白。
3. 解释 `list.append(x)` 与 `list + [x]` 的差异。
4. 说明为什么不要在默认参数中写 `items=[]`。
5. 给出一个 `try/except` 场景：什么时候应该抛出异常，而不是静默返回空结果。

满分证据：

- 函数能处理空列表、单元素列表和重复 pair。
- 文件读取能关闭文件或使用 context manager。
- 能解释 mutable default argument 的状态共享问题。

## PyTorch 基础

1. 给定 `x` shape 为 `[B, T, D]`，`W` shape 为 `[D, 3D]`，写出 `x @ W` 的输出 shape。
2. 给定 `q, k, v` shape 都为 `[B, H, T, D]`，写出 attention scores 和 context 的 shape。
3. 写一个最小 `nn.Module`，包含 `Embedding` 和 `Linear`，输入 token ids 输出 logits。
4. 解释 `model.train()` 与 `model.eval()` 对 dropout 或 norm 的影响。
5. 说明 `.view()` 和 `.reshape()` 在非连续张量上的差异。
6. 给定 logits `[B, T, V]` 和 labels `[B, T]`，说明如何计算 next-token cross entropy。

满分证据：

- shape 推导不丢 batch/head/time 维度。
- loss 计算能正确 flatten logits/labels 或使用等价实现。
- 能说明 device、dtype 和 `requires_grad` 的基本含义。

## 线性代数、概率与统计

1. 解释点积、矩阵乘法和 cosine similarity 的关系。
2. 推导 `Q @ K.transpose(-2, -1)` 为什么得到 pairwise score matrix。
3. 说明 softmax 输出为什么是概率分布。
4. 给定两个 token 序列概率，说明自回归 LM 如何分解联合概率。
5. 解释 perplexity 与 cross entropy 的关系。
6. 给定三次 benchmark 的 P95 latency，说明为什么只看一次运行不能证明系统更快。

满分证据：

- 能写出 shape，而不是只写公式。
- 能说明 softmax 数值稳定化时为什么减去最大值不改变分布。
- 能把 `loss = -log p_y` 与最大似然联系起来。
- 能说明样本数、方差、seed 和负载条件如何影响实验结论。

## ML Foundations

1. 解释 maximum likelihood、cross entropy 和 empirical risk 的关系。
2. 区分 training loss、validation loss、test metric 和 hidden tests。
3. 给出一个 overfitting、data leakage 或 benchmark contamination 的例子。
4. 为一个 RAG 或 serving 项目列出 baseline、ablation 和 held-out evaluation。
5. 说明为什么一个 metric 不能支持所有结论。

满分证据：

- 能把 objective、baseline、split、ablation 和 metric limit 写成可复核证据。
- 能解释训练目标与最终评价指标的差异。
- 能说明结论的 generalization boundary。

## 反向传播与数值稳定性

1. 对 `y = xW + b`，说明 loss 的梯度会流向哪些变量。
2. 解释 embedding 层为什么只有被索引到的行收到梯度。
3. 给出 softmax cross entropy 的梯度形式 `p_i - 1[i=y]`。
4. 说明 LayerNorm backward 为什么不能只写成除以标准差。
5. 举一个会产生 NaN 的训练场景，并说明应该记录哪些证据。

满分证据：

- 能描述链式法则在张量图上的传播路径。
- 能识别 log overflow、division by zero、mask 后全为 `-inf` 等常见数值风险。
- 能把梯度问题和测试/日志连接起来。

## 复现与调试纪律

1. 写出一次作业提交必须包含的最小运行命令。
2. 说明为什么需要记录 Python、PyTorch、CUDA 或 CPU 环境。
3. 给定“公开测试通过、隐藏测试失败”，列出 3 个排查方向。
4. 说明为什么项目报告中不能只给平均延迟。
5. 解释 seed 固定后仍可能不完全复现的原因。

满分证据：

- 能区分代码错误、数据边界、数值容差和环境差异。
- 能说明 P95/P99、错误率、TTFT/TPOT 对服务复现的意义。
- 能把失败日志作为学习证据，而不是只提交成功截图。

## 补救任务

| 低分模块 | 必做任务 | 验收 |
|----------|----------|------|
| Python 基础 | 完成 Ch01 BPE helper 函数前 3 题 | `STUDENT_MODULE=starter .venv/bin/python assignments/ch01_bpe/tests.py` 至少通过 helper tests |
| PyTorch 基础 | 阅读 `math-prerequisites.md` 的 PyTorch 实现纪律，完成 Ch02 embedding shape 题 | 能解释 `[B,T,D]` 到 logits 的路径 |
| 线性代数、概率与统计 | 完成 attention shape 手算、cross entropy 推导和 benchmark variance 解释 | 助教抽查 2 道 shape/统计题 |
| ML Foundations | 完成 [ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md) 的 Diagnostic Add-on 和 Project Evidence Checklist | 能写出 objective、baseline、split、leakage_check、ablation 和 metric_limit |
| 反向传播与数值稳定性 | 完成 CE 梯度、LayerNorm 依赖和 NaN 排查说明 | 提交 1 页推导/调试记录 |
| 复现与调试纪律 | 跑通 `.venv/bin/python verify_course.py` 并解释输出 | 提交命令、环境和失败/通过摘要 |

## 教师使用建议

- 第 1 周前收集诊断结果，只记录模块分数，不把原始答案公开排名。
- 对 `Borderline` 学生安排一次 office hours 检查，重点看 shape、PyTorch loss 和复现命令。
- 诊断题可以作为课堂 quick check 的题库来源。
- 若全班某模块平均低于 70，应在第 1 周增加对应 recap，而不是直接进入作业评分。
- 诊断结果不建议计入总成绩；可计为完成/未完成，避免学生隐藏薄弱点。

## 学生提交模板

```text
姓名：
日期：
Python 基础得分：
PyTorch 基础得分：
线性代数、概率与统计得分：
反向传播与数值稳定性得分：
ML Foundations 得分：
复现与调试纪律得分：

最薄弱模块：
我会完成的补救任务：
我需要助教确认的问题：
```
