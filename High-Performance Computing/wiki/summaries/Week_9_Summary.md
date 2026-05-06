---
title: "Week 9 Summary: Linear Algebra and Matrices"
tags: [summary, hpc, week-9, linear-algebra]
date: 2026-05-05
---

# Week 9 Summary: Linear Algebra and Matrices

## Overview
This week introduces the role of linear algebra in High-Performance Computing, focusing on the differences between dense and sparse matrices and the libraries used to optimize operations on them.

## Key Topics

*   **Linear Algebra in HPC:** Many advanced numerical methods for solving PDEs (like finite volume and finite element methods) and elliptic equations (like the Poisson equation) require solving large systems of linear equations.
*   **Dense vs. Sparse Matrices:**
    *   **[Dense Matrices](../concepts/BLAS_and_Dense_Matrices.md):** Most elements are non-zero. They can be stored in contiguous memory for efficient access, making them well-suited for high-performance arithmetic operations.
    *   **[Sparse Matrices](../concepts/Sparse_Matrices_and_CSR.md):** Most elements are zero. Storing them entirely is inefficient, so alternative formats like the Compressed Sparse Row (CSR) format are used to save memory and computational time, though they require indirect memory addressing.
*   **[BLAS (Basic Linear Algebra Subprograms)](../concepts/BLAS_and_Dense_Matrices.md):** A standardized interface for basic vector and matrix operations, crucial for performance.
    *   **Level 1 (vector-vector):** Arithmetic intensity $O(1)$.
    *   **Level 2 (matrix-vector):** Arithmetic intensity $O(1)$.
    *   **Level 3 (matrix-matrix):** Arithmetic intensity $O(N)$, which increases with matrix size, allowing for high efficiency.
*   **HPC Benchmarks:**
    *   **HPL (High Performance Linpack):** Uses a dense linear algebra workload, heavily compute-bound, achieving a large fraction of the peak performance.
    *   **HPCG (High Performance Conjugate Gradients):** Uses a sparse linear algebra workload to solve a 3D Poisson equation. Memory-bound, achieving a much lower fraction of peak performance.