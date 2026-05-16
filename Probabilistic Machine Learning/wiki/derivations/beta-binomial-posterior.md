# Derivation: Beta-Binomial Posterior Update

**Used in:** [[conjugate-priors]], [[bayesian-inference]], [[map]]
**Source:** [[supp-beta-binomial]]
**Exam status:** ⚠️ *Derivation examinable* (univariate) / ✅ *Formula sheet provided*

## Setup
Prior: $\theta \sim \text{Beta}(\alpha, \beta)$
Likelihood: $y | \theta \sim \text{Binomial}(n, \theta)$ — observe $y$ successes in $n$ trials.

Derive the posterior $p(\theta|y, n)$.

Recall:
$$\text{Beta}(\theta; \alpha, \beta) = \frac{\theta^{\alpha-1}(1-\theta)^{\beta-1}}{B(\alpha,\beta)}$$

## Steps

### 1. Apply Bayes' rule
$$p(\theta|y) \propto p(y|\theta)\,p(\theta)$$

### 2. Substitute likelihood and prior
$$p(y|\theta) = \binom{n}{y}\theta^y(1-\theta)^{n-y}$$
$$p(\theta) \propto \theta^{\alpha-1}(1-\theta)^{\beta-1}$$

So:
$$p(\theta|y) \propto \theta^y(1-\theta)^{n-y} \cdot \theta^{\alpha-1}(1-\theta)^{\beta-1}$$
$$= \theta^{(\alpha+y)-1}(1-\theta)^{(\beta+n-y)-1}$$

### 3. Identify the posterior
This is proportional to a Beta distribution with updated parameters:
$$p(\theta|y) = \text{Beta}(\alpha + y,\; \beta + n - y)$$

$$\boxed{p(\theta|y,n) = \text{Beta}(\alpha + y,\; \beta + n - y)}$$

## Result
| Quantity | Value |
|---------|-------|
| Prior | $\text{Beta}(\alpha, \beta)$ |
| Posterior | $\text{Beta}(\alpha + y,\; \beta + n - y)$ |
| Posterior mean | $\dfrac{\alpha + y}{\alpha + \beta + n}$ |
| MAP estimate | $\dfrac{\alpha + y - 1}{\alpha + \beta + n - 2}$ (mode of Beta) |

## Intuition
- Each observed success ($y$) increments $\alpha$; each failure ($n-y$) increments $\beta$.
- Prior $\alpha, \beta$ act as "pseudo-counts" of prior successes and failures.
- Posterior mean interpolates between prior mean $\alpha/(\alpha+\beta)$ and MLE $y/n$.
- As $n \to \infty$: posterior concentrates at $y/n$ (data dominates prior).
- **Beta is conjugate to Binomial**: the posterior is in the same family as the prior.
