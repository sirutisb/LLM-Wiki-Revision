---
title: "ADWIN"
type: concept
sources: [concept-drift-detection]
related: [concept-drift, ddm-eddm, online-learning]
updated: 2026-05-02
---

# ADWIN

*ADaptive WINdowing — a concept drift detector that maintains a variable-size window over the data stream, growing during stability and shrinking when a change is detected.*

## Definition

**ADWIN** (ADaptive WINdowing) is a parameter-free drift detection algorithm that dynamically adjusts the size of its observation window based on whether the data distribution is stable or changing.

## Why it matters

Fixed-size windows are a poor fit for streaming data — too small and you miss gradual drift, too large and you react too slowly to abrupt drift. ADWIN adapts: it uses a large window when the stream is stable (for better statistical estimates) and shrinks the window when drift occurs (discarding stale data).

## Mechanism

ADWIN maintains a window W of the most recent data points:

1. **Stability**: if the statistics within W are consistent (no sub-window shows a significantly different distribution), the window grows — new data appended.
2. **Drift detection**: ADWIN continuously tests whether any sub-window of W has a statistically different mean from the rest. If the difference exceeds a threshold → drift detected.
3. **Shrink**: the older portion of the window (before the changepoint) is discarded. The window resets to the recent data.

```
Stable stream:  W grows  →  [....older data....newer data]
Drift occurs:   W shrinks → [newer data only]
                            ↑ changepoint detected here
```

ADWIN does not require a pre-set window size — the window length is a *result* of the algorithm, not a parameter.

## Trade-offs

- **+** No window size to tune.
- **+** Handles both abrupt and gradual drift.
- **+** Provides statistical guarantees on false positive/negative rates.
- **−** Maintains the full window in memory — for very long stable periods the window can be large.
- **−** Computationally more expensive than simpler detectors (DDM).

## Examples in the syllabus

- Concept Drift Detection s. 5: ADWIN described as growing when stable, shrinking when data changes.

## Common exam framing

- "How does ADWIN detect concept drift? What happens to the window when drift is detected?"
- "Why does ADWIN not require a fixed window size parameter?"

## See also

- [[concept-drift]]
- [[ddm-eddm]]
- [[online-learning]]
