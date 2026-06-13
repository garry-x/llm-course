# Ch03 Scaled Dot-Product Attention Homework Tests

This directory organizes the programming exercises from Chapter 3 into automatically verifiable homework entry points, covering QKV projection, Scaled Dot-Product Attention, self-attention permutation equivariance, softmax/attention backpropagation, Q/K/V hand-written gradients, attention entropy, attention score memory estimation, Causal Mask, causal+padding mask composition, causal attention, and attention heatmap functions.

## File Description

| File | Purpose |
|------|---------|
| `starter.py` | Student starter code, containing TODOs to be implemented |
| `reference_solution.py` | Instructor reference implementation, used to verify the tests themselves |
| `tests.py` | `unittest` tests, covering shape, scaling, mask, permutation equivariance, softmax Jacobian, attention logits gradient, Q/K/V gradients, attention entropy, attention score memory, causal constraints, padding key masking, and visualization return values |

## Student Run Method

```bash
cp assignments/ch03_attention/starter.py assignments/ch03_attention/student_solution.py
# Edit student_solution.py to complete TODOs
STUDENT_MODULE=student_solution .venv/bin/python assignments/ch03_attention/tests.py
```

You can also directly have the tests load `starter.py`:

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch03_attention/tests.py
```

You can also directly verify the course's built-in reference implementation:

```bash
.venv/bin/python assignments/ch03_attention/tests.py
```

## Grading Rubric

| Item | Points | Criteria |
|------|:--:|---------|
| Written questions | 35 | Derivation of `1/sqrt(d_k)` scaling, self-attention permutation equivariance, softmax Jacobian, chain rule from attention logits to Q/K/V, attention entropy, reason for adding mask before softmax, shape broadcasting of causal mask and padding mask, NaN risk of all-masked rows, complexity, and heatmap interpretation boundaries |
| Programming parts | 55 | Implementation of QKV projection, scaled dot-product attention, numerical verification of permutation equivariance, softmax/attention backward helpers, Q/K/V gradient helper, attention entropy, attention score memory estimation, causal mask, causal+padding mask composition, and attention visualization |
| Analysis / style | 10 | Explanation of mask numerical stability, difference between padding key and padding query, applicable scope of attention heatmap, and common shape bugs |