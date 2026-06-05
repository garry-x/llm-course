# Lecture Notes Quality and Review Standard

课堂同行观察和期中/期末课程评估发现的 lecture clarity、pacing、technical accuracy 和 accessibility 问题，应按 [Teaching Observation and Course Evaluation Dossier](teaching-observation-course-evaluation.md) 回写到本审稿标准；每讲 quick check、exit ticket、office hours、作业失败类别和阅读复盘形成的下次课调整，按 [Weekly Teaching Reflection and Adjustment Log](weekly-teaching-reflection-adjustment-log.md) 记录。

本标准用于把每讲 lecture notes 从“有索引”提升为可审稿、可修订、可追溯的高校课程讲义。它补充 [Lecture Notes Index](lecture-notes-index.md)、[Lecture Notes Review Ledger](lecture-notes-review-ledger.md)、[Lecture Note Sample Pack](lecture-note-sample-pack.md)、[Lecture Slide Outline](lecture-slide-outline.md)、[Lecture Slide Sample Pack](lecture-slide-sample-pack.md)、[Board Derivation and Instructor Notes Pack](board-derivation-pack.md)、[Classroom Demo Runbook](demo-runbook.md)、[Course Materials Index](course-materials-index.md)、[Material Versioning and Archive Policy](material-versioning-archive-policy.md)、[Course Errata and Correction Ledger](course-errata-correction-ledger.md)、[Chapter Source and Accuracy Map](chapter-source-map.md) 和 [External Source Verification Guide](external-source-verification.md)。

## 适用范围

| 材料类型 | 审查重点 | 学生可见性 |
|----------|----------|------------|
| HTML chapter used as notes | 公式、shape、代码练习、来源边界、可访问性 | 学生可见 |
| Markdown handout | 推导完整度、阅读连接、rubric 和提交证据 | 学生可见 |
| slide outline | 是否能映射到正式 notes、demo 和 quick check | 学生可见 |
| board derivation script | 符号一致、推导步骤、常见误区、评分证据 | 可学生可见或 instructor-only |
| external lecture notes | 来源、访问日期、使用范围、与本课程差异 | 仅在复核后作为学生材料 |
| recording transcript / summary | 勘误、隐私剪辑、术语一致、可访问性 | 按媒体政策发布 |

## Notes Quality Rubric

| 维度 | 最低标准 | 高质量标准 |
|------|----------|------------|
| Learning goals | 2-4 条可测目标 | 每条目标都能映射到 quick check、作业、书面题或项目证据 |
| Notation ledger | 写清 batch、sequence、heads、hidden、vocab、dtype 或 metric 符号 | 与章节、板书、作业测试和书面题使用同一符号 |
| Derivation completeness | 给出关键公式的中间步骤 | 标出假设、近似、边界条件和不能外推的结论 |
| Shape and units | 标出核心张量 shape、mask broadcast、metric 单位或成本单位 | 用至少一个 failure mode 检查 shape/units 错误 |
| Code binding | 指向 starter、tests、demo command 或 capstone acceptance | 说明公式对应哪段 API、测试断言或日志字段 |
| Source boundary | 区分论文事实、课程解释、模型卡声明、社区传闻和未复核前沿信息 | 给出来源等级、访问日期和需要复核的易变 claim |
| Misconception coverage | 至少列出 2 个常见误区 | 误区连接到 [Concept Mastery and Misconception Map](concept-misconception-map.md) 或 hidden test 类别 |
| Accessibility | 公式、图、表、视频或板书有文字替代 | 对视觉材料给出 alt text、caption、transcript 或 structured summary |
| Correction path | 明确发现错误后如何公告、修订和验证 | 有 review_record、change_summary 和 affected_materials |

## Per-Lecture Review Checklist

每讲 notes 发布或改动前，教师或指定 reviewer 至少检查：

| check_id | 问题 | 证据 |
|----------|------|------|
| notation_consistency | 符号是否与章节、slide outline、board derivation 和作业测试一致？ | notation ledger、公式片段、测试 API |
| derivation_steps | 是否只给结论而缺少关键中间步骤？ | 推导文本、板书脚本、书面题答案 |
| shape_invariants | 是否标出输入、输出、mask、cache 或 metric shape？ | shape table、demo trace、public tests |
| code_binding | 公式或概念是否能定位到 starter/test/demo/capstone？ | 文件路径、函数名、命令或 assertion |
| source_boundary | 前沿模型、benchmark、API、价格或产品 claim 是否有来源等级？ | source inventory、frontier audit、访问日期 |
| misconception_link | 是否覆盖本讲最容易错的概念边界？ | concept map、FAQ、office hours 聚合 |
| accessibility_asset | 图片、公式、录屏、板书或表格是否有文字替代？ | alt text、caption、transcript、summary |
| release_status | 材料状态是否为 ready、draft、planned、archived 或 retired？ | course materials index 或 archive policy |
| correction_path | 若本讲出错，学生如何知道、如何补救、如何复核？ | announcement、operations log、verification command |

## Sample Lecture Note Packet

每讲 notes 推荐按以下顺序组织，避免只列 slides 标题：

```text
Lecture:
Status: ready / draft / planned / archived / retired
Learning goals:
Notation ledger:
Core derivation:
Shape checks:
Code binding:
Demo command:
Common misconceptions:
Source boundary:
Accessibility notes:
Quick check:
Post-lecture evidence:
Review record:
```

完整学生可见样例见 [Lecture Note Sample Pack](lecture-note-sample-pack.md)，当前提供 L1 tokenization、L3 attention、L9 training 和 L18 serving 四类 notes 样例。

## Review Record Template

| field | 内容 |
|-------|------|
| lecture_id | L1-L20 |
| material_id | chapter、handout、slides、notes、recording 或 summary |
| reviewer | instructor、Head TA、source owner 或 accessibility reviewer |
| review_date | 复核日期 |
| status | ready、draft、planned、archived、retired |
| notation_checked | Yes/No |
| derivation_checked | Yes/No |
| code_binding_checked | Yes/No |
| source_boundary_checked | Yes/No |
| accessibility_checked | Yes/No |
| affected_materials | 章节、作业、阅读、demo、rubric 或项目材料 |
| change_summary | 修改内容和原因 |
| verification_command | 例如 `.venv/bin/python verify_course.py` |

## Correction Workflow

| 触发 | 处理动作 | 学生沟通 |
|------|----------|----------|
| 公式符号错误 | 修正 notes、章节或板书脚本，检查相关作业测试 | 若影响作业或评分，发布公告 |
| shape 或代码绑定错误 | 修正 demo、starter/test 说明或 FAQ | 给出最小复现和受影响范围 |
| 来源事实变化 | 降级 claim、更新 source inventory 或 frontier audit | 说明旧结论为何不再作为事实 |
| 可访问性缺口 | 增加 transcript、summary、alt text 或替代材料 | 通知有影响的学生和 staff |
| 录播或课堂口误 | 发布 correction note，必要时剪辑录播 | 在 materials index 或 operations log 记录 |
| 作业解释歧义 | 更新 handout、rubric 或 assignment guide | 若影响已提交作业，说明统一处理方式 |

更正后至少运行 `.venv/bin/python verify_course.py`；若影响 capstone、release package 或训练/推理验收，运行 `.venv/bin/python verify_course.py --capstone --training`。

## Evidence Matrix

| 讲次范围 | 必须连接的证据 | 复核重点 |
|----------|----------------|----------|
| L1-L2 | Ch01/Ch02 tests、Python/PyTorch review、word vector/RoPE written proof | BPE 贪心边界、embedding 经验结构、RoPE 相对位置符号 |
| L3-L6 | Ch03-Ch05 tests、board derivation、attention/norm/block written problems | mask 位置、variance assumptions、pre-norm、MLA/GQA cache 边界 |
| L7-L10 | Ch06-Ch07 tests、training capstone、optimizer/scheduler proof | next-token shift、MoE routing、CE stability、checkpoint/resume |
| L11-L14 | Ch08-Ch09 tests、generation/alignment written problems | sampling candidate set、speculative decoding、LoRA initialization、DPO/GRPO direction |
| L15-L16 | Ch11 tests、classic NLP handout、data ethics review | metric limitations、dependency parsing constraints、PII/license/contamination |
| L17-L18 | Ch10 tests、inference capstone acceptance、capacity plan | KV cache formula、RAG retrieval vs answer quality、P95/P99/SLO |
| L19-L20 | project report, presentation, peer review, operations log | reproducibility chain、claim/evidence/risk alignment、course improvement |

## Staff Checklist

- 每讲 notes 的 review record 至少有 notation_checked、derivation_checked、code_binding_checked、source_boundary_checked 和 accessibility_checked。
- L1-L20 当前 review record 必须记录在 [Lecture Notes Review Ledger](lecture-notes-review-ledger.md)，且任何新增 slides、录屏或 notebook 需要追加同等级复核。
- 每讲至少一个 formula/shape/code claim 能定位到公开测试、书面题、demo 或 capstone evidence。
- 前沿模型和 benchmark claim 不写成未复核事实；易变信息有访问日期和复核频率。
- 发现错误后按 Correction Workflow 更新 notes、公告、materials index 或 operations log。
- instructor-only notes、隐藏测试、评分校准和 reference solution 不进入学生站点发布包。

## 发布前 Checklist

- [Lecture Notes Index](lecture-notes-index.md) 链接本标准和 [Lecture Notes Review Ledger](lecture-notes-review-ledger.md)，并要求 L1-L20 具备 review record。
- [Lecture Note Sample Pack](lecture-note-sample-pack.md) 提供至少 4 个代表性 notes 样例，覆盖基础、attention、training 和 serving。
- [Course Materials Index](course-materials-index.md) 的 slides / notes / recording 规则引用本标准。
- [Lecture Slide Outline](lecture-slide-outline.md) 要求 slides 映射到 reviewed notes。
- `scripts/build_course_site_release.py` 把本文件列入学生安全文档。
- `.venv/bin/python verify_course.py` 通过。
