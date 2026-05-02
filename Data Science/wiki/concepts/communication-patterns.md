---
title: "Communication patterns (distributed ML)"
type: concept
sources: [distributed-machine-learning]
related: [sgd-all-reduce, distributed-machine-learning]
updated: 2026-05-02
---

# Communication patterns (distributed ML)

*The seven primitives governing how machines in a distributed system exchange data — the vocabulary that every distributed algorithm is built from.*

## Definition

A **communication pattern** describes how data moves between machines in a distributed system. Choosing the right pattern determines whether workers stay busy or sit idle. The key goal: **overlap computation and communication** — workers should do useful work while network transfers happen.

## The seven patterns

| Pattern | Description | Direction |
|---|---|---|
| **Push** | Machine A sends data to Machine B | One-to-one |
| **Pull** | Machine B requests data from Machine A | One-to-one (receiver-initiated) |
| **Broadcast** | Machine A sends data to all other machines | One-to-many |
| **Reduce** | Compute a reduction (e.g., sum) across C₁…Cₙ; result on one machine | Many-to-one |
| **All-reduce** | Same as reduce, but result materialised on *all* machines | Many-to-many |
| **Wait** | One machine pauses until it receives a signal from another | Synchronisation |
| **Barrier** | All machines pause until every machine has reached the barrier point | Global synchronisation |

## Why it matters

Communication over a network is orders of magnitude slower than computation. A barrier or a wait stalls all workers. An all-reduce in [[sgd-all-reduce|distributed SGD]] leaves workers idle during the communication phase — this is the primary performance bottleneck.

## Mechanism — all-reduce in detail

All-reduce is central to distributed training:

```
Workers: W1, W2, W3, W4

Each computes partial gradient g1, g2, g3, g4

All-reduce:
  sum = g1 + g2 + g3 + g4
  → all workers receive sum

Result: every worker holds the full minibatch gradient
```

Ring all-reduce (used in NCCL, Horovod) pipelines the operation to avoid a single bottleneck — each worker passes its partial result to its neighbour, amortising communication.

## Trade-offs

- **Synchronous all-reduce**: all workers must be at the same gradient step — one slow worker (straggler) blocks all others.
- **Asynchronous updates** (parameter server): workers can be at different steps — faster but gradients are "stale", which can hurt convergence.

## Examples in the syllabus

- Distributed Machine Learning s. 3–9: all seven patterns defined.
- s. 10: "overlapping computation and communication" as the key performance principle.

## Common exam framing

- "What is the difference between reduce and all-reduce?"
- "Why is a barrier expensive in a distributed ML system?"

## See also

- [[sgd-all-reduce]]
- [[distributed-machine-learning]]
