# Monte Carlo Integration

**Type:** algorithm
**Week:** 5
**Related:** [[mcmc]], [[rejection-sampling]], [[importance-sampling]], [[bayesian-inference]]
**Source:** [[lecture-w5]]

## Definition
Monte Carlo integration approximates an expectation or integral by averaging the integrand over random samples from the distribution.

## Motivation
Most integrals in Bayesian inference (posterior predictive, model evidence, posterior expectations) are analytically intractable. Monte Carlo provides a general numerical approximation using samples, with convergence guaranteed by the law of large numbers.

## How it works

### Estimator
Goal: estimate $I = \mathbb{E}_{p}[f(\theta)] = \int f(\theta)p(\theta)\,d\theta$.

Draw $\theta_1, \ldots, \theta_S \sim p(\theta)$ independently:
$$\hat{I}_S = \frac{1}{S}\sum_{s=1}^S f(\theta_s) \approx I$$

### Convergence
- **Unbiased**: $\mathbb{E}[\hat{I}_S] = I$ for all $S$.
- **Consistent**: $\hat{I}_S \to I$ as $S \to \infty$ (law of large numbers).
- **Standard error**: $\text{SE}(\hat{I}_S) = \frac{\text{std}(f(\theta))}{\sqrt{S}}$ — convergence at $O(1/\sqrt{S})$ regardless of dimension.

### Why Dimension-Independent Convergence?
Unlike quadrature (which needs exponentially many grid points in $d$ dimensions), Monte Carlo's $O(1/\sqrt{S})$ rate is the same in any dimension — making it the go-to method for high-dimensional integrals.

### Applications in Bayesian Inference
- **Posterior predictive**: $p(y^*|x^*, \mathcal{D}) = \mathbb{E}_{p(\theta|\mathcal{D})}[p(y^*|x^*,\theta)] \approx \frac{1}{S}\sum_s p(y^*|x^*,\theta_s)$
- **Model evidence**: $p(\mathcal{D}) = \mathbb{E}_{p(\theta)}[p(\mathcal{D}|\theta)] \approx \frac{1}{S}\sum_s p(\mathcal{D}|\theta_s)$
- **Posterior expectations**: any function of the posterior.

### Challenge
Requires samples from $p$ — often the posterior we can't sample from directly. Solutions: MCMC (Markov chain samples), importance sampling (reweight from a proposal).

## Key derivation
By the strong law of large numbers: $\frac{1}{S}\sum_s f(\theta_s) \to \mathbb{E}_p[f(\theta)]$ a.s. as $S \to \infty$. Variance: $\text{Var}(\hat{I}_S) = \text{Var}_p(f)/S$.

## Parameters & intuition
- $S$ samples: more samples → lower variance but higher computational cost.
- $f$ with low variance under $p$: fewer samples needed.
- Variance reduction techniques: importance sampling, control variates, antithetic variables.

## Connections
- [[mcmc]]: generates correlated samples from $p$ for Monte Carlo; autocorrelation reduces effective $S$.
- [[importance-sampling]]: Monte Carlo with reweighted samples from a different distribution.
- [[rejection-sampling]]: generates exact independent samples for Monte Carlo.
- [[bayesian-inference]]: Monte Carlo is the main computational tool for posterior inference.

## Exam notes
- Know the MC estimator and convergence rate $O(1/\sqrt{S})$. ⚠️
- Why MC beats numerical integration in high dimensions: dimension-independent convergence.
- Formula status: no formula sheet for Week 5 ⚠️
