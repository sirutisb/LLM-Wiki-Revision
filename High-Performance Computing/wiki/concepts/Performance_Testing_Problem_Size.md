---
title: "Performance Analysis: Problem Size and Memory Footprint"
tags: [hpc, week-6, performance, benchmarking]
date: 2026-05-07
---

# Problem Size and Memory Footprint

In High-Performance Computing, the size of the test case used for performance analysis is critical. Using an unrepresentative "toy" problem can lead to misleading conclusions because performance scaling is often **non-linear** relative to the **memory footprint**.

## Why Size Matters: The Cache Effect
The primary reason for non-linear scaling is the [Memory Hierarchy and Cache](../concepts/Memory_Hierarchy_and_Cache.md). 

*   **Cache-Resident Problems:** If a test case is small enough that its entire data structure fits into the CPU's L1, L2, or L3 cache, it will run significantly faster because it avoids the ~100 cycle latency of main memory.
*   **Memory-Bound Problems:** Real-world problems often have memory footprints far larger than any cache. Once the problem size exceeds the cache capacity, performance "drops off a cliff" as the CPU becomes starved for data.

### The Benchmarking Trap
If you optimize your code using only small test cases, you might be optimizing for a scenario where data movement isn't a bottleneck. Your optimizations might fail to address the [Arithmetic Intensity](../concepts/Arithmetic_Intensity_and_Roofline_Model.md) issues that will dominate the performance of the full-scale application.

## The Golden Rule: Shorten Execution Time, Not the Footprint

When a production-scale problem takes too long for iterative testing, developers are often tempted to shrink the data size. This is a mistake. Instead, follow this principle: **Maintain the representative data size but reduce the total number of operations.**

### Why this works
By keeping the data size large, you ensure the CPU continues to experience the same memory latency and bandwidth bottlenecks as the production run. Reducing the "work" (e.g., iterations) simply stops the test sooner while preserving the performance characteristics of each individual operation.

### Case Study: Weather Simulation
Imagine a 1km resolution simulation of the UK:
*   **Full Run:** 10 GB memory footprint, simulating 24 hours (1,440 time steps), taking 5 hours to execute.
*   **The Wrong Test (Shrink Footprint):** Reducing resolution to 10km. Memory footprint drops to 100 MB. It now fits in L3 cache. Performance data is misleading because memory bottlenecks have vanished.
*   **The Right Test (Shorten Work):** Keeping 1km resolution (10 GB) but simulating only 10 minutes (10 time steps). The test finishes in minutes, but accurately measures the 10 GB memory bottleneck.

### Application Strategies

| Application Type | Instead of shrinking this (Footprint)... | Shrink this instead (Work)... |
| :--- | :--- | :--- |
| **PDE / CFD Solver** | Grid resolution | Number of time steps |
| **Iterative Solver** | Matrix dimensions | Number of iterations |
| **Big Data / Search** | Size of the database | Number of queries performed |
| **Molecular Dynamics** | Number of atoms | Total simulation time |

## Summary Table: Small vs. Large Test Cases

| Feature | Small (Toy) Test Case | Large (Representative) Test Case |
| :--- | :--- | :--- |
| **Data Residency** | Likely fits in Cache (L1/L2/L3) | Resides in Main Memory (RAM) |
| **Primary Bottleneck** | Instruction throughput / Compute | Memory Bandwidth / Latency |
| **Optimization Focus** | Pipeline, Vectorization | [Cache Blocking](../concepts/Cache_Blocking.md), Data Locality |
| **Predictive Value** | Low (for production runs) | High (for production runs) |
