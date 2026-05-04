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

**Physical Interpretation:**
The condition means that no advected material can travel further than one grid cell ($\Delta x$) within a single time step ($\Delta t$). If $\Delta t$ is too large, information "skips" across grid cells, violating the mathematical domain of dependence and causing the numerical solution to blow up.