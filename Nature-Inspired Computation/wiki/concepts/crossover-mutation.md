# Crossover and Mutation Operators

**Type:** algorithm components
**Related:** [[evolutionary-algorithms]], [[representations]], [[fitness-landscapes]]
**Source lectures:** [[lecture04-ea-detail]], [[lecture05-encodings]]

---

## What they are

**Variation operators** generate new candidate solutions from existing ones:
- **Mutation:** modifies a single parent → explores locally
- **Crossover (recombination):** combines two parents → moves between two known-good regions

Together they balance **exploration** (finding new areas of the landscape) and **exploitation** (refining known good areas).

---

## Mutation Operators

### Binary / k-ary encoding

| Operator | Description | Example |
|---------|-------------|---------|
| **Single-gene** | Pick one gene randomly; change to random new value | `352872` → `312872` |
| **Multi-gene (m-gene)** | Single-gene mutation applied $m$ times | |
| **Bit-flip** (binary) | Flip a randomly chosen bit | `00110` → `00010` |

**Swap mutation:** Choose two genes; swap them. E.g. `352872` → `372852`. Note: in k-ary encodings this may not be meaningful — better for permutations.

### Real-valued encoding

| Operator | Description |
|---------|-------------|
| **Single-gene Gaussian** | Pick one gene; add noise $\delta \sim \mathcal{N}(0, \sigma^2)$ |
| **Vector mutation** | Add random vector $\delta \in \mathbb{R}^L$ to the entire solution |

The step size $\sigma$ controls the landscape: large $\sigma$ = long jumps (exploration), small $\sigma$ = fine-tuning (exploitation).

### Permutation encoding (e.g. TSP)

Standard single-gene mutation is **invalid** for permutations (would create duplicates). Valid options:

| Operator | Description |
|---------|-------------|
| **Swap** | Choose two positions; swap the values | `DEGJACBFIH` → swap positions 2,5 |
| **Inversion** | Reverse a sub-sequence | |
| **Insertion** | Remove element; insert at different position | |

---

## Crossover Operators

Crossover requires that children inherit parts from **both** parents. The key challenge: children must remain valid solutions.

### 1-Point Crossover (binary/k-ary)
Choose a random split point. Child 1 gets parent 1's prefix + parent 2's suffix; child 2 gets the reverse.
```
Parent 1: A B C D | E F G H
Parent 2: K L M N | O P Q R
Child 1:  A B C D | O P Q R
Child 2:  K L M N | E F G H
```

### 2-Point Crossover
Two split points; middle segment swapped.

### Uniform Crossover
Generate a random binary mask. Where mask=1, take from parent 2; where mask=0, take from parent 1.
```
Parent 1: A B C D E F G H
Mask:     0 1 0 0 1 1 0 1
Parent 2: K L M N O P Q R
Child 1:  A L C D O P G R
```
Uniform crossover can mix genes more thoroughly than k-point crossover.

### Crossover for permutations

Standard crossover creates **invalid children** (cities visited twice). Two fixes:

**1-Point with repair:**
1. Copy parent 1's prefix
2. Fill remaining positions from parent 2, in order, skipping already-present elements

**Order Crossover (OX):**
1. Copy a random sub-sequence from parent 1
2. Fill remaining positions from parent 2 starting after the crossover point, wrapping around, skipping duplicates

---

## Exploration vs Exploitation

| Aspect | Exploration | Exploitation |
|--------|-------------|-------------|
| **Goal** | Find new promising regions | Refine known good solutions |
| **Favoured by** | Large mutation rate; uniform crossover | Low mutation rate; small tournament |
| **Risk of too much** | Randomness, no progress | Premature convergence |

---

## How operators think of genetic information

- **Selection** decides *which* regions of the search space to focus on
- **Crossover** exploits by recombining good partial solutions from known-good parents
- **Mutation** explores by making small random perturbations

---

## Connections

- [[representations]] — operators must match the encoding; wrong operators = broken solutions
- [[fitness-landscapes]] — mutation step size determines landscape smoothness
- [[genetic-programming]] — tree-based mutation and crossover
- [[pso]] — PSO has no explicit crossover; velocity update plays a similar exploratory role

---

## Exam notes

- Match the operator to the encoding: standard gene mutation **breaks** permutation encoding
- Crossover requires a **fix/repair** step for permutation encodings (e.g. TSP)
- Uniform crossover: the most disruptive crossover (highest gene-mixing); 1-point: least
- **Crossover rate** controls fraction of offspring created by crossover vs. mutation alone
- A child produced by crossover is typically also mutated (crossover rate + mutation rate are independent)
