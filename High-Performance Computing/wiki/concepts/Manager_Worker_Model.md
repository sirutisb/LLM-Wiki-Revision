---
title: "Manager-Worker Model"
tags: [hpc, week-8, mpi, performance, load-balancing]
date: 2026-05-05
---

# Manager-Worker Model

The Manager-Worker (or Master-Slave) model is a parallel programming pattern designed for dynamic load balancing. It is an alternative to static data parallel approaches like domain decomposition.

## How It Works
1.  **Manager Process:** One process is designated as the manager. It holds the queue of remaining tasks but performs no actual computation.
2.  **Worker Processes:** All other processes are workers. They send a request to the manager, receive a unit of work, compute it, send the result back, and immediately request more work.
3.  **Dynamic Balancing:** Because fast workers naturally request more work, and slow workers request less, the workload dynamically balances itself at runtime. This prevents the starvation that occurs when a strict static decomposition assigns a hard problem to one node and an easy problem to another.

## MPI Implementation Details
Implementing this in MPI typically requires:
*   `while` loops instead of `for` loops on the manager to continuously listen for requests until work is depleted.
*   Using [MPI Wildcards](MPI_Advanced_Features.md) so the manager can receive a request from whichever worker finishes first.
*   Using custom communicators if a collective operation (like `MPI_Reduce`) needs to be performed only across the workers, excluding the manager.