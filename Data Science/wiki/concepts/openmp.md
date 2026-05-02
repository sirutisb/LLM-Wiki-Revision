---
title: "OpenMP"
type: concept
sources: [tlp]
related: [thread-level-parallelism, mpi, high-performance-computing]
updated: 2026-05-02
---

# OpenMP

*A shared-memory parallel programming API using compiler directives — annotate a region, the compiler forks threads, they execute in parallel, then join. Simple, implicit, single-node.*

## Definition

**OpenMP** (Open Multi-Processing) is an API for shared-memory parallel programming, supporting C, C++, and Fortran. Parallelism is *implicit* — the programmer annotates code regions with pragmas (compiler directives), and the compiler generates parallel code that spawns threads on available cores.

## Why it matters

Writing efficient parallel code from scratch with raw threads (pthreads) is complex and error-prone. OpenMP abstracts the thread management — you specify *what* to parallelise and the compiler handles *how*.

## Mechanism — fork-join model

```
Master thread ──────► [Fork] ──► Worker 1
                              ──► Worker 2
                              ──► Worker 3
                                   (all compute in parallel)
                       [Join] ◄────────────────────
Master thread ──────► (continue sequentially)
```

1. Program begins with a single **master thread**.
2. At a `#pragma omp parallel` region, the master **forks** N worker threads.
3. Workers execute the parallel region independently on different data.
4. Workers **synchronise** at the end of the region (implicit barrier).
5. Master continues solo after the join.

OpenMP programs are sequences of parallel fork-join sections separated by sequential master-thread segments.

## Key properties

- **Single-node** — threads share memory; requires a multi-core processor.
- **Implicit** — thread count, scheduling, and synchronisation are handled by the runtime.
- **Incremental parallelism** — add `#pragma omp parallel for` before loops to parallelise incrementally.

## Trade-offs

- **+** Easy to add parallelism to existing serial code.
- **+** Implicit thread management.
- **−** Single-node only — does not scale beyond one machine's shared memory.
- **−** Race conditions on shared data require care (critical sections, atomic).

## Examples in the syllabus

- TLP s. 9–11: OpenMP described as the standard shared-memory API with fork-join model.

## Common exam framing

- "Describe the fork-join model used by OpenMP."
- "What type of parallelism does OpenMP support and what is its limitation?"

## See also

- [[thread-level-parallelism]]
- [[mpi]]
