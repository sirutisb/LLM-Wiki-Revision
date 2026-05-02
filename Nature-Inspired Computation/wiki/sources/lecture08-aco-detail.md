# Lecture 8 — ACO Detail and Applications

**File:** `raw/text/2024NICLecture8.txt`
**Lecturer:** Dr Alberto Moraglio
**Concepts introduced:** [[ant-colony-optimization]]

---

## Summary

Detailed ACO algorithm with transition rule, update rule, variants (Max-Min, Elitist Rank), and application to non-TSP problems using a construction graph approach. Also covers bin packing as a CA assessment example.

## Key content

### ACO main components
1. **Transition rule** — probability of moving to next node based on pheromone + heuristic
2. **Update rule** — evaporation + deposition

### ACO variants
- **Basic Ant System (Dorigo 1996):** all ants update pheromone
- **Elitist Rank AS (Bullnheimer 1999):** only best $n$ ants update pheromone
- **Max-Min Ant System (Stützle & Hoos 2000):** only best ant updates; pheromone bounded $[\tau_{\min}, \tau_{\max}]$ — often best performing

### Beyond TSP: construction graph framework
Any problem expressible as path through a graph can use ACO:
- **Job scheduling with due dates:** nodes = jobs; path = schedule order; heuristic = urgency (due date proximity). No need to return to start node (open path problem) → "Start node" added to allow pheromone initialisation on first job selections.
- **Bin packing:** layers in construction graph; nodes = bin assignments; ants move forward one layer at a time

### Why a Start node for scheduling?
The Start node ensures that the first link chosen also accumulates pheromone (first job in schedule gets reinforced), allowing the algorithm to learn good first-job choices.

## Key takeaways
- Construction graph = how ACO is generalised beyond TSP
- MMAS often outperforms Basic AS in practice
- Results competitive with evolutionary algorithms on discrete optimisation problems

## Links to concepts
- [[ant-colony-optimization]]: complete algorithm with all variants and construction graph framework
