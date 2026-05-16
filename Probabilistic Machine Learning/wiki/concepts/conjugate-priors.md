# Conjugate Priors

**Type:** principle
**Week:** 1
**Related:** [[bayesian-inference]], [[mle]], [[map]]
**Source:** [[lecture-w1]], [[supp-beta-binomial]], [[supp-map-gaussian]]

## Definition
A prior $p(\theta)$ is conjugate to a likelihood $p(\mathcal{D}|\theta)$ if the resulting posterior $p(\theta|\mathcal{D})$ belongs to the same parametric family as the prior.

## Motivation
Computing the posterior normally requires evaluating the intractable integral $p(\mathcal{D}) = \int p(\mathcal{D}|\theta)p(\theta)\,d\theta$. Conjugate priors eliminate this problem: the posterior has a known analytic form, obtained by updating the prior hyperparameters with sufficient statistics from the data.

## How it works
With a conjugate prior, Bayes' rule becomes a **hyperparameter update rule**:
$$p(\theta|\mathcal{D}) \propto p(\mathcal{D}|\theta)\,p(\theta) \implies \text{prior family} \to \text{posterior (same family, updated params)}$$

**Beta–Binomial** (canonical discrete example):
- Likelihood: $y \sim \text{Binomial}(n, \theta)$.
- Prior: $\theta \sim \text{Beta}(\alpha, \beta)$.
- Posterior: $\theta|y \sim \text{Beta}(\alpha + y,\; \beta + (n-y))$.
- Update rule: add observed successes to $\alpha$; add observed failures to $\beta$.

**Gaussian–Gaussian** (canonical continuous example):
- Likelihood: $y_i \sim \mathcal{N}(\mu, \sigma^2)$, $\sigma^2$ known.
- Prior: $\mu \sim \mathcal{N}(\mu_0, \sigma_0^2)$.
- Posterior: $\mu|\mathbf{y} \sim \mathcal{N}(\hat{\mu}_{\text{MAP}}, \Sigma_n)$ — also Gaussian.

**Gamma–Poisson**:
- Likelihood: $y_i \sim \text{Poisson}(\lambda)$.
- Prior: $\lambda \sim \text{Gamma}(\alpha, \beta)$.
- Posterior: $\lambda|\mathbf{y} \sim \text{Gamma}(\alpha + \sum_i y_i,\; \beta + n)$.

## Common conjugate pairs — reference table

| Likelihood | Conjugate Prior |
|---|---|
| Bernoulli | Beta |
| Binomial | Beta |
| Poisson | Gamma |
| Normal (fixed variance) | Normal for the mean |
| Normal (fixed mean) | Gamma prior for the inverse variance |
| Exponential | Gamma |
| Multinomial | Dirichlet |

### Likelihood PDFs / PMFs

**Bernoulli** ($x \in \{0,1\}$, parameter $\theta$):
$$p(x|\theta) = \theta^x (1-\theta)^{1-x}$$

**Binomial** ($k$ successes in $n$ trials, parameter $\theta$):
$$p(k|n,\theta) = \binom{n}{k} \theta^k (1-\theta)^{n-k}$$

**Poisson** ($k \in \{0,1,2,\dots\}$, rate $\lambda$):
$$p(k|\lambda) = \frac{\lambda^k e^{-\lambda}}{k!}$$

**Normal** (mean $\mu$, variance $\sigma^2$):
$$p(x|\mu,\sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$

**Exponential** (rate $\lambda$, $x \ge 0$):
$$p(x|\lambda) = \lambda\, e^{-\lambda x}$$

**Multinomial** ($\mathbf{x} = (x_1,\dots,x_K)$ counts over $K$ categories, $n$ trials, probabilities $\boldsymbol{\theta}$):
$$p(\mathbf{x}|n,\boldsymbol{\theta}) = \frac{n!}{x_1!\cdots x_K!}\prod_{k=1}^{K}\theta_k^{x_k}$$

### Conjugate prior PDFs

**Beta** (parameters $\alpha, \beta > 0$, $\theta \in [0,1]$):
$$p(\theta|\alpha,\beta) = \frac{1}{B(\alpha,\beta)}\,\theta^{\alpha-1}(1-\theta)^{\beta-1}, \quad B(\alpha,\beta) = \frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}$$

**Gamma** (shape $\alpha > 0$, rate $\beta > 0$, $x > 0$):
$$p(x|\alpha,\beta) = \frac{\beta^\alpha}{\Gamma(\alpha)}\,x^{\alpha-1}e^{-\beta x}$$

**Normal** (prior on mean $\mu$ with known variance; hyperparameters $\mu_0, \sigma_0^2$):
$$p(\mu|\mu_0,\sigma_0^2) = \frac{1}{\sqrt{2\pi\sigma_0^2}} \exp\!\left(-\frac{(\mu-\mu_0)^2}{2\sigma_0^2}\right)$$

**Dirichlet** (parameters $\boldsymbol{\alpha} = (\alpha_1,\dots,\alpha_K)$, $\boldsymbol{\theta}$ on the simplex):
$$p(\boldsymbol{\theta}|\boldsymbol{\alpha}) = \frac{\Gamma\!\left(\sum_k \alpha_k\right)}{\prod_k \Gamma(\alpha_k)}\prod_{k=1}^{K}\theta_k^{\alpha_k - 1}$$

## Key derivation
**Proving conjugacy** (Beta–Binomial):
1. Write posterior $\propto$ likelihood × prior.
2. Identify the functional form w.r.t. $\theta$.
3. Match to a known distribution family.

$$p(\theta|y) \propto \theta^y(1-\theta)^{n-y} \cdot \theta^{\alpha-1}(1-\theta)^{\beta-1} = \theta^{(\alpha+y)-1}(1-\theta)^{(\beta+n-y)-1}$$
This is $\text{Beta}(\alpha+y, \beta+n-y)$ — same family as prior. ✅

## Parameters & intuition
**Beta hyperparameters** as pseudo-counts:
- $\alpha$ = prior number of "successes" (heads).
- $\beta$ = prior number of "failures" (tails).
- $\alpha + \beta$ = "prior sample size" — how confident the prior is.
- Small $\alpha + \beta$: weakly informative prior, data dominates quickly.

**Posterior mean** for Beta–Binomial:
$$\mathbb{E}[\theta|y] = \frac{\alpha + y}{\alpha + \beta + n} \to \frac{y}{n} = \hat{\theta}_{\text{MLE}} \text{ as } n \to \infty$$

## Worked example sketch
*3 coin flips, 2 heads. Prior: Beta(1, 1) (uniform). Posterior: Beta(1+2, 1+1) = Beta(3, 2).*
*Posterior mean: 3/5 = 0.6. MLE: 2/3 ≈ 0.67. Prior regularises toward 0.5.*

## Connections
- Builds on [[bayesian-inference]] — conjugacy makes Bayesian inference computationally trivial.
- [[map]] using a conjugate posterior: find the mode of the posterior distribution.
- When conjugacy unavailable: use [[laplace-approximation]], [[variational-inference]], or [[mcmc]].
- Mean-field VI in conjugate models produces closed-form factor updates.

## Exam notes
- "What is a conjugate prior? State the advantage": ⚠️ **past exam question**.
- Proving conjugacy for Beta-Binomial: ⚠️ examinable.
- Must show posterior has the same functional form as the prior.
- Key advantage: closed-form posterior, avoids numerical integration, updates are simple parameter updates.
- Formula status: Beta and Gaussian pdfs will be given ✅ (Week 1)
