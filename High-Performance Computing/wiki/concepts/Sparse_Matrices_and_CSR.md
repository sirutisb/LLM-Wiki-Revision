---
title: "Sparse Matrices and CSR"
tags: [hpc, week-9, matrices, sparse, data-structures]
date: 2026-05-05
---

# Sparse Matrices and CSR

## Sparse Matrices
In a sparse matrix, most of the elements are zero. Sparse matrices frequently arise in scientific applications, such as calculating pairwise interactions in finite element methods or finding iterative solutions to partial differential equations on large grids.

Storing every element of a sparse matrix (including the zeros) is inefficient in terms of memory footprint and unnecessary computation. Instead, sparse matrices use specialized storage formats.

## Compressed Sparse Row (CSR) Format
The Compressed Sparse Row (CSR) format is a widely used general format for efficiently storing sparse matrices. It makes no assumptions about the sparsity pattern. 

The matrix is stored using three one-dimensional arrays. For a matrix with `nrow` rows and `nnz` non-zero elements, the arrays are:

1.  **`val(nnz)`**: The actual non-zero floating-point values.
2.  **`col_ind(nnz)`**: The column index for each non-zero value.
3.  **`row_ptr(nrow + 1)`**: The index in the `val` and `col_ind` arrays where each row starts. By convention, the last element is set to `nnz + 1`.

### Memory Footprint
A full $N_{row} \times N_{col}$ dense matrix requires storing $N_{row} \times N_{col}$ values.
The CSR format only stores $2 \times nnz + N_{row} + 1$ values. This drastically reduces the size if $nnz \ll N_{row} \times N_{col}$.

### Addressing Overhead
While CSR saves space, extracting elements requires **indirect addressing** (using `col_ind` and `row_ptr` to locate the `val`), which is inherently slower than the direct addressing used for dense matrices in contiguous memory.

### Other Formats
CSR is not the only format. If the matrix has a particular structure (e.g., banded matrices or dense blocks within a sparse matrix), other specialized sparse formats might be more efficient. CSR is implemented as a general-purpose format in libraries like PETSc.