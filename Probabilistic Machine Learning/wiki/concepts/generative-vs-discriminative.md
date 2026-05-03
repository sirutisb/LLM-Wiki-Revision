# Generative vs Discriminative Models

**Type:** principle
**Week:** 2
**Related:** [[naive-bayes]], [[logistic-regression]], [[bayesian-inference]], [[mle]]
**Source:** [[lecture-w2]]

## Definition
Generative models learn the joint distribution $p(\mathbf{x}, y) = p(\mathbf{x}|y)p(y)$ and use Bayes' rule to classify. Discriminative models directly learn the conditional $p(y|\mathbf{x})$.

## Motivation
The distinction shapes what each model learns, how many parameters it needs, and when it fails. This is a recurring exam question and a foundational concept for understanding the course models.

## How it works

### Generative Models
- Model: $p(y)$ and $p(\mathbf{x}|y)$.
- Classification: $\hat{y} = \arg\max_y p(y|\mathbf{x}) = \arg\max_y p(\mathbf{x}|y)p(y)$.
- Can sample new data $\mathbf{x}$ by first drawing $y$ then $\mathbf{x}|y$.
- Examples: Naive Bayes, Hidden Markov Models, VAEs (as generative models).

### Discriminative Models
- Model: $p(y|\mathbf{x})$ directly (or a decision boundary).
- Classification: $\hat{y} = \arg\max_y p(y|\mathbf{x})$.
- Cannot generate $\mathbf{x}$ from scratch.
- Examples: Logistic regression, neural networks, SVMs.

### Comparison Table

| Dimension | Generative | Discriminative |
|-----------|-----------|---------------|
| What is modelled | $p(\mathbf{x},y) = p(\mathbf{x}|y)p(y)$ | $p(y|\mathbf{x})$ |
| Parameters | More (must model full $\mathbf{x}$) | Fewer (only decision boundary) |
| Can generate data? | Yes | No |
| Handles missing features? | Naturally | Difficult |
| Accuracy (large data) | Often lower | Often higher |
| Training data efficiency | Better with small datasets (via prior) | Needs more data |
| Example | Naive Bayes | Logistic regression |

### When Does Generative Win?
- Small training sets: generative models incorporate prior structure.
- Missing data: can marginalise over missing features.
- Need for data generation or density estimation.

### When Does Discriminative Win?
- Large datasets: discriminative models make fewer assumptions → lower asymptotic error.
- When only the decision boundary matters.

## Key derivation
Naive Bayes vs Logistic Regression: it can be shown that Gaussian Naive Bayes implies a linear decision boundary of the same form as logistic regression, but NB estimates more parameters (per-class covariances) while LR directly estimates the boundary. LR is therefore more efficient with data.

## Parameters & intuition
The generative–discriminative gap narrows as data grows. Generative models are better "teachers" (can explain the data); discriminative models are better "classifiers" (optimise directly for accuracy).

## Connections
- [[naive-bayes]]: canonical generative classifier.
- [[logistic-regression]]: canonical discriminative classifier.
- [[hidden-markov-model]]: generative sequence model.
- [[variational-autoencoder]]: explicitly models generative process $p(z)p(x|z)$.

## Exam notes
- "What is the difference between generative and discriminative models?" — ⚠️ **past exam question**.
- Must give examples: Naive Bayes (generative), Logistic Regression (discriminative).
- Must know which model learns what: joint vs conditional.
- Formula status: conceptual question, no formula ⚠️
