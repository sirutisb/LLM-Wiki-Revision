# Lecture 4 — Evolutionary Algorithms in Detail

**File:** `raw/text/2024NICLecture4.txt`
**Lecturer:** Dr Alberto Moraglio
**Concepts introduced:** [[selection]], [[crossover-mutation]], [[representations]], [[evolutionary-algorithms]]

---

## Summary

Detailed treatment of GA variants, selection operators, replacement strategies, and genetic operators for different encodings. Provides full pseudocode for two complete EA implementations.

## Key content

### Two GA types
**Generational:** Replace entire population per generation. Elitist variant copies top $n$ unchanged.
**Steady-state:** Apply operators 1–2 times, replace bad solutions. Replace Weakest vs Replace First Weaker strategies.

### Selection methods
- **Roulette wheel (fitness proportionate):** $P(i) = f_i / \sum f_k$ — problems with superfit individuals and negative/minimisation fitness
- **Rank-based:** $P(i) \propto \text{rank}_i$ (or $\text{rank}_i^b$) — immune to superfit
- **Tournament:** random tournament of size $t$; return best — tunable, efficient, modern standard

### Crossover operators (k-ary)
- 1-point, 2-point, uniform crossover — all illustrated

### Mutation operators
- k-ary: single-gene (random new value), multi-gene, swap
- Real-valued: single-gene Gaussian, vector mutation
- Permutation: swap (standard mutation breaks validity)

### Complete EA pseudocode
**Steady-state, mutation-only, replace-worst, tournament selection:**
```
0. Initialise: popsize random solutions, evaluate
1. Tournament-select parent X (tsize)
2. With prob mute_rate: mutate X → M; else M = X
3. Evaluate M
4. If M ≥ worst in pop: replace worst with M
5. Termination check; else go to 1
```

**Generational, elitist, rank-based selection, crossover+mutation:**
```
0. Initialise: popsize random solutions
1. Rank-select 2*(popsize-1) parents I
2. Pair up; apply Vary (crossover at cross_rate + mutation) → children C
3. Evaluate C; keep best from G; add all C to G
4. Termination check
```

## Key takeaways
- Representation, selection, and operators are all designed together
- Tournament selection is the modern standard (efficient, tunable, no scaling issues)
- Replacement strategy affects population diversity and convergence speed

## Links to concepts
- [[selection]]: all three methods explained
- [[crossover-mutation]]: all operators for different encodings
- [[representations]]: encoding types introduced here
- [[evolutionary-algorithms]]: two complete pseudocode implementations
