# Private Autograder Operations Guide

本指南把 [Autograder 与隐藏测试设计指南](autograder-hidden-tests.md) 落实为可运行的教师内部流程。它补充 [Assignment Submission and Release Guide](assignment-submission-guide.md)、[Assignment Handout Pack](assignment-handout-pack.md)、[Grading Anchor Sample Feedback Pack](grading-anchor-sample-feedback-pack.md)、[Gradebook and LMS Operations Guide](gradebook-lms-operations.md)、[Academic Integrity Case Process](academic-integrity-case-process.md) 和 `scripts/run_private_autograder.py`。

本文件面向教师、Head TA 和 autograder 管理员。真实 hidden tests 不应提交到本仓库，也不应进入学生站点或作业 release 包。

## Directory Boundary

| 路径 | 状态 | 说明 |
|------|------|------|
| `assignments/ch*/tests.py` | public | 学生可见公开测试，验证核心 API 和典型路径 |
| `assignments/ch*/reference_solution.py` | instructor-only | 仅用于教师验证公开测试和评分口径，不进学生 release |
| `private_autograder/hidden_tests/ch*/tests.py` | instructor-only external | 真实 hidden boundary/property tests；默认不在仓库中保存 |
| `dist/assignments/ch*/` | student release | 由 `scripts/build_assignment_release.py` 生成，只含 README、starter、public tests 和 manifest |
| `private_autograder/reports/` | instructor-only external | autograder JSON manifest、失败日志和复核证据 |

若学校要求把 hidden tests 放在 Gradescope、LMS 容器镜像或私有仓库中，`private_autograder/hidden_tests/` 只是本地挂载点约定；不要把该目录加入学生发布包。

## Runbook

### 1. 构建学生 release 包

```bash
.venv/bin/python scripts/build_assignment_release.py --all --out dist/assignments
```

检查每个 `RELEASE_MANIFEST.json`：

- `included` 只包含 `README.md`、`starter.py`、`tests.py`。
- `excluded` 包含 `reference_solution.py`。
- release 后的 `tests.py` 默认导入 `student_solution`。

### 2. 用参考实现做公开测试 dry run

```bash
.venv/bin/python scripts/run_private_autograder.py --public-only --json-out private_autograder/reports/public-dry-run.json
```

dry run 必须在所有 11 个 assignment 上通过。若公开测试对 reference 失败，先修复 public tests 或 reference solution；不要把失败归因给学生。

### 3. 挂载真实 hidden tests

真实开课时，按以下结构从 LMS 镜像、私有仓库或加密存储挂载：

```text
private_autograder/
  hidden_tests/
    ch01_bpe/tests.py
    ch02_embeddings/tests.py
    ...
    ch11_classic_nlp/tests.py
  reports/
```

hidden tests 必须调用学生公开 API，不依赖私有变量名，除非 handout 明确要求。每个 hidden test 文件应按类别组织：

- `hidden_boundary_tests`
- `hidden_property_tests`
- `hardcoding_and_integrity_checks`
- `performance_or_timeout_checks`

### 4. 运行正式 private autograder

```bash
.venv/bin/python scripts/run_private_autograder.py \
  --student-module student_solution \
  --hidden-dir private_autograder/hidden_tests \
  --json-out private_autograder/reports/chXX-release_batch.json
```

正式 LMS/Gradescope entrypoint 应先复制学生提交到作业目录，再设置 `STUDENT_MODULE=student_solution`。如果平台使用容器隔离，应禁用网络、限制运行时间，并只挂载当前作业目录和 hidden tests 只读目录。

## Manifest Schema

`scripts/run_private_autograder.py` 输出 JSON manifest，至少包含：

| field | 要求 |
|-------|------|
| `mode` | `private_autograder_public_dry_run` 或 `private_autograder` |
| `student_module` | `reference_solution`、`student_solution` 或 LMS 注入模块 |
| `hidden_dir` | instructor-only hidden tests 根目录 |
| `hidden_tests_stored_in_repo` | 必须为 `False` |
| `student_release_excludes` | 必须包含 `reference_solution.py`、`private_autograder/` 和 `hidden_tests/` |
| `assignments[].assignment_id` | `ch01_bpe` 到 `ch11_classic_nlp` |
| `assignments[].public_tests.status` | `pass` / `fail` |
| `assignments[].hidden_tests.status` | `pass` / `fail` / `not_configured` / `skipped_public_only` |
| `assignments[].manual_review_required` | written、run_log、honor_statement、code_quality_and_hardcoding |
| `assignments[].rubric_channels` | public、hidden boundary、hidden property、written/code quality |
| `summary.pass_count` | 通过 assignment 数 |
| `summary.fail_count` | 失败 assignment 数 |

manifest 可进入 LMS 私有附件或 staff drive；学生只看到类别级反馈，不看到 hidden input、seed 组合、完整 expected output 或 hidden test source。

## Rubric Mapping

| rubric channel | 证据 | 学生可见反馈 |
|----------------|------|--------------|
| `public_unit_tests` | `assignments/ch*/tests.py` stdout/stderr | 失败测试名、公开输入和本地复现命令 |
| `hidden_boundary_tests` | 私有边界输入、shape、dtype、非法参数 | 类别级反馈，例如 “4D mask broadcast failed” |
| `hidden_property_tests` | 数学不变量、随机 seed、统计性质 | 性质级反馈，例如 “probabilities did not renormalize after filtering” |
| `written_explanation_code_quality` | `written_answers.md`、`run_log.txt`、人工代码审查 | 具体 rubric 项和下一步修改建议 |
| `hardcoding_and_integrity_checks` | 文件读取、网络访问、公开样例硬编码、相似性报告 | 只给政策和类别说明，按 integrity case 流程处理 |

分数发布前，Head TA 应把 manifest 中的 `rubric_channels` 映射到 [Assignment Handout Pack](assignment-handout-pack.md) 的作业权重和 [Grading Anchor Sample Feedback Pack](grading-anchor-sample-feedback-pack.md) 的 anchor sample。

## Failure Log Contract

隐藏测试失败日志必须保留给 staff，但学生只看类别级摘要。

```text
assignment_id:
release_batch:
rubric_item:
hidden_category:
seed:
shape:
dtype:
device:
expected_property:
observed_summary:
student_visible_feedback:
manual_review_required:
```

禁止在学生可见反馈中写入：

- hidden test exact input
- 完整 expected output
- private test source line number
- `reference_solution.py` 片段
- 其他学生提交内容

## LMS And Gradescope Entrypoint

最小 entrypoint：

```bash
set -euo pipefail
cp /submission/student_solution.py assignments/chXX_name/student_solution.py
cd /course
.venv/bin/python scripts/run_private_autograder.py \
  --chapter chXX_name \
  --student-module student_solution \
  --hidden-dir /mnt/private_hidden_tests \
  --json-out /mnt/private_reports/chXX_name-${SUBMISSION_ID}.json
```

运行环境要求：

| 项 | 要求 |
|----|------|
| Python/PyTorch | 与 [Environment and Reproducibility Guide](environment-reproducibility.md) 一致 |
| network | 默认关闭；RAG/API 项目另用 mock 或受控服务 |
| timeout | 简单作业 60-120 秒，训练/推理项目另设 acceptance timeout |
| filesystem | 学生只能写工作目录和临时目录，hidden tests 只读 |
| secrets | 不把 API key、参考答案或 hidden path 暴露给学生日志 |
| output | stdout/stderr 截断，manifest 私有保存 |

## Integrity Checks

每次正式批改至少启用以下检查：

- 学生提交不得读取 `reference_solution.py`、hidden tests 路径或 `tests.py` 源码。
- 学生提交不得访问网络，除非作业明确允许且使用 mock endpoint。
- 学生提交不得根据公开测试字符串、文件名或 seed 硬编码输出。
- 高分但 written explanation 薄弱的提交进入人工复核。
- 相似性报告只用于排序复核优先级，不能单独证明违规。

涉及诚信争议时，冻结原始提交和 manifest，按 [Academic Integrity Case Process](academic-integrity-case-process.md) 处理；不要在 autograder 日志里写无关个人信息。

## Regrade And Batch Correction

若发现 hidden test bug、容差不合理、rubric ambiguity 或平台配置错误：

1. 冻结受影响 `release_batch`。
2. 保存原 manifest、修正后 manifest 和差异说明。
3. 记录 `regrade_decision_id`。
4. 对所有受影响学生批量重跑，不只处理提出复核的学生。
5. 学生可见说明只写测试类别、影响范围和分数动作。
6. 同步更新 [Grading Calibration Guide](grading-calibration.md)、[Grading Anchor Sample Feedback Pack](grading-anchor-sample-feedback-pack.md) 或 [Autograder 与隐藏测试设计指南](autograder-hidden-tests.md)。

## Release Checklist

| 检查项 | 通过标准 |
|--------|----------|
| public dry run | `.venv/bin/python scripts/run_private_autograder.py --public-only` 通过 11 个 assignment |
| hidden path external | `private_autograder/hidden_tests/` 不进入 git、不进入 student release、不出现在学生日志 |
| reference excluded | `scripts/build_assignment_release.py` 生成的 release 不含 `reference_solution.py` |
| manifest archived | 每个 release_batch 有 JSON manifest、rubric_version 和 staff-only 保存位置 |
| feedback safe | 学生反馈不含 hidden exact input、expected output、reference snippet 或其他学生内容 |
| gradebook linked | 分数、late day、复核和批量修正按 `gradebook-lms-operations.md` 记录 |
