---
title: "Load Balancing and Scheduling"
tags: [hpc, week-7, openmp, performance]
date: 2026-05-05
---

# Load Balancing and Scheduling

If parallel work is unevenly distributed, some threads will finish early and sit idle while waiting for others, leading to **starvation** and wasted resources.

## Barriers and Synchronisation in OpenMP
(See also: [Barriers and Synchronization](../concepts/Barriers_and_Synchronization.md) for a broader comparison including MPI).

*   **Implicit Barriers:** OpenMP automatically places a barrier at the end of parallel regions and work-sharing constructs (like `#pragma omp for`). Threads wait here until all threads have arrived.
*   `nowait` **Clause:** Can be appended to work-sharing constructs (e.g., `#pragma omp for nowait`) to remove the implicit barrier, allowing threads to proceed immediately. Must be used with care to avoid data races.
*   **Explicit Barriers:** Inserted manually using `#pragma omp barrier` when synchronization is strictly required.

## OpenMP Loop Scheduling
When using `#pragma omp for`, the `schedule` clause dictates how iterations are assigned to threads to balance the load.
*   `schedule(static, chunk)`: Iterations are divided into blocks of size `chunk` and assigned to threads in a round-robin fashion at compile time. Low overhead, but poor for unbalanced workloads.
*   `schedule(dynamic, chunk)`: Threads grab a new chunk of iterations dynamically at runtime as soon as they finish their current chunk. Excellent for load balancing, but introduces higher parallel overhead.
*   `schedule(guided, chunk)`: A hybrid approach where the chunk size starts large and exponentially decreases (down to the minimum `chunk` size) as unassigned iterations diminish.