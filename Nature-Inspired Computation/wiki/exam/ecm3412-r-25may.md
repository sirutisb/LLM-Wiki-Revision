# ECM3412 — R-Paper May 2025 Exam Walkthrough

**Year:** 2025 (R-Paper / Resit)
**Module:** ECM3412 Nature-Inspired Computation
**Source:** `raw/past_exam_papers/R-paper/ECM3412-R-25May.pdf`

## Instructions (from paper)

- The **duration** of this paper is 2hr
- Word Count: No Word Count
- Write all answers in the answer booklet provided.
- Do not open the exam paper until instructed by the Invigilator.
- Use only black pen or pencil.
- Mobile and electronic devices are not allowed.
- Do not communicate with other candidates during the exam.

**Exam Instructions:** Answer ALL Questions

---

## Question 1 — Broad Concepts (40 marks total)

### Full question text

**(a)** Compare and contrast *exploration* and *exploitation* in evolutionary algorithms. How do different *selection* methods affect the balance between these two aspects? **(5 marks)**

**(b)** Explain how the following components of a genetic algorithm affect its performance:
- Population size
- Mutation rate
- Crossover operator
- Selection pressure

Provide specific *examples* for each component. **(8 marks)**

**(c)** In the context of Genetic Programming, explain the key differences between program evolution and traditional genetic algorithms. Include a discussion of *representation* and *genetic operators*. **(7 marks)**

**(d)** State why Boids are good choice for producing a computational model of a flock of birds, and state the three properties of motion used to control the movement of Boids. **(4 marks)**

**(e)** Explain the role of *velocity* in particle swarm optimisation. **(5 marks)**

**(f)** Explain why NSGA-II requires both non-dominated sorting *and* crowding distance. **(4 marks)**

**(g)** The ability to *generalise* and *graceful degradation* are biological principles exhibited by neural networks. Explain what is meant by each. **(4 marks)**

**(h)** In the context of cellular automata, explain the properties of *localism*, *parallelism*, and *homogeneity*. **(3 marks)**

---

### Answer

#### Part (a) [5 marks]

**Exploration** is the process of searching new, unexplored regions of the fitness landscape — discovering candidate solutions in areas not yet evaluated. **Exploitation** is the process of refining and improving already-discovered good solutions by focusing search near them. These are fundamentally in tension: too much exploration wastes evaluations on poor regions; too much exploitation leads to premature convergence to a local optimum.

In [[evolutionary-algorithms]], this balance is primarily controlled by **selection pressure**:

- **Roulette wheel (fitness-proportionate) selection** ($P(i) = f_i / \sum f_k$) creates high exploitation when one individual dominates in fitness — a superfit individual will monopolise selection, collapsing diversity. This risks premature convergence (see [[selection]]).
- **Rank-based selection** ($P(i) \propto \text{rank}_i$) decouples selection probability from raw fitness magnitude. This gives more moderate, controllable pressure — the best individual's advantage is bounded by rank, not raw fitness. Better balance of exploration and exploitation.
- **Tournament selection** (size $t$): $t = 1$ gives random selection (pure exploration, no progress); $t = 2$ gives mild pressure; large $t$ approaches deterministic selection of the best (pure exploitation). Practitioners tune $t$ to find the right balance — it is the most widely used method because pressure is directly and simply tunable.

Key principle: **high selection pressure** accelerates convergence (more exploitation) but sacrifices population diversity (less exploration), risking premature convergence to a local optimum.

---

#### Part (b) [8 marks]

**Population size:**
A larger population provides greater genetic diversity, allowing the algorithm to explore more of the fitness landscape simultaneously. With a population of 10 on a complex optimisation problem, there is a high risk of all individuals converging to the same local basin. With a population of 200, multiple basins are explored in parallel. However, larger populations require more fitness evaluations per generation, so they are slower per generation. Too small a population is vulnerable to genetic drift (loss of diversity by chance).

**Mutation rate:**
Mutation introduces random variation into individuals, primarily driving exploration. A low mutation rate (e.g. 0.001 per gene) makes small local changes — fine-tuning good solutions (exploitation). A high mutation rate (e.g. 0.5 per gene) makes large random jumps — effective exploration but risks destroying good solutions. In a binary GA optimising a scheduling problem, a mutation rate of ~0.01 per gene is typically appropriate; setting it to 0.5 effectively randomises chromosomes each generation, preventing convergence.

**Crossover operator:**
The crossover operator determines how genetic material is recombined from two parents. **1-point crossover** swaps one contiguous tail segment — preserving schemata (building blocks) of short defining length. **Uniform crossover** randomly assigns each gene from either parent — the most disruptive, mixing genes most thoroughly. For example, in a feature selection problem (binary chromosome), uniform crossover produces children that are genuinely new combinations of selected features rather than partial sections of parents. **For permutation encodings** (e.g. TSP), standard crossover creates invalid tours, so **Order Crossover (OX)** is required to maintain validity.

**Selection pressure:**
As discussed in (a), higher selection pressure means the fittest individuals are more likely to be selected for reproduction. In a GA solving a neural network weight optimisation problem: high tournament size ($t = 10$) concentrates reproductive effort on the few best weight configurations, rapidly climbing toward a local optimum — fast but potentially trapped. Low tournament size ($t = 2$) keeps a broader diversity of weight configurations in play, slower but less prone to premature convergence. Selection pressure interacts with population size: a small population with high selection pressure is especially prone to losing diversity.

---

#### Part (c) [7 marks]

**Representation:**
A traditional [[genetic-algorithms|GA]] uses a **fixed-length chromosome** — a vector of genes (binary, integer, or real-valued). Each gene encodes a parameter of a candidate solution (e.g. a network weight, a scheduling slot, a pipe diameter). The length is fixed at design time.

[[genetic-programming|GP]] uses a **variable-length tree structure** as the chromosome. Internal nodes contain functions (e.g. `+`, `*`, `IF`) drawn from a function set $F$; leaf nodes contain terminals (e.g. variables or constants) drawn from terminal set $T$. The tree represents an executable program or mathematical expression — for example, the tree for `(X + 3.7) / Y` has `÷` at the root, `+` and `Y` as children, and `X` and `3.7` as leaves. There is no fixed structure: trees can grow or shrink during evolution.

**Genetic operators:**
In a GA, mutation replaces a randomly chosen gene with a new value (e.g. flipping a bit; replacing an integer with another in range). Crossover performs point-based recombination: a 1-point crossover simply swaps the tail segment of two chromosomes. These operators assume positional meaning: gene $k$ in parent 1 corresponds to gene $k$ in parent 2.

In GP:
- **Subtree mutation**: a random node is selected; the entire subtree rooted at that node is removed and replaced with a newly generated random subtree. This can make large structural changes (e.g. replacing a complex sub-expression with a leaf constant).
- **Subtree crossover**: a random subtree is chosen from each parent and they are swapped. Child 1 gets parent 1's tree with parent 2's chosen subtree inserted at the selected node; child 2 is the reverse. This preserves most of each parent's structure while exchanging one sub-expression.

**Fitness evaluation:**
In a GA, fitness is typically a direct computation on the chromosome's parameter values. In GP, fitness evaluation requires **running the program** on every training case and measuring prediction error — significantly more computationally expensive.

**Goal:**
A GA evolves solution *parameters*. GP evolves the solution *algorithm or function* itself — for example, symbolic regression discovers the formula $f(x) = x^2 + x + 1$ from data points, rather than just optimising $f$'s parameters.

---

#### Part (d) [4 marks]

**Why Boids are a good model:**
Boids (Craig Reynolds, 1987) are a good computational model of flocking because they reproduce the key observed properties of real bird flocks — directed group movement, collision avoidance, no central leader, spontaneous polarisation, and flash expansion — using only **three simple, local rules**. The model is scalable (each boid only considers nearby neighbours), parameter-free in terms of global coordination, and captures the emergent nature of flocking: complex global behaviour arising from local interactions alone. This matches the biological reality that real flocks have no leader issuing commands. See [[flocking-boids]].

**The three properties (rules) of motion:**
1. **Separation** — steer to avoid crowding local flockmates (prevents collisions)
2. **Alignment** — steer toward the average heading of local flockmates (synchronises direction)
3. **Cohesion** — steer toward the average position of local flockmates (keeps group together)

---

#### Part (e) [5 marks]

In [[pso|Particle Swarm Optimisation]], **velocity** is the mechanism by which particles move through the search space. It is not merely a step size — it has direction and magnitude, and it encodes the particle's "momentum" as well as the influences pulling it toward good regions of the landscape.

The velocity update equation is:
$$v_{ij}(t+1) = v_{ij}(t) + c_1 z_1 (p_{ij} - x_{ij}(t)) + c_2 z_2 (g_j - x_{ij}(t))$$

There are **three components**:

1. **Inertia** — $v_{ij}(t)$: the particle's current velocity carries it forward in the same direction. This acts as momentum, allowing the particle to pass through local optima rather than stopping at the first good position found.

2. **Cognitive component** — $c_1 z_1 (p_{ij} - x_{ij})$: a pull toward the particle's own personal best position $p_{ij}$. This represents the particle's memory of where it has personally found the best solution so far, driving exploitation of individually promising areas.

3. **Social component** — $c_2 z_2 (g_j - x_{ij})$: a pull toward the swarm's global best position $g_j$. This represents collective knowledge — all particles are drawn toward the best position found by any particle, enabling rapid convergence on promising regions.

The random coefficients $z_1, z_2 \sim U(0,1)$ are drawn independently each iteration, introducing stochasticity that prevents premature collapse of all particles onto a single point.

The position is then updated as $x_{ij}(t+1) = x_{ij}(t) + v_{ij}(t+1)$.

**Summary:** velocity plays the dual role of memory (inertia), individual learning (cognitive), and social learning (global best attraction). It replaces crossover and mutation in EAs as the mechanism balancing exploration and exploitation.

---

#### Part (f) [4 marks]

NSGA-II solves two distinct problems that arise in multi-objective optimisation, and each mechanism addresses one of them. See [[nsga-ii]] and [[multi-objective-optimization]].

**Non-dominated sorting alone is insufficient** because, while it correctly ranks solutions into Pareto layers (Rank 0 = non-dominated front, Rank 1 = next best layer, etc.), it gives no guidance about *which* solutions from the same rank to keep when a rank is too large to fit into the new population. All solutions on the same rank are equally good by dominance criteria — there is no way to choose between them. Without a tiebreaker, the selection among same-rank solutions would be arbitrary.

**Crowding distance alone is insufficient** because it only measures density in objective space — it cannot distinguish a solution on the true Pareto front from one that is dominated but sits in a sparse region. Without non-dominated sorting, dominated solutions could be retained simply because they happen to be in a less crowded part of the objective space.

**Together:** non-dominated sorting assigns rank (measures convergence toward the true Pareto front), and crowding distance breaks ties within the same rank by preferring solutions in less crowded areas of the Pareto front (measures diversity). The combined criterion is: prefer lower rank; if equal rank, prefer larger crowding distance. This produces a population that is both close to the true Pareto front **and** evenly spread along it. Crowding distance also eliminates the need for a niche radius parameter (unlike earlier approaches).

---

#### Part (g) [4 marks]

These are properties of [[neural-networks|artificial neural networks (ANNs)]] that mirror corresponding properties of the biological brain. See also [[neural-networks]].

**Generalisation:**
The ability to generalise means that a trained neural network can correctly classify or predict **novel inputs it has not seen during training**. The network learns the underlying pattern or regularity in the data, not just a lookup table of the training examples. For instance, an ANN trained on images of handwritten digits can correctly classify a new handwritten digit it was never shown. This contrasts with rote memorisation (overfitting), where the network would fail on new inputs. Generalisation arises because of the distributed, weighted representation: the weights encode statistical regularities that apply broadly.

**Graceful degradation:**
Graceful degradation means that when neurons or connections are removed (damaged or lost), the network's performance **decreases gradually rather than failing catastrophically**. Because knowledge is distributed across many weights rather than stored in a single location (as in a symbolic expert system), the loss of a small number of neurons causes a partial reduction in accuracy, not total failure. This mirrors the brain's robustness: people who suffer partial brain damage do not lose all cognitive function — they typically lose specific capabilities to a degree proportional to the damage.

---

#### Part (h) [3 marks]

In the context of [[cellular-automata|cellular automata]] (Ulam and von Neumann, 1940s):

**Localism:**
Each cell's state at the next time step is determined solely by its current state and the states of its immediate **local neighbourhood** (e.g. the 4 orthogonal cells in a von Neumann neighbourhood, or the 8 surrounding cells in a Moore neighbourhood). No cell has access to global information about the grid. Rules are purely local — complex global behaviour is entirely an emergent consequence of these local interactions.

**Parallelism:**
All cells update their state **simultaneously** at each time step. There is no sequential sweep from cell to cell; every cell in the grid applies its rule at the same moment. This means the CA operates as a massively parallel computation, and the updating of one cell does not influence the inputs used to update any other cell in the same time step.

**Homogeneity:**
Every cell in the grid uses the **same update rule**. There are no specialist cells with different rules; every cell is identical in terms of the rule it applies. Differences in behaviour across the grid arise only from differences in initial state and neighbourhood configurations, not from different rule sets.

---

## Question 2 — Ant Colony Optimisation: Water Distribution Network (30 marks total)

### Full question text

Consider optimizing a water distribution network using Ant Colony Optimization (ACO). The problem consists of selecting pipe diameters for a network of water pipes.

**Problem Specifications:**
- Each pipe in the network must be assigned exactly one diameter
- Available diameters: {100mm, 150mm, 200mm, 250mm, 300mm}
- Cost for each pipe = selected diameter × pipe length
- When water flows through the network, each node must maintain a minimum pressure of 15.0 units
- A network simulator is available that can calculate pressure at each node (connection between two pipes) for any given pipe configuration

For example, if we have a pipe of length 10 meters and choose a diameter of 200mm, its cost would be 2000 units.

**(a)** Draw and explain the construction graph that ants would traverse to solve this problem using ACO. How is this different from the TSP construction graph? **(8 marks)**

**(b)** Design a suitable objective function that will:
- Minimize the total network cost
- Ensure all nodes meet the minimum pressure requirement
- Guide ants towards feasible solutions
**(8 marks)**

**(c)** Design a suitable heuristic function ($\eta_{ij}$) to guide ants in selecting pipe diameters. Explain how this heuristic relates to the problem objectives. **(6 marks)**

**(d)** Specify the following ACO parameters for solving this problem:
- Number of ants
- Pheromone evaporation rate ($\rho$)
- Relative importance of pheromone trails ($\alpha$)
- Relative importance of heuristic information ($\beta$)
- Initial pheromone values
- Stopping criterion

Justify your choices. **(8 marks)**

---

### Answer

#### Part (a) [8 marks]

**Construction graph for the pipe diameter problem:**

The construction graph has a **layered structure** with one layer per pipe in the network. Suppose the network has $P$ pipes numbered $1, \ldots, P$. The graph is:

```
[START] → [Pipe 1: d=100] [Pipe 1: d=150] [Pipe 1: d=200] [Pipe 1: d=250] [Pipe 1: d=300]
              ↓               ↓               ↓               ↓               ↓
          [Pipe 2: d=100] [Pipe 2: d=150] ... [Pipe 2: d=300]
              ↓
          ...
              ↓
          [Pipe P: d=100] ... [Pipe P: d=300]
              ↓
            [END]
```

- There are $P$ layers, one per pipe.
- Each layer has 5 nodes, one per available diameter (100mm, 150mm, 200mm, 250mm, 300mm).
- Each ant starts at the START node and at each layer selects one of the 5 diameter nodes for that pipe, moving forward one layer at a time.
- After traversing all $P$ layers, the ant has assembled a complete pipe configuration: one diameter assignment for every pipe.
- Pheromone $\tau_{i,d}$ is maintained on each (pipe $i$, diameter $d$) node (or equivalently on each edge entering it).

**How this differs from the TSP construction graph:**

| Dimension | TSP construction graph | Pipe diameter construction graph |
|-----------|----------------------|----------------------------------|
| Structure | Fully-connected graph of city nodes | Layered graph: $P$ layers, 5 nodes each |
| Path | Ant visits each city exactly once (permutation) | Ant visits each pipe layer exactly once, choosing one of 5 diameter options |
| Path length | $N$ nodes for $N$ cities | $P$ layers — one per pipe |
| Return to start | Yes (complete tour back to start city) | No (open path — no return needed) |
| Constraint | No city revisited | No constraint on which diameter can be chosen (any valid) |
| Pheromone location | On directed edges between cities | On edges into each (pipe, diameter) node |
| Choice size | $N-1$ options at first node, decreasing | Always 5 options at each layer |

In the TSP, the number of available next nodes shrinks as the tour progresses (already-visited cities are excluded). In the pipe problem, the number of choices at each layer is always 5 regardless of previous choices. The pipe problem is therefore closer to ACO's application to bin packing or job scheduling than to TSP — it is a **combinatorial assignment** problem, not a permutation problem. See [[ant-colony-optimization]].

---

#### Part (b) [8 marks]

The objective function must serve two purposes: minimising cost (primary objective) and penalising infeasible solutions where one or more nodes fall below the minimum pressure. Since ACO uses pheromone reinforcement proportional to solution quality, the objective function should map all solutions — feasible and infeasible — to a single scalar that is **larger for better solutions** (or can be inverted: smaller = better, then used as $1/\text{objective}$ for pheromone deposition).

**Proposed objective function (minimisation form):**

$$F(\mathbf{d}) = C_{\text{total}}(\mathbf{d}) + \lambda \cdot V(\mathbf{d})$$

where:

- $\mathbf{d} = (d_1, d_2, \ldots, d_P)$ is the diameter assignment (the ant's solution)
- $C_{\text{total}}(\mathbf{d}) = \sum_{i=1}^{P} d_i \times L_i$ is the total network cost (diameter × length for each pipe $i$ with length $L_i$)
- $V(\mathbf{d})$ is the total pressure violation:
$$V(\mathbf{d}) = \sum_{n \in \text{nodes}} \max(0,\ 15.0 - p_n(\mathbf{d}))$$
where $p_n(\mathbf{d})$ is the pressure at node $n$ computed by the network simulator for configuration $\mathbf{d}$
- $\lambda > 0$ is a penalty weight that controls how strongly infeasible solutions are penalised relative to cost

**Justification of each component:**

1. **$C_{\text{total}}$**: directly encodes the primary objective — minimise total pipe cost. Ants producing cheaper configurations (smaller diameters or fewer large-diameter pipes where not needed) will have lower $C_{\text{total}}$.

2. **$V(\mathbf{d})$**: the pressure violation term penalises infeasible configurations by summing the shortfall at each under-pressure node. A configuration where one node has pressure 10.0 (shortfall 5.0) is penalised less than one where five nodes are at 5.0 (shortfall 50.0). This creates a gradient: ants with near-feasible solutions (small violations) are only slightly penalised, guiding search toward the feasibility boundary.

3. **$\lambda$ (penalty weight)**: must be set large enough that feasible solutions are always preferred over infeasible ones, but not so large that all infeasible solutions are equally bad (which would lose gradient information). A reasonable starting value is $\lambda = \bar{C} / \bar{V}$ where $\bar{C}$ and $\bar{V}$ are typical cost and violation magnitudes, normalising the two terms to the same scale.

**Pheromone deposition** should use $1/F(\mathbf{d})$ so that ants with lower (better) $F$ deposit more pheromone:
$$\Delta\tau^k = Q / F(\mathbf{d}^k)$$

This guides the swarm collectively toward low-cost, feasible configurations.

---

#### Part (c) [6 marks]

The heuristic function $\eta_{ij}$ provides domain knowledge that guides ants even before pheromone has accumulated, and throughout the search when pheromone trails are weak. For pipe $i$ choosing diameter $d_j$:

**Proposed heuristic:**

$$\eta_{i,d_j} = \frac{1}{d_j \times L_i}$$

This is the **inverse cost** of assigning diameter $d_j$ to pipe $i$. Ants will prefer smaller-diameter pipes (lower cost) all else being equal, directly encoding the cost minimisation objective.

**Limitation and refinement:**
The inverse-cost heuristic alone ignores the pressure constraint — it would always favour 100mm pipes regardless of whether they can carry enough flow to maintain pressure. A better heuristic balances cost against expected pressure contribution.

**Improved heuristic using a flow-capacity proxy:**

$$\eta_{i,d_j} = \frac{d_j^\gamma}{d_j \times L_i} = \frac{d_j^{\gamma - 1}}{L_i}$$

where $\gamma > 1$ is a scaling exponent. This gives larger diameters a heuristic boost: the numerator $d_j^\gamma$ approximates the pipe's capacity to support pressure (flow capacity scales with diameter by hydraulic principles — larger diameter reduces head loss), while the denominator $d_j \times L_i$ is the cost. With $\gamma \approx 2$, the heuristic approximates:

$$\eta_{i,d_j} \propto \frac{d_j}{L_i}$$

meaning: prefer larger diameters on longer pipes (which cause more head loss and are more likely to cause pressure violations), and accept small diameters on short pipes (where cost savings are safer).

**Relation to problem objectives:**
- The denominator (cost term) directly guides toward the cost minimisation objective.
- The numerator (diameter proxy for flow capacity) guides toward the pressure constraint: pipes that are likely bottlenecks (long pipes, pipes early in the network) will be heuristically directed toward larger diameters.
- This heuristic effectively incorporates soft domain knowledge without needing to call the expensive network simulator at the heuristic evaluation stage.

See [[ant-colony-optimization]] for the full transition rule: $P_{i,d_j} \propto [\tau_{i,d_j}]^\alpha \cdot [\eta_{i,d_j}]^\beta$.

---

#### Part (d) [8 marks]

**Number of ants:**
Recommend **$m = P$** (one ant per pipe) or **$m = 2P$**, where $P$ is the number of pipes. This is analogous to the TSP convention of using one ant per city. For a moderately sized network ($P = 20$ pipes), this gives 20–40 ants. Too few ants ($m = 3$) limits solution diversity and slows pheromone accumulation; too many ($m = 500$) wastes evaluations per iteration since calling the network simulator is expensive. With $m = P$, each iteration produces a diverse set of solutions at reasonable computational cost.

**Pheromone evaporation rate ($\rho$):**
Recommend $\rho = 0.1$ to $0.2$ (i.e. retain 80–90% of pheromone per iteration). Low evaporation preserves good solutions longer, allowing the algorithm to exploit promising diameter patterns. However, $\rho$ must not be too low (e.g. 0.01), as this causes pheromone to accumulate irreversibly on early good solutions, preventing escape from local optima. If the network simulator is expensive to call, a slightly lower $\rho$ (0.05) slows convergence, allowing more exploration per unit of computational budget.

**Relative importance of pheromone ($\alpha$):**
Recommend $\alpha = 1.0$. Standard value from ACO literature. $\alpha > 1$ causes the algorithm to rely heavily on pheromone and converge fast (exploitation); $\alpha < 1$ reduces reliance on pheromone, making the heuristic more dominant (exploration). Starting at $\alpha = 1$ gives balanced weighting.

**Relative importance of heuristic ($\beta$):**
Recommend $\beta = 2.0$ to $3.0$. In the TSP, $\beta = 5$ is common because the heuristic ($1/d_{ij}$, prefer shorter edges) is highly informative. In this problem, the heuristic encodes useful but less definitive information (balancing cost vs pressure). $\beta = 2$ gives the heuristic meaningful weight without overwhelming the pheromone signal, which accumulates true problem-specific knowledge over iterations.

**Initial pheromone values:**
Set all $\tau_{i,d_j}$ to a **uniform small value**, e.g. $\tau_0 = 1 / (P \times \bar{C})$, where $\bar{C}$ is the estimated average solution cost. Uniform initialisation ensures no bias toward any particular diameter at the start, giving all options equal initial probability. This prevents artificially biasing early exploration toward, for example, the largest (highest-cost) diameters. If using MMAS, $\tau_0 = \tau_{\max}$ (the upper bound) is preferred.

**Stopping criterion:**
Use a combination:
1. **Maximum iterations**: e.g. 500 iterations. Provides a hard budget, important given the expensive simulator.
2. **Convergence criterion**: stop if the best solution has not improved for 50 consecutive iterations. This prevents wasting simulator calls when the algorithm has stagnated.
3. Alternatively: stop when normalised pheromone entropy falls below a threshold (all pheromone concentrated on one diameter per pipe), indicating the algorithm has committed to a solution.

The expensive network simulator call per ant per iteration means computational budget is the primary constraint — maximum iterations combined with a stagnation check balances thoroughness against cost.

---

## Question 3 — PSO, Multi-objective Optimisation, and Neural Networks (30 marks total)

### Full question text

**(a)** Particle swarm optimisation has a number of parameters that control the effectiveness of the algorithm.

  **(i)** State two of them and explain their purpose. **(4 marks)**

  **(ii)** Suggest an experiment that will confirm that the correct parameters have been chosen. **(5 marks)**

**(b)** A dataset has 5,000 attributes. Design a multi-objective optimisation problem that identifies which of the attributes are most vital to a given prediction task (the specific prediction task is not important to this question).

Your problem must comprise two objectives. State the objectives, whether they are to be maximised or minimised, and explain why this objective is important to the problem. Outline the solution representation explaining why it is a sensible choice for this problem. **(9 marks)**

**(c)** The diagram below shows a specific type of neural network. State the type of neural network, provide a use case for this specific type of neural network, and explain why it is a sensible choice for this use case. **(6 marks)**

*[Diagram shows a recurrent/Elman-style network with 4 input nodes $x_1$–$x_4$, 4 hidden nodes $h_1$–$h_4$ connected in a chain with recurrent connections $v_2, v_3, v_4$ going left-to-right, 4 output nodes $y_1$–$y_4$, with weights $u_i$ on input-to-hidden connections and $w_i$ on hidden-to-output connections.]*

**(d)** The Iris dataset contains 150 observations of measurements describing iris flours. Each flower is described by four features: petal length and width, and sepal length and width. The data contains three classes: *iris-virginica*, *iris-versicolor* and *iris-setosa*. Provide a labelled diagram showing the smallest self-organising map needed to model this data, and explain why your proposed structure is appropriate. **(6 marks)**

---

### Answer

#### Part (a)(i) [4 marks]

Two key parameters of [[pso|PSO]] and their purposes:

**1. Acceleration coefficients $c_1$ (cognitive) and $c_2$ (social):**
$c_1$ controls the strength of the pull toward each particle's personal best position ($p_{ij}$). A higher $c_1$ causes particles to trust their own experience more, making them explore more individually and converge socially more slowly. $c_2$ controls the pull toward the global best position ($g_j$). A higher $c_2$ causes all particles to converge rapidly toward the swarm's current best, risking premature convergence to a local optimum. Typically both are set to ~2.0. The balance between $c_1$ and $c_2$ directly controls the exploration-exploitation tradeoff: high $c_1$/low $c_2$ = more individual exploration; low $c_1$/high $c_2$ = rapid social exploitation.

**2. Swarm size $N$:**
The swarm size determines how many candidate solutions are maintained simultaneously. A larger swarm ($N = 100$) provides better coverage of the search space — particles are initially spread more widely, reducing the chance of all particles starting near the same local optimum. However, more particles means more fitness evaluations per iteration, so convergence takes longer in real time. A smaller swarm ($N = 10$) converges faster per generation but risks missing good regions. For high-dimensional problems, a larger swarm is generally required. This is analogous to population size in EAs.

*(Other valid answers: neighbourhood size — controls local vs global topology; number of iterations — sets the total computational budget.)*

---

#### Part (a)(ii) [5 marks]

**Experiment design for parameter validation:**

The appropriate experiment is a **parameter sensitivity study combined with repeated independent runs**, structured as follows:

1. **Define a benchmark problem set**: use multiple test functions with known optima (e.g. Sphere, Rastrigin, Rosenbrock) spanning unimodal and multimodal landscapes. Do not test only on the target problem — this risks overfitting parameters to one problem.

2. **Parameter grid search**: systematically vary the parameters of interest. For example, vary $c_1, c_2 \in \{1.0, 1.5, 2.0, 2.5, 3.0\}$ and $N \in \{20, 50, 100, 200\}$, giving a grid of configurations.

3. **Multiple independent runs**: for each parameter configuration, run PSO **at least 30 times** (with different random seeds) on each benchmark function. This is necessary because PSO is stochastic — a single run gives no reliable information. Record the best fitness found and the number of iterations to convergence.

4. **Statistical comparison**: compare mean best fitness and variance across configurations using appropriate statistical tests (e.g. Wilcoxon signed-rank test). The "correct" parameters are those that give significantly better mean performance and/or faster convergence across the benchmark set.

5. **Validation on target problem**: once good parameters are identified on benchmarks, confirm performance on the actual target problem with 30 independent runs, comparing against the default parameter setting.

**Key criterion for "correct parameters"**: the chosen parameters should give good performance (close-to-optimal solutions) consistently (low variance) across multiple independent runs, on both the benchmarks and the target problem.

---

#### Part (b) [9 marks]

**Problem: Feature selection from a 5,000-attribute dataset.** See [[multi-objective-optimization]] and [[nsga-ii]].

**Two objectives:**

**Objective 1: Maximise predictive accuracy**
Use cross-validated accuracy (or equivalently minimise prediction error, e.g. mean absolute error) of a predictor trained on the selected subset of features. This is important because the ultimate goal is to identify features that are informative for the prediction task — a feature subset that gives poor prediction accuracy is useless regardless of its size. *Maximise* accuracy (or equivalently, *minimise* error).

**Objective 2: Minimise the number of selected features**
Count the number of features included in the selected subset (i.e. the number of 1-bits in the binary representation). This is important for two reasons: (1) fewer features reduce computational cost at both training and deployment time; (2) with 5,000 attributes, using all features risks overfitting and makes the model uninterpretable. Including only the most informative features improves generalisation. *Minimise* feature count.

**Why these two objectives conflict:** adding more features generally improves (or at worst does not worsen) training accuracy, but we want to minimise the count. The Pareto front of this problem represents all optimal trade-offs between accuracy and parsimony — from a single highly discriminative feature (minimum count, lower accuracy) up to the full informative set (maximum accuracy, high count).

**Solution representation:**
A **binary vector of length 5,000**: $\mathbf{x} = (x_1, x_2, \ldots, x_{5000})$ where $x_i = 1$ means feature $i$ is selected and $x_i = 0$ means it is excluded.

This is a sensible choice because:
- It directly encodes the inclusion/exclusion decision for each attribute, making both objectives trivial to compute: feature count = $\sum_i x_i$; predictive accuracy = train and evaluate a model on the selected features.
- Standard binary [[crossover-mutation|genetic operators]] apply: bit-flip mutation (randomly include or exclude one feature) and uniform crossover (randomly combine two feature subsets). Both produce valid binary vectors — there are no constraints on which features can be selected simultaneously, so no repair is needed.
- Binary PSO (see [[pso]]) could also be used, where velocity is interpreted as a probability threshold for each bit, making this problem compatible with MOPSO or NSGA-II with binary encoding.

**Multi-objective algorithm:** NSGA-II ([[nsga-ii]]) or MOPSO ([[mopso]]) would both be appropriate, producing a Pareto front of feature subsets from which a practitioner can choose based on their accuracy-vs-parsimony trade-off preference.

---

#### Part (c) [6 marks]

**Type of neural network:**
The diagram shows a **Recurrent Neural Network (RNN)** — specifically an **Elman network** (or simple recurrent network). The key identifying features are:
- Each hidden unit $h_i$ receives input from its corresponding input $x_i$ (via weight $u_i$) and produces output $y_i$ (via weight $w_i$)
- The hidden units are connected in sequence: $h_1 \to h_2 \to h_3 \to h_4$ via connections $v_2, v_3, v_4$ — these are the **recurrent/lateral connections** that allow information to flow from earlier hidden units to later ones within the same time step (or from $t$ to $t+1$ in a temporal reading)

**Use case:**
A suitable use case is **sequence modelling or time series prediction** — for example, predicting the next word in a sentence (language modelling), or predicting the next value in a time series (stock price, sensor reading, weather variable).

**Why it is a sensible choice:**
A standard feedforward MLP treats each input independently — it has no notion of sequence or context. In language modelling, the probability of the next word depends heavily on the words that preceded it. The recurrent connections in an RNN allow hidden units to maintain a **hidden state** that encodes information from previous inputs in the sequence. As the network processes a sequence token by token, the hidden state accumulates context. At each step, the current input and the previous hidden state jointly determine the new hidden state and the output prediction. This makes RNNs naturally suited to variable-length sequences and temporal dependencies that a standard MLP cannot capture. See [[neural-networks]] for the broader ANN framework.

---

#### Part (d) [6 marks]

**Smallest SOM for the Iris dataset:**

The Iris dataset has **3 classes** (iris-virginica, iris-versicolor, iris-setosa) and **4-dimensional input** (petal length, petal width, sepal length, sepal width).

The smallest SOM that can meaningfully model this data needs at least **3 neurons** — one per class. However, a $1 \times 3$ linear map cannot preserve topology for data that may not lie on a 1D manifold. The minimum 2D grid that provides enough neurons to represent 3 classes with some topological separation is a **$2 \times 2$ grid (4 neurons)**. This provides:
- 4 neurons — enough to assign at least one neuron per class, with one neuron acting as a "boundary" or shared region between two similar classes
- A 2D topology that can separate iris-setosa (which is linearly separable from the other two) from iris-versicolor and iris-virginica (which partially overlap)

**Labelled diagram:**

```
+------------------+------------------+
|                  |                  |
|   iris-setosa    |  iris-versicolor |
|   (neuron 1)     |   (neuron 2)     |
|                  |                  |
+------------------+------------------+
|                  |                  |
|  boundary/mixed  |  iris-virginica  |
|   (neuron 3)     |   (neuron 4)     |
|                  |                  |
+------------------+------------------+
```

Each neuron is a 4-dimensional weight vector (matching the 4 input features). After training, the BMU (Best Matching Unit) for a given iris observation will be the neuron whose weight vector is closest to the 4-feature measurement.

**Why this structure is appropriate:**
- Iris-setosa is linearly separable from the other two classes in petal space — it will naturally cluster to one corner neuron.
- Iris-versicolor and iris-virginica overlap partially, so they may share two adjacent neurons with the SOM boundary between them.
- The 2D topology of a $2 \times 2$ grid means topographically adjacent neurons represent similar regions of the input space — the SOM's neighbourhood update rule during training ensures that nearby neurons learn similar weight vectors, preserving the topology of the 3-class structure.
- A $1 \times 3$ grid would force a linear topology that cannot represent the 2D structure of the class boundaries; a $3 \times 3$ or larger grid is more expressive but not the **smallest** sufficient structure.

See [[self-organising-maps]] for the full SOM algorithm (competition → cooperation → adaptation).

---

## Topics Covered

| Topic | Questions | Concept page |
|-------|-----------|-------------|
| Exploration vs exploitation | Q1(a), Q1(b) | [[evolutionary-algorithms]], [[selection]] |
| GA components (population, mutation, crossover, selection) | Q1(b) | [[genetic-algorithms]], [[crossover-mutation]] |
| Genetic Programming | Q1(c) | [[genetic-programming]] |
| Boids / Flocking | Q1(d) | [[flocking-boids]] |
| PSO velocity | Q1(e), Q3(a) | [[pso]] |
| NSGA-II (non-dominated sort + crowding distance) | Q1(f) | [[nsga-ii]], [[multi-objective-optimization]] |
| Neural network properties (generalisation, graceful degradation) | Q1(g) | [[neural-networks]] |
| Cellular automata (localism, parallelism, homogeneity) | Q1(h) | [[cellular-automata]] |
| ACO construction graph | Q2(a) | [[ant-colony-optimization]] |
| ACO objective / fitness design | Q2(b) | [[ant-colony-optimization]] |
| ACO heuristic function | Q2(c) | [[ant-colony-optimization]] |
| ACO parameter setting | Q2(d) | [[ant-colony-optimization]] |
| PSO parameters | Q3(a) | [[pso]] |
| Multi-objective feature selection | Q3(b) | [[multi-objective-optimization]], [[nsga-ii]] |
| Recurrent neural network | Q3(c) | [[neural-networks]] |
| Self-organising maps | Q3(d) | [[self-organising-maps]] |
