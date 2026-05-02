# Nature-Inspired Computation — Module Overview

**Course:** ECM3412 (UG) / ECMM409 (PG)
**University:** University of Exeter, Department of Computer Science
**Lecturers:** Dr Alberto Moraglio, Dr David Walker
**Assessment:** CA1 Programming Task & Report (40%), Exam May 2026 (60%) [ECM3412]

---

## What is Nature-Inspired Computation?

NIC draws algorithmic inspiration from three natural systems:

| Natural system | Algorithms derived |
|---|---|
| **Evolution** | Evolutionary Algorithms (GA, ES, GP), Multi-objective EAs |
| **Collective behaviour** | Ant Colony Optimisation, Particle Swarm Optimisation, Flocking |
| **Brains** | Artificial Neural Networks, Spiking Neural Networks, SOMs, Neuromorphic Computing |

The common thread: these are all **approximate optimisation / search algorithms** for problems where exact methods are intractable (typically NP-hard).

---

## The central problem: optimisation

Given a **fitness function** $f(s)$ over a search space $S$, find $s^*$ such that $f(s^*)$ is maximal (or minimal). This is hard when $S$ is huge, $f$ is expensive, or the landscape is rugged/multimodal.

**Why exact algorithms fail:** Exhaustive search is infeasible. Gradient methods get stuck in local optima.

**Why NIC works:** Population-based search explores multiple regions in parallel; stochastic operators escape local optima; collective behaviour provides emergent problem-solving.

---

## Module roadmap

### Part 1: Evolutionary Algorithms (Lectures 2–6)
- [[evolutionary-algorithms]] — core EA loop: selection, variation, replacement
- [[fitness-landscapes]] — why hillclimbing fails; population advantage
- [[selection]] — roulette wheel, rank-based, tournament
- [[crossover-mutation]] — operators for binary, real, permutation, tree encodings
- [[representations]] — encoding choice shapes the landscape
- [[genetic-programming]] — evolving programs as trees

### Part 2: Swarm Intelligence (Lectures 7–8, 11–12)
- [[swarm-intelligence]] — emergence, stigmergy, collective behaviour
- [[ant-colony-optimization]] — pheromone-based discrete optimisation
- [[flocking-boids]] — Reynolds' rules; agents and environments
- [[pso]] — particle swarm optimisation for continuous spaces

### Part 3: Multi-objective Optimisation (Lectures 13–15)
- [[multi-objective-optimization]] — Pareto front, dominance, diversity
- [[nsga-ii]] — fast non-dominated sort + crowding distance
- [[mopso]] — PSO adapted for multiple objectives + archives

### Part 4: Neural Computation (Lectures 16–19)
- [[neural-networks]] — ANNs, backpropagation, EAs for weight optimisation
- [[spiking-neural-networks]] — biologically plausible, energy-efficient SNNs
- [[neuromorphic-computing]] — hardware for brain-inspired computation
- [[self-organising-maps]] — unsupervised dimensionality reduction

### Part 5: Artificial Life (Lecture 20)
- [[cellular-automata]] — local rules producing complex global behaviour

### Critical perspective
- [[metaheuristics-critique]] — Sörensen (2013) "Metaphor Exposed": warning against hollow metaphor-driven methods

---

## Key themes across the module

1. **Exploration vs exploitation** — every algorithm must balance search breadth (not missing good regions) with depth (converging on good solutions found).
2. **Representation matters** — how you encode a solution determines the landscape shape, which operators work, and how hard the problem is to solve.
3. **Emergence** — complex intelligent behaviour arises from simple local rules (flocking, ACO, SOMs).
4. **No free lunch** — no single algorithm dominates all problems. The best algorithm exploits problem structure.
5. **Population advantage** — maintaining a population avoids local optima, enables crossover, and allows parallel exploration.
