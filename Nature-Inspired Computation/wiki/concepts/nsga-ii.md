# NSGA-II (Non-dominated Sorting Genetic Algorithm II)

**Type:** algorithm
**Related:** [[multi-objective-optimization]], [[evolutionary-algorithms]], [[mopso]]
**Source lectures:** [[lecture13-14-emo]]

---

## What it is

**NSGA-II** (Deb, Pratap, Agarwal & Meyarivan, 2002) is the most widely cited multi-objective genetic algorithm. It uses **fast non-dominated sort** for ranking and **crowding distance** for diversity. Cited tens of thousands of times — the off-the-shelf default for [[multi-objective-optimization]].

---

## Motivation / Why it exists

NSGA-II was designed to fix **two specific weaknesses** of earlier MOEAs (especially NSGA-I):

**Problem 1 — Niching needs a parameter you cannot choose well.**
Earlier MOEAs maintained Pareto-front spread using [[multi-objective-optimization|niching]]: divide objective space into regions of radius $r$ (the *niche radius*), then prefer solutions in less-crowded niches. The niche radius is hard to set — it's not just problem-specific, it's often *instance*-specific (e.g. different bin-packing instances may need different radii). You either need expertise to guess it, or an adaptive schedule (e.g. start big, shrink over time). NSGA-II replaces niching with **crowding distance**, which is **parameter-free**.

**Problem 2 — Non-dominated sorting was slow.**
NSGA-I's ranking step was $O(MN^3)$. NSGA-II's **fast non-dominated sort** is $O(MN^2)$ — an order-of-magnitude practical speed-up that makes large populations feasible.

**Bonus — Elitism.**
NSGA-II combines parent and offspring populations ($P \cup Q$, size $2N$) before truncating to size $N$. Excellent parents are never thrown away just because a generation has ticked over.

**Why it took over the field.**
- No extra parameters beyond standard GA settings — engineers and planners with no CS background can run it as a black box and get the trade-off curve in a single run
- Returns the *whole* Pareto front approximation, not one point
- Available in standard libraries (DEAP, pymoo, MATLAB, etc.)
- ~70,000 citations and counting

**What it does *not* do well.** Many-objective problems ($M \geq 4$) — see [NSGA-III](#nsga-iii-many-objective) below.

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

Measures how crowded the neighbourhood of a solution is in **objective space**. Used as a tiebreaker on the rank that doesn't fully fit into the next population — **prefer the less crowded** solution (larger $d$).

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

**Intuition.** $d_i$ is the (normalised) perimeter of the "cuboid" formed by the nearest neighbours of $i$ along each objective axis. Large $d$ = isolated point in a sparse region = good for diversity. Small $d$ = surrounded by similar trade-offs = redundant.

**Boundary solutions** ($d = \infty$). The best solution in each individual objective always sits at the end of the sorted list and gets $d = \infty$, so it is *always* kept. This explicitly guarantees the **extremes of the front are preserved** — without this rule the algorithm could converge to a tight cluster in the middle.

**Distance metric.** This is L1 / Manhattan distance across normalised objective ranges — **not** Hamming distance (which counts differing bits between strings; an unrelated metric).

**When is it actually computed?** Only on the **one rank that gets split** when filling the new population. Earlier ranks are kept whole; later ranks are discarded whole. You don't need to compute crowding distance for every rank, only the borderline one.

### Intuitive walkthrough — worked example

Suppose Rank 0 contains **5 solutions** (minimise both objectives):

| Solution | $f_1$ | $f_2$ |
|----------|-------|-------|
| A | 1 | 10 |
| B | 3 | 7 |
| C | 5 | 5 |
| D | 7 | 3 |
| E | 10 | 1 |

Sketched in objective space they lie on a diagonal front: A is best on $f_2$, E best on $f_1$, and B, C, D are spread in between.

```
f2
10 |  A
 7 |     B
 5 |        C
 3 |           D
 1 |              E
   +--1--3--5--7-10-- f1
```

**Step 1 — Initialise all distances to 0.**

**Step 2 — Process objective $f_1$.**
Sort by $f_1$: A(1) → B(3) → C(5) → D(7) → E(10).
Range = $10 - 1 = 9$.
- A and E are boundary → $d = \infty$ immediately.
- B: neighbours are A and C → gap = $(f_1^C - f_1^A)/9 = (5-1)/9 = 0.44$
- C: neighbours are B and D → gap = $(7-3)/9 = 0.44$
- D: neighbours are C and E → gap = $(10-5)/9 = 0.56$

**Step 3 — Process objective $f_2$.**
Sort by $f_2$: E(1) → D(3) → C(5) → B(7) → A(10).
Range = $10 - 1 = 9$.
- E and A are boundary → already $\infty$.
- B: neighbours are C and A → gap = $(f_2^A - f_2^C)/9 = (10-5)/9 = 0.56$
- C: neighbours are D and B → gap = $(7-3)/9 = 0.44$
- D: neighbours are E and C → gap = $(5-1)/9 = 0.44$

**Step 4 — Sum contributions.**

| Solution | $f_1$ contrib | $f_2$ contrib | **Total $d$** |
|----------|---------------|---------------|---------------|
| A | $\infty$ | $\infty$ | $\infty$ |
| E | $\infty$ | $\infty$ | $\infty$ |
| B | 0.44 | 0.56 | **1.00** |
| D | 0.56 | 0.44 | **1.00** |
| C | 0.44 | 0.44 | **0.89** |

**Reading the result.** C sits in the middle of the front — it has the *smallest* cuboid because its neighbours are close on both sides. B and D are more isolated. A and E are the extreme points and are *always* kept.

If this rank needed to be trimmed — say only 3 slots remain — NSGA-II keeps A, E (boundary, $d = \infty$), then picks whichever of B/D/C have the largest $d$. C is dropped first because it is the most redundant point in the crowd.

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

- **What it's for:** the off-the-shelf multi-objective EA — returns a diverse Pareto front approximation in one run
- **Two problems it solved over NSGA-I:** (1) niching needed a hard-to-set radius parameter → replaced by parameter-free crowding distance; (2) ranking was $O(MN^3)$ → fast non-dominated sort is $O(MN^2)$
- NSGA-II = fast non-dominated sort + crowding distance + elitism
- Know the execution flow: $P$ (N) + offspring (N) → combined (2N) → fast ND sort → take whole ranks → split the last rank by crowding distance → discard remainder
- **Crowding distance** = L1 sum of normalised neighbour gaps across objectives; perimeter of "cuboid" formed by neighbours in objective space; $d = \infty$ for boundary solutions → extremes always kept
- Crowding distance is only computed on the **one splitting rank**, not on every rank
- Elitism: using $P \cup Q$ ensures good parents survive into the next generation
- No extra parameters needed (unlike niching-based MOEAs)
- **Many-objective ($M \geq 4$) failure mode:** most solutions become non-dominated → Rank 0 swells → dominance loses selection pressure → use NSGA-III + reference points instead
