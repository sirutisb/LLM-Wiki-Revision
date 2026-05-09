# Exam Overview: Topics & Formulas

**Module:** COM3031 — Probabilistic Machine Learning
**Exam Date:** May 2026
**Format:** 2-hour closed-book written exam (70% of total grade)
**Permitted:** Scientific calculators

---

## Formula Sheet Policy

| Weeks | Topic Scope | Formula Status |
|-------|-------------|----------------|
| **1 – 2** | MLE, MAP, Linear Regression | ✅ Common distribution formulas **will** be provided. |
| **3 – 9** | Laplace, VI, MCMC, Info Theory, HMM, VAE, RL | ⚠️ **No formulas given.** Must know results and derivations from memory. |

### Critical Requirement: Weeks 3–4
For the exam, you must be able to derive the following from scratch as **no formulas** are provided:
- **Laplace Approximation:** All steps to fit a Gaussian at the MAP.
- **ELBO (Evidence Lower Bound):** Full derivation from KL divergence or Jensen's inequality.
- **Mean-Field Update Rule:** The coordinate ascent variational inference (CAVI) update logic.

---

## Examinable Topics & Revision Priority

Ordered by weight (derived from Week 10 review):

1. **Bayesian Inference (Week 1):** MLE, MAP, conjugate priors.
2. **Linear Regression & Classification (Week 2):** OLS, Ridge (MAP), Generative vs Discriminative.
3. **Variational Inference & ELBO (Week 4):** Mean-field, KL divergence, coordinate ascent.
4. **HMMs (Week 7):** Forward algorithm and Viterbi algorithm **only**.
5. **Laplace Approximation (Week 3):** Local Gaussian fit, Hessian calculation.
6. **MCMC (Week 5):** Metropolis-Hastings, Gibbs sampling, Monte Carlo integration.
7. **Information Theory (Week 6):** Entropy, KL, Mutual Information, Cross-entropy.
8. **VAEs (Week 8):** ELBO for latent variables, reparameterization trick.
9. **Reinforcement Learning (Week 9):** Multi-armed bandits (ε-greedy), Q-learning (Bellman).

---

## Techniques to Derive from Scratch

These are high-probability exam questions where you are expected to show full mathematical working:

- **MLE/MAP:** Gaussian (mean/var), Binomial, Linear Regression (Normal Equations).
- **Approximations:** Laplace steps, ELBO derivation.
- **Algorithms:** HMM Forward recursion, Viterbi recursion.
- **RL:** Q-learning update rule.

---

## Exam Question Types
1. **Conceptual / Bookwork:** Definitions, motivations, "Why use X over Y?".
2. **Selected Derivations:** Mathematical proofs of results (see list above).
3. **Practical Problem-Solving:** Numerical calculations (e.g., small HMM, simple MCMC step).
