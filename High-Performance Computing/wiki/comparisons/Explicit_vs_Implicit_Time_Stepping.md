---
title: "Explicit vs Implicit Time Stepping"
tags: [hpc, week-3, numerical, stability, finite-difference]
date: 2026-05-13
---

# Explicit vs Implicit Time Stepping

The distinction is about which time level the right-hand side is evaluated at when advancing a PDE solution forward in time. See [Numerical Stability and CFL](../concepts/Numerical_Stability_and_CFL.md) and [Finite Difference Method](../concepts/Finite_Difference_Method.md).

## Explicit (Forward-Euler)

```
u^(n+1) = u^n + Δt * f(u^n)
```

The new value `u^(n+1)` is computed directly from **known** values at the current time level `n`. No system of equations needs to be solved.

- Simple to implement; one pass over the grid per step.
- Cheap per time step, and trivially parallelisable (each grid point updates independently).
- **Conditionally stable**: must satisfy the CFL condition `Δt ≤ C * Δx / v_max`. Violating it causes exponential blow-up.
- This is the "forward-Euler time step" used throughout Week 3 (exponential decay, advection, diffusion examples).

## Implicit (Backward-Euler)

```
u^(n+1) = u^n + Δt * f(u^(n+1))
```

The right-hand side depends on **unknown** values at the next time level `n+1`. Both sides contain `u^(n+1)`, so a **system of equations** (typically tridiagonal for 1D PDEs) must be solved at every step.

- More complex to implement; requires a linear solver each step.
- Harder to parallelise: unknowns at different grid points are coupled.
- **Unconditionally stable** for many equations (e.g., diffusion): arbitrarily large `Δt` will not cause blow-up. However, accuracy still degrades for large `Δt` even when stable.

## Comparison Table

| Property | Explicit | Implicit |
|---|---|---|
| Time level of RHS | Current (`n`) | Next (`n+1`) |
| Requires solving a system? | No | Yes (e.g. tridiagonal) |
| Per-step cost | Low | Higher |
| Parallelism | Easy (embarrassingly parallel) | Harder (global coupling) |
| Stability | Conditionally stable (CFL) | Often unconditionally stable |
| Time step limit | `Δt ≤ C Δx / v_max` | Accuracy-limited, not stability-limited |

## HPC Implications

Explicit methods dominate in HPC because each grid point updates independently — there is no communication between unknowns at the same time level. This makes them naturally parallelisable across MPI processes or OpenMP threads.

Implicit methods couple all grid points at the next time step, requiring a collective solve (e.g., Gaussian elimination or iterative solvers like conjugate gradient). These introduce global data dependencies that are expensive to parallelise and require more communication in distributed-memory settings.

The practical trade-off: explicit methods on fine grids or fast phenomena (small `Δx`, large `v`) demand very small `Δt` and potentially millions of time steps. Implicit methods allow larger `Δt` — fewer steps — but pay per-step in solver cost and parallelism overhead.
