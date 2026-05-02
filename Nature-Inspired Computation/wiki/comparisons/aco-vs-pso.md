# ACO vs PSO

## Overview

Both ACO and PSO are Swarm Intelligence algorithms, but they differ significantly in their problem domain, communication mechanism, and memory structure. Understanding this comparison clarifies when to use each.

---

## Comparison table

| Dimension | ACO | PSO |
|-----------|-----|-----|
| **Biological inspiration** | Ant pheromone trail following | Bird/fish swarming (Cornfield Vector) |
| **Problem domain** | Discrete / combinatorial (graphs) | Continuous (real vectors) |
| **Communication** | Indirect (stigmergy via pheromone) | Direct (gbest shared across swarm) |
| **Memory** | Pheromone matrix (shared, global) | pbest (personal) + gbest (global) |
| **Solution construction** | Ants construct solutions step by step | Particles have complete solutions at all times |
| **Diversity** | Pheromone evaporation $\rho$ | Random coefficients $z_1, z_2$; inertia |
| **Heuristic incorporation** | $\eta_{ij}$ term in transition rule | Not standard (requires modification) |
| **Main parameters** | $\alpha, \beta, \rho, m$ (ants), $Q$ | $c_1, c_2$, swarm size, iterations |
| **Discrete problems** | Native | Binary PSO needed (Approach 1 or 2) |
| **Continuous problems** | Requires modification | Native |
| **Convergence** | Pheromone concentration → one path | Swarm converges toward gbest region |
| **Speed** | Slower (pheromone accumulates gradually) | Often faster initial convergence |

---

## Key structural difference

**ACO:** solutions are *constructed* incrementally (ant moves node-by-node). The construction graph encodes the solution space. Pheromone = statistical memory of which decisions led to good complete solutions.

**PSO:** solutions are *complete* at all times (particles have positions in the full solution space). Movement = simultaneous update of all dimensions. Personal history = pbest; collective history = gbest.

---

## Multi-objective extensions

Both can be extended to multi-objective optimisation:
- [[nsga-ii]] is the EA analogue (Pareto front + crowding distance)
- [[mopso]] = PSO + archive for Pareto front approximation
- ACO multi-objective variants exist (maintain a Pareto archive; update pheromone based on non-dominated solutions)

---

## When to use which

**ACO:** naturally suited to TSP, job scheduling, routing — any problem where solutions are sequences/paths through a graph. Heuristics (distance, urgency) integrate cleanly.

**PSO:** best for continuous problems (antenna design, neural network weights, parameter tuning). Simpler to implement, fewer concepts.

---

## Related pages
- [[ant-colony-optimization]]
- [[pso]]
- [[swarm-intelligence]]
- [[mopso]]
