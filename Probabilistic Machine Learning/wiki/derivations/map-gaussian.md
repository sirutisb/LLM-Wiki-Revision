# Derivation: MAP Estimate for Gaussian with Gaussian Prior

**Used in:** [[map]], [[bayesian-inference]], [[bayesian-linear-regression]]
**Source:** [[supp-map-gaussian]]
**Exam status:** ⚠️ Derivation examinable / ✅ Formula given

## Setup
Observations $x_1, \ldots, x_n \sim \mathcal{N}(\mu, \sigma^2)$ with known variance $\sigma^2$.
Prior: $\mu \sim \mathcal{N}(\mu_0, \sigma_0^2)$.

Derive $\hat{\mu}_{\text{MAP}} = \arg\max_\mu p(\mu|\mathbf{x})$.

## Steps

### 1. Write the log-posterior
$$\log p(\mu|\mathbf{x}) = \log p(\mathbf{x}|\mu) + \log p(\mu) + \text{const}$$

$$= -\frac{1}{2\sigma^2}\sum_{i=1}^n(x_i-\mu)^2 - \frac{1}{2\sigma_0^2}(\mu-\mu_0)^2 + \text{const}$$

### 2. Expand and collect terms in $\mu$
$$= -\frac{1}{2}\left[\frac{n}{\sigma^2}\mu^2 - \frac{2\sum x_i}{\sigma^2}\mu + \frac{1}{\sigma_0^2}\mu^2 - \frac{2\mu_0}{\sigma_0^2}\mu\right] + \text{const}$$

$$= -\frac{1}{2}\left[\left(\frac{n}{\sigma^2} + \frac{1}{\sigma_0^2}\right)\mu^2 - 2\left(\frac{\bar{x}n}{\sigma^2} + \frac{\mu_0}{\sigma_0^2}\right)\mu\right] + \text{const}$$

This is a quadratic in $\mu$ (negative, so a maximum exists).

### 3. Differentiate and set to zero
$$\frac{d}{d\mu}\log p(\mu|\mathbf{x}) = -\left(\frac{n}{\sigma^2} + \frac{1}{\sigma_0^2}\right)\mu + \left(\frac{n\bar{x}}{\sigma^2} + \frac{\mu_0}{\sigma_0^2}\right) = 0$$

### 4. Solve for $\hat{\mu}_{\text{MAP}}$
$$\hat{\mu}_{\text{MAP}} = \frac{\frac{n\bar{x}}{\sigma^2} + \frac{\mu_0}{\sigma_0^2}}{\frac{n}{\sigma^2} + \frac{1}{\sigma_0^2}}$$

$$\boxed{\hat{\mu}_{\text{MAP}} = \frac{n\sigma_0^2\bar{x} + \sigma^2\mu_0}{n\sigma_0^2 + \sigma^2}}$$

## Result
$$\hat{\mu}_{\text{MAP}} = \frac{n\sigma_0^2}{n\sigma_0^2 + \sigma^2}\bar{x} + \frac{\sigma^2}{n\sigma_0^2 + \sigma^2}\mu_0$$

This is a **weighted average** of the sample mean $\bar{x}$ and the prior mean $\mu_0$.

## Intuition
- Weights are determined by relative precision (inverse variance).
- Large $n$ or small $\sigma^2$ (precise data): MAP → MLE ($\bar{x}$).
- Small $n$ or large $\sigma^2$ (noisy data): MAP → prior mean ($\mu_0$).
- Strong prior ($\sigma_0^2$ small): MAP pulled toward $\mu_0$.
- As $n \to \infty$: prior is washed out; MAP → $\bar{x}$.
