---
title: "Numerical Stability and CFL Condition"
tags: [numerical-methods, stability, math, week-3]
date: 2026-05-05
---

# Numerical Stability and CFL Condition

When solving [Partial Differential Equations (PDEs)](../concepts/Partial_Differential_Equations.md) numerically, we must ensure the solution is both accurate and **stable**.

## Stability Definitions
For a numerical scheme to be viable, the computed solution must remain finite. If errors in the solution amplify and grow without bound over time, the scheme is unstable.

*   **Unconditionally stable:** Errors are always damped, and the solution remains finite regardless of parameters.
*   **Unconditionally unstable:** Errors are always amplified, and the solution diverges.
*   **Conditionally stable:** The solution is stable only if certain constraints on the parameters (like time step and spatial resolution) are met.

Stability depends on:
1.  The specific equation being solved.
2.  The finite difference stencil used for spatial derivatives.
3.  The time-stepping method used.

For instance, solving the [Advection Equation](../concepts/Advection_Equation.md) using a forward-in-time ("forward-Euler") time step and a centred difference for space is unconditionally unstable.

## Courant-Friedrichs-Lewy (CFL) Condition
If we solve the advection equation using a forward-Euler time step and a *one-sided* spatial difference, the scheme is conditionally stable. The stability constraint is known as the **CFL condition**:

$$ \Delta t \le C \frac{\Delta x}{v_{max}} $$

Where:
*   $\Delta t$: Time step size
*   $\Delta x$: Grid spacing (spatial resolution)
*   $v_{max}$: Maximum velocity in the field
*   $C$: The Courant number, a constant where $0 < C < 1$.

The dimensionless ratio `c * Δt / Δx` is called the **Courant number** (or CFL number). The CFL condition requires it stays ≤ C_max (typically 1 for explicit schemes).

**Physical Interpretation:**
$c \times \Delta t$ = how far information physically travels in one timestep; $\Delta x$ = size of one grid cell. The condition means information must not outrun the numerical stencil — no advected material can travel further than one grid cell per timestep. If violated, errors oscillate and grow exponentially.

The condition means that no advected material can travel further than one grid cell ($\Delta x$) within a single time step ($\Delta t$). If $\Delta t$ is too large, information "skips" across grid cells, violating the mathematical domain of dependence and causing the numerical solution to blow up.

**Explicit vs. Implicit:**
- **Explicit methods** are strongly constrained by CFL; violating it causes blow-up.
- **Implicit methods** can sometimes remain stable even when CFL > 1, though accuracy may still degrade.

**Important:** CFL is usually a *necessary* condition for stability, not always sufficient. The forward-Euler + centred-difference scheme for advection is unconditionally unstable regardless of CFL.

**Example:** wave speed c = 10 m/s, Δx = 0.1 m, CFL ≤ 1 → Δt ≤ Δx/c = 0.01 s.

*Named after mathematicians Richard Courant, Kurt Friedrichs, and Hans Lewy.*