---
title: "Parallel Scaling"
tags: [hpc, week-7, performance, scaling, amdahl, gustafson]
date: 2026-05-05
---

# Parallel Scaling

To evaluate how effectively a parallel program utilizes hardware resources, we measure its scaling behavior.

## Fundamental Metrics
*   **Parallel Speed-up ($S_N$):** $S_N = \frac{T_0}{T_N}$, where $T_0$ is the serial execution time and $T_N$ is the parallel execution time on $N$ processors.
*   **Parallel Efficiency ($E_N$):** $E_N = \frac{S_N}{N}$. An efficiency of 1.0 (or 100%) represents ideal, linear speed-up.

## Strong Scaling and Amdahl's Law
**Strong scaling** evaluates performance as the number of processors increases while the **total problem size remains fixed**. The goal is to reduce the execution time of a specific task.

### Amdahl's Law Derivation
1.  **Workload Split:** Define the serial execution time $T_0$ as having a sequential fraction $s$ and a parallelizable fraction $p$ ($s + p = 1$).
    $$T_0 = sT_0 + pT_0$$
2.  **Parallel Execution:** On $N$ processors, the sequential part remains $sT_0$, but the parallel part is divided by $N$.
    $$T_N = sT_0 + \frac{pT_0}{N}$$
3.  **Speed-up ($S_N$):** Speed-up is defined as $T_0 / T_N$.
    $$S_N = \frac{T_0}{sT_0 + \frac{pT_0}{N}} = \frac{1}{s + \frac{p}{N}}$$

**Limit:** As $N \to \infty$, the maximum speed-up is capped at $1/s$. This implies that the sequential portion is the ultimate bottleneck.

### Amdahl's Law with Overheads
In reality, parallelization introduces extra work (communication, synchronization). If $V$ is the total parallel overhead (e.g., $V = n_pv$ where $v$ is overhead per region):
$$ S_N = \frac{1}{s + \frac{p}{N} + \frac{V}{T_0}} $$

## Weak Scaling and Gustafson's Law
**Weak scaling** evaluates performance as the number of processors increases while the **problem size per processor remains fixed** (the total problem size grows). The goal is to solve larger problems in a constant amount of time.

### Gustafson's Law Derivation
Gustafson assumed that as we get more processors, we solve bigger problems.
1.  **Normalized Parallel Time:** Define the parallel execution time on $N$ processors as $T_N = 1$. This consists of a sequential part $s$ and a parallel part $p$ (measured as fractions of the parallel time).
    $$T_N = s + p = 1$$
2.  **Hypothetical Serial Time:** To run this same large workload on one processor, the parallel part $p$ would take $N$ times longer.
    $$T_0 = s + pN$$
3.  **Speed-up ($S_N$):**
    $$S_N = \frac{T_0}{T_N} = \frac{s + pN}{1} = s + pN$$

**Linear Scaling:** This suggests that speed-up can scale linearly with $N$, provided the problem size is allowed to grow.

## Comparison Summary

| Feature | Strong Scaling (Amdahl) | Weak Scaling (Gustafson) |
| :--- | :--- | :--- |
| **Problem Size** | Fixed total size | Fixed size per processor |
| **Metric Goal** | Minimize time (Latency) | Maximize workload (Throughput) |
| **Scaling Limit** | Limited by serial fraction ($1/s$) | Theoretically unlimited (Linear $s + pN$) |
| **Perspective** | Pessimistic: "Parallelism is limited" | Optimistic: "Bigger machines for bigger tasks" |
| **Use Case** | Real-time constraints, fixed datasets | Scientific simulations (e.g., weather, CFD) |