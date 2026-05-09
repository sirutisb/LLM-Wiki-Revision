# Bayesian Information Criterion (BIC)

**Type:** principle
**Week:** 3
**Related:** [[laplace-approximation]], [[bayesian-inference]], [[mle]], [[map]]
**Source:** [[lecture-w3]]

## Definition
The Bayesian Information Criterion (BIC) is an approximation to the log model evidence (marginal likelihood) derived via the Laplace approximation, penalising model complexity by the number of parameters.

## Motivation
Comparing models by likelihood alone favours more complex models (overfitting). The marginal likelihood $p(\mathcal{D}|M)$ provides a principled Bayesian comparison, but is intractable. BIC approximates $\log p(\mathcal{D}|M)$ analytically, enabling tractable model selection.

## How it works

### BIC Formula
$$\text{BIC}(M) = \log p(\mathcal{D}|\hat{\boldsymbol{\theta}}, M) - \frac{k}{2}\log n$$

Where:
- $\log p(\mathcal{D}|\hat{\boldsymbol{\theta}}, M)$: log-likelihood at the MLE $\hat{\boldsymbol{\theta}}$.
- $k$: number of parameters in model $M$.
- $n$: number of data points.

**Model selection**: choose the model with highest BIC.

### Equivalent Form (used in some presentations)
$$\text{BIC} = -2\log p(\mathcal{D}|\hat{\boldsymbol{\theta}}) + k\log n$$
(negated, so **lower is better** in this version — check sign convention used in lectures.)

## Key derivation

### Derivation from Laplace Approximation
Starting from the log marginal likelihood:
$$\log p(\mathcal{D}|M) = \log p(\mathcal{D}|\hat{\boldsymbol{\theta}}) + \log p(\hat{\boldsymbol{\theta}}) + \frac{k}{2}\log(2\pi) - \frac{1}{2}\log|\mathbf{H}|$$
where $\mathbf{H}$ is the Hessian of the negative log-likelihood at $\hat{\boldsymbol{\theta}}$.

BIC approximates the Hessian term as $\frac{k}{2}\log n$, dropping lower-order terms:
$$\log p(\mathcal{D}|M) \approx \log p(\mathcal{D}|\hat{\boldsymbol{\theta}}) - \frac{k}{2}\log n = \text{BIC}$$

### Automatic Occam's Razor
BIC penalises complexity:
- Data fit term ($\log p(\mathcal{D}|\hat{\boldsymbol{\theta}})$): favours complex models.
- Penalty term ($-\frac{k}{2}\log n$): disfavours models with many parameters.
- Balance: avoids both underfitting and overfitting.

## Parameters & intuition
- $k$ (number of parameters): each extra parameter costs $\frac{1}{2}\log n$ in log-evidence.
- $n$ (dataset size): penalty increases with data — with more data, simpler models preferred over complex ones (less uncertainty about the "truth").
- BIC is consistent: for large $n$, BIC selects the true model (if in the candidate set).

## Worked example sketch
Model A: $k=2$, $\log p(\mathcal{D}|\hat{\theta}) = -10$, $n=100$.
$\text{BIC}_A = -10 - \frac{2}{2}\log 100 = -10 - 4.6 = -14.6$

Model B: $k=5$, $\log p(\mathcal{D}|\hat{\theta}) = -8$, $n=100$.
$\text{BIC}_B = -8 - \frac{5}{2}\log 100 = -8 - 11.5 = -19.5$

→ Model A preferred (higher BIC = better Laplace-approximated log evidence).

## Connections
- [[laplace-approximation]]: BIC is derived from the Laplace approximation to the marginal likelihood.
- [[bayesian-inference]]: BIC approximates the Bayes factor for model comparison.
- [[mle]]: BIC uses the MLE log-likelihood as the data fit term.

## Exam notes
- BIC formula and its derivation from Laplace: ⚠️ **examinable** (conceptual).
- Know what each term represents (data fit vs complexity penalty).
- Know direction: higher BIC (first form) = better model.
- Formula status: no formula sheet for Week 3 ⚠️; BIC formula must be known from memory.
