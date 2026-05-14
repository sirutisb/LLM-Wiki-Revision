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

## Implementation in Different Paradigms

### MPI (Distributed Memory)
Implementing this in MPI typically requires:
*   **Dedicated Manager:** One rank (usually rank 0) that handles the queue.
*   **Wildcards:** Using [MPI Wildcards](MPI_ANY_SOURCE) so the manager can receive a request from whichever worker finishes first.
*   **Termination:** The manager must send a specific "DIE_TAG" to workers when the queue is empty.
*   **Communicators:** Often requires a [Workers-Only Communicator](MPI_Advanced_Features.md) for collective results.

### OpenMP (Shared Memory)
OpenMP provides two primary ways to apply the Manager-Worker pattern:
1.  **For Loops:** `schedule(dynamic)` handles the distribution automatically. The runtime acts as the manager.
2.  **Irregular Work:** [OpenMP Tasks](OpenMP_Tasks.md) allow one thread (`#pragma omp single`) to act as the manager/generator, while the rest of the team acts as workers pulling from a task queue.

## Trade-offs
| Pros | Cons |
| :--- | :--- |
| Excellent dynamic load balancing | Manager rank in MPI does no compute (waste) |
| Handles irregular work well | Communication overhead per work unit |
| Scales well for medium-to-coarse work | Manager can become a bottleneck if units are too small |

## Related Concepts
*   [Load Balancing and Scheduling](Load_Balancing_and_Scheduling.md)
*   [OpenMP Tasks](OpenMP_Tasks.md)
*   [Parallel Scaling](Parallel_Scaling.md)