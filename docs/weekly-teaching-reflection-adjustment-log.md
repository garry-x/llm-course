# Weekly Teaching Reflection and Adjustment Log

复核日期：2026-06-05

This log converts post-lecture evidence into concrete next-lecture changes. It complements [10 周 / 20 讲 Lecture Plan](lecture-plan.md), [Discussion Section and Office Hours Guide](discussion-office-hours-guide.md), [Course Operations and Improvement Log](course-operations-log.md), [Learning Analytics and Remediation Plan](learning-analytics-remediation-plan.md), [Teaching Observation and Course Evaluation Dossier](teaching-observation-course-evaluation.md), [Course Materials Index](course-materials-index.md), [Lecture Notes Quality and Review Standard](lecture-notes-quality-review.md), [Lecture Notes Review Ledger](lecture-notes-review-ledger.md), [Lecture Slide Sample Pack](lecture-slide-sample-pack.md), [Recitation Worksheet Pack](recitation-worksheet-pack.md), [Quiz and Checkpoint Guide](quiz-checkpoint-guide.md), [Assessment Item Analysis and Psychometrics Guide](assessment-item-analysis-psychometrics.md), [Participation and Feedback Guide](participation-feedback-guide.md), [Course Communication and Announcement Policy](course-communication-policy.md), [Course Errata and Correction Ledger](course-errata-correction-ledger.md), [Student FAQ and Troubleshooting Guide](student-faq-troubleshooting.md), and [Accessibility and Student Support Guide](accessibility-student-support.md).

Use this file after each lecture or weekly teaching block. It may enter the student site release because it records aggregate patterns and category-level actions only. It must not include student identifiers, raw survey comments, personal grades, accommodation details, integrity cases, hidden tests, `reference_solution.py`, private grading samples, or real student submissions.

## Reflection Schema

| field | required content | validation rule |
|-------|------------------|-----------------|
| reflection_id | Stable ID such as `WTR-2026-L03-MASK` | Must be unique within the offering |
| lecture_or_week | Lecture or week reference tied to `lecture-plan.md` | Must name the source lecture or weekly block |
| evidence_sources | Aggregate evidence IDs from the source table | Must cite at least one `WTR-` source |
| observed_pattern | Category-level learning, pacing, access, or materials pattern | No individual student detail |
| interpretation | Staff explanation of the likely cause | Must separate evidence from inference |
| next_adjustment | Specific patch to a lecture, worksheet, FAQ, assignment note, rubric, or project clinic | Must point to a student-visible or staff-visible artifact |
| student_message | Short category-level communication if students need to know the change | Must avoid private grade or support data |
| verification_signal | Next signal used to check whether the adjustment worked | Must be measurable in the next lecture, quiz, assignment, recap, or milestone |
| owner | Instructor or TA role responsible for the change | Must name a role rather than a student |
| status | `planned`, `in_progress`, `verified`, or `deferred` | Must be updated before the next weekly review |

## Evidence Sources

| source_id | source | use | privacy_boundary | linked_doc |
|-----------|--------|-----|------------------|------------|
| WTR-QUICK | Quick check or recap quiz aggregate | Identify concepts that need immediate recap | Aggregate item or concept pass rates only | `quiz-checkpoint-guide.md` |
| WTR-EXIT | Exit ticket theme coding | Capture the highest-frequency unclear points | Theme counts only; no raw comments | `participation-feedback-guide.md` |
| WTR-OH | Office hours and discussion section themes | Detect repeated failure modes outside lecture | Topic categories only; no names or private circumstances | `discussion-office-hours-guide.md` |
| WTR-ASSIGN | Public assignment failures and rubric notes | Connect lecture gaps to implementation errors | Public failure categories only; no hidden tests or submissions | `assignment-handout-pack.md` |
| WTR-READING | Reading recap and paper discussion evidence | Find source-boundary and paper-to-code misconceptions | Rubric category counts only | `reading-discussion-question-bank.md` |
| WTR-PROJECT | Capstone proposal or milestone aggregate | Detect project scoping, reproducibility, and metric risks | Project category patterns only; no team-sensitive details | `capstone-proposal-milestone.md` |
| WTR-PEER | Peer observation or course evaluation theme | Check pacing, clarity, accessibility, and active learning | Observation dimensions and coded survey themes only | `teaching-observation-course-evaluation.md` |
| WTR-ACCESS | Accessibility or support routing signal | Identify material format, caption, timing, or environment barriers | Category-level support need only; no accommodation detail | `accessibility-student-support.md` |

## Adjustment Action Bank

| action_id | use_when | student_visible_change | staff_record | verification_signal |
|-----------|----------|------------------------|--------------|---------------------|
| WTR-A-RECAP | A prerequisite concept blocks the next lecture | Add 5-10 minute recap at the next opening | Update `lecture-plan.md` and this log | Next quick check improves on the same concept |
| WTR-A-WORKSHEET | Students need practice rather than another explanation | Add or revise a discussion worksheet drill | Update `recitation-worksheet-pack.md` | Worksheet exit ticket shows fewer repeated errors |
| WTR-A-DEMO | A concept fails because students cannot see code behavior | Add a deterministic demo or dry-run trace | Update `demo-runbook.md` and source command | Demo run succeeds before class and students can trace output |
| WTR-A-FAQ | Many questions repeat after lecture or release | Add a FAQ entry with category-level answer | Update `student-faq-troubleshooting.md` | Fewer repeated office-hours questions next week |
| WTR-A-HANDOUT | A formula, shape convention, or source boundary is ambiguous | Patch notes, slide text, or assignment handout | Update materials index and review ledger | Follow-up item shows correct terminology or shape |
| WTR-A-RUBRIC | Errors reflect unclear scoring expectations | Clarify rubric criterion or self-check | Update grading guide or code quality rubric | Regrade and office-hours disputes decrease |
| WTR-A-PACING | Workload or lecture density exceeds the planned envelope | Move optional detail to reading, recitation, or 12-week path | Update workload pacing record | Exit tickets and workload survey themes improve |
| WTR-A-PROJECT | Capstone groups show repeated scoping or reproducibility risk | Schedule project clinic or release sample artifact | Update milestone guide or project dossier | Next milestone evidence meets reproducibility gate |
| WTR-A-SOURCE | A factual claim, benchmark, or API detail is uncertain or changed | Add source card or correction notice | Update source verification and errata ledgers | Claim audit status closes with dated source |
| WTR-A-ACCESS | Students report material-format, timing, caption, or environment barrier | Provide alternate format, caption, transcript, or setup path | Update support and media access records | Barrier category is resolved or routed |

## Current Reflection Records

| reflection_id | lecture_or_week | evidence_sources | observed_pattern | next_adjustment | verification_signal | status |
|---------------|-----------------|------------------|------------------|-----------------|---------------------|--------|
| WTR-2026-L02-ROPE | Week 1 Lecture 2 | WTR-QUICK, WTR-EXIT | Students can state norm preservation but overgeneralize it to semantic preservation | Add a two-vector RoPE counterexample to lecture recap and worked example references | Next RoPE quick check distinguishes norm, dot product, and semantic claim boundaries | planned |
| WTR-2026-L03-MASK | Week 2 Lecture 1 | WTR-QUICK, WTR-OH | Causal mask failures cluster around broadcast shape rather than softmax itself | Add a worksheet drill that traces `[B, H, T, T]` mask expansion before attention scores | Recitation exit ticket shows correct mask dimension naming | in_progress |
| WTR-2026-L05-GQA | Week 3 Lecture 1 | WTR-EXIT, WTR-ASSIGN | GQA and MQA memory savings are understood qualitatively but KV-cache byte estimates are inconsistent | Add a board estimate using `B, T, H_kv, d_head, dtype_bytes` and link it to Ch10 serving | Next assignment explanation uses the same variable names and units | planned |
| WTR-2026-L09-TRAIN | Week 5 Lecture 1 | WTR-ASSIGN, WTR-OH | Training-loop errors combine device mismatch, missing `zero_grad`, and unchecked validation mode | Add a live debugging checklist before optimizer discussion | Public failure categories drop below the remediation threshold | verified |
| WTR-2026-L15-EVAL | Week 8 Lecture 1 | WTR-READING, WTR-PEER | Students mix task metric names with model-quality claims without dataset or split boundaries | Add a metric-card mini case before classic NLP evaluation examples | Reading recap rubric shows source and split boundaries | deferred |
| WTR-2026-L18-SLO | Week 9 Lecture 2 | WTR-PROJECT, WTR-EXIT | P95 latency, tokens/s, and cost are reported without separating prefill and decode | Add a capstone clinic table for TTFT, TPOT, throughput, and concurrency assumptions | Project milestone reports include metric configuration and measurement window | planned |

## Next-Lecture Patch Template

```text
reflection_id:
lecture_or_week:
evidence_sources:
observed_pattern:
interpretation:
next_adjustment:
student_message:
verification_signal:
owner:
status:
```

## Staff Workflow

1. Collect aggregate evidence within 24 hours from quick checks, exit tickets, office hours, public assignment failure categories, reading recap categories, project milestones, or peer observation.
2. Classify the pattern using [Concept Mastery and Misconception Map](concept-misconception-map.md) and [Topic Dependency and Spiral Review Map](topic-dependency-map.md) before choosing a fix.
3. Choose one primary action from the Adjustment Action Bank and assign an owner. If the issue is a factual or source error, route it to [Course Errata and Correction Ledger](course-errata-correction-ledger.md) and [External Source Verification Guide](external-source-verification.md).
4. Update the affected lecture, recitation, FAQ, handout, rubric, source map, or project guide before the next related class session.
5. Communicate only the student-visible category-level change through [Course Communication and Announcement Policy](course-communication-policy.md). If the adjustment affects scoring, route the staff record through [Gradebook and LMS Operations Guide](gradebook-lms-operations.md) and the regrade policy.
6. Verify the change with the next quick check, exit ticket, assignment failure category, reading rubric, project milestone, or office-hours theme, then mark the record `verified` or carry a dated follow-up.

## Release Checklist

- Reflection Schema, Evidence Sources, Adjustment Action Bank, Current Reflection Records, Next-Lecture Patch Template, and Staff Workflow are present.
- Every current record has an evidence source, next adjustment, verification signal, owner through role assignment, and status.
- Privacy boundary excludes student identifiers, raw survey comments, personal grades, accommodation details, integrity cases, hidden tests, `reference_solution.py`, private grading samples, and real student submissions.
- Student site release includes this aggregate template but excludes staff-only raw evidence and private grading artifacts.
- Links to operations, analytics, lecture planning, discussion, FAQ, accessibility, errata, and source-verification documents are current.
