---
title: "Moore's Law"
type: concept
sources: [high-performance-computing]
related: [amdahls-law, flops, software-hardware-codesign]
updated: 2026-05-02
---

# Moore's Law

*The empirical observation that transistor density doubles approximately every two years — a trend that drove 50 years of computing growth but is now slowing, forcing the industry toward specialised hardware.*

## Definition

**Moore's Law** is the observation by Gordon Moore (1965) that the number of transistors on integrated circuits doubles approximately every two years, leading to corresponding increases in computational performance.

## Why it matters

For decades Moore's Law meant that software developers could get free performance improvements just by waiting for the next chip generation. That era is ending. Transistors are approaching physical limits (quantum effects at sub-5nm scales). Performance gains now require:

- Parallelism (more cores).
- Specialised hardware (GPUs, TPUs, tensor cores).
- Software-hardware co-design.

## Current status

The industry is lagging behind Moore's Law. Doubling happens more slowly (every 2.5–3 years) and gains are less in single-threaded performance. Power consumption (thermal design power) is now a hard constraint.

## Implications for data science

- Big data and ML workloads can no longer count on free speedups from next-generation CPUs.
- GPU acceleration and specialised ML chips (TPUs, NPUs) fill the gap.
- Software frameworks (PyTorch, TensorFlow) are increasingly hardware-aware.

## Examples in the syllabus

- HPC s. 5: Moore's Law defined; industry hitting its limits noted.
- Software-Hardware Co-design s. 2–3: slowdown of Moore's Law as the driver for co-design.

## Common exam framing

- "What is Moore's Law? Why is it relevant to modern data science systems?"
- "How does the slowdown of Moore's Law motivate software-hardware co-design?"

## See also

- [[amdahls-law]]
- [[software-hardware-codesign]]
- [[flops]]
