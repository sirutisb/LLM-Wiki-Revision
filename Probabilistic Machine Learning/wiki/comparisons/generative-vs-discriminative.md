# Generative vs Discriminative Models

## Overview
This comparison distinguishes between two fundamental approaches to probabilistic classification. It is a frequent exam topic (⚠️ **Past Exam Question**) and is foundational for understanding the relationship between models like Naive Bayes and Logistic Regression.

The core difference lies in whether the model learns to **describe** the data (Generative) or merely **distinguish** between classes (Discriminative).

## Definition
Generative models learn the joint distribution $p(\mathbf{x}, y) = p(\mathbf{x}|y)p(y)$ and use Bayes' rule to classify. Discriminative models directly learn the conditional $p(y|\mathbf{x})$.

## Motivation
The distinction shapes what each model learns, how many parameters it needs, and when it fails. This is a recurring exam question and a foundational concept for understanding the course models.

## Comparison Table

| Dimension | Generative Models | Discriminative Models |
|-----------|-------------------|----------------------|
| **What is learned?** | Joint distribution $p(\mathbf{x}, y)$ | Conditional distribution $p(y|\mathbf{x})$ |
| **Equation** | $p(\mathbf{x}, y) = p(\mathbf{x}|y)p(y)$ | $p(y|\mathbf{x})$ directly |
| **Intuition** | Models how each class "looks" | Models where the decision boundary lies |
| **Classification** | Via Bayes' Rule: $p(y|\mathbf{x}) \propto p(\mathbf{x}|y)p(y)$ | Direct: $\hat{y} = \arg\max_y p(y|\mathbf{x})$ |
| **Capability** | Can generate new data samples | Classification only |
| **Data Efficiency** | Better for small datasets (incorporates structure) | Better for large datasets (fewer assumptions) |
| **Canonical Example**| [[naive-bayes]] | [[logistic-regression]] |

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

## When to use which

### Use Generative Models when:
- **Small Datasets:** They leverage the structure of $p(\mathbf{x}|y)$, which helps when labels are scarce.
- **Missing Data:** You can naturally marginalise over missing features.
- **Data Generation:** You actually need to produce new synthetic samples.
- **Outlier Detection:** Knowing what the data *should* look like helps identify anomalies.

### Use Discriminative Models when:
- **Large Datasets:** They generally achieve lower asymptotic error because they don't make potentially incorrect assumptions about the distribution of $\mathbf{x}$.
- **Accuracy is the only goal:** They optimise the decision boundary directly for prediction performance.
- **Complex Features:** It is often easier to model $p(y|\mathbf{x})$ than the high-dimensional joint distribution $p(\mathbf{x}, y)$.

## Synthesis

### The $p(x, y) = p(x|y)p(y)$ Decomposition
The generative approach's reliance on $p(x, y)$ is its defining feature. 
1. **$p(y)$ (The Prior):** Represents how common each class is (e.g., probability of "Rain" vs "No Rain").
2. **$p(x|y)$ (The Likelihood):** Describes the "generative process" — if we know the class is "Rain," what do the atmospheric features $x$ typically look like?

By multiplying these, the model builds a complete statistical "story" of the data. To classify, it simply asks which class "story" is the most likely explanation for the observed features.

### Parameters & intuition
The generative–discriminative gap narrows as data grows. Generative models are better "teachers" (can explain the data); discriminative models are better "classifiers" (optimise directly for accuracy).

### Key derivation
Naive Bayes vs Logistic Regression: it can be shown that Gaussian Naive Bayes implies a linear decision boundary of the same form as logistic regression, but NB estimates more parameters (per-class covariances) while LR directly estimates the boundary. LR is therefore more efficient with data.

## Course Connections
- **Week 2:** Comparison of [[naive-bayes]] (Generative) vs [[logistic-regression]] (Discriminative).
- **Week 7:** [[hidden-markov-model]] is a generative sequence model.
- **Week 8:** [[variational-autoencoder]] explicitly learns a generative process $p(z)p(x|z)$.

## Exam notes
- "What is the difference between generative and discriminative models?" — ⚠️ **past exam question**.
- Must give examples: Naive Bayes (generative), Logistic Regression (discriminative).
- Must know which model learns what: joint vs conditional.
- Formula status: conceptual question, no formula ⚠️