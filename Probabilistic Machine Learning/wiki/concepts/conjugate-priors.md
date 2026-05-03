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

## Key derivation
**Proving conjugacy** (Beta–Binomial):
1. Write posterior $\propto$ likelihood × prior.
2. Identify the functional form w.r.t. $\theta$.
3. Match to a known distribution family.

$$p(\theta|y) \propto \theta^y(1-\theta)^{n-y} \cdot \theta^{\alpha-1}(1-\theta)^{\beta-1} = \theta^{(\alpha+y)-1}(1-\theta)^{(\beta+n-y)-1}$$
This is $\text{Beta}(\alpha+y, \beta+n-y)$ — same family as prior. ⚠️

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
