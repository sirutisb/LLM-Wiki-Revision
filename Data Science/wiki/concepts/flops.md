---
title: "FLOPS"
type: concept
sources: [high-performance-computing]
related: [amdahls-law, moores-law, high-performance-computing]
updated: 2026-05-02
---

# FLOPS

*Floating Point Operations Per Second — the standard unit for measuring computational throughput in scientific and ML workloads.*

## Definition

**FLOPS** (Floating Point Operations Per Second) measures how many floating-point arithmetic operations a processor can perform per second. It is the primary performance metric for HPC systems, GPUs, and ML accelerators.

## Scale reference

| Prefix | Value | Symbol | Context |
|---|---|---|---|
| Giga | 10⁹ | GFLOPS | Smartphones (1–2 GFLOPS), laptops (~10 GFLOPS) |
| Tera | 10¹² | TFLOPS | High-end servers (25–100 GFLOPS), GPUs (20 GFLOPS–2 TFLOPS) |
| Peta | 10¹⁵ | PFLOPS | Top supercomputers |
| Exa | 10¹⁸ | EFLOPS | Frontier (world's first exascale computer, 2022) |

## Why it matters

FLOPS determines how quickly you can train a neural network, run a simulation, or process large datasets. A GPU at 2 TFLOPS is ~200× faster than a smartphone at 1 GFLOPS for the same floating-point workload.

## Caveats

- Peak FLOPS ≠ sustained FLOPS — memory bandwidth and data movement often limit real throughput.
- FP16 vs FP32 vs FP64 — GPUs often quote FP16 FLOPS (half precision), which is 2–4× higher than FP32.

## Examples in the syllabus

- HPC s. 3: FLOPS scale defined with device benchmarks.

## See also

- [[amdahls-law]]
- [[moores-law]]
- [[high-performance-computing]]
