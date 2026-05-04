---
title: "Arithmetic Intensity and the Roofline Model"
tags: [hpc, week-6, performance, metrics]
date: 2026-05-05
---

# Arithmetic Intensity and the Roofline Model

Not all applications can achieve a system's theoretical peak performance ($R_{peak}$) because they might be limited by the speed at which data can be fed to the CPU (memory bandwidth).

## Arithmetic Intensity
Also known as algorithmic or operational intensity, this is the ratio of floating-point operations performed to data movement (bytes transferred to/from memory). 
*   **Units:** FLOPs / byte.
*   Algorithms with **low arithmetic intensity** (e.g., basic vector addition or finite difference stencils) are typically **memory bound**.
*   Algorithms with **high arithmetic intensity** (e.g., dense matrix multiplication) perform many operations per byte loaded, making them **compute bound**.

## Roofline Model
The Roofline model is a visual performance model that plots attainable floating-point performance as a function of arithmetic intensity.
*   The "roof" is formed by two limits: the system's memory bandwidth (a slanted line) and its peak compute performance (a horizontal line).
*   By plotting an algorithm's arithmetic intensity against this roofline, developers can immediately see whether their optimization efforts should focus on improving data locality (to reduce memory traffic) or parallelizing calculations (to increase FLOP rate).