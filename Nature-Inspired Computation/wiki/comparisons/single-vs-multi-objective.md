# Single-Objective vs Multi-Objective Optimisation

## Overview

Single-objective optimisation (most standard EAs, PSO, ACO) finds the best single solution. Multi-objective optimisation (MOO) finds a set of trade-off solutions — the Pareto front. Understanding when each applies and how MOO algorithms differ from their single-objective counterparts is essential.

---

## Core difference

| Aspect | Single-objective | Multi-objective |
|--------|-----------------|-----------------|
| **Output** | One best solution | A set of Pareto-optimal solutions |
| **Comparison** | $f(a) > f(b)$ → $a$ better | Pareto dominance: $a \succ b$ only if $a$ ≥ $b$ on all objectives and > on one |
| **"Best" solution** | Uniquely defined | No unique best; trade-offs exist |
| **Goal** | Converge to global optimum | Converge to AND spread across Pareto front |
| **Selection** | Fitness-based tournament/roulette | Dominance + diversity (crowding distance, niching) |
| **Population role** | Explore to find one best | Maintain diverse coverage of Pareto front |
| **Result visualisation** | Single point, scalar | Curve (2 objectives) or surface/hyperplane ($M$ objectives) |

---

## Algorithm modifications for MOO

| Component | Single-objective | Multi-objective |
|-----------|-----------------|-----------------|
| **Fitness comparison** | $f(a) > f(b)$ | Pareto dominance $a \succ b$ |
| **Selection** | Tournament on fitness | Dominance tournament + tiebreak |
| **Tiebreak** | N/A (one fitness) | Crowding distance or niching |
| **Population update** | Best fitness | Non-dominated sort + crowding |
| **Archive** | Not needed (best = current best) | Needed in MOPSO; implicit in NSGA-II |

---

## The Pareto front geometry issue

Different Pareto front shapes affect which algorithms work well:

- **Convex Pareto front:** weighted-sum scalarisation can find all points
- **Non-convex Pareto front:** weighted-sum misses points in concave regions → MOEAs needed
- **Disconnected Pareto front:** population diversity essential; some algorithms lose parts of the front

---

## Many-objective optimisation (≥4 objectives)

Dominance stops working well:
- Most solutions become mutually non-dominated (ranks collapse)
- Selection pressure disappears
- Pareto front has exponentially more points

**Solutions:**
- NSGA-III: reference-point-based diversity
- Average rank, distance ranking (for PSO)
- Decomposition approaches (MOEA/D)
- Visualisation: parallel coordinate plots instead of 2D Pareto curves

---

## Weighted sum approach (and its limitations)

Can solve MOO by running separate optimisations for different weight vectors $w_1 f_1 + w_2 f_2 + \ldots$

**Problems:**
1. Need $k$ separate runs for $k$ Pareto front points
2. Cannot find points on non-convex sections of the Pareto front
3. Hard to choose weights without knowing the front in advance

→ MOEAs (NSGA-II, MOPSO) are preferred because they find the full Pareto front in one run.

---

## Real-world application: offshore wind farms

- **Single-objective:** minimise cost only → cheapest but worst power
- **Single-objective:** maximise power only → best power but most expensive
- **Multi-objective (NSGA-II):** returns the full trade-off curve; decision-maker can pick the preferred trade-off based on budget and power requirements

---

## Related pages
- [[multi-objective-optimization]]
- [[nsga-ii]]
- [[mopso]]
- [[evolutionary-algorithms]]
- [[pso]]
