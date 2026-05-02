# Cellular Automata (CA)

**Type:** model / framework
**Related:** [[swarm-intelligence]], [[flocking-boids]]
**Source lectures:** [[lecture20-alife]]

---

## What it is

A **Cellular Automaton (CA)** is a discrete model of computation where a grid of cells, each in a finite state, evolves over time steps according to a **local rule** based only on the cell's current state and its **neighbourhood**. Complex global behaviour emerges from these simple local interactions.

Devised in the late 1940s by **Stan Ulam** (mathematician) and **John von Neumann**.

Originally intended to model a stylised universe with thermodynamic-like rules. In artificial life, a demonstration of **convergence**: complex global behaviour from local interactions following simple rules.

---

## Basic structure

**Cell:** a unit of the grid, in one of a small finite set of states (typically binary: active/inactive).

**Grid:** typically 1D, 2D, or 3D (but 2D is most common for demonstration purposes).

**State update:** at each time step, every cell simultaneously updates its state according to a **rule** that depends only on the cell's current state and the states of cells in its neighbourhood.

---

## Neighbourhoods (2D)

Two standard neighbourhoods for a 2D grid:

| Neighbourhood | Cells included | Count |
|--------------|---------------|-------|
| **von Neumann** | Cell itself + 4 orthogonal neighbours (N, S, E, W) | 5 cells |
| **Moore** | Cell itself + 8 surrounding cells (includes diagonals) | 9 cells |

The Moore neighbourhood is more commonly used as it captures diagonal interactions.

---

## Rules

A rule specifies: for each possible combination of neighbourhood states, what is the next state of the centre cell?

- For binary states and a von Neumann neighbourhood: $2^5 = 32$ possible neighbourhood configurations → $2^{32}$ possible rules
- Rules are typically described by their number (Wolfram notation for 1D CAs)

---

## Famous example: Conway's Game of Life (1970)

A 2D CA with binary states and Moore neighbourhood:

| Rule | Description |
|------|-------------|
| **Birth** | A dead cell with exactly 3 live neighbours becomes alive |
| **Survival** | A live cell with 2 or 3 live neighbours stays alive |
| **Death** | All other live cells die (underpopulation or overpopulation) |

Results in remarkably complex behaviour: gliders (moving patterns), oscillators, spaceships, and even universal computation.

---

## Artificial Life context

CAs exemplify the **A-life theme**: complex global behaviour from simple local rules. Compare to:
- Flocking ([[flocking-boids]]): 3 simple rules → complex flock behaviour
- Ant colonies ([[ant-colony-optimization]]): simple individual behaviour → collective pathfinding
- Evolution ([[evolutionary-algorithms]]): simple selection + variation → complex adapted solutions

All demonstrate **emergence** — the whole is more than the sum of its parts.

---

## Applications

| Domain | Use |
|--------|-----|
| Physics | Simulating gas dynamics, crystal growth |
| Biology | Modelling tumour growth, ecological systems |
| Computer science | Cryptography, random number generation, parallel computation |
| Traffic simulation | Nagel-Schreckenberg traffic model |
| Urban modelling | Simulating city growth patterns |

---

## Connections

- [[swarm-intelligence]] — CAs and SI both exhibit emergence from local rules
- [[flocking-boids]] — analogous emergence mechanism
- [[neural-networks]] — some CA models are related to Hopfield networks

---

## Exam notes

- CA = grid of cells + finite states + local update rule applied simultaneously to all cells
- Two standard 2D neighbourhoods: **von Neumann** (4 orthogonal) and **Moore** (8 surrounding)
- Key property: **emergent complexity** — simple local rules → complex global behaviour
- Devised by Ulam and von Neumann in the 1940s
- Game of Life: 3 rules (birth, survival, death) → Turing-complete emergent behaviour
- Used in physics, biology, traffic simulation, urban modelling
