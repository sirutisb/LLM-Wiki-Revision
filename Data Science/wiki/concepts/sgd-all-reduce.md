---
title: "SGD with all-reduce"
type: concept
sources: [distributed-machine-learning]
related: [communication-patterns, parallel-kmeans, online-learning]
updated: 2026-05-02
---

# SGD with all-reduce

*Distributed minibatch gradient descent: split the minibatch across M workers, each computes a partial gradient, all-reduce sums them — every machine ends up with the full gradient and updates identically.*

## Definition

**SGD with all-reduce** is a data-parallel distributed training algorithm. It parallelises the gradient computation step of minibatch SGD across M worker machines, using the all-reduce communication primitive to aggregate partial gradients before the parameter update.

## Why it matters

Training large ML models on a single machine is too slow. All-reduce SGD gives a near-linear speedup in the compute phase while remaining statistically equivalent to serial minibatch SGD — same convergence, same hyperparameters, just faster.

## Mechanism

```
Serial minibatch SGD:
  gradient = (1/B) Σ ∇loss(x_m, θ)   for m = 1…B
  θ ← θ - η * gradient

Distributed (M workers, each processes B' = B/M samples):
  Worker k: g_k = (1/B') Σ ∇loss(x_m, θ)  for its B' samples
  All-reduce: g_total = Σ g_k  (sum on all machines)
  Each worker: θ ← θ - η * g_total / M
```

After the all-reduce, every worker holds the same full gradient and applies the same update → all workers stay in sync.

## Properties

- **Statistically equivalent** to serial minibatch SGD with batch size B — use the same learning rate and hyperparameters.
- **Symmetric roles** — all workers do the same thing; no parameter server hierarchy.
- **Simple to implement** — built on standard distributed computing primitives.

## Drawback — idle time during communication

Workers finish their gradient computations and then *wait* for the all-reduce to complete. During this window they are idle. This is the main inefficiency:

- Computation and communication are **not overlapped**.
- A straggler worker delays all others (synchronous barrier).

Solutions (not in the lecture): async SGD, gradient compression, ring all-reduce pipelines.

## Examples in the syllabus

- Distributed Machine Learning s. 11–15: full derivation and discussion.

## Common exam framing

- "Describe how SGD can be parallelised using the all-reduce primitive."
- "What is the statistical relationship between distributed all-reduce SGD and serial minibatch SGD?"
- "What is the main performance limitation of synchronous all-reduce SGD?"

## See also

- [[communication-patterns]]
- [[parallel-kmeans]]
- [[online-learning]]
