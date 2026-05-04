---
title: "Advection Equation"
tags: [pde, advection, numerical-methods, week-3]
date: 2026-05-05
---

# Advection Equation

**Advection** is the transport of a quantity by a velocity field. Examples include silt in a river, dust in the atmosphere, or salt in the ocean.

## 1-D Advection Equation
The advection of a scalar field $u(x, t)$ by a constant velocity $c$ is described by a PDE containing a time derivative and a first-order spatial derivative:
$$ \frac{\partial u}{\partial t} = -c \frac{\partial u}{\partial x} $$

*   If the velocity $c$ is positive, the quantity moves to the right.
*   The initial conditions $f(x)$ translate over time as $f(x - ct)$ without changing shape or amplitude.
*   The sign of the spatial gradient $\frac{\partial u}{\partial x}$ determines whether $u$ is increasing or decreasing at a point over time.

## 2-D Advection Equation
The advection of a scalar field $u(x, y, t)$ by a constant velocity vector $c = (c_x, c_y)$ requires calculating two spatial derivatives:
$$ \frac{\partial u}{\partial t} = -\left( c_x \frac{\partial u}{\partial x} + c_y \frac{\partial u}{\partial y} \right) = -c \cdot \nabla u $$

## Numerical Solution
The equation can be solved numerically by:
1.  Discretizing the spatial domain into grid points.
2.  Approximating the spatial derivatives using the [Finite Difference Method](../concepts/Finite_Difference_Method.md) (e.g., using values from adjacent grid points).
3.  Using a time-stepping loop to update the values over time.
4.  Applying boundary conditions at the edges of the domain to allow calculation of gradients at the boundary cells.