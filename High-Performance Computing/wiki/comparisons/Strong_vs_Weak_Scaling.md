---
title: "Strong Scaling vs. Weak Scaling"
tags: [hpc, scaling, performance, amdahl, gustafson]
date: 2026-05-08
---

# Strong Scaling vs. Weak Scaling

In High-Performance Computing, scaling analysis is critical for understanding how an application's performance changes as computational resources (processors/nodes) are added.

## 1. Strong Scaling (Amdahl's Law)

**Strong scaling** evaluates how the execution time of a program decreases as more processors are added, while the **total problem size remains fixed**.

*   **Primary Goal:** To complete a specific task faster (Latency reduction).
*   **Governing Model:** [Amdahl's Law](../concepts/Parallel_Scaling.md).
*   **Theoretical Limit:** The speedup is capped by the sequential fraction ($s$) of the program. As $N \to \infty$, speedup $S_N \to 1/s$.
*   **Efficiency:** Typically decreases as $N$ increases because the work-per-processor shrinks, making overheads (communication, synchronization) more significant relative to computation.

## 2. Weak Scaling (Gustafson's Law)

**Weak scaling** evaluates how the execution time of a program changes as more processors are added, while the **workload per processor remains constant**. This means the total problem size grows proportionally with the number of processors.

*   **Primary Goal:** To solve larger, more complex problems in a constant amount of wall-clock time (Throughput maximization).
*   **Governing Model:** [Gustafson's Law](../concepts/Parallel_Scaling.md).
*   **Theoretical Limit:** Speedup scales linearly with $N$ ($S_N = s + pN$). There is no theoretical "Amdahl ceiling" if the problem size can grow indefinitely.
*   **Efficiency:** Ideally remains constant at 1.0 (100%), though in practice it may degrade slightly due to increasing communication complexity in larger networks.

## 3. Direct Comparison

| Feature | Strong Scaling (Amdahl) | Weak Scaling (Gustafson) |
| :--- | :--- | :--- |
| **Problem Size** | Fixed total size | Fixed size per processor (Total grows) |
| **Core Metric** | Speedup / Wall-clock time | Time constancy / Parallel Efficiency |
| **Primary Driver** | Time-to-solution (Latency) | Problem complexity (Throughput) |
| **Scaling Limit** | Bottlenecked by serial fraction ($1/s$) | Scalable linearly ($s + pN$) |
| **System View** | Fixed-size machine perspective | Growth-oriented machine perspective |
| **Use Case** | Data processing, real-time response | CFD, weather modeling, molecular dynamics |

## 4. Key Relationships

*   **The "Amdahl Ceiling":** Strong scaling eventually hits a wall where adding more processors provides no benefit (or even degrades performance due to overhead). This is the point where the sequential fraction $s$ dominates.
*   **The "Gustafson Perspective":** Gustafson argued that Amdahl's Law was too pessimistic because users don't keep the problem size fixed; they use more powerful machines to solve more interesting (larger) problems.
*   **Communication-to-Computation Ratio:**
    *   In **Strong Scaling**, this ratio typically **increases** as we scale out, because computation per node shrinks while communication (like halo exchange) often remains constant or grows.
    *   In **Weak Scaling**, this ratio ideally stays **constant**, as both computation and communication volumes scale with the local problem size.

---
**Related Concepts:**
*   [Parallel Scaling](../concepts/Parallel_Scaling.md)
*   [Domain Decomposition Overheads](../concepts/Domain_Decomposition_Overheads.md)
*   [Efficiency and Speedup](../concepts/Parallel_Scaling.md)
