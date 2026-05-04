---
title: "HPC Programming Languages"
tags: [hpc, week-1, languages, mpi, openmp]
date: 2026-05-05
---

# HPC Programming Languages

HPC applications typically prioritize maximum performance, dictating the choice of programming languages and paradigms.

## Compiled Languages
*   HPC uses compiled languages because compilers parse source code and generate an executable, making compile-time optimizations that would be too expensive for an interpreter at runtime.
*   **Dominant Languages:** C, C++, and Fortran.
*   *Note:* Many large, legacy HPC codes and libraries are written in Fortran.

## Parallel Programming
Parallelization is generally too complex for compilers to handle automatically; it must be added explicitly by the programmer. 
It is often based on extensions to existing serial languages:
*   **[OpenMP](../concepts/OpenMP.md):** Directives-based parallelism for **shared memory**.
*   **[MPI](../concepts/MPI.md):** Message Passing Interface for shared or **distributed memory**, using function calls.

There are specific parallel programming languages (e.g., Chapel, Julia), but they are currently less widely used than the C/C++/Fortran + OpenMP/MPI approach.