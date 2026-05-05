---
title: "OpenMP Tasks"
tags: [hpc, week-8, openmp]
date: 2026-05-05
---

# OpenMP Tasks

Introduced in OpenMP 3.0, **Task-based parallelism** handles irregular or unstructured parallelism where the amount of work isn't known in advance (e.g., `while` loops, traversing linked lists, or recursive functions).

## Generating and Executing Tasks
A task is a discrete unit of work. In the standard pattern:
1.  A parallel region is opened, creating a team of threads.
2.  A `#pragma omp single` block ensures that **only one thread** executes the task generation loop.
3.  Inside the loop, `#pragma omp task` is used to define the work unit. The generating thread packages the code and its data environment and places it in a task queue.
4.  The other threads in the team (and the generating thread, once it finishes creating tasks) pull tasks from the queue and execute them concurrently.

## The `firstprivate` Clause
Because tasks are executed asynchronously, loop variables (like an iterator `i`) might change between the time the task is generated and the time it is executed.
To fix this, the `firstprivate(i)` clause is used with `#pragma omp task`. It creates a private copy of the variable for the task and initializes it with the value it had at the exact moment the task was encountered and generated.