---
title: "OpenMP"
tags: [hpc, week-2, openmp, parallel-programming, shared-memory]
date: 2026-05-05
---

# OpenMP (Open Multi-Processing)

OpenMP is an open standard and specification for shared-memory parallel programming in C, C++, and Fortran. It provides extensions to these languages, enabling programmers to easily specify where and how parallelism should be introduced into sequential applications.

## Execution Model: Fork-Join
OpenMP employs a **fork-join** execution model:
1.  **Fork:** Execution begins with a single main thread (master thread). When a parallel region is encountered, the master thread spawns (forks) a team of worker threads.
2.  **Parallel Execution:** The team of threads executes the statements inside the parallel region simultaneously.
3.  **Join:** At the end of the parallel region, the worker threads synchronize and terminate (join), and the master thread continues sequential execution.

## Shared Memory Architecture Requirement
OpenMP is strictly designed for **shared memory environments**. In the context of a [Cluster Architecture](../concepts/Cluster_Architecture.md), this means OpenMP can only be used to parallelise work *within a single compute node*, where all processor cores can address the same physical memory space. It cannot inherently span across multiple independent nodes in a distributed-memory system (which requires tools like MPI).

## Components of OpenMP
OpenMP provides three primary extensions to standard programming languages:
1.  **Compiler Directives:** Used to tell the compiler to parallelise a block of code. In C/C++, they take the form `#pragma omp directive [clause1, ...]`.
2.  **Environment Variables:** Used to control the runtime behavior, such as `OMP_NUM_THREADS` which dictates the number of threads forked in a parallel region.
3.  **Runtime Library Routines:** Callable functions (e.g., `omp_get_thread_num()`, `omp_get_num_threads()`) available by including `<omp.h>`. They allow querying the execution environment and managing synchronization locks.

## Conditional Compilation
Code can be written to compile sequentially if an OpenMP-compatible compiler (or the required compilation flag, like `-fopenmp` for GCC) is not used. OpenMP specifies that the `_OPENMP` macro is defined when enabled, allowing conditional blocks:
```c
#ifdef _OPENMP
  // OpenMP specific library calls
#else
  // Fallback sequential logic
#endif
```