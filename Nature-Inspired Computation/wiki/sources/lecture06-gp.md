# Lecture 6 — Genetic Programming

**File:** `raw/text/2024NICLecture6.txt`
**Lecturer:** Dr Alberto Moraglio
**Concepts introduced:** [[genetic-programming]]

---

## Summary

Introduces Genetic Programming as an EA where individuals are programs represented as trees. Covers the five preparatory steps, random program generation, mutation, crossover, and a full symbolic regression example.

## Key content

### Core idea
Conventional programming: human writes program → program produces output.
GP: required behaviour + training data → GP evolves program automatically.

### History
Invented by Cramer; popularised by John Koza (1992, MIT Press book). Considered a branch of AI.

### Algorithm
1. Generate random programs (as trees)
2. Evaluate each program on training data
3. Select, crossover, mutate
4. Repeat until a good program is found

### Koza's 5 preparatory steps
1. **Terminal set $T$:** inputs, constants (e.g. `{X, Y, random-constants}`)
2. **Function set $F$:** operations (e.g. `{+, -, *, ÷, IF, AND, OR, <, >=}`)
3. **Fitness measure:** e.g. sum of |predicted - actual| over training cases
4. **Parameters:** population size, max depth, crossover rate, mutation rate
5. **Termination:** e.g. error < 0.1, max generations

### Random program generation
Recursive: start with random function node at root; at each childless node, if depth < max-1 choose randomly from $F \cup T$; if depth = max-1, choose only from $T$ (terminals).

### Mutation
Choose a random node (subtree); remove it; generate a new random subtree in its place.

### Crossover
Choose a random subtree from each parent; swap them. Both children inherit most of their parent's structure with a new subtree inserted.

### Fitness evaluation
Must **run** the evolved program on all test cases → significantly more expensive than standard EAs.

### Symbolic regression example
Target: $y = x^2 + x + 1$. Terminal set: $\{X, \text{constants}\}$. Function set: $\{+, -, *, \div\}$.
Generation 0 contains 4 random programs. After selection + operators → GP discovers the correct formula.

### Applications
- Symbolic regression, antenna design, circuit design, robot navigation, data mining

## Key takeaways
- GP = EA with tree-encoded programs; everything else (selection, operators, evaluation loop) same as standard EA
- Fitness evaluation is expensive: must execute program
- Can produce unexpected/innovative solutions (antenna patented)

## Links to concepts
- [[genetic-programming]]: full treatment
- [[representations]]: tree encoding
- [[crossover-mutation]]: subtree-specific mutation and crossover
