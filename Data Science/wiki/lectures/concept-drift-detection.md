---
title: "Lecture: Concept Drift Detection"
type: lecture
sources: [concept-drift-detection]
related: [concept-drift, adwin, ddm-eddm, online-learning, data-shifts]
updated: 2026-05-02
---

# Lecture: Concept Drift Detection

*Streaming data drifts — detecting when it does and how to respond. Three algorithms: ADWIN (adaptive windowing), DDM (error-rate monitoring), EDDM (early detection variant).*

## Slide-by-slide notes

- **(s. 2)** **Online learning recap — three data shifts**:
  - Covariate shift: input distribution changes.
  - Prior probability shift: target distribution changes.
  - Concept drift: input→output relationship changes. *(See [[data-shifts]].)*
- **(s. 3)** **[[concept-drift|Concept drift]] characteristics**:
  - Streaming data is dynamic — underlying statistical characteristics *will* change.
  - **Gradual drift** — slow cultural or economic changes (e.g. user preference evolution).
  - **Abrupt drift** — sudden change (e.g. pandemic disrupts all patterns overnight).
  - **Recurring / cyclical drift** — seasonal patterns that repeat.
  - Batch learner models become outdated and must be retrained.
- **(s. 4)** **Drift detection algorithms** covered:
  - [[adwin|ADWIN]] (ADaptive WINdowing)
  - [[ddm-eddm|DDM]] (Drift Detection Method)
  - [[ddm-eddm|EDDM]] (Early Drift Detection Method)
- **(s. 5)** **[[adwin|ADWIN]]**:
  - Maintains a variable-size window over the stream.
  - **Grows** the window when no change is apparent (accumulating more data for stable estimates).
  - **Shrinks** the window when the data changes (discards older, stale data points).
  - Retains only the most recent relevant data.
- **(s. 6)** **[[ddm-eddm|DDM]]**:
  - Works with any binary-output classifier (correct/incorrect prediction).
  - Tracks error rate pᵢ and standard deviation sᵢ at each time step i.
  - Also tracks the minimum recorded values p_min and s_min.
  - **Warning zone**: pᵢ + sᵢ ≥ p_min + 2 × s_min
  - **Change detected**: pᵢ + sᵢ ≥ p_min + 3 × s_min
  - The 2σ / 3σ thresholds mirror statistical process control.
- **(s. 7 implied)** **[[ddm-eddm|EDDM]]** — an extension of DDM designed to detect gradual drift *earlier*, before DDM's thresholds are crossed.

## Key takeaways

1. **Concept drift is inevitable** in live streaming systems — gradual, abrupt, or cyclical.
2. **ADWIN** adapts its window size dynamically — no fixed window size to tune. Grows during stability, shrinks on drift.
3. **DDM** uses error rate statistics with explicit 2σ warning and 3σ change thresholds — straightforward to implement alongside any classifier.
4. **EDDM** extends DDM for earlier detection of gradual drifts.
5. **Detecting drift is the first step** — the response (retrain, adapt, reset) is a separate design decision.

## Concepts introduced

- [[concept-drift]]
- [[adwin]]
- [[ddm-eddm]]

## Open questions / things to clarify

- EDDM specifics (the metric it tracks differently from DDM) are not detailed in the extracted text — check the raw slide images.
- The lecture doesn't cover the response strategy after drift is detected — Online Learning s. 7 mentions mini-batch retraining as one approach.

## See also

- [[data-shifts]]
- [[online-learning]]
- [[stream-processing]]
