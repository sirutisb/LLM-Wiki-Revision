---
title: "Lecture: Online Learning"
type: lecture
sources: [online-learning]
related: [online-learning, batch-vs-online-learning, data-shifts, concept-drift]
updated: 2026-05-02
---

# Lecture: Online Learning

*From full-batch training through mini-batch to fully online (per-observation) learning — trade-offs of each approach and the three data shifts that make models decay.*

## Slide-by-slide notes

- **(s. 2)** **Gradient descent overview**: learning = minimising a loss surface by following gradients downhill.
- **(s. 3–5)** **Full batch learning**:
  - Uses *all* available data per gradient step → computes the true gradient.
  - Training happens once, *before* deployment (offline).
  - Pros: simpler to reason about; smoother, more consistent convergence.
- **(s. 6)** **Full batch drawbacks**:
  - Data or the problem may not be static (e.g. recommendation systems with drifting preferences → [[concept-drift]]).
  - Retraining with all data becomes increasingly expensive as data grows.
  - All data must fit in memory.
- **(s. 7–8)** **Mini-batch learning**:
  - Uses a *recent subset* of data — less computationally intensive.
  - Older data has less influence on the updated model (incremental/continual learning).
  - Key question: how often to retrain? How much data to include?
  - Cons: batch size choice adds complexity; convergence less stable; smaller batch → higher gradient variance.
- **(s. 9)** **Trade-offs summary**: full batch rarely used in production (only suits tiny datasets); batch size is a critical hyperparameter.
- **(s. 10)** **Streaming data as the extreme case**:
  - Multiple passes over data are no longer possible — one pass only.
  - Data streams may evolve over time → model can become outdated.
  - High speed requirement.
- **(s. 11–12)** **[[online-learning|Online learning]]** (per-observation):
  - Model parameters updated on every new observation.
  - Always adapting to the latest data.
  - Learning rate controls adaptation speed — too high → unstable; too low → slow to adapt.
  - Bad data has *immediate* impact.
  - Equivalent to stochastic gradient descent (one-sample update).
- **(s. 14)** **[[data-shifts|Three types of data shifts]]** that cause model decay:
  - **Covariate shift** — input distribution changes; target (output) unchanged. *Example: face recognition trained pre-pandemic fails on masked faces.*
  - **Prior probability shift** — target distribution changes; inputs unchanged. *Example: flu symptom model during COVID, where underlying flu prevalence changed.*
  - **Concept drift** — the relationship between inputs and outputs changes over time. *Example: fraud patterns evolve after a new attack vector appears.*

## Key takeaways

1. **Three learning modes** — full batch (all data, true gradient), mini-batch (subset, gradient estimate), online (one observation, stochastic update).
2. **Online learning** adapts to change instantly but is sensitive to noise and bad data; learning rate is the key lever.
3. **Data shift ≠ concept drift** — covariate shift (input changes) and prior shift (output distribution changes) are distinct from concept drift (input→output relationship changes). Examiners test these distinctions.
4. **Streaming data forces online learning** — no re-reading, one pass, real-time updates.
5. **Mini-batch is the production default** — balance between computational cost and convergence stability.

## Concepts introduced

- [[online-learning]]
- [[batch-vs-online-learning]]
- [[data-shifts]]
- [[concept-drift]]

## Open questions / things to clarify

- The learning rate scheduling strategies (decay, warmup) are not covered in this deck.
- Evaluation of online models (prequential evaluation) is not mentioned.

## See also

- [[concept-drift]]
- [[sgd-all-reduce]]
- [[stream-processing]]
