---
title: "DDM and EDDM"
type: concept
sources: [concept-drift-detection]
related: [concept-drift, adwin, online-learning]
updated: 2026-05-02
---

# DDM and EDDM

*Two statistical process control–style drift detectors that monitor a classifier's error rate over time, raising warnings and alarms when it deviates significantly from its historical minimum.*

## DDM — Drift Detection Method

### Definition

**DDM** monitors the error rate of a binary classifier to detect concept drift. It compares the current error statistics to the best (lowest) performance observed so far, using standard-deviation thresholds to define warning and change zones.

### Mechanism

At each time step i, DDM tracks:
- **pᵢ** — current instantaneous error rate (proportion of incorrect predictions).
- **sᵢ** — standard deviation of the error rate: sᵢ = √(pᵢ(1 − pᵢ) / i).
- **p_min**, **s_min** — the minimum pᵢ and sᵢ recorded so far (best performance point).

Two thresholds:

| Zone | Condition | Meaning |
|---|---|---|
| **Warning** | pᵢ + sᵢ ≥ p_min + 2 × s_min | Performance degrading — start saving recent data |
| **Change detected** | pᵢ + sᵢ ≥ p_min + 3 × s_min | Drift confirmed — retrain the model |

The 2σ / 3σ structure mirrors statistical process control (SPC) / control charts.

### Why it works

If the data distribution is stationary, the error rate should stabilise around some minimum. A significant upward deviation signals that the underlying distribution (or input→output relationship) has changed.

## EDDM — Early Drift Detection Method

**EDDM** is a variant of DDM designed to detect gradual drift *earlier* than DDM. Instead of tracking the absolute error rate, EDDM focuses on the *distance between consecutive errors* — gradual drift compresses these distances before the overall error rate visibly rises.

EDDM is better suited for slow, gradual drifts; DDM catches abrupt drifts more reliably.

## Trade-offs

| | DDM | EDDM | ADWIN |
|---|---|---|---|
| Drift type strengths | Abrupt | Gradual | Both |
| Requires classifier | Yes (binary output) | Yes | No (any metric) |
| Tuning | None (fixed 2σ/3σ) | None | None |
| Memory | Low | Low | High (stores window) |

## Examples in the syllabus

- Concept Drift Detection s. 6: DDM formula and thresholds.
- s. 4: ADWIN, DDM, EDDM listed as the three algorithms covered.

## Common exam framing

- "Describe how DDM detects concept drift. What are its warning and change thresholds?"
- "How does EDDM differ from DDM in its approach to detecting gradual drift?"
- "What does p_min represent in DDM and why is it used as the baseline?"

## See also

- [[concept-drift]]
- [[adwin]]
- [[online-learning]]
