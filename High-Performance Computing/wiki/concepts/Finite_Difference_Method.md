---
title: "Finite Difference Method"
tags: [numerical-methods, finite-difference, math, accuracy, week-3]
date: 2026-05-05
---

# Finite Difference Method

The Finite Difference Method discretizes a spatial or temporal domain to approximate derivatives. The continuous variable $u(x)$ is represented by regularly spaced grid points $u_i = u(x_i)$ with separation $\Delta x$ (or $dx$).

## Approximating Spatial Derivatives

Spatial derivatives are approximated using differences between grid points. 

### First-Order Derivatives
Several stencils can calculate a first derivative $\frac{\partial u}{\partial x}$ at point $i$:
*   **Forward difference:** $\frac{u_{i+1} - u_i}{\Delta x}$
*   **Backward difference:** $\frac{u_i - u_{i-1}}{\Delta x}$
*   **Centred difference:** $\frac{u_{i+1} - u_{i-1}}{2\Delta x}$

### Second-Order Derivatives
The second derivative (gradient of the gradient) can be approximated by applying differences to the first derivatives:
$$ \frac{\partial^2 u}{\partial x^2} \approx \frac{u_{i+1} - 2u_i + u_{i-1}}{(\Delta x)^2} $$

## Boundary Conditions
At the edges of the computational domain ($i=0$ or $i=max$), adjacent points necessary for the finite difference stencil do not exist. Extra information, known as **boundary conditions**, must be supplied. These can be fixed values of $u$ or specified gradients at the boundary.

## Accuracy and Truncation Error
If $u(x)$ is a straight line, finite differences are exact. For curved lines, they are approximations. We quantify the error using a **Taylor series** expansion.

A Taylor series approximates a function $f(x+\Delta x)$ in terms of $f(x)$ and its derivatives:
$$ f(x+\Delta x) = f(x) + \frac{\partial f}{\partial x}\Delta x + \frac{\partial^2 f}{\partial x^2}\frac{(\Delta x)^2}{2!} + \dots $$

By rearranging the Taylor series for a discrete representation, we separate the finite difference from the remainder, which is the **truncation error**:
$$ \frac{\partial u_i}{\partial x} = \frac{u_{i+1} - u_i}{\Delta x} - \left[ \frac{\partial^2 u_i}{\partial x^2} \frac{\Delta x}{2} + \dots \right] $$

*   The remainder is the truncation error, denoted by its leading-order term, e.g., $\mathcal{O}(\Delta x)$.
*   An error of $\mathcal{O}(\Delta x)$ means the scheme is **first-order accurate**.
*   The centred difference stencil $\frac{u_{i+1} - u_{i-1}}{2\Delta x}$ leaves a leading error term of $\mathcal{O}(\Delta x)^2$, making it **second-order accurate** (the error approaches zero more rapidly as $\Delta x$ shrinks).
*   Smaller grid spacing ($\Delta x$) reduces truncation error at the cost of higher computational expense.

*(Note: Truncation error is inherent to the mathematical approximation, distinct from round-off error caused by floating-point precision).*