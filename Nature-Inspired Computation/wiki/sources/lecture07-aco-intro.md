# Lecture 7 — Swarm Intelligence I: Ant Colony Optimisation

**File:** `raw/text/2024NICLecture7.txt`
**Lecturer:** Dr Alberto Moraglio
**Concepts introduced:** [[swarm-intelligence]], [[ant-colony-optimization]]

---

## Summary

Introduces Swarm Intelligence as a framework, then motivates ACO through the biology of real ant colonies. Walks through a 4-city TSP example showing how pheromone-based path selection works.

## Key content

### Swarm Intelligence definition
Groups exhibit properties no individual could: emergent behaviour from local interactions following simple rules. No central controller; every element is equal. E.g. ants finding food, termites building mounds.

### Emergent behaviours in Lasius Niger ants (Franks 1989)
- Regulate nest temperature within 1°C range
- Form living bridges
- Find shortest route from nest to food
- Preferentially exploit richest food source

### Double bridge experiment (Deneubourg et al., 1989)
**Experiment 1 (two equal-length paths):** Ants initially choose randomly; over time one path dominates (random positive feedback).

**Experiment 2 (two unequal-length paths):** Over time the **shorter path** is selected by most ants. Why? Ants on the shorter path return faster → deposit pheromone more frequently on it → positive feedback selects the shorter path.

### Stigmergy
Indirect communication via interaction with the environment. Sign-based stigmergy: ants lay pheromone trails; other ants follow stronger trails.

### ACO on 4-city TSP (conceptual walkthrough)
Initial pheromone levels (random). Ant placed at random node. Chooses next node based on probabilities from pheromone strength + distance heuristic. Avoids already-visited nodes (tour memory). After completing tour: evaporate pheromone on all edges; add pheromone to the traversed edges.

## Key takeaways
- Stigmergy = indirect communication via environment modification
- Positive feedback (trail following) + negative feedback (evaporation) → emergent path optimisation
- Real ants demonstrate the algorithm — the double-bridge experiment is the biological proof

## Links to concepts
- [[swarm-intelligence]]: full SI framework
- [[ant-colony-optimization]]: transition rule, update rule, full algorithm
