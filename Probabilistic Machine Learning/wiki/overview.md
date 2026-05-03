# COM3031 Probabilistic Machine Learning — Module Overview

**Module:** COM3031 | **Lecturer:** Dr Zeyu Fu | **University of Exeter, Term 2 2025-2026**
**Exam:** 2-hour closed-book, May 2026 (70% of grade)

---

## What this module is about

Probabilistic machine learning treats models as probability distributions rather than point estimates. The central idea is **Bayesian inference**: instead of finding one best parameter value, we maintain a distribution over parameters and update it with data via Bayes' theorem. This gives us uncertainty quantification, principled regularisation, and a coherent framework that extends to complex latent-variable models.

The module builds from first principles (MLE → MAP → full Bayes) through approximate inference methods (Laplace, Variational, MCMC) and then into structured models (HMMs, VAEs) and sequential decision-making (RL).

---

## Topic map

```
FOUNDATIONS
  MLE → MAP → Bayesian Inference (Week 1)
     ↓
  Linear Regression (Week 2) → Classification (Week 2)

APPROXIMATE INFERENCE                    (Weeks 3–5, exam: no formulas given)
  Laplace Approximation (Week 3)
  Variational Inference / ELBO (Week 4)
  MCMC / Metropolis-Hastings (Week 5)

INFORMATION THEORY                       (Week 6, some formulas given)
  Entropy, KL Divergence, Mutual Information

STRUCTURED / LATENT VARIABLE MODELS     (Weeks 7–8)
  Hidden Markov Models (Week 7)  ← forward algorithm + Viterbi only
  Variational Autoencoders (Week 8)  ← builds on Variational Inference

SEQUENTIAL DECISION-MAKING              (Week 9)
  Reinforcement Learning: Bandits + Q-learning only
```

---

## Conceptual thread

| Stage | Key question | Answer |
|-------|-------------|--------|
| MLE | What parameter best explains the data? | $\hat{\theta} = \arg\max_\theta p(D\|\theta)$ |
| MAP | What parameter is most probable given the data and a prior? | $\hat{\theta} = \arg\max_\theta p(\theta\|D) \propto p(D\|\theta)p(\theta)$ |
| Full Bayes | What is the full posterior distribution? | $p(\theta\|D) = p(D\|\theta)p(\theta)/p(D)$ |
| Approximate Bayes | Posterior is intractable — how to approximate? | Laplace (Gaussian fit) / VI (optimise a simpler $q$) / MCMC (sample) |
| Latent variables | Data has hidden structure — how to learn it? | EM, HMMs (discrete latents), VAEs (continuous latents + VI) |
| Decisions | How to act under uncertainty? | RL: bandits (exploration/exploitation), MDPs + Q-learning |

---

## Exam-critical techniques (must derive from scratch)

These have **no formula given** — understand the full derivation:

- MLE for Gaussian (mean and variance)
- MAP for Gaussian with Gaussian prior
- MLE for linear regression (normal equations)
- Laplace approximation steps
- ELBO derivation (from KL divergence)
- Variational inference for a simple model
- HMM forward algorithm (recursion)
- Viterbi algorithm (recursion)
- VAE ELBO and reparameterisation trick
- Epsilon-greedy bandit strategy
- Q-learning update rule

---

## Sources

| Week | Lecture | Supplementary notes |
|------|---------|---------------------|
| 1 | [[lecture-w1]] | [[supp-beta-binomial]], [[supp-mle-binomial]], [[supp-mle-gaussian]], [[supp-map-gaussian]] |
| 2 | [[lecture-w2]] | [[supp-mle-simple-lr]], [[supp-mle-multiple-lr]] |
| 3 | [[lecture-w3]] | — |
| 4 | [[lecture-w4]] | [[supp-elbo]] |
| 5 | [[lecture-w5]] | — |
| 6 | [[lecture-w6]] | — |
| 7 | [[lecture-w7]] | [[supp-hmm-forward-viterbi]] |
| 8 | [[lecture-w8]] | — |
| 9 | [[lecture-w9]] | — |
| 10 | [[lecture-w10]] | — |

---

## Key textbooks

- **Bishop** — *Pattern Recognition and Machine Learning* (2006) — primary reference
- **MacKay** — *Information Theory, Inference, and Learning* (2006)
- **Murphy** — *Machine Learning: A Probabilistic Perspective* (2012)
- **Russell & Norvig** — *Artificial Intelligence: A Modern Approach, 4th ed.* (2016)
