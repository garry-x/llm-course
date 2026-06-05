# Safety and Societal Impact Casebook

复核日期：2026-06-05

本 casebook 把 LLM 课程中的安全、伦理、社会影响和部署风险落成可讨论、可评分、可复核的案例。它补充 [Data and Ethics Review](data-ethics-review.md)、[Frontier Seminar Handout](frontier-seminar-handout.md)、[Project Report Template and Reproducibility Checklist](project-report-template.md)、[Capstone 项目报告 Rubric](project-report-rubric.md)、[Reading Discussion Question Bank](reading-discussion-question-bank.md)、[Chapter Source and Accuracy Map](chapter-source-map.md)、[External Source Verification Guide](external-source-verification.md)、[Experimental Rigor and Evaluation Statistics Guide](experimental-rigor-evaluation-statistics.md) 和 [Course Policies](course-policies.md)。

使用边界：本文件可以进入 student site release。案例使用 synthetic 或 generic 场景，不包含真实学生提交、真实敏感数据、攻击 payload、绕过安全机制的操作步骤、私有评分样例、hidden tests 或 reference_solution.py。

## Case Analysis Schema

| field | requirement |
| --- | --- |
| case_id | Stable `SSI-*` identifier. |
| scenario | Student-facing scenario with no real personal data or exploit steps. |
| primary_risk | Main risk category: privacy, bias, safety, contamination, misuse, copyright, access, evaluation or governance. |
| evidence_to_collect | Data, metric, source, log, model card or human-review evidence needed. |
| mitigation | Concrete change to data, model, prompt, evaluation, logging, deployment or report scope. |
| residual_risk | What still cannot be guaranteed after mitigation. |
| course_link | Chapter, project, reading question, rubric or ethics review artifact. |

## Core Cases

| case_id | scenario | primary_risk | evidence_to_collect | mitigation | residual_risk | course_link |
| --- | --- | --- | --- | --- | --- | --- |
| SSI-RAG-MED | A team builds a RAG demo over public medical FAQ pages and claims it can answer patient-specific questions. | safety | Source records, retrieval accuracy, generated answer audit, refusal cases, medical-advice boundary. | Limit scope to general information, add refusal/redirect policy, evaluate retrieval and generation separately. | Cannot guarantee clinical correctness, individualized advice or emergency handling. | Ch10, data-ethics-review.md, RDQ-W9-RAG |
| SSI-HIRING-BIAS | A classifier ranks resumes using a dataset from one region and one industry. | bias | Dataset demographics if available, feature audit, subgroup performance, false positive/negative examples. | Report representativeness limits, avoid high-stakes automation claim, add human review and subgroup analysis. | Hidden proxy variables and unobserved demographic harms may remain. | project-report-template.md, nlp-evaluation-coverage.md |
| SSI-RAG-PII | A RAG system indexes internal documents and sometimes returns names, emails or private notes. | privacy | Data inventory, PII scan, retrieval logs, redaction rules, access-control boundary. | Remove or redact sensitive docs, restrict retrieval scope, avoid storing raw prompts with identifiers. | PII detection can miss context-specific identifiers. | data-ethics-review.md, dataset-model-artifact-registry.md |
| SSI-BENCH-LEAK | A project tunes prompts repeatedly on a fixed benchmark and reports final score as general performance. | contamination | Split policy, prompt-tuning history, held-out set, access date and benchmark version. | Freeze a dev set, reserve final evaluation, report tuning exposure and downgrade broad claims. | Public benchmark contamination may still be unknown. | experimental-rigor-evaluation-statistics.md, RDQ-W0-CLAIM |
| SSI-PROMPT-INJECT | A tool-using or RAG assistant follows instructions embedded in retrieved content instead of the user goal. | safety | Prompt assembly trace, retrieved chunk content, tool-call logs, failure taxonomy. | Treat retrieved content as untrusted, separate instructions from evidence, restrict tool permissions. | New instruction-injection variants can bypass tested templates. | Ch10, project-report-rubric.md |
| SSI-COPYRIGHT-DATA | A team fine-tunes on scraped text and plans to publish weights or generated samples. | copyright | Dataset origin, license or terms, redistribution permission, generated sample review. | Use permitted data, document terms, avoid redistributing restricted material or model artifacts. | License interpretation can require institutional review beyond course staff. | data-ethics-review.md, dataset-model-artifact-registry.md |
| SSI-DUAL-USE | A student proposes an agent that can automate security testing for arbitrary websites. | misuse | Intended scope, authorization evidence, tool permissions, allowed targets, abuse cases. | Restrict to owned sandbox targets, remove exploit details, require authorization and logging. | Even sandbox techniques can be adapted outside intended scope. | course-policies.md, academic-integrity-case-process.md |
| SSI-ACCESS-COST | A final project relies on paid APIs or GPUs and reports quality without cost or fallback. | access | Cost log, compute budget, CPU or smaller-model baseline, failure due to quota or latency. | Provide fallback, report cost per run, avoid grading advantage from private resources. | Some students may still face unequal hardware or API access. | compute-resource-guide.md, accessibility-student-support.md |
| SSI-LLM-JUDGE | A team uses an LLM judge as the only metric for open-ended answers. | evaluation | Judge prompt, model/version/date, pairwise calibration, human spot checks, disagreement examples. | Add human calibration or task metric, report judge bias and version boundary. | Judge behavior may drift across versions and prompts. | Ch11, experimental-rigor-evaluation-statistics.md |
| SSI-SAFETY-LOGS | A deployed demo stores raw prompts and model outputs for debugging. | privacy | Logging fields, retention period, access list, deletion policy, sample redaction check. | Minimize logs, remove secrets and personal data, set retention and staff-only access. | Users may still enter sensitive data despite warnings. | lecture-media-access-policy.md, data-ethics-review.md |

## Classroom Use

| use_id | use_case | student_output | grading_evidence |
| --- | --- | --- | --- |
| SSI-U-DISCUSS | 10-minute lecture discussion | Risk category, strongest evidence, residual risk. | Participation or reading recap field. |
| SSI-U-RECITATION | Recitation worksheet drill | Completed case schema plus one rewritten claim boundary. | Worksheet exit ticket and TA feedback. |
| SSI-U-PROPOSAL | Capstone proposal clinic | Risk register, mitigation, fallback and review owner. | Proposal or milestone review note. |
| SSI-U-FINAL | Final report check | Data, Ethics and Limitations subsection with evidence table. | Project report rubric and data ethics review. |
| SSI-U-REVIEW | Peer review or poster Q&A | One concrete risk question and one evidence-based suggestion. | Presentation peer-review rubric. |

## Assessment Rubric

| dimension | full_credit_evidence | common_failure |
| --- | --- | --- |
| Risk specificity | Names a concrete risk category, affected stakeholder and trigger condition. | Says only "ethical issue" or "safety problem". |
| Evidence quality | Cites data, source, log, metric, model card, failure case or human-review evidence. | Gives an opinion without verifiable evidence. |
| Mitigation realism | Proposes a change that can be implemented or audited within the project. | Claims the model will learn to be safe without a test or control. |
| Residual risk | States what remains uncertain or unsupported after mitigation. | Claims a risk is fully solved. |
| Course connection | Links to a chapter, reading question, project rubric or ethics review field. | Treats safety as unrelated to technical design. |

## Staff Review Workflow

1. Select 1-2 cases during Week 8-10 or whenever a project enters a high-impact domain.
2. Ask students to fill the case schema before discussing mitigation.
3. During project proposal review, require teams to map their largest risk to one `SSI-*` case or create a project-specific case row.
4. If multiple teams miss the same risk category, record an aggregate action in [Learning Analytics and Remediation Plan](learning-analytics-remediation-plan.md) and add a recap or clinic.
5. Before public archive, check that reports do not include private data, exploit steps, sensitive prompts, hidden tests or unauthorized artifacts.

## Release Checklist

- Case Analysis Schema includes case_id, scenario, primary_risk, evidence_to_collect, mitigation, residual_risk and course_link.
- Core Cases cover privacy, bias, safety, contamination, misuse, copyright, access, evaluation and governance-adjacent risks.
- Classroom Use maps cases to discussion, recitation, proposal, final report and peer review.
- Assessment Rubric covers specificity, evidence, mitigation, residual risk and course connection.
- Staff Review Workflow connects case failures to project review, learning analytics and public archive checks.
- Student site release excludes real sensitive data, exploit steps, private grading samples, hidden tests, reference_solution.py and real student submissions.
