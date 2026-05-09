# Naive Bayes Variants

## Overview
Naive Bayes is a family of algorithms that share the conditional independence assumption. The primary difference between variants is the **distribution** used to model the feature likelihood $p(x_j | y=k)$.

## Comparison Table

| Feature Type | Model Variant | Likelihood $p(x_j | y=k)$ | Typical Use Case |
| :--- | :--- | :--- | :--- |
| **Continuous** | **Gaussian NB** | Gaussian PDF ($\mathcal{N}$) | Physical measurements (height, weight, temperature) |
| **Binary** | **Bernoulli NB** | Bernoulli ($p$ or $1-p$) | Document classification (word present / absent) |
| **Count / Integer** | **Multinomial NB** | Multinomial / Categorical | Document classification (word frequencies / bag-of-words) |

## Key Differences

### 1. Feature Representation
- **Gaussian:** $x_j \in \mathbb{R}$. We model the probability density at a specific point.
- **Bernoulli:** $x_j \in \{0, 1\}$. We model the probability of a feature occurring.
- **Multinomial:** $x_j \in \{0, 1, 2, \dots\}$. We model the probability of observing a specific sequence of counts.

### 2. Decision Boundaries
- **Gaussian NB:** Can be linear or **quadratic (curved)** depending on whether variances are shared across classes.
- **Bernoulli/Multinomial NB:** Usually result in **linear** decision boundaries in log-space.

### 3. Parameters
- **Gaussian:** Needs mean $\mu$ and variance $\sigma^2$ for every (feature, class) pair.
- **Bernoulli:** Needs a single probability $p$ for every (feature, class) pair.
- **Multinomial:** Needs a probability vector for every class across all features.

## When to use which?
- Use **Gaussian** when your data is "natural" measurements where values are spread around a mean.
- Use **Bernoulli** for "hit or miss" data. In text, this means you only care *if* a word appeared, not how many times.
- Use **Multinomial** for "frequency" data. In text, this is more common as it accounts for word importance (frequent words in one class vs another).

## Synthesis
While the "Naive" assumption (conditional independence) simplifies the model significantly by ignoring feature correlations, the choice of distribution (Gaussian, Bernoulli, or Multinomial) allows Naive Bayes to be adapted to almost any type of input data. The core logic—multiplying likelihoods by a prior and applying Bayes' rule—remains identical.
