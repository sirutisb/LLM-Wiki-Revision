# Derivation: MLE for the Gaussian Distribution

**Used in:** [[mle]], [[linear-regression]], [[bayesian-inference]]
**Source:** [[supp-mle-gaussian]]
**Exam status:** ⚠️ Univariate derivation EXAMINABLE; ✅ Formulas GIVEN (W1)

## Setup
Given $n$ i.i.d. observations $x_1, \ldots, x_n \sim \mathcal{N}(\mu, \sigma^2)$.
Derive MLE estimates $\hat{\mu}$ and $\hat{\sigma}^2$.

Note: Univariate derivation is examinable (Week 1); **multivariate derivations are NOT examinable** for Weeks 1-3.

Parameters: $\boldsymbol{\theta} = (\mu, \sigma^2)$.

## Steps

### 1. Write the likelihood
$$p(\mathbf{x}|\mu,\sigma^2) = \prod_{i=1}^n \frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left(-\frac{(x_i-\mu)^2}{2\sigma^2}\right)$$

### 2. Take the log-likelihood
$$\ell(\mu,\sigma^2) = -\frac{n}{2}\log(2\pi) - \frac{n}{2}\log\sigma^2 - \frac{1}{2\sigma^2}\sum_{i=1}^n(x_i-\mu)^2$$

### 3. Optimise for $\mu$ (differentiate and set to zero)
$$\frac{\partial\ell}{\partial\mu} = \frac{1}{\sigma^2}\sum_{i=1}^n(x_i-\mu) = 0$$
$$\sum_{i=1}^n x_i - n\mu = 0$$

$$\boxed{\hat{\mu}_{\text{MLE}} = \frac{1}{n}\sum_{i=1}^n x_i}$$

### 4. Optimise for $\sigma^2$ (differentiate and set to zero)
Let $v = \sigma^2$:
$$\frac{\partial\ell}{\partial v} = -\frac{n}{2v} + \frac{1}{2v^2}\sum_{i=1}^n(x_i-\hat{\mu})^2 = 0$$
$$n = \frac{1}{v}\sum_{i=1}^n(x_i-\hat{\mu})^2$$

$$\boxed{\hat{\sigma}^2_{\text{MLE}} = \frac{1}{n}\sum_{i=1}^n(x_i-\hat{\mu})^2}$$

## Result

$$\hat{\mu}_{\text{MLE}} = \bar{x} = \frac{1}{n}\sum_i x_i \qquad \hat{\sigma}^2_{\text{MLE}} = \frac{1}{n}\sum_i (x_i - \bar{x})^2$$

Note: $\hat{\sigma}^2_{\text{MLE}}$ divides by $n$ (biased — underestimates true variance). The unbiased estimator divides by $n-1$.

## Intuition
- MLE for $\mu$: minimises mean squared deviation from data — the sample mean is the "centre of mass" of the data.
- MLE for $\sigma^2$: average squared deviation from the estimated mean. Biased because we estimated $\mu$ from the same data.
