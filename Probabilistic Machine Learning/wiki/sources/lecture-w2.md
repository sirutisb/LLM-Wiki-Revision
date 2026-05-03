# Week 2 — Linear Regression & Classification

**File:** `raw/text/COM3031_2526_week2.txt`
**Type:** lecture
**Week:** 2
**Concepts introduced:** [[linear-regression]], [[bayesian-linear-regression]], [[generalised-linear-models]], [[logistic-regression]], [[naive-bayes]], [[generative-vs-discriminative]], [[poisson-regression]]

## Summary
Week 2 extends Bayesian ideas to regression and classification. Linear regression is derived probabilistically via MLE; a Gaussian prior on weights gives Bayesian linear regression, connecting MAP to L2 regularisation. Generalised Linear Models (GLMs) extend this to non-Gaussian outputs (count data with Poisson, binary data with Logistic regression). The lecture then introduces two approaches to classification: discriminative (logistic regression, models $p(y|x)$) and generative (Naive Bayes, models $p(x,y)$).

## Key content

### Linear Regression (Probabilistic View)
- Simple model: $y = wx + \epsilon$, $\epsilon \sim \mathcal{N}(0, \sigma^2)$.
- Likelihood: $p(y_i|x_i, w, \sigma^2) \sim \mathcal{N}(wx_i, \sigma^2)$.
- MLE $\Rightarrow$ minimise sum of squared errors.

### Multiple Linear Regression
- $y_i = \mathbf{w}^\top \mathbf{x}_i + \epsilon$.
- MLE (normal equations): $\hat{\mathbf{w}}_{\text{MLE}} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$.

### Bayesian Linear Regression
- Prior on weights: $p(\mathbf{w}) = \mathcal{N}(\mathbf{w}_0, \boldsymbol{\Sigma}_0)$.
- Posterior (closed form via Gaussian conjugacy):
$$\boldsymbol{\Sigma}_n^{-1} = \boldsymbol{\Sigma}_0^{-1} + \frac{1}{\sigma^2}\mathbf{X}^\top\mathbf{X}, \qquad \mathbf{w}_n = \boldsymbol{\Sigma}_n\!\left(\boldsymbol{\Sigma}_0^{-1}\mathbf{w}_0 + \frac{1}{\sigma^2}\mathbf{X}^\top\mathbf{y}\right)$$
- MAP with Gaussian prior $\equiv$ L2-regularised least squares (ridge regression).

### Generalised Linear Models (GLMs)
- Keep linear predictor $\eta_i = \mathbf{w}^\top\mathbf{x}_i$, change the output distribution.
- **Link function** maps the linear predictor to the mean of the distribution.
- Example: Poisson regression for count data — $\log\lambda_i = \mathbf{w}^\top\mathbf{x}_i$ (log link).
- MLE for GLMs has no closed form; use iterative optimisation (gradient ascent, Newton–Raphson, IRLS).

### Classification: Discriminative vs Generative
- **Discriminative**: learn $p(y|x)$ directly. Example: logistic regression.
- **Generative**: learn $p(x|y)$ and $p(y)$; use Bayes' rule to get $p(y|x)$. Example: Naive Bayes.

### Logistic Regression
- Binary $y_i \in \{0,1\}$, link function is logit: $\log\frac{\theta_i}{1-\theta_i} = \mathbf{w}^\top\mathbf{x}_i$.
- Inverse link (sigmoid): $\theta_i = \sigma(\mathbf{w}^\top\mathbf{x}_i) = \frac{1}{1+e^{-\mathbf{w}^\top\mathbf{x}_i}}$.
- Log-likelihood (cross-entropy):
$$\ell(\mathbf{w}) = \sum_{i=1}^n [y_i\log\theta_i + (1-y_i)\log(1-\theta_i)]$$
- No closed form; use gradient ascent.
- **Bayesian logistic regression**: Gaussian prior on $\mathbf{w}$; posterior is intractable → approximate inference needed (Laplace, VI, MCMC).

### Naive Bayes
- Assumption: features are conditionally independent given the class.
$$p(\mathbf{x}|y=k) = \prod_{j=1}^D p(x_j|y=k)$$
- **Gaussian Naive Bayes**: each $p(x_j|y=k) = \mathcal{N}(\mu_{jk}, \sigma^2_{jk})$.
- Decision boundary: $\hat{y} = \arg\max_k [\log\pi_k + \sum_j \log p(x_j|y=k)]$.
- Variants: Bernoulli NB (binary features), Multinomial NB (count features).

## Key takeaways
- MLE for linear regression = minimising sum of squared errors.
- Bayesian linear regression has a closed-form posterior (Gaussian conjugacy).
- MAP with Gaussian prior = ridge regression: regularisation is a prior in disguise.
- GLMs handle non-Gaussian outputs via link functions; MLE requires iterative methods.
- Logistic regression: no closed-form MLE; gradients used.
- Naive Bayes is a generative classifier with strong (often violated) independence assumption.

## Exam relevance
- MLE for simple and multiple linear regression: **examinable** (univariate).
- Logistic regression mechanics (sigmoid, log-likelihood): **examinable** conceptually.
- Generative vs discriminative distinction: **examinable** (past exam question).
- "What is naïve about Naïve Bayes?": **examinable** (past question).
- "Why is logarithmic function not a suitable link for logistic regression?": **examinable**.
- Multivariate derivations NOT examinable.
- Formula sheet: Wk2 distribution formulas **will be given**.

## Links to concepts
- [[linear-regression]]: introduced here
- [[bayesian-linear-regression]]: introduced here
- [[generalised-linear-models]]: introduced here
- [[logistic-regression]]: introduced here
- [[naive-bayes]]: introduced here
- [[generative-vs-discriminative]]: introduced here
- [[poisson-regression]]: introduced here
