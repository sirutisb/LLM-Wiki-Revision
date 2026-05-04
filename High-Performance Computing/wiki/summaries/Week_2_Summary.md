---
title: "Week 2 Summary: Introduction to OpenMP"
tags: [hpc, week-2, openmp, parallel-programming, shared-memory]
date: 2026-05-05
---

# Week 2 Summary: Introduction to OpenMP

## Overview
Week 2 introduces OpenMP (Open Multi-Processing), an open specification for shared memory parallel programming in C, C++, and Fortran. It covers the core execution model, how to parallelise existing sequential code using compiler directives, and the critical issues surrounding data dependencies and variable scoping.

## Key Concepts

*   **[OpenMP](../concepts/OpenMP.md)**: An API that uses a fork-join execution model, specifically designed for shared-memory architectures (e.g., within a single compute node of a cluster).
*   **[Parallel Loops](../concepts/Parallel_Loops_OpenMP.md)**: Distributing loop iterations across multiple threads using `#pragma omp for`.
*   **[Variable Scoping](../concepts/Variable_Scoping_OpenMP.md)**: Managing how variables are accessed by threads (`private`, `shared`, `reduction`, `lastprivate`).
*   **[Data Dependencies](../concepts/Data_Dependencies.md)**: Understanding data races and loop-carried dependencies (flow, anti, output) that can lead to incorrect behavior in parallel regions.

## Practical Usage
OpenMP extensions include:
*   **Compiler Directives:** `#pragma omp ...` to specify parallel regions and workload distribution.
*   **Environment Variables:** Controlling execution (e.g., `OMP_NUM_THREADS` for setting the number of threads).
*   **Runtime Library Routines:** Querying the environment (e.g., `omp_get_thread_num()`, `omp_get_num_threads()`) and managing synchronization, enabled by including `<omp.h>`.
*   **Conditional Compilation:** Using the `#ifdef _OPENMP` pre-processor macro to maintain serial execution when OpenMP is not enabled.
