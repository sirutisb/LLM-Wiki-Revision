---
title: "Week 8 Summary: Manager-Worker and Task-Based Parallelism"
tags: [hpc, week-8, summary, load-balancing]
date: 2026-05-05
---

# Week 8 Summary: Manager-Worker and Task-Based Parallelism

This week explores flexible alternatives to standard data parallelism (like simple parallel loops or static domain decomposition). By using dynamic work distribution, applications can avoid starvation and achieve better load balancing.

## Key Concepts Covered
*   **Manager-Worker Model:** A dynamic load-balancing pattern where a central manager process distributes small units of work to worker processes upon request.
*   **Advanced MPI Features:** Implementing the manager-worker pattern requires wildcards (`MPI_ANY_SOURCE`, `MPI_ANY_TAG`) to handle asynchronous requests. It also introduces custom MPI Groups and Communicators to isolate worker-only collective communications.
*   **Advanced OpenMP Work Sharing:** Moving beyond parallel loops using `#pragma omp sections` (for concurrent distinct code blocks) and `#pragma omp single` (for single-thread execution within a parallel region).
*   **OpenMP Tasks:** Using `#pragma omp task` to handle unstructured parallelism, such as `while` loops, linked lists, or recursive algorithms, where the total amount of work isn't known ahead of time.