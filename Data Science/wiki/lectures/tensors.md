---
title: "Lecture: Tensors"
type: lecture
sources: [tensor, review]
related: [tensors, sparse-tensors, software-hardware-codesign]
updated: 2026-05-02
---

# Lecture: Tensors

*Data is tensors — understanding orders, dense vs sparse, and the three sparse representations that avoid storing millions of zeros.*

## Slide-by-slide notes

- **(s. 2–3)** **[[tensors|Tensor orders]]**:
  - 0-order: **scalar** (single number).
  - 1-order: **vector** (1D array of features).
  - 2-order: **matrix** (2D array — rows × columns).
  - 3-order and above: **tensor** (general term for higher-order arrays).
  - Real-world data shapes:
    - Vector data: features.
    - Time series: features × timestamps.
    - Image: width × height × channels (e.g. RGB = 3 channels).
    - Video: frames × width × height × channels.
- **(s. 4–5)** **[[sparse-tensors|Sparse tensors]]**:
  - A sparse tensor has most elements equal to zero. Formal: #non-zero elements ≈ O(n) for an n × n tensor.
  - Dense tensor: most elements are non-zero.
  - **Sparsity**: proportion of zero-valued elements.
  - Real-world data is frequently very sparse (social graphs, fault sensors).
  - A 10⁶ × 10⁶ matrix of 64-bit floats would need ~58 GB — storing zeros is wasteful.
- **(s. 6)** **DOK — Dictionary of Keys**:
  - Stores only non-zero values in a dictionary keyed by (row, column).
  - Example: `{(0,0): 1.0, (0,2): 5.0, (1,1): 3.0, (1,5): 11.0}`.
  - O(nnz) storage where nnz = number of non-zero elements.
- **(s. 7)** **COO — Coordinate List**:
  - Stores non-zero values as a list of `(row, column, value)` tuples.
  - Example: `[(0,0,1.0), (0,2,5.0), (1,1,3.0), ...]`.
  - Simple to construct; easy to convert to other formats.
- **(s. 8–11)** **CSR — Compressed Sparse Row**:
  - Three arrays: `V` (non-zero values), `COL_INDEX` (column index per non-zero), `ROW_INDEX` (length m+1, where m = rows).
  - `ROW_INDEX[i]` = index in V where row i starts; `ROW_INDEX[i+1]` = where row i ends.
  - To reconstruct row r: `row_start = ROW_INDEX[r]`, `row_end = ROW_INDEX[r+1]`, then `V[row_start:row_end]` are the values, `COL_INDEX[row_start:row_end]` are the column indices.
  - Efficient for row-oriented operations and matrix-vector multiplication.

## Key takeaways

1. **Everything is a tensor** — scalar, vector, matrix are special cases (orders 0, 1, 2).
2. **Real data shapes**: vector = features, image = W×H×C, video adds the frames dimension.
3. **Sparse vs dense** — sparse tensors have most elements zero; storing them densely wastes memory.
4. **Three sparse formats**: DOK (dict of keys), COO (coordinate list), CSR (compressed rows). CSR is the most efficient for row-wise computation.
5. **CSR mechanics**: `ROW_INDEX[r]` to `ROW_INDEX[r+1]` gives the slice of `V` and `COL_INDEX` for row r.

## Concepts introduced

- [[tensors]]
- [[sparse-tensors]]

## Open questions / things to clarify

- CSC (Compressed Sparse Column) — the column-oriented equivalent of CSR — is not mentioned in the slides.

## See also

- [[software-hardware-codesign]]
- [[communication-patterns]]
