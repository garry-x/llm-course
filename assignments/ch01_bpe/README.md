# Ch01 BPE Tokenizer Homework Test

This directory organizes the programming exercises from Chapter 1 into an auto-gradable homework entry point. The goal is not to replace the chapter explanation, but to give learners a submission standard similar to university course assignments.

## File Description

| File | Purpose |
|------|---------|
| `starter.py` | Starter code with TODOs |
| `reference_solution.py` | Instructor reference implementation, used to verify the tests themselves |
| `tests.py` | `unittest` tests, covering `_get_stats`, `_merge`, `train`, `encode`, `decode`, BPE merge trace, tokenizer statistics report, and grouped token cost comparison |

## Run Instructions

```bash
cp assignments/ch01_bpe/starter.py assignments/ch01_bpe/student_solution.py
# Edit student_solution.py to complete TODOs
STUDENT_MODULE=student_solution .venv/bin/python assignments/ch01_bpe/tests.py
```

You can also directly load `starter.py` for testing:

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch01_bpe/tests.py
```

You can also directly verify the built-in reference implementation from the course:

```bash
.venv/bin/python assignments/ch01_bpe/tests.py
```

## Grading Rubric

| Item | Points | Criteria |
|------|:--:|---------|
| Written questions | 30 | Explain byte-level BPE reversibility, token savings per merge step, frequency-based merge compression heuristic, impact of tie-breaking on vocabulary, trade-offs between vocabulary size and sequence length/embedding parameter count/multilingual and domain text cost |
| Programming parts | 60 | Implement `_get_stats`, `_merge`, `train`, `encode`, `decode`, `bpe_training_trace`, `tokenizer_report`, and `tokenizer_group_report`, passing tests for mixed text, emoji, multi-byte UTF-8 round trip, merge trace, and grouped token cost statistics |
| Analysis / style | 10 | Report at least 2 tokenizer failures or edge cases, and compare compression rate, reversibility, special tokens, and domain text segmentation |
