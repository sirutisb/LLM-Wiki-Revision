# Lecture 15 — Multi-objective Particle Swarm Optimisation

**File:** `raw/text/15-mopso.txt`
**Lecturer:** Dr David Walker
**Concepts introduced:** [[mopso]]

---

## Summary

Extends PSO to multi-objective optimisation. Covers multi-objective pbest update, the archive (Pareto front approximation), archive diversity methods (clustering, crowding distance), leader selection strategies, and many-objective solutions (average rank, distance ranking).

## Key content

### Basic PSO recap (used as foundation)
Standard PSO equations recalled. Multi-objective challenge: no single global best → need leader selection from a set of non-dominated solutions.

### Multi-objective pbest
- If new position dominates pbest → always update
- If pbest dominates new position → keep oldest (never update)
- If mutually non-dominating → policy choice

### Archive
$A_t$ = set of all non-dominated solutions at time $t$ (Pareto front approximation). All members mutually non-dominated.

Update procedure: for new solution $y$:
1. Remove archive members dominated by $y$
2. If $y$ is dominated by any archive member: discard $y$
3. Otherwise: add $y$ to archive

Archive has a **size limit** (computational and decision-maker concerns). When full: use diversity mechanism.

### Archive diversity methods
- **Hierarchical clustering (Zitzler 1999):** join adjacent clusters until target size; keep solution with minimum average distance to cluster centre
- **Crowding distance (Deb et al. 2002):** score by proximity to neighbours; keep solutions in sparsely-populated areas; boundary solutions get $\infty$

### Leader selection strategies
1. **Random:** select random archive member. Simple; doesn't account for diversity.
2. **Sparse-region preference:** prefer archive members in less-crowded objective space areas.
3. **Dominated solution count:** archive members that dominate fewer swarm solutions are more likely to be selected (encourages less-exploited areas).
4. **Hypervolume contribution:** choose archive member whose contribution to hypervolume (between non-dominated solutions and a reference point) is maximum.

### Many-objective PSO (≥4 objectives)
Same three challenges as many-objective GA (dominance loses power, visualisation, exponential solutions).

**Average rank:**
$$\bar{r}_i = \frac{1}{M} \sum_{m=1}^{M} r_{im}$$
Rank solutions $M$ times (once per objective); average the ranks. Lower average rank = better leader.

**Distance ranking:**
$$r(x_i) = \sum_{m=1}^{M} \sum_{j \neq i} d_{ijm}$$
where $d_{ijm}$ = objective-space distance between solutions $i$ and $j$ on objective $m$. Prefers solutions in uncrowded regions.

## Key takeaways
- Archive = Pareto front approximation; maintained by dominance checks
- Leader selection is the key design challenge for MOPSO
- Hypervolume contribution is theoretically grounded but computationally expensive
- Average rank and distance ranking handle many-objective settings where dominance fails

## Links to concepts
- [[mopso]]: full algorithm treatment
- [[pso]]: the single-objective foundation
- [[multi-objective-optimization]]: Pareto dominance, crowding distance
- [[nsga-ii]]: crowding distance borrowed from here
