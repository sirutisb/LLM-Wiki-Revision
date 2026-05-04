---
title: "Domain Decomposition"
tags: [hpc, week-4, mpi, algorithms]
date: 2026-05-05
---

# Domain Decomposition

Domain decomposition is a fundamental strategy for parallelizing computations, particularly [Partial Differential Equations (PDEs)](../concepts/Partial_Differential_Equations.md) solvers, across distributed-memory systems using [MPI](../concepts/Message_Passing_Interface_MPI.md). 

Unlike [OpenMP](../concepts/OpenMP.md), which can automatically distribute loop iterations using `#pragma omp for`, MPI requires the programmer to explicitly divide the computational work and data. In domain decomposition, the global computational domain (e.g., a 2D grid) is divided into smaller sub-domains, and each MPI process is assigned one sub-domain to compute.

## Synchronization and Boundary Handling

### Global Parameters
When using domain decomposition, processes often need to agree on global parameters.
*   **Initialization**: The rank zero process typically reads input parameters and initial conditions, then distributes them using collectives like `MPI_Bcast` (for global parameters) and `MPI_Scatter` (for sub-domain initial conditions). Output is usually gathered using `MPI_Gather`.
*   **Time Stepping**: In a PDE solver restricted by a stability constraint (e.g., [Numerical Stability and CFL](../concepts/Numerical_Stability_and_CFL.md)), different domains may calculate different maximum allowable time steps. Since all processes must advance by the same synchronized time step, an `MPI_Allreduce` with the `MPI_MIN` operator is used to find and broadcast the global minimum time step.

### Halo Exchange
When calculating a [Finite Difference Method](../concepts/Finite_Difference_Method.md) stencil, an update for a grid point at the edge of a sub-domain requires values from the adjacent sub-domain.
*   **Halos**: To resolve this, each process stores a "halo" (or ghost region) — an extra copy of the row/column of data belonging to its neighboring processes.
*   **Halo Exchange**: After every time step update, neighboring domains must exchange their boundary values to update their halos. This is typically implemented efficiently using [MPI Non-blocking Communication](../concepts/MPI_Non_blocking_Communication.md) (`MPI_Isend` and `MPI_Irecv`) to avoid deadlocks and overlap communication.