# Bayesian Linear Regression

**Type:** model
**Week:** 2
**Related:** [[linear-regression]], [[bayesian-inference]], [[map]], [[conjugate-priors]], [[variational-inference]]
**Source:** [[lecture-w2]]

## Definition
Bayesian linear regression places a Gaussian prior on the weight vector $\mathbf{w}$ and computes the posterior analytically, yielding a distribution over predictions rather than a point estimate.

## Motivation
MLE for linear regression gives a single weight vector — no uncertainty about the weights. In low-data regimes or when regularisation is needed, treating $\mathbf{w}$ probabilistically prevents overfitting and provides principled uncertainty estimates.

## How it works

### Model
$$\mathbf{w} \sim \mathcal{N}(\mathbf{w}_0, \mathbf{S}_0), \qquad y_i | \mathbf{x}_i, \mathbf{w} \sim \mathcal{N}(\mathbf{w}^\top\mathbf{x}_i, \sigma^2)$$
- **Prior**: Gaussian over weights.
- **Likelihood**: Gaussian (same as standard linear regression).
- **Both Gaussian**: conjugate pair → closed-form posterior.

### Posterior
Because the likelihood is Gaussian in $\mathbf{w}$ and the prior is Gaussian, the posterior is also Gaussian:
$$p(\mathbf{w}|\mathbf{X}, \mathbf{y}) = \mathcal{N}(\mathbf{w}_N, \mathbf{S}_N)$$
$$\mathbf{S}_N^{-1} = \mathbf{S}_0^{-1} + \frac{1}{\sigma^2}\mathbf{X}^\top\mathbf{X}, \qquad \mathbf{w}_N = \mathbf{S}_N\left(\mathbf{S}_0^{-1}\mathbf{w}_0 + \frac{1}{\sigma^2}\mathbf{X}^\top\mathbf{y}\right)$$

### Predictive Distribution
For a new input $\mathbf{x}_*$:
$$p(y_*|\mathbf{x}_*, \mathbf{X}, \mathbf{y}) = \mathcal{N}(\mathbf{w}_N^\top\mathbf{x}_*, \; \sigma^2 + \mathbf{x}_*^\top\mathbf{S}_N\mathbf{x}_*)$$
- Predictive variance = observation noise $\sigma^2$ + epistemic uncertainty from $\mathbf{S}_N$.

### Connection to MAP / Ridge Regression
With isotropic prior $\mathbf{w} \sim \mathcal{N}(\mathbf{0}, \tau^2 I)$:
$$\hat{\mathbf{w}}_{\text{MAP}} = \arg\max p(\mathbf{w}|\mathcal{D}) = \left(\mathbf{X}^\top\mathbf{X} + \frac{\sigma^2}{\tau^2}I\right)^{-1}\mathbf{X}^\top\mathbf{y}$$
This is **ridge regression** with $\lambda = \sigma^2/\tau^2$.

## Key derivation
Completing the square in the exponent of $p(\mathbf{y}|\mathbf{w})p(\mathbf{w})$. The Gaussian-Gaussian conjugacy ensures the posterior is Gaussian — the precision matrices (inverse covariances) add, and the posterior mean is a weighted combination of prior mean and data.
✅ *Formula sheet provided*. Multivariate derivation is not examinable.

## Parameters & intuition
- $\mathbf{w}_0$: prior mean for weights (often $\mathbf{0}$).
- $\mathbf{S}_0$: prior covariance — large diagonal = weak prior, small diagonal = strong regularisation.
- $\mathbf{S}_N$: shrinks as more data arrives → posterior concentrates around MLE.
- As $n \to \infty$: $\mathbf{w}_N \to \hat{\mathbf{w}}_{\text{MLE}}$; prior washed out.

## Worked example sketch
Prior: $w \sim \mathcal{N}(0, 1)$, $\sigma^2 = 1$. One observation $(x_1=1, y_1=2)$:
$$S_N^{-1} = 1 + 1 = 2, \quad w_N = \frac{1}{2}(0 + 2) = 1$$
Posterior: $w | \mathcal{D} \sim \mathcal{N}(1, 0.5)$.

## Connections
- [[linear-regression]]: Bayesian version; MLE is limiting case as prior strength → 0.
- [[conjugate-priors]]: Gaussian-Gaussian conjugacy enables closed-form posterior.
- [[map]]: MAP estimate from Bayesian LR = ridge regression.
- [[variational-inference]]: needed for non-conjugate priors or non-Gaussian likelihoods.

## Exam notes
- MAP = ridge regression derivation: Multivariate derivations are not examinable, but conceptually examinable.
- Posterior predictive variance formula: understand epistemic vs aleatoric uncertainty.
- Key conceptual exam question: "Why does MAP with Gaussian prior correspond to ridge regression?"
- Formula status: ✅ Formula sheet provided (Week 2 formulas are given).
