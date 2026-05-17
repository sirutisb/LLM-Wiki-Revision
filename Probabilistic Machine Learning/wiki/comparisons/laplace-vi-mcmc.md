# Laplace Approximation vs Variational Inference vs MCMC

**⚠️ Past exam question: "Explain the key differences between Laplace approximation, variational approximation and Markov Chain Monte Carlo approximation."**

## Overview

All three methods address the same core problem: the exact posterior $p(\theta|\mathcal{D})$ is intractable because the normalising constant $p(\mathcal{D})$ cannot be computed. They differ in how they construct a tractable substitute.

## Comparison table

| Dimension                          | Laplace Approximation                                           | Variational Inference (VI)                                         | MCMC                                                                    |
| ---------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| **Core idea**                      | Fit a Gaussian at the MAP via a 2nd-order Taylor expansion      | Optimise a tractable $q(\theta)$ to minimise $\text{KL}(q \| p)$   | Construct a Markov chain whose stationary distribution is the posterior |
| **Output**                         | Analytic Gaussian $q(\theta) = \mathcal{N}(\hat\theta, A^{-1})$ | Analytic distribution $q^*(\theta)$ from a chosen family           | A set of correlated samples $\{\theta^i\}$                              |
| **Exact?**                         | No — Gaussian bias                                              | No — family bias (reverse KL mode-seeking)                         | Asymptotically yes — converges to true posterior                        |
| **Scope**                          | Local — only near the MAP mode                                  | Global — searches over a family of distributions                   | Global — explores the full posterior                                    |
| **Multimodal posteriors**          | Fails — captures only one mode                                  | May fail — reverse KL is mode-seeking, tends to lock onto one mode | Handles multimodal posteriors (if chain mixes)                          |
| **Skewed posteriors**              | Poor — forces a symmetric Gaussian                              | Better — richer families available                                 | Handles arbitrary shapes                                                |
| **Computational cost**             | Cheap — one MAP optimisation + one Hessian                      | Moderate — iterative optimisation (ELBO maximisation)              | Expensive — many sequential iterations                                  |
| **Scalability**                    | Good                                                            | Good — scales to large datasets                                    | Poor — samples are correlated; slow mixing in high dimensions           |
| **Requires normalising constant?** | No (MAP + curvature only)                                       | No (ELBO uses only likelihood, prior, $q$)                         | No (MH acceptance ratio cancels $Z$)                                    |
| **Week**                           | 3                                                               | 4                                                                  | 5                                                                       |

## Detailed explanation of each

### Laplace Approximation
Finds the MAP estimate $\hat\theta$, then approximates the log-posterior as a quadratic around $\hat\theta$. Exponentiating gives a Gaussian:
$$q(\theta) = \mathcal{N}(\hat\theta,\, A^{-1}), \qquad A = -\frac{d^2}{d\theta^2}\log p(\theta|\mathcal{D})\bigg|_{\hat\theta}$$
**Limitation:** Only valid near the mode — fails for multimodal, skewed, or heavy-tailed posteriors.

### Variational Inference
Turns posterior inference into an optimisation problem. Choose a tractable family $\mathcal{Q}$ and find:
$$q^* = \arg\min_{q \in \mathcal{Q}}\,\text{KL}(q(\theta)\|p(\theta|\mathcal{D}))$$
Since $\text{KL}$ depends on the intractable $p(\theta|\mathcal{D})$, the equivalent objective is to **maximise the ELBO**:
$$\mathcal{L}(q) = \mathbb{E}_q[\log p(\mathcal{D}|\theta)] - \text{KL}(q(\theta)\|p(\theta))$$
**Limitation:** Biased — restricted to the chosen family. Reverse KL is mode-seeking: $q$ may underestimate posterior uncertainty.

### MCMC
Constructs a Markov chain $\theta^0 \to \theta^1 \to \cdots$ with stationary distribution $p(\theta|\mathcal{D})$. After burn-in, samples are approximately from the posterior. Posterior expectations are estimated by:
$$\mathbb{E}[f(\theta)] \approx \frac{1}{N}\sum_{i=1}^N f(\theta^i)$$
Metropolis–Hastings accepts proposed moves with probability $\alpha = \min\!\left(1, \frac{\tilde p(\theta')}{\tilde p(\theta^m)}\right)$ (symmetric proposal), cancelling the unknown normaliser.
**Limitation:** Samples are correlated; slow to converge; computationally expensive for large datasets.

## Key distinctions to memorise

- **Laplace vs VI**: Laplace is *local* (Taylor expansion at one point); VI is *global* (optimises over a full distribution family). Both are deterministic and analytic.
- **Laplace/VI vs MCMC**: Laplace and VI are *optimisation-based* (fast, deterministic, biased); MCMC is *sampling-based* (slow, stochastic, asymptotically unbiased).
- **Exactness**: Only MCMC is asymptotically exact. Laplace and VI always introduce approximation bias.
- **Multimodality**: MCMC is the only method that can represent multimodal posteriors; Laplace is worst (single Gaussian); VI may capture one mode (mode-seeking).

## Synthesis

There is a bias–cost tradeoff across the three methods:

$$\underbrace{\text{Laplace}}_{\text{cheapest, most biased}} \;\longrightarrow\; \underbrace{\text{VI}}_{\text{moderate}} \;\longrightarrow\; \underbrace{\text{MCMC}}_{\text{most expensive, asymptotically exact}}$$

In practice: use Laplace for a quick sanity check or when the posterior is known to be near-Gaussian; use VI for large-scale inference where scalability matters; use MCMC when accuracy is paramount and the posterior may have complex structure.
