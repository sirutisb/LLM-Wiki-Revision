---
title: "Diffusion Equation"
tags: [pde, diffusion, numerical-methods, week-3]
date: 2026-05-05
---

# Diffusion Equation

**Diffusion** is the net movement of a quantity from a region of high concentration to a region of lower concentration. It is caused by random molecular motions (e.g., spreading dye in a liquid, heat transfer).

## 1-D Diffusion Equation
The diffusion of a scalar field $u(x, t)$ is described by a PDE containing a time derivative and a **second-order** spatial derivative:
$$ \frac{\partial u}{\partial t} = K \frac{\partial^2 u}{\partial x^2} $$
Where $K$ is a diffusion constant.

The second derivative $\frac{\partial^2 u}{\partial x^2}$ represents the *gradient of the gradient*, which measures the curvature of the field.
*   Positive curvature implies $\frac{\partial u}{\partial t}$ is positive ($u$ increases).
*   Negative curvature implies $\frac{\partial u}{\partial t}$ is negative ($u$ decreases).
*   Over time, diffusion causes variations in $u$ to spread out and smoothen.

## 2-D Diffusion Equation
The 2-D diffusion equation involves two second derivatives with respect to $x$ and $y$:
$$ \frac{\partial u}{\partial t} = K \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right) = K \nabla^2 u $$

## Numerical Solution
Like advection, diffusion can be solved numerically using time-stepping and the [Finite Difference Method](../concepts/Finite_Difference_Method.md). 

For the 1-D second derivative, the finite difference approximation uses values from the point itself and its two neighbors:
$$ \frac{\partial^2 u}{\partial x^2} \approx \frac{u_{i+1} - 2u_i + u_{i-1}}{(\Delta x)^2} $$

For 2-D, a "five-point stencil" is commonly used, involving the central point $(i, j)$ and its top, bottom, left, and right neighbors.

Boundary conditions must be provided at both edges of the domain to calculate the spatial derivatives for boundary cells.