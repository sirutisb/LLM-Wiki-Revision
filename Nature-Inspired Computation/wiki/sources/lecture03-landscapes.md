# Lecture 3 — Search Landscapes and Population-Based Search

**File:** `raw/text/2024NICLecture3.txt`
**Lecturer:** Dr Alberto Moraglio
**Concepts introduced:** [[fitness-landscapes]], [[evolutionary-algorithms]]

---

## Summary

Introduces the fitness landscape metaphor, shows hillclimbing on TSP as a concrete example, then motivates population-based search as a solution to hillclimbing's local optima problem. Also introduces local search (Monte Carlo, Tabu).

## Key content

### Hillclimbing on TSP
Concrete 5-city TSP example. Encoding: permutation. Mutation: swap adjacent nodes. Shows accepted and rejected mutants step by step.

Start ABDEC (fitness 32) → BADEC (fitness 28) → ... eventually converges.

### Landscapes
The graph of $f(s)$ over $S$ imposed by mutation. Landscape shape depends on encoding + mutation.

**Typical landscape:** Huge majority of space = poor fitness; good solutions in tiny islands. Large mutations jump out of good regions.

**Landscape types:** Unimodal, Multimodal (most realistic), Plateau, Deceptive.

### Neighbourhoods
Given mutation $M$, neighbourhood of $s$ = all possible mutants of $s$:
- Binary length $L$, flip one bit → $L$ neighbours
- Permutation length $k$, swap adjacent pair → $k$ neighbours

### Local Search (beyond HC)
- **Monte Carlo:** accept worse solution with probability $p$
- **Tabu search:** evaluate all neighbours; take best even if worse; avoid "tabu" recently visited solutions

### Population-based search
Adds two differences from single-solution search:
1. Need to select which of multiple solutions to vary → selection
2. Can recombine/crossover multiple solutions → crossover

## Key takeaways
- Hillclimbing gets stuck in local optima; local search reduces this but still stuck
- Population explores multiple landscape regions simultaneously
- Mutation defines the neighbourhood, which defines the landscape topology

## Links to concepts
- [[fitness-landscapes]]: complete treatment
- [[evolutionary-algorithms]]: population-based search
- [[selection]]: motivates why selection is needed with a population
