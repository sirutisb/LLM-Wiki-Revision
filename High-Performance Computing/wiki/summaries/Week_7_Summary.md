---
title: "Week 7 Summary: Factors Affecting Parallel Performance"
tags: [hpc, week-7, summary, performance]
date: 2026-05-05
---

# Week 7 Summary: Factors Affecting Parallel Performance

This week categorizes the sources of performance degradation in parallel applications and models their limits using scaling laws.

## Key Concepts Covered
*   **Performance Degradation (SLOW):** Real-world parallel performance is limited by **S**tarvation (insufficient/uneven work), **L**atency (memory/network delays), **O**verhead (extra parallel work), and **W**aiting (contention for shared resources).
*   **[Parallel Scaling](../concepts/Parallel_Scaling.md):** Definitions of parallel speed-up and efficiency.
*   **[Amdahl's Law & Strong Scaling](../concepts/Parallel_Scaling.md):** Strong scaling fixes the total problem size. Amdahl's Law models maximum speed-up based on the strict sequential fraction of the program.
*   **[Gustafson's Law & Weak Scaling](../concepts/Parallel_Scaling.md):** Weak scaling fixes the problem size per processor. Gustafson's Law provides a more optimistic view of scaling for large problems.
*   **[Load Balancing & Scheduling](../concepts/Load_Balancing_and_Scheduling.md):** Handling starvation by balancing workloads. In OpenMP, this is managed via loop scheduling (`static`, `dynamic`, `guided`) and explicit/implicit barriers.
*   **[Interconnects & Messages](../concepts/Interconnects_and_Network_Topologies.md):** Modelling communication time as $t = L + M/B$ (Latency + Message/Bandwidth).
*   **[Domain Decomposition Overhead](../concepts/Domain_Decomposition_Overheads.md):** Analyzing how the communication-to-computation ratio scales ($1/N$) as sub-domains shrink during strong scaling.