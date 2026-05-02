---
title: "Concept drift"
type: concept
sources: [concept-drift-detection, online-learning]
related: [data-shifts, adwin, ddm-eddm, online-learning, stream-processing]
updated: 2026-05-02
---

# Concept drift

*A change in the statistical relationship between inputs and outputs over time — the most challenging form of data shift because the model's learned mappings become wrong, not just mismatched to new data.*

## Definition

**Concept drift** occurs when the joint distribution P(X, Y) changes over time — specifically when P(Y | X) changes. The model's learned mapping from inputs to outputs becomes invalid, causing performance degradation even if the input data (P(X)) looks the same.

## Why it matters

Unlike covariate shift (input distribution changes) or prior shift (output distribution changes), concept drift means the *rules have changed*. A fraud detector trained on one attack pattern may correctly identify the input features but predict the wrong label if fraudsters have changed their behaviour.

## Types of concept drift

| Type | Description | Example |
|---|---|---|
| **Gradual** | Slow, continuous change over weeks/months | Evolving consumer preferences |
| **Abrupt** | Sudden step-change | Pandemic changes all shopping behaviour overnight |
| **Recurring / cyclical** | Periodic pattern that repeats | Seasonal demand shifts (summer vs winter) |

## Mechanism — why batch models fail

A model trained on historical data encodes P(Y | X) at training time. If that relationship changes:

1. Model outputs stale mappings.
2. Performance metrics (accuracy, AUC) degrade on live data.
3. No new training = continued degradation.

Batch models require explicit retraining; online models with drift detection can adapt automatically.

## Detection and response

Drift detection algorithms (see [[adwin]], [[ddm-eddm]]) monitor a performance signal (error rate, accuracy) and raise an alert when drift is detected. Common responses:

- **Retrain from scratch** on recent data.
- **Adapt the model** (update weights on new samples).
- **Reset and retrain** after abrupt drift.
- **Ensemble approaches**: combine old and new models weighted by recency.

## Examples in the syllabus

- Concept Drift Detection s. 3: gradual, abrupt, and recurring drift types.
- Online Learning s. 14: concept drift as one of three data shifts.

## Common exam framing

- "What is concept drift and how does it differ from covariate shift?"
- "Give an example of abrupt vs gradual concept drift."
- "Why does a batch-trained model eventually fail in a streaming environment?"

## See also

- [[data-shifts]]
- [[adwin]]
- [[ddm-eddm]]
- [[online-learning]]
- [[stream-processing]]
