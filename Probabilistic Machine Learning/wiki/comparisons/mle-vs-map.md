# MLE vs MAP

## Overview
Maximum Likelihood Estimation (MLE) and Maximum A Posteriori (MAP) are the two primary point-estimation methods in probabilistic machine learning. While MLE is a frequentist approach that relies solely on observed data, MAP is a Bayesian approach that incorporates prior beliefs. In the context of linear regression, MLE leads to Ordinary Least Squares (OLS), whereas MAP leads to Ridge Regression (L2 regularisation).

## Comparison table

| Dimension | Maximum Likelihood (MLE) | Maximum A Posteriori (MAP) |
|-----------|--------------------------|----------------------------|
| **Objective** | $\arg\max_\theta p(\mathcal{D}\|\theta)$ | $\arg\max_\theta p(\theta\|\mathcal{D}) \propto p(\mathcal{D}\|\theta)p(\theta)$ |
| **Philosophy** | Frequentist: data only | Bayesian: data + prior |
| **Regularisation** | None (prone to overfitting) | Implicit via prior (prevents overfitting) |
| **Prior** | Flat / Uniform prior | Informative prior (e.g., Gaussian) |
| **Output** | Single point estimate $\hat{\theta}_{\text{MLE}}$ | Single point estimate $\hat{\theta}_{\text{MAP}}$ |
| **Linear Regression** | Ordinary Least Squares (OLS) | Ridge Regression (L2) |
| **Uncertainty** | None (Point estimate) | None (Point estimate) |
| **Data Limit** | Consistent as $n \to \infty$ | Converges to MLE as $n \to \infty$ |

## The "Uncertainty" Pitfall
A common exam confusion is thinking that because MAP is "Bayesian," it provides uncertainty quantification. **It does not.**

- **MLE and MAP** are both **point estimation** methods. They return a single weight vector $\mathbf{w}$. When you make a prediction for a new $x^*$, you get a single number $y^*$.
- **Full Bayesian Linear Regression** computes the entire posterior distribution $p(\mathbf{w}|\mathcal{D})$. When you predict, you integrate over all possible weights, which gives you a **predictive distribution**. This distribution has a variance that represents the model's uncertainty.

**To get uncertainty from MAP**, you must use an approximation like the [[laplace-approximation]], which fits a Gaussian distribution around the MAP estimate.

## When to use which

### Use MLE when:
- **Large dataset**: You have enough data that the likelihood dominates any reasonable prior.
- **No prior knowledge**: You have no objective or subjective reason to prefer certain parameter values over others.
- **Simplicity**: You want the simplest model without tuning hyper-parameters (like prior variance).

### Use MAP when:
- **Small dataset**: You want to prevent the model from overfitting to noise in a small sample.
- **Prior knowledge exists**: You have historical data or physical constraints that suggest certain parameter ranges.
- **Regularisation is needed**: You want to perform ridge regression or similar penalised estimation in a principled probabilistic framework.

## Synthesis
MAP is the "bridge" between frequentist MLE and full Bayesian inference. It is an optimisation-based method like MLE, making it computationally efficient, but it inherits the Bayesian ability to handle uncertainty via the prior.

In **Linear Regression**, the relationship is mathematically precise:
- **MLE** assumes $y_i \approx \mathbf{w}^\top\mathbf{x}_i + \epsilon$ and finds $\mathbf{w}$ by minimising the sum of squares.
- **MAP** with a Gaussian prior $\mathbf{w} \sim \mathcal{N}(0, \tau^2 I)$ adds a penalty term $\lambda\|\mathbf{w}\|^2$ to the sum of squares, where $\lambda = \sigma^2/\tau^2$. This shows that the regularisation strength $\lambda$ in Ridge Regression is actually the ratio of observation noise to prior uncertainty.

## Connections
- [[mle]]: The frequentist foundation.
- [[map]]: The Bayesian point-estimate extension.
- [[bayesian-linear-regression]]: The full Bayesian treatment (distribution over $\mathbf{w}$), of which MAP is just the mode.
- [[laplace-approximation]]: Centred at the MAP estimate.
