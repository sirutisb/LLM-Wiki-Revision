---
title: "Thread-level parallelism"
type: concept
sources: [tlp]
related: [openmp, mpi, high-performance-computing, amdahls-law]
updated: 2026-05-02
---

# Thread-level parallelism

*Using multiple threads within a single process to exploit multi-core CPUs — lighter than processes, sharing memory, and enabling parallelism without inter-process communication overhead.*

## Definition

**Thread-level parallelism (TLP)** is a programming model that exploits the multiple cores of a modern processor by running multiple threads simultaneously. Threads are semi-independent execution streams spawned by a process that *share* the parent's memory space (global variables, heap, file descriptors) while each having their own stack and program counter.

## Why it matters

Process-level parallelism is expensive — each process has its own memory, and communication between processes requires IPC. Threads are lightweight: spawning is cheap, and shared memory means data doesn't need to be copied between execution units. TLP is the basis for multi-core utilisation on a single node.

## Flynn's taxonomy — parallel architecture classes

| Class | Instructions | Data | Example |
|---|---|---|---|
| **SISD** | Single | Single | Classic uniprocessor |
| **SIMD** | Single | Multiple | GPU cores, CPU vector units (AVX) |
| **MIMD** | Multiple | Multiple | Multi-core CPUs, clusters |

Most HPC/data science workloads run on MIMD machines. SIMD is exploited within each core for vectorised operations (important for ML tensor operations).

## Shared memory vs distributed memory

| | Shared memory (TLP) | Distributed memory |
|---|---|---|
| Scope | Single node | Multiple nodes |
| Data access | All threads see same memory | Each process has private memory |
| Communication | Read/write shared variables | Explicit message passing ([[mpi]]) |
| Parallel API | [[openmp|OpenMP]], pthreads | MPI |

## Examples in the syllabus

- TLP s. 2–8: thread definition, shared memory systems, assigned to different cores.

## Common exam framing

- "Distinguish SISD, SIMD, and MIMD architectures."
- "Why are threads considered lighter-weight than processes?"
- "What does shared memory mean in the context of thread-level parallelism?"

## See also

- [[openmp]]
- [[mpi]]
- [[high-performance-computing]]
