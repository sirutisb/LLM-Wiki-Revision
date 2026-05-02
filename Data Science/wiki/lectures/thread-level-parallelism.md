---
title: "Lecture: Thread-Level Parallelism"
type: lecture
sources: [tlp]
related: [thread-level-parallelism, openmp, mpi, high-performance-computing]
updated: 2026-05-02
---

# Lecture: Thread-Level Parallelism

*Moving from node-level parallelism down to threads — shared memory with OpenMP for single-node parallelism, message passing with MPI for multi-node distributed parallelism.*

## Slide-by-slide notes

- **(s. 2–4)** **Parallelism levels** — we've seen system (node) level; there's also process, instruction, data, and thread level. Thread-level parallelism (TLP) leverages multi-core processors. Process-level parallelism is expensive (each process has its own memory); threads share memory, making them lighter.
- **(s. 5)** **[[thread-level-parallelism|Parallel architectures]] (Flynn's taxonomy)**:
  - **SISD** — Single Instruction, Single Data: standard uniprocessor.
  - **SIMD** — Single Instruction, Multiple Data: same instruction applied to different data streams simultaneously (GPU cores, vector units).
  - **MIMD** — Multiple Instructions, Multiple Data: each processor fetches its own instructions and operates on its own data — the model for most clusters and multi-core CPUs.
- **(s. 6–8)** **Threads**:
  - A thread is a semi-independent execution stream spawned by a process.
  - Threads share global variables, file descriptors, and heap memory with each other and the parent process.
  - Assigned to different physical cores → parallel speedup.
  - **Shared memory systems**: all threads on one node see the same memory address space. Require cores to share memory (single node).
- **(s. 9–11)** **[[openmp|OpenMP]]**:
  - Industry-standard API for shared-memory parallel programming in C, C++, Fortran.
  - Compiler-directive based — annotate loops/regions, compiler generates parallel code.
  - **Fork-join model**: master thread forks worker threads at a parallel region; workers execute independently; all synchronise (join) at the end.
  - OpenMP programs alternate between parallel regions (fork) and sequential master-only segments (join).
- **(s. 12–13)** **Distributed memory parallelism**:
  - Data is *distributed* across processes — no shared memory.
  - Processes can only see their own data.
  - Processes communicate by passing messages.
  - Each process can send data to another process explicitly.
- **(s. 14–20)** **[[mpi|MPI]] (Message Passing Interface)**:
  - Standard library specification for distributed-memory parallel programming.
  - **Communicator** — an object connecting a group of processes. Has: context (unique ID), group (set of processes), size, and ranks (0-indexed integer ID per process).
  - **MPI_COMM_WORLD** — the default communicator containing all processes.
  - **Groups** — the set of all processes managed by a communicator.
  - **Ranks** — unique integer IDs assigned to each process in a communicator.
  - Processes can belong to multiple communicators.
- **(s. 20)** **Point-to-point communication** — one process (sender) posts a message to another (receiver). Two-sided: both sender and receiver must participate (send + receive). Must specify data and destination rank.

## Key takeaways

1. **SISD / SIMD / MIMD** — Flynn's taxonomy for parallel architecture. Know all three.
2. **Threads are lightweight** — they share memory with the parent process; spawning is cheap compared to new processes.
3. **OpenMP = shared memory, single node** — fork-join model, compiler directives, implicit parallelism.
4. **MPI = distributed memory, multi-node** — explicit message passing, two-sided communication, processes have private memory.
5. **Communicators** are MPI's fundamental group abstraction — every message goes through a communicator; each process has a rank within it.
6. **MPI_COMM_WORLD** contains all processes in the session.

## Concepts introduced

- [[thread-level-parallelism]]
- [[openmp]]
- [[mpi]]

## Open questions / things to clarify

- Collective operations in MPI (broadcast, scatter, gather, reduce) are not covered in the slide text — these are extensions of the point-to-point model.
- OpenMP thread safety and race conditions (critical sections, atomic) are not detailed.

## See also

- [[high-performance-computing]]
- [[amdahls-law]]
- [[communication-patterns]]
