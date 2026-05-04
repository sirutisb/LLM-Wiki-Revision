---
title: "Data Dependencies and Data Races"
tags: [hpc, week-2, openmp, data-race, loop-dependency]
date: 2026-05-05
---

# Data Dependencies and Data Races

When executing code in parallel, the non-deterministic execution order of threads can lead to bugs if data accesses are not carefully managed. These bugs typically arise from data races or loop-carried dependencies.

## Data Races
A data race occurs when:
1.  Multiple threads access the same memory location simultaneously.
2.  At least one of these accesses is a **write** operation.
3.  The threads are not using any exclusive synchronization mechanism.

This causes updates to be corrupted because threads can overwrite each other's intermediate values. In [OpenMP](../concepts/OpenMP.md), data races are often resolved by adjusting [Variable Scoping](../concepts/Variable_Scoping_OpenMP.md), such as using `private` or `reduction` variables instead of `shared` variables.

## Loop-Carried Dependencies
A loop-carried dependency exists when an operation in one iteration of a loop depends on the results of another iteration of the same loop. If the loop is parallelised, iterations may execute out of order, violating the dependency.

There are three primary types of loop-carried dependencies:

### 1. Flow Dependency (Read-after-Write)
*   **Also known as:** True dependency.
*   **Description:** Iteration `i` reads a value that was written by iteration `i-1`.
*   **Issue:** In parallel, iteration `i` might execute before iteration `i-1` finishes updating the value.
*   **Resolution:** Often impossible to parallelise directly without rethinking or rewriting the underlying algorithm.

### 2. Anti-Dependency (Write-after-Read)
*   **Description:** Iteration `i` writes to a variable after iteration `i-1` has read from it (or iteration `i` needs a value before iteration `i+1` overwrites it).
*   **Issue:** In parallel, iteration `i+1` may execute first and overwrite the value before iteration `i` can read it.
*   **Resolution:** Can usually be corrected by allocating a new temporary array to write the outputs to, ensuring the original read array remains unmodified during execution.

### 3. Output Dependency (Write-after-Write)
*   **Description:** Multiple iterations write to the exact same memory location.
*   **Issue:** In serial execution, the sequentially last iteration dictates the final value left in the variable. In parallel, it's impossible to know which thread will write last, causing non-deterministic final state.
*   **Resolution:** In OpenMP, this can be corrected by scoping the variable as `lastprivate`, which guarantees the variable retains the value from the sequentially last iteration.