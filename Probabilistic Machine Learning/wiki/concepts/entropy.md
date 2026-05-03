# Entropy

**Type:** principle
**Week:** 6
**Related:** [[kl-divergence]], [[cross-entropy]], [[mutual-information]], [[maximum-entropy-principle]], [[information-content]]
**Source:** [[lecture-w6]], [[lecture-w10]]

## Definition
Entropy is the average information content (surprise) of a distribution — it measures the uncertainty or unpredictability of a random variable.

## Motivation
In probabilistic ML, we repeatedly measure "how uncertain" a distribution is, compare two distributions, and quantify information. Entropy unifies all of these: it is the fundamental measure from which KL divergence, cross-entropy, and mutual information are all derived.

## How it works

### Discrete Entropy
For a discrete RV $X \sim p(x)$:
$$H(X) = -\sum_x p(x)\log p(x) = \mathbb{E}_p[-\log p(X)]$$
- Units: **bits** if $\log_2$, **nats** if $\ln$.
- Measures average surprise over the whole distribution.

### Key Properties
- $H(X) \geq 0$.
- **Maximum**: $H(X)$ is maximised by the uniform distribution. For $K$ outcomes: $H_{\max} = \log K$.
- **Minimum**: $H(X) = 0$ iff $X$ is deterministic (one outcome with probability 1).
- Low entropy → low uncertainty (concentrated distribution).
- High entropy → high uncertainty (spread-out distribution).

### Coding Interpretation
- Shannon's Noiseless Coding Theorem: entropy = minimum average code length.
- Optimal code: $\ell(x) = -\log_2 p(x)$ bits per symbol.
- Average code length: $\mathbb{E}[\ell(X)] = H(X)$.

### Differential Entropy (Continuous)
$$h(X) = -\int p(x)\log p(x)\,dx$$
- Can be **negative** (unlike discrete entropy).
- Depends on scale (not invariant to reparameterisation).
- Gaussian: $h(X) = \frac{1}{2}\log(2\pi e\sigma^2)$ — increases with variance.

## Key derivation

**Entropy of uniform distribution** over $K$ outcomes:
$$H(X) = -K \cdot \frac{1}{K}\log\frac{1}{K} = \log K$$

**Differential entropy of Gaussian** $\mathcal{N}(\mu, \sigma^2)$:
$$h(X) = \frac{1}{2}\log(2\pi\sigma^2) + \frac{1}{2} = \frac{1}{2}\log(2\pi e\sigma^2)$$
(Uses $\mathbb{E}[(X-\mu)^2] = \sigma^2$.)

## Parameters & intuition
- Entropy depends only on the shape of $p$, not the values of $x$.
- For Gaussian: entropy depends only on $\sigma^2$ (not $\mu$). Wider → more uncertain → higher entropy.
- Two Gaussians with the same $\sigma^2$ have the same entropy, regardless of their means.

## Worked example sketch
*Past exam question*: "Which distribution has larger entropy: $\mathcal{N}(0,1)$ or $\mathcal{N}(0, 2.5^2)$?"
Answer: $\mathcal{N}(0, 2.5^2)$ — larger variance → larger entropy. Mean irrelevant.

*Discrete example*: $p = (1/2, 1/4, 1/8, 1/8)$, 4 outcomes.
$H = -\frac{1}{2}\log_2\frac{1}{2} - \frac{1}{4}\log_2\frac{1}{4} - 2\cdot\frac{1}{8}\log_2\frac{1}{8} = \frac{1}{2}(1) + \frac{1}{4}(2) + 2\cdot\frac{1}{8}(3) = 0.5 + 0.5 + 0.75 = 1.75$ bits.

## Connections
- [[cross-entropy]]: $H(p,q) = H(p) + D_{\text{KL}}(p\|q)$.
- [[kl-divergence]]: $D_{\text{KL}}(p\|q) = H(p,q) - H(p)$.
- [[mutual-information]]: $I(X;Y) = H(X) - H(X|Y)$.
- [[maximum-entropy-principle]]: uses entropy as objective to choose the least-biased distribution.

## Exam notes
- "Which distribution has larger entropy and why?": ⚠️ **past exam question**.
- Discrete entropy calculation: **examinable**.
- Gaussian differential entropy: $h = \frac{1}{2}\log(2\pi e\sigma^2)$ — formula may be given.
- Entropy of uniform: $\log K$ — must know.
- **Key insight**: entropy of a Gaussian depends only on $\sigma^2$, not $\mu$.
- Formula status: formulas for Week 6 **will be given** ✅
