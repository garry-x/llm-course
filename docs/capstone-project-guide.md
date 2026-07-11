# End-to-End LLM Capstone Guide

This guide turns the chapter exercises into one auditable engineering project. It is deliberately smaller than a production launch: the goal is not to train a frontier model, but to show that a learner can connect a task, data contract, model or pipeline, evaluation evidence, serving constraints, and a release decision. The Chinese edition is available as [端到端 LLM 结课项目指南](capstone-project-guide.zh.md).

## What This Capstone Proves

Individual exercises prove that a component works. A capstone should prove that the components work **together** for a defined decision. By the end, a reviewer should be able to answer all of the following without guessing:

- What user task and failure cost does the system address?
- What enters the system, what state is retained, and what output is allowed?
- Which baseline is being improved, and what single change is being tested?
- What evidence supports quality, safety, latency, cost, and reproducibility claims?
- Under what conditions would the team decline to deploy, roll back, or hand off to a human?

The work is compatible with a CPU-sized teaching model, mock engine, or small local corpus. Never use a small demo score to claim production-scale quality or safety.

## Choose One Bounded Project Track

Choose one primary track. All tracks must retain the common evidence contract below; the track only changes the main question and the most useful baseline.

| Track | Example question | Minimal baseline | Main chapters to reuse | Strong evidence is not |
|---|---|---|---|---|
| Adapted assistant | Does SFT or a small preference-data change improve a narrow answer style without harming a held-out task? | Base model or prompt-only behavior | Ch01, Ch06-Ch09, Ch11 | A lower training loss alone |
| Retrieval / tool assistant | Does retrieval, structured output, or one guarded tool improve grounded task completion within an SLO? | No-retrieval or free-form generation | Ch01, Ch08, Ch10-Ch11 | A valid JSON string alone |
| Structured NLP pipeline | Is extraction, reranking, or classification safer and cheaper than free-form generation for this output space? | Decoder-only prompting or a simple rule baseline | Ch02-Ch03, Ch08, Ch10-Ch11 | Token accuracy without field-level errors |

A useful scope has one user, one task family, one data source or simulator, and one explicit non-goal. For example: “Answer policy questions from a versioned handbook with citations; do not provide legal advice or execute external actions.” “Build a chatbot” is not yet a testable project question.

## Milestone Map: From Chapters to a System

| Milestone | Course connection | Deliverable | Acceptance signal |
|---|---|---|---|
| M0 — Project contract | Ch01, Ch11 | One-page task, risk, and measurement contract | A reader can state the allowed input/output and reject conditions |
| M1 — Data and interface | Ch01-Ch02, Ch07 | Versioned dataset or corpus manifest; tokenizer/template decision | Sample IDs, splits, token-length distribution, and leakage check are recorded |
| M2 — Reference path | Ch03-Ch06 | Smallest correct forward, retrieval, or extraction path | Shapes, masks, and one deterministic golden example pass |
| M3 — Improvement | Ch07-Ch09 | One controlled training, tuning, or pipeline change | Baseline and variant differ in one documented factor |
| M4 — Evaluation | Ch08, Ch11 | Frozen eval set, slice table, error taxonomy | Quality claim includes sample count, settings, uncertainty, and failures |
| M5 — Serving and safety | Ch08, Ch10 | Request contract, budget, validation, and fallback | Load, malformed-input, and unsafe-action drills have expected outcomes |
| M6 — Release decision | Ch07, Ch10-Ch11 | Evidence ledger, rollback rule, and final report | A reviewer can approve, reject, or request a bounded follow-up |

Do not postpone evaluation until M6. Start a tiny held-out set in M0, run the baseline in M2, and extend its slices only when the system changes.

## M0: Write the Project Contract Before Coding

Create a short `project_contract.md` with these fields. The wording matters less than making each field decidable.

| Field | Example of a useful statement | Common weak statement |
|---|---|---|
| User task | “Return one cited answer to a handbook question.” | “Make answers better.” |
| Output contract | “`answer`, `citations`, and `abstain_reason` must validate; citations must be from the retrieved corpus.” | “Return JSON.” |
| Non-goal | “No legal, medical, or account-changing action.” | Leaving scope implicit |
| Baseline | “Top-1 retrieval plus deterministic answer template.” | “Existing model.” |
| Success metric | “Citation-supported answer accuracy on the frozen test set.” | “The model feels useful.” |
| Guardrail / reject rule | “Abstain if no source clears the retrieval threshold; block tools outside an allow-list.” | “Prompt the model to be safe.” |
| Resource envelope | “P95 end-to-end latency under 3 seconds on this machine; request input under 4K tokens.” | “Fast enough.” |

The contract should name the owner of each external datum or tool, its version, and its permissions. Treat retrieved text and tool responses as untrusted input, not as instructions.

## M1: Build a Data, Token, and State Ledger

The data ledger connects Ch01’s tokenizer contract to Ch07’s training/evaluation split and Ch10’s context budget. Record at least:

- Dataset or corpus version, license/permission boundary, collection date, and content owner.
- Stable sample IDs; train/dev/test or retrieval-corpus/query split; a check for exact duplicates and answer leakage.
- Tokenizer, chat template, special-token IDs, maximum length, truncation direction, and length percentiles.
- For retrieval: document ID, chunk ID, source version, chunking rule, embedding or index version, and deletion/update path.
- For tools: schema version, permission class, timeout, retry limit, and whether results can enter later model context.

Use one small, hand-inspected golden sample to trace the full path: raw input → rendered prompt or query → token IDs → mask/position IDs → model/pipeline output → validator → user-facing response. This trace catches interface mismatches earlier than aggregate metrics.

## M2 and M3: Establish a Correct Reference Path, Then Change One Thing

Before optimizing, make the simplest path reproducible. Reuse course checks where appropriate:

| Layer | What to verify | Relevant course work |
|---|---|---|
| Token / template | Same text renders to the expected IDs and assistant-loss mask | Ch01, Ch02, Ch09 |
| Model path | Tensor shape, causal visibility, logit or loss parity on a fixed input | Ch03-Ch06 |
| Training / adaptation | Seed, optimizer/scheduler state, checkpoint resume, valid-token denominator | Ch07, Ch09 |
| Decoding | Sampling or constrained decoding parameters are logged with output | Ch08 |
| Pipeline | Retrieval rank, selected context, tool plan, validation result, and fallback are traceable | Ch10 |

Make one primary intervention per experiment: change the retrieval top-k, chunk rule, LoRA rank, data filter, decoding policy, or batching policy—not several at once. If a necessary configuration changes at the same time, label the comparison confounded and use it only for exploration, not a causal claim.

For training-related work, save the complete resume state: model, optimizer, scheduler, scaler when used, RNG state, consumed data/token position, and configuration. For serving-related work, version the model, prompt/template, corpus/index, schema, and engine configuration together.

## M4: Evaluate the Claim, Not Just the Demo

Freeze a test set before choosing the final setting. Separate the system into observable stages so an incorrect result has a location:

| System question | Minimum evidence | Useful failure slices |
|---|---|---|
| Is the answer or extraction correct? | Task-specific accuracy, EM/F1, pass rate, or calibrated human/judge rubric | short/long input, rare format, ambiguity, multilingual input |
| Is RAG finding evidence? | Recall@k/MRR/nDCG plus retrieved chunk IDs | no relevant chunk, stale source, duplicate chunk, position lost during packing |
| Is generation grounded and structured? | Citation support, schema validity, semantic validation, abstention correctness | valid JSON with wrong field, unsupported claim, partial answer, overly broad refusal |
| Is the system usable? | TTFT, end-to-end P50/P95, error rate, cost/request, token counts | long prompt, concurrent load, cache miss, timeout, retry storm |
| Is the safety boundary working? | Attack success, allowed-task completion, over-refusal, blocked-action rate | injected document, unauthorized tool, malformed schema, conflicting policy |

For a small evaluation set, report the number of examples and the uncertainty of the comparison. Repeated seeds, bootstrap intervals, or a transparent statement that the sample is too small for a deployment claim are all better than rounding a small change into certainty. Keep an error taxonomy with at least three categories chosen from data/interface, retrieval, generation/modeling, validation/tooling, safety, and serving.

## M5: Turn the Demo into a Bounded Service

Describe the request as a contract, not merely a prompt. At minimum specify input size limits, authentication/tenant boundary if relevant, output schema, validator behavior, tool allow-list, timeout/retry/cancellation behavior, and fallback or human-handoff path.

Run these drills before calling the project complete:

| Drill | Expected safe behavior | Evidence to save |
|---|---|---|
| Missing or malformed input | Reject with a machine-readable error; do not invent fields | Request, validation result, response code |
| Prompt injection in retrieved text | Treat the text as data; do not widen permissions or follow embedded instructions | Retrieved chunk, policy decision, trace |
| Invalid tool arguments | Block before execution; return repairable validation feedback | Parsed plan, schema/permission result |
| Retrieval miss / low confidence | Abstain, request clarification, or use a declared fallback | Threshold, selected fallback, user response |
| Longer input or concurrency burst | Apply admission control or degrade deliberately, not silently | Input/output tokens, queue time, TTFT/TPOT/P95 |
| Regression after a version change | Stop rollout or roll back when the predeclared gate fails | Baseline/variant report and rollback decision |

“The model usually follows the system prompt” is not a control. Validation, authorization, budgets, and observability must exist outside the model output.

## Evidence Ledger and Repository Layout

Keep the report backed by small, inspectable artifacts. This layout is only a suggestion; the important part is that every conclusion points to a versioned input and a reproducible command.

Start from the copyable [capstone template](../capstone-template/). It contains the contract, JSONL records, decision-report scaffold, and a local evidence checker; rename the `*.template.*` files only after replacing every placeholder with project-specific evidence.

```text
capstone/
  README.md                 # question, scope, baseline, commands, decision
  project_contract.md       # output/risk/resource contract
  configs/                  # model, template, index, and serving configs
  data_manifest.jsonl       # IDs, versions, split, permissions; no secret data
  eval/                     # frozen cases, rubric, slice definitions
  runs/                     # immutable run metadata and aggregate metrics
  traces/                   # redacted retrieval/tool/validation traces
  reports/                  # baseline-vs-variant table and failure analysis
  scripts/                  # deterministic preparation, eval, and load commands
```

Each run record should include commit ID, command, seed, hardware/runtime, model/checkpoint, tokenizer/template, data/index version, generation parameters, concurrency/load shape, start/end time, and metric definitions. Redact secrets and personal data; a reproducibility artifact must not become a privacy leak.

## Final Report and Grading Rubric

The final report can fit in 4–8 pages if it links to the evidence ledger. It should answer: question, scope and non-goals, baseline, intervention, data/interface contract, evaluation design, results by slice, failures, resource profile, safety/serving controls, decision, and limits.

| Dimension | 0 — missing | 1 — partial | 2 — convincing |
|---|---|---|---|
| Problem and boundary | Vague demo | Task stated but output/risk boundary incomplete | Decidable task, non-goals, failure cost, and reject rule |
| System correctness | Components described only | One happy-path example | Golden trace plus shape/schema/validator checks |
| Experiment design | Single final score | Baseline or metric present | Frozen eval, controlled change, slices, uncertainty, failure taxonomy |
| Engineering evidence | Unversioned screenshots | Some logs or code | Reproduction command, versions, resource metrics, rollback gate |
| Safety and operation | Prompt-only claim | Manual caution described | External validation, permissions, budgets, fallback, and adversarial drill |

A sound minimum is 7/10 with no zero in **System correctness**, **Experiment design**, or **Safety and operation**. A project that gets a strong demo result but cannot say what data/version/configuration produced it is incomplete.

## Definition of Done

Before submitting, verify all of these statements are true:

- A new reader can run the baseline and the final variant from documented commands.
- The report identifies one controlled change and does not claim causality from a confounded comparison.
- The frozen evaluation includes task-relevant slices and at least one observed failure category.
- The output, retrieval, or tool path is validated at the boundary where its result can cause harm.
- Latency/cost results state the model, hardware, input/output distribution, concurrency, and percentile.
- A concrete reject, rollback, or human-handoff rule exists and was exercised in a drill.
- The conclusion states both what the evidence supports and what it does not support.

Use this guide alongside the chapter assignments, [Written Derivation and Conceptual Question Bank](written-problem-set.md), and [Worked Example Pack](worked-example-pack.md). The capstone does not replace those exercises; it demonstrates that their formulas, tests, and diagnostics can support one end-to-end engineering judgment.
