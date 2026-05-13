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
*   [Week 6 Summary: Memory and Cache](summaries/Week_6_Summary.md) - Memory hierarchy, cache locality, arithmetic intensity, Roofline model, and NUMA architectures.
*   [Week 7 Summary: Factors Affecting Parallel Performance](summaries/Week_7_Summary.md) - SLOW overheads, parallel scaling laws, load balancing, and network topologies.
*   [Week 8 Summary: Manager-Worker and Task-Based Parallelism](summaries/Week_8_Summary.md) - Dynamic load balancing, advanced MPI features, OpenMP sections, and tasks.

## Topics by Week

### Week 1
*   [High Performance Computing (HPC)](concepts/High_Performance_Computing_HPC.md)
*   [Performance Metrics and Top500](concepts/Performance_Metrics_and_Top500.md)
*   [Moore's Law and Dennard Scaling](concepts/Moores_Law_and_Dennard_Scaling.md)
*   [Cluster Architecture](concepts/Cluster_Architecture.md)
*   [HPC Programming Languages](concepts/HPC_Programming_Languages.md)

### Week 2
*   [OpenMP](concepts/OpenMP.md)
*   [Parallel Loops in OpenMP](concepts/Parallel_Loops_OpenMP.md)
*   [Variable Scoping in OpenMP](concepts/Variable_Scoping_OpenMP.md)
*   [Data Dependencies and Data Races](concepts/Data_Dependencies.md)

### Week 3
*   [Partial Differential Equations (PDEs)](concepts/Partial_Differential_Equations.md)
*   [Exponential Decay](concepts/Exponential_Decay.md)
*   [Advection Equation](concepts/Advection_Equation.md)
*   [Diffusion Equation](concepts/Diffusion_Equation.md)
*   [Finite Difference Method](concepts/Finite_Difference_Method.md)
*   [Numerical Stability and CFL](concepts/Numerical_Stability_and_CFL.md)

### Week 4
*   [Message Passing Interface (MPI)](concepts/Message_Passing_Interface_MPI.md)
*   [MPI Point-to-Point Communication](concepts/MPI_Point_to_Point_Communication.md)
*   [MPI Collective Communication](concepts/MPI_Collective_Communication.md)
*   [MPI Non-blocking Communication](concepts/MPI_Non_blocking_Communication.md)
*   [Domain Decomposition](concepts/Domain_Decomposition.md)

### Week 5
*   [Floating Point Arithmetic](concepts/Floating_Point_Arithmetic.md)

### Week 6
*   [Memory Hierarchy and Cache](concepts/Memory_Hierarchy_and_Cache.md)
*   [Cache Blocking (Loop Tiling)](concepts/Cache_Blocking.md)
*   [Problem Size and Memory Footprint](concepts/Performance_Testing_Problem_Size.md)
*   [Arithmetic Intensity and the Roofline Model](concepts/Arithmetic_Intensity_and_Roofline_Model.md)
*   [NUMA and First-Touch Policy](concepts/NUMA_and_First_Touch_Policy.md)

### Week 7
*   [Parallel Scaling](concepts/Parallel_Scaling.md)
*   [Load Balancing and Scheduling](concepts/Load_Balancing_and_Scheduling.md)
*   [Barriers and Synchronization](concepts/Barriers_and_Synchronization.md)
*   [Interconnects and Network Topologies](concepts/Interconnects_and_Network_Topologies.md)
*   [Domain Decomposition Overheads](concepts/Domain_Decomposition_Overheads.md)

### Week 8
*   [Manager-Worker Model](concepts/Manager_Worker_Model.md)
*   [MPI Advanced Features](concepts/MPI_Advanced_Features.md)
*   [OpenMP Advanced Work Sharing](concepts/OpenMP_Advanced_Work_Sharing.md)
*   [OpenMP Tasks](concepts/OpenMP_Tasks.md)

### Week 9
*   [BLAS and Dense Matrices](concepts/BLAS_and_Dense_Matrices.md)
*   [Sparse Matrices and CSR](concepts/Sparse_Matrices_and_CSR.md)

### Week 10
*   [Graphics Processing Units (GPUs)](concepts/Graphics_Processing_Units_GPUs.md)
*   [GPU Architecture and Warps](concepts/GPU_Architecture_and_Warps.md)
*   [GPU Programming and OpenMP Offloading](concepts/GPU_Programming_and_OpenMP_Offloading.md)

### Week 11
*   [Hybrid Parallelism (MPI + OpenMP)](concepts/Hybrid_Parallelism_MPI_OpenMP.md)

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
*   [Barriers and Synchronization](concepts/Barriers_and_Synchronization.md) - Explicit and implicit synchronization mechanisms in OpenMP and MPI.
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
*   [Floating Point Arithmetic](concepts/Floating_Point_Arithmetic.md) - Representation of non-integer numbers, IEEE 754 standard, exceptions, and precision.
*   [Memory Hierarchy and Cache](concepts/Memory_Hierarchy_and_Cache.md) - L1/L2/L3 caches, spatial locality, and temporal locality.
*   [Performance Analysis: Problem Size and Memory Footprint](concepts/Performance_Testing_Problem_Size.md) - Why using realistic problem sizes is critical to account for non-linear scaling due to cache boundaries.
*   [Cache Blocking (Loop Tiling)](concepts/Cache_Blocking.md) - Exploiting temporal locality by restructuring loops to work on cache-sized data blocks.
*   [Arithmetic Intensity and the Roofline Model](concepts/Arithmetic_Intensity_and_Roofline_Model.md) - Relationship between FLOPs, memory bandwidth, and performance bounds.
*   [NUMA and First-Touch Policy](concepts/NUMA_and_First_Touch_Policy.md) - Non-uniform memory access across CPU sockets and implications for shared-memory paradigms.
*   [Parallel Scaling](concepts/Parallel_Scaling.md) - Strong vs Weak scaling, Amdahl's Law, and Gustafson's Law.
*   [Load Balancing and Scheduling](concepts/Load_Balancing_and_Scheduling.md) - Minimizing starvation using OpenMP loop scheduling and barriers.
*   [Interconnects and Network Topologies](concepts/Interconnects_and_Network_Topologies.md) - Modeling communication time and exploring HPC network designs like Fat Tree.
*   [Domain Decomposition Overheads](concepts/Domain_Decomposition_Overheads.md) - How communication-to-computation ratios change with sub-domain size.
*   [Manager-Worker Model](concepts/Manager_Worker_Model.md) - Dynamic load balancing pattern using a central queue.
*   [MPI Advanced Features](concepts/MPI_Advanced_Features.md) - Wildcards and custom communicators.
*   [OpenMP Advanced Work Sharing](concepts/OpenMP_Advanced_Work_Sharing.md) - Sections and single thread constructs.
*   [OpenMP Tasks](concepts/OpenMP_Tasks.md) - Unstructured parallelism and the firstprivate clause.
*   [BLAS and Dense Matrices](concepts/BLAS_and_Dense_Matrices.md) - Dense matrices, and the Basic Linear Algebra Subprograms (Levels 1, 2, and 3).
*   [Sparse Matrices and CSR](concepts/Sparse_Matrices_and_CSR.md) - Compressed Sparse Row format for memory-efficient sparse matrix operations.
*   [Graphics Processing Units (GPUs)](concepts/Graphics_Processing_Units_GPUs.md) - Hardware accelerators, energy efficiency, Green500, and PCIe connectivity.
*   [GPU Architecture and Warps](concepts/GPU_Architecture_and_Warps.md) - Streaming Multiprocessors, blocks, warps, SIMD execution, and branch divergence.
*   [GPU Programming and OpenMP Offloading](concepts/GPU_Programming_and_OpenMP_Offloading.md) - Hiding memory latency via over-commitment, data movement, and OpenMP `target` and `map` directives.
*   [Hybrid Parallelism (MPI + OpenMP)](concepts/Hybrid_Parallelism_MPI_OpenMP.md) - Combining MPI for inter-node and OpenMP for intra-node parallelism.

## Comparisons
*   [OpenMP vs. MPI](comparisons/OpenMP_vs_MPI.md) - Comparison between shared-memory (OpenMP) and distributed-memory (MPI) programming paradigms.
*   [Strong vs. Weak Scaling](comparisons/Strong_vs_Weak_Scaling.md) - Detailed comparison of scaling laws (Amdahl vs. Gustafson) and their performance implications.
*   [Finite Difference Stencils: Forward, Backward, and Centered](comparisons/Finite_Difference_Stencils_Comparison.md) - Accuracy (O(Δx) vs O(Δx²)) and stability (FTCS unstable vs upwind CFL-stable) trade-offs for all three first-derivative stencils.
*   [Explicit vs Implicit Time Stepping](comparisons/Explicit_vs_Implicit_Time_Stepping.md) - Forward-Euler (explicit, CFL-constrained, parallel-friendly) vs Backward-Euler (implicit, unconditionally stable, requires linear solve).

## Final Prep
*   [Compute Node Architecture: Cores, Processors, Sockets, and NUMA](final_prep/Compute_Node_Architecture.md) — Hardware hierarchy (core < processor < socket < node), memory controllers, and how multi-socket design causes NUMA.
*   [OpenMP — Complete Exam Reference](final_prep/OpenMP_Complete_Reference.md) — All directives, clauses (scoping, scheduling, GPU map), implicit barriers, data dependency fixes, tasks/sections/offloading patterns across Weeks 2, 7, 8, 10, 11.

## Past Exam Papers
*   [Exams Index (README)](exams/README.md) - Overview of all available past papers and recurring exam themes.
*   [ECM3446 May 2023 — Worked Answers](exams/ECM3446-23May.md) - Full answers with concept backlinks (Top500, CSR, MPI deadlock, scaling, halo exchange).
*   [ECM3446 May 2024 — Worked Answers](exams/ECM3446-24May.md) - Full answers (Mira, MPI_Gather identification, OpenMP vs MPI, Amdahl/Gustafson laws, Memory Intensive Service).
*   [ECM3446 May 2025 — Worked Answers](exams/ECM3446-25May.md) - Full answers (Frontier, OpenMP loop analysis, race-condition fix, diffusion stability, CFL).
*   [ECMM461 May 2021 — Worked Answers (older module)](exams/ECMM461-21May.md) - Full answers (K computer, prefix-sum dependency, ARCHER, advection in 3D, CSR decoding).