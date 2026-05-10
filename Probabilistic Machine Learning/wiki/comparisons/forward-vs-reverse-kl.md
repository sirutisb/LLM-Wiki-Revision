# Forward vs Reverse KL Divergence

## Overview
Kullback–Leibler (KL) divergence measures the extra information required to encode samples from a true distribution $p$ using a code optimised for an approximate distribution $q$. Because KL divergence is asymmetric—i.e., $\text{KL}(q\|p) \neq \text{KL}(p\|q)$—the direction we choose to minimise drastically changes the behaviour of the approximation. Understanding the difference between Forward KL and Reverse KL is crucial for Variational Inference (VI) and is a common conceptual question in the exam.

## Comparison table

| Dimension | Reverse KL (VI Objective) | Forward KL (MLE Limit) |
|-----------|---------------------------|------------------------|
| **Notation** | $\text{KL}(q\|p)$ | $\text{KL}(p\|q)$ |
| **Formula** | $\mathbb{E}_q[\log q(x) - \log p(x)]$ | $\mathbb{E}_p[\log p(x) - \log q(x)]$ |
| **Expectation under**| Approximate distribution $q$ | True distribution $p$ |
| **Behaviour name** | Mode-seeking / Zero-forcing | Mass-covering / Zero-avoiding |
| **Tractability** | Tractable (we can sample/evaluate over $q$) | Intractable (requires evaluating true posterior $p$) |
| **Penalty region** | Penalises heavily if $q(x) > 0$ when $p(x) \approx 0$ | Penalises heavily if $q(x) \approx 0$ when $p(x) > 0$ |
| **Resulting shape** | $q$ latches onto a single mode of $p$ | $q$ spreads out to cover all modes of $p$ |
| **Variance effect** | Underestimates variance / uncertainty | Overestimates variance / uncertainty |

## When to use which

### Reverse KL: Variational Inference (VI)
We almost always use **Reverse KL** in Variational Inference because it is computationally tractable.
- The expectation is taken with respect to $q(\theta)$, which is a distribution we choose and control (e.g., a Gaussian).
- Since $p(\theta|\mathcal{D})$ is intractable, we cannot compute expectations over it. However, the ELBO derivation allows us to rewrite the minimisation of Reverse KL purely in terms of the tractable joint distribution $p(\mathcal{D}, \theta)$ and $q(\theta)$:
  $$\arg\min_q \text{KL}(q(\theta)\|p(\theta|\mathcal{D})) \Longleftrightarrow \arg\max_q \text{ELBO}(q)$$
- **Consequence:** Because it is "zero-forcing", $q(\theta)$ will avoid areas where $p(\theta|\mathcal{D})$ is zero. If the true posterior is multimodal, $q$ will typically collapse onto a single mode, leading to an underestimation of the true posterior uncertainty.

### Forward KL: Maximum Likelihood & Expectation Propagation
**Forward KL** is used when we want to ensure our approximation covers all plausible regions of the true distribution.
- Because the expectation is over the true distribution $p$, it is generally intractable for complex Bayesian posteriors.
- **Maximum Likelihood Estimation (MLE)** implicitly minimises a form of Forward KL: minimising the cross-entropy between the empirical data distribution (true $p$) and the model ($q$) is equivalent to minimising $\text{KL}(p\|q)$.
- **Consequence:** Because it is "zero-avoiding", $q$ is heavily penalised if it assigns zero probability to a region where $p$ has mass. Thus, $q$ stretches to cover all modes, often overestimating the variance and placing mass in low-probability valleys between modes.

## Synthesis & Exam Link
- **Conceptual understanding:** You must know that VI uses Reverse KL because of tractability (expectation over $q$).
- **Visual intuition:** Imagine a bimodal true distribution $p$ (two peaks).
  - Reverse KL (VI) will fit a single narrow Gaussian over *one* of the peaks (mode-seeking).
  - Forward KL will fit a single wide Gaussian that spans across *both* peaks, filling in the valley between them (mass-covering).
- **Exam tip:** The mode-seeking vs mass-covering distinction and why VI uses Reverse KL are highly examinable concepts (⚠️ past exam questions). Understand the penalty mechanisms:
  - Reverse KL blows up when $p \to 0$ (forces $q \to 0$ there).
  - Forward KL blows up when $q \to 0$ (forces $q > 0$ where $p > 0$).