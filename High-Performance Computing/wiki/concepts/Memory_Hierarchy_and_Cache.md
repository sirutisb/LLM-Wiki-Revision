---
title: "Memory Hierarchy and Cache"
tags: [hpc, week-6, hardware, architecture]
date: 2026-05-05
---

# Memory Hierarchy and Cache

Accessing main memory is slow compared to CPU execution speeds (taking ~100 clock cycles). To prevent the CPU from stalling while waiting for data, modern architectures use a **memory hierarchy**.

## Cache
A cache is a small amount of fast, expensive memory located close to or on the CPU, holding frequently used data from main memory. CPUs typically have multiple cache levels (L1, L2, L3) balancing speed, size, and cost.

## Locality of Reference
To make effective use of cache, programs must exhibit predictability in how they access data.

*   **Spatial Locality:** Data located near recently accessed data in memory is likely to be used next. Data is moved from main memory to cache in fixed-size chunks called **cache lines** (e.g., 64 bytes). To exploit spatial locality, applications should access memory sequentially (e.g., iterating over arrays with a "stride of one"). In C, this means having the inner loop iterate over the last index of a multi-dimensional array.
*   **Temporal Locality:** Data accessed recently is likely to be accessed again soon. A common technique to exploit this is **cache blocking** (or loop tiling), which involves breaking down large workloads into smaller, cache-sized blocks, ensuring data remains in the cache while being operated on repeatedly.

Performance test cases should accurately represent real-world memory footprints, as cache sizes can cause nonlinear performance scaling when problem sizes change.