---
title: "Arithmetic Intensity and the Roofline Model"
tags: [hpc, week-6, performance, metrics]
date: 2026-05-05
---

# Arithmetic Intensity and the Roofline Model

Not all applications can achieve a system's theoretical peak performance ($R_{peak}$) because they might be limited by the speed at which data can be fed to the CPU (memory bandwidth).

## Arithmetic Intensity
Also known as algorithmic or operational intensity, this is the ratio of floating-point operations performed to data movement (bytes transferred to/from memory). 

### Formula
$$AI = \frac{\text{Floating Point Operations (FLOPs)}}{\text{Data Movement (Bytes)}}$$

*   **Units:** FLOPs / byte.
*   **Low Arithmetic Intensity:** Algorithms that do little work per byte of data (e.g., $AI < 1.0$). These are typically **memory bound**.
*   **High Arithmetic Intensity:** Algorithms that perform many operations per byte loaded. These are typically **compute bound**.

### Examples
*   **Memory Bound:** Vector addition ($C = A + B$) or finite difference stencils. In vector addition, you perform 1 FLOP (addition) for every 24 bytes moved (loading two 8-byte doubles and storing one).
*   **Compute Bound:** Dense matrix-matrix multiplication ($C = A \times B$). The computational complexity is $O(N^3)$ while data movement is $O(N^2)$, meaning AI increases with problem size.

## Roofline Model
The Roofline model is a visual performance model that plots attainable floating-point performance ($P$) as a function of arithmetic intensity ($I$).

### The Limits
The attainable performance is limited by:
$$P = \min(R_{peak}, \text{Bandwidth} \times I)$$

*   **The "Roof":** The horizontal line representing the system's peak compute performance ($R_{peak}$).
*   **The "Slope":** The slanted line representing the system's memory bandwidth.

| Feature | Memory Bound | Compute Bound |
| :--- | :--- | :--- |
| **Arithmetic Intensity** | Low | High |
| **Bottleneck** | Memory Bandwidth | CPU/GPU Peak Speed |
| **Optimization Focus** | Data locality, cache blocking, reducing memory traffic | Vectorization (SIMD), parallelization, loop unrolling |

### The Cache-Aware Roofline Model
In reality, a system doesn't have just one memory bandwidth limit. Modern CPUs have a memory hierarchy (L1, L2, L3 caches, and main DRAM). The speed at which data can be fed to the CPU depends heavily on where that data currently resides.

When we incorporate cache into the Roofline model, it introduces **multiple slanted ceilings** (bandwidth roofs):
*   **L1 Cache Bandwidth:** The steepest slope (fastest data delivery).
*   **L2 / L3 Cache Bandwidth:** Intermediate slopes.
*   **DRAM Bandwidth:** The shallowest slope (slowest data delivery).

**Impact on Performance:**
If an algorithm's working set fits entirely within the L1 or L2 cache, it operates under those higher bandwidth ceilings. This means it can achieve much higher overall floating-point performance even if its arithmetic intensity is relatively low, because the CPU doesn't have to wait as long for data. 

This is the primary motivation for techniques like [Cache Blocking](Cache_Blocking.md) (Loop Tiling). By breaking a large problem into smaller chunks that fit entirely within the L1 or L2 cache, you effectively move the application off the slow DRAM bandwidth curve and up to the faster cache bandwidth curves, significantly raising the ceiling on your potential performance.

By plotting an algorithm's arithmetic intensity against this roofline, developers can immediately see whether their optimization efforts should focus on improving data locality or increasing the FLOP rate.