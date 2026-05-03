# Naive Bayes

**Type:** model
**Week:** 2
**Related:** [[bayesian-inference]], [[logistic-regression]], [[generative-vs-discriminative]], [[mle]]
**Source:** [[lecture-w2]]

## Definition
Naive Bayes is a generative classification model that applies Bayes' rule and assumes all features are conditionally independent given the class label.

## Motivation
Directly modelling $p(\mathbf{x}|y)$ and $p(y)$ separates the problem into tractable per-feature distributions. The conditional independence assumption makes parameter estimation feasible even in high dimensions, at the cost of model accuracy when features are correlated.

## How it works

### Generative Model
$$p(y, \mathbf{x}) = p(y)\prod_{j=1}^d p(x_j | y)$$

### Classification Rule (MAP)
$$\hat{y} = \arg\max_y p(y|\mathbf{x}) = \arg\max_y p(y)\prod_{j=1}^d p(x_j|y)$$
(denominator $p(\mathbf{x})$ is constant across classes, so we ignore it.)

In log form:
$$\hat{y} = \arg\max_y \left[\log p(y) + \sum_{j=1}^d \log p(x_j|y)\right]$$

### Parameter Estimation (MLE)
- **Class prior**: $\hat{p}(y=c) = \frac{n_c}{n}$ (fraction of training examples in class $c$).
- **Feature likelihood**: depends on feature type:
  - Discrete (categorical): $\hat{p}(x_j = v | y = c)$ = fraction of class-$c$ examples with feature $j = v$.
  - Continuous (Gaussian NB): $p(x_j|y=c) = \mathcal{N}(\mu_{jc}, \sigma_{jc}^2)$ fitted by MLE per class.

### Naive Assumption
$$p(\mathbf{x}|y) = \prod_{j=1}^d p(x_j|y) \quad \text{(features independent given label)}$$
- "Naive" because this is almost never exactly true in real data.
- Despite this, Naive Bayes often performs well in practice (text classification, spam filtering).

## Key derivation
Bayes' rule + conditional independence factorisation:
$$p(y|\mathbf{x}) \propto p(y)p(\mathbf{x}|y) = p(y)\prod_j p(x_j|y)$$

## Parameters & intuition
- One parameter set per (feature, class) pair.
- $p(y)$: class imbalance captured by the prior.
- If a feature value was never seen in class $c$ during training → zero probability → use Laplace smoothing to avoid zero products.

## Worked example sketch
Spam classification: $p(\text{spam}=1) = 0.4$, $p(\text{"free"}|\text{spam}) = 0.6$, $p(\text{"free"}|\text{ham}) = 0.1$.
$$p(\text{spam}|\text{"free"}) \propto 0.4 \times 0.6 = 0.24; \quad p(\text{ham}|\text{"free"}) \propto 0.6 \times 0.1 = 0.06$$
→ classify as spam (0.24 > 0.06).

## Connections
- [[generative-vs-discriminative]]: Naive Bayes is generative; models $p(y)$ and $p(\mathbf{x}|y)$.
- [[logistic-regression]]: discriminative counterpart; models $p(y|\mathbf{x})$ directly.
- [[bayesian-inference]]: uses Bayes' rule for classification.
- [[mle]]: parameters estimated by MLE (count-based for discrete features).

## Exam notes
- Conceptual comparison with logistic regression: ⚠️ **examinable** (generative vs discriminative).
- Know how to apply the classification rule given class priors and likelihoods.
- "What assumption does Naive Bayes make?" — conditional independence of features given class.
- Formula status: no formula sheet for Week 2 classification models ⚠️
