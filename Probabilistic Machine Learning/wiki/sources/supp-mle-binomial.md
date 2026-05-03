# Supp — MLE for Binomial Observations

**File:** `raw/text/COM3031_W1_MLE4Binomial.txt`
**Type:** supplementary-note
**Week:** 1
**Concepts introduced:** [[mle]]

## Summary
Derives the MLE for the success probability $\theta$ of a Binomial (coin-flip) model. The MLE is the sample proportion: number of heads divided by total flips.

## Key content

### Setup
- $n$ independent coin flips; $y = \sum_i y_i$ heads observed.
- Likelihood: $p(y|\theta) = \binom{n}{y}\theta^y(1-\theta)^{n-y}$.
- Log-likelihood: $\ell(\theta) = y\log\theta + (n-y)\log(1-\theta) + \text{const}$.

### Derivative and MLE
$$\frac{d\ell}{d\theta} = \frac{y}{\theta} - \frac{n-y}{1-\theta} = 0$$
Cross-multiplying and simplifying:
$$y(1-\theta) = (n-y)\theta \implies y = n\theta$$

### Result
$$\hat{\theta}_{\text{MLE}} = \frac{y}{n}$$
The MLE is the sample proportion: number of successes / total trials.

## Exam notes
- Derivation ⚠️ **examinable** (Week 1).
- Result must be known from memory: $\hat{\theta} = y/n$.
- Log-binomial coefficient drops out in the derivative (constant w.r.t. $\theta$).

## Links to concepts
- [[mle]]: canonical derivation for Binomial
- [[conjugate-priors]]: Bayesian version uses Beta prior ([[supp-beta-binomial]])
- [[map]]: MAP for Binomial uses Beta prior; reduces to MLE when prior is flat
