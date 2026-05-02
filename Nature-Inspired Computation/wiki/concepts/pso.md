# Particle Swarm Optimisation (PSO)

**Type:** algorithm
**Related:** [[swarm-intelligence]], [[flocking-boids]], [[evolutionary-algorithms]], [[mopso]]
**Source lectures:** [[lecture11-flocking]], [[lecture12-pso]], [[lecture15-mopso]]

---

## What it is

**Particle Swarm Optimisation (PSO)** is a population-based, continuous optimisation algorithm introduced by Kennedy & Eberhart (1995). Each individual ("particle") has a position (candidate solution) and a velocity. Particles are attracted toward the best position they have personally visited (**pbest**) and the best position any particle in the swarm has visited (**gbest**).

Inspired by the "Cornfield Vector" — birds/fish converge on a food source by combining personal experience and social information from the group.

---

## Algorithm

```
1. Initialise N particles with random positions x_i and velocities v_i
2. For each particle i:
   - Set pbest_i = x_i
3. Set gbest = best x_i in swarm
4. Repeat until termination:
   For each particle i:
     a. UPDATE VELOCITY
     b. UPDATE POSITION
     c. Evaluate f(x_i)
     d. If f(x_i) > f(pbest_i): pbest_i = x_i
     e. If f(x_i) > f(gbest): gbest = x_i
```

---

## The Update Equations

### Position update
$$x_{ij}(t+1) = x_{ij}(t) + v_{ij}(t+1)$$

where $j$ indexes dimension, $i$ indexes particle.

### Velocity update
$$v_{ij}(t+1) = v_{ij}(t) + c_1 \cdot z_1 \cdot (p_{ij} - x_{ij}(t)) + c_2 \cdot z_2 \cdot (g_j - x_{ij}(t))$$

**Three terms:**
| Term | Role | Name |
|------|------|------|
| $v_{ij}(t)$ | Previous velocity (momentum/inertia) | Inertia component |
| $c_1 z_1 (p_{ij} - x_{ij})$ | Pull toward personal best | Cognitive (personal) component |
| $c_2 z_2 (g_j - x_{ij})$ | Pull toward global best | Social (global) component |

**Variables:**
- $c_1, c_2$: acceleration coefficients (cognitive and social weights, typically 2.0)
- $z_1, z_2 \sim U(0,1)$: independent random draws each iteration (prevent premature convergence)
- $p_{ij}$: particle $i$'s best position on dimension $j$
- $g_j$: swarm's global best position on dimension $j$

---

## Parameters

| Parameter | Effect of increasing |
|-----------|---------------------|
| **Swarm size $N$** | Better global search; slower iteration |
| **$c_1$ (cognitive)** | Particles trust personal history more → slower social convergence |
| **$c_2$ (social)** | Particles follow swarm best more → faster convergence, less diversity |
| **Neighbourhood size** | Smaller neighbourhood → more diversity; larger → faster convergence |

**Too low $c_1$, $c_2$:** slow convergence
**Too high $c_1$, $c_2$:** oscillation, premature convergence

---

## Termination criteria

- Maximum number of iterations
- An acceptable solution quality is found
- No improvement for $N$ iterations
- Normalised swarm radius ≈ 0 (swarm has converged)

---

## Binary PSO

PSO is naturally continuous. Two approaches for discrete/binary spaces:

**Approach 1 — Velocity as probability (traditional BPSO):**
$$x_{ij}(t+1) = \begin{cases} 1 & \text{if } \text{rand}() < v_{ij}(t+1) \\ 0 & \text{otherwise} \end{cases}$$
Velocity is clipped to $[0, 1]$ before use as a probability threshold.

**Approach 2 — Geometric/Hamming BPSO:**
No explicit velocity. Position updated by moving proportionally toward pbest and gbest. In Hamming space this corresponds to a multi-string recombination (similar to crossover).

---

## PSO vs Evolutionary Algorithms

| Property | PSO | EA |
|----------|-----|-----|
| Representation | Real vector (native) | Any |
| Crossover | None (velocity acts similarly) | Yes |
| Memory per individual | pbest (personal history) | No individual memory |
| Global memory | gbest | Entire population |
| Diversity mechanism | Stochastic velocity update | Mutation, crossover |
| Good for | Continuous optimisation | General purpose |
| Parameters | $c_1, c_2$, swarm size | Many (encoding-specific) |

---

## PSO vs ACO

| Property | PSO | ACO |
|----------|-----|-----|
| Communication | Direct (gbest shared) | Indirect (pheromone = stigmergy) |
| Space | Continuous | Discrete |
| Memory | Per-particle (pbest) + global (gbest) | Pheromone matrix |
| Diversity | $z_1, z_2$ randomness | Pheromone evaporation |

---

## Connections

- [[flocking-boids]] — PSO formalises flocking into an optimisation algorithm
- [[multi-objective-optimization]] → [[mopso]] — extends PSO to multi-objective problems
- [[swarm-intelligence]] — PSO is the canonical SI algorithm for continuous optimisation

---

## Exam notes

- Three components of velocity: **inertia** + **cognitive** (personal best) + **social** (global best)
- $z_1, z_2 \sim U(0,1)$: randomness prevents premature convergence
- $c_1$ controls personal confidence; $c_2$ controls social confidence
- PSO has **no crossover** — the velocity update combines information from multiple sources instead
- Binary PSO: velocity interpreted as probability for each bit (Approach 1) or Hamming-space recombination (Approach 2)
- PSO struggles with discrete problems natively — need binary/integer PSO extensions
