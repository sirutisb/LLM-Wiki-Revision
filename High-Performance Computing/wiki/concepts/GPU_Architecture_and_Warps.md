---
title: "GPU Architecture and Warps"
tags: [hpc, week-10, gpu, hardware, architecture]
date: 2026-05-05
---

# GPU Architecture and Warps

To understand how to program GPUs effectively, it is necessary to understand their physical architecture. We use the **NVIDIA Pascal** architecture as a representative example of a GPU designed for HPC.

## Streaming Multiprocessors (SMs)
A GPU comprises multiple **Streaming Multiprocessors (SMs)** (e.g., up to 60 in a Pascal GPU). These are grouped into Graphics Processing Clusters. 
*   The GPU features high-bandwidth memory (e.g., 720 GB/s) and an L2 cache.

## Thread Hierarchy: Blocks and Warps
A hardware scheduler (like the GigaThread Engine) handles context switching, which is extremely fast on a GPU compared to a CPU. Threads are organized hierarchically:

1.  **Thread Blocks:** The scheduler assigns blocks of threads (up to 1024 threads per block) to execute on a single SM. 
    *   Threads within the same block can access shared memory, utilize cache, and synchronize with one another.
2.  **Warps:** Within an SM, a thread block is subdivided into **warps** of 32 threads.
    *   **SIMD Execution:** All 32 threads in a warp execute the *exact same instruction* at the same time, but on different data elements. This is a form of Single Instruction, Multiple Data (SIMD) execution.

## Branch Divergence
Because all threads in a warp execute in lockstep, **branching (e.g., if/else statements) is bad for performance**. 
If the threads within a warp evaluate a conditional differently (branch divergence), the hardware must execute the different execution paths serially, masking out the inactive threads for each path. GPUs also lack the complex branch prediction hardware found in CPUs. Therefore, algorithms must be designed to minimize branch divergence within warps.