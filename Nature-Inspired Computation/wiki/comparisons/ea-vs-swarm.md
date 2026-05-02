# Evolutionary Algorithms vs Swarm Intelligence

## Overview

Both EA and SI are population-based nature-inspired optimisation frameworks. Both maintain a set of candidate solutions and iteratively improve them. The key difference lies in **how individuals communicate and what metaphor structures the algorithm**.

---

## Comparison table

| Dimension | Evolutionary Algorithms | Swarm Intelligence (ACO/PSO) |
|-----------|------------------------|------------------------------|
| **Biological inspiration** | Darwinian evolution | Collective animal behaviour |
| **Individual memory** | None (no single-individual history) | PSO: pbest per particle; ACO: no individual memory |
| **Communication** | Indirect (through selection and shared population) | Direct (PSO: gbest known to all) or indirect (ACO: pheromone environment) |
| **Shared memory** | None beyond the population | ACO: pheromone matrix; PSO: gbest |
| **Key operators** | Selection + crossover + mutation | Velocity update (PSO); pheromone update (ACO) |
| **Crossover** | Yes (standard) | No (PSO has no crossover; ACO transitions are individual) |
| **Diversity mechanism** | Mutation + crossover + selection pressure | Evaporation (ACO); random velocity terms $z_1, z_2$ (PSO) |
| **Best for** | General purpose; any encoding | PSO: continuous; ACO: discrete/combinatorial |
| **Parameters** | Many (encoding-specific) | Fewer; PSO: $c_1, c_2$, swarm size |
| **Theoretical grounding** | Schema theorem; convergence proofs | ACO: convergence results; PSO: less formal |

---

## When to use which

**Use EA when:**
- Problem requires non-standard encoding (permutation, tree)
- Domain-specific crossover operators add significant value
- Well-understood problem class with known encoding strategies

**Use PSO when:**
- Problem is naturally real-valued (continuous optimisation)
- Fewer parameters is important
- Faster initial convergence on smooth landscapes wanted

**Use ACO when:**
- Problem is naturally a sequencing/routing problem (TSP, scheduling)
- Can represent solutions as paths through a construction graph
- Domain heuristics (e.g. distance) are available and can be incorporated as $\eta$

---

## Synthesis

The distinction between EA and SI is somewhat artificial at an algorithmic level — both are population-based stochastic search. PSO can be seen as an EA without crossover but with a persistent personal memory (pbest). ACO can be seen as an EA where "selection" is replaced by pheromone-guided probabilistic construction.

The deeper difference is in the **abstraction**: EAs abstract "chromosomes" and "fitness evaluation"; SI abstracts "agents" interacting with an "environment." Both are valid and often complementary; on many problems, their performance is comparable.

---

## Related pages
- [[evolutionary-algorithms]]
- [[pso]]
- [[ant-colony-optimization]]
- [[swarm-intelligence]]
- [[metaheuristics-critique]]
