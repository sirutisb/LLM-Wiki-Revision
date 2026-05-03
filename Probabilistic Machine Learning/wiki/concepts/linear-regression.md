# Linear Regression

**Type:** model
**Week:** 2
**Related:** [[mle]], [[map]], [[bayesian-linear-regression]], [[generalised-linear-models]]
**Source:** [[lecture-w2]], [[supp-mle-simple-linear-regression]], [[supp-mle-multiple-linear-regression]]

## Definition
Linear regression models the conditional distribution of a continuous output $y$ as a Gaussian centred on a linear function of the input $x$, with constant noise variance.

## Motivation
The simplest model of continuous input–output relationships. Forms the foundation for Bayesian linear regression, GLMs, and regularised regression. Understanding its probabilistic derivation (Gaussian noise = MLE minimises squared error) clarifies why least squares works.

## How it works

### Simple Linear Regression
$$y_i = wx_i + \epsilon_i, \qquad \epsilon_i \sim \mathcal{N}(0, \sigma^2)$$
Equivalently: $y_i | x_i, w, \sigma^2 \sim \mathcal{N}(wx_i, \sigma^2)$.

**MLE**:
$$\hat{w}_{\text{MLE}} = \frac{\sum_i x_iy_i}{\sum_i x_i^2}, \qquad \hat{\sigma}^2_{\text{MLE}} = \frac{1}{n}\sum_i(y_i - \hat{w}x_i)^2$$
Minimising sum of squared errors (OLS) = maximising Gaussian log-likelihood.

### Multiple Linear Regression
$$y_i = \mathbf{w}^\top\mathbf{x}_i + \epsilon_i, \quad \epsilon_i \sim \mathcal{N}(0,\sigma^2)$$
**MLE (Normal Equations)**:
$$\hat{\mathbf{w}}_{\text{MLE}} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$$

### Assumptions
- Gaussian noise with constant variance (homoscedastic).
- Linear relationship between inputs and mean output.
- Outputs are continuous; errors can be negative.

### When Assumptions Fail
- Binary outputs → logistic regression (Bernoulli, logit link).
- Count outputs → Poisson regression (Poisson, log link).
- Non-constant variance → generalised least squares or GLMs.

## Key derivation
See [[supp-mle-simple-linear-regression]] for the full univariate derivation.

Key step: differentiate $\ell(w) = -\frac{1}{2\sigma^2}\sum_i(y_i-wx_i)^2$ w.r.t. $w$, set to zero → $\hat{w} = \sum_i x_iy_i / \sum_i x_i^2$.

⚠️ *Univariate MLE derivation examinable.*

## Parameters & intuition
- $w$ (slope): increase in $y$ per unit increase in $x$.
- $\sigma^2$: noise variance — how spread out the observations are around the line.
- Intercept: often included by appending a 1 to $\mathbf{x}_i$ (bias term).

## Worked example sketch
*Data*: $(x_1, y_1) = (1,2)$, $(x_2, y_2) = (2,3)$, $(x_3, y_3) = (3,5)$ (no intercept).
$\hat{w} = (1\cdot2 + 2\cdot3 + 3\cdot5)/(1^2+2^2+3^2) = 23/14 \approx 1.64$.

## Connections
- [[bayesian-linear-regression]]: Gaussian prior on $\mathbf{w}$ → posterior is Gaussian (closed form).
- MAP with Gaussian prior = ridge regression (L2 regularisation).
- [[generalised-linear-models]]: extend to non-Gaussian outputs.
- MLE for linear regression = OLS = minimise sum of squared errors.

## Exam notes
- MLE for simple linear regression: ⚠️ **examinable**.
- Normal Equations result ($(\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$): know the formula, derivation NOT examinable.
- "Why is log not a suitable link function for logistic regression?" — log link maps to $(0,\infty)$, not $[0,1]$.
- Formula status: Gaussian pdf will be given ✅
