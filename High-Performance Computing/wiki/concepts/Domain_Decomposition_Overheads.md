---
title: "Domain Decomposition Overheads"
tags: [hpc, week-7, mpi, performance, scaling]
date: 2026-05-05
---

# Domain Decomposition Overheads

When a spatial domain is decomposed across MPI processes, processes must communicate boundary data (halo exchange). This introduces communication overhead.

## Scaling of Overheads
For an $N \times N$ 2D sub-domain:
*   Computation (area) $\propto N^2$
*   Communication (perimeter) $\propto 4N$
*   Communication to Computation Ratio $\propto \frac{1}{N}$

For an $N \times N \times N$ 3D sub-domain:
*   Computation (volume) $\propto N^3$
*   Communication (surface area) $\propto 6N^2$
*   Communication to Computation Ratio $\propto \frac{1}{N}$

In both cases, as you **strong scale** the application (keep total domain fixed, increase processor count), the sub-domain size $N$ shrinks. Consequently, the **ratio of communication to computation increases**, which eventually limits parallel scaling.

## Super-linear Speed-up
Occasionally, strong scaling can result in super-linear speed-up ($E_N > 1$). This typically happens when the shrinking sub-domain size $N$ suddenly allows a critical data structure to fit entirely within the processor's high-speed memory **cache**, dramatically reducing memory latency.