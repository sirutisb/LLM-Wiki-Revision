# Supp — MLE for Simple Linear Regression

**File:** `raw/text/COM3031_W2_MLE4Simple_linear_regression.txt`
**Type:** supplementary-note
**Week:** 2
**Concepts introduced:** [[linear-regression]], [[mle]]

## Summary
Derives MLE estimates for the weight $w$ and noise variance $\sigma^2$ in simple (univariate) linear regression. Shows that maximising the Gaussian log-likelihood is equivalent to minimising sum of squared errors — the OLS connection.

## Key content

### Setup
- Model: $y_i = wx_i + \epsilon_i$, $\epsilon_i \sim \mathcal{N}(0, \sigma^2)$.
- Single observation likelihood: $p(y_i|x_i, w, \sigma^2) = \mathcal{N}(wx_i, \sigma^2)$.
- Log-likelihood:
$$\ell(w, \sigma^2) = -\frac{n}{2}\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}\sum_{i=1}^n(y_i - wx_i)^2$$

### MLE for $w$
$$\frac{\partial\ell}{\partial w} = \frac{1}{\sigma^2}\sum_{i=1}^n x_i(y_i - wx_i) = 0$$
$$\implies \sum_i x_i y_i - w\sum_i x_i^2 = 0$$
$$\hat{w}_{\text{MLE}} = \frac{\sum_{i=1}^n x_i y_i}{\sum_{i=1}^n x_i^2}$$

### MLE for $\sigma^2$
$$\frac{\partial\ell}{\partial\sigma^2} = -\frac{n}{2\sigma^2} + \frac{1}{2(\sigma^2)^2}\sum_i(y_i-wx_i)^2 = 0$$
$$\hat{\sigma}^2_{\text{MLE}} = \frac{1}{n}\sum_{i=1}^n (y_i - \hat{w}x_i)^2$$

### Interpretation
- MLE for $w$ minimises $\sum_i(y_i - wx_i)^2$ (ordinary least squares).
- MLE for $\sigma^2$ = mean squared error (MSE).
- Connection: Gaussian noise model $\Leftrightarrow$ least squares objective.

## Exam notes
- MLE for simple linear regression: ⚠️ **examinable** (univariate only).
- Must be able to derive both $\hat{w}$ and $\hat{\sigma}^2$.
- Formula sheet: Gaussian pdf **will be given** (Week 2).

## Links to concepts
- [[linear-regression]]: core model
- [[mle]]: procedure applied here
- [[bayesian-linear-regression]]: Bayesian version adds prior on $w$
