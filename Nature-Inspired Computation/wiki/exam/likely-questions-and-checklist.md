# NIC — Likely Questions & Exam Prep Checklist

**Module:** ECM3412 / ECMM409 — Nature-Inspired Computation
**Based on:** 7 past papers (May 2019, 2020, 2021, 2022, 2023, 2024, R-25) and the 2024–25 lecture set
**Last updated:** 2026-05-11

---

## 1. The shape of every paper (2019–2025)

Every paper has the same skeleton — **3 questions, 100 marks, all compulsory**:

| Q | Marks | Pattern |
|---|------|---------|
| **Q1** | **40** | "Broad concepts" — 6–9 short sub-parts of 2–10 marks each, spanning the whole syllabus. Touches *most* topics. |
| **Q2** | **30** | Deep dive into ONE topic — usually **ACO** (with a worked numerical calculation OR construction graph design) OR a **GA-numeric** question OR an **open-ended design** problem. |
| **Q3** | **30** | Another deep dive — usually mixes **neural networks** (perceptron / MLP / SOM) with **PSO** or **multi-objective optimisation**, often with a worked numerical calculation. |

**Time budget:** 2 hours typical → 1.2 min/mark. Q1 ~48 min, Q2 ~36 min, Q3 ~36 min.

---

## 2. Topic frequency matrix (across 7 papers)

✓ = appeared, ✓✓ = worked numerical calculation

| Topic | '19 | '20 | '21 | '22 | '23 | '24 | R-25 | n |
|-------|----|----|----|----|----|----|------|---|
| **Selection methods (any)** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **7** |
| Roulette wheel | | | | ✓✓ | ✓✓ | ✓ | ✓ | 4 |
| Tournament selection / pressure | ✓ | | ✓ | | ✓ | | ✓ | 4 |
| **Exploration vs Exploitation** | ✓ | | ✓ | ✓ | | ✓ | ✓ | **5** |
| **PSO theory + velocity equation** | ✓ | ✓ | ✓ | | ✓ | ✓ | ✓ | **6** |
| PSO numerical calc | | | | | | ✓✓ | | 1 |
| PSO parameters ($c_1, c_2, w$) | ✓ | | ✓ | | | ✓ | ✓ | 4 |
| **GA full loop / EA elements** | ✓ | ✓ | ✓ | ✓ | | | ✓ | **5** |
| Crossover (often worked) | | | ✓ | ✓✓ | ✓✓ | | ✓ | 4 |
| Mutation operators | | | ✓ | ✓ | | ✓ | ✓ | 4 |
| GA vs GP | | ✓ | | ✓ | | ✓ | ✓ | 4 |
| Genetic Programming | | ✓ | | ✓ | | ✓ | ✓ | 4 |
| Direct vs Indirect encoding | | ✓ | ✓ | ✓ | ✓ | | | 4 |
| Representations (TSP/knapsack) | | | ✓ | | | | | 1 |
| Fitness landscape / Hillclimbing | ✓ | ✓ | | | ✓ | | | 3 |
| **ACO theory** | ✓ | ✓ | | | ✓ | ✓ | ✓ | **5** |
| ACO worked numerical calc | ✓✓ | | | | | ✓✓ | ✓ | 3 |
| Construction graph design | | ✓ | | | | ✓ | ✓ | 3 |
| ACO experimental design | | ✓ | | | | | | 1 |
| AntNet (Di Caro & Dorigo) | | ✓ | | | | | | 1 |
| Flocking / Boids rules | | ✓ | | | ✓ | | ✓ | 3 |
| Swarm intelligence properties | ✓ | | | ✓ | ✓ | ✓ | | 4 |
| **Pareto dominance / front** | ✓ | ✓ | | | ✓ | ✓ | ✓ | **5** |
| NSGA-II (sort + crowding) | | | | | | ✓✓ | ✓✓ | 2 |
| MOPSO | | | | | | | | 0 |
| Many-objective / curse of dim | ✓ | | | | | | | 1 |
| **Perceptron (theory + worked)** | ✓ | | ✓✓ | ✓✓ | ✓✓ | | | 4 |
| MLP / hidden layers / backprop | ✓ | ✓ | ✓ | ✓ | | | | 4 |
| SOM | | | ✓ | | ✓ | ✓ | ✓ | 4 |
| RNN | | ✓ | | | | | ✓ | 2 |
| Overfitting / early stopping | ✓ | | | | | ✓ | ✓ | 3 |
| Weight initialisation | | | | ✓ | | | | 1 |
| **Game of Life / Cellular Automata** | ✓ | ✓ | | ✓ | | ✓ | ✓ | **5** |
| Fractals (Koch / Menger) | | ✓ | | | | | | 1 |
| AIS (Artificial Immune Systems) | | | | | ✓ | | | 1 |
| **Open-ended DESIGN problem** | | | ✓ | ✓ | ✓ | ✓ | ✓ | **5** |
| Graceful degradation | | | | | | ✓ | ✓ | 2 |

---

## 3. Tier 1 — Almost certain to appear (must master)

These are in **5 or more** of the last 7 papers.

### ☐ 3.1 Selection methods
**Why:** *every* paper tests this. **What to memorise:**
- **Roulette wheel:** $P(i) = f_i / \sum_k f_k$. Be ready to compute probabilities from a fitness table and pick parents using a given list of random numbers.
- **Tournament selection:** pick $t$ candidates uniformly, keep the best. Increasing $t$ → higher **selection pressure**, less diversity. $t = N$ is deterministic (always pick the global best).
- **Rank-based:** assign rank, then probability ∝ rank. Robust to fitness outliers.
- **Elitism:** carry the best $k$ unchanged.
- **Why roulette can fail:** super-fit individuals dominate early; can't handle negative fitness.

**Drill:** Given fitnesses `[2, 3, 1, 4]`, compute roulette probabilities and pick 2 parents using random numbers `[0.86, 0.23]`. See `ecm3412-22may.md` and `ecm3412-23may.md` for worked examples.

### ☐ 3.2 PSO — velocity equation, parameters, behaviour
**Equation (memorise exactly):**
$$v_{ij}(t+1) = w \cdot v_{ij}(t) + c_1 z_1 (p_{ij} - x_{ij}(t)) + c_2 z_2 (g_j - x_{ij}(t))$$
$$x_{ij}(t+1) = x_{ij}(t) + v_{ij}(t+1)$$

Three terms = **inertia** + **cognitive (pbest)** + **social (gbest)**. $z_1, z_2 \sim U(0,1)$.

**Parameter effects:**
- High $c_1$ → exploration (personal experience)
- High $c_2$ → exploitation/convergence (swarm-following)
- High $w$ → exploration; low $w$ → exploitation
- Typical: $c_1 = c_2 = 2$, $w \in [0.4, 0.9]$

**Drill:** Given particle position, velocity, pbest, gbest, $c_1$, $c_2$, random numbers — compute new velocity and position. See `ecm3412-24may.md` Q3(a).

### ☐ 3.3 EA / GA full loop
Be able to write out the **5-step cycle**:
1. Initialise population
2. Evaluate fitness
3. **Select** parents
4. **Vary** (crossover + mutation)
5. **Replace** (generational or steady-state) → loop until termination

**Parameters to name:** population size $N$, crossover rate $p_c$, mutation rate $p_m$, tournament size $t$, max generations. Know effect of each on exploration vs exploitation.

### ☐ 3.4 ACO — transition rule, update rule, construction graph
**Transition probability** (ant $k$ at node $i$ chooses $j$):
$$P_{ij}^k = \frac{\tau_{ij}^\alpha \cdot \eta_{ij}^\beta}{\sum_{l \in N_i^k} \tau_{il}^\alpha \cdot \eta_{il}^\beta}$$

**Pheromone update:**
$$\tau_{ij} \leftarrow (1-\rho)\tau_{ij} + \sum_k \Delta\tau_{ij}^k, \quad \Delta\tau_{ij}^k = Q / L_k \text{ if ant } k \text{ used edge } (i,j)$$

**Construction graph:** nodes = variables/cities, edges = choices. For 5 variables with 3 choices each → 5 layers of 3 nodes (plus a start node).

**Heuristic** $\eta$ is problem-specific: $1/d_{ij}$ for TSP, $1/\text{cost}$ for scheduling, etc.

**Drill:** Given a pheromone matrix and distance matrix, compute transition probabilities from a node, then update pheromones after ants complete tours. See `ecm3412-19may.md` Q4(b) and `ecm3412-24may.md` Q2(b).

### ☐ 3.5 Pareto dominance & non-dominated sorting
- **Dominance:** $a$ dominates $b$ iff $a$ is no worse on all objectives and strictly better on at least one.
- **Pareto front:** the set of non-dominated solutions.
- **Non-dominated sorting:** Rank 0 = solutions dominated by nobody; remove them, Rank 1 = dominated only by Rank 0; etc.
- **Crowding distance** (NSGA-II): for each objective, sort by it; assign $\infty$ to boundary points; for the rest, $d_i += (f_m^{i+1} - f_m^{i-1}) / (f_m^{\max} - f_m^{\min})$. Pick the *higher* crowding distance to preserve diversity.

**Drill:** Given 6–10 solutions in 2D objective space, do non-dominated sort then break ties on the last front using crowding distance. See `ecm3412-24may.md` Q3(b) — 10-solution worked example.

### ☐ 3.6 Conway's Game of Life / Cellular Automata
**Rules (B3/S23):**
- A live cell with **2 or 3** live neighbours **survives**.
- A live cell with **< 2** (underpopulation) or **> 3** (overpopulation) **dies**.
- A dead cell with **exactly 3** live neighbours **becomes alive** (birth).

Neighbours counted in **Moore neighbourhood** (8 cells).

**Properties of CA:** localism, parallelism, homogeneity (same rule everywhere). **Emergence:** complex global patterns (gliders, oscillators, Turing-completeness) from simple local rules.

**Drill:** Given a starting configuration, step it forward 2–3 generations.

### ☐ 3.7 Open-ended design problem
**Pattern:** "Design a NIC system to solve [timetabling / scheduling / pipe routing / feature selection]."

**5-step answer template** (use this exact structure):
1. **Hard vs soft constraints.** Hard = must satisfy (no clashes); soft = preferred (gaps between classes). Hard violations → infeasible. Soft → penalty.
2. **Objective function.** $f = \sum w_i \cdot \text{violations}_i$ — weighted sum of penalties, with hard violations weighted ≫ soft.
3. **Algorithm + representation choice.** State which algorithm (GA / ACO / PSO) with reason; pick direct or indirect encoding and justify.
4. **Operators + parameters.** Say which crossover, mutation, selection; give typical values; describe parameter-tuning experiment.
5. **Success criteria.** Average fitness over N runs, statistical test (Mann-Whitney U or Wilcoxon), variance, time-to-solution, comparison vs baseline.

Practised papers: 2021 (timetabling), 2022 (scheduling), 2024 (job-shop), R-25 (pipe network + feature selection).

### ☐ 3.8 Exploration vs Exploitation
- **Exploration** = sampling new regions; avoids local optima but wastes evaluations.
- **Exploitation** = refining current best; converges fast but can get stuck.
- The **fundamental trade-off** in all NIC algorithms.

| Lever | Exploration ↑ if... | Exploitation ↑ if... |
|-------|---------------------|----------------------|
| GA mutation rate $p_m$ | high | low |
| GA crossover rate $p_c$ | high | low |
| Tournament size $t$ | small | large |
| Population size $N$ | large | small |
| PSO $c_1$ | large | — |
| PSO $c_2$ | — | large |
| PSO inertia $w$ | large | small |
| ACO $\alpha$ (pheromone weight) | small | large |
| ACO $\beta$ (heuristic weight) | large | small |
| ACO $\rho$ (evaporation) | large | small |

---

## 4. Tier 2 — Highly likely (in 3–4 papers)

### ☐ 4.1 Crossover operators
- **Single-point**: cut both parents at the same point, swap tails.
- **Two-point**: cut twice, swap middle segments.
- **Uniform**: per-bit coin flip; uses a *mask*. Given mask `101010` and parents `001011`/`101001` → Child1 = `001001`, Child2 = `101011` (where mask=1, take from P1; mask=0, take from P2 — or vice versa, state your convention).
- **PMX / Order crossover / Cycle crossover**: for permutations (TSP) — ordinary crossover would produce invalid tours.

### ☐ 4.2 Mutation operators
- **Bit-flip** (binary): flip each bit with probability $p_m$.
- **Gaussian** (real-valued): $x' = x + \mathcal{N}(0, \sigma^2)$.
- **Swap / Insert / Inverse** (permutations).

Typical $p_m \approx 1/L$ where $L$ = chromosome length.

### ☐ 4.3 GA vs GP

| Dimension | GA | GP |
|-----------|-----|-----|
| Chromosome | fixed-length string (binary/real/int) | tree / variable-length program |
| Encoding | direct parameter representation | functions + terminals |
| Crossover | bit / segment exchange | subtree swap |
| Mutation | bit-flip / Gaussian | subtree replace / node mutate |
| Fitness eval | direct formula | run the evolved program |
| Output | a parameter vector | a program / expression |
| Example | tuning a neural network | symbolic regression |

GP has **5 preparatory steps** (Koza): function set, terminal set, fitness measure, run parameters, termination & result.

### ☐ 4.4 Direct vs Indirect encoding

| | Direct | Indirect |
|-|--------|----------|
| Genotype | identical to/maps trivially to phenotype | needs a decoder / generator |
| Example | (x, y) coordinates | a rule that builds the structure |
| Search space | usually larger | usually smaller, can be biased |
| Operators | simple | must preserve validity |
| Use when | structure is fixed | structure is large/repetitive |

### ☐ 4.5 Perceptron (decision boundary + learning)
- **Equation:** $y = \text{step}\!\left( \sum_i w_i x_i + b \right)$
- **Decision boundary** is the line $\sum w_i x_i + b = 0$.
- For a line $x_2 = x_1 + 1$: rewrite as $-x_1 + x_2 - 1 = 0$, giving $w_1 = -1, w_2 = 1, b = -1$.
- **Learning rule:** $\Delta w_i = \eta (t - y) x_i$, $\Delta b = \eta (t - y)$.

**Drill:** Given 3–4 training patterns and starting weights, apply the learning rule pattern-by-pattern until convergence. Sketch the final decision boundary. See 2019, 2021, 2022, 2023 papers.

### ☐ 4.6 MLP & Backpropagation
- **MLP:** input → hidden layer(s) → output. Needed when classes are **not linearly separable** (XOR is the canonical example).
- **Activation:** sigmoid, tanh, ReLU. Must be **differentiable** for backprop (step function won't work).
- **Backprop update:** $w_{ij}^{(t+1)} = w_{ij}^{(t)} + \eta \delta_{pj} o_{pj}$ where $\delta$ is the error signal propagated backwards.
- For output: $\delta_j = (t_j - o_j) \cdot \sigma'(\text{net}_j)$.
- For hidden: $\delta_j = \sigma'(\text{net}_j) \sum_k \delta_k w_{jk}$.

### ☐ 4.7 SOM (Self-Organising Map)
- **Unsupervised** topology-preserving 2D grid of neurons.
- **Algorithm:**
  1. Find Best Matching Unit (BMU): neuron with weights closest to input (Euclidean).
  2. Update BMU **and neighbourhood** weights: $w_i(t+1) = w_i(t) + \eta(t) h_{ci}(t) (x - w_i(t))$.
  3. Shrink learning rate $\eta(t)$ and neighbourhood radius over time.
- **vs MLP:** SOM has no labels, no error to backprop, no hidden layer; just a competitive map.
- **Use cases:** clustering, dimensionality reduction, visualisation (e.g. Iris dataset on 2×2 or 10×10 grid).

### ☐ 4.8 Swarm Intelligence properties
- **Emergence:** complex group behaviour from simple local rules.
- **Stigmergy:** indirect communication via environment (pheromones).
- **Decentralisation:** no leader; no global plan.
- **Robustness:** loss of one agent doesn't break the system.
- **Examples:** ant trails (ACO), bird flocks (PSO, Boids), bee waggle dance.

### ☐ 4.9 Boids / Reynolds' three rules
1. **Separation:** steer to avoid crowding.
2. **Alignment:** steer toward the average heading of neighbours.
3. **Cohesion:** steer toward the average position of neighbours.

This is the canonical example of **agent-based / multi-agent systems** with local rules producing emergent global flocking.

---

## 5. Tier 3 — Possible (in 1–2 papers, but still in lectures)

### ☐ 5.1 Fitness landscape & hillclimbing
- **Landscape** = solution space × fitness; rugged landscapes = many local optima.
- **Hillclimbing:** local search; accepts only improving moves → trapped in local optima.
- **Escape mechanisms:** Monte Carlo (random restart), Simulated Annealing (accept worse with probability), Tabu Search (forbid recent moves).
- Population-based search (GA) explores multiple basins simultaneously.

### ☐ 5.2 Overfitting & early stopping
- Training error ↓ monotonically; validation error is U-shaped.
- **Early stopping:** stop training at validation-error minimum.
- **Other regularisers:** L1/L2 penalty, dropout, more data, smaller network.

### ☐ 5.3 RNN
- Has **feedback loops** — output (or hidden state) at $t$ feeds into network at $t+1$.
- Used for **sequence data**: time series, language.
- Trained with **backprop through time (BPTT)**.
- Vanishing/exploding gradients → motivated LSTM/GRU.

### ☐ 5.4 Graceful degradation
- An ANN losing a few neurons or weights still works (with degraded accuracy) — unlike a symbolic program.
- Tied to **distributed representations** and the brain analogy.
- **Test:** kill $k$% of neurons; plot accuracy vs $k$.

### ☐ 5.5 AIS (Artificial Immune Systems)
**Four key properties** the immune system inspires:
1. **Self / non-self discrimination** (unique recognition).
2. **Diversity** of receptors via random generation.
3. **Adaptability** via clonal selection (proliferate good detectors).
4. **Immunological memory** (remember past pathogens).

### ☐ 5.6 Fractals
- **Self-similar** at multiple scales; **non-integer dimension**.
- **Koch curve:** start with segment, replace middle third with triangular bump; length after $n$ iterations = $(4/3)^n \to \infty$.
- **Hausdorff dimension** for Koch = $\log 4 / \log 3 \approx 1.262$. For Menger sponge = $\log 20 / \log 3 \approx 2.727$.

### ☐ 5.7 AntNet (network routing)
- ACO for telecom routing (Di Caro & Dorigo 1998).
- **Forward ants** explore the network and record path & timings.
- **Backward ants** retrace the path, updating routing-table "pheromones".
- Outperforms Bellman-Ford and Q-routing under **dynamic** traffic.

---

## 6. Tier 4 — Newer syllabus topics (in current lectures, NOT in past papers)

These could appear for the first time in 2026. Don't skip them.

### ☐ 6.1 SNN (Spiking Neural Networks) — Lecture 17
- Third-generation NNs; communicate via **discrete spikes** in time.
- **LIF model:** $\tau \frac{dV}{dt} = -(V - V_{\text{rest}}) + RI(t)$; fire when $V > V_{\text{threshold}}$, then reset.
- **STDP** (Spike-Timing Dependent Plasticity): if pre-spike *before* post-spike → strengthen; *after* → weaken.
- **Training challenge:** spike function is non-differentiable → use **surrogate gradients** or **EAs to evolve weights**.
- **Bi-level EA optimisation:** outer EA tunes architecture/hyperparams; inner EA tunes weights.

### ☐ 6.2 Neuromorphic computing — Lecture 18
- Brain-inspired hardware (Intel Loihi, IBM TrueNorth, SpiNNaker).
- Avoids the **von Neumann bottleneck** (separated memory & CPU): collocated memory and processing.
- **Event-driven** (asynchronous), massively parallel, ultra-low-power.

### ☐ 6.3 MOPSO — Lecture 15
- Multi-objective PSO. Maintains an **archive** of non-dominated solutions.
- **Leader selection** strategies: random from archive, crowding-distance-weighted, sigma method.
- For **many-objective** (M ≥ 4): use **average rank** $\bar{r}_i = \frac{1}{M} \sum_m r_{im}$ since Pareto dominance becomes too weak.

### ☐ 6.4 Sörensen's metaphor critique (2013)
- Many "novel" NIC algorithms (firefly, krill herd, grey wolf, etc.) **rebrand existing metaheuristics** behind biological metaphors.
- A *genuinely* novel algorithm must add a **new search mechanism** — not just a new story.
- Backed by the **No Free Lunch theorem**: averaged over all problems, no algorithm beats random search.
- **Implication:** justify algorithm choice on *mechanism*, not biology.

---

## 7. Worked-calculation drills (DO THESE)

Numerical questions appear in Q2/Q3 nearly every year. Practise these to fluency:

| Drill | Pattern | Practice from |
|-------|---------|---------------|
| **Roulette wheel** | Compute $P_i$ from fitness list; pick parents from given random numbers | 22, 23 |
| **Crossover** | Apply single-point or uniform crossover with given mask | 22 (single-point), 23 (uniform) |
| **Tournament-pressure analysis** | Compare $t/N$ for given values; rank pressure | 21, 23 |
| **Perceptron learning** | Trace weight updates over 3–4 training patterns; sketch boundary | 19, 21, 22, 23 |
| **Perceptron design (manual)** | Given a target boundary line, write down $w$ and $b$; verify all patterns | 21, 23 |
| **PSO velocity & position update** | One step of $v$ and $x$ update from given $c_1, c_2, z_1, z_2$ | 24 |
| **ACO transition probabilities** | $P_{ij} = \tau^\alpha \eta^\beta / \sum$ for a given pheromone & distance matrix | 19, 24, R-25 |
| **ACO pheromone update** | $(1-\rho)\tau + \sum Q/L$ after ants complete tours | 19 |
| **NSGA-II non-dominated sort** | Multi-front sort of 6–10 solutions in 2D | 24, R-25 |
| **NSGA-II crowding distance** | Pick last-front survivors using crowding | 24, R-25 |
| **Conway's GoL** | Step a small grid forward 2–3 generations | 22, 24 |
| **ACO scheduling fitness** | Compute total tardiness from a job schedule | 24 |

---

## 8. Open-ended design problem template

For any "Design a NIC algorithm to solve [problem]" question (Q2 or Q3, typically 25–30 marks):

### Skeleton answer

**1. Problem analysis (3–5 marks)**
- Identify decision variables (what is being assigned/ordered/chosen).
- List **hard constraints** (must hold) and **soft constraints** (preferred).
- State the search space size if possible (e.g. $n!$ for TSP, $2^n$ for subset selection).

**2. Encoding / representation (5–6 marks)**
- Choose direct vs indirect, and justify.
- State chromosome structure (e.g. "permutation of $n$ jobs", "binary vector of length $f$").
- Show how it maps to a candidate solution.

**3. Algorithm choice (3–5 marks)**
- GA for combinatorial with constraints; ACO for graph/route problems with natural construction; PSO for continuous; NSGA-II if multi-objective.
- Justify the choice — don't just name an algorithm.

**4. Operators (5–6 marks)**
- Selection (tournament size $t = 3$ default).
- Crossover (specify operator and rate $p_c \approx 0.7$).
- Mutation (specify and rate $p_m \approx 1/L$).
- For ACO: pheromone init, $\alpha, \beta, \rho$ values.

**5. Fitness function (5 marks)**
- Weighted sum: $f = w_{\text{hard}} \cdot H + w_{\text{soft}} \cdot S$, with $w_{\text{hard}} \gg w_{\text{soft}}$.
- Or hierarchical: feasibility first, quality second.
- For multi-objective: list all $M$ objectives explicitly.

**6. Experimental design (3–5 marks)**
- 30+ independent runs per configuration.
- Parameter sweep across at least one key parameter.
- Compare against baseline (random search, hand-crafted heuristic).
- Statistical test (Mann-Whitney U) on best-of-run fitness.

**7. Success criteria (2–4 marks)**
- Beats baseline by significant margin.
- Convergence within budget.
- Feasibility rate.

---

## 9. Master must-know checklist

Tick off when you can do each without notes.

### Foundations
- ☐ Define optimisation: variables, objective, constraints, search space.
- ☐ Explain exact vs approximate algorithms; when each is appropriate.
- ☐ Define fitness landscape; explain rugged vs smooth.
- ☐ Explain why hillclimbing fails on multimodal landscapes.
- ☐ Define exploration vs exploitation; name 3 mechanisms favouring each.
- ☐ State No Free Lunch and its implication.

### EAs and GAs
- ☐ Write out the 5-step EA loop.
- ☐ Name and describe 4 selection methods (roulette, tournament, rank, elitism).
- ☐ Compute roulette probabilities and pick parents from random numbers.
- ☐ Apply single-point, two-point and uniform crossover by hand.
- ☐ Apply bit-flip and Gaussian mutation by hand.
- ☐ Explain effect of $p_c$, $p_m$, $t$, $N$ on exploration/exploitation.
- ☐ Compare generational vs steady-state replacement.
- ☐ Compare direct vs indirect encoding (with timetabling/TSP examples).
- ☐ Explain why permutation problems need special crossover (PMX, OX).

### Genetic Programming
- ☐ Tree representation; function & terminal sets.
- ☐ Koza's 5 preparatory steps.
- ☐ Subtree crossover and mutation.
- ☐ Symbolic regression as the canonical example.
- ☐ Compare GA vs GP across all dimensions (see Tier 2 table).

### Swarm Intelligence — ACO
- ☐ State the double-bridge experiment.
- ☐ Define stigmergy.
- ☐ Write the transition rule with $\alpha, \beta$.
- ☐ Write the pheromone update rule with $\rho$.
- ☐ Compute transition probabilities by hand.
- ☐ Compute pheromone updates by hand.
- ☐ Draw a construction graph for a given problem.
- ☐ Pick a heuristic $\eta$ for TSP / scheduling / pipe-routing.
- ☐ Name variants: Ant System, MMAS, Elitist, AntNet.

### Swarm Intelligence — PSO & Boids
- ☐ Write the PSO velocity equation with all three terms.
- ☐ Compute one step of PSO update by hand.
- ☐ Explain effect of $c_1, c_2, w$ on exploration/exploitation.
- ☐ Describe pbest vs gbest.
- ☐ State the 3 Boids rules with steering interpretation.
- ☐ Explain how Boids leads to emergent flocking.

### Multi-objective Optimisation
- ☐ Define Pareto dominance; show worked example.
- ☐ Identify Pareto front from a 2D scatter plot.
- ☐ Do non-dominated sorting on 6–10 solutions.
- ☐ Compute crowding distance for one front.
- ☐ Explain why dominance fails for many-objective ($M \geq 4$).
- ☐ State NSGA-II steps: sort → crowd → tournament → vary → merge → repeat.
- ☐ State MOPSO archive idea and a leader-selection strategy.
- ☐ List 2 challenges for convergence; 2 challenges for diversity.

### Neural Networks
- ☐ State the perceptron equation; sketch its decision boundary.
- ☐ Design perceptron weights by hand for a given linear boundary.
- ☐ Apply the perceptron learning rule pattern-by-pattern.
- ☐ Explain why a single perceptron cannot solve XOR.
- ☐ Pick an MLP architecture for a given separability problem.
- ☐ State the backprop weight update equation.
- ☐ Explain why activation must be differentiable.
- ☐ Compare perceptron / MLP / SOM / RNN in one row each.
- ☐ Describe SOM update including BMU and neighbourhood.
- ☐ Explain overfitting and 3 remedies (early stopping, more data, smaller net).
- ☐ State the weight-initialisation problem with zeros.
- ☐ Explain graceful degradation.

### Artificial Life & Cellular Automata
- ☐ State the 4 Game-of-Life rules (B3/S23).
- ☐ Define Moore vs von Neumann neighbourhood.
- ☐ Step a small CA grid forward by hand.
- ☐ List 3 emergent patterns (glider, oscillator, still life).
- ☐ State CA properties: locality, parallelism, homogeneity.
- ☐ Define fractal dimension; compute for Koch curve.

### Critical perspective
- ☐ State Sörensen's main critique of metaphor-based metaheuristics.
- ☐ State the No Free Lunch theorem.
- ☐ Distinguish genuine algorithmic novelty from rebranding.

### Newer / Bi-level / Spiking
- ☐ Describe LIF neuron and STDP rule.
- ☐ Explain why SNNs are hard to train and how EAs help.
- ☐ State the von Neumann bottleneck and how neuromorphic hardware avoids it.
- ☐ Name an EA application optimising NN architecture or weights.

---

## 10. Quick-reference equation card

| Concept | Equation |
|---------|----------|
| Roulette wheel | $P(i) = f_i / \sum_k f_k$ |
| Tournament | pick $t$ uniformly, keep best |
| PSO velocity | $v \leftarrow w v + c_1 z_1 (p - x) + c_2 z_2 (g - x)$ |
| PSO position | $x \leftarrow x + v$ |
| ACO transition | $P_{ij} = \tau_{ij}^\alpha \eta_{ij}^\beta / \sum_l \tau_{il}^\alpha \eta_{il}^\beta$ |
| ACO update | $\tau_{ij} \leftarrow (1-\rho)\tau_{ij} + \sum_k Q/L_k$ |
| Perceptron | $y = \text{step}(\sum w_i x_i + b)$ |
| Perceptron learning | $\Delta w_i = \eta(t-y) x_i$ |
| Backprop | $w \leftarrow w + \eta \delta o$, $\delta_{\text{out}} = (t-o)\sigma'$, $\delta_{\text{hid}} = \sigma' \sum \delta w$ |
| SOM update | $w_i \leftarrow w_i + \eta(t) h_{ci}(t)(x - w_i)$ |
| Crowding distance | $d_i \mathrel{+}= (f_m^{i+1} - f_m^{i-1}) / (f_m^{\max} - f_m^{\min})$ |
| Average rank (MOPSO) | $\bar{r}_i = \frac{1}{M} \sum_m r_{im}$ |
| LIF neuron | $\tau \dot V = -(V - V_{\text{rest}}) + RI$, spike when $V > V_\theta$ |
| Hausdorff dim | $D = \log N / \log(1/s)$ |
| Game of Life | survive: 2–3 neighbours; birth: exactly 3 |

---

## 11. Exam-day strategy

1. **Read every question first** (~3 min). Mark the one you feel strongest on — start there to bank marks early.
2. **Allocate time by marks**: 1.2 min/mark with a 10% buffer for the end.
3. **For multi-part questions**: budget per sub-part; don't blow 20 minutes on one 4-mark sub-part.
4. **Worked calculations**: *show every step* — partial credit is huge.
5. **Pseudocode questions**: write clean numbered steps, name your operators. A line per step.
6. **Comparison questions (6+ marks)**: ALWAYS use a table — it forces structure and is faster to mark.
7. **Design questions**: use the 7-section template (problem → encoding → algo → operators → fitness → experiments → success).
8. **End-of-paper sweep**: re-read Q1 short answers; they're cheap marks if you missed one.

---

## 12. Where to look in this wiki

| If you need... | Go to |
|----------------|-------|
| Algorithm definitions | `wiki/concepts/` |
| Lecture-by-lecture summaries | `wiki/sources/` |
| Cross-cutting comparisons | `wiki/comparisons/` |
| Worked exam examples | `wiki/exam/ecm3412-*.md` |
| Equations index | `wiki/index.md` (bottom of page) |

---

## Topics Covered (in this prep doc)
Selection, GA, EA loop, GP, encodings, fitness landscape, exploration/exploitation, ACO, PSO, Boids, swarm intelligence, multi-objective optimisation, Pareto, NSGA-II, MOPSO, perceptron, MLP, backpropagation, SOM, RNN, overfitting, graceful degradation, cellular automata, Game of Life, fractals, AIS, AntNet, SNN, neuromorphic computing, Sörensen metaphor critique, premature convergence, GP bloat, hypervolume, time-series NN design.

---

## 13. Older Papers (2015–2018) — additional patterns

*Added after ingesting 2015, 2016, 2017, 2018. The 2024–25 syllabus has shifted somewhat, so treat these as **secondary** prep — but recurring themes carry through and several topics here are still in current lectures.*

### 13.1 Different paper structure (DO NOT ASSUME)

**Older format (2015–2018):** Q1 compulsory (40 marks) + answer **2 of 3** elective questions from Q2/Q3/Q4 (30 marks each). This means you could **drop your weakest topic**.

**Current format (2019–2025):** all 3 questions compulsory. No drop allowed.

If your 2026 paper uses the older format, you'll have a 30-mark "lifeline" — but plan as if every topic is mandatory.

### 13.2 New topics that appeared in 2015–2018 but NOT in 2019–2025

These are still on the current concept pages or naturally extend them — worth knowing.

#### ☐ 13.2.1 Premature convergence — detection & remediation
(2016 Q2(b), 2018 Q2(e))

- **Definition:** the population loses diversity and converges to a suboptimal region before exploring enough of the search space.
- **Detection signals:**
  - Population diversity (mean Hamming distance / fitness variance) drops sharply.
  - Best fitness plateaus while mean fitness rises toward it.
  - High proportion of identical individuals.
- **Remediation:**
  - Increase mutation rate temporarily.
  - Inject random immigrants / restart with diversity.
  - Larger population.
  - Adaptive operator rates.
  - Niching / fitness sharing.
  - Switch to a higher-pressure-resistant selection (tournament with smaller $t$).

#### ☐ 13.2.2 Edge-case mutation/crossover rates
(2016 Q2(d))

- **$p_m = 0$ (no mutation):** algorithm can only recombine existing genes. Once the population converges on a region, it **cannot escape** — pure crossover preserves alleles that are common to all parents. Causes severe premature convergence.
- **$p_c = 0$ (no crossover):** degenerates to **parallel hillclimbing** — each individual climbs independently via mutation. Loses the *building-block* benefit (good schemas combining across parents).
- **$p_m = 1$, $p_c = 1$ (maximum):** most aggressive variation; can destroy good solutions; effectively random search.

#### ☐ 13.2.3 Convergence indicators per algorithm
(2016 Q3(d))

| Algorithm | Convergence signal |
|-----------|--------------------|
| **GA** | Population diversity ↓ (Hamming distance / fitness variance); best fitness plateaus |
| **PSO** | Swarm radius (mean distance from gbest) → 0; particle velocities → 0 |
| **ACO** | Pheromone on best path → 1, others → 0; tour similarity (% shared edges) → 100% |

#### ☐ 13.2.4 GP bloat
(2017 Q3, 2018 Q2)

- **Definition:** trees grow in size over generations *without* a corresponding fitness improvement.
- **Causes:** subtree crossover preferentially produces ever-larger offspring; selection favours slightly-better-but-larger trees; "introns" (neutral code) accumulate.
- **Remedies:**
  - **Depth or node limit** (hard cap).
  - **Parsimony pressure**: penalise size in fitness ($f = \text{accuracy} - \lambda \cdot \text{size}$).
  - **Tarpeian method**: randomly kill oversized individuals before evaluation.
  - **Operator equalisation**: enforce uniform size distribution.
  - **Dynamic limits**: adaptively grow the limit only when fitness improves.

#### ☐ 13.2.5 Hypervolume (HV) — multi-objective metric
(2018 Q3)

- $\text{HV}(S, r) = $ volume in objective space dominated by $S$ and bounded by reference point $r$.
- **Pareto-compliant**: if A dominates B (set-wise), HV(A) ≥ HV(B). One of the only single-number metrics that is.
- **Worked pattern (2D minimisation):** sort the front by $f_1$; sum vertical strips $(r_2 - f_2^i) \times (f_1^{i+1} - f_1^i)$.
- Used by **SMS-EMOA**: at each generation, remove the solution with the *smallest exclusive HV contribution* (the one whose removal shrinks HV the least).

#### ☐ 13.2.6 Sigmoid backprop explicit form
(2018 Q4)

For sigmoid output $o = \sigma(\text{net})$, $\sigma'(\text{net}) = o(1-o)$, giving the form you should *quote directly* in any backprop question:
- **Output node:** $\delta_j = o_j(1 - o_j)(t_j - o_j)$
- **Hidden node:** $\delta_j = o_j(1 - o_j) \sum_k \delta_k w_{kj}$
- **Weight update:** $w_{ij} \leftarrow w_{ij} + \eta \delta_j o_i$

#### ☐ 13.2.7 NN design for time-series (weather-forecasting pattern)
(2015 Q4)

When asked to design an NN for time-series prediction (rainfall, demand, etc.):

1. **Input encoding:** sliding window of past $k$ timesteps; one-hot for categorical (e.g. wind direction = 8 binary inputs).
2. **Output:** regression (next value) or classification (softmax over discrete buckets).
3. **Architecture:** MLP with 1–2 hidden layers (or RNN/LSTM if order matters); sigmoid/ReLU activations.
4. **Train/val/test split:** **time-respecting** (60/20/20 in chronological order — never shuffle time-series).
5. **Overfitting prevention:** early stopping on validation loss, L1/L2 regularisation, dropout, smaller net, more data, ensemble.
6. **Evaluation:** MAE/RMSE for regression, accuracy/F1 for classification, compared against a persistence (yesterday-equals-today) baseline.

#### ☐ 13.2.8 Exhaustive search — pros and cons
(2017 Q1(b))

| Pros | Cons |
|------|------|
| Guaranteed global optimum | Exponential time complexity |
| Deterministic / reproducible | Infeasible beyond ~25 binary variables |
| Easy to verify correctness | No early-termination quality estimate |
| No parameter tuning | Cannot exploit problem structure |

Use only when the search space is tiny or you can prove the optimum is needed.

#### ☐ 13.2.9 SOM 3-phase learning decomposition
(2016 Q4(d), 2017 Q2(b))

The SOM update can be cleanly decomposed:
1. **Competition:** each neuron computes $\|x - w_i\|$; the **BMU** $c$ is the argmin.
2. **Cooperation:** the BMU defines a *neighbourhood* via $h_{ci}(t) = \exp(-\|r_c - r_i\|^2 / 2\sigma(t)^2)$ — a Gaussian over the grid.
3. **Adaptation:** $w_i(t+1) = w_i(t) + \eta(t) \cdot h_{ci}(t) \cdot (x - w_i(t))$.

Both $\eta(t)$ and $\sigma(t)$ **decay over time** (exponential or linear).

### 13.3 Confirmed-recurring topics across both eras

These appear in both old and new papers — high priority is unchanged:
- **AntNet** (2015, 2020) — Tier 3 in section 5.7 — keep it on the list.
- **F1 GA case study (Wloch & Bentley 2004)** (2016, 2019) — solid Tier 3 case study.
- **ACO symbol definitions** $\alpha, \beta, \rho$ — recurring quick-definition mark.
- **Reynolds' three Boids rules** — appears in every era.
- **Tournament selection vs roulette comparison** — recurring 6+ mark question.
- **GA vs GP comparison table** — recurring; section 4.3 table covers it.

### 13.4 Out-of-syllabus topics (do NOT spend time on these)

These appeared in 2016–2018 but have been **dropped from current lectures**. You will not be tested on them by name. Recognising them is enough.

| Topic | Where appeared | Why ignored |
|-------|----------------|-------------|
| **NETtalk** (Sejnowski & Rosenberg 1987) | 2017 Q2, 2018 Q4 | Replaced by current ANN/SNN material; named case study no longer in syllabus |
| **Widrow-Hoff (Delta rule)** | 2017 Q1(f)(iii) | Subsumed by general backprop coverage |
| **ZDT benchmark family** by name | 2018 Q3 | Not in current MOO lectures |
| **SMS-EMOA** by name | 2018 Q3 | Not in current MOO lectures (NSGA-II/MOPSO are) |
| **Fractals (Koch, Menger)** | 2015 (?), 2020 only | Last appeared 2020; not in current A-life slides — low priority |

### 13.5 Amendments to earlier sections (Tier rankings revised)

After seeing 11 papers (2015–2018 + 2019–2025):

- **AIS (Section 5.5):** Only 1 appearance (2023). With more data, this is a **single-paper anomaly** — keep at Tier 3 but do not over-invest.
- **Premature convergence (NEW):** add to **Tier 2** — appeared 2016 and 2018, conceptually adjacent to exploration-exploitation which is Tier 1.
- **GP bloat (NEW):** add to **Tier 3** — appeared 2017 and 2018; GP itself is Tier 2 so a sub-topic question is plausible.
- **Hypervolume (NEW):** add to **Tier 3** — only 2018 by name, but the *concept* (measuring MO performance) is implicit in NSGA-II questions.
- **SOM (Section 4.7):** now seen 6 times across both eras — promote in your prep priority from "Tier 2" to "Tier 1.5". Memorise the 3-phase competition/cooperation/adaptation decomposition.
- **Sigmoid backprop form $o(1-o)$:** add this to your equation card — it is the *expected* derivative form in any worked backprop question.

### 13.6 Updated equation card additions

| Concept | Equation |
|---------|----------|
| Sigmoid derivative | $\sigma'(\text{net}) = o(1-o)$ |
| Backprop output node | $\delta_j = o_j(1-o_j)(t_j - o_j)$ |
| Backprop hidden node | $\delta_j = o_j(1-o_j) \sum_k \delta_k w_{kj}$ |
| SOM Gaussian neighbourhood | $h_{ci}(t) = \exp(-\|r_c - r_i\|^2 / 2\sigma(t)^2)$ |
| Hypervolume (2D, min) | $\text{HV} = \sum_i (r_2 - f_2^i)(f_1^{i+1} - f_1^i)$ |
| Parsimony pressure (GP) | $f' = f - \lambda \cdot \text{size}$ |

### 13.7 Additional checklist items (from 2015–2018)

- ☐ Detect premature convergence (3 signals); apply 3 remedies.
- ☐ Predict behaviour of $p_m = 0$ and $p_c = 0$.
- ☐ Name a convergence indicator for GA, for PSO, and for ACO.
- ☐ Define GP bloat; name 3 countermeasures.
- ☐ Compute hypervolume of a 3–4-solution Pareto front in 2D.
- ☐ Write sigmoid backprop $\delta$ formulas without notes.
- ☐ Describe SOM as competition / cooperation / adaptation.
- ☐ Sketch a time-series NN with time-respecting train/val/test split.
- ☐ State 2 pros and 2 cons of exhaustive search.
