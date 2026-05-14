---
title: "Week 9 Practice Questions: BLAS and Sparse Matrices"
tags: [hpc, week-9, blas, sparse, csr, practice]
date: 2026-05-14
---

# Week 9 Practice Questions: BLAS and Sparse Matrices

**Source concepts:** [BLAS and Dense Matrices](../wiki/concepts/BLAS_and_Dense_Matrices.md) · [Sparse Matrices and CSR](../wiki/concepts/Sparse_Matrices_and_CSR.md) · [Arithmetic Intensity and the Roofline Model](../wiki/concepts/Arithmetic_Intensity_and_Roofline_Model.md)

---

## Section A: Short Answer and Definitions

### Q1. Define the three levels of BLAS and give one example operation for each.

**Model Answer:**

| Level       | Category      | Example operation                   | FLOPs | Memory | AI   |
| :---------- | :------------ | :---------------------------------- | :---- | :----- | :--- |
| **Level 1** | Vector–vector | `y ← αx + y` (DAXPY) or dot product | O(N)  | O(N)   | O(1) |
| **Level 2** | Matrix–vector | `y ← αAx + βy` (DGEMV)              | O(N²) | O(N²)  | O(1) |
| **Level 3** | Matrix–matrix | `C ← αAB + βC` (DGEMM)              | O(N³) | O(N²)  | O(N) |

Key marking points:
- All three levels identified with correct category (1 mark each)
- Correct example for each level (1 mark each)
- Correct FLOPs and memory scaling (1 mark each)

---

### Q2. Decode the BLAS routine name `DGEMM`. What does each letter/pair of letters represent?

**Model Answer:**

- `D` — **Double precision** floating point (64-bit)
- `GE` — **General** matrix (no special structure assumed, e.g. not symmetric or triangular)
- `MM` — **Matrix–Matrix** multiplication

The full operation is: `C ← αAB + βC` where A, B, C are general double-precision matrices.

---

### Q3. What are the three arrays that define the CSR (Compressed Sparse Row) format? For a matrix with `nrow` rows and `nnz` non-zero elements, state the size of each array.

**Model Answer:**

1. **`val(nnz)`** — stores the actual non-zero floating-point values. Size: `nnz`.
2. **`col_ind(nnz)`** — stores the column index of each non-zero value. Size: `nnz`.
3. **`row_ptr(nrow + 1)`** — stores the index into `val` and `col_ind` where each row begins. By convention, `row_ptr(nrow+1) = nnz + 1` (1-indexed). Size: `nrow + 1`.

---

### Q4. What is the memory footprint (in number of stored values) of:
**(a)** A dense N × N matrix?
**(b)** The same matrix stored in CSR format with `nnz` non-zeros?

**Model Answer:**

**(a)** Dense: **N²** values. Every element is stored, including zeros.

**(b)** CSR: **2·nnz + N + 1** values.
- `val`: nnz values
- `col_ind`: nnz values
- `row_ptr`: N + 1 values

CSR is more efficient when `nnz << N²`, i.e. when the matrix is genuinely sparse.

---

### Q5. Why is BLAS Level 3 more efficient than BLAS Levels 1 and 2 on modern hardware?

**Model Answer:**

BLAS Level 3 performs O(N³) floating-point operations while only requiring O(N²) memory transfers. This gives an arithmetic intensity of O(N), which **grows with problem size**. For large N, the operation becomes heavily **compute-bound**, allowing the CPU to spend most time executing FLOPs rather than waiting for memory.

In contrast, Levels 1 and 2 both have arithmetic intensity O(1) — independent of N — so they are **memory-bandwidth-bound** regardless of problem size.

Additionally, optimised BLAS Level 3 implementations (e.g. OpenBLAS, Intel MKL) use **cache blocking (loop tiling)** to keep data in fast L1/L2 cache, further exploiting the high arithmetic intensity.

---

### Q6. What is `SpMV`? Why is it typically slower (in terms of fraction of peak performance achieved) than dense matrix–matrix multiplication?

**Model Answer:**

**SpMV** is Sparse Matrix–Vector Multiplication: `y = Ax` where A is stored in a sparse format such as CSR.

It is slower relative to peak because:
1. **Low arithmetic intensity:** each non-zero element is multiplied once and added once (2 FLOPs), but requires loading the value, its column index, and a vector element — many bytes per FLOP.
2. **Indirect memory addressing:** CSR requires using `col_ind` to gather elements of the input vector `x`. These accesses are non-contiguous and defeat hardware prefetchers.
3. **No data reuse:** each non-zero is used exactly once; there is no opportunity for cache reuse analogous to DGEMM's O(N) data reuse.

Typical SpMV achieves ~5–10% of peak performance; DGEMM can exceed 80–90%.

---

### Q7. Describe what "indirect addressing" means in the context of CSR sparse matrix storage and explain why it is slower than direct addressing.

**Model Answer:**

In CSR format, to access the value at position (i, j), you must:
1. Look up `row_ptr[i]` to find where row i starts in `val`.
2. Scan `col_ind` entries from `row_ptr[i]` to `row_ptr[i+1]-1` to find the entry for column j.
3. Use the found index to retrieve `val[index]`.

This is **indirect addressing** — you follow a chain of pointers/indices rather than computing a memory offset directly. It is slower because:
- It produces **irregular, non-contiguous memory access patterns** that cannot be predicted or prefetched by the CPU.
- It causes frequent **cache misses** since the next address to access is only known after reading the current one.
- Dense matrix storage uses `A[i][j] = base + i*N + j` (direct formula) — a single predictable, sequential access pattern that prefetchers can exploit.

---

### Q8. When is it beneficial to use sparse storage over dense storage? Give a rule of thumb for the sparsity threshold.

**Model Answer:**

Sparse storage is beneficial when the fraction of non-zero elements is **well below ~10%** of the total N × N elements (i.e. nnz < ~0.1·N²), as this is when:
- The memory saving from not storing zeros exceeds the overhead of the extra index arrays (`col_ind` and `row_ptr`).
- The computational saving from skipping zero multiplications exceeds the cost of indirect addressing.

For a 1000×1000 matrix (1,000,000 elements), sparse storage is clearly beneficial if there are fewer than ~100,000 non-zeros.

**Typical sources of sparse matrices:** finite element/finite difference PDE discretisations (each grid point only connects to its direct neighbours), molecular dynamics pairwise interactions in large molecules, graph adjacency matrices for large social networks.

---

## Section B: CSR Encoding and Decoding

### Q9. Encode the following 4×4 sparse matrix in CSR format. Use 1-based indexing. Show your working clearly.

```
A = [ 5  0  0  2 ]
    [ 0  0  3  0 ]
    [ 0  7  0  0 ]
    [ 4  0  6  8 ]
```

**Model Answer:**

**Step 1 — Identify all non-zeros (reading row by row):**

| Entry | Row | Col | Value |
|:------|:----|:----|:------|
| 1 | 1 | 1 | 5 |
| 2 | 1 | 4 | 2 |
| 3 | 2 | 3 | 3 |
| 4 | 3 | 2 | 7 |
| 5 | 4 | 1 | 4 |
| 6 | 4 | 3 | 6 |
| 7 | 4 | 4 | 8 |

Total nnz = 7.

**Step 2 — Build the three arrays:**

```
val     = [ 5, 2, 3, 7, 4, 6, 8 ]
col_ind = [ 1, 4, 3, 2, 1, 3, 4 ]
row_ptr = [ 1, 3, 4, 5, 8 ]
```

**Verification of `row_ptr`:**
- Row 1 starts at index 1, contains entries 1–2 (indices 1 and 2), so `row_ptr[2] = 3`
- Row 2 starts at index 3, contains entry 3 only, so `row_ptr[3] = 4`
- Row 3 starts at index 4, contains entry 4 only, so `row_ptr[4] = 5`
- Row 4 starts at index 5, contains entries 5–7, `row_ptr[5] = 8 = nnz + 1`

**Memory footprint of CSR representation:** 2×7 + 4 + 1 = **19 values** vs 4×4 = **16 values** for dense. (In this case dense is slightly cheaper — the matrix is not sparse enough. Only ~44% zeros.)

---

### Q10. The following three arrays represent a sparse matrix stored in CSR format (1-based indexing). Reconstruct the full matrix, including zeros.

```
val     = [ 3,  1,  9, 13,  1,  8, 10 ]
col_ind = [ 2,  1,  2,  4,  4,  2,  4 ]
row_ptr = [ 1,  2,  5,  6,  8 ]
```

**Model Answer:**

`row_ptr` has 5 entries → **4 rows**. Largest column index = 4 → **4×4 matrix**.

Decode each row using `row_ptr[i]` to `row_ptr[i+1] - 1` (1-indexed):

**Row 1:** indices 1 to 1 (i.e. just entry 1)
- `val[1]=3` at column `col_ind[1]=2` → `[0, 3, 0, 0]`

**Row 2:** indices 2 to 4 (entries 2, 3, 4)
- `val[2]=1` at column `col_ind[2]=1`
- `val[3]=9` at column `col_ind[3]=2`
- `val[4]=13` at column `col_ind[4]=4` → `[1, 9, 0, 13]`

**Row 3:** indices 5 to 5 (just entry 5)
- `val[5]=1` at column `col_ind[5]=4` → `[0, 0, 0, 1]`

**Row 4:** indices 6 to 7 (entries 6, 7)
- `val[6]=8` at column `col_ind[6]=2`
- `val[7]=10` at column `col_ind[7]=4` → `[0, 8, 0, 10]`

**Full reconstructed matrix:**

```
[ 0   3   0   0  ]
[ 1   9   0  13  ]
[ 0   0   0   1  ]
[ 0   8   0  10  ]
```

---

### Q11. Encode the following 5×5 matrix in CSR format using 1-based indexing.

```
B = [ 0  0  0  0  0 ]
    [ 2  0  0  5  0 ]
    [ 0  0  1  0  0 ]
    [ 0  3  0  0  7 ]
    [ 0  0  0  0  9 ]
```

**Model Answer:**

**Non-zeros identified row by row:**

| Entry | Row | Col | Value |
|:------|:----|:----|:------|
| 1 | 2 | 1 | 2 |
| 2 | 2 | 4 | 5 |
| 3 | 3 | 3 | 1 |
| 4 | 4 | 2 | 3 |
| 5 | 4 | 5 | 7 |
| 6 | 5 | 5 | 9 |

nnz = 6.

```
val     = [ 2, 5, 1, 3, 7, 9 ]
col_ind = [ 1, 4, 3, 2, 5, 5 ]
row_ptr = [ 1, 1, 3, 4, 6, 7 ]
```

**Note on row 1 (all zeros):** `row_ptr[1] = row_ptr[2] = 1` — both point to the same index, indicating zero non-zeros in that row. This is how empty rows are represented in CSR.

**Memory footprint:** 2×6 + 5 + 1 = **18 values** vs 5×5 = **25 values** for dense. CSR saves ~28% here.

---

### Q12. Explain the role of `row_ptr` in CSR format. Why does it have `nrow + 1` entries rather than `nrow`?

**Model Answer:**

`row_ptr[i]` gives the index into `val` and `col_ind` where row `i` begins. The number of non-zeros in row `i` is therefore `row_ptr[i+1] - row_ptr[i]`.

The **extra final entry** (`row_ptr[nrow+1] = nnz + 1`) is necessary so that the formula `row_ptr[i+1] - row_ptr[i]` works uniformly for every row, including the last one. Without it, the last row would require a special case to know where it ends.

This sentinel value also makes it trivial to check whether a row is empty: if `row_ptr[i] == row_ptr[i+1]`, the row contains no non-zeros.

---

## Section C: Arithmetic Intensity and Performance

### Q13. Calculate the arithmetic intensity for each of the following BLAS Level 1 and Level 2 operations. Assume all vectors and matrices contain double-precision (8-byte) values and that N is large.

**(a)** DAXPY: `y ← αx + y` (vectors of length N)
**(b)** DDOT: `s = x · y` (dot product of two vectors of length N)
**(c)** DGEMV: `y ← Ax` (N×N matrix A times vector x, writing result to y)

**Model Answer:**

**(a) DAXPY:**
- FLOPs: N multiplications + N additions = **2N FLOPs**
- Memory: read x (N×8 bytes), read y (N×8 bytes), write y (N×8 bytes) = **24N bytes**
- AI = 2N / 24N = **1/12 ≈ 0.083 FLOPs/byte**

This is strongly memory-bound — less than 1 FLOP per byte.

**(b) DDOT:**
- FLOPs: N multiplications + N additions = **2N FLOPs**
- Memory: read x (N×8 bytes), read y (N×8 bytes) = **16N bytes** (no write of a vector, only a scalar)
- AI = 2N / 16N = **1/8 = 0.125 FLOPs/byte**

Still strongly memory-bound; slightly better than DAXPY due to no write-back.

**(c) DGEMV:**
- FLOPs: N² multiplications + N² additions = **2N² FLOPs**
- Memory: read A (N²×8 bytes), read x (N×8 bytes), write y (N×8 bytes) ≈ **8N² + 16N bytes** ≈ **8N²** for large N
- AI = 2N² / 8N² = **1/4 = 0.25 FLOPs/byte** (constant, independent of N)

Still memory-bound but higher than DAXPY. AI does not grow with N — this is the fundamental weakness of Level 2 BLAS.

---

### Q14. Calculate the arithmetic intensity for DGEMM: `C ← AB` where A, B, C are N×N double-precision matrices. Explain why this AI grows with N.

**Model Answer:**

- **FLOPs:** For each of the N² elements of C, we compute a dot product of length N: N multiplications + (N-1) additions ≈ **2N³ FLOPs**
- **Memory:** Read A (N²×8 bytes), read B (N²×8 bytes), write C (N²×8 bytes) = **24N² bytes** (if A and B are each read once)
- **AI = 2N³ / 24N² = N/12 FLOPs/byte**

AI **scales linearly with N** because the number of FLOPs grows as N³ while the data to load/store only grows as N². Each element of A and B is reused N times across the computation.

**Implication:** For large enough N, DGEMM crosses the **ridge point** on the Roofline model and becomes compute-bound rather than memory-bound. This is why dense matrix-matrix multiplication achieves a high fraction of peak FLOP/s on modern hardware, and why it is the benchmark of choice for HPL/LINPACK.

---

### Q15. A computer has a memory bandwidth of 50 GB/s and a peak compute performance of 100 GFLOPs/s. The ridge point of the Roofline model is at what arithmetic intensity? Where do BLAS Level 1, Level 2, and Level 3 (for N=100, N=1000) operations fall on the Roofline?

**Model Answer:**

**Ridge point:** the AI at which compute-bound and memory-bound ceilings intersect.

```
AI_ridge = R_peak / Bandwidth = 100 GFLOPs/s / 50 GB/s = 2 FLOPs/byte
```

**Placing the BLAS levels:**

| Operation | Approximate AI | Region |
|:----------|:--------------|:-------|
| DAXPY (Level 1) | ~0.083 FLOPs/byte | Memory-bound (far left of ridge) |
| DGEMV (Level 2) | ~0.25 FLOPs/byte | Memory-bound (left of ridge) |
| DGEMM N=100 | ~100/12 ≈ 8.3 FLOPs/byte | Compute-bound (right of ridge) |
| DGEMM N=1000 | ~1000/12 ≈ 83 FLOPs/byte | Strongly compute-bound |

Level 1 and Level 2 operations will never cross the ridge point regardless of N. DGEMM crosses the ridge for any N > 2×12 = 24 on this machine.

**Attainable performance:**
- DAXPY: P = min(100, 50 × 0.083) = min(100, 4.2) = **4.2 GFLOPs/s** (4.2% of peak)
- DGEMM (N=1000): P = min(100, 50 × 83) = **100 GFLOPs/s** (100% of peak, in theory)

---

### Q16. Explain why HPCG (High-Performance Conjugate Gradients) achieves a much lower fraction of peak performance than HPL (High-Performance LINPACK) on real supercomputers.

**Model Answer:**

- **HPL** uses DGEMM (BLAS Level 3): arithmetic intensity O(N), compute-bound, achieves 80–95% of R_peak.
- **HPCG** solves a sparse 3D Poisson equation using a Conjugate Gradient method with sparse matrix operations. The core computation is SpMV (sparse matrix–vector multiply) using CSR format with indirect addressing.

SpMV has O(1) arithmetic intensity — every non-zero element is multiplied exactly once by one vector element. The random access pattern from `col_ind` means data cannot be prefetched. Operations are entirely **memory-bandwidth-bound**.

On the K computer: HPL achieved 10,510 TFLOPs/s (~93% of peak); HPCG achieved 602.7 TFLOPs/s (~5.3% of peak). The 18× gap reflects the difference between compute-bound and memory-bound workloads.

HPCG was introduced as a benchmark precisely because it better represents the memory-bound, sparse linear algebra workloads common in real scientific applications — workloads that HPL completely fails to capture.

---

## Section D: Memory and Storage

### Q17. A scientist has a 10,000 × 10,000 sparse matrix arising from a 2D finite difference discretisation of a PDE on a regular grid. Each interior grid point connects to its 4 direct neighbours (N, S, E, W) plus itself — a 5-point stencil.

**(a)** How many non-zero elements does the matrix have (approximately)?
**(b)** What is the memory requirement to store the matrix in dense double-precision format? Give your answer in MB.
**(c)** What is the memory requirement to store the matrix in CSR double-precision format (assume 4-byte integers for `col_ind` and `row_ptr`)? Give your answer in MB.
**(d)** What fraction of entries are non-zero?

**Model Answer:**

**(a)** N_row = N_col = 10,000. Each row has at most 5 non-zeros (the diagonal plus up to 4 neighbours; boundary rows have fewer). Approximately:
```
nnz ≈ 5 × 10,000 = 50,000
```
(A more precise count accounts for boundary cells, but 5×N_row is the standard estimate.)

**(b)** Dense storage:
```
10,000 × 10,000 × 8 bytes = 800,000,000 bytes = 800 MB
```

**(c)** CSR storage:
- `val`: 50,000 × 8 bytes = 400,000 bytes = 0.4 MB
- `col_ind`: 50,000 × 4 bytes = 200,000 bytes = 0.2 MB
- `row_ptr`: (10,000 + 1) × 4 bytes = 40,004 bytes ≈ 0.04 MB
- **Total CSR ≈ 0.64 MB**

**(d)** Fraction non-zero:
```
50,000 / (10,000 × 10,000) = 50,000 / 100,000,000 = 0.05%
```

CSR uses ~1250× less memory than dense for this matrix. This is a textbook case where sparse storage is essential.

---

### Q18. Compare row-major and column-major storage for dense matrices. What is the implication for cache performance when iterating over rows vs columns in C (which uses row-major)?

**Model Answer:**

**Row-major (C, C++):** Elements of the same row are contiguous in memory.
```
A[0][0], A[0][1], A[0][2], ..., A[0][N-1], A[1][0], A[1][1], ...
```

**Column-major (Fortran, MATLAB):** Elements of the same column are contiguous.
```
A[0][0], A[1][0], A[2][0], ..., A[N-1][0], A[0][1], A[1][1], ...
```

**Cache implications in C (row-major):**

- **Row iteration (inner loop over j):** `A[i][j]` then `A[i][j+1]` — consecutive in memory. **Cache-friendly** — exploits spatial locality. Each cache line loaded is fully used.
- **Column iteration (inner loop over i):** `A[i][j]` then `A[i+1][j]` — stride N in memory. **Cache-unfriendly** — each access skips to a new cache line. For large N, causes frequent cache misses.

This is why naive matrix multiplication in C (with inner loop over k computing `C[i][j] += A[i][k] * B[k][j]`) has poor cache behaviour for `B`: the k-loop accesses `B` in column order, which is stride-N in row-major C. Cache blocking (loop tiling) and BLAS Level 3 optimised libraries reorder the loops to maximise cache hits.

---

## Section E: Multi-Part Exam Questions

### Q19. (Multi-part) Consider BLAS and its role in HPC.

**(a)** State the arithmetic intensity for each of the three BLAS levels, and state whether each is typically compute-bound or memory-bound. *(3 marks)*

**(b)** For BLAS Level 3 (matrix-matrix multiplication of two N×N matrices), derive an expression for the arithmetic intensity in terms of N. *(4 marks)*

**(c)** A cluster node has a peak performance of 200 GFLOPs/s and a memory bandwidth of 40 GB/s. What is the minimum matrix size N at which DGEMM becomes compute-bound on this node? *(3 marks)*

**(d)** Why do optimised BLAS libraries such as OpenBLAS or Intel MKL nearly always outperform a naive hand-written matrix multiplication loop in C? *(3 marks)*

**Model Answer:**

**(a)**

| Level | Arithmetic Intensity | Bound |
|:------|:--------------------|:------|
| 1 (vector-vector) | O(1) — ~0.083–0.25 FLOPs/byte | Memory-bound |
| 2 (matrix-vector) | O(1) — ~0.25 FLOPs/byte | Memory-bound |
| 3 (matrix-matrix) | O(N) — grows with matrix size | Memory-bound for small N; compute-bound for large N |

**(b)** For `C ← A × B` with A, B, C of size N×N:
- FLOPs: each of N² output elements requires N multiply-add pairs → **2N³ FLOPs** total
- Memory transfers (minimum, reading each matrix once): 3 matrices × N² elements × 8 bytes = **24N² bytes**
- **AI = 2N³ / 24N² = N/12 FLOPs/byte**

**(c)** The ridge point is where compute and memory ceilings intersect:
```
AI_ridge = R_peak / Bandwidth = 200 / 40 = 5 FLOPs/byte
```
Setting AI_DGEMM = AI_ridge:
```
N/12 = 5
N = 60
```
DGEMM becomes compute-bound for **N > 60** on this node.

**(d)** Reasons why optimised libraries outperform naive code:
1. **Cache blocking / loop tiling:** Reorders the computation so that sub-matrices fit in L1/L2 cache, raising effective AI by exploiting data reuse before data is evicted.
2. **SIMD vectorisation:** Uses architecture-specific vector instructions (e.g. AVX-512) to process multiple FLOPs per clock cycle — a naive loop rarely auto-vectorises perfectly.
3. **Software pipelining and instruction scheduling:** Hides memory latency by interleaving memory loads with arithmetic from previous iterations, maximising functional unit utilisation.

---

### Q20. (Multi-part) CSR encoding and analysis.

Consider the following matrix:

```
M = [ 0  4  0  0  0 ]
    [ 0  0  0  2  0 ]
    [ 6  0  0  0  3 ]
    [ 0  0  0  0  0 ]
    [ 0  5  0  8  0 ]
```

**(a)** Encode M in CSR format using 1-based indexing. Show all three arrays: `val`, `col_ind`, and `row_ptr`. *(5 marks)*

**(b)** What is the memory footprint of the CSR representation assuming 8-byte doubles for `val` and 4-byte integers for `col_ind` and `row_ptr`? *(2 marks)*

**(c)** What is the memory footprint of the dense representation (8-byte doubles)? *(1 mark)*

**(d)** When would the dense representation become more efficient than CSR for a matrix of this size? *(2 marks)*

**Model Answer:**

**(a)** Identify non-zeros row by row:

| Entry | Row | Col | Value |
|:------|:----|:----|:------|
| 1 | 1 | 2 | 4 |
| 2 | 2 | 4 | 2 |
| 3 | 3 | 1 | 6 |
| 4 | 3 | 5 | 3 |
| 5 | 5 | 2 | 5 |
| 6 | 5 | 4 | 8 |

nnz = 6.

```
val     = [ 4, 2, 6, 3, 5, 8 ]
col_ind = [ 2, 4, 1, 5, 2, 4 ]
row_ptr = [ 1, 2, 3, 5, 5, 7 ]
```

Note: `row_ptr[4] = row_ptr[5] = 5` because row 4 is entirely zero (no non-zeros).

**(b)** CSR memory footprint:
- `val`: 6 × 8 = 48 bytes
- `col_ind`: 6 × 4 = 24 bytes
- `row_ptr`: (5+1) × 4 = 24 bytes
- **Total: 96 bytes**

**(c)** Dense memory footprint:
- 5 × 5 × 8 = **200 bytes**

**(d)** CSR stores 2·nnz + (nrow+1) integers plus nnz doubles. As nnz increases towards N², the index arrays become overhead. The crossover depends on exact integer vs double sizes, but the rule of thumb is that CSR becomes less efficient once roughly **10–20% of elements are non-zero**. For a 5×5 matrix with 25 elements, CSR would become comparable to dense at around 3–5 non-zeros per row (15–25 nnz total), i.e. when over ~60% of elements are non-zero (though at this scale both representations are trivially small).

---

### Q21. (Multi-part) Benchmarking and performance interpretation.

**(a)** Name two standard HPC benchmarks and briefly describe the computational workload each uses. *(4 marks)*

**(b)** On a given supercomputer, HPL achieves 85% of R_peak while HPCG achieves 4% of R_peak. Explain this large discrepancy in terms of arithmetic intensity and memory behaviour. *(5 marks)*

**(c)** Which benchmark is a better predictor of performance for a scientific code that solves large sparse linear systems arising from finite element analysis? Justify your answer. *(3 marks)*

**Model Answer:**

**(a)**
- **HPL (High-Performance LINPACK):** Solves a large dense system of linear equations using LU factorisation. The dominant operation is DGEMM (BLAS Level 3 matrix-matrix multiplication), which is compute-bound with AI = O(N).
- **HPCG (High-Performance Conjugate Gradients):** Solves a sparse 3D Poisson equation using the Conjugate Gradient iterative method. The dominant operation is SpMV (sparse matrix-vector multiplication) using CSR storage, which is memory-bound with AI = O(1).

**(b)** HPL dominates because:
- DGEMM has AI = O(N) → grows unboundedly. For large matrices, operations are firmly in the compute-bound region of the Roofline model. The compute units are always busy.
- Dense contiguous memory access allows the hardware prefetcher to stream data efficiently; cache blocking in optimised BLAS libraries maximises data reuse.

HPCG is limited because:
- SpMV has AI ≈ O(1) → always memory-bandwidth-bound.
- CSR's indirect addressing (`col_ind` lookups) causes irregular, non-prefetchable memory access. CPU cores stall waiting for data from DRAM.
- Even if the CPU is fast, performance is capped at `bandwidth × AI_SpMV`, which is a small fraction of R_peak.

The 85% vs 4% gap directly reflects the difference between a compute-bound and a memory-bound workload.

**(c)** **HPCG** is the better predictor. Finite element codes produce large sparse matrices where the assembled stiffness/mass matrix has only a few non-zeros per row (typically 5–50 for 3D problems). The solver phase is dominated by SpMV — the same operation HPCG benchmarks. HPCG captures the memory bandwidth, latency, and indirect-access costs that dominate real engineering workloads. HPL would overestimate the performance of such a code by a factor of ~20 or more.

---

### Q22. (Multi-part) Dense vs sparse matrix storage trade-offs.

**(a)** Explain what a "dense matrix" is and why dense storage is preferred for compute-heavy operations. *(3 marks)*

**(b)** Give two real-world application domains that naturally produce sparse matrices and briefly explain why the matrices are sparse in each case. *(4 marks)*

**(c)** A programmer proposes storing a 100,000 × 100,000 matrix in dense format. If each element is a double-precision float (8 bytes), how much memory is required? Why is this impractical? *(3 marks)*

**(d)** The matrix in part (c) arises from a finite difference discretisation of a 2D PDE with a 5-point stencil. Estimate nnz and the memory required for CSR storage (8-byte doubles, 4-byte ints). *(3 marks)*

**Model Answer:**

**(a)** A dense matrix is one where most or all elements are non-zero. Dense storage places all elements in a contiguous block of memory (row-major or column-major). This is preferred for compute-heavy operations because:
- Memory access is predictable and sequential → hardware prefetchers work well
- No index overhead (no `col_ind` or `row_ptr` arrays)
- High arithmetic intensity operations (BLAS Level 3) can reuse data from cache many times
- Highly optimised libraries (BLAS) achieve near-peak performance

**(b)**
1. **Finite element analysis (structural mechanics, fluid dynamics):** The global stiffness matrix has a non-zero entry K[i,j] only if mesh nodes i and j are connected by an element. In a large 3D mesh, each node connects to only a handful of neighbours, so the vast majority of matrix entries are zero.
2. **Social network graph analysis / web link graphs:** The adjacency matrix A[i,j] = 1 if user i is connected to user j (or page i links to page j). With millions of nodes but each user having only ~100–1000 connections, the matrix is extremely sparse (density << 0.001%).

**(c)** Dense memory requirement:
```
100,000 × 100,000 × 8 = 80,000,000,000 bytes = 80 GB
```
This is **impractical** because:
- 80 GB exceeds the RAM of most individual compute nodes (typical nodes have 64–512 GB, but a single matrix consuming 80 GB leaves little room for anything else)
- Even if memory were available, a 100,000×100,000 matrix in a PDE context is almost entirely zeros — dense storage wastes the vast majority of memory on meaningless zeros
- Memory allocation of 80 GB for a single matrix is extremely wasteful compared to the ~2–5 MB that CSR would require

**(d)** nnz estimate with 5-point stencil:
```
nnz ≈ 5 × 100,000 = 500,000
```

CSR memory:
- `val`: 500,000 × 8 = 4,000,000 bytes = 4 MB
- `col_ind`: 500,000 × 4 = 2,000,000 bytes = 2 MB
- `row_ptr`: 100,001 × 4 = 400,004 bytes ≈ 0.4 MB
- **Total CSR ≈ 6.4 MB**

CSR uses ~12,500× less memory than dense for this matrix — the practical benefit of sparse storage is decisive.

---

## Section F: Compare and Contrast

### Q23. Compare BLAS Level 1, Level 2, and Level 3 across all key dimensions. Complete the table below and add an explanation of why BLAS level matters for performance on modern hardware.

| Property | Level 1 (vector-vector) | Level 2 (matrix-vector) | Level 3 (matrix-matrix) |
|:----------|:------------------------|:------------------------|:------------------------|
| Example operation | ? | ? | ? |
| FLOPs | ? | ? | ? |
| Memory transfers | ? | ? | ? |
| Arithmetic intensity | ? | ? | ? |
| Bound by | ? | ? | ? |
| Fraction of R_peak achievable | ? | ? | ? |

**Model Answer (completed table):**

| Property | Level 1 (vector-vector) | Level 2 (matrix-vector) | Level 3 (matrix-matrix) |
|:----------|:------------------------|:------------------------|:------------------------|
| Example operation | `y ← αx + y` (DAXPY) | `y ← αAx + βy` (DGEMV) | `C ← αAB + βC` (DGEMM) |
| FLOPs | O(N) | O(N²) | O(N³) |
| Memory transfers | O(N) | O(N²) | O(N²) |
| Arithmetic intensity | O(1) — constant, ~0.083–0.25 FLOPs/byte | O(1) — constant, ~0.25 FLOPs/byte | O(N) — grows linearly with N |
| Bound by | Memory bandwidth | Memory bandwidth | Memory BW for small N; compute for large N |
| Fraction of R_peak achievable | ~1–5% | ~5–15% | ~80–95% |

**Explanation:** The key distinguishing feature is that Level 3's arithmetic intensity grows with problem size. For large N, Level 3 crosses the Roofline ridge point and becomes compute-bound. In contrast, Levels 1 and 2 are permanently memory-bandwidth-limited — no amount of increasing N changes this, because FLOPs and memory scale identically. This is why HPC codes should be structured to cast as much work as possible into BLAS Level 3 calls.

---

### Q24. Compare dense matrix storage and CSR sparse matrix storage across the following dimensions.

**(a)** Memory footprint for an N×N matrix with nnz non-zeros.
**(b)** Memory access pattern during matrix-vector multiplication.
**(c)** Suitability for BLAS Level 3 type operations.
**(d)** When each format is preferred.

**Model Answer:**

**(a) Memory footprint:**
- **Dense:** N² values → N²×8 bytes (for double precision). All elements stored regardless.
- **CSR:** 2·nnz + (N+1) values → (2·nnz×8) + (nnz+N+1)×4 bytes (mixing double and int). If nnz << N², drastically smaller.

**(b) Memory access pattern during SpMV / dense MVM:**
- **Dense MVM (DGEMV):** Row i accesses `A[i][0..N-1]` — contiguous memory read, followed by scatter into `y[i]`. Predictable, prefetchable. Still O(1) AI.
- **CSR SpMV:** For row i, reads `row_ptr[i]`, then iterates over `col_ind[row_ptr[i]]..col_ind[row_ptr[i+1]-1]` to gather `x[col_ind[k]]`. The gather step accesses `x` at arbitrary column indices — irregular, non-contiguous, cache-unfriendly. Causes cache misses.

**(c) Suitability for BLAS Level 3 operations:**
- **Dense:** Naturally supports DGEMM and related Level 3 operations. Highly suitable — this is the intended use case.
- **CSR:** Not suitable for Level 3 operations. Sparse matrix-matrix multiplication (SpGEMM) is a specialised, complex operation handled by libraries like PETSc or cuSPARSE. AI is still O(1) for sparse-dense multiplications.

**(d) When each is preferred:**
- **Dense:** When most elements are non-zero; when maximum computational throughput is needed (e.g. neural network layers, linear solvers on small to medium systems).
- **CSR:** When nnz << N² (roughly < 10% density); when the zero pattern arises naturally from a physical model (PDE stencils, graph structure). Essential for large-scale sparse PDE solvers.

---

---

## Section G: Exam-Style Questions (May 2024 Paper)

### Q25 — Sparse vs dense matrix: definition *(2 marks)*

State the difference between a **sparse matrix** and a **dense matrix**. Give one example of an application domain that naturally produces each type.

> **Model Answer:**
>
> - A **dense matrix** is one in which most or all elements are non-zero; every element must be stored explicitly. Memory requirement = N × M × (element size). Dense matrices arise naturally in: linear algebra (arbitrary systems of equations), small neural network weight matrices, or any computation where there is no structural reason for zeros.
>
> - A **sparse matrix** is one in which the vast majority of elements are zero; only the non-zero elements (and their indices) need to be stored. Memory requirement scales with nnz (number of non-zeros) << N × M. Sparse matrices arise naturally in: finite-difference or finite-element discretisations of PDEs (each node only connects to a few neighbours), graph adjacency matrices (social networks, web link graphs), and circuit simulation.
>
> [1 mark for each correct definition with example, or 2 marks for both definitions clearly contrasted.]

---

### Q26 — Memory scaling for dense matrix multiplication *(2 marks)*

For dense matrix multiplication of two N × N matrices (double precision, 8 bytes per element):

**(a)** How does the **number of floating-point operations** scale with N? *(1 mark)*

**(b)** How does the **memory transferred** (total data read from memory) scale with N? *(1 mark)*

> **Model Answer:**
>
> **(a) FLOPs scale as O(N³).**
> For C = A × B with N × N matrices, computing each element C[i,j] requires N multiplications and N−1 additions ≈ 2N FLOPs. There are N² output elements, giving approximately **2N³ FLOPs** in total. Scaling: **O(N³)**. [1 mark]
>
> **(b) Memory transferred scales as O(N²).**
> The three matrices A, B, C each contain N² elements × 8 bytes = 8N² bytes. Total memory footprint (and maximum data that needs to be read/written) is proportional to **3 × 8N² = 24N²** bytes. Scaling: **O(N²)**. [1 mark]
>
> **Consequence:** Since FLOPs grow as N³ but memory transfers grow as N², the arithmetic intensity AI = FLOPs/bytes ∝ N³/(N²) = N grows linearly with N. For sufficiently large N, matrix multiplication becomes compute-bound — this is why BLAS Level 3 achieves near-peak performance on large matrices.

---

### Q27 — CSR encoding: exam matrix *(5 marks)*

Encode the following 4×4 matrix in **CSR (Compressed Sparse Row)** format using **0-based indexing**. Show all three arrays: `val`, `col_ind`, and `row_ptr`, and state their lengths.

```
A = [ 5  0  2  0 ]
    [ 0  1  0  0 ]
    [ 2  0  0  0 ]
    [ 0  0  0  7 ]
```

> **Model Answer:**
>
> First, identify all non-zeros by scanning row by row:
>
> | Index | Row | Col | Value |
> |:------|:----|:----|:------|
> | 0 | 0 | 0 | 5 |
> | 1 | 0 | 2 | 2 |
> | 2 | 1 | 1 | 1 |
> | 3 | 2 | 0 | 2 |
> | 4 | 3 | 3 | 7 |
>
> nnz = 5.
>
> **CSR arrays (0-based indexing):**
> ```
> val     = [ 5, 2, 1, 2, 7 ]          length = nnz = 5
> col_ind = [ 0, 2, 1, 0, 3 ]          length = nnz = 5
> row_ptr = [ 0, 2, 3, 4, 5 ]          length = nrow + 1 = 5
> ```
>
> **Explanation of `row_ptr`:**
> - `row_ptr[0] = 0`: row 0 starts at index 0 in `val`/`col_ind`
> - `row_ptr[1] = 2`: row 1 starts at index 2 (row 0 had 2 non-zeros: A[0,0]=5 and A[0,2]=2)
> - `row_ptr[2] = 3`: row 2 starts at index 3 (row 1 had 1 non-zero: A[1,1]=1)
> - `row_ptr[3] = 4`: row 3 starts at index 4 (row 2 had 1 non-zero: A[2,0]=2)
> - `row_ptr[4] = 5`: sentinel — total nnz = 5 (row 3 had 1 non-zero: A[3,3]=7)
>
> **Marking points (5 marks):**
> - Correct `val` array (1 mark)
> - Correct `col_ind` array (1 mark)
> - Correct `row_ptr` array (2 marks: 1 for structure, 1 for all values correct)
> - Correct lengths stated (1 mark)

---

*End of Week 9 Practice Questions*

**Concept links:** [BLAS and Dense Matrices](../wiki/concepts/BLAS_and_Dense_Matrices.md) | [Sparse Matrices and CSR](../wiki/concepts/Sparse_Matrices_and_CSR.md) | [Arithmetic Intensity and the Roofline Model](../wiki/concepts/Arithmetic_Intensity_and_Roofline_Model.md) | [Week 9 Summary](../wiki/summaries/Week_9_Summary.md)
