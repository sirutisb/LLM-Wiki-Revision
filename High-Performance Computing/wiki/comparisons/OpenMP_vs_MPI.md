---
title: "OpenMP vs. MPI"
tags: [hpc, week-4, openmp, mpi, comparison]
date: 2026-05-05
---

# OpenMP vs. MPI

A comparison between the two primary parallel programming paradigms used in High-Performance Computing.

| Feature | OpenMP | MPI |
| :--- | :--- | :--- |
| **Execution Model** | Single instance of a program which forks threads in parallel regions (fork-join model). | Multiple independent copies of a program running concurrently. |
| **Communication** | Shared memory (implicit communication via shared variables). | Message passing (explicit communication via network or memory). |
| **Implementation** | Implemented as compiler directives (`#pragma`) alongside a runtime library. | Implemented as an external library accessed via function calls. |
| **Target Architecture** | Shared-memory systems only (e.g., single multicore node). | Both distributed-memory clusters and shared-memory systems. |
| **Parallelization Strategy** | Suitable for incremental parallelization of existing serial code. | Requires explicit data distribution (e.g., [Domain Decomposition](../concepts/Domain_Decomposition.md)); better if designed in from the start. |

## Advantages and Disadvantages

*   **MPI Advantages**: The most significant advantage of MPI is its ability to scale across distributed-memory cluster architectures, allowing execution across thousands of independent nodes.
*   **MPI Disadvantages**: MPI requires significantly more programming effort. The programmer is completely responsible for data distribution, synchronization, and explicit communication.
*   **OpenMP Advantages**: Much easier to adopt incrementally into an existing codebase.
*   **OpenMP Disadvantages**: Confined to the compute capacity and memory limits of a single node.

## Hybrid Parallelism (MPI + OpenMP)
Because modern HPC clusters consist of distributed nodes that each contain multi-core shared-memory processors, the most effective strategy is often **Hybrid Parallelism**. 
By combining the two, MPI handles the domain decomposition and network communication between nodes, while OpenMP parallelizes the computation across the cores within each node. This approach reduces memory overhead, decreases the number of MPI messages, and can extend scaling limits when pure MPI becomes communication-bound.