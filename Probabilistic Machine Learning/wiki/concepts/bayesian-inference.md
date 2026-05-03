# Bayesian Inference

**Type:** framework
**Week:** 1
**Related:** [[mle]], [[map]], [[conjugate-priors]], [[laplace-approximation]], [[variational-inference]], [[mcmc]]
**Source:** [[lecture-w1]], [[supp-beta-binomial]], [[supp-map-gaussian]]

## Definition
Bayesian inference treats model parameters as random variables and computes a posterior distribution $p(\theta|\mathcal{D})$ that combines a likelihood and a prior via Bayes' rule.

## Motivation
MLE and MAP give only point estimates — they cannot quantify parameter uncertainty, cannot produce calibrated predictions, and are vulnerable to overfitting with small datasets. Bayesian inference addresses all three by maintaining a full distribution over parameters.

## How it works
**Bayes' rule**:
$$p(\theta|\mathcal{D}) = \frac{p(\mathcal{D}|\theta)\,p(\theta)}{p(\mathcal{D})}$$

Four components:
| Term | Name | Role |
|------|------|------|
| $p(\mathcal{D}\|\theta)$ | Likelihood | How well parameters explain the data |
| $p(\theta)$ | Prior | Beliefs before seeing data |
| $p(\theta\|\mathcal{D})$ | Posterior | Updated beliefs after seeing data |
| $p(\mathcal{D}) = \int p(\mathcal{D}\|\theta)p(\theta)\,d\theta$ | Marginal likelihood (evidence) | Normalising constant; usually intractable |

Because $p(\mathcal{D})$ is constant w.r.t. $\theta$:
$$p(\theta|\mathcal{D}) \propto p(\mathcal{D}|\theta)\,p(\theta)$$

**Posterior predictive distribution**:
$$p(y'|\mathcal{D}) = \int p(y'|\theta)\,p(\theta|\mathcal{D})\,d\theta$$
Integrates over parameter uncertainty → produces calibrated, uncertainty-aware predictions.

## Key derivation
See [[supp-map-gaussian]] for MAP (point estimate of posterior mode).
See [[supp-beta-binomial]] for the closed-form Beta-Binomial posterior.

The key identity:
$$\log p(\theta|\mathcal{D}) = \log p(\mathcal{D}|\theta) + \log p(\theta) + \text{const}$$
(posterior = likelihood × prior, up to normalisation).

⚠️ *No formula given for Bayes' rule in the exam; must know from memory.*

## Parameters & intuition

**Prior types**:
- Non-informative: $p(\theta) \approx \text{const}$ (very large variance) → posterior ≈ likelihood.
- Weakly informative: moderate variance — regularises but doesn't dominate.
- Informative: small variance — strong belief; useful with little data.

**Effect of data size**:
- $n \to 0$: posterior ≈ prior.
- $n \to \infty$: posterior concentrates on MLE; prior is washed out.

## Worked example sketch
*Exam-type question*: Given Poisson likelihood $p(y|\lambda) \propto \lambda^y e^{-\lambda}$ and Gamma prior $\lambda \sim \text{Gamma}(\alpha, \beta)$, find the posterior.

Solution: $p(\lambda|y) \propto \lambda^{y+\alpha-1}e^{-(\beta+1)\lambda}$ → Gamma$(\alpha + y,\, \beta + 1)$.
(See [[lecture-w10]] for the $n > 1$ version.)

## Connections
- Builds on [[likelihood]] (frequentist) and adds [[conjugate-priors]] for tractability.
- When posterior is intractable: use [[laplace-approximation]] (local Gaussian), [[variational-inference]] (global optimisation), or [[mcmc]] (sampling).
- [[map]] is a point estimate of the posterior mode.

## Exam notes
- **Conceptual**: "What are the advantages of Bayesian inference over MLE/MAP?" — posterior uncertainty, credible intervals, posterior predictive.
- **Derivation**: univariate posterior (conjugate prior case) is examinable. ⚠️
- **Formula sheet**: Gaussian and Binomial pdfs will be given (Weeks 1–2).
- **Common pitfall**: the unnormalised posterior $p(\mathcal{D}|\theta)p(\theta)$ is NOT a probability distribution and cannot be used directly for probabilistic statements.
- Formula status: Bayes' rule must be known from memory ⚠️
