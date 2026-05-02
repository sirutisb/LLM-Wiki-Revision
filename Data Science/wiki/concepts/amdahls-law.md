---
title: "Amdahl's Law"
type: concept
sources: [high-performance-computing]
related: [moores-law, flops, scalability, high-performance-computing]
updated: 2026-05-02
---

# Amdahl's Law

*The speedup from adding more processors is bounded by the sequential fraction of the workload — a hard ceiling that no amount of parallelism can overcome.*

## Definition

**Amdahl's Law** predicts the theoretical maximum speedup S achievable when parallelising part of a computation:

```
S_latency = 1 / ((1 − p) + p/s)
```

Where:
- **p** = proportion of execution time that *can* be parallelised.
- **s** = speedup of the parallelisable part (e.g. number of processors).
- **(1 − p)** = the sequential fraction that *cannot* be parallelised.

## Why it matters

It tells you the upper bound before you invest in more hardware. A 10% sequential fraction caps your maximum possible speedup at 10×, no matter how many cores you add. Adding more processors has diminishing returns.

## Worked example (from the lecture)

Workload: 10 sequential scalar additions + 100 parallel matrix additions.

- **1 processor**: time = (10 + 100) × t_add = 110 × t_add
- **10 processors**: time = 10 × t_add + 100/10 × t_add = 20 × t_add
- **Speedup** = 110 / 20 = **5.5×** with 10 processors

The sequential part (10 t_add) prevented us from getting the full 10× speedup.

## Maximum speedup (as s → ∞)

```
lim(s→∞) S_latency = 1 / (1 − p)
```

If 90% of the work is parallelisable (p = 0.9): max speedup = 10×.  
If 95% parallelisable (p = 0.95): max speedup = 20×.  
If 99% parallelisable (p = 0.99): max speedup = 100×.

## Implications

- Before optimising, measure the sequential fraction.
- Optimising the bottleneck (sequential part) yields more gain than adding processors.
- Explains why HPC clusters still need software-hardware co-design — raw scale isn't enough.

## Examples in the syllabus

- HPC s. 6–7: formula defined with the scalar + matrix example.

## Common exam framing

- "State Amdahl's Law and explain what it implies for parallel computing."
- "A workload is 80% parallelisable. What is the maximum speedup achievable with unlimited processors?"
- "Why does doubling the number of processors not double performance?"

## See also

- [[moores-law]]
- [[flops]]
- [[scalability]]
