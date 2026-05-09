# Logistic Regression

**Type:** model
**Week:** 2
**Related:** [[linear-regression]], [[generalised-linear-models]], [[bayesian-inference]], [[naive-bayes]], [[generative-vs-discriminative]]
**Source:** [[lecture-w2]]

## Definition
Logistic regression is a discriminative binary classification model that models the probability of class $y=1$ as a sigmoid function of a linear predictor, trained by maximum likelihood.

## Motivation
Linear regression with Gaussian noise is unsuitable for binary outcomes — it can predict probabilities outside $[0,1]$. Logistic regression is a GLM that uses the Bernoulli distribution and logit link to correctly model binary data.

### From Bernoulli Model to Logistic Regression
1. **Bernoulli model (No Features):** We have binary outcomes $y_i \in \{0, 1\}$. We assume each observation is a Bernoulli trial with the *same* constant probability $\theta$. The MLE is simply the proportion of class 1 in the data. The limitation is that it cannot adapt predictions to different inputs.
2. **Input-dependent probability:** We replace the constant probability with an input-dependent probability $\theta_i = p(y_i=1 | \mathbf{x}_i)$.
3. **Attempt a linear model:** Try $\theta_i = w_0 + w_1 x_{i1} + \dots$ (or $\mathbf{w}^\top \mathbf{x}_i$). 
   - *Problem:* Probabilities must satisfy $0 \leq \theta_i \leq 1$, but linear functions are unbounded.
4. **Transform the probability:** We need a quantity that can take any real value $(-\infty, +\infty)$ but maps back to a valid probability in $[0,1]$.
   - *Solution:* Use **log-odds (logit)**: $\log \frac{\theta_i}{1-\theta_i} = \mathbf{w}^\top \mathbf{x}_i$. This is the key modelling step in logistic regression.

## How it works

### Model
$$\theta_i = P(y_i=1|x_i) = \sigma(\mathbf{w}^\top\mathbf{x}_i) = \frac{1}{1+e^{-\mathbf{w}^\top\mathbf{x}_i}}$$
- **Linear predictor**: $\eta_i = \mathbf{w}^\top\mathbf{x}_i$.
- **Link function** (logit): $\log\frac{\theta_i}{1-\theta_i} = \eta_i$.
- **Inverse link** (sigmoid): $\theta_i = \sigma(\eta_i) = 1/(1+e^{-\eta_i})$.
- **Prediction**: $\hat{y}_i = 1$ if $\theta_i \geq 0.5$ (i.e. $\eta_i \geq 0$), else 0.

### Why logit and not log?
- Log link: maps linear predictor to $(0,\infty)$ — not a valid probability range.
- Logit link: maps linear predictor $\in (-\infty, +\infty)$ to probability $\in (0,1)$ ✓.

### Log-Likelihood
$$\ell(\mathbf{w}) = \sum_{i=1}^n [y_i\log\theta_i + (1-y_i)\log(1-\theta_i)]$$
- This is the **binary cross-entropy** (negative cross-entropy loss).
- Maximising log-likelihood = minimising cross-entropy loss.

### MLE
$$\hat{\mathbf{w}}_{\text{MLE}} = \arg\max_\mathbf{w} \ell(\mathbf{w})$$
- No closed-form solution (sigmoid is non-linear).
- Use iterative methods: gradient ascent, Newton–Raphson, L-BFGS.

### Bayesian Logistic Regression
Key idea: Treat the weights as random variables, not fixed values.
- **Likelihood** (same as logistic regression): $y_i \sim \text{Bernoulli}(\theta_i)$, where $\theta_i = \sigma(\mathbf{w}^\top\mathbf{x}_i)$.
- **Prior on weights:** $\mathbf{w} \sim \mathcal{N}(\mathbf{w}_0, \boldsymbol{\Sigma}_0)$.
- **Posterior:** $p(\mathbf{w}|\mathcal{D}) \propto p(\mathbf{y}|\mathbf{X}, \mathbf{w})p(\mathbf{w})$.
- **Note:** There is no closed-form for the posterior (sigmoid makes likelihood non-Gaussian). The posterior needs to be approximated using: [[mcmc]] (Markov Chain Monte Carlo), [[laplace-approximation]], or [[variational-inference]].

## Key derivation
No closed-form MLE — derivation involves showing $\nabla_\mathbf{w}\ell = \sum_i(y_i-\theta_i)\mathbf{x}_i$ (difference between true and predicted class × input).

## Parameters & intuition
- $\mathbf{w}$: weights — each $w_j$ controls how much feature $x_j$ influences the log-odds.
- Large positive $w_j$: feature $x_j$ strongly predicts class 1.
- Decision boundary: $\mathbf{w}^\top\mathbf{x} = 0$ — a hyperplane in feature space.

## Worked example sketch
*1D*: $P(y=1|x) = \sigma(w_0 + w_1 x)$. If $w_0 = 0$, $w_1 = 1$: decision boundary at $x=0$; $P(y=1|x=2) = \sigma(2) \approx 0.88$.

## Connections
- Compare with [[naive-bayes]] ([[generative-vs-discriminative]]): logistic regression models $p(y|x)$ directly (discriminative); Naive Bayes models $p(x|y)p(y)$ (generative).
- [[generalised-linear-models]]: logistic regression is a GLM with Bernoulli distribution and logit link.
- [[linear-regression]]: special case with Gaussian distribution and identity link.

## Exam notes
- "Why is the log function not a suitable choice for the link function in logistic regression?": ⚠️ **past exam question**.
  - Log maps to $(0,\infty)$, not $[0,1]$. Probabilities must be in $[0,1]$.
- Logistic regression trains by MLE; no closed form — requires iterative optimisation.
- "What is the difference between generative and discriminative models?": ⚠️ **past exam question**.
- Formula status: logistic/sigmoid formulas — Gaussian pdf given ✅; logistic function should be known ⚠️
