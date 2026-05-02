---
title: "Parallel k-means"
type: concept
sources: [distributed-machine-learning]
related: [mapreduce, communication-patterns, sgd-all-reduce]
updated: 2026-05-02
---

# Parallel k-means

*A MapReduce implementation of k-means clustering that distributes the expensive distance computation across mappers and uses combiners to reduce network traffic.*

## Definition

**Parallel k-means** is a distributed implementation of the k-means clustering algorithm using the [[mapreduce|MapReduce]] framework. The iterative centroid-update loop maps naturally to the map-combine-reduce cycle.

## Why it matters

Standard k-means requires computing distances from every point to every centroid on every iteration — O(n × K) per iteration. For large datasets this is prohibitive on a single machine. The MapReduce implementation parallelises the distance step across all mappers.

## Mechanism — three phases per iteration

```
Input: data points + current K centroids

MAP:
  For each data point:
    compute distance to each centroid
    assign point to nearest centroid
    emit (cluster_id, point_coordinates)

COMBINE (local aggregation before shuffle):
  For each cluster_id seen on this mapper:
    compute local mean (sum of coordinates + count)
    emit (cluster_id, (local_sum, local_count))

REDUCE:
  For each cluster_id:
    aggregate all local sums and counts from all mappers
    new_centroid = total_sum / total_count
    test convergence (has centroid moved < threshold?)
    emit new centroid

Repeat until convergence.
```

## Why combiners help

Without combiners, every point's coordinates travel the network to the reducer. With combiners, each mapper pre-aggregates its local cluster members — only (sum, count) per cluster per mapper crosses the network. Significant bandwidth saving.

## Trade-offs

- **+** Scales to very large datasets — distance computation is embarrassingly parallel.
- **+** Combiners drastically reduce shuffle volume.
- **−** Multiple MapReduce iterations (one per k-means round) — job startup overhead per iteration.
- **−** Centroid broadcast is a sequential step before each round.

## Examples in the syllabus

- Distributed Machine Learning s. 32: the three-phase MapReduce structure.

## Common exam framing

- "Explain how k-means clustering can be implemented using MapReduce."
- "What role does the combiner play in parallel k-means?"

## See also

- [[mapreduce]]
- [[communication-patterns]]
