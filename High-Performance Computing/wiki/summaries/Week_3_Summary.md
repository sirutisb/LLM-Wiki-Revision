---
title: "Week 3 Summary: Numerical Solutions to PDEs"
tags: [hpc, week-3, pde, numerical-methods]
date: 2026-05-05
---

# Week 3 Summary: Numerical Solutions to PDEs

This week focuses on calculating numerical solutions to Partial Differential Equations (PDEs), a common requirement for many High-Performance Computing (HPC) applications (e.g., fluid dynamics, astrophysics).

## Key Equations Covered
*   **[Exponential Decay](../concepts/Exponential_Decay.md):** An ordinary differential equation describing a quantity decreasing at a rate proportional to itself: $\frac{dN}{dt} = -\lambda N$.
*   **[Advection Equation](../concepts/Advection_Equation.md):** A PDE describing the transport of a scalar field by a velocity field containing a first-order spatial derivative: $\frac{\partial u}{\partial t} = -c \frac{\partial u}{\partial x}$.
*   **[Diffusion Equation](../concepts/Diffusion_Equation.md):** A PDE describing the net movement of a quantity from high to low concentration containing a second-order spatial derivative: $\frac{\partial u}{\partial t} = K \frac{\partial^2 u}{\partial x^2}$.

## Core Concepts
*   **[Partial Differential Equations (PDEs)](../concepts/Partial_Differential_Equations.md):** Equations containing derivatives with respect to more than one variable (typically time and space).
*   **[Finite Difference Method](../concepts/Finite_Difference_Method.md):** A numerical technique for approximating derivatives (both temporal and spatial) using discrete grid points. Includes concepts of spatial resolution, Taylor series expansion, and truncation error (accuracy).
*   **Boundary Conditions:** Values specified at the edge of a domain, necessary to calculate spatial derivatives at the boundaries.
*   **[Numerical Stability and CFL](../concepts/Numerical_Stability_and_CFL.md):** Analysis of whether a numerical scheme's errors remain bounded over time. Examines conditionally stable schemes and the Courant-Friedrichs-Lewy (CFL) condition.

Solutions are typically calculated by discretizing the domain and using time-stepping, calculating spatial derivatives via a finite difference stencil. The choice of time step and spatial resolution directly impacts both the **accuracy** (truncation error) and **stability** of the solution, as well as the overall computational cost.