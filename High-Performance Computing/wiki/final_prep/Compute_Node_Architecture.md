---
title: "Compute Node Architecture: Cores, Processors, Sockets, and NUMA"
tags: [hpc, week-1, week-6, architecture, numa, memory]
date: 2026-05-13
---

# Compute Node Architecture: Cores, Processors, Sockets, and NUMA

## The Hardware Hierarchy

From smallest to largest:

```
Core < Processor (CPU chip) < Socket < Node
```

| Level | What it is |
|---|---|
| **Core** | The individual execution unit — runs instructions. One chip contains many. |
| **Processor (CPU chip)** | A physical chip containing many cores, shared cache, and an integrated memory controller. Typically 8–64+ cores per chip in modern HPC. |
| **Socket** | A physical slot on the motherboard that holds one processor chip. "Dual-socket" = two CPU chips on one board. |
| **Node** | One complete physical machine (motherboard + all its sockets + all RAM). Connected to other nodes via an interconnect. |

A **dual-socket node with 16-core CPUs** = 1 node, 2 sockets, 2 processor chips, 32 cores total. It is **not** a 2-core node.

---

## Compute Node

A **compute node** is one physical machine in a cluster. It provides the processor cores and memory used to run workloads. Clusters chain together hundreds or thousands of these nodes via a high-speed interconnect (e.g., Infiniband).

---

## Socket

A socket holds one processor chip. In a multi-socket node, the two (or more) chips sit on the same motherboard and can communicate via a CPU-to-CPU link (e.g., Intel QPI, AMD Infinity Fabric). Each socket has:

- Its own bank of RAM physically attached to it.
- Its own **memory controller** managing that RAM.

The CPU-to-CPU link is slower than accessing local RAM — this asymmetry is the source of NUMA.

---

## Memory Controller

Each processor chip has an **integrated memory controller** — hardware that manages all reads/writes to the RAM physically attached to that socket. It handles addressing, scheduling, and timing for its local memory bank.

Because each socket has its own controller, a CPU accessing the *other* socket's RAM must route the request through that remote socket's memory controller — adding latency. There is no shortcut.

---

## How They Connect: NUMA

```
Node (one physical machine)
├── Socket 0 ──── Memory Controller 0 ──── RAM Bank 0   ← fast for CPU 0
│      └── CPU 0 (e.g. 16 cores)
│                      ↕  slow cross-socket link
└── Socket 1 ──── Memory Controller 1 ──── RAM Bank 1   ← fast for CPU 1
       └── CPU 1 (e.g. 16 cores)
```

- CPU 0 → RAM Bank 0 = **local access, fast**
- CPU 0 → RAM Bank 1 = **remote access, slow** (crosses to Socket 1's memory controller)

This is **NUMA (Non-Uniform Memory Access)**: memory access time is not uniform — it depends on which socket's RAM you are accessing.

---

## NUMA Penalty in OpenMP

If a shared array is initialised sequentially by the master thread (on Socket 0), all its pages are allocated on RAM Bank 0. When OpenMP threads on Socket 1 access that array, they pay the remote-access penalty on every read.

**Fix:** Initialise the array in parallel so each thread (on its own socket) touches its portion first — pages are then placed locally via the **first-touch policy**.

---

## Best Practice: MPI Per Socket

The cleanest NUMA mitigation is **one MPI process per socket**, with OpenMP threads confined within that socket:

- Each MPI process has an independent address space → allocates its own local memory.
- OpenMP threads within that process only touch that process's local RAM.
- No cross-socket traffic.

See also: [NUMA and First-Touch Policy](../concepts/NUMA_and_First_Touch_Policy.md), [Hybrid Parallelism (MPI + OpenMP)](../concepts/Hybrid_Parallelism_MPI_OpenMP.md), [Cluster Architecture](../concepts/Cluster_Architecture.md)
