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
**Strong scaling** evaluates performance as the number of processors increases while the **total problem size remains fixed**.

**Amdahl's Law** states that the maximum theoretical speed-up is strictly limited by the fraction of the program that cannot be parallelized ($s$). If $p$ is the parallelizable fraction ($s + p = 1$):
$$ S_N = \frac{1}{s + \frac{p}{N}} $$
As $N \to \infty$, the maximum speed-up is capped at $1/s$. 
We can also include a term for parallel overheads ($V = n_pv$, overhead per region $\times$ number of regions). The speed-up becomes:
$$ S_N = \frac{1}{s + \frac{p}{N} + \frac{n_pv}{T_0}} $$

## Weak Scaling and Gustafson's Law
**Weak scaling** evaluates performance as the number of processors increases while the **problem size per processor remains fixed** (the total problem size grows).

**Gustafson's Law** notes that in practice, larger computers are used to run larger problems. If the parallel portion of the workload scales linearly with $N$:
$$ S_N = s + pN $$
This indicates that massive parallelism is highly effective when the problem size is allowed to grow.