# Generalised Linear Models (GLMs)

**Type:** model
**Week:** 2
**Related:** [[linear-regression]], [[logistic-regression]], [[bayesian-inference]]
**Source:** [[lecture-w2]]

## Definition
A Generalised Linear Model (GLM) is a flexible extension of linear regression that connects a linear predictor to the mean of any exponential-family distribution via a link function.

## Motivation
Linear regression assumes Gaussian noise and continuous unbounded outputs. Many real outcomes are binary, counts, proportions, or strictly positive — GLMs handle all these by choosing the appropriate distribution and link function.

## How it works

### Three Components
1. **Linear predictor**: $\eta_i = \mathbf{w}^\top\mathbf{x}_i$.
2. **Link function** $g$: relates $\eta_i$ to the mean $\mu_i = \mathbb{E}[y_i|\mathbf{x}_i]$ via $g(\mu_i) = \eta_i$.
3. **Response distribution**: $y_i \sim$ exponential family with mean $\mu_i$.

### Common GLMs

| Response | Distribution | Link | Inverse link |
|----------|-------------|------|-------------|
| Continuous | Gaussian | Identity: $\eta = \mu$ | $\mu = \eta$ |
| Binary | Bernoulli | Logit: $\eta = \log\frac{\mu}{1-\mu}$ | $\mu = \sigma(\eta)$ |
| Count | Poisson | Log: $\eta = \log\mu$ | $\mu = e^\eta$ |

### Why Link Functions Matter
The link must map $(-\infty, +\infty)$ (domain of $\eta$) to the valid range of $\mu$:
- Probabilities: must be in $[0,1]$ → logit link.
- Counts/rates: must be positive → log link.
- Continuous: can be anything → identity link works.

### Canonical Link
Each exponential-family distribution has a **canonical link** (the natural choice that leads to mathematical simplifications). Logit is canonical for Bernoulli; log is canonical for Poisson.

### Training
All GLMs are trained by MLE. The log-likelihood depends on the chosen distribution. For most GLMs other than Gaussian linear regression, there is no closed-form MLE — use gradient-based optimisation.

## Key derivation
No single derivation — the key insight is that the three-component structure unifies diverse regression models. The GLM log-likelihood gradient always has the form $\nabla_\mathbf{w} \ell = \mathbf{X}^\top(\mathbf{y} - \boldsymbol{\mu})$ (observed minus expected), which is elegant and numerically stable.

## Parameters & intuition
- $\mathbf{w}$: effect of each feature on the linear predictor (= log-odds for logistic, log-rate for Poisson).
- The link function determines how to interpret coefficients.
- Larger $|w_j|$: stronger effect of feature $x_j$ on the outcome.

## Connections
- [[linear-regression]]: Gaussian GLM with identity link — special case.
- [[logistic-regression]]: Bernoulli GLM with logit link.
- [[bayesian-inference]]: GLMs can be given priors; MAP = regularised MLE.

## Exam notes
- "Why is log not a suitable link function for logistic regression?" — log maps to $(0,\infty)$ not $[0,1]$. ⚠️
- Know which distribution/link pair corresponds to which regression type.
- GLM unification concept is examinable conceptually.
- Formula status: Gaussian pdf given ✅; logistic sigmoid should be known ⚠️
