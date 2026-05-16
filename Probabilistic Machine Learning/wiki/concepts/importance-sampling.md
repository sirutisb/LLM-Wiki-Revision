# Importance Sampling

**Type:** algorithm
**Week:** 5
**Related:** [[mcmc]], [[rejection-sampling]], [[monte-carlo-integration]], [[bayesian-inference]]
**Source:** [[lecture-w5]]

## Definition
Importance sampling is a Monte Carlo technique that estimates expectations under a target distribution $p^*(\theta)$ by drawing samples from a proposal distribution $q(\theta)$ and reweighting them by importance weights.

## Motivation
Rejection sampling discards samples — wasteful if the acceptance rate is low. Importance sampling never throws samples away; instead, it reweights all of them. Every sample contributes, but samples from low-probability regions under $p^*$ get low weight.

## How it works

### Estimating Expectations
Goal: estimate $\mathbb{E}_{p^*}[f(\theta)] = \int f(\theta)p^*(\theta)\,d\theta$.

Rewrite:
$$\mathbb{E}_{p^*}[f(\theta)] = \int f(\theta)\frac{p^*(\theta)}{q(\theta)}q(\theta)\,d\theta = \mathbb{E}_q\left[f(\theta)w(\theta)\right]$$

where $w(\theta) = p^*(\theta)/q(\theta)$ is the **importance weight**.

### Importance Sampling Estimator
Draw $\theta_1, \ldots, \theta_S \sim q(\theta)$:
$$\hat{\mu} = \frac{1}{S}\sum_{s=1}^S f(\theta_s)w(\theta_s)$$

### Self-Normalised Importance Sampling
When $p^*(\theta) = \tilde{p}(\theta)/Z$ is unnormalised:
$$\hat{\mu} = \frac{\sum_s f(\theta_s)\tilde{w}(\theta_s)}{\sum_s \tilde{w}(\theta_s)}, \qquad \tilde{w}(\theta_s) = \frac{\tilde{p}(\theta_s)}{q(\theta_s)}$$
Normalises the weights to sum to 1 — does not require knowing $Z$.

### Effective Sample Size (ESS)
$$\text{ESS} = \frac{(\sum_s w_s)^2}{\sum_s w_s^2} \leq S$$
Measures how many equally-weighted samples the importance-weighted estimate is worth. Low ESS = poor proposal.

### High-Dimensional Problem
As $d$ increases, the proposal $q$ covers regions where $p^*$ has almost no mass — a few samples get very large weights, the rest get near-zero weights. ESS collapses exponentially. Importance sampling fails in high dimensions for the same reason as rejection sampling.

## Key derivation
⚠️ *Derivation not examinable*

The estimator is unbiased because $\mathbb{E}_q[f(\theta)w(\theta)] = \int f(\theta)\frac{p^*(\theta)}{q(\theta)}q(\theta)d\theta = \mathbb{E}_{p^*}[f(\theta)]$.

## Parameters & intuition
- $q$ should cover the support of $p^*f$: if $f(\theta)p^*(\theta) > 0$ but $q(\theta) = 0$, those regions are missed.
- Heavier-tailed proposal than $p^*$: helps avoid missing important regions.
- Variance: minimised when $q \propto |f|p^*$.

## Connections
- [[rejection-sampling]]: also uses $q$; rejects rather than reweights; produces independent samples.
- [[monte-carlo-integration]]: importance sampling provides variance-reduced Monte Carlo estimates.
- [[mcmc]]: preferred over IS in high dimensions; trades independence for scalability.

## Exam notes
- Know the importance weight definition and self-normalised estimator.
- Know why IS fails in high dimensions (weight degeneracy).
- Compare IS vs rejection sampling vs MCMC.
- Formula status: no formula sheet for Week 5 ⚠️
