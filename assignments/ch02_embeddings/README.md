# Ch02 Embedding and Position Encoding Assignment Tests

This directory organizes the programming exercises from Chapter 2 into automatically verifiable assignment entry points, covering TokenEmbedding, one-hot matrix multiplication form of embedding lookup, word vector co-occurrence statistics, skip-gram negative sampling, SGNS center vector gradient, shifted PMI, GloVe weighted least squares objective, cosine similarity, 3CosAdd analogy, SinusoidalEncoding, RoPE, and verification of RoPE relative position properties.

## File Description

| File | Purpose |
|------|---------|
| `starter.py` | Student starter code, containing TODOs that need implementation |
| `reference_solution.py` | Instructor reference implementation, used to verify the tests themselves |
| `tests.py` | `unittest` tests, covering shape, one-hot lookup equivalence, co-occurrence counts, SGNS loss, SGNS center gradient, shifted PMI, GloVe loss, cosine similarity, 3CosAdd, buffer, norm preservation, and relative position properties |

## Student Run Method

```bash
cp assignments/ch02_embeddings/starter.py assignments/ch02_embeddings/student_solution.py
# Edit student_solution.py to complete TODOs
STUDENT_MODULE=student_solution .venv/bin/python assignments/ch02_embeddings/tests.py
```

You can also directly load `starter.py` for testing:

```bash
STUDENT_MODULE=starter .venv/bin/python assignments/ch02_embeddings/tests.py
```

You can also directly verify the course's built-in reference implementation:

```bash
.venv/bin/python assignments/ch02_embeddings/tests.py
```

## Grading Rubric

| Item | Points | Criteria |
|------|:--:|---------|
| Written questions | 35 | Derive embedding parameter count, explain one-hot and lookup equivalence, compare word2vec/GloVe statistical objectives, derive SGNS positive/negative sample pair gradients with respect to center vector, PMI/shifted PMI, compute cosine similarity and 3CosAdd analogy, distinguish input embedding, contextualized hidden state, and output logits, prove self-attention permutation equivariance, derive RoPE dot product dependence on relative position |
| Programming parts | 55 | Implement `TokenEmbedding`, `embedding_lookup_as_matmul`, co-occurrence matrix, SGNS loss, SGNS center gradient, shifted PMI, GloVe weighted loss, cosine similarity, 3CosAdd, `SinusoidalEncoding`, `RoPE`, and relative position numerical verification |
| Analysis / style | 10 | Explain the interpretation boundary of input embedding nearest neighbors, RoPE extrapolation failure modes, odd head dimension rejection strategy, and dtype/device migration |