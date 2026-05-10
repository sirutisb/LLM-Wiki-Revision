# MCMC Algorithms — Synthesis

**Related:** [[mcmc]], [[metropolis-hastings]], [[gibbs-sampling]]
**Source:** [[lecture-w5]]

## Overview
Markov Chain Monte Carlo (MCMC) algorithms are a class of methods used to sample from intractable posterior distributions by constructing a Markov chain whose stationary distribution is the target posterior. The core MCMC algorithms covered in Week 5 differ primarily in how they propose new states and how they determine whether to accept them. Understanding their distinctions is conceptually examinable.

## Comparison table

| Feature / Algorithm | Metropolis-Hastings (MH) | Metropolis | Gibbs Sampling |
|---------------------|--------------------------|------------|----------------|
| **Proposal Distribution ($q$)** | Asymmetric or symmetric (general $q(\theta'\|\theta)$) | Symmetric only ($q(\theta'\|\theta) = q(\theta\|\theta')$) | Exact full conditional distributions |
| **Acceptance Ratio ($A$)** | $\frac{\tilde{p}(\theta') q(\theta^{(t-1)}\|\theta')}{\tilde{p}(\theta^{(t-1)}) q(\theta'\|\theta^{(t-1)})}$ | $\frac{\tilde{p}(\theta')}{\tilde{p}(\theta^{(t-1)})}$ | 1 (always accepts) |
| **Acceptance Step** | Probabilistic: Accept with prob $\min(1, A)$ | Probabilistic: Accept with prob $\min(1, A)$ | Deterministic acceptance (no rejections) |
| **Tuning Required** | Yes (proposal type, variance/step size $\sigma$) | Yes (proposal variance/step size $\sigma$) | No proposal tuning required |
| **Prerequisites** | Can evaluate target unnormalised posterior $\tilde{p}(\theta)$ | Can evaluate target unnormalised posterior $\tilde{p}(\theta)$ | Must be able to sample from exact full conditionals |
| **Update Mechanism** | Usually updates all dimensions simultaneously | Usually updates all dimensions simultaneously | Updates one dimension (or block) at a time |

## When to use which

- **Metropolis-Hastings:** Use as the general-purpose fallback when you can evaluate the unnormalised posterior, but the proposal distribution needs to be tailored (e.g., asymmetric proposals) to efficiently explore a complex space.
- **Metropolis (Special case of MH):** Use when a simple symmetric proposal (like a Gaussian random walk) is sufficient to explore the posterior. It simplifies the acceptance ratio calculation since the proposal terms cancel out.
  - *Why it is useful:* (1) Very simple to implement. (2) Requires only the unnormalised posterior. (3) Forms the foundation of many MCMC methods.
- **Gibbs Sampling (Special case of MH):** Use when working with conjugate priors or conditionally tractable models where you can mathematically derive and easily sample from the full conditional distribution $p(\theta_j | \theta_{-j}, \mathcal{D})$ for each parameter.

## Synthesis
All three methods guarantee that the long-run stationary distribution converges to the exact target posterior, provided the chain is ergodic and satisfies detailed balance. 

The differences lie in the **efficiency vs. analytical requirement trade-off**:
- **MH/Metropolis** are very flexible but require tuning the proposal step size. Too small a step leads to slow mixing (high correlation between samples), while too large a step leads to frequent rejections and wasted computation.
- **Gibbs Sampling** represents the ideal scenario of MH where the proposal perfectly matches the target along one dimension. Because the acceptance probability is exactly 1, no samples are rejected. However, this comes at a steep analytical cost: you must be able to analytically derive and draw from the full conditionals, which is impossible for many non-conjugate models (like neural networks or complex non-linear models).