# NIC Wiki — Master Index

**Module:** ECM3412/ECMM409 – Nature-Inspired Computation, University of Exeter
**Wiki built:** 2026-05-02 | **Sources ingested:** 19 | **Pages:** 37

---

## Concepts (20 pages)

### Evolutionary Algorithms
- [[concepts/evolutionary-algorithms]] — Generic EA framework: select → vary → replace loop, generational vs steady-state
- [[concepts/genetic-algorithms]] — GAs specifically: binary encoding, Holland's formulation, schema theorem
- [[concepts/genetic-programming]] — Evolving programs as trees; Koza's 5 steps; symbolic regression
- [[concepts/selection]] — Roulette wheel, rank-based, tournament — comparison and tradeoffs
- [[concepts/crossover-mutation]] — Variation operators for all encoding types including permutations
- [[concepts/representations]] — Direct vs indirect; encoding shapes landscape and operator choice
- [[concepts/fitness-landscapes]] — Landscape metaphor, hillclimbing, local search, multimodality

### Swarm Intelligence
- [[concepts/swarm-intelligence]] — Emergence, stigmergy, no central control; biological examples
- [[concepts/ant-colony-optimization]] — ACO algorithm: transition rule, update rule, construction graph, variants
- [[concepts/pso]] — PSO: velocity = inertia + cognitive + social; binary PSO extensions
- [[concepts/flocking-boids]] — Reynolds' 3 rules (separation, alignment, cohesion); agents and MAS

### Multi-objective Optimisation
- [[concepts/multi-objective-optimization]] — Pareto dominance, Pareto front, non-dominated sorting, niching
- [[concepts/nsga-ii]] — Fast non-dominated sort + crowding distance + elitism; NSGA-III preview
- [[concepts/mopso]] — Archive, pbest update, leader selection strategies, many-objective methods

### Neural Computation
- [[concepts/neural-networks]] — ANNs: neurons, MLP, backpropagation, EAs for weight optimisation
- [[concepts/spiking-neural-networks]] — SNNs: spike coding, LIF, STDP, surrogate gradients, EA optimisation
- [[concepts/neuromorphic-computing]] — Brain-inspired hardware: event-driven, collocated memory+processing
- [[concepts/self-organising-maps]] — Unsupervised topology-preserving maps; competition + cooperation

### Artificial Life
- [[concepts/cellular-automata]] — Grid cells, local rules, von Neumann/Moore neighbourhoods, emergence

### Critical Perspective
- [[concepts/metaheuristics-critique]] — Sörensen (2013): metaphors ≠ algorithms; No Free Lunch; scientific rigour

---

## Sources (19 pages)

### Introductory
- [[sources/lecture01-intro]] — Module introduction; NIC = Evolution + Brains + Collective Behaviour
- [[sources/lecture02-ea-motivation]] — EA motivation; optimisation complexity; generic EA loop

### Evolutionary Algorithms
- [[sources/lecture03-landscapes]] — Fitness landscapes; hillclimbing; population-based search motivation
- [[sources/lecture04-ea-detail]] — EA variants; all selection methods; crossover/mutation operators; full pseudocode
- [[sources/lecture05-encodings]] — Permutation crossover problems; direct vs indirect; antenna design application
- [[sources/lecture06-gp]] — Genetic Programming; 5 preparatory steps; symbolic regression worked example

### Swarm Intelligence
- [[sources/lecture07-aco-intro]] — SI introduction; double bridge experiment; stigmergy; 4-city TSP walkthrough
- [[sources/lecture08-aco-detail]] — ACO transition/update rules; variants (AS/MMAS/Elitist); construction graph
- [[sources/aco-notebook]] — Python ACO implementation on 5-city TSP; heuristic/pheromone matrices
- [[sources/lecture11-flocking]] — Reynolds' Boids; agents & environments; MAS introduction
- [[sources/lecture12-pso]] — Full PSO with equations; parameters; Binary PSO approaches

### Multi-objective
- [[sources/lecture13-14-emo]] — MOO; dominance; non-dominated sorting; NSGA-II; wind farm example
- [[sources/lecture15-mopso]] — MOPSO; archive management; leader selection; many-objective average rank

### Neural Computation
- [[sources/lecture16-ann]] — ANNs; backpropagation equations; EA weight optimisation; rainfall case study
- [[sources/lecture17-snn]] — SNNs; LIF dynamics; STDP; surrogate gradients; bi-level EA optimisation
- [[sources/lecture18-neuromorphic]] — Neuromorphic hardware; von Neumann bottleneck; Loihi chip
- [[sources/lecture19-som]] — SOMs; unsupervised topology-preserving maps; vs MLP

### Artificial Life & Critical Perspective
- [[sources/lecture20-alife]] — Cellular automata; von Neumann/Moore neighbourhoods; A-life emergence
- [[sources/metaphor-exposed]] — Sörensen 2013 critique; No Free Lunch; genuine innovation criteria

---

## Comparisons (3 pages)

- [[comparisons/ea-vs-swarm]] — EA vs SI: communication, memory, problem fit, algorithmic structure
- [[comparisons/aco-vs-pso]] — ACO vs PSO: discrete vs continuous; indirect vs direct communication
- [[comparisons/single-vs-multi-objective]] — Single vs multi-objective: Pareto front, dominance, many-objective challenges

---

## Quick reference: key equations

| Equation | Page |
|---------|------|
| Roulette wheel: $P(i) = f_i / \sum f_k$ | [[concepts/selection]] |
| PSO velocity: $v_{ij}(t+1) = v_{ij}(t) + c_1 z_1(p_{ij}-x_{ij}) + c_2 z_2(g_j-x_{ij})$ | [[concepts/pso]] |
| ACO transition: $P_{ij} \propto \tau_{ij}^\alpha \eta_{ij}^\beta$ | [[concepts/ant-colony-optimization]] |
| ACO evaporation: $\tau_{ij} \leftarrow (1-\rho)\tau_{ij} + \sum_k \Delta\tau_{ij}^k$ | [[concepts/ant-colony-optimization]] |
| Crowding distance: $d_i += (Y_{i+1}^m - Y_{i-1}^m)/(f_m^{\max} - f_m^{\min})$ | [[concepts/nsga-ii]] |
| Backprop: $w_{ij}^{(t+1)} = w_{ij}^{(t)} + \eta \delta_{pj} o_{pj}$ | [[concepts/neural-networks]] |
| Average rank (MOPSO): $\bar{r}_i = \frac{1}{M}\sum_m r_{im}$ | [[concepts/mopso]] |
