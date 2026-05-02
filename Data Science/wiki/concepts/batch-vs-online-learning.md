---
title: "Batch vs online learning"
type: concept
sources: [online-learning]
related: [online-learning, data-shifts, concept-drift, sgd-all-reduce]
updated: 2026-05-02
---

# Batch vs online learning

*The spectrum from training once on all data to updating on every observation — each point on the spectrum trades gradient quality for adaptability and computational cost.*

## Definition

The three learning modes form a spectrum based on how much data is used per gradient update:

- **Full batch** — all available data used per update; computes the exact gradient.
- **Mini-batch** — a recent subset of data per update; computes a gradient estimate.
- **Online (per-observation)** — one data point per update; computes a noisy gradient estimate.

## Comparison table

| Dimension | Full batch | Mini-batch | Online |
|---|---|---|---|
| Gradient quality | True gradient | Estimate | Very noisy |
| Convergence stability | Smoothest | Moderate | Least stable |
| Memory requirement | All data | Batch size | O(1) |
| Handles drift? | Only after full retrain | With periodic retraining | Continuously |
| Sensitivity to bad data | Low (averaged) | Medium | High (immediate) |
| Production suitability | Rarely (only small datasets) | Most common | Streaming/real-time |

## Decision rule

Use **full batch** only if your dataset is small and static. Use **mini-batch** as the default for production ML. Use **online** when data is a live stream and the distribution is expected to change over time.

## Key differences explained

**Why full batch is expensive**: as data accumulates, retraining cost grows linearly. Memory must hold the entire dataset.

**Why mini-batch is a good middle ground**: controls the recency bias through batch size; more recent data has more influence. Batch size is a hyperparameter — smaller = more adaptation to recent data but noisier gradients.

**Why online is dangerous**: a single bad data point (corrupted sensor, fraudulent input) immediately shifts the model before any batching dilutes the effect. Requires close monitoring.

## Examples in the syllabus

- Online Learning s. 3–9: full batch and mini-batch defined with pros/cons.
- s. 11–12: online learning as the streaming extreme.

## Common exam framing

- "Compare full batch, mini-batch, and online learning on gradient quality, convergence stability, and suitability for streaming data."

## See also

- [[online-learning]]
- [[data-shifts]]
- [[concept-drift]]
