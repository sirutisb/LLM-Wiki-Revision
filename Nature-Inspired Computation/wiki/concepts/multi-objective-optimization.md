# Multi-Objective Optimisation (MOO)

**Type:** framework / problem class
**Related:** [[evolutionary-algorithms]], [[nsga-ii]], [[mopso]]
**Source lectures:** [[lecture13-14-emo]]

---

## What it is

**Multi-objective optimisation** involves simultaneously optimising two or more conflicting objectives. There is no single "best" solution — instead, there is a **Pareto front** of trade-off solutions.

**Example:** Offshore wind farm layout:
- Objective 1: minimise cost
- Objective 2: maximise power output
- These conflict — cheapest design = fewest turbines = worst power; best power = many turbines = most expensive

**Formal definition:**
$$\text{minimise } \mathbf{y} = (f_1(\mathbf{x}), f_2(\mathbf{x}), \ldots, f_M(\mathbf{x}))$$
where $M$ is the number of objectives and $\mathbf{x}$ is the decision vector.

---

## Dominance

Solution $\mathbf{a}$ **dominates** solution $\mathbf{b}$ ($\mathbf{a} \succ \mathbf{b}$) if:
- $\mathbf{a}$ is **at least as good** as $\mathbf{b}$ on **every** objective, AND
- $\mathbf{a}$ is **strictly better** than $\mathbf{b}$ on **at least one** objective

**Mutually non-dominating:** neither dominates the other (each is better on at least one objective).

---

## Pareto front

The **Pareto front** is the set of all non-dominated solutions. These are the optimal trade-offs — you can't improve on any objective without worsening another.

**Desired Pareto front approximation:**
- **Evenly spaced** solutions along the front
- **Covers the largest possible area** (spread/diversity)
- **Close to the true Pareto front** (convergence)

---

## Non-dominated Sorting

Used to assign **rank** to every solution in a population:

```
Rank 0: the non-dominated set (Pareto front approximation)
Rank 1: non-dominated set of remaining solutions (after removing Rank 0)
Rank 2: non-dominated set of remaining (after removing Ranks 0 & 1)
...
```

Solutions of Rank 0 are selected first in replacement; Rank $k$ before Rank $k+1$.

---

## Selection for MOO

Single-objective tournament selection doesn't directly apply. Options:

### Basic Pareto dominance tournament
- Select two random individuals; if one dominates → select it
- Problem: if both are non-dominated → random tiebreak → insufficient pressure

### Pareto dominance tournament with comparison set
1. Select two random solutions $x$ and $y$
2. Select comparison set $Z = \{z_i\}_{i=1}^C$
3. Prefer the solution that is non-dominated w.r.t. more members of $Z$
4. Tiebreak: random
- $C$ controls selection pressure

### Crowding distance tiebreak (NSGA-II approach)
When two solutions have the same rank, prefer the one in a **less crowded** area of objective space. See [[nsga-ii]].

---

## Niching

**Niching** = separate the objective space into regions; prefer solutions in less-populated regions. Controlled by a **niche radius** parameter.
- Promotes diversity across the Pareto front
- More parameters to tune than crowding distance

---

## Why EAs are ideal for MOO

Population-based search:
- Maintains a **diverse set** of solutions naturally
- Can approximate the entire Pareto front in a single run
- Single-objective EA would require separate runs for each point (with weighted objectives)

**Alternative: weighted sum scalarisation:**
Run separate EAs for different weights $w_1 f_1 + w_2 f_2$. Problems:
- Requires $k$ separate runs for $k$ Pareto front points
- Misses Pareto front regions in non-convex areas

---

## Many-objective optimisation (≥ 4 objectives)

Three key challenges:
1. **Visualisation:** cannot display a 4+ dimensional Pareto front easily
2. **Degraded search:** with many objectives, nearly all solutions become non-dominated → rank 0 contains almost the whole population → no selection pressure
3. **Solution count:** number of solutions needed to approximate Pareto front grows exponentially

**Solution:** Replace dominance-based comparison with **average rank** or **hypervolume contribution** (see [[mopso]] and [[nsga-ii]]).

Visualisation with **parallel coordinate plots** for many objectives.

---

## Connections

- [[nsga-ii]] — most cited multi-objective EA; uses fast non-dominated sort + crowding distance
- [[mopso]] — extends PSO to multi-objective using archives
- [[evolutionary-algorithms]] — MOGA = EA with multi-objective selection
- [[representations]] — same encoding issues apply; problem-specific

---

## Exam notes

- **Dominance**: $a$ dominates $b$ ↔ at least as good on all objectives AND strictly better on at least one
- **Pareto front** = set of all non-dominated solutions = the optimal trade-off curve
- **Non-dominated sorting**: peel off Pareto layers iteratively to assign ranks
- **Crowding distance**: prefer solutions in sparsely populated regions of the Pareto front
- Many-objective (≥4): dominance loses power — most solutions non-dominated → no selection pressure
- EAs preferred over scalarisation: approximate whole Pareto front in one run
