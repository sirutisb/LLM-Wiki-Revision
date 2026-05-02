# Lecture 12 — Swarm Intelligence III: Particle Swarm Optimisation

**File:** `raw/text/12-pso.txt`
**Lecturer:** Dr David Walker
**Concepts introduced:** [[pso]]

---

## Summary

Full treatment of PSO: the "Cornfield Vector" biological motivation, the position and velocity update equations with all components explained, parameter guidance, and Binary PSO variants for discrete problems.

## Key content

### Motivation: the Cornfield Vector (Rooster Effect)
When food is left for birds, many birds converge on it within minutes. Define fitness = "odour of the food." The knowledge of where the food is (global best) is incorporated into local behaviour — all particles collaborate to find the optimum quickly.

### PSO model
- **Particle:** candidate solution with position and velocity (no mass, no volume)
- **Swarm:** N particles; velocity matching not strictly included (unlike true flocking)
- **Optimisation:** discover near-optimal solutions via particle population

### Continuous optimisation
PSO designed for continuous representations, e.g.:
- Feature selection (binary): `x = (1, 1, 0, 0, 1, 0, 0, 1)`
- TSP (permutation): `x = (2, 0, 6, 7, 5, 1, 4, 3)`
- Antenna design (real): `x = (-1.322, 0.130, 2.312, -0.644, ...)`

Applications: antenna design, aircraft wings, amplifiers, controllers, circuits.

### Equations (complete)

**Position update:**
$$x_{ij}(t+1) = x_{ij}(t) + v_{ij}(t+1)$$

**Velocity update:**
$$v_{ij}(t+1) = v_{ij}(t) + c_1 z_1 (p_{ij} - x_{ij}(t)) + c_2 z_2 (g_j - x_{ij}(t))$$

- $c_1, c_2$: constants — control weighting between personal and global experience
- $z_1, z_2 \sim U(0,1)$: random draws (prevent premature convergence)
- $p_{ij}$: particle $i$'s personal best on dimension $j$ (draws back to best seen areas)
- $g_j$: swarm's global best on dimension $j$ (enables collective knowledge)

### Parameters
- Swarm size (analogue to population size in GA)
- Neighbourhood size (for local best)
- Number of iterations
- Acceleration coefficients $c_1$ and $c_2$

**Too low $c_1, c_2$:** slow progress. **Too high:** premature convergence.

### Termination criteria
- Max iterations
- Acceptable solution found
- No improvement for N iterations
- Normalised swarm radius ≈ 0 (converged)

### Binary PSO
**Approach 1 (Kennedy & Eberhart):** velocity → probability threshold:
$x_{ij}(t+1) = 1$ if $\text{rand}() < v_{ij}$, else 0.

**Approach 2 (Geometric BPSO):** no velocity; move toward pbest and gbest proportionally via multi-string recombination in Hamming space. Mask-based update.

## Key takeaways
- PSO velocity = inertia + cognitive pull + social pull
- Random coefficients $z_1, z_2$ prevent swarm from collapsing too fast
- Binary PSO extends to discrete problems via probability-based bit-flip or Hamming-space recombination

## Links to concepts
- [[pso]]: full algorithm with all variants
- [[flocking-boids]]: the biological inspiration
- [[mopso]]: extends PSO to multi-objective
