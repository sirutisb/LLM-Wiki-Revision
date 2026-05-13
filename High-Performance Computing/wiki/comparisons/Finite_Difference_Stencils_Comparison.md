---
title: "Finite Difference Stencils: Forward, Backward, and Centered"
tags: [hpc, week-3, numerical-methods, finite-difference, stability, accuracy]
date: 2026-05-13
---

# Finite Difference Stencils: Forward, Backward, and Centered

When solving PDEs numerically we must discretise spatial derivatives. The choice of **stencil** (which neighbouring grid points to use) determines two independent properties: **accuracy** and **stability**. Critically, the more accurate stencil is not always the safer one.

See also: [Finite Difference Method](../concepts/Finite_Difference_Method.md) | [Numerical Stability and CFL](../concepts/Numerical_Stability_and_CFL.md) | [Advection Equation](../concepts/Advection_Equation.md)

---

## The Three First-Derivative Stencils

Given a uniform grid of spacing `Δx` with values `u_i = u(x_i)`:

| Stencil | Formula | Points used |
|---|---|---|
| **Forward difference** | `(u[i+1] - u[i]) / Δx` | i and i+1 (looks right) |
| **Backward difference** | `(u[i] - u[i-1]) / Δx` | i and i-1 (looks left) |
| **Centered difference** | `(u[i+1] - u[i-1]) / (2Δx)` | i-1 and i+1 (symmetric) |

```c
// Forward (one-sided, right)
dudx = (u[i+1] - u[i]) / dx;

// Backward (one-sided, left)
dudx = (u[i] - u[i-1]) / dx;

// Centered
dudx = (u[i+1] - u[i-1]) / (2 * dx);
```

---

## Accuracy: Taylor Series Analysis

Accuracy is determined by expanding in a Taylor series and finding the **leading-order truncation error**.

### Forward/Backward Difference — First-Order Accurate

From the Taylor expansion of `u[i+1]` around `u[i]`:

```
u[i+1] = u[i] + (du/dx)*Δx + (d²u/dx²)*(Δx²/2) + ...
```

Rearranging for `du/dx`:

```
du/dx = (u[i+1] - u[i]) / Δx  -  [(d²u/dx²) * Δx/2 + ...]
                ↑                          ↑
        finite difference          truncation error = O(Δx)
```

The leading error term is `O(Δx)` — **first-order accurate**. Halving `Δx` halves the error.

### Centered Difference — Second-Order Accurate

Write Taylor expansions for both neighbours and **subtract** them:

```
u[i+1] = u[i] + (du/dx)*Δx + (d²u/dx²)*(Δx²/2) + (d³u/dx³)*(Δx³/6) + ...
u[i-1] = u[i] - (du/dx)*Δx + (d²u/dx²)*(Δx²/2) - (d³u/dx³)*(Δx³/6) + ...

→ u[i+1] - u[i-1] = 2*(du/dx)*Δx + 2*(d³u/dx³)*(Δx³/6) + ...
→ du/dx = (u[i+1] - u[i-1]) / (2Δx)  +  O(Δx²)
```

The even-order error terms (`Δx²`) **cancel** by symmetry, leaving a leading error of `O(Δx²)` — **second-order accurate**. Halving `Δx` quarters the error.

### Why Centered Is More Accurate

The subtraction trick works because the forward and backward errors have opposite signs for odd-order terms. The `O(Δx)` terms cancel, leaving the much smaller `O(Δx²)` term. This is why centered differences converge to the true derivative faster as the grid is refined.

---

## Second-Order Derivative — Centered Only

For diffusion, we need `d²u/dx²`. This is obtained by **adding** the two Taylor expansions (not subtracting):

```
u[i+1] + u[i-1] = 2*u[i] + (d²u/dx²)*(Δx²) + O(Δx⁴)

→ d²u/dx² = (u[i+1] - 2*u[i] + u[i-1]) / Δx²  +  O(Δx²)
```

This three-point stencil is **second-order accurate** and is the standard formula used for the [Diffusion Equation](../concepts/Diffusion_Equation.md).

---

## Stability: The Counterintuitive Result

Accuracy alone does not determine which stencil to use. When combined with a **forward-Euler** time step (`u^(n+1) = u^n + Δt * RHS`), the stencils behave very differently for the [Advection Equation](../concepts/Advection_Equation.md).

| Scheme | Spatial stencil | Time step | Stability for advection |
|---|---|---|---|
| **FTCS** (Forward-Time Centred-Space) | Centered | Forward-Euler | **Unconditionally unstable** |
| **FTFS/FTBS** (Upwind) | Forward or backward (one-sided) | Forward-Euler | **Conditionally stable** (CFL) |

**The more accurate centered stencil produces an always-unstable scheme. The less accurate upwind stencil can be made stable.**

### Why FTCS is Unconditionally Unstable

The centered stencil is symmetric — it draws information equally from both left and right neighbours. The advection equation, however, describes information travelling in **one direction** (set by the sign of velocity `c`). The centered scheme ignores this physical directionality, introducing an artificial energy feed that amplifies errors regardless of how small `Δt` is.

### Why Upwind is Conditionally Stable

The one-sided (upwind) stencil is chosen to match the physical direction of propagation:
- If `c > 0` (rightward flow): use **backward difference** (`u[i] - u[i-1]`) — information comes from the left.
- If `c < 0` (leftward flow): use **forward difference** (`u[i+1] - u[i]`) — information comes from the right.

This respects the **domain of dependence** of the PDE — the scheme only uses information that physically influences point `i`. Stability is then conditional on the **CFL condition**:

```
Δt ≤ C * Δx / v_max     where 0 < C < 1
```

If the CFL condition is satisfied, errors are damped rather than amplified. See [Numerical Stability and CFL](../concepts/Numerical_Stability_and_CFL.md) for details.

---

## Side-by-Side Comparison

| Property | Forward/Backward (One-Sided) | Centered |
|---|---|---|
| **Formula** | `(u[i+1]-u[i])/Δx` or `(u[i]-u[i-1])/Δx` | `(u[i+1]-u[i-1])/(2Δx)` |
| **Points used** | 2 (asymmetric) | 3 (symmetric) |
| **Accuracy order** | O(Δx) — **first order** | O(Δx²) — **second order** |
| **Error halving** | Halving Δx halves error | Halving Δx quarters error |
| **Advection + Euler stability** | **Conditionally stable** (needs CFL) | **Unconditionally unstable** |
| **Diffusion + Euler stability** | N/A (not suitable for 2nd derivative) | Conditionally stable (diffusion number) |
| **Physical interpretation** | Directional — respects wave propagation | Symmetric — no preferred direction |
| **Boundary cost** | Needs one boundary value | Needs two boundary values |
| **Typical use case** | Advection (upwind scheme) | Diffusion; higher-accuracy approximations |

---

## Key Exam Points

1. **Centered is more accurate but not always better.** For the advection equation with forward-Euler time stepping, centered difference is unconditionally unstable — it gives a worse result than the first-order upwind scheme regardless of grid resolution.

2. **"FTCS" is the name for the doomed combination.** Forward-Time Centered-Space applied to advection always blows up.

3. **Upwind = one-sided in the direction of flow.** The naming comes from numerical weather prediction — you look "upwind" (upstream) for information.

4. **CFL only applies when using upwind spatial differences.** It is the stability condition for the Forward-Euler + one-sided stencil combination applied to advection: `c*Δt/Δx ≤ 1`.

5. **The second-order spatial derivative** (for diffusion) uses the centered three-point stencil `(u[i+1] - 2u[i] + u[i-1]) / Δx²` — there is no upwind alternative because diffusion has no preferred direction.

6. **Accuracy vs. stability is a design trade-off.** Real solvers often use higher-order or flux-limiter schemes that attempt to get both, but for this module the key fact is the FTCS instability result.
