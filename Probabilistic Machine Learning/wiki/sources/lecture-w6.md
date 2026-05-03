# Week 6 — Information Theory

**File:** `raw/text/COM3031_2526_Week6.txt`
**Type:** lecture
**Week:** 6
**Concepts introduced:** [[entropy]], [[mutual-information]], [[cross-entropy]], [[kl-divergence]], [[maximum-entropy-principle]], [[information-content]]

## Summary
Week 6 unifies the probabilistic machinery used throughout the course under information theory. Self-information, entropy, conditional entropy, mutual information, cross-entropy, and KL divergence are introduced as facets of a single framework for measuring and comparing uncertainty. The maximum entropy principle shows that the uniform distribution (no constraints), exponential family (mean constraint), and Gaussian (mean + variance constraints) are all maximum-entropy solutions. Differential entropy extends these ideas to continuous variables.

## Key content

### Self-Information
- Information content of outcome $x$: $I(x) = -\log_2 p(x)$ (bits) or $-\ln p(x)$ (nats).
- Rare events → high information. Certain events → zero information.
- Additivity: independent events $x, y$: $I(x,y) = I(x) + I(y)$.

### Entropy (Discrete)
$$H(X) = \mathbb{E}_p[I(X)] = -\sum_x p(x)\log p(x)$$
- Average surprise / uncertainty of a distribution.
- Maximised by the **uniform distribution**: $H_{\max} = \log K$ for $K$ equally likely outcomes.
- Shannon's Noiseless Coding Theorem: entropy is the minimum average code length.
  - Optimal code: $\ell(x) \approx -\log_2 p(x)$ bits.

### Differential Entropy (Continuous)
$$h(X) = -\int p(x)\log p(x)\,dx$$
- Can be negative. Depends on scale (not invariant under reparameterisation).
- Gaussian: $h(X) = \frac{1}{2}\log(2\pi e\sigma^2)$ — increases with variance.

### Maximum Entropy Principle
- Choose the distribution with **maximum entropy** subject to known constraints (least biased choice).
- No constraints → **Uniform**.
- Mean constraint $\mathbb{E}[f(X)] = \mu$ → **Exponential family**: $p(x) = \frac{1}{Z(\lambda)}\exp(\lambda f(x))$.
- Mean + variance constraints → **Gaussian** $\mathcal{N}(\mu, \sigma^2)$ (maximum differential entropy under fixed mean and variance).

### Conditional Entropy
$$H(X|Y) = \mathbb{E}_{p(x,y)}[-\log p(x|y)] = \sum_{x,y} p(x,y)(-\log p(x|y))$$
- Remaining uncertainty in $X$ after observing $Y$.
- Chain rule: $H(X,Y) = H(Y) + H(X|Y)$.

### Mutual Information
$$I(X;Y) = H(X) - H(X|Y) = D_{\text{KL}}(p(x,y)\|p(x)p(y))$$
- Information gain about $X$ from observing $Y$.
- $I(X;Y) = 0$ iff $X \perp Y$.
- Bayesian perspective: $I(\theta;\mathcal{D}) = H(\theta) - H(\theta|\mathcal{D})$ — how much data reduces parameter uncertainty.

### KL Divergence (Relative Entropy)
$$D_{\text{KL}}(p\|q) = \sum_x p(x)\log\frac{p(x)}{q(x)} = H(p,q) - H(p)$$
where $H(p,q) = -\sum_x p(x)\log q(x)$ is the **cross-entropy**.

- $D_{\text{KL}}(p\|q) \geq 0$, equals 0 iff $p = q$.
- Asymmetric.

### Cross-Entropy and Classification
$$H(p,q) = H(p) + D_{\text{KL}}(p\|q)$$
- In classification with one-hot labels: minimising cross-entropy loss ≡ minimising KL divergence between true and predicted distributions (since $H(p)$ is fixed).

## Key takeaways
- Log-likelihood, cross-entropy, KL divergence, ELBO — all connect back to information-theoretic quantities.
- Entropy = minimum average code length (Shannon). 
- Max-entropy principle: among all distributions satisfying constraints, choose the most uncertain one.
- Minimising cross-entropy loss = minimising KL = MLE (when true distribution is the data distribution).
- "KL divergence = extra coding cost when using $q$ instead of $p$."

## Exam relevance
- "What is measured by KL divergence between two distributions?": **past exam question**.
- "Which distribution has larger entropy and why?": **past exam question**.
- Entropy calculations: **examinable**.
- Maximum entropy principle (discrete): **examinable** (uniform result).
- Gaussian differential entropy result: conceptual understanding.
- Derivations NOT examinable (Week 6).
- Formula sheet for Week 6: formulas **will be given**.

## Links to concepts
- [[entropy]]: introduced here
- [[mutual-information]]: introduced here
- [[cross-entropy]]: introduced here
- [[kl-divergence]]: expanded from [[lecture-w4]]
- [[maximum-entropy-principle]]: introduced here
- [[information-content]]: introduced here
