---
title: "MPI Collective Communication"
tags: [hpc, week-4, mpi, communication]
date: 2026-05-05
---

# MPI Collective Communication

MPI collective communications involve operations that act across a group of processes defined by a communicator. These operations are typically more convenient and efficient than manually constructing the equivalent logic using multiple point-to-point calls. All processes in the specified communicator must call the collective function, otherwise, a deadlock will occur (for blocking collectives).

## Types of Collective Operations

### Broadcast (One-to-All)
Sends identical data from one process (the root) to all other processes in the communicator.
*   `MPI_Bcast(void *buffer, int count, MPI_Datatype datatype, int root, MPI_Comm comm)`

### Scatter (One-to-All, Segmented)
Distributes different subsets of a data array from one root process to all processes in the communicator. Each process receives a portion of the data.
*   `MPI_Scatter(...)`

### Gather (All-to-One / All-to-All)
Collects subsets of data from all processes in the communicator.
*   **`MPI_Gather(...)`**: (All-to-One) Gathers data from all processes and stores the combined data array on a single root process.
*   **`MPI_Allgather(...)`**: (All-to-All) Gathers data from all processes and distributes the complete collected array to *every* process in the communicator.

### Reduction (All-to-One / All-to-All)
Performs a global computation (e.g., sum, max, min, logical operations) across values provided by all processes.
*   **`MPI_Reduce(...)`**: (All-to-One) Carries out a reduction using a specified operator (e.g., `MPI_SUM`, `MPI_MAX`) and returns the final result only to the root process.
*   **`MPI_Allreduce(...)`**: (All-to-All) Carries out the reduction and returns the final result to *all* processes.

Using collectives like `MPI_Allgather` or `MPI_Allreduce` involves a higher communication overhead compared to their single-root counterparts but is necessary when all processes need the resulting global data.