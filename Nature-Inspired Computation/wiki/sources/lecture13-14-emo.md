# Lectures 13 & 14 — Multi-objective Evolutionary Algorithms

**File:** `raw/text/13-14-emo.txt`
**Lecturer:** Dr David Walker
**Concepts introduced:** [[multi-objective-optimization]], [[nsga-ii]]

---

## Summary

Introduces multi-objective optimisation, Pareto dominance, non-dominated sorting, crowding distance, and NSGA-II. Uses offshore wind farm layout as the motivating real-world example throughout.

## Key content

### Motivating example: offshore wind farm
Minimise cost AND maximise power. Wind wake effect: turbines in shadow of others generate less power. Trade-off: more turbines = more power but more expensive. Need a multi-objective approach.

### Multi-objective problem definition
Objective vector: $\mathbf{y} = (f_1(\mathbf{x}), f_2(\mathbf{x}), \ldots, f_M(\mathbf{x}))$

### Pareto dominance
$a$ dominates $b$ if $a$ is at least as good as $b$ on all objectives AND strictly better on at least one.
- Red solution: better on both $f_1$ and $f_2$ than Green → Red dominates Green
- Red vs Black: Red better on $f_2$, Black better on $f_1$ → mutually non-dominating

### Pareto front
The set of all non-dominated solutions. Goal: find solutions that are evenly spaced AND cover the largest possible area of the front.

### Non-dominated sorting
Iteratively peel off Pareto layers:
- Rank 0: non-dominated set; remove and find
- Rank 1: next non-dominated set; remove and find
- Continue…

### Selection for MOO: Pareto dominance tournament with comparison set
1. Select $x$ and $y$
2. Select comparison set $Z$ of size $C$
3. If $x$ (or $y$) is non-dominated w.r.t. all $z_i \in Z$ → select it
4. Equal domination → random tiebreak
Parameter $C$ controls selection pressure.

### Tiebreak: niching vs crowding distance
**Niching:** define fitness landscape niches; prefer solutions in less populated niches. Requires niche radius parameter.
**Crowding distance (NSGA-II):** measure "cuboid" formed by neighbours in objective space; prefer larger.

### NSGA-II
- **Elitist** MOGA (parents + offspring combined; best N selected)
- **Fast non-dominated sort**
- **Crowding distance** as tiebreaker
- No extra parameters beyond standard GA

NSGA-II execution:
1. $P$ (N) + offspring $Q$ (N) → $R$ (2N)
2. Fast non-dominated sort of $R$
3. Fill new $P$: take complete ranks until full; last rank sorted by crowding distance (descending)
4. Discard remainder

### Elitist vs non-elitist
Elitist (PAES, SPEA, NSGA-II) superseded non-elitist because: no loss of good solutions; faster convergence; fewer parameters.

### Weighted sum alternative
Run separate GA per weight combination. Problems: $k$ runs needed; misses non-convex Pareto regions.

### Many-objective optimisation
≥4 objectives → dominance loses power (most solutions non-dominated → no selection pressure). Issues: visualisation, search capability reduction, exponential solution count growth. NSGA-III uses reference points.

## Key takeaways
- Pareto dominance replaces single fitness comparison
- NSGA-II: fast non-dominated sort + crowding distance + elitism = no extra parameters
- Many-objective: need alternative to dominance (average rank, hypervolume)

## Links to concepts
- [[multi-objective-optimization]]: full MOO framework
- [[nsga-ii]]: detailed algorithm with pseudocode
- [[mopso]]: analogous for PSO
