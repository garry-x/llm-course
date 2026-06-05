# External Expert Review Dossier

复核日期：2026-06-05

本档案用于记录课程材料的独立专家复核流程。它补充 [高校课程质量审计与升级路线](university-course-quality-audit.md)、[Chapter Claim Audit Ledger](chapter-claim-audit-ledger.md)、[Chapter Source and Accuracy Map](chapter-source-map.md)、[Mathematical Derivation Audit](mathematical-derivation-audit.md)、[External Source Verification Guide](external-source-verification.md)、[前沿模型来源等级与复核记录](frontier-source-audit.md)、[Course Errata and Correction Ledger](course-errata-correction-ledger.md)、[Teaching Observation and Course Evaluation Dossier](teaching-observation-course-evaluation.md) 和 [Course Operations and Improvement Log](course-operations-log.md)。

本档案可以随 student site release 发布。记录只使用 reviewer_role、scope_id、review_id 和聚合状态，不公开个人姓名、私人评语、真实学生反馈、成绩、住宿安排、隐藏测试输入、参考解答或 staff personnel evaluation。

## Review Scope

| scope_id | material boundary | expert task | required evidence |
| --- | --- | --- | --- |
| ER-CONTENT | chapters, lecture samples, recitation worksheets | Check factual accuracy, prerequisite flow, terminology, and topic depth against an upper-level NLP/LLM course standard. | marked chapter list, issue log, response owner |
| ER-MATH | derivations, written problems, formula rendering | Re-derive equations, verify tensor shapes, identify unstated assumptions, and confirm notation consistency. | derivation trace, shape table, verifier command |
| ER-SOURCES | source maps, claim ledger, external links, frontier model notes | Check source tier, date sensitivity, claim wording, and volatile benchmark/API/model-card boundaries. | source tier decisions, replacement links, errata linkage |
| ER-ASSIGNMENTS | public handouts, starters, visible tests, rubrics | Check feasibility, alignment, grading clarity, runtime expectations, and student release safety. | assignment matrix, failing-case notes, runtime evidence |
| ER-ASSESSMENT | quizzes, written problem bank, review packs, item analysis | Check outcome coverage, item difficulty, discrimination signals, and exam integrity procedures. | blueprint mapping, item notes, administration note |
| ER-PROJECTS | capstone guides, report templates, rigor/evaluation guides | Check project scope, reproducibility, statistical evaluation, ethics review, and archival policy. | project evidence packet, rubric trace, closure note |
| ER-ACCESSIBILITY | media policy, support docs, slides/notes samples | Check accessibility text, pacing, accommodations boundary, and student support language. | accessibility pass list, remediation note |
| ER-RELEASE | student site, assignment release, manifest, link graph | Check that student-visible artifacts exclude private grading material while preserving required guidance. | release manifest, forbidden-content scan, browser smoke |

## Reviewer Independence Rules

| rule_id | rule | operational check |
| --- | --- | --- |
| ER-IND-ROLE | Record reviewer_role instead of personal names in the public dossier. | `reviewer_role` must appear in every evidence packet. |
| ER-IND-CONFLICT | Run a conflict_check before assigning a reviewer. | The reviewer did not author the reviewed artifact and has no direct grading authority for it. |
| ER-IND-EXPERTISE | Match source expertise to scope. | NLP instructor for content/math, systems reviewer for serving/training, accessibility reviewer for media/support. |
| ER-IND-SEPARATION | Keep reviewer comments separate from grade decisions. | Reviews can request rubric changes, but cannot change individual grades. |
| ER-IND-CONFIDENTIALITY | Protect confidential materials. | Private notes use internal storage; student release shows only aggregate status and public-safe summaries. |

## Review Rubric

| dimension | review question | pass evidence |
| --- | --- | --- |
| technical_accuracy | Are statements, definitions, claims, diagrams, and implementation descriptions correct within the stated source boundary? | no S0/S1 open findings; claim ledger updated |
| mathematical_rigor | Are derivations complete enough for students to reproduce, with assumptions, shapes, and boundary cases explicit? | derivation audit row and formula verifier pass |
| source_traceability | Can high-risk claims be traced to stable papers, official docs, or clearly labeled current sources? | source tier, access date, volatile-source review date |
| assessment_alignment | Do exams, quizzes, written tasks, assignments, and rubrics measure declared course outcomes? | blueprint link, item bank link, rubric mapping |
| implementation_reproducibility | Can code examples, starters, tests, and demos run in the stated environment without hidden dependencies? | command output, runtime note, failure-mode review |
| project_rigor | Do capstone materials require sound baselines, metrics, uncertainty, ethics, and reproducibility evidence? | project dossier, report template, evaluation statistics link |
| accessibility_inclusion | Are media, slides, notes, pacing, and support routes usable by students with different access needs? | accessibility checklist and remediation status |
| release_safety | Does the public release omit private grading/security content while retaining enough student guidance? | release manifest, forbidden-content scan, link check |

## Current External Review Ledger

| review_id | reviewer_role | scope_id | finding | severity | required_response | status |
| --- | --- | --- | --- | --- | --- | --- |
| ER-2026-MATH-ROPE | external NLP instructor | ER-MATH | Ch02 RoPE section needed explicit complex-plane analogy boundary and raw TeX rendering gate. | ER-S1 | Patch chapter, add formula gate, record errata. | closed; verifier covers raw TeX and KaTeX render |
| ER-2026-SOURCE-FRONTIER | external model evaluation reviewer | ER-SOURCES | Frontier model claims needed date-sensitive wording and source tier separation. | ER-S1 | Add frontier source audit and volatile-source复核 rule. | closed; linked to source governance docs |
| ER-2026-ASSIGN-ATTN | external teaching assistant lead | ER-ASSIGNMENTS | Attention assignment needed clearer visible tests and hidden-boundary separation. | ER-S2 | Update handout, starter failure modes, and release builder checks. | closed; public assignment tests pass |
| ER-2026-PROJECT-CAPSTONE | external systems reviewer | ER-PROJECTS | Capstone reports needed stronger reproducibility, latency/throughput evidence, and artifact manifests. | ER-S2 | Add project submission dossier and acceptance evidence. | closed; capstone evidence recorded |
| ER-2026-ACCESS-MEDIA | accessibility reviewer | ER-ACCESSIBILITY | Slide and media review needed alt text, transcript policy, and support escalation language. | ER-S2 | Add media access policy, slide sample accessibility text, and support guide hooks. | closed; release checklist covers accessibility |
| ER-2026-RELEASE-SAFETY | external course operations reviewer | ER-RELEASE | Student site release needed proof that instructor-only docs and inline solutions are excluded. | ER-S1 | Extend release builder, browser smoke, manifest evidence, and forbidden-doc checks. | closed; release builder validates student site |

## Response and Closure Workflow

| step | action | required output |
| --- | --- | --- |
| 1. intake | Assign review_id, reviewer_role, scope_id, reviewed materials, and conflict_check. | evidence packet starts with public-safe identifiers |
| 2. triage | Classify severity, affected learning outcomes, and release risk. | severity code and owner recorded |
| 3. response | Instructor writes accept, revise, or reject with rationale tied to evidence. | required_response field updated |
| 4. patch | Update chapters, docs, tests, scripts, release notes, or errata as needed. | patch reference or changed artifact list |
| 5. verify | Run the narrow gate and then `.venv/bin/python verify_course.py` when release-facing materials changed. | verification_command and result |
| 6. close | Reviewer or designated owner confirms closure and updates public-safe ledger. | closure_status and next review date |

## Evidence Packet Template

```yaml
review_id: ER-YYYY-SCOPE-SLUG
reviewer_role: external NLP instructor | external systems reviewer | accessibility reviewer | assessment reviewer
scope_id: ER-CONTENT | ER-MATH | ER-SOURCES | ER-ASSIGNMENTS | ER-ASSESSMENT | ER-PROJECTS | ER-ACCESSIBILITY | ER-RELEASE
conflict_check: reviewer did not author the artifact and has no direct grading authority
materials_reviewed: chapters, docs, assignments, projects, release manifest, or verifier gates
findings: public-safe summary of technical issue or confirmation
severity: ER-S0 | ER-S1 | ER-S2 | ER-S3
response_owner: instructor role or course operations role
patch_ref: changed file list, commit id, or release batch identifier
verification_command: .venv/bin/python verify_course.py
closure_status: open | accepted_for_patch | verified | closed
```

## Severity and Required Response

| severity | meaning | required response |
| --- | --- | --- |
| ER-S0 | Safety, privacy, academic integrity, or release leak issue. | Remove affected release artifact, notify staff, patch before any student publication. |
| ER-S1 | Technical inaccuracy, broken formula, wrong source claim, or grading-impacting issue. | Patch before next release, add errata entry, run verifier and affected tests. |
| ER-S2 | Ambiguity, missing assumption, incomplete evidence, or uneven assessment alignment. | Patch in the next maintenance window and record closure evidence. |
| ER-S3 | Style, clarity, optional enrichment, or future expansion suggestion. | Track in operations log and batch with normal course improvements. |

## Release Checklist

- Review Scope includes content, math, sources, assignments, assessment, projects, accessibility, and release safety.
- Reviewer Independence Rules include reviewer_role, conflict_check, source expertise, no grading authority, and confidentiality.
- Review Rubric covers technical_accuracy, mathematical_rigor, source_traceability, assessment_alignment, implementation_reproducibility, project_rigor, accessibility_inclusion, and release_safety.
- Current External Review Ledger has public-safe review_id records with severity, required_response, and status.
- Response and Closure Workflow includes intake, triage, response, patch, verify, and close.
- Evidence Packet Template includes review_id, reviewer_role, conflict_check, materials_reviewed, verification_command, and closure_status.
- Severity table defines ER-S0, ER-S1, ER-S2, and ER-S3.
- Student site release contains only public-safe aggregate review evidence.
