# Genetic Algorithms (GA)

**Type:** algorithm
**Related:** [[evolutionary-algorithms]], [[selection]], [[crossover-mutation]], [[representations]]
**Source lectures:** [[lecture02-ea-motivation]], [[lecture04-ea-detail]]

---

## What it is

A **Genetic Algorithm (GA)** is the most well-known type of EA, typically using **binary or integer encoding** with **selection, crossover, and mutation** operators. Introduced by John Holland (1975) based on Darwinian evolution analogy (chromosomes, genes, fitness, natural selection).

GAs are a specific instantiation of the general [[evolutionary-algorithms]] framework with emphasis on crossover as the primary operator.

---

## Standard GA (generational)

```
1. Initialise: N random binary chromosomes; evaluate fitness
2. Repeat:
   a. Select 2*(N-1) parents via rank-based or roulette selection
   b. Pair up parents; apply crossover + mutation → N-1 children
   c. Evaluate children's fitness
   d. Keep best 1 from current generation (elitism)
   e. New generation = best 1 + N-1 children
3. Return best individual found
```

---

## Standard GA (steady-state)

```
1. Initialise: N random chromosomes; evaluate fitness
2. Repeat:
   a. Tournament-select 1 parent (or 2 for crossover)
   b. Mutate (and optionally crossover)
   c. Evaluate offspring
   d. Replace weakest member if offspring is not worse
3. Return best
```

---

## Key design choices

| Component | Common choices |
|---------|---------------|
| **Encoding** | Binary string (classic); integer vector; real vector; permutation |
| **Selection** | Tournament (modern standard); rank-based; roulette wheel (historical) |
| **Crossover** | 1-point, 2-point, uniform (for binary/integer); order-based (for permutation) |
| **Mutation** | Bit-flip (binary); single-gene random (integer); Gaussian (real) |
| **Replacement** | Generational + elitism; steady-state replace-worst |

---

## The Schema Theorem (Holland)

A **schema** is a template that matches a subset of chromosomes — e.g. `1**0*` matches all 5-bit strings with 1 in position 1 and 0 in position 4.

The theorem shows that short, high-fitness, low-order schemata (building blocks) receive exponentially increasing representation over generations. This is the theoretical justification for why GAs work — they implicitly process many schemata in parallel ("implicit parallelism").

**Note:** The schema theorem applies strictly to binary encoding; its relevance to real-valued or other encodings is more complex.

---

## GA vs GP

| | GA | GP |
|--|----|----|
| Chromosome | Fixed-length vector | Variable-length tree |
| Represents | Solution parameter values | Program or function |
| Crossover | Point-based | Subtree swapping |
| Mutation | Gene replacement | Subtree replacement |
| Fitness evaluation | Direct computation | Run program on test cases |

---

## Connections

- [[evolutionary-algorithms]] — GAs are the most studied EA variant
- [[genetic-programming]] — tree-structured GA; evolves programs
- [[selection]] — selection methods
- [[crossover-mutation]] — crossover and mutation operators
- [[representations]] — encoding choice

---

## Exam notes

- GA = Holland's EA with emphasis on crossover as the main operator
- Two types: **generational** (full replacement) and **steady-state** (incremental)
- **Elitism**: always keep the best individual across generations
- Know the key operators for binary, integer, real-valued, and permutation encodings
- GA vs GP: GA = fixed-length parameters; GP = variable-length tree programs
