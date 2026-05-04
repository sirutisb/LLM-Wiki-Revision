---
title: "NUMA and First-Touch Policy"
tags: [hpc, week-6, architecture, openmp, mpi]
date: 2026-05-05
---

# NUMA and First-Touch Policy

**NUMA (Non-Uniform Memory Access)** is a hardware design phenomenon where the time it takes a processor to access memory depends on the memory's physical location relative to the processor.

## Multi-Socket Architecture
In modern HPC compute nodes, which typically have multiple processor sockets, each CPU has its own integrated memory controller.
*   **Local Access:** Accessing memory attached directly to the local CPU's memory controller is fast.
*   **Remote Access:** Accessing memory attached to another CPU's memory controller is slower because the request must traverse an interconnect between the CPUs.

## First-Touch Memory Allocation Policy
Operating systems typically allocate physical memory when it is first accessed ("touched" or written to), not when it is requested (e.g., via `malloc`).
Under a **first-touch allocation policy**, memory pages are physically placed on the memory controller of the CPU core that executes the first write instruction to that page.

## Implications for OpenMP
If a shared array in an OpenMP program is initialized sequentially by a single master thread (e.g., thread 0), all the memory pages for that array will be mapped to the socket where the master thread is running. When parallel worker threads on other sockets subsequently access that array, they will suffer a performance penalty due to remote memory access.

## Hybrid Parallelism (MPI + OpenMP)
To mitigate NUMA effects while leveraging shared-memory parallelism, a common strategy is **Hybrid Parallelism**:
*   Launch one **MPI process per socket**.
*   Spawn **OpenMP threads** strictly within that socket.
Since MPI processes have independent address spaces, this ensures that each process allocates its memory locally on its own socket, and its OpenMP threads only access that local memory.