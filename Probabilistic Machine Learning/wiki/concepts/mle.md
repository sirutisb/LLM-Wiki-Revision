# Maximum Likelihood Estimation (MLE)

**Type:** algorithm
**Week:** 1
**Related:** [[map]], [[bayesian-inference]], [[linear-regression]], [[logistic-regression]]
**Source:** [[lecture-w1]], [[supp-mle-gaussian]], [[supp-mle-binomial]], [[supp-mle-simple-linear-regression]], [[supp-mle-multiple-linear-regression]]

## Definition
MLE finds the parameter values that maximise the probability (likelihood) of the observed data under the model.

## Motivation
The likelihood $L(\theta) = p(\mathcal{D}|\theta)$ measures how well parameters explain observed data. MLE picks $\hat{\theta}$ that makes the data most probable. It is the standard frequentist inference procedure.

## How it works
$$\hat{\theta}_{\text{MLE}} = \arg\max_\theta L(\theta) = \arg\max_\theta \prod_{i=1}^n p(y_i|\theta)$$

In practice: maximise the **log-likelihood** (same argmax, avoids numerical underflow):
$$\hat{\theta}_{\text{MLE}} = \arg\max_\theta \ell(\theta) = \arg\max_\theta \sum_{i=1}^n \log p(y_i|\theta)$$

Set $\frac{d\ell}{d\theta} = 0$ and solve for $\hat{\theta}$.

## Key derivation

**Gaussian MLE**: $y_i \sim \mathcal{N}(\mu, \sigma^2)$:
$$\hat{\mu}_{\text{MLE}} = \frac{1}{N}\sum_{i=1}^N y_i \qquad \hat{\sigma}^2_{\text{MLE}} = \frac{1}{N}\sum_{i=1}^N(y_i - \hat{\mu})^2$$
Full derivation: [[supp-mle-gaussian]].

**Binomial MLE**: $y$ heads in $n$ coin flips:
$$\hat{\theta}_{\text{MLE}} = \frac{y}{n}$$
Full derivation: [[supp-mle-binomial]].

**Simple linear regression MLE**: $y_i = wx_i + \epsilon$, $\epsilon \sim \mathcal{N}(0,\sigma^2)$:
$$\hat{w}_{\text{MLE}} = \frac{\sum_i x_iy_i}{\sum_i x_i^2}$$
Full derivation: [[supp-mle-simple-linear-regression]].

**Multiple linear regression MLE** (Normal Equations):
$$\hat{\mathbf{w}}_{\text{MLE}} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$$

⚠️ *Univariate MLE derivations examinable; multivariate NOT.*

## Parameters & intuition
- MLE gives a **single point estimate** — no uncertainty quantification.
- For Gaussian: MLE = sample mean and biased variance (divide by $N$).
- For linear regression: MLE = OLS (ordinary least squares).
- MLE is a special case of MAP with a flat (uniform) prior.

## Worked example sketch
*Coin flipped 10 times, 7 heads. MLE for $\theta$:* $\hat{\theta} = 7/10 = 0.7$.

*Gaussian, 5 observations $(2, 4, 4, 4, 6)$:* $\hat{\mu} = 4$, $\hat{\sigma}^2 = \frac{1}{5}\sum(y_i-4)^2 = 2$.

## Connections
- Compare with [[map]]: MAP = MLE + log-prior term; regularises the estimate.
- MLE is the frequentist limit of Bayesian inference with a flat prior.
- Minimising negative log-likelihood = maximising likelihood (same objective).
- Cross-entropy loss in classification = negative log-likelihood.
- For GLMs (Poisson, logistic): MLE has no closed form; requires iterative optimisation.

## Exam notes
- Derivations for Gaussian and Binomial: ⚠️ examinable.
- Derivation for simple linear regression: ⚠️ examinable.
- Multiple linear regression: Normal Equations result required, derivation NOT examinable.
- **Pitfall**: $\hat{\sigma}^2_{\text{MLE}} = \frac{1}{N}\sum(y_i-\hat{\mu})^2$ divides by $N$, not $N-1$ (biased).
- Formula status: Gaussian, Binomial pdfs will be given ✅
