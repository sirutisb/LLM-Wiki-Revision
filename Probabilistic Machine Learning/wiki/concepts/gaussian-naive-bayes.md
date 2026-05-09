# Gaussian Naive Bayes

**Type:** model
**Week:** 2
**Related:** [[naive-bayes]], [[mle]], [[linear-regression]]
**Source:** [[lecture-w2]]

## Definition
Gaussian Naive Bayes (GNB) is a variant of the Naive Bayes classifier designed for continuous features, where each feature is assumed to follow a Gaussian (normal) distribution within each class.

## Motivation
Standard Naive Bayes handles discrete data (like word counts) using frequency tables. For real-valued data like height, weight, or sensor readings, we need a continuous probability density function (PDF) to model $p(x_j | y=c)$. The Gaussian distribution is the natural choice for modelling continuous noise or measurements.

## How it works

### The Model
Like all Naive Bayes models, GNB assumes conditional independence:
$$p(\mathbf{x}|y=k) = \prod_{j=1}^d p(x_j | y=k)$$

In GNB, we define each individual feature likelihood as a Gaussian PDF:
$$p(x_j | y=k) = \mathcal{N}(x_j | \mu_{jk}, \sigma_{jk}^2) = \frac{1}{\sqrt{2\pi\sigma_{jk}^2}} \exp\left( -\frac{(x_j - \mu_{jk})^2}{2\sigma_{jk}^2} \right)$$

### Parameters (Estimated via MLE)
For each class $k$ and each feature $j$, we estimate:
- **Mean** ($\mu_{jk}$): The average value of feature $j$ for all training samples in class $k$.
- **Variance** ($\sigma_{jk}^2$): The variance of feature $j$ for samples in class $k$.
- **Prior** ($\pi_k$): $p(y=k)$, typically the fraction of samples in class $k$.

### Classification Rule (Log-Space)
To avoid underflow, we use the log of the MAP rule:
$$\hat{y} = \arg\max_k \left[ \log \pi_k + \sum_{j=1}^d \log \mathcal{N}(x_j | \mu_{jk}, \sigma_{jk}^2) \right]$$

Expanding the log-Gaussian:
$$\hat{y} = \arg\max_k \left[ \log \pi_k - \sum_{j=1}^d \left( \frac{1}{2} \log(2\pi\sigma_{jk}^2) + \frac{(x_j - \mu_{jk})^2}{2\sigma_{jk}^2} \right) \right]$$

## Decision Boundary
- Unlike Logistic Regression (which has a linear boundary), Gaussian Naive Bayes often has a **curved (quadratic)** decision boundary.
- This happens because the variances $\sigma_{jk}^2$ can differ between classes, causing the boundary to "bend" towards the class with higher variance.
- If all classes share the same variance for a feature, the boundary becomes linear (similar to LDA).

## Connection to General Naive Bayes
The "Naive" part is identical: we assume features don't interact ($p(\text{height}, \text{weight} | \text{male}) = p(\text{height} | \text{male})p(\text{weight} | \text{male})$). The only difference is the **likelihood function**:
- **Discrete NB:** Uses counts/probabilities from a table.
- **Gaussian NB:** Uses the value $x_j$ as an input to a Gaussian formula.

## Worked Example Sketch
Predicting gender (M/F) from height $h$.
- Training: $\mu_{h,M}=175, \sigma_{h,M}=10$; $\mu_{h,F}=160, \sigma_{h,F}=10$.
- Test: $h=170$.
- Calculate $p(h=170|M)$ and $p(h=170|F)$ using the normal PDF.
- Multiply by priors $p(M), p(F)$ and pick the highest.

## Exam Notes
- **What is "Naive"?** The assumption of conditional independence given the class.
- **Boundary Type:** Quadratic/Curved (due to class-specific variances).
- **Formula status:** ⚠️ No formula sheet for Week 2. You should know the Gaussian PDF form and how it fits into the NB product rule.
