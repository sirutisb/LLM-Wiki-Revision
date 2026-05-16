# Laplace Approximation

**Type:** approximation method
**Week:** 3
**Related:** [[map]], [[variational-inference]], [[mcmc]], [[bic]], [[bayesian-inference]]
**Source:** [[lecture-w3]], [[lecture-w10]]

## Definition
The Laplace approximation replaces an intractable posterior with a Gaussian centred at the MAP estimate, using the local curvature of the log-posterior to determine the variance.

## Motivation
The exact posterior $p(\theta|\mathcal{D})$ is usually intractable (the evidence $p(\mathcal{D})$ cannot be computed). The Laplace approximation gives a cheap, analytic approximation when the posterior is unimodal and near-Gaussian — the cost is just one MAP optimisation plus one Hessian computation.

## How it works

### 1D Case
1. Compute $g(\theta) = \log p(\mathcal{D}|\theta) + \log p(\theta)$ (log unnormalised posterior).
2. Find MAP: $\hat{\theta} = \arg\max_\theta g(\theta)$.
3. Second-order Taylor expand $g$ around $\hat{\theta}$ (first-order term = 0 at the mode):
$$g(\theta) \approx g(\hat{\theta}) - \frac{A}{2}(\theta - \hat{\theta})^2, \qquad A = -g''(\hat{\theta}) > 0$$
4. Exponentiate: $p(\theta|\mathcal{D}) \approx q(\theta) = \mathcal{N}(\theta\,|\,\hat{\theta},\, A^{-1})$.

### Multi-dimensional Case
$$p(\boldsymbol{\theta}|\mathcal{D}) \approx \mathcal{N}(\boldsymbol{\theta}\,|\,\hat{\boldsymbol{\theta}},\, \mathbf{H}^{-1})$$
where $\mathbf{H} = -\nabla^2 g(\boldsymbol{\theta})|_{\hat{\boldsymbol{\theta}}}$ is the **negative Hessian of the log-posterior** evaluated at the MAP. ⚠️ *Multivariate derivation NOT examinable.*

**Interpretation**: sharper peak $\Rightarrow$ larger curvature $\Rightarrow$ smaller variance in the Gaussian approximation.

## Key derivation
⚠️ *No formula given in exam*

**Worked example** (from Week 10):
$p(\theta|y) \propto \theta^y(1-\theta)^{n-y}$

Step 1: $g(\theta) = y\log\theta + (n-y)\log(1-\theta)$.

Step 2: $g'(\theta) = y/\theta - (n-y)/(1-\theta) = 0 \Rightarrow \hat{\theta} = y/n$.

Step 3: $g''(\theta) = -y/\theta^2 - (n-y)/(1-\theta)^2$; at $\hat{\theta}$:
$$A = -g''(\hat{\theta}) = \frac{n^3}{y(n-y)}$$

Step 4: Variance $= A^{-1} = \frac{y(n-y)}{n^3}$.

Laplace approximation: $q(\theta) = \mathcal{N}\!\left(\frac{y}{n},\, \frac{y(n-y)}{n^3}\right)$.

⚠️ *This type of worked example is examinable.*

## Parameters & intuition
- **Mean** = MAP estimate (posterior mode).
- **Variance** = $-1/g''(\hat{\theta})$ = inverse curvature.
- Curvature measures "how peaked" the posterior is.
- Connection to Fisher information: curvature = observed Fisher information.

## Worked example sketch
Gamma approximation: $p(\theta) \propto \theta^{\alpha-1}e^{-\beta\theta}$ → Mode: $\hat{\theta} = (\alpha-1)/\beta$; curvature: $A = \beta^2/(\alpha-1)$; variance: $(\alpha-1)/\beta^2$. (See full derivation: [[laplace-gamma]])

## Connections
- Requires [[map]] as a prerequisite — Laplace is centred at the MAP.
- Compare with [[variational-inference]]: VI is a global approximation; Laplace is local (near the mode only).
- [[bic]] is derived by applying Laplace to the model evidence integral.
- Works well for Bayesian logistic regression (approximates the non-Gaussian posterior).

## Exam notes
- "What is the main use? State one limitation": ⚠️ **past exam question**.
  - Use: approximate intractable posteriors with a Gaussian (MAP + curvature).
  - Limitation: fails for multimodal, skewed posteriors; local only.
- Worked calculation (find MAP, compute second derivative, find variance): ⚠️ **examinable**.
- Multivariate: concept required, derivation NOT examinable.
- No formulas given for Week 3. ⚠️
- **Common pitfall**: at the mode, $g'(\hat{\theta}) = 0$; the linear Taylor term vanishes. Students sometimes forget this step.
- Formula status: must know the 1D procedure from memory ⚠️
