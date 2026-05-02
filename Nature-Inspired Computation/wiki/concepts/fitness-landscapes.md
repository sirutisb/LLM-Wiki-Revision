# Fitness Landscapes

**Type:** concept / framework
**Related:** [[evolutionary-algorithms]], [[selection]], [[representations]]
**Source lectures:** [[lecture03-landscapes]]

---

## What it is

A **fitness landscape** is the geometric metaphor that maps a search space $S$ to fitness values $f(s)$, imagining solutions arranged spatially so that the mutation operator defines "distance". Moving to a nearby solution = a small mutation.

Formally: given search space $S$, fitness function $f(s)$, and mutation operator $M$, the **neighbourhood** of $s$ is $\{M(s) : \text{all possible applications of } M\}$.

---

## Why landscapes matter

The shape of the landscape determines how hard it is to optimise:
- **Smooth / unimodal** — hillclimbing works fine; one global peak
- **Rugged / multimodal** — many local optima; hillclimbing gets stuck
- **Deceptive** — local optima lead away from the global optimum
- **Plateau** — large flat region; no gradient to follow

**Key insight:** With realistic large problems, the vast majority of the search space has very poor fitness. Good solutions are concentrated in tiny regions. Large random mutations jump out of these good regions; small mutations stay in them.

---

## Hillclimbing

```
0. Initialise: generate random solution c; evaluate f(c)
1. Mutate copy of c → mutant m; evaluate f(m)
2. If f(m) ≥ f(c): replace c with m (else discard m)
3. Repeat until termination
```

**Problem:** Gets trapped in local optima because it never accepts a worse solution (no downhill moves).

---

## Local Search (beyond hillclimbing)

**Monte Carlo search:** Accept worse solutions with probability $p$ (e.g. 0.1). Escapes local optima randomly.

**Tabu search:** Evaluate all neighbours; accept the best (even if worse than current). Mark recently visited solutions as "tabu" to prevent cycling.

Both are improvements on hillclimbing but still a single-solution approach — vulnerable to local optima on highly multimodal landscapes.

---

## Population-based search advantages

With a **population**, multiple regions are explored simultaneously:
1. Different individuals may be in different basins of attraction
2. Crossover can combine partial solutions from different regions
3. Population diversity prevents premature convergence

---

## Neighbourhoods

The neighbourhood structure is **defined by the mutation operator**, not inherent to the problem:

| Encoding | Mutation | Neighbourhood size |
|----------|----------|-------------------|
| Binary string length $L$ | Flip one bit | $L$ neighbours |
| Permutation length $k$ | Swap adjacent pair | $k$ neighbours |
| Real vector | Add Gaussian noise to one gene | Continuous |

**Important:** Choosing a mutation operator = choosing a neighbourhood = choosing a landscape shape. The encoding and operator are designed together.

---

## Landscape topology types

| Type | Description | Difficulty |
|------|-------------|-----------|
| Unimodal | Single global optimum, smooth | Easy |
| Multimodal | Multiple local optima | Medium–Hard |
| Plateau | Large flat region | Hard |
| Deceptive | Local optima mislead toward wrong region | Very hard |

Most real-world problems are **multimodal** — locally smooth but globally rugged.

---

## Connections

- [[evolutionary-algorithms]] — populations address the local optima problem
- [[representations]] — encoding choice determines landscape shape
- [[selection]] — selection pressure determines how fast the population climbs the landscape
- [[ant-colony-optimization]] — pheromone trails are a landscape-like structure on a graph

---

## Exam notes

- Hillclimbing = population of 1, no downhill moves — gets stuck in local optima
- Population-based search explores multiple landscape regions simultaneously
- Mutation operator **defines** the neighbourhood, which **defines** the landscape
- A landscape that looks rugged at one scale may be smooth at another (depends on mutation step size)
- Crossover = jumping between two known-good regions of the landscape (not a random jump)
