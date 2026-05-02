---
title: "Data shifts"
type: concept
sources: [online-learning, concept-drift-detection]
related: [online-learning, concept-drift, batch-vs-online-learning]
updated: 2026-05-02
---

# Data shifts

*Three distinct ways a deployed ML model's world can change, each requiring a different response: the input distribution shifts, the output distribution shifts, or the input-output relationship itself changes.*

## Definition

A **data shift** is a change in the statistical properties of data after a model has been trained, causing the model's performance to degrade. There are three types:

### Covariate shift
The distribution of **input variables** changes; the target variable distribution (given inputs) remains the same.

> Example: a face recognition model trained on unmasked faces encounters masked faces during a pandemic. The input images look systematically different, but the relationship "this face belongs to person X" hasn't changed.

### Prior probability shift
The distribution of **target variables** changes; input distributions remain the same.

> Example: a flu prediction model trained on pre-pandemic symptom data encounters a world where the base rate of flu has changed dramatically due to COVID. The symptoms still mean the same things, but the underlying probability of having flu is different.

### Concept drift
The **relationship between inputs and outputs** changes over time.

> Example: fraud detection — what constitutes suspicious behaviour changes as attackers evolve their methods. The same transaction patterns that weren't fraud yesterday may be fraud today.

## Why the distinction matters

The correct response differs:

| Shift type | Root cause | Response |
|---|---|---|
| Covariate | Input distribution changed | Collect new representative training data |
| Prior | Base rates changed | Update priors / class weights |
| Concept drift | Feature→label mapping changed | Retrain / use drift detection + adaptation |

Confusing them leads to the wrong fix. A model that fails due to covariate shift may recover by normalising inputs; a model failing due to concept drift needs new labelled examples.

## Examples in the syllabus

- Online Learning s. 14 / Concept Drift Detection s. 2: all three types defined with examples.

## Common exam framing

- "Distinguish covariate shift, prior probability shift, and concept drift. Give an example of each."
- "A spam filter's accuracy drops over time. What type of data shift is most likely responsible?"

## See also

- [[concept-drift]]
- [[online-learning]]
- [[batch-vs-online-learning]]
