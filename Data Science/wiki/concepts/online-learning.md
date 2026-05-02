---
title: "Online learning"
type: concept
sources: [online-learning]
related: [batch-vs-online-learning, data-shifts, concept-drift, sgd-all-reduce, stream-processing]
updated: 2026-05-02
---

# Online learning

*A model update paradigm where parameters are revised on every arriving observation, enabling continuous adaptation to evolving data at the cost of increased sensitivity to noise.*

## Definition

**Online learning** (also called per-observation or incremental learning) updates model parameters with each new data point as it arrives. There is no batching — the model is always in a state of learning. This is equivalent to stochastic gradient descent (SGD) with batch size 1.

## Why it matters

When data streams are live and the underlying distribution can change (concept drift, covariate shift), a model trained once on historical data will decay. Online learning keeps the model perpetually current without requiring expensive full retraining.

## Mechanism

```
For each new observation (x, y):
  Compute gradient: g = ∇loss(x, y; θ)
  Update:           θ ← θ - η * g
```

The **learning rate η** controls how aggressively the model adapts:
- High η → fast adaptation, but noisy updates dominate; convergence unstable.
- Low η → stable convergence, but slow to react to real distribution shifts.

A bad or anomalous observation has *immediate* impact on the model — there is no averaging over a batch to dilute outliers.

## Trade-offs vs full batch and mini-batch

| | Full batch | Mini-batch | Online |
|---|---|---|---|
| Data used | All data | Recent subset | One observation |
| Gradient | True gradient | Estimate | Noisy estimate |
| Convergence | Smooth | Moderate variance | High variance |
| Adaptation to drift | Requires full retrain | Periodic retrain | Immediate |
| Memory requirement | All data in memory | Batch in memory | O(1) |
| Production use | Rare (small data only) | Common | Streaming pipelines |

## Examples in the syllabus

- Online Learning s. 11–12: definition, learning rate, monitoring requirements.
- Real-world use: recommendation systems that need to react to the latest user interaction.

## Common exam framing

- "What is online learning and how does it differ from mini-batch learning?"
- "What is the role of the learning rate in online learning?"
- "Why is online learning more sensitive to bad data than batch learning?"

## See also

- [[batch-vs-online-learning]]
- [[data-shifts]]
- [[concept-drift]]
- [[sgd-all-reduce]]
- [[stream-processing]]
