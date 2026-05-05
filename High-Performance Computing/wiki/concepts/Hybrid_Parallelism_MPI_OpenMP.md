---
title: "Hybrid Parallelism (MPI + OpenMP)"
tags: [hpc, week-11, mpi, openmp, architecture]
date: 2026-05-05
---

# Hybrid Parallelism (MPI + OpenMP)

Modern high-performance computing (HPC) clusters are hierarchies: they consist of multiple distributed-memory compute nodes connected by a network, where each individual node contains multiple processors that share memory.

To fully exploit this architecture, applications often use **Hybrid Parallelism**, combining [MPI](../concepts/Message_Passing_Interface_MPI.md) and [OpenMP](../concepts/OpenMP.md).

## The MPI + OpenMP Model

*   **MPI (Distributed Level):** MPI handles the coarse-grained parallelism across the cluster. It divides the global problem (e.g., using [Domain Decomposition](../concepts/Domain_Decomposition.md)) across the distributed compute nodes. Each MPI process handles communication (halo exchanges) over the interconnect network.
*   **OpenMP (Shared Level):** OpenMP handles the fine-grained parallelism within each compute node. The MPI process on a node forks OpenMP threads that share the node's memory to process the local data block (e.g., by parallelizing loops).

## Advantages

1.  **Reduced Memory Footprint:** Using only MPI, every process requires its own memory overhead (e.g., storing its own halo boundaries and duplicate variables). By sharing memory within a node using OpenMP, the number of halos required per node decreases, freeing up memory for larger problem sizes.
2.  **Extended Scaling:** Applications often hit a scaling limit with pure MPI (e.g., the domains become too small, leading to high communication overhead). Introducing OpenMP allows scaling to continue further because OpenMP parallelism occurs within the node, independent of the network communication overhead.
3.  **Improved Load Balancing:** OpenMP provides dynamic loop scheduling (`dynamic`, `guided`), which is often easier to implement for localized load imbalances than writing a full manager-worker model in MPI.
4.  **Fewer MPI Messages:** Fewer MPI processes per node means fewer, larger messages sent across the network, which utilizes bandwidth more efficiently and reduces total network latency.