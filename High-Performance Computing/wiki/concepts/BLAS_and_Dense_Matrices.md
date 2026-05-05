---
title: "BLAS and Dense Matrices"
tags: [hpc, week-9, matrices, dense, linear-algebra]
date: 2026-05-05
---

# BLAS and Dense Matrices

## Dense Matrices
In a dense matrix, most or all of the elements are non-zero. They can be stored efficiently in contiguous memory, allowing for predictable and highly optimized access patterns, making them suitable for heavily compute-bound operations.

## BLAS (Basic Linear Algebra Subprograms)
BLAS is a standardized interface for basic vector and matrix operations, serving as low-level building blocks for linear algebra libraries (such as numpy). Using optimized versions of BLAS (like OpenBLAS or Intel MKL) can significantly improve application performance.

BLAS routines are categorized into three levels, which have different characteristics regarding [Arithmetic Intensity](../concepts/Arithmetic_Intensity_and_Roofline_Model.md):

### Level 1: Vector-Vector Operations
*   **Example:** $y \leftarrow \alpha x + y$ (Dot product or scalar-vector multiplication and addition).
*   **Performance:** Requires $O(N)$ operations and $O(N)$ memory transfers.
*   **Arithmetic Intensity:** $\sim O(1)$. It is independent of the vector length and generally memory-bound.

### Level 2: Matrix-Vector Operations
*   **Example:** $y \leftarrow \alpha Ax + \beta y$.
*   **Performance:** Requires $O(N^2)$ operations and $O(N^2)$ memory transfers.
*   **Arithmetic Intensity:** $\sim O(1)$. Independent of the matrix size and generally memory-bound.

### Level 3: Matrix-Matrix Operations
*   **Example:** $C \leftarrow \alpha AB + \beta C$ (e.g., General Matrix Multiplication or DGEMM).
*   **Performance:** Requires $O(N^3)$ operations and $O(N^2)$ memory transfers.
*   **Arithmetic Intensity:** $\sim O(N)$. The arithmetic intensity increases as the matrix size increases, allowing these operations to become heavily compute-bound and very efficient on modern hardware.

### Naming Convention
BLAS routines follow a standard naming convention indicating:
1.  Precision (e.g., `D` for double precision).
2.  Type of matrix (e.g., `GE` for general matrix).
3.  Operation (e.g., `MM` for matrix-matrix multiplication).
*Example:* `DGEMM` represents Double precision, General Matrix, Matrix-Matrix multiplication.