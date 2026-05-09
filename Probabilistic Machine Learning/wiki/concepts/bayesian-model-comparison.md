# Bayesian Model Comparison

**Type:** framework
**Week:** 3
**Related:** [[laplace-approximation]], [[bic]], [[bayesian-inference]]
**Source:** [[lecture-w3]]

## Definition
Bayesian model comparison is a framework for evaluating and selecting between different models based on their marginal likelihood (or model evidence), automatically penalising overly complex models.

## Motivation
Maximum Likelihood Estimation (MLE) always favours more complex models, leading to overfitting. Bayesian comparison integrates out the parameters, rewarding models that allocate their probability mass efficiently without unnecessary flexibility.

## How it works
For models $M_1, M_2$, we compare their marginal likelihoods:
$$P(\mathcal{D} | M_i) = \int P(\mathcal{D} | \theta, M_i) P(\theta | M_i) d\theta$$
We can compute the Bayes Factor:
$$K = \frac{P(\mathcal{D} | M_1)}{P(\mathcal{D} | M_2)}$$
If $K > 1$, $M_1$ is preferred.

## Key derivation
Not applicable; framework concept.

## Parameters & intuition
- **Occam's Razor:** Complex models can explain many datasets but spread their prior mass thinly. Simple models concentrate their mass. The marginal likelihood naturally selects the simplest model that explains the data well.

## Connections
- Often intractable to compute exactly, so we use approximations like [[laplace-approximation]] or [[bic]].

## Exam notes
- Understand the conceptual argument for why Bayesian evidence penalises complexity.
- Formula status: conceptual ⚠️
