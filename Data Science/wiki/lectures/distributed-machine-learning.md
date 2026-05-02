---
title: "Lecture: Distributed Machine Learning"
type: lecture
sources: [distributed-machine-learning]
related: [communication-patterns, sgd-all-reduce, parallel-kmeans, mapreduce, batch-processing]
updated: 2026-05-02
---

# Lecture: Distributed Machine Learning

*How to train ML models across multiple machines — the communication patterns that matter, distributed SGD via all-reduce, and parallel k-means via MapReduce.*

## Slide-by-slide notes

- **(s. 2)** **Core challenge**: the primary design concern for distributed algorithms is communication patterns. Avoid idle workers waiting on other machines.
- **(s. 3–9)** **[[communication-patterns|Communication patterns]]** — the building blocks:
  - **Push** — Machine A sends data to Machine B.
  - **Pull** — Machine B requests data from Machine A.
  - **Broadcast** — Machine A sends data to many machines.
  - **Reduce** — compute a reduction (usually sum) across machines C₁…Cₙ; materialise result on one machine B.
  - **All-reduce** — same as reduce but materialise result on *all* participating machines.
  - **Wait** — one machine pauses and waits on a signal from another.
  - **Barrier** — all machines wait until every machine reaches the same point, then continue together.
- **(s. 10)** **Overlapping computation and communication**: network is slow — best performance comes from doing useful work *while* communication is happening, not stopping to wait for it.
- **(s. 11–15)** **[[sgd-all-reduce|SGD with all-reduce]]**:
  - Terminology: *epoch* = one full pass over training data; *batch* = entire dataset per gradient step; *minibatch* = subset per gradient step.
  - With M workers and minibatch size B: assign B' = B/M samples to each worker.
  - Each worker computes its partial gradient; an all-reduce sums all gradients → each machine now holds the full minibatch gradient.
  - All workers update their local model copy identically — statistically equivalent to standard minibatch SGD.
  - **Advantage**: same hyperparameters as serial SGD; all workers have the same role; built on standard primitives.
  - **Drawback**: workers are *idle* during the all-reduce communication — computation and communication are *not* overlapped.
- **(s. 16, 32–36)** **[[parallel-kmeans|Parallel k-means]] via MapReduce**:
  - **Map**: compute distances from each point to all K centroids; assign points to clusters; emit (cluster_id, point) pairs.
  - **Combine** (combiner): compute local centroid of each cluster — emit local sums and sample counts.
  - **Reduce**: test convergence; update global centroid positions.
  - Enables large-scale k-means by distributing distance computation across mappers and aggregating locally with combiners before the reduce.

## Key takeaways

1. **Communication patterns are the vocabulary** of distributed ML — push, pull, broadcast, reduce, all-reduce, wait, barrier.
2. **All-reduce = distributed minibatch SGD**: split the minibatch across M workers, compute partial gradients, all-reduce sums them so all workers get the full gradient and update identically.
3. **Statistically equivalent** to serial minibatch SGD — same hyperparameters, just faster wall-clock time (linear speedup when communication is free).
4. **Idle workers during all-reduce** is the main performance bottleneck — the gap that async and overlap techniques try to close.
5. **Parallel k-means** maps naturally to MapReduce: map = assign to clusters, combine = local sums, reduce = update centroids.

## Concepts introduced

- [[communication-patterns]]
- [[sgd-all-reduce]]
- [[parallel-kmeans]]

## Open questions / things to clarify

- Slides from s.16 onward are almost entirely figures — the parallel k-means algorithm is described at s.32. Steps between may show visual diagrams not captured in text.
- Async SGD and parameter server patterns are not covered in this deck — more advanced distributed ML topics.

## See also

- [[mapreduce]]
- [[batch-processing]]
- [[online-vs-batch-vs-stream]]
