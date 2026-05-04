---
title: "Wiki Index"
tags: [index, hpc]
date: 2026-05-05
---

# High-Performance Computing Wiki Index

Welcome to the HPC revision wiki.

## Summaries
*   [Week 1 Summary: Introduction to HPC](summaries/Week_1_Summary.md) - Overview of HPC, Top500, hardware trends, cluster architectures, and programming languages.
*   [Week 2 Summary: Introduction to OpenMP](summaries/Week_2_Summary.md) - Overview of OpenMP, fork-join model, parallel loops, variable scoping, and data dependencies.
*   [Week 3 Summary: Numerical Solutions to PDEs](summaries/Week_3_Summary.md) - Calculating numerical solutions to PDEs, advection, diffusion, finite differences, and numerical stability.
*   [Week 4 Summary: Introduction to MPI](summaries/Week_4_Summary.md) - Overview of MPI, point-to-point and collective communications, non-blocking operations, and domain decomposition.
*   [Week 5 Summary: Floating Point Arithmetic](summaries/Week_5_Summary.md) - Floating-point representation, IEEE 754 standard, range, accuracy, and calculating peak performance.

## Concepts
*   [High Performance Computing (HPC)](concepts/High_Performance_Computing_HPC.md) - Definition and application areas of HPC.
*   [Performance Metrics and Top500](concepts/Performance_Metrics_and_Top500.md) - Measuring system performance via FLOPs and the Top500 HPL benchmark.
*   [Moore's Law and Dennard Scaling](concepts/Moores_Law_and_Dennard_Scaling.md) - Hardware scaling trends explaining the fundamental need for parallelism.
*   [Cluster Architecture](concepts/Cluster_Architecture.md) - Overview of the dominant HPC topology comprising compute, login, mass storage nodes, and interconnects.
*   [HPC Programming Languages](concepts/HPC_Programming_Languages.md) - Role of compiled languages (C, C++, Fortran) and parallel extensions (OpenMP, MPI) in HPC.
*   [OpenMP](concepts/OpenMP.md) - OpenMP standard, fork-join model, and basic directives for shared-memory parallelism.
*   [Parallel Loops in OpenMP](concepts/Parallel_Loops_OpenMP.md) - Distributing loop workload among threads using `#pragma omp for`.
*   [Variable Scoping in OpenMP](concepts/Variable_Scoping_OpenMP.md) - Managing `shared`, `private`, `reduction`, and `lastprivate` variables.
*   [Data Dependencies and Data Races](concepts/Data_Dependencies.md) - Dealing with data races and loop-carried dependencies (flow, anti, output).
*   [Partial Differential Equations (PDEs)](concepts/Partial_Differential_Equations.md) - Equations containing derivatives with respect to multiple variables.
*   [Exponential Decay](concepts/Exponential_Decay.md) - ODE describing a quantity decreasing at a rate proportional to itself.
*   [Advection Equation](concepts/Advection_Equation.md) - PDE describing transport of a quantity by a velocity field.
*   [Diffusion Equation](concepts/Diffusion_Equation.md) - PDE describing movement from high to low concentration.
*   [Finite Difference Method](concepts/Finite_Difference_Method.md) - Approximating derivatives using discrete grid points and Taylor series error analysis.
*   [Numerical Stability and CFL](concepts/Numerical_Stability_and_CFL.md) - Condition for numerical schemes to prevent errors from growing without bound.
*   [Message Passing Interface (MPI)](concepts/Message_Passing_Interface_MPI.md) - Parallel programming standard for distributed-memory systems using explicit message passing.
*   [MPI Point-to-Point Communication](concepts/MPI_Point_to_Point_Communication.md) - Direct communication between a specific pair of MPI processes (MPI_Send, MPI_Recv).
*   [MPI Collective Communication](concepts/MPI_Collective_Communication.md) - Communication operations across a group of processes (Broadcast, Scatter, Gather, Reduce).
*   [MPI Non-blocking Communication](concepts/MPI_Non_blocking_Communication.md) - Non-blocking send and receive operations to overlap computation and avoid deadlocks.
*   [Domain Decomposition](concepts/Domain_Decomposition.md) - Distributing a computational domain across MPI processes, requiring halo exchanges.

## Comparisons
*   [OpenMP vs. MPI](comparisons/OpenMP_vs_MPI.md) - Comparison between shared-memory (OpenMP) and distributed-memory (MPI) programming paradigms.