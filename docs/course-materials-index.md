# Course Materials Index

本索引用于集中管理每讲的章节、阅读、代码 demo、作业、讨论课和发布状态。它补充 [10 周 / 20 讲 Lecture Plan](lecture-plan.md)、[Weekly Teaching Reflection and Adjustment Log](weekly-teaching-reflection-adjustment-log.md)、[Lecture Slide Outline](lecture-slide-outline.md)、[Lecture Slide Sample Pack](lecture-slide-sample-pack.md)、[Lecture Notes Index](lecture-notes-index.md)、[Lecture Notes Quality and Review Standard](lecture-notes-quality-review.md)、[Board Derivation and Instructor Notes Pack](board-derivation-pack.md)、[Classroom Demo Runbook](demo-runbook.md)、[逐周阅读清单与复盘 Handout](reading-list.md)、[Concept Mastery and Misconception Map](concept-misconception-map.md)、[Recitation Worksheet Pack](recitation-worksheet-pack.md)、[Material Versioning and Archive Policy](material-versioning-archive-policy.md)、[Frontier Seminar Handout](frontier-seminar-handout.md)、[Assignment Handout Pack](assignment-handout-pack.md)、[Assignment Submission and Release Guide](assignment-submission-guide.md)、[Default Final Project Guide](default-final-project-guide.md)、[Project Report Template and Reproducibility Checklist](project-report-template.md)、[Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md)、[Environment and Reproducibility Guide](environment-reproducibility.md)、[Compute Resource and Cost Guide](compute-resource-guide.md)、[Course Staff Runbook](staff-runbook.md) 和 [Accessibility and Student Support Guide](accessibility-student-support.md)。

## 使用规则

- 每次开课前，课程经理应检查本索引中的章节、阅读、作业和项目入口是否仍有效。
- 每次修改章节、作业、阅读或项目后，应更新“版本记录”并运行 `.venv/bin/python verify_course.py`；旧材料、往届样例和 retired 项按 [Material Versioning and Archive Policy](material-versioning-archive-policy.md) 标注，不得作为本轮评分依据。
- 若某讲的 slides、录屏或外部 notebook 尚未准备好，应标为 `planned`，不要假装已发布。
- 正式学生站点应由 `scripts/build_course_site_release.py` 构建，避免发布章节内嵌参考解答；正式作业包应由 `scripts/build_assignment_release.py` 构建，避免发布 `reference_solution.py`。
- 本索引不替代 lecture plan、slide outline、lecture notes index、lecture notes quality review、board derivation pack、concept misconception map 或 demo runbook；lecture plan 说明如何授课，slide outline 说明课件如何组织，lecture notes index 说明每讲 notes、板书推导和复盘证据，lecture notes quality review 说明每讲 notes 的审稿字段和更正流程，board derivation pack 提供可直接讲授的核心推导脚本，concept misconception map 说明概念掌握、常见误区和补救路径，demo runbook 说明课堂演示如何复现，本索引说明材料在哪里、何时发布、如何验证。

## 发布状态

| 状态 | 含义 |
|------|------|
| ready | 材料已可发布，链接有效，已纳入验证 |
| draft | 内容可内部使用，但还需教师审查 |
| planned | 计划加入，但本轮不作为正式交付 |
| retired | 已停用，不能作为作业或考试依据 |

## 20 讲材料索引

| 讲次 | 主题 | 章节/讲义 | 阅读 | Demo / 代码 | 作业或证据 | 状态 |
|------|------|-----------|------|-------------|------------|------|
| L1 | 课程导论、PyTorch、BPE | Ch01; [math-prerequisites.md](math-prerequisites.md) | Week 1 reading | `assignments/ch01_bpe/tests.py` | Ch01 starter + reading recap | ready |
| L2 | Embedding、Word Vectors、RoPE | Ch02 | Week 1 reading | Ch02 embedding/RoPE tests | Ch02 starter + RoPE written problem | ready |
| L3 | Scaled Dot-Product Attention | Ch03 | Week 2 reading | Ch03 attention tests | Ch03 starter | ready |
| L4 | Causal Mask、Backprop、Dependency Parsing 预告 | Ch03; [classic-nlp-handout.md](classic-nlp-handout.md) | Week 2 reading | causal mask failure demo | Ch03 written problem | ready |
| L5 | MHA 与 GQA | Ch04 | Week 3 reading | MHA/GQA shape and cache tests | Ch04 starter | ready |
| L6 | MLA、Norm、FFN、Block | Ch04-Ch05 | Week 3 reading | block grad flow tests | Ch05 starter | ready |
| L7 | GPT Model Assembly | Ch06 | Week 4 reading | GPT parameter audit tests | Ch06 starter | ready |
| L8 | MoE、Routing、参数/显存审计 | Ch06 | Week 4 reading | MoE router tests | Ch06 written problem | ready |
| L9 | Dataset、CE、Optimizer、Scheduler | Ch07 | Week 5 reading | Ch07 dataloader/CE tests | Ch07 starter | ready |
| L10 | Training Loop、Checkpoint、Scaling | Ch07; training capstone README | Week 5 reading | training capstone acceptance | training proposal | ready |
| L11 | Generation、Sampling、Degeneration | Ch08 | Week 6 reading | top-k/top-p tests | Ch08 starter | ready |
| L12 | Speculative Decoding、Constraints、MTP | Ch08 | Week 6 reading | speculative decoding tests | Ch08 written problem | ready |
| L13 | SFT、LoRA | Ch09 | Week 7 reading | LoRA/SFT tests | Ch09 starter | ready |
| L14 | DPO、GRPO、Alignment 边界 | Ch09 | Week 7 reading | DPO/GRPO tests | Ch09 written problem | ready |
| L15 | Classic NLP、BERT、Evaluation | [classic-nlp-handout.md](classic-nlp-handout.md); [classic-nlp-deep-dive-module.md](classic-nlp-deep-dive-module.md); [nlp-evaluation-coverage.md](nlp-evaluation-coverage.md) | Week 8 reading | `assignments/ch11_classic_nlp/tests.py` | Ch11 supplement | ready |
| L16 | Ethics、Safety、Data Review | [data-ethics-review.md](data-ethics-review.md); [frontier-seminar-handout.md](frontier-seminar-handout.md) | Week 8 reading | project data review walk-through | data/ethics review + social impact seminar | ready |
| L17 | KV Cache、Quantization、RAG | Ch10 | Week 9 reading | KV/RAG tests | Ch10 starter | ready |
| L18 | Serving、Benchmark、SLO、Capacity | Ch10; inference capstone README | Week 9 reading | inference capstone benchmark/SLO | inference proposal | ready |
| L19 | Capstone Reproducibility Rehearsal | capstone READMEs; [default-final-project-guide.md](default-final-project-guide.md); [project-report-template.md](project-report-template.md); rubrics | Week 10 reading | acceptance dry run | project draft + peer review | ready |
| L20 | Final Presentation and Course Review | presentation rubric; operations log; [frontier-seminar-handout.md](frontier-seminar-handout.md) | Week 10 reading | final report checklist | final report + presentation + open questions seminar | ready |

## Demo 与代码发布规则

每个课堂 demo 应满足：

- 能在 CPU 或明确说明的硬件上运行。
- 记录运行命令、预期输出和常见失败。
- 不依赖私有路径、隐藏环境变量或网络下载。
- 不泄露 reference solution、隐藏测试或学生提交。
- 若发布完整网页站点给正式课程学生，使用 `scripts/build_course_site_release.py --out <dir>`，并检查 `SITE_RELEASE_MANIFEST.json`。
- 与至少一个章节、作业测试或 capstone 验收对应。

如果 demo 只适合教师现场演示，应在 lecture plan 中标注为 board work 或 instructor-only，不应作为学生必交材料。

## Slides / Notes / Recording 规则

直播、录播、公开历史视频、字幕、文字稿、demo 录屏和课堂照片的访问边界按 [Lecture Media Access Policy](lecture-media-access-policy.md) 执行。

本仓库当前以 HTML 章节、Markdown handout 和作业测试作为主讲义。若教师后续加入 slides、录屏或 notebook，应遵守：

| 材料 | 发布要求 |
|------|----------|
| slides | 标明对应讲次、章节、发布日期和最后更新时间 |
| lecture notes | 链接到章节或 handout，公式符号与正文一致，并按 [Lecture Notes Quality and Review Standard](lecture-notes-quality-review.md) 保留 review record |
| recording | 若用于正式评分，应提供字幕、文字摘要或替代材料 |
| notebook | 固定依赖版本，不下载私有数据，不覆盖学生文件 |
| demo script | 包含运行命令、预期输出和失败排查 |

## 版本记录

| 日期 | 材料 | 改动 | 验证 |
|------|------|------|------|
| 2026-06-04 | course materials index | 新增 20 讲材料索引、发布状态和 demo 规则 | `.venv/bin/python verify_course.py` |
| 2026-06-04 | lecture slide outline | 新增 20 讲 slide deck 大纲和发布前 checklist | `.venv/bin/python verify_course.py` |
| 2026-06-04 | lecture notes index | 新增 20 讲 notes、板书推导、复盘问题和证据索引 | `.venv/bin/python verify_course.py` |
| 2026-06-05 | lecture notes quality review | 新增 notes 审稿 rubric、per-lecture checklist、review record、correction workflow 和 evidence matrix | `.venv/bin/python verify_course.py` |
| 2026-06-04 | classroom demo runbook | 新增 20 讲 demo 命令、预期输出和失败排查 | `.venv/bin/python verify_course.py` |
| 2026-06-04 | compute resource guide | 新增 CPU baseline、GPU/API 额度、公平使用、成本记录和降级路径 | `.venv/bin/python verify_course.py` |
| 2026-06-05 | board derivation pack | 新增 12 个核心板书推导脚本、20 讲 quick check 和评分衔接 | `.venv/bin/python verify_course.py` |
| 2026-06-05 | default final project guide | 新增默认 GPT-2 风格最终项目、三个下游任务、proposal/milestone/poster/report 交付路径 | `.venv/bin/python verify_course.py` |
| 2026-06-05 | assignment handout pack | 新增 11 个作业的 written/programming 双轨 handout 摘要和隐藏测试边界 | `.venv/bin/python verify_course.py` |
| 2026-06-05 | environment reproducibility guide | 新增 `.venv`、PyTorch smoke test、CPU/GPU fallback 和提交日志模板 | `.venv/bin/python verify_course.py` |
| 2026-06-05 | frontier seminar handout | 新增 interpretability、多模态、社会影响和开放问题专题讨论与评分 rubric | `.venv/bin/python verify_course.py` |
| 2026-06-05 | project report template | 新增最终项目报告模板、复现证据清单和 TA review checklist | `.venv/bin/python verify_course.py` |
| 2026-06-05 | student site release builder | 新增 `scripts/build_course_site_release.py`，用于剥离章节内嵌参考解答并生成学生安全站点清单 | `.venv/bin/python verify_course.py` |

## 发布前 Checklist

| 检查项 | 通过标准 |
|--------|----------|
| 章节链接 | 每讲至少有一个章节、handout 或项目 README |
| 阅读链接 | 每周阅读能在 reading list 中找到 |
| 作业证据 | 每周至少有作业、书面题、阅读复盘或项目证据 |
| Demo 证据 | 课堂 demo 对应到公开测试、capstone acceptance 或可手算推导 |
| 可访问性 | 图片、公式、录屏和 slides 有文本替代或说明 |
| 验证命令 | `.venv/bin/python verify_course.py` 通过 |
