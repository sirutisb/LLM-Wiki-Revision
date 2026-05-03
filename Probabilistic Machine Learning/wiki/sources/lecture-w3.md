# Week 3 — Laplace Approximation & Bayesian Model Comparison

**File:** `raw/text/COM3031_2526_Week3.txt`
**Type:** lecture
**Week:** 3
**Concepts introduced:** [[laplace-approximation]], [[bayesian-model-comparison]], [[bic]]

## Summary
Week 3 motivates approximate inference by showing that exact posteriors are intractable for most models (e.g. Bayesian logistic regression). The Laplace approximation is introduced as the simplest bridge from optimisation to Bayesian uncertainty: fit a Gaussian centred at the MAP, with variance given by the inverse curvature of the log-posterior. The lecture then applies Laplace to model evidence computation, deriving the Bayesian Information Criterion (BIC).

## Key content

### Why Approximate Inference
- Exact posterior $p(\theta|\mathcal{D})$ requires computing the evidence $p(\mathcal{D}) = \int p(\mathcal{D}|\theta)p(\theta)\,d\theta$ — usually intractable.
- Bayesian linear regression is a rare exception (Gaussian conjugacy gives closed form).
- Bayesian logistic regression: sigmoid likelihood makes posterior non-Gaussian; no closed-form normaliser.
- Three main families: local approximations (Laplace), optimisation-based (VI), sampling-based (MCMC).

### Laplace Approximation: 1D
1. Compute $g(\theta) = \log\tilde{p}(\theta) = \log p(\mathcal{D}|\theta) + \log p(\theta)$ (log unnormalised posterior).
2. Find MAP: $\hat{\theta} = \arg\max_\theta g(\theta)$.
3. Second-order Taylor expansion about $\hat{\theta}$ (first-order term vanishes at the mode):
$$g(\theta) \approx g(\hat{\theta}) - \frac{1}{2}A(\theta - \hat{\theta})^2, \qquad A = -g''(\hat{\theta}) > 0$$
4. Exponentiate: posterior $\approx \mathcal{N}(\hat{\theta}, A^{-1})$.

**Interpretation**: sharper peak (larger curvature) → smaller variance → more confident.

### Laplace Approximation: Multi-dimensional
- Log unnormalised posterior: $g(\boldsymbol{\theta}) = \log p(\mathcal{D}|\boldsymbol{\theta}) + \log p(\boldsymbol{\theta})$.
- Step 1: Find MAP $\hat{\boldsymbol{\theta}} = \arg\max_{\boldsymbol{\theta}} g(\boldsymbol{\theta})$ (via gradient ascent or Newton's method).
- Step 2: Compute **Hessian** at the mode: $\mathbf{H} = -\nabla^2 g(\boldsymbol{\theta})|_{\boldsymbol{\theta}=\hat{\boldsymbol{\theta}}}$ (negative Hessian of log-posterior).
- Approximation: $p(\boldsymbol{\theta}|\mathcal{D}) \approx \mathcal{N}(\hat{\boldsymbol{\theta}}, \mathbf{H}^{-1})$.

**Covariance interpretation**: strong curvature (large eigenvalues of $\mathbf{H}$) → small uncertainty.

### Strengths and Limitations
- Works well: unimodal, near-symmetric posterior; moderate to large data.
- Works poorly: multimodal posterior, highly skewed posterior, deep neural networks.
- Laplace is **local** — it only captures the behaviour near one peak.

### Bayesian Model Comparison
- Compare models $\mathcal{M}_1, \ldots, \mathcal{M}_K$ via posterior: $p(\mathcal{M}|\mathcal{D}) \propto p(\mathcal{D}|\mathcal{M})p(\mathcal{M})$.
- With equal priors: prefer $\mathcal{M}$ with highest **model evidence** $p(\mathcal{D}|\mathcal{M}) = \int p(\mathcal{D}|\theta,\mathcal{M})p(\theta|\mathcal{M})\,d\theta$.
- Evidence balances data fit and model complexity (**Occam's razor** — complex models spread probability mass thinly).

### Bayesian Information Criterion (BIC)
- Apply Laplace to the evidence integral around MAP $\hat{\theta}$:
$$\log p(\mathcal{D}|\mathcal{M}) \approx \log p(\mathcal{D}|\hat{\theta}) - \frac{k}{2}\log n + \text{const}$$
- Leads to BIC:
$$\text{BIC} = -2\log p(\mathcal{D}|\hat{\theta}) + k\log n$$
  where $k$ = number of parameters, $n$ = number of data points.
- **Lower BIC = better model.** First term rewards fit; second term penalises complexity.
- Assumptions: large $n$ (asymptotic), unimodal posterior.

## Key takeaways
- Laplace approximation is the simplest approximate inference method: fit a Gaussian at the MAP.
- Variance comes from the inverse curvature (Hessian) of the log-posterior at the mode.
- For logistic regression: MAP = regularised logistic regression; Hessian gives uncertainty.
- BIC = Laplace approximation to log model evidence, approximates Bayesian model selection.

## Exam relevance
- "Main use of Laplace approximation; state one limitation": **past exam question**.
- Laplace approximation worked example (finding mode and variance for a given distribution): **examinable**.
- Multivariate Laplace: NOT examinable (derivation).
- BIC: conceptual understanding required.
- No formulas given for Week 3.

## Links to concepts
- [[laplace-approximation]]: introduced here
- [[bayesian-model-comparison]]: introduced here
- [[bic]]: introduced here
- [[map]]: prerequisite — Laplace is centred at MAP
- [[variational-inference]]: next step — global approximation ([[lecture-w4]])
