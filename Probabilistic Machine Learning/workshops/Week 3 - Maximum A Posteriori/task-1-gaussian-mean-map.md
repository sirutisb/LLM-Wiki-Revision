# Task 1 — MAP for the Mean of a Gaussian (with known variance)

**Source:** `3031_MAP_Workshop.pdf` Q1, `Solution Q1.ipynb`
**Concepts tested:** [[map]], [[mle]], [[bayesian-inference]], [[conjugate-priors]], [[mcmc]]
**Related derivation:** [[map-gaussian]]

---

## The question (paraphrased)

We are given data $\mathbf{y} = (y_1, \dots, y_n)^T$ assumed to be drawn i.i.d. from a Normal distribution.

(a) Estimate the mean and variance by maximising the likelihood (i.e. compute the MLEs).

(b) Now place a prior on the mean: $\mu \sim \mathcal{N}(\mu_0, \sigma_0^2)$. Estimate the posterior $p(\mu \mid \mathbf{y})$ in two ways:
  - numerically, using MCMC via PyMC, and
  - analytically, exploiting Gaussian–Gaussian conjugacy (variance treated as known).

Then experiment with $\mu_0$ and $\sigma_0^2$ to see how the prior shapes the posterior.

This question is the canonical Gaussian conjugate example — exactly the worked derivation in [[supp-map-gaussian]].

---

## Why MAP rather than MLE?

[[mle]] picks the single $\mu$ that makes the observed data most probable. It treats $\mu$ as a fixed unknown number and ignores any prior knowledge.

[[map]] treats $\mu$ as a random variable. Bayes' theorem lets us combine
$$
\underbrace{p(\mu \mid \mathbf{y})}_{\text{posterior}} \propto \underbrace{p(\mathbf{y} \mid \mu)}_{\text{likelihood}} \cdot \underbrace{p(\mu)}_{\text{prior}}
$$
and the MAP estimate is the mode of that posterior — the most likely $\mu$ in light of *both* the data and our prior beliefs.

The role of the prior here is twofold:
1. It expresses what we believed about $\mu$ before seeing the data (centre $\mu_0$, spread $\sigma_0^2$).
2. It regularises: a tight prior pulls the estimate toward $\mu_0$ when data are scarce; a loose prior lets the data dominate.

When the prior is flat (very large $\sigma_0^2$), MAP collapses back onto MLE — the prior contributes nothing.

---

## Cell-by-cell walkthrough

### Cell 1 — imports

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import norm
import pymc as pm
```

`pymc` is the probabilistic-programming library that runs MCMC under the hood. We will use it to *sample* from $p(\mu \mid \mathbf{y})$ rather than work it out on paper. `scipy.stats.norm` is used later to plot the analytical posterior PDF.

### Cell 2 — generate synthetic data

```python
data = np.random.normal(loc=3, scale=2, size=100000)
```

We fabricate ground-truth data: $y_i \sim \mathcal{N}(3, 2^2)$. Because we *know* the truth, we can later check whether MLE/MAP recover $\mu = 3$ and $\sigma^2 = 4$. Using a large $n=100{,}000$ makes the likelihood so strong that priors will barely matter — useful for sanity-checking, less useful for studying prior influence (more on this below).

### Cell 3 — MLE for $\mu$ and $\sigma^2$

```python
def mle_estimation(y):
    n = len(y)
    mu = sum(y) / n
    sigma2 = sum((yi - mu) ** 2 for yi in y) / n
    return mu, sigma2
```

These are the closed-form MLEs for a Gaussian (see [[mle-gaussian]]):
$$
\hat\mu_{\text{MLE}} = \frac{1}{n}\sum_{i=1}^n y_i, \qquad
\hat\sigma^2_{\text{MLE}} = \frac{1}{n}\sum_{i=1}^n (y_i - \hat\mu)^2.
$$
Note the variance MLE divides by $n$, not $n-1$ — it is biased but it *is* the maximum-likelihood estimate. The output is approximately $(3.00, 4.01)$, recovering the truth.

We use this MLE variance later as the "known" $\sigma^2$ in the conjugate-Gaussian update — a pragmatic shortcut (the question says "with known variance" but does not give one).

### Cell 4 — set the prior and run PyMC

```python
mu0 = 0
sigma0_squared = 10

with pm.Model() as model:
    mu = pm.Normal("mu", mu=mu0, sigma=np.sqrt(sigma0_squared))
    sigma = np.sqrt(mle_variance)
    likelihood = pm.Normal("likelihood", mu=mu, sigma=sigma, observed=data)
    trace = pm.sample(1000, random_seed=42)
```

What is happening intuitively:

1. `pm.Normal("mu", ...)` — declares that $\mu$ is a random variable with prior $\mathcal{N}(\mu_0, \sigma_0^2) = \mathcal{N}(0, 10)$. We chose $\mu_0 = 0$ even though the truth is $3$; this lets us see the data overcome a slightly biased prior.
2. `pm.Normal("likelihood", ..., observed=data)` — declares that each observation comes from $\mathcal{N}(\mu, \sigma^2)$, *clamped* to the observed values.
3. `pm.sample(...)` — runs an MCMC sampler (NUTS by default) that draws samples from $p(\mu \mid \mathbf{y})$. We never compute the posterior in closed form; we just get many samples whose histogram approximates it. See [[mcmc]].

The output summary shows posterior mean $\approx 2.998$, std $\approx 0.006$. The posterior is *vastly* tighter than the prior because $n = 100{,}000$ data points dominate.

### Cell 5 — diagnostics: trace plot

```python
pm.plot_trace(trace)
```

Two plots per parameter:

- **Posterior density (left):** should be unimodal and bell-shaped. The peak is the MAP estimate.
- **Trace (right):** the chain of sampled values over iterations. We want it to look like white noise ("hairy caterpillar") around a stable mean — that is the visual signature of convergence. Trends, drift, or sticking indicate the chain has not mixed well.

### Cell 7 — extract numerical posterior summaries

```python
pymc_posterior_mean = summary.loc['mu', 'mean']
pymc_posterior_var  = np.square(summary.loc['mu', 'sd'])
```

The MCMC samples give us $\hat E[\mu \mid \mathbf{y}]$ and $\hat{\text{Var}}[\mu \mid \mathbf{y}]$ as Monte Carlo averages.

### Cell 8 — analytical derivation (markdown)

This re-derives the conjugate-Gaussian posterior. The key result: with a Gaussian prior $\mu \sim \mathcal{N}(\mu_0, \sigma_0^2)$ and Gaussian likelihood with known variance $\sigma^2$, the posterior is again Gaussian (this is what *conjugate* means — see [[conjugate-priors]]):

$$
\mu \mid \mathbf{y} \sim \mathcal{N}\!\left(\mu_n, \sigma_n^2\right)
$$
where
$$
\sigma_n^2 = \frac{1}{\dfrac{n}{\sigma^2} + \dfrac{1}{\sigma_0^2}}, \qquad
\mu_n = \sigma_n^2 \left( \frac{n\bar y}{\sigma^2} + \frac{\mu_0}{\sigma_0^2}\right).
$$

**Intuition for the precision-weighted mean.** Precision is the reciprocal of variance. The posterior mean is a weighted average of the prior mean and the sample mean, with weights given by their precisions:
- Prior precision: $1/\sigma_0^2$.
- Data precision: $n/\sigma^2$ (more data $\Rightarrow$ more precise estimate of $\mu$).

When $n$ is large (or the prior is vague, $\sigma_0^2 \to \infty$), the data precision dominates and $\mu_n \to \bar y$, i.e. MAP $\to$ MLE. When $n$ is small or the prior is tight ($\sigma_0^2$ small), the prior pulls the estimate toward $\mu_0$.

For a Gaussian, the posterior mode equals the posterior mean, so $\mu_n$ *is* the MAP estimate.

### Cell 9 — analytical posterior in code

```python
def analytical_posterior(data, mu0, sigma0_squared, known_variance):
    n = len(data)
    data_mean = np.mean(data)
    posterior_variance = 1 / (n / known_variance + 1 / sigma0_squared)
    posterior_mean = posterior_variance * (data_mean * n / known_variance + mu0 / sigma0_squared)
    return posterior_mean, posterior_variance
```

Direct translation of the formulas above. Output for our run: posterior mean $\approx 2.998$, variance $\approx 4 \times 10^{-5}$ — essentially identical to the MCMC result, validating both methods.

### Cell 10 — overlay plot

```python
plt.hist(pm_posterior_samples, bins=30, density=True, ...)
plt.plot(x, norm.pdf(x, loc=posterior_mean, scale=np.sqrt(posterior_variance)), ...)
```

The MCMC histogram should sit on top of the red analytical Gaussian PDF. They agree because the model has a closed-form posterior; MCMC was unnecessary here but is a valuable sanity check before tackling models that *do not* have one (e.g. those needing [[laplace-approximation]] or [[variational-inference]]).

---

## Effect of $\mu_0$ and $\sigma_0^2$ — the core insight

Trying different priors:

- **Vague prior** ($\sigma_0^2$ large, e.g. $10^6$): posterior is essentially the likelihood. MAP $\approx$ MLE.
- **Tight, accurate prior** ($\mu_0 = 3, \sigma_0^2 = 0.01$): posterior shrinks even further around the truth.
- **Tight, wrong prior** ($\mu_0 = 0, \sigma_0^2 = 0.01$, with small $n$): posterior gets pulled toward $0$, biasing the estimate. With large $n$, the data eventually wash this out.

This is the whole point of MAP: **the prior matters most when data are few or noisy, and progressively less as $n$ grows**.

---

## What to take away for the exam

- **Setup:** Gaussian likelihood $\times$ Gaussian prior $\Rightarrow$ Gaussian posterior. This is *the* canonical conjugate pair. See [[conjugate-priors]] and [[map-gaussian]].
- **Posterior parameters (memorise — no formula sheet from Week 3 onwards):**
  $$
  \sigma_n^2 = \left(\tfrac{n}{\sigma^2} + \tfrac{1}{\sigma_0^2}\right)^{-1}, \qquad
  \mu_n = \sigma_n^2 \left(\tfrac{n\bar y}{\sigma^2} + \tfrac{\mu_0}{\sigma_0^2}\right).
  $$
- **Precision-weighted average:** the posterior mean is a weighted average of prior mean and sample mean, weighted by their precisions. State this in words on the exam — examiners love it.
- **MAP vs MLE:** MAP = mode of posterior; MLE = maximiser of likelihood. MAP $\to$ MLE in the limit of a flat (improper uniform) prior or as $n \to \infty$.
- **Why use MCMC if there is a closed form?** Practice: in problems where conjugacy fails, MCMC (or [[variational-inference]] or [[laplace-approximation]]) is all we have. This question lets us validate MCMC against the known answer.
- **Diagnostic literacy:** know to read trace plots — bell-shaped posterior + hairy-caterpillar trace = healthy chain.
- **Conceptual exam hook:** be ready to say what happens when (i) $n \to \infty$, (ii) $\sigma_0^2 \to \infty$, (iii) $\sigma_0^2 \to 0$. These are favourite limits for short-answer questions.
