---
title: "Week 3 Practice Questions: Numerical Solutions to PDEs"
tags: [hpc, week-3, numerical, pde, practice]
date: 2026-05-14
---

# Week 3 Practice Questions: Numerical Solutions to PDEs

> Source material: [Week 3 Summary](../wiki/summaries/Week_3_Summary.md) | [Finite Difference Method](../wiki/concepts/Finite_Difference_Method.md) | [Numerical Stability and CFL](../wiki/concepts/Numerical_Stability_and_CFL.md) | [Advection Equation](../wiki/concepts/Advection_Equation.md) | [Diffusion Equation](../wiki/concepts/Diffusion_Equation.md) | [Exponential Decay](../wiki/concepts/Exponential_Decay.md) | [Stencil Comparison](../wiki/comparisons/Finite_Difference_Stencils_Comparison.md) | [Explicit vs Implicit](../wiki/comparisons/Explicit_vs_Implicit_Time_Stepping.md)

---

## Section A: Short Answer and Definitions

---

### Q1. Distinguish between an ODE and a PDE. Give one example of each from the Week 3 material.

**Model Answer:**

- An **Ordinary Differential Equation (ODE)** contains derivatives with respect to only one independent variable (e.g., time alone).
- A **Partial Differential Equation (PDE)** contains derivatives with respect to **more than one** independent variable (e.g., both time `t` and space `x`).

**Examples from Week 3:**

| Type | Equation | Why |
|---|---|---|
| ODE | Exponential decay: `dN/dt = -λN` | Only one independent variable: `t` |
| PDE | Advection: `∂u/∂t = -c ∂u/∂x` | Two independent variables: `t` and `x` |

Key marking points: correct definition, correct classification of `∂` notation, valid examples.

---

### Q2. Define each of the following terms as used in numerical PDE solving:

**(a)** Discretization  
**(b)** Truncation error  
**(c)** Numerical stability  
**(d)** Boundary condition

**Model Answer:**

**(a) Discretization:** The process of replacing a continuous domain (in time and/or space) with a finite set of grid points separated by `Δt` (time) and `Δx` (space). Derivatives are replaced by finite differences between neighbouring grid values.

**(b) Truncation error:** The mathematical error introduced by replacing a derivative with its finite difference approximation. It arises because the finite difference only retains the leading terms of a Taylor series — higher-order terms are discarded ("truncated"). Expressed as `O(Δx)` (first-order) or `O(Δx²)` (second-order) for spatial stencils.

**(c) Numerical stability:** A scheme is **stable** if errors (from rounding, truncation, or initial condition perturbations) remain bounded and do not grow without limit over time. An **unstable** scheme produces solutions that diverge exponentially, rendering the result meaningless.

**(d) Boundary condition:** A value (or constraint on the gradient) specified at the edge of the computational domain. Necessary because interior stencils require neighbouring points that do not exist at the boundary. Examples: fixed value `u(0,t) = 0` (Dirichlet) or specified gradient `∂u/∂x|_boundary = 0` (Neumann).

---

### Q3. What is the physical meaning of the advection equation `∂u/∂t = -c ∂u/∂x`? What does the solution look like for a positive wave speed `c`?

**Model Answer:**

The advection equation describes the **transport** of a scalar quantity `u` by a constant velocity field `c`. The quantity is carried passively — its shape is preserved but its position shifts with time.

For an initial profile `u(x, 0) = f(x)`, the solution is `u(x, t) = f(x - ct)`. This means:
- The entire initial profile **translates to the right** at speed `c` without changing shape or amplitude.
- There is no diffusion or distortion in the exact solution.

Physical examples: silt concentration carried downstream, a dust cloud advected by wind, salt in ocean currents.

Key marking points: transport/translation interpretation; `f(x - ct)` solution form; no shape change; physical example.

---

### Q4. What is the diffusion constant `K` in `∂u/∂t = K ∂²u/∂x²`, and what physical effect does it describe?

**Model Answer:**

`K` is the **diffusion coefficient** (units: m²/s for mass diffusion, or thermal diffusivity for heat). It controls the rate at which gradients in `u` are smoothed out.

Physical effect: Diffusion causes net movement from **high concentration** to **low concentration** due to random molecular motion. The second spatial derivative `∂²u/∂x²` measures the *curvature* of the field:
- Where curvature is **positive** (valley shape), `∂u/∂t > 0` — the concentration rises.
- Where curvature is **negative** (peak shape), `∂u/∂t < 0` — the concentration falls.

Over time, peaks flatten and valleys fill: the solution smooths toward a uniform distribution.

---

### Q5. Name the three discretization methods for PDEs covered in the module. State one advantage and one disadvantage of the Finite Difference Method.

**Model Answer:**

**Three methods:**
1. Finite Difference Method (FDM)
2. Finite Volume Method (FVM) — e.g., OpenFOAM
3. Finite Element Method (FEM) — e.g., Nektar++, Firedrake

**Finite Difference Method:**
- Advantage: Simple to implement; straightforward to derive and code on regular grids.
- Disadvantage: Not well-suited to complex geometries or unstructured meshes — it assumes a regular, structured grid.

---

### Q6. What is the Courant number (CFL number)? Write its formula and state what value it must not exceed for a stable explicit scheme.

**Model Answer:**

The Courant number (or CFL number) is a dimensionless ratio that compares the distance information physically travels in one timestep to the grid spacing:

```
CFL number = c * Δt / Δx
```

Where:
- `c` = wave/advection speed
- `Δt` = time step size
- `Δx` = spatial grid spacing

For a stable explicit (forward-Euler + upwind) scheme, the CFL number must satisfy:

```
c * Δt / Δx ≤ 1    (for C_max = 1)
```

Equivalently written as: `Δt ≤ Δx / c`

If the CFL number exceeds the limit, errors grow exponentially and the solution diverges.

---

### Q7. State the physical interpretation of the CFL condition. Why does violating it cause the scheme to blow up?

**Model Answer:**

**Physical interpretation:** The CFL condition requires that the physical domain of dependence is contained within the numerical domain of dependence. Concretely: the distance that information (a wave, an advected quantity) physically travels in one timestep (`c × Δt`) must be **no larger than one grid cell** (`Δx`).

**Why violation causes blow-up:** If `c × Δt > Δx`, the information physically "jumps over" grid cells — the updated value at point `i` should depend on data from points that the numerical stencil never sampled. The scheme uses the wrong data, introducing errors that do not cancel but instead amplify each timestep, leading to exponential divergence.

Named after Richard Courant, Kurt Friedrichs, and Hans Lewy (1928).

---

## Section B: Derivations

---

### Q8. Derive the forward difference approximation for `∂u/∂x` from a Taylor series. What is the order of the truncation error?

**Model Answer:**

**Step 1 — Write the Taylor expansion of `u(x + Δx)` about `x`:**

```
u(x + Δx) = u(x) + (∂u/∂x) Δx + (∂²u/∂x²) (Δx²/2!) + (∂³u/∂x³) (Δx³/3!) + ...
```

In index notation with `u[i] = u(x_i)` and `u[i+1] = u(x_i + Δx)`:

```
u[i+1] = u[i] + (∂u/∂x)|_i * Δx + (∂²u/∂x²)|_i * (Δx²/2) + O(Δx³)
```

**Step 2 — Rearrange to isolate `∂u/∂x`:**

```
(∂u/∂x)|_i = (u[i+1] - u[i]) / Δx  -  (∂²u/∂x²)|_i * (Δx/2)  -  O(Δx²)
```

**Step 3 — Identify the truncation error:**

The finite difference approximation is `(u[i+1] - u[i]) / Δx`. The remainder (error) is:

```
Error = - (∂²u/∂x²)|_i * (Δx/2) + O(Δx²)
```

The **leading-order term is proportional to `Δx`**, so the forward difference is **first-order accurate**: `O(Δx)`.

**Consequence:** Halving the grid spacing `Δx` halves the truncation error.

---

### Q9. Derive the centred difference approximation for `∂u/∂x` from a Taylor series. Show why it is second-order accurate.

**Model Answer:**

**Step 1 — Write Taylor expansions for both neighbours:**

```
u[i+1] = u[i] + (∂u/∂x) Δx + (∂²u/∂x²)(Δx²/2) + (∂³u/∂x³)(Δx³/6) + O(Δx⁴)
u[i-1] = u[i] - (∂u/∂x) Δx + (∂²u/∂x²)(Δx²/2) - (∂³u/∂x³)(Δx³/6) + O(Δx⁴)
```

**Step 2 — Subtract the second from the first:**

```
u[i+1] - u[i-1] = 2*(∂u/∂x) Δx + 2*(∂³u/∂x³)(Δx³/6) + O(Δx⁵)
```

Note: the even-power terms (`Δx²`, `Δx⁴`, ...) **cancel by symmetry**.

**Step 3 — Rearrange for `∂u/∂x`:**

```
(∂u/∂x)|_i = (u[i+1] - u[i-1]) / (2Δx)  -  (∂³u/∂x³)|_i * (Δx²/6)  -  O(Δx⁴)
```

**Step 4 — Identify the truncation error:**

The leading error term is `O(Δx²)` — the scheme is **second-order accurate**.

**Why it beats forward/backward:** Subtraction cancels the `O(Δx)` odd-power terms from both expansions simultaneously. The symmetric stencil gains an order of accuracy for free.

**Consequence:** Halving `Δx` reduces the truncation error by a factor of **four**.

---

### Q10. Derive the centred difference approximation for the second derivative `∂²u/∂x²`. What is its order of accuracy?

**Model Answer:**

**Step 1 — Start from the same Taylor expansions as Q9:**

```
u[i+1] = u[i] + (∂u/∂x) Δx + (∂²u/∂x²)(Δx²/2) + (∂³u/∂x³)(Δx³/6) + (∂⁴u/∂x⁴)(Δx⁴/24) + ...
u[i-1] = u[i] - (∂u/∂x) Δx + (∂²u/∂x²)(Δx²/2) - (∂³u/∂x³)(Δx³/6) + (∂⁴u/∂x⁴)(Δx⁴/24) + ...
```

**Step 2 — ADD the two expansions (instead of subtracting):**

```
u[i+1] + u[i-1] = 2*u[i] + (∂²u/∂x²) Δx² + (∂⁴u/∂x⁴)(Δx⁴/12) + O(Δx⁶)
```

The odd-power terms cancel; the even-power terms reinforce.

**Step 3 — Rearrange for `∂²u/∂x²`:**

```
(∂²u/∂x²)|_i = (u[i+1] - 2*u[i] + u[i-1]) / Δx²  -  (∂⁴u/∂x⁴)|_i * (Δx²/12)  + O(Δx⁴)
```

**Step 4 — Result:**

Three-point centred stencil for the second derivative:

```
d²u/dx² ≈ (u[i+1] - 2*u[i] + u[i-1]) / Δx²
```

Truncation error: **`O(Δx²)` — second-order accurate.** This is the standard stencil used in the FTCS scheme for the diffusion equation.

---

### Q11. Derive the stability condition for the explicit (FTCS) solution of the 1D diffusion equation.

**Model Answer:**

The FTCS scheme for diffusion `∂u/∂t = K ∂²u/∂x²` combines forward-Euler in time with the centred second-derivative stencil in space:

**Step 1 — Write the update rule:**

```
u_i^(n+1) = u_i^n + (K * Δt / Δx²) * (u[i+1]^n - 2*u_i^n + u[i-1]^n)
```

Define the **diffusion number** `r = K * Δt / Δx²`.

```
u_i^(n+1) = r * u[i+1]^n + (1 - 2r) * u_i^n + r * u[i-1]^n
```

**Step 2 — Apply Von Neumann stability analysis.** Assume an error mode of the form `ε_i^n = ξ^n * e^(I*k*i*Δx)` where `ξ` is the amplification factor and `k` is a wavenumber.

Substituting into the update rule:

```
ξ = r*e^(I*k*Δx) + (1 - 2r) + r*e^(-I*k*Δx)
  = (1 - 2r) + 2r*cos(k*Δx)
  = 1 - 2r*(1 - cos(k*Δx))
```

**Step 3 — Require `|ξ| ≤ 1` for stability:**

The worst case is when `cos(k*Δx) = -1` (maximum oscillation, `k*Δx = π`):

```
ξ_min = 1 - 2r*(1 - (-1)) = 1 - 4r
```

For stability: `|ξ_min| ≤ 1`, so `-1 ≤ 1 - 4r`, giving:

```
4r ≤ 2  →  r ≤ 1/2
```

**Step 4 — State the stability condition:**

```
K * Δt / Δx² ≤ 1/2
```

Equivalently: `Δt ≤ Δx² / (2K)`

This is the **diffusion stability condition**. It is much more restrictive than the advection CFL condition because it scales as `Δx²` — halving the spatial resolution requires four times smaller time steps.

---

### Q12. Starting from the exponential decay ODE `dN/dt = -λN`, derive the forward-Euler update formula and state the exact (analytical) solution. Under what condition does the numerical solution remain accurate?

**Model Answer:**

**Exact analytical solution:**

Separating variables: `dN/N = -λ dt` → integrating: `ln(N) = -λt + C` → applying `N(0) = N_0`:

```
N(t) = N_0 * e^(-λt)
```

**Forward-Euler discretization:**

Approximate the derivative: `dN/dt ≈ (N_{n+1} - N_n) / Δt`

Substituting into the ODE:

```
(N_{n+1} - N_n) / Δt = -λ * N_n
N_{n+1} = N_n - λ * Δt * N_n
N_{n+1} = N_n * (1 - λ*Δt)
```

This is the forward-Euler update rule.

**Accuracy condition:**

The scheme assumes the rate of change is constant over `Δt`. This is only a good approximation when `Δt` is small relative to the timescale of decay (`1/λ`). Formally: `λ * Δt << 1`.

Also, for the solution to remain non-negative (physically sensible): `1 - λ*Δt ≥ 0` → `Δt ≤ 1/λ`. If `Δt > 2/λ`, the numerical solution oscillates with growing amplitude — it becomes unstable.

---

## Section C: Calculations and Stability Analysis

---

### Q13. Check whether the following simulation parameters satisfy the CFL condition. For each case, state whether the scheme is stable, and if not, what maximum time step would be allowed.

Given: advection equation `∂u/∂t = -c ∂u/∂x`, forward-Euler time step, upwind spatial difference.

**(a)** `c = 5 m/s`, `Δx = 0.2 m`, `Δt = 0.03 s`  
**(b)** `c = 100 m/s`, `Δx = 0.5 m`, `Δt = 0.01 s`  
**(c)** `c = 1 m/s`, `Δx = 0.01 m`, `Δt = 0.005 s`

**Model Answer:**

CFL condition: `c * Δt / Δx ≤ 1`

**(a)** CFL number = `5 * 0.03 / 0.2 = 0.15 / 0.2 = 0.75`  
`0.75 ≤ 1` → **STABLE.** The scheme satisfies the CFL condition.

**(b)** CFL number = `100 * 0.01 / 0.5 = 1.0 / 0.5 = 2.0`  
`2.0 > 1` → **UNSTABLE.** Maximum allowed: `Δt_max = Δx / c = 0.5 / 100 = 0.005 s`

**(c)** CFL number = `1 * 0.005 / 0.01 = 0.5`  
`0.5 ≤ 1` → **STABLE.**

---

### Q14. A diffusion simulation uses `K = 0.01 m²/s` and `Δx = 0.05 m`.

**(a)** What is the maximum time step allowed by the explicit (FTCS) stability condition?  
**(b)** If the domain has length `L = 1 m` and we must simulate `T = 10 s`, how many spatial grid points and time steps are required?  
**(c)** If we halve the grid spacing to `Δx = 0.025 m`, by what factor does the maximum allowed `Δt` change?

**Model Answer:**

Diffusion stability condition: `K * Δt / Δx² ≤ 1/2`  →  `Δt ≤ Δx² / (2K)`

**(a)** `Δt_max = (0.05)² / (2 * 0.01) = 0.0025 / 0.02 = 0.125 s`

**(b)**
- Spatial points: `N_x = L / Δx = 1.0 / 0.05 = 20` points (plus 1 for boundaries = 21, depending on convention)
- Time steps: `N_t = T / Δt_max = 10 / 0.125 = 80` steps (minimum; fewer steps if we use a larger Δt within the stable range — but using the maximum stable Δt is typical)

**(c)** With `Δx' = 0.025 m`:

`Δt'_max = (0.025)² / (2 * 0.01) = 0.000625 / 0.02 = 0.03125 s`

Ratio: `Δt'_max / Δt_max = 0.03125 / 0.125 = 0.25`

Halving `Δx` reduces the maximum allowed `Δt` by a **factor of 4** (since the stability condition scales as `Δx²`). This is why fine-grid diffusion simulations are so expensive: doubling the spatial resolution increases the number of spatial points by 2 AND the number of required time steps by 4, giving an overall `8×` cost increase in 1D.

---

### Q15. For the following stencils, identify the truncation error order and whether the stencil is one-sided or symmetric.

**(a)** `(u[i+1] - u[i]) / Δx`  
**(b)** `(u[i] - u[i-1]) / Δx`  
**(c)** `(u[i+1] - u[i-1]) / (2Δx)`  
**(d)** `(u[i+1] - 2*u[i] + u[i-1]) / Δx²`

**Model Answer:**

| Stencil | Name | Type | Truncation Error | Order |
|---|---|---|---|---|
| **(a)** `(u[i+1] - u[i]) / Δx` | Forward difference | One-sided (right) | `O(Δx)` | 1st order |
| **(b)** `(u[i] - u[i-1]) / Δx` | Backward difference | One-sided (left) | `O(Δx)` | 1st order |
| **(c)** `(u[i+1] - u[i-1]) / (2Δx)` | Centred difference | Symmetric | `O(Δx²)` | 2nd order |
| **(d)** `(u[i+1] - 2u[i] + u[i-1]) / Δx²` | Centred 2nd derivative | Symmetric | `O(Δx²)` | 2nd order |

Key note: (d) is the only standard stencil for the second derivative and is always used for the diffusion equation — there is no upwind alternative because diffusion has no preferred direction.

---

### Q16. Calculate the truncation error for the forward difference stencil when `Δx = 0.1` vs `Δx = 0.05`. Assume the second derivative of `u` at the point is `∂²u/∂x² = 6` (i.e., `u = x³` near that point).

**Model Answer:**

The truncation error of the forward difference is:

```
Error = -(∂²u/∂x²)|_i * (Δx/2) + O(Δx²)
```

Leading-order error magnitude:

**With `Δx = 0.1`:**
```
Error ≈ 6 * (0.1 / 2) = 6 * 0.05 = 0.3
```

**With `Δx = 0.05`:**
```
Error ≈ 6 * (0.05 / 2) = 6 * 0.025 = 0.15
```

Halving `Δx` halves the truncation error — confirming **first-order convergence**.

For comparison, the centred difference (second-order) has leading error `O(Δx²)`:
- At `Δx = 0.1`: error ~ `Δx² = 0.01` (30 times smaller)
- At `Δx = 0.05`: error ~ `0.0025` (60 times smaller than forward at `Δx = 0.1`)

This illustrates why second-order stencils are preferred when accuracy matters.

---

### Q17. Consider solving the 1D advection equation with `c = 2 m/s`, `Δx = 0.1 m`.

**(a)** Using FTCS (forward-Euler + centred difference): is there any value of `Δt` that makes this scheme stable?  
**(b)** Using FTBS (forward-Euler + backward difference, i.e., upwind for `c > 0`): what is the maximum stable `Δt`?  
**(c)** If `Δt = Δt_max` from (b) is used, what is the CFL number?

**Model Answer:**

**(a)** FTCS applied to advection is **unconditionally unstable** — no value of `Δt` can make it stable. The centred stencil draws equally from left and right, ignoring the physical direction of information flow (rightward for `c > 0`). Von Neumann analysis shows the amplification factor always exceeds 1 in magnitude. This is a fundamental property of the scheme, not fixable by reducing `Δt`.

**(b)** FTBS (upwind for `c > 0`): CFL condition `c * Δt / Δx ≤ 1`:
```
Δt_max = Δx / c = 0.1 / 2 = 0.05 s
```

**(c)** At `Δt = 0.05 s`:
```
CFL = c * Δt / Δx = 2 * 0.05 / 0.1 = 1.0
```
The CFL number is exactly 1 — the marginally stable case. In practice, use slightly less than `Δt_max` to keep CFL < 1 with a small margin.

---

## Section D: Explain and Describe

---

### Q18. Explain, using physical reasoning, why the upwind scheme for advection is stable while the centred scheme (FTCS) is unconditionally unstable.

**Model Answer:**

**Physical directionality of advection:** The advection equation `∂u/∂t = -c ∂u/∂x` describes information propagating in one direction. For `c > 0`, the wave moves rightward — the value at point `i` at the next timestep is determined by what was **to its left** (upstream), not by what was to its right.

**Why the upwind scheme is stable:** The backward difference `(u[i] - u[i-1]) / Δx` for `c > 0` only looks to the left (upstream), mirroring where the physical information actually comes from. The scheme's **domain of numerical dependence** matches the **domain of physical dependence**. Provided CFL ≤ 1 (the information doesn't travel more than one cell per timestep), errors are damped — the scheme is conditionally stable.

**Why FTCS fails:** The centred difference `(u[i+1] - u[i-1]) / (2Δx)` samples symmetrically — equally from upstream (left) and downstream (right). For rightward advection, the downstream point `u[i+1]` should have **no physical influence** on `u[i]` at the next step. Including it introduces spurious information that feeds errors back into the solution. Von Neumann analysis confirms the amplification factor `|ξ| > 1` for all wavenumbers, for any `Δt`. The scheme adds energy to every error mode rather than damping it.

**Summary:** Stability requires the numerical stencil to respect the physical domain of dependence. FTCS violates this by including downstream information in an upstream-propagating problem.

---

### Q19. Compare explicit and implicit time-stepping methods. Address: (a) computational cost per step, (b) parallelisability, (c) stability, (d) when each is preferred in HPC contexts.

**Model Answer:**

**(a) Computational cost per step:**
- **Explicit (forward-Euler):** Each grid point updates independently using only known values from time level `n`. Cost per step: `O(N)` for `N` grid points — one arithmetic operation per point.
- **Implicit (backward-Euler):** The unknown `u^(n+1)` appears on both sides of the equation, coupling all grid points. Requires solving a linear system (e.g., tridiagonal) at every step — cost `O(N)` for 1D via Thomas algorithm, but more expensive in 2D/3D and harder to precondition.

**(b) Parallelisability:**
- **Explicit:** Embarrassingly parallel — each grid point's update is independent. Trivially distributed across MPI processes or OpenMP threads. Ideal for GPU offloading.
- **Implicit:** Grid points are coupled through the linear system. Global solver dependencies limit parallelism. Distributed solvers (e.g., conjugate gradient) require collective communication — higher MPI overhead.

**(c) Stability:**
- **Explicit:** Conditionally stable — must satisfy CFL: `Δt ≤ C * Δx / v_max`. Violating CFL causes exponential blow-up.
- **Implicit:** Often unconditionally stable for diffusion-type problems — arbitrarily large `Δt` will not cause blow-up. However, accuracy degrades for large `Δt` even without instability.

**(d) HPC preference:**
- Explicit methods dominate in HPC due to their parallelism and simplicity, especially for wave/advection problems or when fine `Δx` is already required for accuracy (making the CFL-limited `Δt` acceptable).
- Implicit methods are preferred when the problem has a very stiff component (e.g., fast diffusion with small `K` relative to `Δx²`) that would require impractically small `Δt` under an explicit scheme. The trade-off is accepting higher per-step cost and communication overhead in exchange for larger timesteps.

---

## Section E: Sketch and Describe Plots

---

### Q20. Sketch and describe what the exact solution of the 1D advection equation looks like for an initial Gaussian pulse `u(x, 0) = exp(-x²)` with wave speed `c = 1 m/s`. Then describe what a numerically computed solution using (a) FTBS upwind scheme at CFL = 0.8 and (b) FTCS scheme would look like after 10 timesteps.

**Model Answer:**

**Exact solution:** The Gaussian pulse `exp(-x²)` translates rigidly to the right at speed `c = 1 m/s`, becoming `exp(-(x - t)²)`. The shape, peak height, and width are perfectly preserved at all times. No spreading, no distortion.

**(a) FTBS upwind scheme (CFL = 0.8):**
The pulse still moves rightward, but the upwind scheme introduces **numerical diffusion** — an artificial smoothing effect caused by the first-order spatial truncation error. After 10 timesteps:
- The pulse has shifted rightward by approximately `c * 10 * Δt` grid positions.
- The peak is slightly **lower** than the initial height.
- The edges of the Gaussian are **broader/more spread out** than the exact solution.
- The solution remains non-negative and bounded — it is stable.
- Numerical diffusion is worse for larger `Δt` (larger CFL numbers) and coarser grids.

**(b) FTCS scheme:**
The solution is **unconditionally unstable**. Even after a very small number of timesteps:
- Short-wavelength oscillations (high-frequency "noise") begin to appear superimposed on the pulse.
- These oscillations grow exponentially each timestep.
- After 10 timesteps, the solution has typically diverged completely — the values are orders of magnitude larger than the initial condition and bear no resemblance to a Gaussian.
- The solution is numerically meaningless regardless of the CFL number chosen.

---

### Q21. Describe how a sharp initial condition (step function) evolves under the 1D diffusion equation `∂u/∂t = K ∂²u/∂x²` over time. Sketch the profile at three different times `t₁ < t₂ < t₃`.

**Model Answer:**

**Initial condition:** A step function — `u = 1` for `x < 0`, `u = 0` for `x ≥ 0`.

**Evolution under diffusion:**

The diffusion equation smooths gradients. At the sharp discontinuity, the second derivative `∂²u/∂x²` is initially infinite (or very large in a discrete sense), driving rapid initial change.

**At time `t₁` (early):** The step has begun to round. The sharp edge is now a smooth S-shaped transition zone of width approximately `2√(Kt₁)`. The maximum and minimum values are still close to 1 and 0.

**At time `t₂` (moderate):** The transition zone is wider — width `~2√(Kt₂)`. The S-curve is more gradual. The values away from the transition approach 0 and 1 asymptotically.

**At time `t₃` (late):** The transition zone is very wide. If the domain has finite boundaries, the solution is approaching the boundary condition values everywhere, and the profile is nearly flat.

**Key physical insight:** The width of the transition zone grows as `√(Kt)` — not linearly with time. This is the hallmark of diffusive spreading. Contrast with advection, where the shape translates at fixed speed without changing.

**Sketch description (3 curves, same axes):**
- `t = 0`: Vertical step at `x = 0`
- `t = t₁`: Smooth S-curve, narrow transition
- `t = t₂`: Wider S-curve, same asymptotes (0 and 1)
- `t = t₃`: Very gentle S-curve, nearly flat

---

## Section F: Multi-Part Exam Questions

---

### Q22. [Multi-part] Numerical Solution of the Advection Equation

A 1D advection problem has the following parameters:
- Wave speed: `c = 4 m/s`
- Domain: `x ∈ [0, 2]` m, discretized into 100 equally spaced grid points
- Simulation time: `T = 0.5 s`
- Scheme: forward-Euler time step + backward difference spatial stencil (upwind)

**(a)** What is `Δx` for this domain?  
**(b)** Calculate the maximum stable time step `Δt_max`.  
**(c)** If we use `Δt = 0.004 s`, what is the CFL number? Is the scheme stable?  
**(d)** Write out the explicit update formula for `u_i^(n+1)` using the upwind stencil.  
**(e)** Why is the backward difference (looking left) the correct choice here for `c > 0`?  
**(f)** What happens to accuracy if we double `Δx` (i.e., use only 50 grid points)? What happens to the maximum allowed `Δt`?

**Model Answer:**

**(a)** `Δx = (2 - 0) / (100 - 1) ≈ 0.0202 m` (or equivalently `2/100 = 0.02 m` if treating 100 intervals).

Using 100 equally spaced points over [0, 2]: `Δx = 2 / 99 ≈ 0.0202 m`  
(If the domain has 100 intervals: `Δx = 2/100 = 0.02 m` — either interpretation acceptable, state assumption.)

**(b)** CFL condition: `Δt ≤ Δx / c`

Using `Δx = 0.02 m`: `Δt_max = 0.02 / 4 = 0.005 s`

**(c)** CFL number = `c * Δt / Δx = 4 * 0.004 / 0.02 = 0.016 / 0.02 = 0.8`

`0.8 < 1` → **Stable.** The scheme satisfies the CFL condition.

**(d)** Forward-Euler + backward difference update:

```
u_i^(n+1) = u_i^n - c * (Δt / Δx) * (u_i^n - u[i-1]^n)
```

Rearranged:
```
u_i^(n+1) = (1 - CFL) * u_i^n + CFL * u[i-1]^n
```
where `CFL = c * Δt / Δx = 0.8` in this case.

**(e)** For `c > 0`, the wave travels to the **right** — information is carried from left to right. The backward difference `(u_i - u[i-1]) / Δx` samples the value **upstream** (to the left), i.e., from where the information is coming. This respects the physical domain of dependence. The forward difference would sample downstream (to the right), where the physical information has not yet arrived, producing an unstable result.

**(f)**
- Doubling `Δx` to `0.04 m` doubles the spatial truncation error (from `O(Δx)` to `O(2Δx)`). The solution becomes coarser and less accurate — features smaller than `0.04 m` cannot be resolved.
- The maximum allowed `Δt` **also doubles**: `Δt_max = 0.04 / 4 = 0.01 s`. Fewer time steps are needed. The coarser grid is both less accurate and allows cheaper computation — typical accuracy-vs-cost trade-off.

---

### Q23. [Multi-part] Stability Analysis and Scheme Selection

You are asked to choose a numerical scheme for solving the 1D diffusion equation `∂u/∂t = K ∂²u/∂x²` with `K = 0.5 m²/s` on a grid with `Δx = 0.1 m`.

**(a)** State the FTCS update formula for this equation.  
**(b)** Derive or state the stability condition for this scheme. Calculate the maximum stable `Δt`.  
**(c)** A colleague suggests using `Δt = 0.015 s`. Show whether this is stable or not.  
**(d)** Your colleague instead proposes an implicit (backward-Euler) scheme. Write the implicit update rule.  
**(e)** What is the key advantage of the implicit scheme over the explicit scheme for this problem? What is its main disadvantage in an HPC context?  
**(f)** If this were changed to an advection equation (`∂u/∂t = -c ∂u/∂x`) instead, would the FTCS scheme be viable? Explain.

**Model Answer:**

**(a)** FTCS update for diffusion:

```
u_i^(n+1) = u_i^n + r * (u[i+1]^n - 2*u_i^n + u[i-1]^n)
```

where `r = K * Δt / Δx²` is the diffusion number.

**(b)** Stability condition (from Von Neumann analysis):

```
r = K * Δt / Δx² ≤ 1/2
Δt ≤ Δx² / (2K) = (0.1)² / (2 * 0.5) = 0.01 / 1.0 = 0.01 s
```

Maximum stable `Δt = 0.01 s`.

**(c)** Proposed `Δt = 0.015 s`:

```
r = K * Δt / Δx² = 0.5 * 0.015 / (0.1)² = 0.0075 / 0.01 = 0.75
```

`0.75 > 0.5` → **UNSTABLE.** The diffusion number exceeds the stability limit. The solution will oscillate and diverge.

**(d)** Implicit (backward-Euler) update:

```
u_i^(n+1) = u_i^n + r * (u[i+1]^(n+1) - 2*u_i^(n+1) + u[i-1]^(n+1))
```

Rearranging (all `^(n+1)` terms to the left):

```
-r * u[i-1]^(n+1) + (1 + 2r) * u_i^(n+1) - r * u[i+1]^(n+1) = u_i^n
```

This is a tridiagonal system that must be solved simultaneously for all `u_i^(n+1)`.

**(e)**
- **Advantage:** The implicit scheme is unconditionally stable for the diffusion equation — `Δt` can be made arbitrarily large without triggering blow-up. For a problem with `K = 0.5` and fine grids, the explicit `Δt` limit becomes tiny (`Δt ∝ Δx²`); the implicit scheme allows much larger steps and thus fewer total steps.
- **Disadvantage in HPC:** The implicit scheme couples all grid points at the new time level, requiring a global linear solve each step. In parallel, this means all MPI processes must communicate to solve the tridiagonal system, introducing synchronisation overhead and limiting scalability. Explicit methods are embarrassingly parallel by comparison.

**(f)** For the advection equation, FTCS (forward-Euler + centred space) is **not viable**. It is **unconditionally unstable** — no value of `Δt` prevents blow-up. The centred spatial stencil does not respect the directional nature of advection; it amplifies all error modes regardless of timestep size. The correct approach is to use an upwind (one-sided) stencil with the CFL condition.

---

### Q24. [Multi-part] Taylor Series and Truncation Error

**(a)** Write the Taylor series expansion of `u(x + Δx)` about `x`, including terms up to `O(Δx³)`.  
**(b)** Using this expansion, derive the forward difference approximation for `∂u/∂x` and identify its truncation error order.  
**(c)** Write a second Taylor expansion for `u(x - Δx)`. By combining the two expansions appropriately, derive the centred difference formula and show that its truncation error is `O(Δx²)`.  
**(d)** A student uses a centred difference in space and forward-Euler in time to solve the advection equation. They claim their scheme is "better" than upwind because it has `O(Δx²)` accuracy. Is this claim correct? Justify your answer.  
**(e)** Explain the distinction between truncation error and round-off error.

**Model Answer:**

**(a)** Taylor series for `u(x + Δx)`:

```
u(x + Δx) = u(x) + (∂u/∂x) Δx + (∂²u/∂x²)(Δx²/2!) + (∂³u/∂x³)(Δx³/3!) + O(Δx⁴)
```

**(b)** Forward difference derivation:

Rearranging the Taylor series:
```
(∂u/∂x) = (u(x + Δx) - u(x)) / Δx  -  (∂²u/∂x²)(Δx/2)  -  O(Δx²)
```

The finite difference formula is `(u[i+1] - u[i]) / Δx`. The truncation error is dominated by `-(∂²u/∂x²)(Δx/2)` — this is `O(Δx)`. The scheme is **first-order accurate**.

**(c)** Taylor series for `u(x - Δx)`:

```
u(x - Δx) = u(x) - (∂u/∂x) Δx + (∂²u/∂x²)(Δx²/2) - (∂³u/∂x³)(Δx³/6) + O(Δx⁴)
```

Subtract from the `u(x + Δx)` expansion:

```
u(x + Δx) - u(x - Δx) = 2*(∂u/∂x) Δx + 2*(∂³u/∂x³)(Δx³/6) + O(Δx⁵)
```

The `Δx²` terms cancel (they have the same sign in both expansions). Rearranging:

```
(∂u/∂x) = (u[i+1] - u[i-1]) / (2Δx)  -  (∂³u/∂x³)(Δx²/6)  +  O(Δx⁴)
```

The leading truncation error is `O(Δx²)` — **second-order accurate**.

**(d)** The student's claim is **incorrect in a practical sense**. While the centred difference has `O(Δx²)` spatial accuracy, FTCS applied to the advection equation is **unconditionally unstable** — it blows up regardless of `Δt`. A higher-order-accurate scheme that diverges is worse than a lower-order scheme that produces stable (if somewhat diffusive) results. Accuracy is meaningless if the solution is unstable.

Key point: accuracy and stability are independent properties. For advection, stability requires using a directionally appropriate stencil; the centred scheme fails this requirement at a fundamental level.

**(e)**
- **Truncation error** is the mathematical error introduced by replacing a continuous derivative with a finite difference. It arises because the Taylor series is truncated at a finite number of terms. It depends on grid spacing (`Δx`, `Δt`) and the smoothness of the solution. It is controllable by refining the grid.
- **Round-off error** is the error arising from the finite precision of floating-point arithmetic — computers store real numbers with limited binary digits (e.g., ~15 significant digits for double precision). It is unrelated to grid spacing and is present even if the grid is infinitely fine. In practice, overly fine grids can amplify round-off errors (e.g., catastrophic cancellation in subtraction).

---

### Q25. [Multi-part] Comparing ODE and PDE Time Stepping

Consider the exponential decay ODE `dN/dt = -λN` with `λ = 2 s⁻¹` and `N(0) = 1000`.

**(a)** Write the exact analytical solution.  
**(b)** Apply two steps of the forward-Euler method with `Δt = 0.1 s`. Compare the numerical result at `t = 0.2 s` to the exact value.  
**(c)** How is the time-stepping procedure for a PDE (e.g., advection) different from the ODE case? What additional steps are required?  
**(d)** For the ODE, is there a stability condition analogous to the CFL condition? What is it?

**Model Answer:**

**(a)** Exact solution:

```
N(t) = N_0 * e^(-λt) = 1000 * e^(-2t)
```

**(b)** Forward-Euler: `N_{n+1} = N_n * (1 - λ * Δt) = N_n * (1 - 2 * 0.1) = 0.8 * N_n`

- `N_0 = 1000`
- `N_1 = 1000 * 0.8 = 800` (at `t = 0.1 s`)
- `N_2 = 800 * 0.8 = 640` (at `t = 0.2 s`)

Exact value at `t = 0.2 s`:
```
N_exact = 1000 * e^(-2 * 0.2) = 1000 * e^(-0.4) ≈ 1000 * 0.6703 = 670.3
```

Numerical result: `640`. Error: `670.3 - 640 = 30.3` (about 4.5% — the forward-Euler method underestimates `N` because it uses the rate at the beginning of each interval, which overestimates the decay for a decreasing `N`).

**(c)** For a PDE like advection:
- **Spatial discretization** is required first: the continuous domain is replaced by a grid of points `u_i`.
- **Spatial derivatives** must be computed using a finite difference stencil at each timestep (e.g., `(u_i - u[i-1]) / Δx`).
- **Boundary conditions** must be applied at the domain edges to provide the "missing" neighbour values for boundary cells.
- Only then is the time step applied using the computed spatial derivatives as the rate of change.

For the ODE, there is only one independent variable (time), so no spatial grid or boundary conditions are needed.

**(d)** Yes — for the forward-Euler ODE solver `N_{n+1} = (1 - λΔt) N_n`, stability requires the amplification factor to stay within unity:

```
|1 - λ * Δt| ≤ 1
```

This gives: `-1 ≤ 1 - λ*Δt ≤ 1`

The right inequality is always satisfied for positive `λ, Δt`. The left inequality gives:

```
λ * Δt ≤ 2    →    Δt ≤ 2/λ
```

For `λ = 2`: `Δt ≤ 2/2 = 1 s`. Beyond this, the solution oscillates with growing amplitude (unstable). For best accuracy, `λ * Δt << 1` is preferred (much smaller than the stability limit).

---

## Quick Reference: Key Formulas

| Quantity | Formula | Notes |
|---|---|---|
| Exponential decay (exact) | `N(t) = N_0 * exp(-λt)` | Analytical solution |
| Forward-Euler update | `u^(n+1) = u^n + Δt * f(u^n)` | Explicit, 1st order in time |
| Forward difference | `(u[i+1] - u[i]) / Δx` | O(Δx), first-order |
| Backward difference | `(u[i] - u[i-1]) / Δx` | O(Δx), first-order |
| Centred difference (1st) | `(u[i+1] - u[i-1]) / (2Δx)` | O(Δx²), second-order |
| Centred difference (2nd) | `(u[i+1] - 2u[i] + u[i-1]) / Δx²` | O(Δx²), second-order |
| CFL condition (advection) | `c * Δt / Δx ≤ 1` | Upwind + explicit only |
| Diffusion stability | `K * Δt / Δx² ≤ 0.5` | FTCS explicit diffusion |
| Diffusion FTCS update | `u_i^(n+1) = u_i^n + r*(u[i+1] - 2u_i + u[i-1])` | `r = K*Δt/Δx²` |
| Advection upwind update | `u_i^(n+1) = u_i^n - (c*Δt/Δx)*(u_i - u[i-1])` | For `c > 0` |
| Exact advection solution | `u(x, t) = f(x - ct)` | Rigid translation |
| Diffusion spreading width | `~ 2*sqrt(K*t)` | Gaussian broadening |
