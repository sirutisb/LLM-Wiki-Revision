---
title: "Exponential Decay"
tags: [ode, time-stepping, mathematics, week-3]
date: 2026-05-05
---

# Exponential Decay

Exponential decay occurs when a quantity decreases at a rate which is proportional to the quantity itself. Common examples include radioactive decay, chemical reaction rates, and heat transfer.

## Equation
The exponential decay of a quantity $N(t)$ is described by the Ordinary Differential Equation (ODE):
$$ \frac{dN}{dt} = -\lambda N $$
Where:
*   $N$: Number of items (e.g., nuclei)
*   $t$: Time
*   $\lambda$: A positive constant related to the half-life ($t_{1/2}$) by $\lambda = \frac{\ln(2)}{t_{1/2}}$

## Numerical Approximation
The differential equation tells us how $N_t$ changes over time, not the value of $N_t$ directly. We can approximate the derivative using small, finite differences:
$$ \frac{dN_t}{dt} \approx \frac{\Delta N_t}{\Delta t} $$

Substituting this into the decay equation gives the change in nuclei over a time interval $\Delta t$:
$$ \Delta N_t \approx -\lambda N_t \Delta t $$

## Computational Solution (Time Stepping)
To solve this computationally:
1.  **Initialise:** Start with $N_0$ items at $t = 0$.
2.  **Calculate Rate:** Find the rate of change at $t$: $\frac{dN_t}{dt} = -\lambda N_t$.
3.  **Calculate Change:** Compute the change $\Delta N_t$ over interval $\Delta t$: $\Delta N_t \approx \frac{dN_t}{dt} \Delta t$. (This assumes the rate remains constant over $\Delta t$).
4.  **Update:** Compute the new value: $N_{t+\Delta t} = N_t + \Delta N_t$.
5.  **Iterate:** Repeat step 2 for the required number of steps.

### Accuracy Trade-off
This scheme assumes a constant rate of change over the discrete time step $\Delta t$. 
*   **Larger time steps:** Less computation required, but the result diverges more from the exact analytical solution (less accurate).
*   **Smaller time steps:** More accurate result, but requires more computational steps.