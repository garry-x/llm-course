# Pre-Semester Readiness Audit

本文件记录课程在正式发布或开课前的可执行验收证据。它补充 [Course Operations and Improvement Log](course-operations-log.md)、[高校课程质量审计与升级路线](university-course-quality-audit.md)、[External Source Verification Guide](external-source-verification.md)、[CS224N Current Benchmark Snapshot](cs224n-current-benchmark-snapshot.md) 和 [Gradebook and LMS Operations Guide](gradebook-lms-operations.md)。

复核日期：2026-06-05
环境：`.venv` 虚拟环境，PyTorch 已安装
状态：release-candidate

## Audit Scope

| 范围 | 通过标准 | 证据 |
|------|----------|------|
| CS224N current benchmark | 官方页关键 marker 全部匹配，且 manifest 可归档 | `.venv/bin/python scripts/verify_cs224n_snapshot.py` 输出 `status=pass`、`matched_marker_count=38`、`missing_marker_count=0` |
| 课程总门禁 | 课程结构、链接、公式、release builder、作业测试全部通过 | `.venv/bin/python verify_course.py` 输出 `COURSE VERIFY: PASS` |
| 作业公开测试 | 11 个作业 suite 全部通过 reference solution | `ASSIGNMENT TESTS: PASS (11 suite(s))` |
| 学生发布包 | reference solution 和内部评分文档不进入学生站点 | course site release builder 报告 strips inline solutions、excludes instructor-only docs |
| 浏览器渲染 | 首页和 10 章页面可执行 JS，并渲染 KaTeX | browser render smoke: `11 pages`、`397 rendered KaTeX nodes`；release smoke: `11 pages`、`376 KaTeX nodes` |
| 外部来源治理 | 来源分层、frontier claim、CS224N snapshot verifier 和 frontier source verifier 均有门禁 | source governance rows、frontier claims、CS224N snapshot verifier、frontier source evidence verifier 均 PASS |
| Capstone 发布准备 | 推理/训练 capstone 代码可编译，样例验收可运行，并通过 full acceptance | `.venv/bin/python verify_course.py --capstone --training` 输出 inference `ACCEPTANCE: PASS`、training `ACCEPTANCE: PASS` 和 `COURSE VERIFY: PASS` |

## Command Evidence

| Command | Evidence status | Recorded output marker |
|---------|-----------------|------------------------|
| `.venv/bin/python -m py_compile verify_course.py scripts/verify_cs224n_snapshot.py scripts/verify_frontier_sources.py scripts/generate_course_evidence_manifest.py` | PASS | Python 编译无错误 |
| `.venv/bin/python scripts/verify_cs224n_snapshot.py` | PASS | `status: pass`, `expected_marker_count: 38`, `matched_marker_count: 38` |
| `.venv/bin/python scripts/verify_frontier_sources.py --json-out frontier-sources-2026-06-05.json` | PASS | `mode: frontier_source_evidence_verification`, `status: pass`, `passed_check_count: 4` |
| `.venv/bin/python scripts/generate_course_evidence_manifest.py --check` | PASS | `mode: course_evidence_manifest`, `verification_status: pass`, `required_evidence_files: 111`, `required_marker_checks: 63`, no missing required files or markers |
| `.venv/bin/python verify_course.py` | PASS | `COURSE VERIFY: PASS` |
| `.venv/bin/python run_assignment_tests.py` | PASS via verifier | `ASSIGNMENT TESTS: PASS (11 suite(s))` |
| `.venv/bin/python verify_course.py --capstone --training` | PASS | inference `ACCEPTANCE: PASS`; training `ACCEPTANCE: PASS`; SLO `PASS`; `COURSE VERIFY: PASS` |

## Evidence Manifest Scope

| Evidence area | Manifest evidence |
|---------------|-------------------|
| Course document coverage | `required_evidence_files: 111`; all `COURSE_DOCS` `docs/*.md` entries are present in the manifest; `missing_required_files: 0` |
| Marker coverage | `required_marker_checks: 63`; `missing_required_markers: 0` |
| Core teaching packet | `docs/syllabus.md` 12/12 markers; `docs/lecture-plan.md` 9/9; `docs/reading-list.md` 10/10; `docs/written-problem-set.md` 12/12 |
| Instructor and grading packet | `docs/instructor-solution-guide.md` 10/10 markers; `docs/grading-calibration.md` 11/11; `docs/assignment-submission-guide.md` 11/11 |
| Source and breadth evidence | `docs/external-source-inventory.md` 16/16 markers; `docs/classic-nlp-deep-dive-module.md` 16/16 |

## Full Capstone Acceptance Evidence

| Evidence item | Recorded marker |
|---------------|-----------------|
| Inference eval | `pass_rate: 5/5 = 100.0%` |
| Inference SLO | `SLO: PASS` |
| Inference throughput | `tokens_per_second: 299.2739 >= 100.0000` |
| Inference P95 latency | `latency_ms.p95: 306.9216 <= 2000.0000` |
| Inference TTFT | `ttft_ms.p95: 3.1919 <= 800.0000` |
| Inference TPOT | `tpot_ms.p95: 6.5226 <= 40.0000` |
| Capacity plan | `fits_gpu: True`, `max_batch_by_memory: 53`, `cost_per_1m_tokens_usd: 0.1389` |
| Training data audit | `sample_corpus.txt`, `lines: 7`, `duplicate_non_empty_lines: 1` |
| Training plan | `steps: 977`, `gpu_hours: 0.28`, `estimated_cost_usd: 0.42`, `checkpoint_count: 1` |
| Training acceptance | `final_step: 12`, `device: cpu`, `ACCEPTANCE: PASS` |

## Release Safety Evidence

| Release surface | Required invariant | Evidence |
|-----------------|--------------------|----------|
| Student site docs | instructor-only docs excluded | `instructor-solution-guide.md`, `autograder-hidden-tests.md`, `grading-calibration.md`, `grading-anchor-sample-feedback-pack.md`, `private-autograder-operations.md`, `staff-runbook.md` 不进入 student release |
| Assignment packages | `reference_solution.py` excluded | assignment release builder packages 11 student-safe suites |
| Tests in release | default module is `student_solution` | release builder rewrites tests default import |
| Chapter pages | inline reference solutions stripped | course site release builder reports stripped inline solutions |
| Local links | no broken local links in release | course site release builder validates release-local links |

## Known Human Sign-Off Boundaries

| Boundary | Why automatic evidence is insufficient | Required human sign-off |
|----------|----------------------------------------|--------------------------|
| LMS / Gradescope configuration | 仓库只能生成发布包，不能证明真实平台权限、隐藏测试和成绩册字段已配置 | Instructor / Course Manager 保存平台截图或配置导出 |
| School-specific policy | 迟交、复核、可及性和隐私流程依赖学校政策 | Instructor 确认 syllabus 中日期、联系人和处理时限 |
| Real staff roster | 仓库只提供 staff role template | Course Manager 填入真实 staff、Office Hours、联系方式和 escalation owner |
| Hidden tests | 仓库不存储真实隐藏输入 | Head TA 在私有 autograder 环境归档 manifest 和失败类别统计 |
| Live lecture quality | 文档和 demo dry-run 不能证明课堂讲授效果 | 课堂观察、exit ticket 和期中反馈记录 |
| Project report quality | 自动验收只能证明能跑，不能证明研究/工程报告优秀 | rubric 二评、报告样例和复现审查 |

## Pre-Semester Checklist

- Run `.venv/bin/python scripts/verify_cs224n_snapshot.py --json-out cs224n-snapshot-2026-06-05.json` and archive the dated manifest.
- Run `.venv/bin/python scripts/verify_frontier_sources.py --json-out frontier-sources-2026-06-05.json` and archive the dated frontier-source manifest.
- Run `.venv/bin/python scripts/generate_course_evidence_manifest.py --check --json-out course-evidence-2026-06-05.json` and archive the machine-readable evidence manifest.
- Run `.venv/bin/python verify_course.py`.
- Run `.venv/bin/python verify_course.py --capstone --training` before publishing capstone milestones; current readiness run is PASS and must be rerun after project code changes.
- Build a student site release and inspect that instructor-only docs and reference solutions are absent.
- Record LMS/Gradescope, staff roster, Office Hours, accessibility contact, late-day and regrade settings in private course operations records.
- Update [Course Operations and Improvement Log](course-operations-log.md) with command output summaries, not raw private logs.
- If any official source marker changes, update [CS224N Current Benchmark Snapshot](cs224n-current-benchmark-snapshot.md), [CS224N Benchmark Crosswalk](cs224n-benchmark-crosswalk.md), [Frontier Seminar Handout](frontier-seminar-handout.md) and [External Source Inventory](external-source-inventory.md).

## Next Audit Actions

| Priority | Action | Owner | Evidence |
|----------|--------|-------|----------|
| High | Rerun full capstone acceptance after any project code change | Instructor / TA Lead | `.venv/bin/python verify_course.py --capstone --training` output |
| High | Archive machine-readable course evidence before publishing | Instructor / TA Lead | `.venv/bin/python scripts/generate_course_evidence_manifest.py --check --json-out ...` |
| High | Archive private autograder manifest outside the student release | Head TA | `scripts/run_private_autograder.py --public-only --json-out ...` plus hidden-run manifest in private storage |
| Medium | Replace portable staff/support placeholders with institution-specific contacts | Course Manager | syllabus and staff directory sign-off |
| Medium | Add real anonymized course-run statistics after first offering | Instructor | operations log rows for quick checks, assignment failure categories, project reproducibility |
