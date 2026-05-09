# Practice Question: Beta–Binomial Reliability Analysis

**Topic:** Bayesian Inference / Conjugate Priors
**Week:** 1
**Difficulty:** ⭐ (Introductory)
**Status:** 🟢 Unsolved

---

It is great to see you diving into the Week 1 material for COM3031. Conjugacy is a powerful tool because it turns what could be a messy calculus problem into a simple bookkeeping exercise. Since you are focusing on high-performance applications and probabilistic machine learning, mastering these analytic updates is a vital first step before moving on to more complex approximation methods like MCMC or Variational Inference.

Here is a problem based on the canonical **Beta–Binomial** example discussed in your notes.

---

## The Problem: Reliability Analysis

Suppose you are developing a new high-frequency data ingestion module. You want to estimate $\theta$, the probability that a specific packet is processed within a 10-microsecond window.

### 1. The Likelihood

You assume the number of packets $y$ processed within the time limit out of $n$ total packets follows a **Binomial distribution**:

$$p(y|\theta) = \binom{n}{y} \theta^y (1-\theta)^{n-y}$$

### 2. The Prior

Before running any tests, you choose a **Beta distribution** as your prior for $\theta$. You decide to use a "Flat" or **Uniform prior**, which corresponds to $Beta(\alpha=1, \beta=1)$.

### 3. The Data

You run a test batch of $n = 50$ packets. You observe that $y = 42$ of them were successfully processed within the 10-microsecond window.

---

### Your Tasks:

1. **Identify the Posterior:** State the name of the posterior distribution and provide its updated hyperparameters, namely $\alpha_{post}$ and $\beta_{post}$.
2. **Calculate the Point Estimate:** Based on the properties of the Beta distribution, calculate the **posterior mean** for $\theta$.
3. **The Intuition Check:** In the context of "pseudo-counts," what do the original prior hyperparameters ($\alpha=1, \beta=1$) represent regarding your "prior knowledge" before you saw the 50 packets?

How would you like to proceed with the derivation?

---

## Solution Space
*Double-click to edit and add your derivation here.*

---
**Related:** [[concepts/conjugate-priors]], [[concepts/bayesian-inference]], [[derivations/beta-binomial-posterior]]
