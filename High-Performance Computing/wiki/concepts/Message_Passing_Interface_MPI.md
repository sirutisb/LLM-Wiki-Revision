---
title: "Message Passing Interface (MPI)"
tags: [hpc, week-4, mpi, distributed-memory]
date: 2026-05-05
---

# Message Passing Interface (MPI)

The Message Passing Interface (MPI) is a standard for parallel programming in distributed-memory systems, though it can also be used in shared-memory environments. Unlike [OpenMP](../concepts/OpenMP.md), which uses a single program instance that forks threads, an MPI program consists of multiple copies of the program running as separate processes with isolated memory address spaces. These processes communicate by explicitly passing messages.

## Basic Execution Environment

To use MPI, the environment must be set up and torn down:
*   `MPI_Init(int *argc, char ***argv)`: Must be called once before any other MPI functions. It sets up the MPI environment and passes command-line arguments to all processes.
*   `MPI_Finalize()`: Must be called once to cleanly shut down the MPI environment after all other MPI calls are completed.

## Communicators, Size, and Rank

A **communicator** defines a group of processes that can communicate with each other. The default predefined communicator that includes all concurrent MPI processes is `MPI_COMM_WORLD`.

*   `MPI_Comm_size(MPI_Comm comm, int *size)`: Returns the total number of MPI processes in the specified communicator.
*   `MPI_Comm_rank(MPI_Comm comm, int *rank)`: Returns the unique rank (identifier) of the calling process within the communicator. Ranks are integers ranging from `0` to `size - 1`.

## Building and Running

MPI functions are provided via external libraries (such as OpenMPI or MPICH) with C and Fortran interfaces. 
*   **Compilation:** Typically done using a wrapper script like `mpicc` (e.g., `mpicc -o hello_mpi hello_mpi.c`), which automatically handles include paths, library paths, and necessary compiler flags.
*   **Execution:** Handled by a command like `mpirun` which starts multiple instances of the compiled executable (e.g., `mpirun -np 4 hello_mpi` starts 4 processes).