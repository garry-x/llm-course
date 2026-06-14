# Ch04 Multi-Head Attention / GQA / MLA Homework Tests

This directory organizes the programming exercises from Chapter 4 into auto-gradable homework entry points, covering MHA, single-head parameter equivalence, GQA KV head repetition, GQA head mapping, simplified MLA, MLA matrix absorption equivalence, KV Cache size calculation, and cross-layer memory budget.

## File Descriptions

| File | Purpose |
|------|---------|
| `starter.py` | Starter code with TODOs |
| `reference_solution.py` | Instructor reference implementation, used to verify the tests themselves |
| `tests.py` | `unittest` tests covering shape, mask, parameter count, KV head repeat, GQA head mapping, MLA latent score equivalence, cache compression ratio, and batch/layer/dtype memory budget |

## Run Instructions

```bash
cp assignments/ch04_multihead/starter.py assignments/ch04_multihead/student_solution.py
# Edit student_solution.py to complete TODOs
STUDENT_MODULE=student_solution .venv/bin/python assignments/ch04_multihead/tests.py
```

You can also directly load `starter.py` for testing:

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch04_multihead/tests.py
```

Or directly verify the built-in course reference implementation:

```bash
.venv/bin/python assignments/ch04_multihead/tests.py
```

## Grading Rubric

| Item | Points | Criteria |
|------|:--:|---------|
| Written questions | 35 | Calculate MHA parameter count, compare MHA/MQA/GQA/MLA KV cache, write Q head to KV head mapping, derive MLA K decompression matrix absorption equivalence, explain head redundancy, RoPE and latent cache boundary, and incorporate batch/layers/dtype into memory budget |
| Programming parts | 55 | Implement MHA, single-head comparison, `repeat_kv_heads`, GQA, GQA head mapping, simplified MLA, MLA absorbed scores, KV cache analysis, and cross-layer memory budget |
| Analysis / style | 10 | Explain head grouping, head redundancy, latent cache, mask broadcast, and implementation complexity trade-offs |