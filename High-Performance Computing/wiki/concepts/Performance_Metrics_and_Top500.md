---
title: "Performance Metrics and Top500"
tags: [hpc, week-1, metrics, benchmarking]
date: 2026-05-05
---

# Performance Metrics and Top500

## Measuring Performance
No single number fully captures all aspects of performance. Different metrics and benchmarks exist depending on what is being measured.

## FLOPs
HPC applications perform many operations on floating-point numbers. Performance is often measured in **flops** (floating point operations per second). Today's fastest systems achieve 10's to 100's of petaflops ($10^{15}$ flops).

## Linpack & HPL
*   **Linpack:** A performance benchmark that measures flops using a dense linear algebra workload.
*   **HPL (High-Performance Linpack):** A widely used parallel version of Linpack used to benchmark HPC systems.

## The Top500 List
*   The fastest known machines in the world appear in the **Top 500** list.
*   Published twice a year.
*   Ranks HPC systems according to their HPL (Linpack) performance.
*   It serves as a long-term dataset revealing global trends in HPC since the mid-1990s. Performance growth has historically been exponential.

## Peak Performance ($R_{peak}$)
The theoretical maximum performance of a system is known as the peak performance ($R_{peak}$). While Top500 ranks systems based on actual benchmarked performance ($R_{max}$), it also reports $R_{peak}$.

We can calculate $R_{peak}$ for a compute node using:
$$ R_{peak} = N_{\text{sockets}} \times N_{\text{cores/socket}} \times R_{\text{clock}} \times N_{\text{operations/cycle}} $$

*   **$N_{\text{operations/cycle}}$**: The number of floating-point operations a core can perform per cycle. This depends on the instruction set (e.g., AVX vector instructions) and whether it supports Fused Multiply-Add (FMA).
To find the total cluster peak performance, simply multiply the compute node $R_{peak}$ by the total number of compute nodes.