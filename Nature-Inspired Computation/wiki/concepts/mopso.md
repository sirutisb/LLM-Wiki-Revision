# Multi-Objective Particle Swarm Optimisation (MOPSO)

**Type:** algorithm
**Related:** [[pso]], [[multi-objective-optimization]], [[nsga-ii]]
**Source lectures:** [[lecture15-mopso]]

---

## What it is

**MOPSO** extends the basic PSO algorithm to handle multiple conflicting objectives. The main challenge: in multi-objective settings, there is no single "global best" — the "best" is a set of non-dominated solutions (the Pareto front). MOPSO maintains an **archive** of Pareto-front approximation solutions and uses these as leaders.

---

## Multi-objective pbest

In standard PSO, update pbest only if the new position is better. In multi-objective PSO:

| Case | Action |
|------|--------|
| New position $y_i$ **dominates** pbest $p_i$ | Always update: $p_i \leftarrow y_i$ |
| $p_i$ **dominates** $y_i$ | Never update (keep oldest) |
| **Mutually non-dominating** | Policy choice: keep oldest OR always update with newest |

---

## The Archive

The **archive $A_t$** is a set of non-dominated solutions at time $t$. It represents the current best approximation of the Pareto front.

### Updating the archive (given new solution $y$):
```
For each a_i in archive A_t:
    If y dominates a_i: remove a_i from archive
    If a_i dominates y: mark y as dominated
If y is not marked as dominated: add y to archive
```

### Why a separate archive? (not just the current swarm's Pareto front)

The archive solves a problem specific to how PSO moves, not just "store the Pareto front."

**The swarm ≠ the solution set.** In NSGA-II the population *is* the solution approximation — you keep the best $N$ solutions, so Rank 0 is always a decent sample. In PSO, particles are **explorers**. They fly around the search space; their job is to probe regions, not to be good solutions. At any timestep, most particles are mid-flight somewhere suboptimal.

**Particles forget where they've been.** A particle might pass through a Pareto-optimal region at $t=5$, then accelerate away to explore at $t=10$. If you only look at current swarm positions, you've lost that good point. The archive is the **accumulated memory** of every non-dominated point any particle has ever visited — the same idea as `pbest` (which tracks each particle's personal best over time) but applied globally to the whole non-dominated set.

**The current non-dominated front of the swarm is a weak approximation.** Because particles are spread across the search space for exploration, the non-dominated subset of current positions may be sparse and poorly distributed. The archive builds up density over many iterations.

**The archive also serves as gbest.** In single-objective PSO, gbest is unambiguous — one best position. In multi-objective, you need a *set* of leaders to pull particles toward different parts of the front. The archive is that set. Using only the current swarm's non-dominated front as leaders would give a much noisier, less reliable guide signal.

> **Summary:** The archive is to MOPSO what `pbest` is to each particle — the historical record of the best trade-offs ever found, not just what is visible in the current swarm snapshot.

### Doesn't elitism already solve this? (NSGA-II comparison)

Yes — and that is exactly why NSGA-II does not need a separate archive. Its $P \cup Q$ pool *is* its archive: combining parents and offspring before truncating means no good solution is ever discarded just because a generation ticked over. The elitist truncation step does implicitly what an explicit archive does explicitly.

MOPSO needs an explicit archive because PSO has no equivalent of "keep the parent." Particles do not reproduce and compete for slots — they **move**. There is no natural moment to compare old position vs new position and keep the winner in the population. Once a particle flies away from a good region, that position is gone unless something stores it. The archive is that something.

| | Good solutions preserved by... |
|---|---|
| NSGA-II | elitism ($P \cup Q$ truncation) — implicit archive |
| MOPSO | explicit archive — because movement discards positions |

MOPSO's archive and NSGA-II's elitism are solving the **same problem** (don't lose your best solutions found so far) via different mechanisms, because GA and PSO update solutions in fundamentally different ways.

**Archive size limit:** The archive is often capped at a maximum size because:
- Large archives → expensive leader selection
- Decision-makers don't want thousands of solutions

**Diversity preserving when archive is full:**
- **Clustering (Zitzler 1999):** hierarchical clustering; keep representative (minimum average distance to cluster centre)
- **Crowding distance (Deb et al. 2002):** same as NSGA-II; prefer solutions in sparse areas

---

## Leader selection

In standard PSO, gbest is unambiguous. In MOPSO, the archive contains many non-dominated candidates. How to choose which archive member guides each particle?

### Method 1: Random selection
Simply pick a random archive member as leader. Simple but doesn't guide diversity.

### Method 2: Prefer sparse regions of archive
Prefer archive members that are in areas of the objective space with fewer solutions (similar spirit to crowding distance).

### Method 3: Dominated solution count
- Rank archive members by how many swarm solutions each archive member dominates
- Archive solutions dominating fewer swarm solutions are **more likely** to be selected
- Encourages particles to follow less-exploited archive regions

### Method 4: Hypervolume contribution
**Hypervolume** = area/volume dominated by the Pareto front approximation between the solutions and a reference point.

The leader is the archive member whose **hypervolume contribution is maximum** for the particle's position as reference point. If the particle is not dominated by the archive, choose at random.

---

## Many-objective MOPSO

For $M \geq 4$ objectives, dominance loses effectiveness (most solutions become non-dominated).

### Average rank method
Rank each archived solution $M$ times — once per objective — then take the average:
$$\bar{r}_i = \frac{1}{M} \sum_{m=1}^{M} r_{im}$$
where $r_{im}$ = rank of solution $i$ on objective $m$.
Solutions with lower average rank are more likely to be selected as leaders.

### Distance ranking
$$r(x_i) = \sum_{m=1}^{M} \sum_{j \neq i} d_{ijm}$$
where $d_{ijm} = |f_m(x_i) - f_m(x_j)|$ is the objective-space distance.

Solutions in **uncrowded regions** (high $d_{ij}$ sums) receive better ranks → maintained as diverse leaders.

---

## MOPSO vs NSGA-II

| Feature | MOPSO | NSGA-II |
|---------|-------|---------|
| Base algorithm | PSO | GA |
| Population structure | Swarm + separate archive | Single combined population |
| Diversity mechanism | Archive + leader selection | Crowding distance |
| Pareto front | Stored in archive | Rank 0 of sorted population |
| Memory | pbest per particle | None (no individual history) |
| Continuous | Native | Via encoding |

---

## Connections

- [[pso]] — MOPSO is PSO adapted for multiple objectives
- [[multi-objective-optimization]] — Pareto front, dominance, crowding distance
- [[nsga-ii]] — analogous algorithm from EA side; crowding distance borrowed here

---

## Exam notes

- Archive = Pareto front approximation; only non-dominated solutions stored
- Three archive update operations: remove dominated members, check if new solution is dominated, add if not
- Leader selection methods: random, sparse-region preference, dominated solution count, hypervolume contribution
- Many-objective: dominance fails → use average rank or distance ranking
- Crowding distance from NSGA-II can be used for archive diversity in MOPSO
