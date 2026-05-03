# Supp — MLE for Multiple Linear Regression

**File:** `raw/text/COM3031_W2_MLE4Multiple_linear_regression.txt`
**Type:** supplementary-note
**Week:** 2
**Concepts introduced:** [[linear-regression]], [[mle]]

## Summary
Derives MLE for the weight vector $\mathbf{w}$ and noise variance $\sigma^2$ in multiple linear regression using matrix calculus. The MLE weight vector is the Normal Equations solution (closed form). The MLE variance is the mean squared error.

## Key content

### Setup
- $y_i = \mathbf{w}^\top\mathbf{x}_i + \epsilon_i$, $\epsilon_i \sim \mathcal{N}(0,\sigma^2)$; $\mathbf{x}_i \in \mathbb{R}^d$.
- Design matrix: $\mathbf{X} \in \mathbb{R}^{n\times d}$ (rows = $\mathbf{x}_i^\top$).
- Log-likelihood: $\ell(\mathbf{w},\sigma^2) = -\frac{n}{2}\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}(\mathbf{y}-\mathbf{X}\mathbf{w})^\top(\mathbf{y}-\mathbf{X}\mathbf{w})$.

### MLE for $\mathbf{w}$ (Normal Equations)
Minimise $(\mathbf{y}-\mathbf{X}\mathbf{w})^\top(\mathbf{y}-\mathbf{X}\mathbf{w}) = \mathbf{y}^\top\mathbf{y} - 2\mathbf{w}^\top\mathbf{X}^\top\mathbf{y} + \mathbf{w}^\top\mathbf{X}^\top\mathbf{X}\mathbf{w}$.

Taking gradient and setting to zero:
$$\nabla_\mathbf{w} = 2\mathbf{X}^\top\mathbf{X}\mathbf{w} - 2\mathbf{X}^\top\mathbf{y} = 0 \implies \mathbf{X}^\top\mathbf{X}\mathbf{w} = \mathbf{X}^\top\mathbf{y}$$

$$\hat{\mathbf{w}}_{\text{MLE}} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$$
(Requires $\mathbf{X}^\top\mathbf{X}$ invertible, i.e. $n \geq d$ and no perfectly collinear features.)

### MLE for $\sigma^2$
$$\hat{\sigma}^2_{\text{MLE}} = \frac{1}{n}(\mathbf{X}\hat{\mathbf{w}}-\mathbf{y})^\top(\mathbf{X}\hat{\mathbf{w}}-\mathbf{y})$$

### Interpretation
- Same MLE principle as simple regression, now in matrix form.
- $\hat{\mathbf{w}}$ is the projection of $\mathbf{y}$ onto the column space of $\mathbf{X}$.
- Derivation relies on vector calculus: $\nabla_\mathbf{w}(\mathbf{w}^\top\mathbf{A}\mathbf{w}) = 2\mathbf{A}\mathbf{w}$.

## Exam notes
- Multivariate derivations: ❌ NOT examinable.
- Understand the structure: Normal Equations, design matrix.
- Know the result: $\hat{\mathbf{w}} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$.

## Links to concepts
- [[linear-regression]]: multivariate version
- [[mle]]: applied with matrix calculus
- [[bayesian-linear-regression]]: adds Gaussian prior → posterior is Gaussian
