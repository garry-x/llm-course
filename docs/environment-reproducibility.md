# Environment and Reproducibility Guide

本指南规定课程本地环境、依赖版本、CPU/GPU fallback 和验收命令的记录方式。它补充 [Student FAQ and Troubleshooting Guide](student-faq-troubleshooting.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md)、[Compute Resource and Cost Guide](compute-resource-guide.md)、[Dataset, Model, and Artifact Provenance Registry](dataset-model-artifact-registry.md) 和 [Course Materials Index](course-materials-index.md)。

## 本仓库当前验证环境

| 项 | 当前值 | 说明 |
|----|--------|------|
| Python | 3.12.3 | 由 `.venv/bin/python` 实测 |
| PyTorch | 2.12.0+cu130 | 由 `.venv/bin/python -c "import torch; print(torch.__version__)"` 实测 |
| CUDA 可用性 | True | 当前机器可用；正式必交作业仍必须有 CPU fallback |
| 验证日期 | 2026-06-05 | 每次课程发布前应重新运行 smoke test |

本表不是要求所有学生必须使用完全相同版本；它是课程团队发布材料时的实测基线。学生或助教若使用不同 Python/PyTorch 版本，需要在 `run_log.txt` 或复核请求中写明版本。

## 推荐本地命令

所有命令默认从仓库根目录运行：

```bash
.venv/bin/python -c "import sys, torch; print(sys.version.split()[0], torch.__version__, torch.cuda.is_available())"
.venv/bin/python verify_course.py
.venv/bin/python run_assignment_tests.py
.venv/bin/python verify_course.py --capstone --training
```

若已经激活等价虚拟环境，可以把 `.venv/bin/python` 替换为 `python`，但提交日志必须记录实际解释器路径：

```bash
python -c "import sys; print(sys.executable)"
```

## 依赖版本策略

| 依赖 | 课程用途 | 推荐策略 |
|------|----------|----------|
| PyTorch | Ch02-Ch10 作业、训练 capstone、张量/梯度测试 | 优先使用已安装 `.venv`；重新安装时按 PyTorch 官网选择 CPU/CUDA wheel |
| NumPy | Ch10 inference/RAG/benchmark 辅助 | 使用 `requirements.txt` 中的最低版本或更高兼容版本 |
| tqdm | 训练/项目日志 | 非核心依赖，缺失时不应影响基础作业 |
| transformers | 阅读和扩展实验 | 不作为必交作业的联网或大模型依赖 |

`requirements.txt` 使用兼容下限而非完整 lockfile，是为了允许 CPU-only、CUDA、macOS 和课程服务器环境共存。正式 LMS/autograder 若需要完全一致环境，应在平台镜像中固定 Python、PyTorch、NumPy 和 CUDA 版本，并把镜像摘要记录到 [Course Operations and Improvement Log](course-operations-log.md)。

## CPU/GPU 边界

- Ch01-Ch11 公开作业测试必须能在 CPU 上运行。
- `verify_course.py`、`run_assignment_tests.py` 和两个 capstone acceptance 是发布前最低门槛。
- CUDA 可用于加速训练 capstone 扩展，但不能成为必交作业唯一通过路径。
- GPU/API 实验报告必须提供 CPU 或小配置 fallback，并说明哪些结论来自扩展资源。

## 提交日志模板

学生提交 `run_log.txt` 时建议包含：

```text
Command:
Working directory:
Python executable:
Python version:
PyTorch version:
CUDA available:
Device used:
First failing test, if any:
```

## 发布前 Checklist

| 检查项 | 通过标准 |
|--------|----------|
| smoke test | `.venv/bin/python -c "import sys, torch; ..."` 成功 |
| 基础验收 | `.venv/bin/python verify_course.py` 成功 |
| 作业验收 | `.venv/bin/python run_assignment_tests.py` 成功或由 `verify_course.py` 触发成功 |
| capstone 验收 | `.venv/bin/python verify_course.py --capstone --training` 成功 |
| CPU fallback | 必交项不依赖 CUDA；CUDA 结果只作为扩展或加速 |
| 版本记录 | README、FAQ、submission guide 和 operations log 的命令口径一致 |
