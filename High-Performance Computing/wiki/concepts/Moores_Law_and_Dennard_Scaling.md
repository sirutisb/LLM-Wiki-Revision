---
title: "Moore's Law and Dennard Scaling"
tags: [hpc, week-1, hardware, parallelism]
date: 2026-05-05
---

# Moore's Law and Dennard Scaling

Understanding trends in processor design explains the fundamental requirement for parallelism in modern computing.

## Moore's Law
*   **Definition:** "The number of transistors incorporated in a chip will approximately double every 24 months" (Gordon Moore).
*   **Status:** It became a target for the semiconductor industry. While progress is getting more difficult, transistor density continues to increase. We get more processor cores per chip.

## Dennard Scaling
*   **Definition:** A scaling rule stating that power per unit area (power density) stays constant as transistors scale to smaller sizes. As transistors became smaller, they also became faster (delay reduction) and more energy-efficient (reduced threshold voltage).
*   **Breakdown:** With very small features, physical limits (e.g., leakage current) are reached.
*   **Status:** Dennard scaling has broken down. Consequently, processor clock speeds (frequencies) are no longer increasing.

## The Need for Parallelism
Because Dennard scaling has stopped (clock speeds stalled) but Moore's law continues (transistor counts increase), modern processors achieve performance gains by increasing the *number of cores* per chip rather than individual core speed. To use modern multi-core processors efficiently and achieve high performance, parallel programming is required.