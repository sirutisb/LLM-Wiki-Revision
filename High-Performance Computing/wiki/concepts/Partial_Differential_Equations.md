---
title: "Partial Differential Equations (PDEs)"
tags: [pde, mathematics, numerical-methods, week-3]
date: 2026-05-05
---

# Partial Differential Equations (PDEs)

Many high-performance computing applications, such as weather forecasting, fluid dynamics, and astrophysics, require calculating numerical solutions to differential equations.

## Definitions
*   **Differential Equation (DE):** An equation that contains one or more derivatives. Derivatives describe the rate of change of one variable with respect to another (e.g., velocity $v = \frac{dx}{dt}$).
*   **Partial Differential Equation (PDE):** A differential equation that contains derivatives with respect to *more than one variable*.

If a variable $u$ depends on two variables $x$ and $t$, $u = u(x,t)$:
*   **Time Derivative:** The rate of change of $u$ with respect to time $t$ is denoted as $\frac{\partial u}{\partial t}$ or $\frac{du}{dt}$.
*   **Spatial Derivative:** The rate of change of $u$ with respect to a spatial coordinate $x$ is denoted as $\frac{\partial u}{\partial x}$. Spatial gradients describe how a property changes in space (e.g., pressure gradients in fluid motion).

The curly $\partial$ symbol indicates the rate of change with respect to one variable while keeping the other variable(s) constant.

## Numerical Solutions
Because analytical solutions for complex PDEs are often impossible to find, HPC systems compute **numerical approximations**. This involves discretizing the problem into small, finite steps (e.g., using the [Finite Difference Method](../concepts/Finite_Difference_Method.md)) and stepping forward in time from given initial conditions and boundary conditions.

### Examples of Differential Equations
*   [Exponential Decay](../concepts/Exponential_Decay.md) (ODE)
*   [Advection Equation](../concepts/Advection_Equation.md) (PDE)
*   [Diffusion Equation](../concepts/Diffusion_Equation.md) (PDE)