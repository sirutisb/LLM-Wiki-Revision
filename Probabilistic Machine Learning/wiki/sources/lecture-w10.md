# Week 10 — Exam Preparation & Course Review

**File:** `raw/text/COM3031_2526_Week10_Summary.txt`
**Type:** lecture
**Week:** 10
**Concepts introduced:** *(review only — no new concepts)*

## Summary
Week 10 is a course review and exam preparation session. It covers the exam format, specifies exactly which topics and derivations are examinable, walks through past exam questions with worked solutions, and provides a high-level recap of each week's key ideas. This is the authoritative source for exam scope.

## Exam Format
- **Closed-book**, 2 hours, May 2026.
- Answer **all** questions.
- Approved non-programmable scientific calculators permitted.
- Question types: (1) conceptual/bookwork, (2) selected derivations, (3) practical problem-solving.

## Examinable Topics by Week

| Week | Topic | Formulas given? | Derivations examinable? |
|------|-------|----------------|------------------------|
| 1 | Bayesian inference (MLE, MAP, conjugate priors) | ✅ Yes | ✅ Univariate only |
| 2 | Linear regression & classification | ✅ Yes | ✅ Univariate only |
| 3 | Laplace approximation | ⚠️ No | ⚠️ Univariate only; multivariate NOT |
| 4 | Variational approximation | ⚠️ No | ⚠️ ELBO derivation only |
| 5 | MCMC | ⚠️ No | ❌ Not examinable |
| 6 | Information Theory | ✅ Yes | ❌ Not examinable |
| 7 | Hidden Markov Models (Forward + Viterbi only) | ⚠️ No | ❌ Not examinable |
| 8 | Variational Autoencoders | ⚠️ No | ❌ Not examinable |
| 9 | Reinforcement Learning (bandits + Q-learning only) | ⚠️ No | ❌ Not examinable |

## Key Revision Points per Topic

### Week 1 — Bayesian Inference
- MLE derivation (univariate Gaussian and Binomial) — examinable.
- MAP derivation (univariate) and conjugate prior proof — examinable.
- Advantages of Bayesian inference over MLE/MAP.
- Predictive distribution: conceptual understanding.
- Past question: "What is a conjugate prior? State the advantage."

### Week 2 — Regression & Classification
- Linear regression MLE; Bayesian linear regression (MAP = ridge).
- Generative vs discriminative distinction.
- Naïve about Naïve Bayes.
- Past question: "Why is a log function not a suitable link for logistic regression?"

### Week 3 — Laplace Approximation
- Core idea: Gaussian at MAP with variance = inverse curvature.
- Past question: "Main use + one limitation of Laplace approximation."
- Worked example: given $p(\theta|y)$, find MAP and Laplace variance.

### Week 4 — Variational Inference / ELBO
- ELBO derivation from KL decomposition.
- ELBO = expected log-likelihood − KL to prior.
- Maximising ELBO ≡ minimising KL.

### Week 5 — MCMC
- Difference between Laplace, VI, and MCMC.
- Rejection vs importance sampling (key difference + one limitation each).
- MH algorithm steps (conceptual).

### Week 6 — Information Theory
- KL divergence meaning; cross-entropy = entropy + KL.
- Entropy comparison between distributions.

### Week 7 — Hidden Markov Models
- Forward algorithm: compute $P(O|\lambda)$.
- Viterbi algorithm: find best state sequence.
- Numerical worked examples.

### Week 8 — VAEs
- AE vs VAE; ELBO structure.

### Week 9 — Reinforcement Learning
- ε-greedy action selection; sample-average Q estimates.
- Q-learning update formula; numerical worked examples.

## Worked Exam Solutions in Week 10

### Conjugacy example (Poisson-Gamma)
- Posterior: $\lambda|y \sim \text{Gamma}(\alpha + \sum y_i, \beta + n)$.
- With $n=1, y=10, \alpha=25, \beta=3$: $\alpha_{\text{new}}=35$, $\beta_{\text{new}}=4$, $\mathbb{E}[\lambda|y]=8.75$.

### Laplace approximation example
- $p(\theta|y) = \theta^y(1-\theta)^{n-y}$. MAP: $\hat{\theta} = y/n$. Variance: $\sigma^2 = \frac{y(n-y)}{n^3}$.

### Q-learning example
- $\alpha = 0.6$, $\gamma = 0.4$. Update Q-table step by step from observed transitions.

### HMM example
- Identify transition/emission/initial matrices from a diagram.
- Enumerate possible state sequences given observations.

## Exam relevance
- This file **is** the exam specification — read it carefully before revising.

## Links to concepts
- All concepts — this is the review
