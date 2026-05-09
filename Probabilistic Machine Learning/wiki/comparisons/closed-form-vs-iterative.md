# Closed-Form vs Iterative Solutions

## Overview
A major recurring theme in probabilistic machine learning is whether an inference problem or parameter estimation has a **closed-form** (analytical) solution, or whether it requires **iterative optimisation** (numerical approximation). 

This distinction often dictates which algorithms we can apply. When models become more complex (e.g., non-linear link functions, deep networks, or non-conjugate priors), we generally lose closed-form guarantees and must fall back on iterative methods like Gradient Ascent, Variational Inference, or MCMC.

## Comparison Table
| Dimension | Closed-Form Solutions | Iterative / Approximate Solutions |
|-----------|-----------------------|-----------------------------------|
| **Definition** | The solution can be expressed exactly using a finite number of standard mathematical operations (algebra, matrices). | The solution is found by repeatedly updating a guess until it converges to an optimum or stationary distribution. |
| **Computation** | Direct, deterministic, "one-shot" calculation. | Requires multiple steps/epochs; convergence speed depends on learning rate/step size. |
| **Typical Requirement** | Linear models, Gaussian noise, Conjugate priors. | Non-linear activations/link functions, non-conjugate priors, complex graphical models. |
| **Optimization** | Solves $\nabla_\theta \mathcal{L}(\theta) = 0$ directly for $\theta$. | Evaluates $\nabla_\theta \mathcal{L}(\theta)$ to take steps: $\theta \leftarrow \theta + \eta \nabla_\theta \mathcal{L}(\theta)$. |

## Models with Closed-Form Solutions

In this module, exact analytical solutions are rare but highly desirable. They occur in:

1. **[[linear-regression]] (MLE & MAP)**
   - **Why:** The sum of squared errors (or Gaussian log-likelihood) is a quadratic function of the weights. Taking the derivative yields linear equations.
   - **Result:** The Normal Equations: $\mathbf{w}_{MLE} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$.
2. **[[bayesian-linear-regression]]**
   - **Why:** The Gaussian prior on weights and the Gaussian likelihood form a [[conjugate-priors|conjugate pair]].
   - **Result:** The posterior distribution over weights is exactly a Gaussian.
3. **Simple Bayesian Inference ([[conjugate-priors]])**
   - **Why:** The prior and likelihood are mathematically matched such that the posterior belongs to the same family as the prior.
   - **Result:** E.g., Beta prior + Binomial likelihood = Beta posterior. The normalisation constant $p(\mathbf{y})$ evaluates to a known integral (e.g. Beta function).
4. **[[mean-field-vi]] (Coordinate updates)**
   - **Why:** If the model components belong to the exponential family and are conjugate, the optimal variational factor $q_j(z_j)$ has a closed-form update equation.
5. **KL Divergence between two Gaussians**
   - **Why:** Required for [[variational-autoencoder|VAEs]], the integral evaluates exactly, allowing the use of the reparameterization trick on the expected log-likelihood.

## Models Requiring Iterative Optimisation

Most real-world models lack closed-form solutions and rely on iterative techniques:

1. **[[logistic-regression]] & [[poisson-regression]] (GLMs)**
   - **Why:** They apply a non-linear link function (sigmoid or exponential) to $\mathbf{w}^\top\mathbf{x}$. The parameter $\mathbf{w}$ becomes trapped inside this non-linear function.
   - **Result:** We cannot isolate $\mathbf{w}$ to solve $\nabla_\mathbf{w} \ell = 0$. We must use Gradient Ascent or Newton-Raphson.
2. **Bayesian Logistic Regression**
   - **Why:** The Gaussian prior and Bernoulli (sigmoid) likelihood are not conjugate.
   - **Result:** The posterior $p(\mathbf{w}|\mathbf{X},\mathbf{y})$ is non-Gaussian and its normaliser $\int p(\mathbf{y}|\mathbf{w})p(\mathbf{w}) d\mathbf{w}$ has no closed form. Requires approximations like [[laplace-approximation]] or [[mcmc]].
3. **[[laplace-approximation]]**
   - **Why:** Needs to find the MAP estimate (the mode of the posterior).
   - **Result:** Uses iterative optimization (e.g., Newton's method) to find the mode, then evaluates the Hessian at that point to fit a Gaussian.
4. **[[variational-inference]] & [[variational-autoencoder|VAEs]]**
   - **Why:** The Evidence Lower Bound ([[elbo]]) must be maximized. 
   - **Result:** VI uses iterative coordinate ascent or gradient descent. VAEs use stochastic gradient descent with backpropagation.
5. **[[mcmc]] (Markov Chain Monte Carlo)**
   - **Why:** Exact inference is intractable.
   - **Result:** Iteratively draws samples (e.g., Metropolis-Hastings or Gibbs Sampling) that eventually converge to the true posterior distribution.
6. **[[reinforcement-learning]]**
   - **Why:** The Bellman optimality equation is recursive.
   - **Result:** [[q-learning]] relies on iterative updates to approximate the true Q-values.

## Exam Synthesis
- **Spotting the difference:** If an exam question asks "Why is there no closed-form solution?", look for a non-linear function (like $\sigma$ or $\exp$) trapping the parameters. Mention that you cannot isolate the parameter algebraically when setting the derivative to zero.
- **Conjugacy is key:** To explicitly state *why* a Bayesian model has a closed-form posterior, you must use the phrase "conjugate prior".
- **The Trade-off:** Closed-form methods are fast and exact but severely limit the complexity of your model (mostly to linear/Gaussian assumptions). Iterative methods allow for highly flexible, non-linear models (like Deep Learning and VAEs) but are computationally expensive, require hyperparameter tuning (learning rate), and may get stuck in local optima.