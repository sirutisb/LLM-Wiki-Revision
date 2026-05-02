# ACO Jupyter Notebook (Practical Implementation)

**File:** `raw/text/Ant Colony Optimisation - Jupyter Notebook.txt`
**Type:** Practical / code walkthrough
**Concepts demonstrated:** [[ant-colony-optimization]]

---

## Summary

A step-by-step Python implementation of ACO on a 5-city TSP. Shows the initialisation of distance matrix, heuristic matrix, and pheromone matrix, then demonstrates ant solution construction with the transition probability rule.

## Key content

### Problem setup
- 5 cities (nodes 0–4)
- 3 ants
- **Distance matrix** $d$: symmetric; $d_{01} = 10$, $d_{02} = 12$, etc.
- **Heuristic matrix** $H = \eta_{ij} = 1/d_{ij}$ (prefer shorter edges)
- **Pheromone matrix** $T$: initialised to all 1s (uniform)

### Step 1: Initialisation
```python
H = [[round(1/d[i][j], 4) if i != j else 0 for j in range(5)] for i in range(5)]
T = [[1 for j in range(5)] for i in range(5)]
```

### Step 2: Construct ant solutions
For each ant: place on a start node; at each step, choose next node using probabilities proportional to $\tau_{ij}^\alpha \cdot \eta_{ij}^\beta$. Maintain an allowed node set; remove each node after visiting.

### Example output (Iteration 1)
- Heuristic matrix shown (inverse distances)
- Initial pheromone matrix: all 1s
- Ant solution construction traced step-by-step

## Key takeaways
- Implementation confirms the transition rule as described in lectures
- Heuristic ($1/d$) + pheromone (initially uniform) → first iteration is essentially heuristic-guided
- Pheromone accumulates over iterations to encode learned good solutions

## Links to concepts
- [[ant-colony-optimization]]: theoretical treatment
- [[lecture07-aco-intro]]: conceptual introduction
- [[lecture08-aco-detail]]: variants and applications
