# Representations and Encodings

**Type:** design concept
**Related:** [[evolutionary-algorithms]], [[crossover-mutation]], [[fitness-landscapes]], [[genetic-programming]]
**Source lectures:** [[lecture04-ea-detail]], [[lecture05-encodings]]

---

## What it is

A **representation** (or encoding) maps a candidate solution (phenotype) to a chromosome (genotype). The choice of encoding:
- Defines which mutation/crossover operators are valid
- Determines the shape of the fitness landscape
- Shapes the difficulty of the problem

**This is arguably the most important design decision in applying EAs.**

---

## Types of encoding

### Binary strings
- Chromosome: `01101011`
- Mutation: flip one bit
- Crossover: standard 1-point, 2-point, uniform
- Good for: feature selection, bounded integer problems
- Historical note: originally considered most general (Holland's GA theory)

### Integer / k-ary vectors
- Chromosome: `[17, 2, 19, 1, 1, 5]`
- Each gene: integer in range `[0, k-1]`
- Mutation: replace gene with random value in range
- Example: Water distribution pipe diameters (k = number of possible sizes)

### Real-valued vectors
- Chromosome: `(0.3, 0.2, 0.4, 0.2, 0.1)`
- Mutation: add Gaussian noise $\delta \sim \mathcal{N}(0, \sigma^2)$
- Used for: continuous optimisation (antenna design, neural network weights)
- PSO uses this natively

### Permutations
- Chromosome: `(2, 0, 6, 7, 5, 1, 4, 3)`
- Must visit each element exactly once
- Mutation: **swap** two elements (not random replacement — would create duplicates)
- Crossover: requires repair (e.g. order crossover)
- Used for: TSP, job scheduling, any sequencing problem

### Trees
- Chromosome: a tree structure (functions at internal nodes, terminals at leaves)
- This is the basis of **Genetic Programming**
- Mutation: replace a random subtree
- Crossover: swap random subtrees between parents

---

## Direct vs Indirect Encoding

| | Direct | Indirect |
|--|--------|---------|
| **What the gene represents** | A variable in the problem directly | A rule/parameter of a constructive heuristic |
| **Example** | Exam in time slot 4 | "Use the 4th clash-free slot for this exam" |
| **Invalid solutions** | Handled by penalising fitness | Mostly handled by encoding — fewer invalid solutions |
| **Search space** | Larger (includes invalid regions) | Smaller (invalid solutions removed structurally) |
| **Landscape smoothness** | Smooth | Can be rugged |
| **Speed** | Fast to decode | Slow to decode |
| **Domain knowledge** | Not required | Required to build the heuristic |

**Key insight:** Indirect encodings exploit domain knowledge to make the search space smaller and the problem easier. Direct encodings are simpler to apply but may waste effort on invalid regions.

---

## The encoding–landscape relationship

Different encodings for the same problem create different landscapes:
- A mutation that changes one gene might produce a large phenotypic change (rugged) or a small one (smooth)
- The "right" encoding is one where similar genotypes produce similar phenotypes (epistasis is low)

**Epistasis:** when the effect of one gene depends on the value of another gene. High epistasis = rugged landscape = harder for EAs.

---

## Real-world examples

| Problem | Encoding | Type |
|---------|---------|------|
| Travelling Salesman | Permutation of cities | Direct |
| Exam Timetabling | Integer vector (direct slot) | Direct |
| Exam Timetabling | Integer vector (clash-free slot index) | Indirect |
| Water pipe diameters | k-ary vector | Direct |
| Antenna design | Real vector (3D coordinates) | Direct |
| Neural network weights | Real vector | Direct |
| Program evolution | Tree | Direct |

---

## Connections

- [[crossover-mutation]] — operators must be designed for the encoding
- [[fitness-landscapes]] — encoding shapes the landscape
- [[genetic-programming]] — tree-based encoding specialised for program evolution
- [[pso]] — requires real-valued encoding; [[pso#Binary PSO]] for discrete problems

---

## Exam notes

- Encoding choice = landscape shape = operator choice — all three are tightly coupled
- Permutations: standard mutation breaks validity; must use swap/inversion/OX crossover
- Direct encoding: simple but may include large invalid regions (high dimensionality wasted on infeasible solutions)
- Indirect encoding: smaller, harder landscape but requires domain knowledge
- The **same problem** can have many valid encodings; each may require different operators and produce different difficulty
