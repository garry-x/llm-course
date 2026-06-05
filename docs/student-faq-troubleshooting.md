# Student FAQ and Troubleshooting Guide

本指南面向学生，集中回答环境、作业测试、PyTorch、公式阅读、项目复现和评分复核中的常见问题。它补充 [课程 Syllabus](syllabus.md)、[Course Communication and Announcement Policy](course-communication-policy.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md)、[Environment and Reproducibility Guide](environment-reproducibility.md)、[Discussion Section and Office Hours Guide](discussion-office-hours-guide.md)、[Weekly Teaching Reflection and Adjustment Log](weekly-teaching-reflection-adjustment-log.md)、[Course Policies](course-policies.md) 和 [Accessibility and Student Support Guide](accessibility-student-support.md)。

## 使用规则

- 先用本指南定位问题类别，再去讨论区或 Office Hours 提问。
- 提问时提供命令、当前目录、Python/PyTorch 版本、完整 traceback、输入 shape 和已尝试步骤。
- 不要在公开讨论区贴隐藏测试、参考解、其他学生代码或个人敏感信息。
- 如果问题涉及健康、便利安排、迟交、复核升级或个人情况，使用 syllabus 指定的私密渠道。

## 环境与命令

最小自检命令应从仓库根目录运行：

```bash
pwd
.venv/bin/python -c "import sys, torch; print(sys.version.split()[0], torch.__version__, torch.cuda.is_available())"
.venv/bin/python verify_course.py
.venv/bin/python run_assignment_tests.py
```

如果你没有使用根目录 `.venv`，需要在提问或提交日志里写清 Python 路径、PyTorch 版本和安装方式。

| 问题 | 常见原因 | 处理方式 |
|------|----------|----------|
| `.venv/bin/python verify_course.py` 找不到模块 | 没有使用课程虚拟环境或当前目录不对 | 在仓库根目录运行；本机建议使用 `.venv/bin/python verify_course.py` |
| PyTorch import 失败 | 虚拟环境未激活或安装不完整 | 运行 `.venv/bin/python -c "import torch; print(torch.__version__)"` |
| 路径相关错误 | 从子目录运行了根目录脚本，或提交包使用绝对路径 | 回到仓库根目录；代码中使用相对路径或测试传入的路径 |
| 测试很慢 | 使用了大模型、大数据或未限制循环 | 作业测试应使用小输入；不要在公开测试中下载模型或数据 |
| 浏览器公式显示异常 | KaTeX 属性或浏览器缓存问题 | 先刷新页面；若仍异常，报告章节、公式附近文字和浏览器版本 |

## 作业测试

| 现象 | 排查顺序 |
|------|----------|
| 公开测试失败 | 读第一个失败测试名和 assert message；不要先改 tests；用最小输入复现 |
| starter 运行失败 | starter 未完成时失败是正常的；确认失败指向 TODO，而不是 import/path 错误 |
| 本地通过、提交后失败 | 检查 Python/PyTorch 版本、随机 seed、文件名、函数签名和是否依赖本机路径 |
| 公开测试通过、隐藏测试失败 | 检查边界输入、batch/seq_len 变化、dtype/device、数值容差和硬编码公开样例 |
| gradcheck 失败 | 使用 double precision；检查 `eps`、broadcast、mean/variance 依赖和 in-place 操作 |

提交时建议保留：

```text
Command:
Working directory:
Python version:
PyTorch version:
First failing test:
Input shape:
Expected vs actual:
What I tried:
```

## Shape / Mask / Tensor Debugging

| 症状 | 可能原因 | 快速检查 |
|------|----------|----------|
| `matmul` shape mismatch | batch、seq、head 维顺序混乱 | 打印 `q.shape, k.shape, v.shape`；确认最后两维参与矩阵乘法 |
| causal attention 泄露未来 token | mask 方向或应用位置错误 | mask 应在 softmax 前应用到 logits；检查上三角是否被屏蔽 |
| `view` 报错或结果错 | tensor 非 contiguous | `transpose` 后使用 `reshape` 或 `.contiguous().view(...)` |
| loss 是 NaN | logits 过大、学习率过高、mask 全 -inf、除零 | 检查 `torch.isfinite`、lr、mask 后每行是否至少有一个合法 token |
| 训练 tokens/s 突降 | batch 太大、数据加载慢、日志过频、设备拷贝 | 固定 batch，减少打印，检查 CPU/GPU 数据传输 |

## 章节概念 FAQ

| 主题 | 常见误解 | 正确口径 |
|------|----------|----------|
| BPE | 贪心 merge 保证全局最优分词 | BPE 每步最大化当前频率收益，不保证全局最优 |
| Word vectors | 类比关系由训练目标数学保证 | 类比是经验结构，不是训练目标的保证 |
| RoPE | RoPE 是非线性操作 | RoPE 是位置相关线性正交变换；长上下文外推仍受训练分布和数值范围限制 |
| Attention | attention head 可以完整解释模型理由 | attention 可用于诊断，但不能直接等同于模型解释 |
| MLA | latent cache 让注意力免费 | MLA 降低 KV cache，但仍有投影、RoPE 分支和注意力计算 |
| PPL | perplexity 低等于事实正确 | PPL 衡量 next-token 概率，不直接衡量事实性 |
| RAG | 检索命中相似文档就保证答案正确 | 还要检查 chunking、rerank、prompt assembly 和 generation |
| Structured output | 模型承诺 JSON 就不用校验 | 应使用结构化输出/约束解码，并在应用侧做 schema 校验 |

## Capstone Troubleshooting

| 项目 | 常见问题 | 处理方式 |
|------|----------|----------|
| Training capstone | resume 后 step 不对 | 检查 checkpoint 是否保存 model、optimizer、scheduler、step 和 best metric |
| Training capstone | loss spike / NaN | 降低 lr，检查 grad norm、batch、数据异常、mask 和 dtype |
| Training capstone | 报告只有成功曲线 | 至少加入 3 个失败案例和排查记录 |
| Inference capstone | health 通过但 eval 失败 | 固定评测集，逐条看 prompt、expected behavior 和返回 JSON |
| Inference capstone | SLO 失败 | 区分 error_rate、TTFT、TPOT、P95 latency 和 tokens/s 哪一项失败 |
| Inference capstone | RAG 答案错 | 分别检查 chunking、embedding、retrieval、reranking、prompt assembly 和 generation |

## Office Hours 提问模板

```text
Course item:
Goal:
Command:
Working directory:
Environment:
Input shape or sample:
Expected behavior:
Actual output / traceback:
Smallest reproduction:
What I already tried:
Question for staff:
```

高质量问题应能让助教在 2-5 分钟内复现或定位。只贴“跑不通”通常无法有效排查。

## 评分与复核

| 问题 | 答案 |
|------|------|
| 公开测试全过为什么不是满分？ | 正式评分还包括隐藏边界测试、隐藏性质测试、书面解释、错误分析和代码质量。 |
| 能否提交修改后的代码作为复核依据？ | 不能。复核基于原始提交；修改后代码可作为学习记录，但不是原始评分依据。 |
| 隐藏测试失败能否要求公开输入？ | 不公开隐藏输入。课程组应提供类别级反馈和 rubric 映射。 |
| AI 工具能否用于 debug？ | 可以辅助理解和定位，但最终代码、推导和报告必须能独立解释，并按政策披露。 |
| 遇到个人困难怎么办？ | 使用私密渠道联系课程组；不要在公开讨论区披露个人敏感信息。 |

## 发布前 Checklist

- 本指南链接到 syllabus、staff runbook 或 course operations log。
- 常见问题来自公开测试、Office Hours、讨论课和复核记录的聚合，不泄露学生个人信息。
- 每个 FAQ 回答都指向可执行动作，而不是只给抽象建议。
- 新增高频问题后同步更新 [Course Operations and Improvement Log](course-operations-log.md)。
