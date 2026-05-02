---
title: "Topic: Machine learning at scale"
type: topic
sources: []
related: [sgd-all-reduce, communication-patterns, parallel-kmeans, online-learning, batch-vs-online-learning, data-shifts, concept-drift, adwin, ddm-eddm]
updated: 2026-05-02
---

# Topic: Machine learning at scale

*How ML training and inference are distributed, how models adapt to live data, and how drift is detected before models decay.*

## Distributed training

- [[communication-patterns]] — the seven primitives (push, pull, broadcast, reduce, all-reduce, wait, barrier).
- [[sgd-all-reduce]] — distributed minibatch SGD; statistically equivalent to serial; idle time during all-reduce is the bottleneck.
- [[parallel-kmeans]] — MapReduce implementation: map=assign, combine=local sums, reduce=update centroids.

## Online vs batch learning

- [[batch-vs-online-learning]] — full batch (all data, true gradient) vs mini-batch (subset) vs online (one observation, stochastic).
- [[online-learning]] — continuous adaptation; learning rate controls adaptation speed.

## Data drift

- [[data-shifts]] — covariate shift (inputs), prior probability shift (outputs), concept drift (relationship changes).
- [[concept-drift]] — gradual, abrupt, recurring.
- [[adwin]] — adaptive windowing drift detector.
- [[ddm-eddm]] — error-rate statistical drift detectors.

## See also

- [[mapreduce]]
- [[stream-processing]]
- [[event-time-vs-processing-time]]
