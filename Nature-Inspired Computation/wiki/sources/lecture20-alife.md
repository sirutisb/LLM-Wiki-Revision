# Lecture 20 — Artificial Life and Cellular Automata

**File:** `raw/text/ECM3412___ECMM409_25_26 (10).txt`
**Lecturer:** Dr David Walker
**Concepts introduced:** [[cellular-automata]]

---

## Summary

Introduces cellular automata (CA) as an A-life framework demonstrating emergence of complex global behaviour from simple local rules. Covers the history, basic structure, neighbourhoods (von Neumann, Moore), rules, and applications.

## Key content

### Historical context
Devised in the late 1940s by **Stan Ulam** (mathematician) and **John von Neumann**. Intended to model a stylised universe following physical rules (thermodynamics). In A-life: demonstrates **convergence** — complex global behaviour from local interactions following simple rules.

### CA structure
- **Grid** of cells
- Each cell: one of a finite (normally binary) set of states (active/inactive)
- **Simultaneous update:** all cells update state at each time step
- **Local rule:** new state depends only on current cell state + neighbourhood states

### Neighbourhoods (2D)
- **von Neumann:** cell + 4 orthogonal neighbours (5 cells total)
- **Moore:** cell + 8 surrounding cells including diagonals (9 cells total)

### A-life context
CAs join a family of emergence demonstrations:
- **Boids** (3 rules → flocking)
- **Ant colonies** (simple individuals → collective pathfinding)
- **Evolution** (selection + variation → complex adapted solutions)
All: whole > sum of parts.

### Applications
Chemistry, physics, biology simulation; traffic models; urban growth; cryptography.

## Key takeaways
- CA = grid cells + finite states + simultaneous local update rule
- Two standard 2D neighbourhoods: von Neumann (4 orthogonal) and Moore (8 surrounding)
- Emergence is the A-life theme: complexity from simplicity

## Links to concepts
- [[cellular-automata]]: full treatment
- [[swarm-intelligence]]: analogous emergence principle
- [[flocking-boids]]: the Boids system = another emergence example
