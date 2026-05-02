# NSGA-II (Non-dominated Sorting Genetic Algorithm II)

**Type:** algorithm
**Related:** [[multi-objective-optimization]], [[evolutionary-algorithms]], [[mopso]]
**Source lectures:** [[lecture13-14-emo]]

---

## What it is

**NSGA-II** (Deb, Pratap, Agarwal & Meyarivan, 2002) is the most widely cited multi-objective genetic algorithm. It uses **fast non-dominated sort** for ranking and **crowding distance** for diversity. Cited tens of thousands of times.

---

## Algorithm

```
1. Initialise population P (size N)
2. Repeat:
   a. Select, crossover & mutate P → offspring Q (size N)
   b. Combine: R = P ∪ Q (size 2N)
   c. Fast non-dominated sort R → assign ranks 0, 1, 2, ...
   d. Build new P:
      - Add complete Rank 0 front, then Rank 1, etc.
      - When a rank cannot fit fully: sort by crowding distance (descending)
        and take as many as needed to fill P to size N
      - Discard the rest
```

This is **elitist** — good solutions from the parent generation survive into the next.

---

## Fast Non-Dominated Sort

Assigns each solution a rank:
- **Rank 0:** non-dominated solutions (Pareto front approximation)
- **Rank 1:** non-dominated solutions after removing Rank 0
- **Rank 2:** non-dominated solutions after removing Ranks 0 & 1
- … and so on

---

## Crowding Distance

Measures how crowded the neighbourhood of a solution is in objective space. Used as a tiebreaker when two solutions have the same rank: **prefer the less crowded one**.

**Algorithm for a front $Y$ of size $N$, with $M$ objectives:**

```
for each individual i:
    d_i = 0

for each objective m = 1..M:
    sort Y by objective m
    set d_1 = d_N = ∞  (boundary solutions always kept)
    for i = 2..(N-1):
        d_i += (Y[i+1].m - Y[i-1].m) / (f_max_m - f_min_m)
```

Intuition: $d_i$ is the side length of the "cuboid" formed by the neighbouring solutions in objective space. Large distance = isolated = diverse. Small distance = crowded.

**Boundary solutions** ($d = \infty$) are always preferred — guarantees the extreme solutions of the front are retained.

---

## NSGA-II execution diagram

```
Initial pop P (N) → select/crossover/mutate → offspring (N)
                    ↓
         Combined R = P ∪ offspring (2N)
                    ↓
         Fast non-dominated sort → Rank 0, Rank 1, Rank 2, ...
                    ↓
         Fill new P (N): take Rank 0 complete, Rank 1 complete,
         last rank: sort by crowding distance, take top-k
                    ↓
         Discard rest
```

---

## NSGA-II advantages over earlier MOEAs

| Advantage | Why |
|-----------|-----|
| **Elitist** | Parent population can survive → good solutions never lost |
| **No niche radius** | Crowding distance is parameter-free diversity measure |
| **Fast** | $O(MN^2)$ sort; faster than earlier approaches |
| **Converges quickly** | Elitism + selection pressure from dominance |

**Potential issue:** Can prematurely converge on some problems (some evidence from literature).

---

## Elitist vs non-elitist

**Non-elitist MOGA:** New population = children only. Parents discarded even if they were excellent.

**Elitist MOGA (NSGA-II):** New population from $P \cup Q$. Elitist MOGAs (also: PAES, SPEA) have largely superseded non-elitist versions because:
- Elitism prevents loss of good solutions
- Faster practical convergence

---

## Crowding distance vs niching

| Feature | Crowding distance | Niching |
|---------|------------------|---------|
| Parameters | None | Niche radius (extra parameter) |
| Computation | $O(MN \log N)$ | $O(N^2)$ |
| Result | Promotes diversity | Promotes diversity |
| Used in | NSGA-II | Earlier MOEAs |

---

## Real-world application example

**Offshore wind farm layout (Walker et al., 2021):**
- Two objectives: minimise cost AND maximise power output
- Wind wake effect: turbines in shadow of others produce less power
- NSGA-II finds the entire trade-off curve in one run
- Result: diverse set of layouts from cheapest (low power) to most powerful (high cost)

---

## NSGA-III (many-objective)

For $M \geq 4$ objectives:
- Dominance loses power — most solutions become non-dominated
- NSGA-III replaces crowding distance with **reference-point-based selection** to maintain diversity along a predefined set of reference directions
- Visualised with parallel coordinate plots

---

## Connections

- [[multi-objective-optimization]] — Pareto dominance, non-dominated sorting, crowding distance
- [[evolutionary-algorithms]] — NSGA-II is an EA; same crossover/mutation operators
- [[mopso]] — analogous adaptation of PSO for multi-objective problems

---

## Exam notes

- NSGA-II = fast non-dominated sort + crowding distance + elitism
- Know the execution flow: $P$ (N) + offspring (N) → combined (2N) → sort → select N
- Crowding distance: perimeter of cuboid formed by neighbours in objective space; $\infty$ for boundary points
- Elitism: using $P \cup Q$ ensures good solutions survive
- No extra parameters needed (unlike niching-based approaches)
- Many-objective (≥4): dominance fails → NSGA-III uses reference points
