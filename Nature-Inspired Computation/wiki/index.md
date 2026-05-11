# NIC Wiki — Master Index

**Module:** ECM3412/ECMM409 – Nature-Inspired Computation, University of Exeter
**Wiki built:** 2026-05-02 | **Last updated:** 2026-05-11 | **Sources ingested:** 19 | **Pages:** 40

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

## Past Exam Papers (5 pages)

- [[exam/ecm3412-19may]] — May 2019 paper: emergence/swarm intelligence, tournament selection pressure, local search vs hill-climbing, perceptron OR gate, overfitting diagram, Conway's Game of Life, F1 GA case study (Wloch & Bentley 2004), exploration–exploitation in GA/PSO/ACO, Pareto dominance, non-dominated sorting (worked 10-solution example), curse of dimensionality, EA optimisation of MLP weights, ACO 4-city TSP calculations (pheromone/heuristic matrices, transition probabilities, pheromone update worked)
- [[exam/ecm3412-21may]] — May 2021 paper: representations/operators, exploration–exploitation, MLP vs SOM, timetabling design, perceptron arithmetic
- [[exam/ecm3412-22may]] — May 2022 paper: EA elements/parameters, direct/indirect encoding, exploration–exploitation, GA vs GP, swarm intelligence, weight initialisation, Game of Life, roulette wheel (worked), crossover (worked), bit-flip mutation, scheduling design, perceptron learning rule (worked), MLP architecture
- [[exam/ecm3412-23may]] — May 2023 paper: exact vs approximate, direct/indirect encoding, SI/PSO, flocking, AIS, hillclimbing, tournament selection, roulette wheel (worked), uniform crossover (worked), Pareto front, SOM unsupervised learning, perceptron (worked)
- [[exam/ecm3412-24may]] — May 2024 paper: NIC advantages, roulette wheel selection, ML applications of optimisation, GA vs GP fitness, PSO pbest/gbest, Pareto dominance, early stopping, SOM weight update, CA transitions, swarm intelligence properties, ACO multi-machine scheduling (construction graph + fitness + worked calculation), PSO velocity/position calculation (worked), NSGA-II sorting + crowding (worked), graceful degradation experiment, Conway's Game of Life (3 timesteps worked)
- [[exam/ecm3412-r-25may]] — R-Paper May 2025: exploration/exploitation + selection methods, GA components, GP vs GA, Boids rules, PSO velocity, NSGA-II (sort + crowding), generalisation/graceful degradation, CA localism/parallelism/homogeneity, ACO pipe-network design (construction graph/objective/heuristic/parameters), PSO parameter experiment, multi-objective feature selection (binary rep), RNN identification, SOM for Iris (2×2 grid)

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
