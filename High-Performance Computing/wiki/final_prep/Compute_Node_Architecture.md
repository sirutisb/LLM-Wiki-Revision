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

| Level                    | What it is                                                                                                                              |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Core**                 | The individual execution unit — runs instructions. One chip contains many.                                                              |
| **Processor (CPU chip)** | A physical chip containing many cores, shared cache, and an integrated memory controller. Typically 8–64+ cores per chip in modern HPC. |
| **Socket**               | A physical slot on the motherboard that holds one processor chip. "Dual-socket" = two CPU chips on one board.                           |
| **Node**                 | One complete physical machine (motherboard + all its sockets + all RAM). Connected to other nodes via an interconnect.                  |

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

See also: [NUMA and First-Touch Policy](../concepts/NUMA_and_First_Touch_Policy.md), [Hybrid Parallelism (MPI + OpenMP)](../concepts/Hybrid_Parallelism_MPI_OpenMP.md), [Cluster Architecture](../concepts/Cluster_Architecture.md)

---

## NUMA in Depth

### What NUMA Is

**NUMA (Non-Uniform Memory Access)** is the consequence of multi-socket design: because each socket has its own memory controller and its own RAM bank, access time depends on *where* the memory physically lives relative to the requesting core.

- Core on Socket 0 reads RAM Bank 0 → fast (local, through its own controller)
- Core on Socket 0 reads RAM Bank 1 → slow (remote, must traverse the cross-socket link to Socket 1's controller, wait for it to service the request, and return the data)

The word "non-uniform" is the key: memory access is not a constant-time operation across the whole node.

---

### When Memory Is Actually Allocated: First-Touch Policy

A critical and often misunderstood point:

> **`malloc` (or array declaration) does not immediately place memory anywhere in physical RAM.**

When you call `malloc`, the OS gives you a *virtual address reservation* — a promise that memory exists. No physical RAM page is assigned yet. The physical page is only allocated the **first time that page is actually read or written** — i.e., the first "touch."

Under the **first-touch policy** (the default on Linux HPC systems), that physical page is placed on the **memory controller closest to the core that performed the first touch**.

```
int *arr = malloc(N * sizeof(int));   // ← NO physical allocation yet
                                      //   just a virtual address reservation

arr[0] = 0;                           // ← FIRST TOUCH of this page
                                      //   physical page now allocated on the
                                      //   memory controller of whichever core
                                      //   ran this line
```

Once a page is placed, it stays there for the lifetime of the allocation — it does not migrate automatically when other sockets access it.

---

### The OpenMP Trap

The classic mistake in OpenMP programs:

```c
// Initialisation done by master thread (Socket 0, core 0)
for (int i = 0; i < N; i++) arr[i] = 0.0;   // all pages → RAM Bank 0

// Parallel computation — threads spread across both sockets
#pragma omp parallel for
for (int i = 0; i < N; i++) result[i] = arr[i] * 2.0;
```

Step 1 runs on one thread → all pages of `arr` are first-touched by Socket 0 → all land in RAM Bank 0. In step 2, the OpenMP threads on Socket 1 must fetch every element of `arr` via the slow cross-socket link. You get NUMA penalty on every single memory access in the hot loop, even though the computation itself is embarrassingly parallel.

**The fix — parallel initialisation:**

```c
// Initialise in parallel so each thread first-touches its own portion
#pragma omp parallel for
for (int i = 0; i < N; i++) arr[i] = 0.0;
```

Now thread 0 (Socket 0) first-touches indices 0..N/2, and thread 8 (Socket 1) first-touches indices N/2..N. Pages are spread across both RAM banks. In the later parallel computation, each thread reads from its local bank → no remote penalty.

---

### Best Practice: MPI Per Socket

The cleanest NUMA mitigation is **one MPI process per socket**, with OpenMP threads confined within that socket:

- Each MPI process has an entirely independent address space — it calls its own `malloc`, performs its own first-touches, and all its pages land on its local socket's RAM.
- OpenMP threads spawned within that process all share that local memory and never need to cross a socket boundary.
- No cross-socket traffic at all, regardless of initialisation order.

This is why hybrid MPI+OpenMP is the standard pattern on multi-socket HPC nodes, not pure OpenMP across all cores.
