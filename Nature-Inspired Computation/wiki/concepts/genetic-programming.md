# Genetic Programming

**Type:** algorithm
**Related:** [[evolutionary-algorithms]], [[representations]], [[crossover-mutation]]
**Source lectures:** [[lecture06-gp]]

---

## What it is

**Genetic Programming (GP)** is an EA where the individuals (chromosomes) are **programs** represented as **tree structures**. Instead of evolving a solution to a problem, GP evolves the **algorithm or function** that solves it.

> Conventional programming: human writes program → program produces output  
> GP: GP evolves program from examples of (input, desired output) pairs

Popularised by John Koza (1992); considered a branch of AI.

---

## The GP tree representation

A program is a tree where:
- **Internal nodes:** functions from a function set $F$ (e.g. `+, -, *, ÷, IF`)
- **Leaf nodes (terminals):** variables or constants from terminal set $T$ (e.g. `X, Y, 3.14`)

Example tree for the expression `(X + 3.7) / Y`:
```
        ÷
       / \
      +   Y
     / \
    X  3.7
```

---

## The five preparatory steps (Koza)

1. **Terminal set $T$** — the inputs and constants (e.g. `{X, Y, random constants}`)
2. **Function set $F$** — the operations (e.g. `{+, -, *, ÷, IF, AND, OR, <}`)
3. **Fitness measure** — how to score a candidate program (e.g. sum of absolute errors over training data)
4. **Parameters** — population size, crossover/mutation rates, max tree depth
5. **Termination criterion** — e.g. error < 0.1, or max generations reached

---

## Generating random programs

Recursive procedure:
1. Start with random function node at root (depth 1)
2. For each node without children:
   - If depth < max_depth − 1: randomly choose a function or terminal as child
   - If depth = max_depth − 1: **must choose a terminal** (prevents infinite growth)

---

## GP mutation

**Subtree mutation:**
1. Select a random node in the tree
2. Remove the subtree rooted at that node
3. Generate a new random subtree in its place (following depth rules)

This is the standard approach — biased toward high-depth nodes.

---

## GP crossover

**Subtree crossover:**
1. Select a random subtree from parent 1 (a node and everything below it)
2. Select a random subtree from parent 2
3. Swap the two subtrees: child 1 gets parent 1 with parent 2's subtree inserted; child 2 gets parent 2 with parent 1's subtree inserted

---

## Fitness evaluation in GP

Unlike standard EAs, the chromosome is a **program** — to evaluate it you must **run it**:
1. For each test case (input, expected output):
   - Execute the GP-generated program on the input
   - Compute error vs. expected output
2. Aggregate errors over all test cases → fitness

This makes GP significantly more computationally expensive than standard EAs.

---

## Applications

| Task | GP approach |
|------|-------------|
| **Symbolic regression** | Discover the formula $y = f(x)$ from data points |
| **Antenna design** | Evolve wire geometry for optimal radiation pattern |
| **Circuit design** | Evolve circuit topologies |
| **Robot navigation** | Evolve navigation programs |
| **Data mining** | Evolve classification rules |

**Real example — antenna design (Altshuler & Linden 1998):**
- 7-wire antenna represented as 105-bit chromosome (7 × 3 coordinates × 5 bits each)
- Fitness: radiation pattern closeness to target (simulated with NEC)
- Result: patented antenna design (US Patent 5,719,794)

---

## Symbolic Regression example

Objective: Find the function $f(x) = x^2 + x + 1$ from 11 data points.

- Terminal set: `{X, random constants}`
- Function set: `{+, -, *, ÷}`
- Fitness: sum of |predicted − actual| across training data
- GP discovers `x² + x + 1` from scratch

---

## Pros & Cons

| Advantage | Disadvantage |
|-----------|--------------|
| Can evolve novel program structures | Very expensive fitness evaluation |
| No predefined solution structure needed | Programs can grow very large (bloat) |
| Works on symbolic/logical as well as numeric problems | Hard to interpret results |
| Can innovate beyond human-designed solutions | Requires careful choice of $F$ and $T$ |

---

## Connections

- [[representations]] — tree representation is a specialised encoding
- [[evolutionary-algorithms]] — GP is an EA; the loop is identical
- [[crossover-mutation]] — GP uses subtree-specific versions of these

---

## Exam notes

- GP = EA where individuals are **programs** in tree form
- 5 preparatory steps (Koza): terminal set, function set, fitness measure, parameters, termination
- Mutation: replace a random subtree with a newly generated random subtree
- Crossover: swap subtrees between two parents
- Fitness evaluation requires **running the program** on test cases — expensive
- Applications: symbolic regression, antenna design, circuit design, robot navigation
