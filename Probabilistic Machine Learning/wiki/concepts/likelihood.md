# Likelihood

**Type:** concept
**Week:** 1
**Related:** [[bayesian-inference]], [[mle]], [[map]]
**Source:** [[lecture-w1]]

## Definition
The likelihood is the probability of observing the data given a specific set of model parameters, treated as a function of the parameters rather than the data.

## Motivation
To learn from data, we need a way to score how well different parameter values explain what we actually observed.

## How it works
For data $\mathcal{D}$ and parameters $\theta$:
$$\mathcal{L}(\theta) = P(\mathcal{D} | \theta)$$
For i.i.d. observations, the joint likelihood is the product of individual likelihoods:
$$\mathcal{L}(\theta) = \prod_{i=1}^n P(x_i | \theta)$$
In practice, we usually work with the log-likelihood to prevent underflow and simplify math:
$$\ell(\theta) = \sum_{i=1}^n \log P(x_i | \theta)$$

## Key derivation
Not applicable; foundational definition.

## Parameters & intuition
- Likelihood is *not* a probability distribution over $\theta$ (it doesn't integrate to 1).
- Higher likelihood means the parameters make the observed data more probable.

## Connections
- Maximising it yields [[mle]].
- Combined with a prior, it gives the posterior in [[bayesian-inference]] and [[map]].

## Exam notes
- Fundamental building block for all inference in the module.
- Formula status: general concept ⚠️
