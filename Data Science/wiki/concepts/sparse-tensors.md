---
title: "Sparse tensors"
type: concept
sources: [tensor, review]
related: [tensors, software-hardware-codesign]
updated: 2026-05-02
---

# Sparse tensors

*When most of a tensor's elements are zero, storing only the non-zeros saves orders of magnitude in memory — three standard formats trade off construction complexity against operation efficiency.*

## Definition

A **sparse tensor** is one where the number of non-zero elements is much smaller than the total number of elements — formally, O(n) non-zeros in an n × n matrix. **Sparsity** is the proportion of zero-valued elements.

A **dense tensor** has most elements non-zero and is stored as a full array.

## Why it matters

A 10⁶ × 10⁶ dense float64 matrix requires ≈58 GB. If only ~10⁶ elements are non-zero (sparsity ~99.9999%), a dense representation is catastrophically wasteful. Sparse formats store only the non-zero values and their locations.

Real-world sparse data: social network adjacency matrices, recommendation system user-item matrices, fault detection sensor readings, NLP term-document matrices.

## Three sparse representations

### DOK — Dictionary of Keys

Store non-zeros in a hashmap: `(row, column) → value`.

```
{(0,0): 1.0,  (0,2): 5.0,
 (1,1): 3.0,  (1,5): 11.0}
```

- Easy to build and to update individual elements.
- Slow for arithmetic operations (hashmap overhead).

### COO — Coordinate List

Store non-zeros as a list of `(row, column, value)` triples.

```
[(0, 0, 1.0), (0, 2, 5.0), (1, 1, 3.0), (1, 5, 11.0)]
```

- Simple, format-agnostic, easy to convert to CSR.
- Not efficient for repeated row access.

### CSR — Compressed Sparse Row

Three arrays:
- **V** — non-zero values in row-major order.
- **COL_INDEX** — column index for each entry in V.
- **ROW_INDEX** — length (m + 1), where `ROW_INDEX[i]` is the index in V where row i starts.

To reconstruct row r:
```
row_start = ROW_INDEX[r]
row_end   = ROW_INDEX[r + 1]
values    = V[row_start : row_end]
cols      = COL_INDEX[row_start : row_end]
```

Example:
```
V         = [5, 8, 3, 6]
COL_INDEX = [0, 1, 2, 1]
ROW_INDEX = [0, 1, 2, 3, 4]  ← 4 rows, each has 1 non-zero
```

- Efficient for row slicing, matrix-vector products, and most numerical operations.
- The standard format in scientific computing (SciPy, BLAS).

## Comparison

| Format | Build | Row access | Arithmetic | Memory |
|---|---|---|---|---|
| DOK | Fast | O(1) | Slow | O(nnz) |
| COO | Fast | O(nnz) | Slow | O(nnz) |
| CSR | Moderate | O(k) for k non-zeros | Fast | O(nnz + m) |

## Examples in the syllabus

- Tensor s. 6–11: DOK, COO, CSR defined with worked examples.
- Review s. 32: sparse representations in the tensor section.

## Common exam framing

- "Describe the CSR sparse format. How do you extract row r?"
- "Give the DOK and COO representations of a 3×3 matrix with non-zeros at (0,0)=5, (1,2)=8."
- "Why is storing a social graph as a dense matrix inefficient?"

## See also

- [[tensors]]
- [[software-hardware-codesign]]
