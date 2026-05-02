# Ant Colony Optimisation (ACO)

**Type:** algorithm
**Related:** [[swarm-intelligence]], [[evolutionary-algorithms]], [[pso]]
**Source lectures:** [[lecture07-aco-intro]], [[lecture08-aco-detail]]

---

## What it is

**Ant Colony Optimisation (ACO)** is a population-based metaheuristic for discrete/combinatorial optimisation inspired by how real ants find shortest paths using pheromone trails. Introduced by Marco Dorigo (1996) as the **Basic Ant System (AS)**.

---

## Biological motivation

**Deneubourg double-bridge experiment (1989):**
- A nest and food source connected by two paths of different lengths
- Ants initially choose randomly
- Shorter path accumulates more pheromone faster (ants complete it sooner, deposit pheromone more frequently)
- Positive feedback: more ants follow stronger pheromone trail
- Eventually: nearly all ants use the shortest path

**Mechanism: Sign-based stigmergy** — ants communicate via pheromone deposited on the ground, not directly.

---

## ACO on the TSP

Each **ant** constructs a solution (tour) by traversing a graph:

### Algorithm

```
1. Initialise pheromone levels τ_ij on all edges (random or uniform)
2. Repeat until termination:
   For each ant k = 1..m:
     a. Place ant at a random start node
     b. Repeat until tour complete:
        - Choose next node j from allowed nodes using TRANSITION RULE
        - Move to j; add j to tour memory (cannot revisit)
   c. Update pheromone using UPDATE RULE
```

### Transition Rule

The probability that ant at node $i$ moves to node $j$:
$$P_{ij}^k = \frac{[\tau_{ij}]^\alpha \cdot [\eta_{ij}]^\beta}{\sum_{l \in \text{allowed}} [\tau_{il}]^\alpha \cdot [\eta_{il}]^\beta}$$

where:
- $\tau_{ij}$ = pheromone strength on edge $(i,j)$
- $\eta_{ij}$ = heuristic value (e.g. $1/d_{ij}$ where $d_{ij}$ is distance)
- $\alpha$ = pheromone weight (exploitation)
- $\beta$ = heuristic weight (exploitation of domain knowledge)
- Allowed nodes = those not yet visited (tour memory)

### Update Rule (pheromone evaporation + deposition)

**Evaporation:** all pheromone decays
$$\tau_{ij} \leftarrow (1 - \rho) \cdot \tau_{ij}$$

**Deposition:** ants lay pheromone proportional to solution quality
$$\tau_{ij} \leftarrow \tau_{ij} + \sum_k \Delta\tau_{ij}^k$$

where $\Delta\tau_{ij}^k = Q/L^k$ if ant $k$ used edge $(i,j)$ (otherwise 0), and $L^k$ is the tour length. Better tours → more pheromone deposited.

---

## Key components summary

| Component | Role |
|---------|------|
| **Pheromone $\tau_{ij}$** | Stigmergic memory — encodes collective experience |
| **Heuristic $\eta_{ij}$** | Domain knowledge (e.g. prefer shorter edges) |
| **Evaporation rate $\rho$** | Forgetting — prevents premature convergence |
| **Tour memory** | Ensures each ant constructs a valid solution |

---

## ACO variants

| Variant | Difference | Paper |
|---------|-----------|-------|
| **Basic Ant System (AS)** | All ants update pheromone | Dorigo (1996) |
| **Elitist Rank AS** | Only best $n$ ants update pheromone | Bullnheimer (1999) |
| **Max-Min Ant System (MMAS)** | Only best ant updates; pheromone bounded $[\tau_\min, \tau_\max]$ | Stützle & Hoos (2000) |

MMAS often outperforms basic AS because:
- Bounding prevents pheromone from becoming too extreme
- Only the best ant reinforcing keeps the search focused

---

## Beyond TSP: construction graph framework

ACO works on **any problem expressible as a path through a graph** (the **construction graph**):

| Problem | Nodes | Edges | Heuristic $\eta$ |
|---------|-------|-------|-----------------|
| TSP | Cities | Possible next cities | $1/d_{ij}$ |
| Job scheduling | Jobs | Sequencing options | Urgency (due date proximity) |
| Bin packing | Items | Bin assignment layers | Item-bin fit |
| Feature selection | Features | Include/exclude | Feature relevance score |

---

## Pros & Cons

| Advantage | Disadvantage |
|-----------|-------------|
| Natural for discrete/combinatorial problems | Slow convergence on large instances |
| Competitive with EAs on many benchmarks | Convergence to suboptimal if $\rho$ too low |
| Exploits domain heuristics naturally | Several hyperparameters ($\alpha, \beta, \rho, Q$) to tune |
| Can handle dynamic problems (pheromone adapts) | Less natural for continuous spaces |

---

## ACO vs EA

| Property | ACO | EA |
|----------|-----|-----|
| Solution representation | Path through graph | Encoded chromosome |
| Memory | Pheromone matrix (shared) | Population |
| Communication | Indirect (stigmergy) | None (only through selection) |
| Diversity mechanism | Evaporation + random choices | Mutation, crossover |
| Best for | Discrete sequencing problems | General purpose |

---

## Connections

- [[swarm-intelligence]] — ACO is the canonical stigmergy-based SI algorithm
- [[pso]] — both are population-based; PSO uses direct position/velocity instead of pheromone
- [[evolutionary-algorithms]] — results often competitive

---

## Exam notes

- Transition rule: probability of moving to next node depends on **pheromone** ($\tau^\alpha$) × **heuristic** ($\eta^\beta$)
- Update rule: evaporation (all edges lose pheromone) + deposition (used edges gain, proportional to quality)
- **Evaporation** is the diversity mechanism — prevents pheromone from accumulating irreversibly
- Construction graph: any problem solvable by building a solution node-by-node can use ACO
- Three AS variants: Basic AS, Elitist Rank AS, Max-Min AS — differ in which ants update pheromone
- Double bridge experiment: real biological evidence that pheromone → shortest path finding
