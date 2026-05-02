---
title: "MPI (Message Passing Interface)"
type: concept
sources: [tlp]
related: [thread-level-parallelism, openmp, communication-patterns, high-performance-computing]
updated: 2026-05-02
---

# MPI (Message Passing Interface)

*The standard for distributed-memory parallel programming — processes have private memory and communicate explicitly through two-sided messages, coordinated via communicators and ranks.*

## Definition

**MPI** (Message Passing Interface) is a language-independent specification of a library for distributed-memory parallel programs. Processes have their own private address spaces and can only exchange data by explicitly sending and receiving messages. It is the foundation of nearly all large-scale HPC and multi-node distributed computing.

## Why it matters

When multiple nodes must cooperate on a computation but cannot share memory (because they are separate machines), explicit message passing is required. MPI standardises this, enabling portable parallel programs across different clusters and supercomputers.

## Key concepts

### Communicator
An object that connects a group of processes:
- **Context** — a unique identifier that distinguishes one communicator from another.
- **Group** — the set of processes in the communicator.
- **Size** — the number of processes in the group.
- **Rank** — a zero-indexed integer ID assigned to each process. Process 0 = rank 0, etc.

**MPI_COMM_WORLD** is the default communicator that includes *all* processes started in an MPI session.

### Groups
The set of all processes belonging to a communicator. A process can belong to multiple communicators (and thus have different ranks in different communicators).

### Ranks
Each process's unique integer identifier within a communicator. Used to address messages: "send to rank 2".

## Communication model

```
Communicator: MPI_COMM_WORLD
  Rank 0  ──[send]──►  Rank 1 (receiver must call recv)
  Rank 1  ──[send]──►  Rank 2
  ...
```

- **Point-to-point**: one sender, one receiver. The sender specifies the data and the destination rank. The receiver must call `MPI_Recv` to accept the message. Both sides must participate — **two-sided communication**.
- Messages are sent within a communicator context — same-context messages don't interfere with other communicators.

## OpenMP vs MPI

| | OpenMP | MPI |
|---|---|---|
| Memory model | Shared | Distributed (private per process) |
| Scope | Single node | Multiple nodes |
| Communication | Shared variables (implicit) | Explicit messages (two-sided) |
| Complexity | Low | Higher |
| Scales to | ~100s of cores (1 node) | Millions of cores (clusters) |

## Examples in the syllabus

- TLP s. 14–20: MPI concepts defined — communicator, group, rank, point-to-point.

## Common exam framing

- "What is a communicator in MPI? What attributes does it have?"
- "Explain two-sided communication in MPI."
- "What is MPI_COMM_WORLD?"
- "Compare OpenMP and MPI for parallelising a workload."

## See also

- [[thread-level-parallelism]]
- [[openmp]]
- [[communication-patterns]]
