# Derivation: MLE for Simple Linear Regression

**Used in:** [[linear-regression]], [[mle]]
**Source:** [[supp-mle-simple-linear-regression]]
**Exam status:** ⚠️ Must know — explicitly stated examinable derivation

## Setup
Model: $y_i = wx_i + \epsilon_i$, $\epsilon_i \sim \mathcal{N}(0, \sigma^2)$ i.i.d.
Equivalently: $y_i \sim \mathcal{N}(wx_i, \sigma^2)$.

Observations: $(x_1, y_1), \ldots, (x_n, y_n)$.
No intercept (intercept case: append 1 to $x_i$).

Derive $\hat{w}_{\text{MLE}}$ and $\hat{\sigma}^2_{\text{MLE}}$.

## Steps

### 1. Write the log-likelihood
$$\ell(w, \sigma^2) = \sum_{i=1}^n \log\mathcal{N}(y_i; wx_i, \sigma^2)$$
$$= -\frac{n}{2}\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}\sum_{i=1}^n(y_i - wx_i)^2$$

### 2. Optimise for $w$
The $\sigma^2$ terms are constant w.r.t. $w$, so:
$$\hat{w} = \arg\min_w \sum_{i=1}^n(y_i - wx_i)^2$$

Differentiate:
$$\frac{\partial}{\partial w}\sum_i(y_i - wx_i)^2 = -2\sum_i x_i(y_i - wx_i) = 0$$

$$\sum_i x_iy_i = w\sum_i x_i^2$$

$$\boxed{\hat{w}_{\text{MLE}} = \frac{\sum_i x_iy_i}{\sum_i x_i^2}}$$

### 3. Optimise for $\sigma^2$
With $\hat{w}$ substituted, differentiate w.r.t. $v = \sigma^2$:
$$\frac{\partial\ell}{\partial v} = -\frac{n}{2v} + \frac{1}{2v^2}\sum_i(y_i - \hat{w}x_i)^2 = 0$$
$$\hat{v} = \frac{1}{n}\sum_i(y_i - \hat{w}x_i)^2$$

$$\boxed{\hat{\sigma}^2_{\text{MLE}} = \frac{1}{n}\sum_{i=1}^n(y_i - \hat{w}x_i)^2}$$

## Result
$$\hat{w}_{\text{MLE}} = \frac{\sum_i x_iy_i}{\sum_i x_i^2}, \qquad \hat{\sigma}^2_{\text{MLE}} = \frac{1}{n}\sum_i(y_i - \hat{w}x_i)^2$$

## Intuition
- MLE for $w$ = **OLS (ordinary least squares)**: minimise sum of squared residuals. The Gaussian noise assumption makes these equivalent.
- The OLS estimator $\hat{w} = \sum x_iy_i / \sum x_i^2$ is the ratio of the cross-moment to the second moment of $x$.
- $\hat{\sigma}^2$: mean squared residual — how spread the data is around the fitted line.

## Worked Example
Data: $(1,2), (2,3), (3,5)$.

$\hat{w} = (1\cdot2 + 2\cdot3 + 3\cdot5)/(1^2+2^2+3^2) = (2+6+15)/(1+4+9) = 23/14 \approx 1.643$

Residuals: $2 - 1.643 = 0.357$; $3 - 3.286 = -0.286$; $5 - 4.929 = 0.071$.

$\hat{\sigma}^2 = (0.357^2 + 0.286^2 + 0.071^2)/3 \approx 0.054$.
