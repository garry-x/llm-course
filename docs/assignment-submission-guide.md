# Assignment Submission and Release Guide

本指南用于把章节作业从“本地可跑测试”整理成正式课程可发布、可提交、可批改、可复核的流程。它补充 `assignments/ch*/README.md`、[Assignment Handout Pack](assignment-handout-pack.md)、[Programming Assignment Code Quality Rubric](programming-assignment-code-quality-rubric.md)、[Autograder 与隐藏测试设计指南](autograder-hidden-tests.md)、[Environment and Reproducibility Guide](environment-reproducibility.md)、[Grading Calibration Guide](grading-calibration.md)、[Gradebook and LMS Operations Guide](gradebook-lms-operations.md)、[Staff Assistance and Code Review Boundary Policy](staff-assistance-code-review-policy.md) 和 [Academic Integrity Case Process](academic-integrity-case-process.md)。

## 发布前 Checklist

每次发布作业前，教师或助教必须检查：

| 检查项 | 通过标准 |
|--------|----------|
| handout | 作业 README 写清目标、文件说明、运行方式、评分 Rubric |
| starter | `starter.py` 只包含学生需要实现的 TODO，不泄露 reference |
| public tests | `tests.py` 可在 CPU 上运行，并能加载 `STUDENT_MODULE=starter` |
| reference | `reference_solution.py` 通过公开测试，用于验证测试本身 |
| hidden tests | 隐藏测试类别映射到 rubric，不发布源码和精确输入 |
| environment | 写清 Python/PyTorch/NumPy 版本范围和运行命令 |
| integrity | 禁止网络访问、读取 reference、修改 tests 或硬编码公开样例 |
| integrity review | 相似性检测、AI 披露争议和 suspected hidden test leakage 有私密个案流程 |
| release note | 写清发布时间、截止时间、late day 规则、复核窗口 |

发布前至少运行。若仓库根目录已有 `.venv`，优先使用 `.venv/bin/python`，这样教师、助教和学生的 PyTorch 版本更容易对齐：

```bash
.venv/bin/python -c "import sys, torch; print(sys.version.split()[0], torch.__version__)"
.venv/bin/python verify_course.py
.venv/bin/python run_assignment_tests.py
```

涉及训练、推理或 capstone 的作业还应运行：

```bash
.venv/bin/python verify_course.py --capstone --training
```

## 学生提交包

编程作业建议提交以下文件：

| 文件 | 要求 |
|------|------|
| `student_solution.py` 或 LMS 指定代码文件 | 保持 starter API，不改函数签名 |
| `run_log.txt` | 公开测试命令和输出摘要 |
| `error_analysis.md` | 至少 1 个失败、边界或调试案例；若全部通过，也写一个潜在边界 |
| `honor_statement.txt` | 协作、AI 工具和外部资源披露 |
| `written_answers.pdf` 或 `.md` | 对应书面题、shape、复杂度、引用 |

不允许提交：

- 修改后的 `tests.py` 作为评分依据。
- `reference_solution.py` 或从参考答案复制的代码。
- 大型二进制文件、模型 checkpoint 或数据集，除非作业明确要求。
- 依赖本机绝对路径、网络下载或隐藏环境变量的代码。

若出现 suspected plagiarism、similarity report 高风险命中、AI 工具披露不一致、`reference_solution.py` 接触或 hidden tests 泄漏线索，课程组按 [Academic Integrity Case Process](academic-integrity-case-process.md) 私密复核，不在公开讨论区处理。

学生寻求 office hours 或 forum 帮助时，应按 [Staff Assistance and Code Review Boundary Policy](staff-assistance-code-review-policy.md) 提供命令、first failure、expected shape、minimal reproduction 和 attempted fix。Ch01-Ch02 可获得有限局部代码查看；Ch03-Ch11 默认不审阅完整可提交实现。

## 学生发布包构建

仓库中的 `reference_solution.py` 只供教师、助教和自学者验证测试本身。正式发布到 LMS/Gradescope 时，应使用学生版发布包，不应直接上传完整 `assignments/ch*/` 目录。

构建单个作业发布包：

```bash
.venv/bin/python scripts/build_assignment_release.py ch03_attention --out /tmp/assignment-release
```

构建全部 11 个作业发布包：

```bash
.venv/bin/python scripts/build_assignment_release.py --all --out /tmp/assignment-release
```

发布包只包含：

| 文件 | 用途 |
|------|------|
| `README.md` | 学生 handout、运行方式和评分 rubric |
| `starter.py` | 学生起始代码 |
| `tests.py` | public tests，默认加载 `student_solution` |
| `RELEASE_MANIFEST.json` | 发布包包含/排除文件和默认模块记录 |

发布包必须排除：

- `reference_solution.py`
- `__pycache__/`
- 隐藏测试源码、隐藏输入和教师评分脚本
- 其他学生提交、助教批改记录或 LMS 私有配置

发布前检查：

```bash
.venv/bin/python scripts/build_assignment_release.py --all --dry-run
.venv/bin/python verify_course.py
```

如果需要把 `tests.py` 上传到 Gradescope public tests，确认默认模块是 `student_solution`；教师本地验证 reference 时仍使用仓库原始作业目录。

## 学生站点发布包构建

仓库根目录的 HTML 章节是自学版材料，包含可折叠的编程练习参考解答。正式开课时，如果这些章节作为学生站点发布，应使用学生站点发布包，避免把参考解答随页面源码一起发布。

构建学生站点：

```bash
.venv/bin/python scripts/build_course_site_release.py --out /tmp/course-site-release
```

预览发布清单：

```bash
.venv/bin/python scripts/build_course_site_release.py --out /tmp/course-site-release --dry-run
```

学生站点发布包包含：

| 路径 | 用途 |
|------|------|
| `index.html` | 课程首页 |
| `chapters/` | 已剥离 `solution-toggle` 和 `.solution` 参考解答块的章节 HTML |
| `css/`, `js/`, `images/` | 前端运行资源 |
| `docs/` | 学生安全的 syllabus、reading、policy、source audit、project 和 review 材料 |
| `SITE_RELEASE_MANIFEST.json` | 站点发布模式、包含/排除文档和章节剥离统计 |

学生站点发布包必须排除：

- 章节内 `<button class="solution-toggle">` 与 `<div class="solution">` 参考解答块
- `docs/instructor-solution-guide.md`
- `docs/autograder-hidden-tests.md`
- `docs/grading-calibration.md`
- `docs/grading-anchor-sample-feedback-pack.md`
- `docs/private-autograder-operations.md`
- `docs/staff-runbook.md`
- 其他隐藏测试、教师批改记录、staff runbook、lecture-only notes 或私有评分脚本

## LMS / Gradescope 配置

若使用 Gradescope 或类似 LMS，建议配置：

| 项 | 建议 |
|----|------|
| autograder image | 固定 Python、PyTorch、NumPy 版本；默认 CPU |
| entrypoint | 复制学生文件后设置 `STUDENT_MODULE=student_solution` 运行 tests |
| timeout | 简单作业 60-120 秒；训练类作业使用小样例和较长 timeout |
| output | 显示公开测试摘要、失败测试名、seed、rubric 项，不显示隐藏输入 |
| score split | 公开测试、隐藏边界、隐藏性质、书面解释分开计分 |
| regrade window | 成绩发布后 7 天内，按 syllabus 复核政策执行 |

最小 autograder 流程：

```text
1. 安装依赖。
2. 复制学生提交文件。
3. 禁止网络或忽略网络权限。
4. 设置 STUDENT_MODULE。
5. 运行公开测试和隐藏测试；教师内部流程可使用 `scripts/run_private_autograder.py` 生成 manifest。
6. 汇总分数、失败项、seed、rubric 映射和 `release_batch`。
```

## 运行命令规范

学生本地运行：

```bash
cd assignments/chXX_name
cp starter.py student_solution.py
STUDENT_MODULE=student_solution ../../.venv/bin/python tests.py
```

教师验证参考实现：

```bash
.venv/bin/python assignments/chXX_name/tests.py
```

教师验证 starter 行为：

```bash
cd assignments/chXX_name
STUDENT_MODULE=starter ../../.venv/bin/python tests.py
```

注意：starter 未完成时失败是正常的；发布前要确认失败信息指向 TODO 或待实现 API，而不是 import、路径或环境错误。

## 成绩发布说明模板

```text
作业：
发布时间：
截止时间：
公开测试权重：
隐藏测试权重：
书面解释/代码质量权重：
late day 规则：
复核截止时间：
运行环境：
本次常见失败：
```

成绩发布时至少给学生：

- 总分和分项分。
- 公开测试失败摘要。
- 隐藏测试类别级反馈，不泄露隐藏输入。
- 书面解释或代码质量扣分原因。
- 复核请求方式和截止时间。

成绩册字段、`release_batch`、`rubric_version`、late-day ledger、weighted gradebook 和 LMS 导出审计按 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md) 执行。成绩发布前应确认权重复算、late-day 消耗和 regrade window 与 syllabus 和 deadline ledger 一致。

## 复核材料

学生提交复核请求时必须提供：

| 材料 | 说明 |
|------|------|
| 具体 rubric 项 | 不能只写“我觉得分低” |
| 原始提交文件 | 不接受修改后代码作为复核依据 |
| 本地运行命令和输出 | 用于定位环境或测试差异 |
| 复核理由 | 指出评分、测试或人工判断哪里可能有误 |
| 引用或推导证据 | 书面题需给出公式、来源或 shape 说明 |

复核处理规则：

- 助教先检查是否属于运行环境、测试误判、隐藏边界或人工评分争议。
- 若复核暴露 rubric 含糊，应同步更新 [Grading Calibration Guide](grading-calibration.md)。
- 若复核暴露隐藏测试问题，应修复测试并重新评估受影响学生。
- 复核可能上调或下调分数。
- 复核状态、`regrade_decision_id`、批量修正范围和学生可见决定说明按 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md) 记录。

## 发布后复盘

每次作业结束后，助教应记录：

| 字段 | 内容 |
|------|------|
| 作业名 | 例如 Ch03 Attention |
| 提交人数 | 用于估计失败率 |
| 公开测试通过率 | 典型路径掌握情况 |
| 隐藏测试失败 Top 3 | 边界和性质缺口 |
| 书面题常见误解 | 下次 lecture recap 或 office hours 主题 |
| 需要改进的测试 | 漏测、误判、耗时或反馈不清 |
| 需要改进的 handout | 题意、运行命令、rubric 或示例 |

这些记录应反馈到 [Course Outcome Map](course-outcome-map.md)、[Grading Calibration Guide](grading-calibration.md) 和 [Autograder 与隐藏测试设计指南](autograder-hidden-tests.md)。
