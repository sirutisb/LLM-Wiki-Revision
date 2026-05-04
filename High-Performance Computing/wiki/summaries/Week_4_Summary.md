---
title: "Week 4 Summary: Introduction to MPI"
tags: [hpc, week-4, mpi]
date: 2026-05-05
---

# Week 4 Summary: Introduction to MPI

This week introduces the Message Passing Interface (MPI), which enables parallel programming on distributed memory systems (such as clusters) by passing messages between multiple instances of a program, each with separate memory address spaces.

## Key Concepts Covered
*   **[Message Passing Interface (MPI)](../concepts/Message_Passing_Interface_MPI.md):** The basics of initializing and finalizing the MPI environment, determining process rank and total size, and compiling/running MPI programs.
*   **[MPI Point-to-Point Communication](../concepts/MPI_Point_to_Point_Communication.md):** Communication between a specific pair of MPI processes using blocking operations like `MPI_Send` and `MPI_Recv`.
*   **[MPI Collective Communication](../concepts/MPI_Collective_Communication.md):** Communication operations that involve a group of MPI processes (a communicator), including broadcast, scatter, gather, and reduction operations.
*   **[MPI Non-blocking Communication](../concepts/MPI_Non_blocking_Communication.md):** Operations like `MPI_Isend` and `MPI_Irecv` that do not block the program, allowing overlapping of computation with communication and helping avoid deadlocks.
*   **[Domain Decomposition](../concepts/Domain_Decomposition.md):** A technique to distribute computational work (such as solving PDEs) among multiple MPI processes, requiring the use of "halo" exchanges to communicate boundary values.
*   **[OpenMP vs. MPI](../comparisons/OpenMP_vs_MPI.md):** A comparison between the shared memory model of OpenMP and the distributed memory model of MPI.