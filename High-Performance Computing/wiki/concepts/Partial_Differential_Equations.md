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
Because analytical solutions for complex PDEs are often impossible to find, HPC systems compute **numerical approximations**. This involves discretizing the problem into small, finite steps and solving systems of linear equations to advance the solution.

### Discretization Methods
*   [Finite Difference Method](../concepts/Finite_Difference_Method.md): Approximates derivatives by stepping forward in time/space from given initial and boundary conditions. It is easy to implement but not well-suited for complex geometries or meshes.
*   **Finite Volume Method:** Considers fluxes (the flow of mass, momentum, energy) between adjacent grid cells. It is widely used in Computational Fluid Dynamics (CFD), such as the OpenFOAM software.
*   **Finite Element Method:** Approximates the solution using expansion functions that are non-zero over a small region of the domain. Examples include Nektar++ and Firedrake.

Both finite volume and finite element methods require solving large systems of linear equations, heavily relying on [Linear Algebra and BLAS](../concepts/BLAS_and_Dense_Matrices.md) or [Sparse Matrices](../concepts/Sparse_Matrices_and_CSR.md).

### Examples of Differential Equations
*   [Exponential Decay](../concepts/Exponential_Decay.md) (ODE)
*   [Advection Equation](../concepts/Advection_Equation.md) (PDE)
*   [Diffusion Equation](../concepts/Diffusion_Equation.md) (PDE)
*   **Elliptic Equations (e.g., Poisson Equation):** Some PDEs do not contain a time dependence and therefore cannot be solved via time stepping. An example is the Poisson equation used to calculate self-gravity: $\nabla^2\phi(\mathbf{r}) = 4\pi G\rho(\mathbf{r})$, where $\phi$ is the gravitational potential, $\rho$ is the density, and $G$ is a constant. Solving these also requires computing solutions to systems of linear equations.