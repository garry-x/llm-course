# Python and PyTorch Review Session

This handout is used for Week 1 Python Review Session and Week 2 PyTorch Tutorial Session. It pairs with the [Math and PyTorch Prerequisite Review](math-prerequisites.md) to help learners directly connect Python, tensor shape, autograd, and test debugging skills to Transformer code exercises.

This course schedules a Python Review Session in Week 1 and a PyTorch Tutorial Session in Week 2, combining both reviews into a portable handout: you first confirm the environment and Python helpers, then proceed to PyTorch tensors, `nn.Module`, loss, autograd, and assignment submission logs.

## Session Goals

| Session | Duration | Target Audience | Deliverable |
|---------|:--:|----------|----------|
| Python Review Session | 80-90 minutes | Learners who are close to the Python prerequisite boundary, transitioning from another language, or have not completed the Ch01 helper | Able to implement pair counting, non-overlapping merge, file reading, and exception boundaries |
| PyTorch Tutorial Session | 80-90 minutes | Learners who are close to the PyTorch prerequisite boundary, unstable with shape derivation, or have not completed the Ch02 starter | Able to explain `[B,T,D]` to logits, compute next-token CE, and locate a failing test |

## Prerequisites

Run from the repository root:

```bash
.venv/bin/python -c "import sys, torch; print(sys.version.split()[0], torch.__version__, torch.cuda.is_available())"
.venv/bin/python run_assignment_tests.py
STUDENT_MODULE=starter .venv/bin/python assignments/ch01_bpe/tests.py
STUDENT_MODULE=starter .venv/bin/python assignments/ch02_embeddings/tests.py
```

If `.venv/bin/python run_assignment_tests.py` fails, first record `Python executable`, `PyTorch version`, `CUDA available`, and the first failing item according to the Environment and Reproducibility Guide.

## Python Review Session Agenda

| Time | Topic | Activity | Deliverable |
|------|------|------|------|
| 0-10 min | Environment smoke test | Run `.venv/bin/python -c "import sys, torch; ..."` | Record interpreter, PyTorch version, and working directory |
| 10-25 min | Functions and tests | Read helper tests in `assignments/ch01_bpe/tests.py` | Write input, output, and empty boundary for `_get_stats` |
| 25-45 min | Dictionaries and pair counting | Hand-write `count_pairs(tokens)` | Handle empty list, single element, and duplicate pairs |
| 45-65 min | Non-overlapping merge | Hand-calculate then implement for `[1,1,1]` and pair `(1,1)` | Explain why overlapping merge is not allowed |
| 65-80 min | Files, exceptions, and logs | Read non-empty lines, preserve first failure traceback | Submit minimal run log |
| 80-90 min | Exit ticket | Write one question you're still unsure about | Enter office hours triage |

### Python Drill

Learners should be able to explain without reference solutions:

- Why `_get_stats([])` and `_get_stats([1])` both return an empty dictionary.
- Why `list.append(x)` modifies in place, while `list + [x]` creates a new list.
- Why default parameters should not be written as `items=[]`.
- When to raise `ValueError` or `KeyError` instead of silently returning an empty result.
- Why the first traceback should be preserved when a test fails, rather than only the last line.

## PyTorch Tutorial Session Agenda

| Time | Topic | Activity | Deliverable |
|------|------|------|------|
| 0-10 min | Tensor shape contract | Write `[B,T] -> [B,T,D] -> [B,T,V]` | Shape trace |
| 10-25 min | Embedding lookup | Compare `nn.Embedding` and `one_hot @ E` | Explain lookup equivalence |
| 25-40 min | Linear projection | Derive logits shape given `x @ W` | Parameter count and output shape |
| 40-55 min | Next-token CE | Flatten logits/labels or use equivalent implementation | Loss input/output explanation |
| 55-70 min | Autograd | Execute forward, loss, backward; check `.grad` | Gradient flow explanation |
| 70-85 min | Debug drill | Locate dtype, device, contiguous, mask, or shape errors | First failing test and fix hypothesis |
| 85-90 min | Exit ticket | Write one PyTorch bug pattern | FAQ or office hours record |

### PyTorch Drill

Mandatory checklist:

- Shape trace: The path from [B,T,D] to logits must be explainable in both text and tensor dimensions.
- `input_ids` dtype should be integer token ids; embedding output is a floating tensor.
- When computing CE with logits `[B,T,V]` and labels `[B,T]`, the batch/time dimensions must align.
- `.reshape` is more suitable than `.view` for potentially non-contiguous tensors.
- `model.train()` / `model.eval()` affects dropout or some normalization behavior.
- After `loss.backward()`, check that key parameters have `.grad is not None`, but do not treat identical gradient values as a correctness indicator.

## Common Failures and Handling

| Failure Mode | Typical Symptom | Handling |
|----------|----------|------|
| Wrong working directory | `FileNotFoundError` or cannot find assignments | Return to repository root to run commands |
| Wrong module selection | Tests import the wrong file | Use `STUDENT_MODULE=starter` or the module name required by the submission package |
| dtype error | Embedding reports token id type error | Use integer tensor for token ids, floating tensor for logits/loss |
| Shape error | Batch/time misalignment after CE flatten | Write `[B,T,V] -> [B*T,V]` and `[B,T] -> [B*T]` |
| Device error | CPU/GPU tensor mixing | Public tests in this course default to CPU; GPU is only for extension |
| Silently swallowing exceptions | Test fails but no traceback | Preserve the first failure traceback and command |

## Submission Template

```text
Session:
Command:
Working directory:
Python executable:
Python version:
PyTorch version:
CUDA available:
First failing test:
Shape trace:
Fix hypothesis:
Question for office hours:
```
