# Derivation: MLE for Multiple Linear Regression (Normal Equations)

**Used in:** [[linear-regression]], [[mle]], [[bayesian-linear-regression]]
**Source:** [[supp-mle-multiple-linear-regression]]
**Exam status:** ✅ Result (Normal Equations) must be known; full derivation NOT examinable

## Setup
Model: $y_i = \mathbf{w}^\top\mathbf{x}_i + \epsilon_i$, $\epsilon_i \sim \mathcal{N}(0,\sigma^2)$ i.i.d.

Matrix form: $\mathbf{y} = \mathbf{X}\mathbf{w} + \boldsymbol{\epsilon}$

Where:
- $\mathbf{X} \in \mathbb{R}^{n \times d}$: design matrix (row $i$ = input $\mathbf{x}_i^\top$).
- $\mathbf{y} \in \mathbb{R}^n$: response vector.
- $\mathbf{w} \in \mathbb{R}^d$: weight vector to estimate.

Derive $\hat{\mathbf{w}}_{\text{MLE}}$.

## Steps

### 1. Write the log-likelihood
$$\ell(\mathbf{w}) = -\frac{n}{2}\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}\|\mathbf{y} - \mathbf{X}\mathbf{w}\|^2$$

Maximising $\ell(\mathbf{w})$ is equivalent to minimising the sum of squared residuals:
$$\text{RSS}(\mathbf{w}) = \|\mathbf{y} - \mathbf{X}\mathbf{w}\|^2 = (\mathbf{y}-\mathbf{X}\mathbf{w})^\top(\mathbf{y}-\mathbf{X}\mathbf{w})$$

### 2. Expand RSS
$$\text{RSS}(\mathbf{w}) = \mathbf{y}^\top\mathbf{y} - 2\mathbf{w}^\top\mathbf{X}^\top\mathbf{y} + \mathbf{w}^\top\mathbf{X}^\top\mathbf{X}\mathbf{w}$$

### 3. Differentiate with respect to $\mathbf{w}$
$$\frac{\partial\,\text{RSS}}{\partial\mathbf{w}} = -2\mathbf{X}^\top\mathbf{y} + 2\mathbf{X}^\top\mathbf{X}\mathbf{w} = \mathbf{0}$$

### 4. Solve (Normal Equations)
$$\mathbf{X}^\top\mathbf{X}\hat{\mathbf{w}} = \mathbf{X}^\top\mathbf{y}$$

Assuming $\mathbf{X}^\top\mathbf{X}$ is invertible:

$$\boxed{\hat{\mathbf{w}}_{\text{MLE}} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}}$$

## Result
$$\hat{\mathbf{w}}_{\text{MLE}} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$$

The **Moore-Penrose pseudoinverse** solution when $\mathbf{X}^\top\mathbf{X}$ is singular: $\hat{\mathbf{w}} = \mathbf{X}^+\mathbf{y}$.

## Intuition
- $\mathbf{X}^\top\mathbf{X}$: Gram matrix — captures feature correlations (if diagonal: features are orthogonal).
- $\mathbf{X}^\top\mathbf{y}$: cross-covariance between features and target.
- $(X^\top X)^{-1} X^\top$: left pseudoinverse — projects $\mathbf{y}$ onto the column space of $\mathbf{X}$ (orthogonal projection).
- When $\mathbf{X}^\top\mathbf{X}$ is near-singular: features are nearly collinear → numerically unstable → use ridge regression (add $\lambda I$).
