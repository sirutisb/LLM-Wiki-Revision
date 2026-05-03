# Supp — MLE for a Gaussian Distribution

**File:** `raw/text/COM3031_W1_MLE4Gaussian.txt`
**Type:** supplementary-note
**Week:** 1
**Concepts introduced:** [[mle]]

## Summary
Derives MLE estimates for both the mean $\mu$ and variance $\sigma^2$ of a Gaussian distribution from i.i.d. samples. Mean MLE = sample mean; variance MLE = biased sample variance (divide by $N$, not $N-1$).

## Key content

### Setup
- $\mathcal{D} = \{y_1,\ldots,y_N\}$ i.i.d. from $\mathcal{N}(\mu, \sigma^2)$.
- Log-likelihood:
$$\ell(\mu, \sigma^2) = \sum_{i=1}^N\left[-\frac{1}{2}\log(2\pi\sigma^2) - \frac{(y_i-\mu)^2}{2\sigma^2}\right]$$

### MLE for the Mean
$$\frac{\partial\ell}{\partial\mu} = \sum_{i=1}^N\frac{y_i - \mu}{\sigma^2} = 0 \implies \hat{\mu}_{\text{MLE}} = \frac{1}{N}\sum_{i=1}^N y_i$$

### MLE for the Variance
$$\frac{\partial\ell}{\partial\sigma^2} = -\frac{N}{2\sigma^2} + \frac{1}{2(\sigma^2)^2}\sum_{i=1}^N(y_i-\mu)^2 = 0 \implies \hat{\sigma}^2_{\text{MLE}} = \frac{1}{N}\sum_{i=1}^N(y_i - \hat{\mu})^2$$

### Results
$$\hat{\mu}_{\text{MLE}} = \frac{1}{N}\sum_{i=1}^N y_i \qquad \hat{\sigma}^2_{\text{MLE}} = \frac{1}{N}\sum_{i=1}^N(y_i - \hat{\mu})^2$$

### Interpretation
- MLE for mean = sample mean (centre of the data).
- MLE for variance = average squared deviation (biased estimator; unbiased uses $N-1$).
- MLE = "parameters making the observed data most probable".
- Directly links to least squares regression (minimising $\sum(y_i-\mu)^2$ is the same as maximising the Gaussian log-likelihood for fixed $\sigma^2$).

## Exam notes
- MLE derivation for Gaussian (univariate): ⚠️ **examinable**.
- Both partial derivatives must be computed and set to zero.
- Formula sheet: Gaussian pdf **will be given** (Week 1).

## Links to concepts
- [[mle]]: canonical derivation for Gaussian
- [[map]]: Bayesian version → adds prior term ([[supp-map-gaussian]])
- [[linear-regression]]: Gaussian MLE = OLS
