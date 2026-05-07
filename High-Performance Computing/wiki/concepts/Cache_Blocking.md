---
title: "Cache Blocking (Loop Tiling)"
tags: [hpc, week-6, optimization, memory]
date: 2026-05-07
---

# Cache Blocking (Loop Tiling)

**Cache blocking**, also known as **loop tiling**, is a code optimization technique used to improve the performance of applications by better utilizing the processor's [Memory Hierarchy and Cache](../concepts/Memory_Hierarchy_and_Cache.md).

## Relationship to Cache Locality

To understand cache blocking, one must first understand the two types of **locality of reference**:

1.  **Spatial Locality:** If a memory location is accessed, nearby locations are likely to be accessed soon. This is exploited by loading data in "cache lines" (e.g., 64 bytes).
2.  **Temporal Locality:** If a memory location is accessed, it is likely to be accessed again in the near future. **Cache blocking specifically targets the exploitation of temporal locality.**

## The Problem: Cache Eviction
When working with large datasets (e.g., a massive matrix), the data may be too large to fit in the CPU cache. If a program iterates through the entire dataset, by the time it returns to the "beginning" for the next pass, the original data has likely been evicted from the cache to make room for newer data. This results in frequent, slow trips to main memory.

## The Solution: Blocking
Instead of operating on the entire dataset at once, the algorithm is restructured to work on small "blocks" or "tiles" of data that fit comfortably within the cache (L1, L2, or L3).

*   **Mechanism:** The loops are transformed (often "strip-mined" and "interchanged") so that the inner loops iterate within the boundaries of a block.
*   **Result:** All necessary data for a block is loaded into the cache once, reused multiple times for all operations involving that block, and then discarded. This minimizes the total number of memory transfers.

## Example: Matrix Multiplication
In a naive matrix multiplication $C = A \times B$, for each element of $C$, we iterate over a row of $A$ and a column of $B$. For large matrices, the elements of $B$ are likely to be evicted before they can be reused for the next row of $C$.

By applying **cache blocking**, we multiply sub-matrices (blocks) together. These small blocks remain in the cache, drastically increasing the [Arithmetic Intensity](../concepts/Arithmetic_Intensity_and_Roofline_Model.md) and moving the application from being **memory-bound** toward being **compute-bound**.

## Implementation Note
*   **Compilers:** Modern compilers (using flags like `-O3`) can sometimes perform cache blocking automatically, but complex loop dependencies often require manual implementation or the use of optimized libraries like **BLAS** (Basic Linear Algebra Subprograms).
*   **Block Size:** The optimal block size depends on the specific cache sizes of the hardware.
