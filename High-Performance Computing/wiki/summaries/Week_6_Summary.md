---
title: "Week 6 Summary: Memory and Cache"
tags: [hpc, week-6, summary]
date: 2026-05-05
---

# Week 6 Summary: Memory and Cache

This week covers how the memory subsystem significantly impacts the real-world performance of HPC applications, shifting the focus from theoretical peak compute ($R_{peak}$) to memory bandwidth and memory access patterns.

## Key Concepts Covered
*   **[Memory Hierarchy and Cache](../concepts/Memory_Hierarchy_and_Cache.md):** The gap between fast CPU speeds and slow main memory, and how L1/L2/L3 caches mitigate this latency.
*   **Locality of Reference:** Exploiting spatial locality (accessing contiguous memory, e.g., stride-one arrays) and temporal locality (re-using recently accessed data, e.g., via cache blocking) to maximize cache hits.
*   **[Arithmetic Intensity](../concepts/Arithmetic_Intensity_and_Roofline_Model.md):** The ratio of floating-point operations to data movement (FLOPs/byte). Helps determine if an algorithm is compute-bound or memory-bound.
*   **[Roofline Model](../concepts/Arithmetic_Intensity_and_Roofline_Model.md):** A visual performance model connecting peak performance, memory bandwidth, and arithmetic intensity.
*   **[NUMA (Non-Uniform Memory Access)](../concepts/NUMA_and_First_Touch_Policy.md):** The phenomenon in multi-socket architectures where memory access times vary depending on which memory controller physically holds the data.
*   **[First-Touch Allocation Policy](../concepts/NUMA_and_First_Touch_Policy.md):** Physical memory is allocated on the memory controller of the CPU that first writes to ("touches") it, which is critical for OpenMP performance.
*   **Hybrid Parallelism:** Combining MPI (one process per socket) and OpenMP (threads within the socket) to avoid crossing NUMA domains.