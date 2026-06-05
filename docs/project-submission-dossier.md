# Project Submission Dossier

复核日期：2026-06-05

本文件定义 final project、训练工程 capstone 和推理工程 capstone 的学生提交包结构。它补充 [Capstone Proposal and Milestone Guide](capstone-proposal-milestone.md)、[Project Report Template and Reproducibility Checklist](project-report-template.md)、[Capstone 项目报告 Rubric](project-report-rubric.md)、[Capstone Defense and Oral Exam Question Bank](capstone-defense-oral-exam-bank.md)、[Dataset, Model, and Artifact Provenance Registry](dataset-model-artifact-registry.md)、[Data and Ethics Review](data-ethics-review.md)、[Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md)、[Compute Resource and Cost Guide](compute-resource-guide.md)、[Project Team and Mentor Policy](project-team-mentor-policy.md)、[Final Project Showcase and Archive Policy](final-project-showcase-archive-policy.md) 和 [Academic Integrity Case Process](academic-integrity-case-process.md)。

目标是让学生、助教和教师对“提交什么才算完整”有同一个答案：proposal、milestone、final report、presentation 和 archive candidate 都映射到同一组机器可读或人工可复核证据。

## Dossier Stages

| stage_id | 时间点 | 学生交付 | TA review focus | 不通过风险 |
|----------|--------|----------|-----------------|------------|
| DSR-PROPOSAL | proposal | project brief、risk register、data/source plan、compute plan、split_card 草案、metric_card 草案、artifact_manifest 草案 | 可行性、数据合规、资源预算、claim 降级路径 | 目标过大、数据来源不清、无 baseline |
| DSR-MILESTONE | milestone | minimal runnable loop、logs、first results、failure cases、updated split_card、metric_card、uncertainty_record、claim_audit、leakage_check | 最小闭环、日志可追溯、风险是否收敛 | 只有成功 demo、没有机器可读证据 |
| DSR-FINAL | final report | report、source code、reproduction commands、environment record、metrics、error analysis、data ethics、artifact_manifest、contribution record | rubric 评分、claim/evidence 对齐、复现性 | 数字无法复现、claim 过强、缺少伦理审查 |
| DSR-PRESENTATION | poster or slides | poster/slides、2-minute pitch、failure case、reproduction command、risk boundary | 展示是否反映真实证据和局限 | 只展示成功样例或隐藏风险 |
| DSR-ARCHIVE | optional archive | redacted report、public abstract、consent record、archive record、artifact retention plan | consent、redaction、source boundary、public safety | 公开敏感信息、未授权数据或 hidden tests |

## Required File Map

| file_or_record | required_stage | owner | evidence_type | minimum_content | reviewer_action |
|----------------|----------------|-------|---------------|-----------------|-----------------|
| `proposal.md` | DSR-PROPOSAL | student | narrative + tables | problem、non-goals、baseline、risk register、compute budget | approve / revise / reject scope |
| `artifact_manifest.md` | DSR-PROPOSAL; DSR-MILESTONE; DSR-FINAL | student | structured provenance | artifact_id、type、origin、license、PII、contamination、retention | compare with registry and data ethics |
| `split_card.md` | DSR-PROPOSAL; DSR-MILESTONE; DSR-FINAL | student | experiment control | split_id、train_source、dev_policy、test_policy、leakage_check | verify no dev/test leakage |
| `metric_card.md` | DSR-PROPOSAL; DSR-MILESTONE; DSR-FINAL | student | metric definition | metric、definition、aggregation、limit、failure mode | check metric supports target claim |
| `uncertainty_record.md` | DSR-MILESTONE; DSR-FINAL | student | statistical evidence | bootstrap_ci、seed_sensitivity、paired_comparison、load-test variance 或 single_seed_limit | match claim strength to evidence |
| `claim_audit.md` | DSR-MILESTONE; DSR-FINAL | student | source and claim gate | claim、evidence、source level、boundary、downgrade_decision | downgrade unsupported claims |
| `leakage_check.md` | DSR-MILESTONE; DSR-FINAL | student | contamination evidence | exact/near duplicate、prompt leakage、retrieval contamination、benchmark contamination | block high-confidence claims if missing |
| `run_log.txt` | DSR-MILESTONE; DSR-FINAL | student | command evidence | command、cwd、Python、PyTorch、device、seed、first failing test | reproduce or spot-check |
| `metrics.jsonl` or `benchmark_report.json` | DSR-MILESTONE; DSR-FINAL | student | machine-readable results | metric values、timestamp、config、hardware、workload | reconcile with report tables |
| `data_ethics_review.md` | DSR-FINAL | student | risk review | license、PII、bias、contamination、safety、residual risk | apply data ethics rubric |
| `contributions.md` | DSR-FINAL | student | authorship record | member roles、external code、AI tool use、mentor input | check team policy and integrity cases |
| `poster_or_slides.*` | DSR-PRESENTATION | student | presentation artifact | problem、method、result、failure、repro command、risk | map to presentation rubric |
| `archive_record.md` | DSR-ARCHIVE | staff + student | public archive control | consent_status、redaction_status、artifact_manifest、archived_label | approve public / institution-only / staff-only |

## Structured Templates

### artifact_manifest

```text
artifact_id:
artifact_type:
course_use:
storage_location:
source_or_origin:
license_or_access:
pii_risk:
contamination_risk:
retention_scope:
student_action:
review_gate:
```

### split_card

```text
split_id:
train_source:
dev_policy:
test_policy:
freeze_date:
leakage_check:
known_overlap:
allowed_tuning:
disallowed_tuning:
```

### metric_card

```text
metric:
definition:
aggregation:
unit:
higher_is_better:
minimum_success_threshold:
known_limit:
failure_mode:
```

### uncertainty_record

```text
method: bootstrap_ci / seed_sensitivity / paired_comparison / load_test_variance / single_seed_limit
sample_count:
seed_list:
confidence_level:
result_summary:
claim_allowed:
claim_not_allowed:
```

### claim_audit

```text
claim_id:
claim_text:
claim_type: quality / efficiency / safety / robustness / generalization / source
evidence_files:
source_level:
statistical_support:
boundary:
downgrade_decision:
```

## Stage Acceptance Matrix

| criterion | DSR-PROPOSAL | DSR-MILESTONE | DSR-FINAL |
|-----------|--------------|---------------|-----------|
| scope | problem、non-goals、baseline | revised scope explains changes | final scope matches evidence |
| reproducibility | planned command and environment | one runnable core loop | primary command reproduces core result |
| data provenance | source and artifact_manifest draft | audit result and leakage_check draft | license、PII、split、retention complete |
| experiment design | split_card and metric_card draft | first result plus failure cases | baseline、ablation、uncertainty and claim audit complete |
| engineering evidence | compute budget and fallback | logs、checkpoint or benchmark report | metrics、cost、capacity or training stability evidence |
| communication | risk register | mentor questions and next actions | report、poster and contribution disclosure |

## TA Review Procedure

| review_step | check | evidence | outcome |
|-------------|-------|----------|---------|
| R1 completeness | required files for the stage are present | Required File Map | pass / missing item list |
| R2 reproducibility | command, environment and output agree | `run_log.txt` and metrics file | pass / rerun required |
| R3 provenance | artifacts map to registry and data ethics review | `artifact_manifest.md` and registry IDs | pass / license or PII revision |
| R4 experiment rigor | split, metric, uncertainty and leakage gates are aligned | split_card、metric_card、uncertainty_record、leakage_check | pass / claim downgrade |
| R5 report alignment | report tables, figures and claims match logs | final report, metrics, claim_audit | pass / grading note |
| R6 integrity and archive | authorship, external help and public boundary are clear | contributions、mentor notes、archive_record | pass / staff-only or case review |

## Common Downgrade Decisions

| trigger | downgrade_decision | scoring consequence |
|---------|--------------------|---------------------|
| single seed only | write single_seed_limit; avoid robust or significant language | metric/experiment score capped unless limitation is clear |
| public benchmark may be contaminated | use benchmark as diagnostic result; add held-out or manual error analysis | no broad generalization claim |
| toy corpus only | claim engineering workflow, not model quality | data and result claims stay local |
| missing model card | cite model as unavailable or remove model-specific claim | source and ethics score reduced |
| no P95/P99 latency | report average latency only as preliminary evidence | inference engineering score capped |
| no artifact_manifest | block final grading until provenance is submitted | project cannot receive full reproducibility or ethics credit |

## Student Final Checklist

| item | pass condition |
|------|----------------|
| primary command | one command or clear command sequence runs core result |
| environment | Python、PyTorch、dependency、hardware and seed recorded |
| artifact_manifest | every dataset/model/tokenizer/checkpoint/eval/runtime asset has provenance |
| split_card | train/dev/test or prompt tuning/final eval boundary is explicit |
| metric_card | every headline metric has definition, aggregation and limitation |
| uncertainty_record | comparisons have CI、seed sensitivity、paired comparison、load-test variance or single_seed_limit |
| claim_audit | strong words are supported or downgraded |
| leakage_check | duplicate、prompt leakage、RAG leakage and benchmark contamination addressed |
| data_ethics_review | license、PII、bias、safety and residual risk addressed |
| contributions | team roles、external code、AI tools and mentor input disclosed |
| presentation | failure case and reproduction command appear in poster/slides |
| archive boundary | public release, institution-only or staff-only status is stated |

## Release Checklist

| 检查项 | 通过标准 |
|--------|----------|
| dossier stages | DSR-PROPOSAL、DSR-MILESTONE、DSR-FINAL、DSR-PRESENTATION 和 DSR-ARCHIVE 均定义 |
| required files | proposal、artifact_manifest、split_card、metric_card、uncertainty_record、claim_audit、leakage_check、run_log、metrics、data_ethics_review、contributions、poster/slides 和 archive_record 均有行 |
| stage acceptance | proposal、milestone 和 final report 的 acceptance matrix 可逐项评分 |
| TA workflow | completeness、reproducibility、provenance、rigor、alignment、integrity/archive 六步 review procedure 完整 |
| linked governance | capstone guide、report template、rubric、registry、data ethics、experimental rigor、compute、team policy、archive policy 和 academic integrity 均链接本文件 |
| verifier gate | `verify_course.py` 检查 dossier markers、表格结构、交叉链接和 release inclusion |
