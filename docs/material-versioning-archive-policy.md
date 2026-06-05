# Material Versioning and Archive Policy

本政策用于管理课程章节、作业、slides、notes、demo、项目样例和学生站点发布包的版本边界。高校课程不能只提供“当前文件”；还需要说明哪些材料是正式评分依据，哪些是历史参考，哪些已经 retired，哪些只供教师内部使用。内容勘误、修订、公告和验证闭环按 [Course Errata and Correction Ledger](course-errata-correction-ledger.md) 记录。

参照点：CS224N 当前公开页会区分本轮课程、往年网站、往年报告、公开视频和当前作业，并明确提醒学生不要把旧作业当作本轮提交依据。本课程采用同类原则，但用可移植的仓库规则表达。

## 版本状态

| 状态 | 是否可作为评分依据 | 学生可见性 | 使用边界 |
|------|--------------------|------------|----------|
| current | 是 | 可公开 | 本轮课程正式材料；必须通过 `.venv/bin/python verify_course.py` |
| release-candidate | 暂不作为最终评分依据 | 可限量预览 | 可用于教师 dry run、TA 校准和少量学生试读；发布前必须转为 current |
| archived | 否 | 可公开或校内可见 | 仅作历史参考；不得作为本轮作业、quiz、项目或评分依据 |
| retired | 否 | 通常不公开 | 已被替换、含错误或不适合本轮课程；不能在学生站点发布 |
| instructor-only | 否 | 不公开 | 参考解答、隐藏测试、评分校准、staff runbook、内部事故记录 |

## 材料类型规则

| 材料 | 版本要求 | 归档要求 | 禁止事项 |
|------|----------|----------|----------|
| HTML 章节 | 标明章节号、学习目标、来源复核入口和最后验证命令 | 若内容大改，应保留变更摘要，不要求保留旧 HTML | 不发布内嵌参考解答到正式学生站点 |
| 作业包 | 每次发布记录 assignment id、发布时间、截止时间、测试入口和 `RELEASE_MANIFEST.json` | 旧作业包只能作为 archived，不得混入 current LMS | 不上传 `reference_solution.py`、隐藏测试或教师答案 |
| Slides / notes | 标明讲次、发布日期、最后更新时间、对应章节和可访问替代材料 | 往年 slides 或 notes 必须标为 archived | 不把 planned outline 伪装成已发布 slides |
| Demo / notebook | 固定运行命令、依赖版本、预期输出和 fallback | 旧 demo 若依赖失效，应标为 retired 或更新 | 不依赖私有路径、私有数据、隐藏环境变量 |
| 项目报告样例 | 标明课程轮次、依赖、硬件、数据许可和脱敏状态 | 仅作写作结构参考，不作可复制答案 | 不公开敏感数据、密钥、私有路径或未授权材料 |
| 外部链接与论文 | 记录访问日期、版本、来源等级和复核频率 | 链接迁移时保留旧链接处理记录 | 不把二手解读作为唯一证据支撑前沿数字 |

## 学生站点发布规则

正式学生站点必须由 `scripts/build_course_site_release.py` 构建，并满足：

- 只包含 current 或学生可见的 release-candidate 材料。
- 排除 instructor-only 文档、参考解答、隐藏测试和评分校准材料。
- `SITE_RELEASE_MANIFEST.json` 记录 included roots、safe docs、excluded docs、章节剥离统计、作业发布包清单。
- 发布包内 HTML/Markdown 本地链接必须全部有效。
- 发布前运行 `.venv/bin/python verify_course.py`，期末或重大改版运行 `.venv/bin/python verify_course.py --capstone --training`。

## 旧材料与历史报告

历史材料可以帮助学生理解课程演进，但必须满足：

- 明确标注 archived 或 retired。
- 明确说明“不作为本轮课程评分依据”。
- 若含往届项目报告或优秀作业样例，必须脱敏，并删除私有数据、密钥、学生身份和未授权代码。
- 若旧材料与当前章节公式、API、作业接口或政策冲突，当前 syllabus、assignment release manifest 和 course materials index 优先。
- 学生不得直接复用旧代码、旧报告文字或往届项目实验结果作为本轮提交。

## 版本记录字段

每次发布或归档至少记录：

| 字段 | 说明 |
|------|------|
| material_id | 例如 `ch03`, `assignment-ch03-attention`, `lecture-L07-slides`, `site-release-2026-06-05` |
| status | current / release-candidate / archived / retired / instructor-only |
| release_date | 发布或归档日期 |
| audience | students / staff / public / institution-only |
| source_files | 相关源码或文档路径 |
| validation | 运行过的命令或人工审查证据 |
| change_summary | 改动摘要和影响范围 |
| replacement | 若 retired，说明替代材料 |

## 归档记录样例

| material_id | status | release_date | audience | source_files | validation | change_summary | replacement |
|-------------|--------|--------------|----------|--------------|------------|----------------|-------------|
| site-release-2026-06-05 | release-candidate | 2026-06-05 | students | `index.html`, `chapters/`, `docs/`, `assignments/` | `.venv/bin/python verify_course.py` reports `COURSE VERIFY: PASS`; course site release builder strips inline solutions and excludes instructor-only docs | readiness release includes chapter pages, student-safe docs, and assignment packages for dry-run review | N/A |
| assignment-ch03-attention-2026-06-05 | release-candidate | 2026-06-05 | students | `assignments/ch03_attention/` | assignment release builder packages student-safe suite; public tests target `student_solution` in release | attention assignment package ready for live LMS upload after private hidden-test sign-off | N/A |
| assignment-ch02-legacy-rope | archived | 2026-06-05 | staff | prior Ch02 notes or assignment variants if retained outside this repository | archived manually by course staff; not referenced by current syllabus or LMS | old RoPE explanations that suggest monotonic distance decay must not be used for current scoring | `assignment-ch02_embeddings` current release |

## 发布前 Checklist

- [Course Materials Index](course-materials-index.md) 中没有 planned 材料被描述为 ready。
- [Assignment Submission and Release Guide](assignment-submission-guide.md) 的发布包命令仍能生成 student-safe assignment release。
- 学生站点发布包不含 instructor-only 文档、`reference_solution.py`、隐藏测试或 grading calibration。
- 旧材料若仍可访问，必须标明 archived/retired 和“不作为本轮评分依据”。
- 每次重大内容更新后，同步更新 [Course Errata and Correction Ledger](course-errata-correction-ledger.md)、[Course Operations and Improvement Log](course-operations-log.md) 或本文件的归档记录。
