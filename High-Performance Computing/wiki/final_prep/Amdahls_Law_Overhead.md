---
title: "Amdahl's Law with Parallel Overhead"
tags: [hpc, week-7, performance, openmp, scaling]
date: 2026-05-13
---

# Amdahl's Law with Parallel Overhead

## Standard Amdahl's Law (no overhead)

```
S_N = 1 / (s + p/N)
```

- `s` = sequential fraction of the workload (`s + p = 1`)
- `p` = parallelisable fraction
- `N` = number of processors
- Maximum speedup as N → ∞ is `1/s`

---

## Why Real Speedup Falls Short

Four sources of degradation (from lecture unit 7.5):

| Factor | Example |
|---|---|
| **Starvation** | Not enough parallel work to keep all processors busy |
| **Latency** | Time to access memory or send a message |
| **Overhead** | Starting/stopping an OpenMP parallel region |
| **Waiting** | Contention for shared memory or network bandwidth |

---

## Adding Overhead to Amdahl's Law

**Define the overhead:**

- `v` = cost (seconds) of one overhead event (e.g. launching one OpenMP parallel region)
- `n_p` = number of times that overhead is incurred (e.g. number of parallel regions)
- `V = n_p * v` = total overhead time in seconds

**Serial runtime** (unchanged):
```
T_0 = sT_0 + pT_0
```

**Parallel runtime** (overhead added):
```
T_N = sT_0 + pT_0/N + n_p*v
```

**Speedup:**
```
S_N = T_0 / T_N = 1 / (s + p/N + n_p*v/T_0)
```

The term `n_p*v/T_0 = V/T_0` is the total overhead expressed as a **fraction of the serial runtime**.

---

## Key Insight: When Does Overhead Dominate?

`V/T_0` grows and hurts speedup when:

1. **More parallel regions** — `n_p` increases, so `V` grows linearly
2. **Higher per-region cost** — `v` increases (e.g. heavy synchronisation)
3. **Smaller problem size** — `T_0` shrinks, so `V/T_0` grows even if `V` is fixed

This is why **fine-grained parallelism** (many small `#pragma omp parallel` regions) kills performance even when `p ≈ 1`. The overhead fraction dominates once the problem gets small.

**Fix:** use fewer, coarser parallel regions — merge parallel sections where possible.

---

## Exam Tip

The overhead term sits **alongside** `s` in the denominator. If the exam gives you `v`, `n_p`, and `T_0`, compute `V/T_0` first, then substitute into the formula. The overhead is significant when `V/T_0` is comparable in magnitude to `s`.
