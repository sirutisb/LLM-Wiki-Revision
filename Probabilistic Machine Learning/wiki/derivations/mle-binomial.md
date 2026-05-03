# Derivation: MLE for the Binomial Distribution

**Used in:** [[mle]], [[bayesian-inference]], [[conjugate-priors]]
**Source:** [[supp-mle-binomial]]
**Exam status:** ⚠️ Must know — examinable derivation

## Setup
We observe $y$ successes in $n$ independent Bernoulli trials, where each trial has success probability $\theta$.

Likelihood: $p(y|\theta, n) = \binom{n}{y}\theta^y(1-\theta)^{n-y}$

Derive $\hat{\theta}_{\text{MLE}}$.

## Steps

### 1. Write the log-likelihood
$$\ell(\theta) = \log\binom{n}{y} + y\log\theta + (n-y)\log(1-\theta)$$

The first term is constant w.r.t. $\theta$, so:
$$\ell(\theta) \propto y\log\theta + (n-y)\log(1-\theta)$$

### 2. Differentiate and set to zero
$$\frac{d\ell}{d\theta} = \frac{y}{\theta} - \frac{n-y}{1-\theta} = 0$$

### 3. Solve for $\theta$
$$\frac{y}{\theta} = \frac{n-y}{1-\theta}$$
$$y(1-\theta) = (n-y)\theta$$
$$y - y\theta = n\theta - y\theta$$
$$y = n\theta$$

$$\boxed{\hat{\theta}_{\text{MLE}} = \frac{y}{n}}$$

### 4. Verify it's a maximum (second derivative)
$$\frac{d^2\ell}{d\theta^2} = -\frac{y}{\theta^2} - \frac{n-y}{(1-\theta)^2} < 0 \quad \text{for } 0 < \theta < 1$$
Negative second derivative → global maximum.

## Result
$$\hat{\theta}_{\text{MLE}} = \frac{y}{n}$$

The sample proportion: the fraction of successes in $n$ trials.

## Intuition
The MLE is the empirical fraction — the most natural estimate. No prior information is used; if all trials are successes, $\hat{\theta} = 1$ (no shrinkage toward 0.5, unlike Bayesian estimates with non-trivial priors).
