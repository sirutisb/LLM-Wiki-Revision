---
title: "Parallel Loops in OpenMP"
tags: [hpc, week-2, openmp, parallel-programming, shared-memory]
date: 2026-05-05
---

# Parallel Loops in OpenMP

A fundamental way to distribute workload between threads in OpenMP is by parallelising loops. In this approach, different threads carry out different iterations of a loop, accelerating the overall execution of the loop's body.

## Basic Syntax
To parallelise a loop from within an already established parallel region, use:
```c
#pragma omp for
for (i = 0; i < N; i++) { ... }
```

Often, starting a parallel region and parallelising a loop are combined into a single directive:
```c
#pragma omp parallel for
for (i = 0; i < N; i++) { ... }
```

## Order of Iterations
When a loop is parallelised, the loop iterations **will not** necessarily take place in the order specified by the original loop iterator. It is unsafe to rely on sequential execution order. If the results are stored in an array (which holds data continuously), you will often require a second, completely sequential (non-parallelised) loop if you wish to print or access the results in sequential order.

## Scoping in Loops
Correct behavior relies heavily on appropriate [Variable Scoping in OpenMP](../concepts/Variable_Scoping_OpenMP.md). By default, variables declared before the loop are shared, while loop iterators (like `i`) are made private to each thread to ensure they don't overwrite each other's iteration counts. If loop iterations rely on data from other iterations, [Data Dependencies](../concepts/Data_Dependencies.md) must be managed to avoid race conditions.