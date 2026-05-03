# Supp — MAP Estimation for a Univariate Gaussian

**File:** `raw/text/COM3031_W1_MAP4Gaussian.txt`
**Type:** supplementary-note
**Week:** 1
**Concepts introduced:** [[map]], [[bayesian-inference]]

## Summary
Derives the MAP estimate for the mean $\mu$ of a Gaussian likelihood with Gaussian prior on $\mu$. The result is a weighted average of the sample mean and the prior mean, with weights determined by relative precisions (inverse variances).

## Key content

### Setup
- Likelihood: $y_i|\mu \sim \mathcal{N}(\mu, \sigma^2)$, $i=1,\ldots,n$.
- Prior: $\mu \sim \mathcal{N}(\mu_0, \sigma_0^2)$.
- Goal: $\hat{\mu}_{\text{MAP}} = \arg\max_\mu [\log p(\mathbf{y}|\mu) + \log p(\mu)]$.

### Log-posterior
$$\log p(\mu|\mathbf{y}) = -\frac{1}{2\sigma^2}\sum_{i=1}^n(y_i-\mu)^2 - \frac{1}{2\sigma_0^2}(\mu-\mu_0)^2 + \text{const}$$

### Derivative and MAP Condition
$$\frac{\partial}{\partial\mu}\log p(\mu|\mathbf{y}) = \frac{1}{\sigma^2}\left(\sum_{i=1}^n y_i - n\mu\right) + \frac{\mu_0 - \mu}{\sigma_0^2} = 0$$

### MAP Estimate
$$\hat{\mu}_{\text{MAP}} = \frac{n\sigma_0^2}{n\sigma_0^2 + \sigma^2}\cdot\bar{y} + \frac{\sigma^2}{n\sigma_0^2 + \sigma^2}\cdot\mu_0$$
where $\bar{y} = \frac{1}{n}\sum_{i=1}^n y_i$ is the sample mean.

Equivalently, using precisions $\lambda = 1/\sigma^2$ and $\lambda_0 = 1/\sigma_0^2$:
$$\hat{\mu}_{\text{MAP}} = \frac{n\lambda}{\,n\lambda + \lambda_0\,}\bar{y} + \frac{\lambda_0}{n\lambda + \lambda_0}\mu_0$$

### Interpretation
- MAP = weighted average of prior mean and sample mean.
- **No data** ($n=0$): $\hat{\mu}_{\text{MAP}} = \mu_0$ (pure prior).
- **Infinite data** ($n \to \infty$): $\hat{\mu}_{\text{MAP}} \to \bar{y}$ (pure MLE).
- **Strong prior** ($\sigma_0^2 \to 0$): MAP pulled toward $\mu_0$.
- **Weak prior** ($\sigma_0^2 \to \infty$): MAP $\to$ MLE.
- Gaussian–Gaussian is a conjugate pair: posterior is Gaussian (see [[supp-beta-binomial]] for the discrete analogue).

## Exam notes
- MAP derivation for Gaussian (univariate): ⚠️ **examinable**.
- Weighted average interpretation: know which weight belongs to which term.
- Formula sheet: Gaussian pdf **will be given** (Week 1).

## Links to concepts
- [[map]]: canonical derivation
- [[mle]]: limiting case of MAP as $n \to \infty$
- [[conjugate-priors]]: Gaussian–Gaussian conjugacy
- [[bayesian-linear-regression]]: extends this to weights $\mathbf{w}$
