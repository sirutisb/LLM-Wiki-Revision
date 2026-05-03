# KL Divergence (Kullback–Leibler Divergence)

**Type:** principle
**Week:** 4 (introduced), 6 (information-theoretic perspective)
**Related:** [[variational-inference]], [[elbo]], [[entropy]], [[cross-entropy]], [[mutual-information]]
**Source:** [[lecture-w4]], [[lecture-w6]]

## Definition
The KL divergence from distribution $q$ to distribution $p$ measures the expected extra information needed to encode samples from $p$ using a code optimised for $q$:
$$\text{KL}(q\|p) = \int q(x)\log\frac{q(x)}{p(x)}\,dx = \mathbb{E}_q[\log q(x) - \log p(x)]$$

## Motivation
In variational inference, we need a measure of how "different" our approximation $q$ is from the true posterior $p$. KL divergence is the standard choice: it's non-negative, tractable to compute under $q$, and leads directly to the ELBO.

## How it works

### Properties
- **Non-negative**: $\text{KL}(q\|p) \geq 0$, with equality iff $q = p$.
  - Proof: Jensen's inequality applied to the concave function $-\log$.
- **Asymmetric**: $\text{KL}(q\|p) \neq \text{KL}(p\|q)$ in general.
- Not a true distance metric (violates symmetry and triangle inequality).

### Reverse vs Forward KL
| | Formula | Behaviour | Name |
|---|---|---|---|
| **Reverse** | $\text{KL}(q\|p)$ | Zero-forcing: $q$ avoids where $p \approx 0$ | Mode-seeking |
| **Forward** | $\text{KL}(p\|q)$ | Zero-avoiding: $q$ must cover where $p > 0$ | Mass-covering |

**Reverse KL** (used in VI):
- Expectation taken under $q$ → tractable (we can sample from $q$).
- If $q(\theta) > 0$ where $p(\theta) \approx 0$: log ratio blows up → $q$ is penalised.
- Result: $q$ latches onto one mode of $p$; underestimates uncertainty.

**Forward KL** (MLE limit):
- Expectation taken under $p$ → intractable (need to evaluate true posterior).
- Penalised if $q(\theta) \approx 0$ where $p(\theta) > 0$.
- Result: $q$ must cover all mass of $p$; overestimates uncertainty.

## Key derivation

**Non-negativity** (Jensen's inequality):
$$\text{KL}(q\|p) = \mathbb{E}_q\!\left[-\log\frac{p(x)}{q(x)}\right] \geq -\log\,\mathbb{E}_q\!\left[\frac{p(x)}{q(x)}\right] = -\log 1 = 0$$
(because $-\log$ is convex, Jensen gives $f(\mathbb{E}) \leq \mathbb{E}[f]$).

**Relationship to entropy and cross-entropy** (Week 6):
$$\text{KL}(p\|q) = H(p,q) - H(p)$$
where $H(p,q) = -\sum_x p(x)\log q(x)$ is cross-entropy and $H(p) = -\sum_x p(x)\log p(x)$ is entropy.

## Parameters & intuition
- KL(q||p): "how surprised would I be, on average, if I thought the world was $q$ but it's really $p$?"
- KL = 0: perfect approximation. Large KL: $q$ is far from $p$.
- In VI: VI objective = minimise reverse KL ≡ maximise ELBO.

## Worked example sketch
*Classification loss*: In one-hot classification, cross-entropy loss = KL(true||predicted) + $H$(true). Since entropy of one-hot labels is fixed, minimising cross-entropy = minimising KL.

## Connections
- [[elbo]]: derived by rearranging KL(q||posterior).
- [[entropy]] + cross-entropy: $\text{KL}(p\|q) = H(p,q) - H(p)$.
- [[mutual-information]]: $I(X;Y) = \text{KL}(p(x,y)\|p(x)p(y))$.
- [[variational-autoencoder]]: KL$(q_\phi(z|x)\|p(z))$ is the regularisation term in the VAE ELBO.

## Exam notes
- "What is measured by the KL divergence?": ⚠️ **past exam question**.
  - Answer: extra information (surprise) when using $q$ to encode samples from $p$.
- Asymmetry must be understood: $\text{KL}(q\|p) \neq \text{KL}(p\|q)$.
- Mode-seeking vs mass-covering distinction: **conceptual** exam question.
- Non-negativity proof via Jensen: understand the argument.
- No formulas given for Week 4. ⚠️
- Formula status: definition must be known from memory ⚠️
