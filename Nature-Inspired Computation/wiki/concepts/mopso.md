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
