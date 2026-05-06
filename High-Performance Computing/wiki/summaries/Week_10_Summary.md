---
title: "Week 10 Summary: Accelerators and GPUs"
tags: [summary, hpc, week-10, gpu, hardware]
date: 2026-05-05
---

# Week 10 Summary: Accelerators and GPUs

## Overview
This week explores the role of accelerators, specifically Graphics Processing Units (GPUs), in High-Performance Computing. It covers their hardware architecture, energy efficiency, and the programming models required to offload computational workloads from the host CPU to the GPU device.

## Key Topics

*   **[Accelerators and GPUs](../concepts/Graphics_Processing_Units_GPUs.md):** GPUs offer superior floating-point performance, high memory bandwidth, and excellent energy efficiency compared to CPUs. This makes them a dominant component in modern supercomputers (e.g., Exascale systems like Frontier) and dominant on the Green500 list.
*   **GPU Connectivity:** GPUs are physically separate from CPUs and have their own memory. They are typically connected via the PCIe bus, which has high latency. Proprietary connections like NVIDIA's NVLink offer better bandwidth. Minimizing data transfer between the host (CPU) and device (GPU) is critical for performance.
*   **[NVIDIA Pascal Architecture](../concepts/GPU_Architecture_and_Warps.md):**
    *   Composed of Streaming Multiprocessors (SMs).
    *   Features high bandwidth memory and L2 cache.
    *   **[Threads and Warps](../concepts/GPU_Architecture_and_Warps.md):** Threads are grouped into blocks (up to 1024 threads) that execute on the same SM and share memory. Blocks are divided into **warps** (32 threads). All threads in a warp execute the same instructions simultaneously (SIMD).
*   **[GPU Programming Principles](../concepts/GPU_Programming_and_OpenMP_Offloading.md):**
    *   **Data Movement:** Crucial to minimize PCIe transfers.
    *   **Hiding Latency:** Unlike CPUs that use large caches, GPUs hide memory latency by over-committing cores and rapidly context-switching between threads.
    *   **Branching:** Highly detrimental to performance. If threads in a warp take different branches (branch divergence), they must execute serially.
*   **Programming Models:** Standard languages require extensions for GPUs. Options include CUDA (NVIDIA), HIP (AMD), OpenCL, OpenACC, and OpenMP.
*   **[OpenMP Offloading](../concepts/GPU_Programming_and_OpenMP_Offloading.md):** Using `#pragma omp target teams distribute` to offload work to the GPU. The `map` clause (`map(to:)`, `map(from:)`) explicitly controls data movement between host and device memory to optimize performance.