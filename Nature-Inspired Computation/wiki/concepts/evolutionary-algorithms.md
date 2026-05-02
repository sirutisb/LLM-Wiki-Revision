# Evolutionary Algorithms

**Type:** framework
**Related:** [[genetic-algorithms]], [[genetic-programming]], [[selection]], [[crossover-mutation]], [[representations]], [[fitness-landscapes]]
**Source lectures:** [[lecture02-ea-motivation]], [[lecture03-landscapes]], [[lecture04-ea-detail]]

---

## What it is

An **Evolutionary Algorithm (EA)** is a population-based, stochastic optimisation framework inspired by Darwinian evolution. A population of candidate solutions is iteratively improved by selection, variation (mutation/crossover), and replacement.

---

## Motivation

Exact algorithms (exhaustive search, branch-and-bound) are infeasible for NP-hard problems. Hillclimbing is fast but gets trapped in local optima. EAs escape local optima by:
1. Maintaining a **population** — many regions explored in parallel
2. **Crossover** — combining parts of two good solutions
3. **Stochastic selection** — non-zero probability of selecting sub-optimal individuals (preserving diversity)

---

## The Generic EA Loop

```
1. Initialise population P of N random solutions; evaluate fitness f(s) for each
2. Repeat until termination:
   a. SELECT parents from P (biased toward fitter individuals)
   b. VARY: apply mutation and/or crossover to produce offspring
   c. EVALUATE fitness of offspring
   d. REPLACE: update P using offspring (various strategies)
3. Return best solution found
```

---

## Algorithm types

### Generational EA
- Entire population replaced each generation
- Generate `popsize` new children per generation
- **Elitist variant:** copy the top $n$ individuals unchanged to the next generation to prevent losing the best solution

### Steady-state EA
- Only 1–2 offspring produced per iteration
- Offspring replace the weakest member(s) of the population
- More incremental; suitable for online/continuous optimisation

---

## The three selection-variation-replacement decisions

| Decision | Options | See |
|----------|---------|-----|
| **Selection** | Roulette wheel, rank-based, tournament | [[selection]] |
| **Variation** | Mutation, crossover — representation-specific | [[crossover-mutation]] |
| **Replacement** | Replace worst, replace first weaker, generational | below |

### Replacement strategies (steady-state)
- **Replace Weakest:** always replace the globally weakest individual. Aggressive — keeps population quality high.
- **Replace First Weaker:** replace the first individual in the population that is weaker than the new offspring. Less aggressive.

---

## Key parameters

| Parameter | Typical range | Effect of increasing |
|-----------|--------------|---------------------|
| Population size | 50–500 | Better diversity, slower per generation |
| Mutation rate | 0.001–0.1 | More exploration, can destroy good solutions |
| Crossover rate | 0.6–0.95 | More recombination, less mutation-only |
| Tournament size | 2–10 | Higher selection pressure, faster convergence, less diversity |
| Generations | 100–10,000 | More evaluation budget |

---

## EA vs Hillclimbing vs Local Search

| Property | Hillclimbing | Local Search | EA |
|----------|-------------|-------------|-----|
| Population | 1 | 1 | N |
| Downhill moves | Never | Sometimes (e.g. Monte Carlo, Tabu) | Via diversity/selection |
| Crossover | No | No | Yes |
| Stuck in local optima | Very easily | Less so | Least likely |

---

## Connections

- [[fitness-landscapes]] — the landscape concept explains why EAs work and when they struggle
- [[selection]] — the most studied component; determines evolutionary pressure
- [[crossover-mutation]] — representation-specific variation operators
- [[representations]] — encoding choice is arguably the most important design decision
- [[multi-objective-optimization]] — EA extended to multiple conflicting objectives

---

## Exam notes

- Know the generic EA loop: initialise → select → vary → evaluate → replace
- Distinguish **generational** (full population turnover) vs **steady-state** (incremental replacement)
- Know **elitism**: preserving the best solution across generations prevents regression
- Understand the **exploration–exploitation tradeoff**: high selection pressure → fast convergence but loss of diversity → premature convergence
- The **No Free Lunch theorem**: no EA is universally best; the best EA matches the problem's structure
