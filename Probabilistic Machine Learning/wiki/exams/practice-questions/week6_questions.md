# Week 6 Practice Questions — Information Theory

> ✅ **Formula policy:** All information-theory formulas are provided in the exam for Week 6.
> Questions test your ability to *apply* these formulas, not recall them verbatim.

---

## Formulas Provided in Exam

- **Information Content:** $I(x) = -\log_2 p(x)$
- **Entropy:** $H(X) = -\sum_{x} p(x) \log_2 p(x)$
- **Joint Entropy:** $H(X, Y) = -\sum_{x, y} p(x, y) \log_2 p(x, y)$
- **Conditional Entropy:** $H(Y|X) = -\sum_{x, y} p(x, y) \log_2 p(y|x)$
- **Chain Rule:** $H(X, Y) = H(X) + H(Y|X)$
- **KL Divergence:** $D_{\text{KL}}(p \| q) = \sum_{x} p(x) \log_2 \frac{p(x)}{q(x)}$
- **Mutual Information:** $I(X; Y) = H(X) - H(X|Y) = \sum_{x, y} p(x, y) \log_2 \frac{p(x, y)}{p(x)p(y)}$
- **Cross-Entropy:** $H(p, q) = -\sum_x p(x) \log_2 q(x) = H(p) + D_{\text{KL}}(p \| q)$

---

## Conceptual / Bookwork

### Q1 — Information content and entropy

**(a)** Define the *information content* (self-information) of an outcome $x$. Explain, in one sentence, why the negative log of the probability is an appropriate measure of surprise.

**(b)** Define Shannon entropy $H(X)$ and explain its relationship to information content.

**(c)** State two properties of entropy: one about the minimum value and one about the maximum value. In each case state when the bound is achieved.

---

### Q2 — KL divergence properties

**(a)** Write down the formula for the KL divergence $D_{\text{KL}}(p \| q)$ for discrete distributions.

**(b)** State whether KL divergence is (i) non-negative, and (ii) symmetric. For each, state the condition under which equality / symmetry holds (or explain why symmetry never holds in general).

**(c)** In variational inference we minimise $D_{\text{KL}}(q \| p)$ (the *reverse* KL). Briefly explain what behavioural tendency this creates in the approximate posterior $q$ when the true posterior $p$ is multimodal.

---

### Q3 — Maximum entropy principle

**(a)** State the maximum entropy principle in one sentence.

**(b)** Complete the following table by identifying the maximum-entropy distribution for each set of constraints:

| Known constraints | Max-entropy distribution |
|---|---|
| Discrete, $K$ outcomes, no other constraints | ??? |
| Continuous, mean $\mu$, variance $\sigma^2$ | ??? |

**(c)** A student argues: *"We should always choose the distribution with the lowest entropy, because that makes the most definite predictions."* Identify the flaw in this reasoning.

---

## Practical / Calculation

### Q4 — Entropy of simple discrete distributions

A discrete random variable $X$ takes three values with probabilities:

$$p(X=1) = \tfrac{1}{2}, \quad p(X=2) = \tfrac{1}{4}, \quad p(X=3) = \tfrac{1}{4}$$

**(a)** Compute $H(X)$ in bits.

**(b)** Compare this to the entropy of a *uniform* distribution over the same three outcomes. Which is larger and why?

---

### Q5 — KL divergence: numerical calculation and asymmetry

Let $p$ and $q$ be distributions over $\{A, B, C\}$:

| Outcome | $p(x)$ | $q(x)$ |
|---------|--------|--------|
| $A$ | $\tfrac{1}{2}$ | $\tfrac{1}{4}$ |
| $B$ | $\tfrac{1}{4}$ | $\tfrac{1}{2}$ |
| $C$ | $\tfrac{1}{4}$ | $\tfrac{1}{4}$ |

**(a)** Compute $D_{\text{KL}}(p \| q)$ in bits (use $\log_2$).

**(b)** Compute $D_{\text{KL}}(q \| p)$ in bits.

**(c)** Are the two values equal? What does this illustrate about KL divergence?

---

### Q6 — Cross-entropy, entropy, and KL divergence

Using the same distributions $p$ and $q$ from Q5:

**(a)** Compute the cross-entropy $H(p, q)$.

**(b)** Compute the entropy $H(p)$.

**(c)** Verify numerically that $H(p, q) = H(p) + D_{\text{KL}}(p \| q)$.

**(d)** State one consequence of this identity for training a classifier with cross-entropy loss when the true label entropy $H(p)$ is fixed.

---

### Q7 — Joint entropy, conditional entropy, and mutual information

Two binary random variables $X$ and $Y$ have joint distribution:

| | $Y=0$ | $Y=1$ |
|-|-------|-------|
| $X=0$ | $\tfrac{1}{4}$ | $\tfrac{1}{4}$ |
| $X=1$ | $\tfrac{1}{4}$ | $\tfrac{1}{4}$ |

**(a)** Write down the marginal distributions $p(X)$ and $p(Y)$.

**(b)** Compute $H(X)$, $H(Y)$, and the joint entropy $H(X,Y)$.

**(c)** Use the chain rule $H(X,Y) = H(Y) + H(X|Y)$ to find $H(X|Y)$.

**(d)** Compute the mutual information $I(X;Y) = H(X) - H(X|Y)$. Interpret the result.

---

## Answers / Mark Schemes

---

### A1 — Information content and entropy

**(a)** The information content of outcome $x$ is:
$$I(x) = -\log_2 p(x)$$
The negative log is appropriate because (i) it is non-negative (probabilities are $\leq 1$ so the log is $\leq 0$, and negating gives $\geq 0$), (ii) it is monotonically decreasing in $p(x)$ — rare events give large values — and (iii) it is additive for independent events: $I(x,y) = I(x) + I(y)$.

**(b)** Shannon entropy is the expected value of information content:
$$H(X) = \mathbb{E}_p[I(X)] = -\sum_x p(x)\log_2 p(x)$$
It measures the average surprise (or uncertainty) of the whole distribution, not any single outcome.

**(c)**
- **Minimum:** $H(X) \geq 0$, with $H(X) = 0$ iff $X$ is deterministic — one outcome has probability 1 and all others have probability 0.
- **Maximum:** $H(X)$ is maximised when $X$ is *uniformly distributed*. For $K$ outcomes: $H_{\max} = \log_2 K$ bits.

---

### A2 — KL divergence properties

**(a)**
$$D_{\text{KL}}(p \| q) = \sum_x p(x)\log_2\frac{p(x)}{q(x)}$$

**(b)**
- **(i) Non-negative:** $D_{\text{KL}}(p \| q) \geq 0$ always, with equality if and only if $p = q$ (identical distributions).
- **(ii) Asymmetry:** $D_{\text{KL}}(p \| q) \neq D_{\text{KL}}(q \| p)$ in general — there is no condition under which they are always equal. KL divergence is not a true distance metric.

**(c)** Minimising the reverse KL $D_{\text{KL}}(q \| p)$ is *mode-seeking*: wherever $p(\theta) \approx 0$, the ratio $q(\theta)/p(\theta)$ can blow up, so $q$ is strongly penalised for placing mass there. As a result, $q$ collapses onto a single mode of $p$ and ignores other modes. This leads to an approximation that *underestimates* posterior uncertainty.

---

### A3 — Maximum entropy principle

**(a)** Among all distributions that satisfy the stated constraints, choose the one with the highest entropy — this makes the fewest additional assumptions beyond the given facts.

**(b)**

| Known constraints | Max-entropy distribution |
|---|---|
| Discrete, $K$ outcomes, no other constraints | Uniform: $p(x_i) = 1/K$ |
| Continuous, mean $\mu$, variance $\sigma^2$ | Gaussian: $\mathcal{N}(\mu, \sigma^2)$ |

**(c)** The student is confusing *predictive confidence* with *epistemic honesty*. Choosing a low-entropy (highly concentrated) distribution implies certainty that is not justified by the available evidence. A distribution with entropy 0 would assign probability 1 to a single outcome — that is fabricating knowledge we do not have. Maximum entropy is the principled default: it matches all known facts while committing to nothing else.

---

### A4 — Entropy of simple discrete distributions

**(a)** Compute each term $-p(x)\log_2 p(x)$:

$$-\tfrac{1}{2}\log_2\tfrac{1}{2} = \tfrac{1}{2} \times 1 = 0.5 \text{ bits}$$

$$-\tfrac{1}{4}\log_2\tfrac{1}{4} = \tfrac{1}{4} \times 2 = 0.5 \text{ bits}$$

$$-\tfrac{1}{4}\log_2\tfrac{1}{4} = \tfrac{1}{4} \times 2 = 0.5 \text{ bits}$$

$$H(X) = 0.5 + 0.5 + 0.5 = 1.5 \text{ bits}$$

**(b)** Uniform distribution over 3 outcomes: $p = (1/3, 1/3, 1/3)$.
$$H_{\text{uniform}} = \log_2 3 \approx 1.585 \text{ bits}$$

The uniform distribution has larger entropy ($1.585 > 1.5$ bits). This is expected: entropy is maximised by the uniform distribution; any non-uniform distribution over the same support has strictly lower entropy.

---

### A5 — KL divergence: numerical calculation and asymmetry

**(a)** $D_{\text{KL}}(p \| q)$: expectation taken under $p$.

| Outcome | $p(x)$ | $q(x)$ | $\log_2(p/q)$ | $p(x)\log_2(p/q)$ |
|---------|--------|--------|----------------|---------------------|
| $A$ | $1/2$ | $1/4$ | $\log_2 2 = 1$ | $1/2 \times 1 = 0.5$ |
| $B$ | $1/4$ | $1/2$ | $\log_2(1/2) = -1$ | $1/4 \times (-1) = -0.25$ |
| $C$ | $1/4$ | $1/4$ | $\log_2 1 = 0$ | $1/4 \times 0 = 0$ |

$$D_{\text{KL}}(p \| q) = 0.5 - 0.25 + 0 = \boxed{0.25 \text{ bits}}$$

**(b)** $D_{\text{KL}}(q \| p)$: expectation taken under $q$.

| Outcome | $q(x)$ | $p(x)$ | $\log_2(q/p)$ | $q(x)\log_2(q/p)$ |
|---------|--------|--------|----------------|---------------------|
| $A$ | $1/4$ | $1/2$ | $\log_2(1/2) = -1$ | $1/4 \times (-1) = -0.25$ |
| $B$ | $1/2$ | $1/4$ | $\log_2 2 = 1$ | $1/2 \times 1 = 0.5$ |
| $C$ | $1/4$ | $1/4$ | $\log_2 1 = 0$ | $1/4 \times 0 = 0$ |

$$D_{\text{KL}}(q \| p) = -0.25 + 0.5 + 0 = \boxed{0.25 \text{ bits}}$$

**(c)** They happen to be equal here (a numerical coincidence for this symmetric example). In general $D_{\text{KL}}(p \| q) \neq D_{\text{KL}}(q \| p)$. This illustrates that KL divergence is **not symmetric** — it is not a true metric. The direction of the KL matters: $D_{\text{KL}}(p\|q)$ penalises regions where $p$ is large but $q$ is small; $D_{\text{KL}}(q\|p)$ penalises the opposite.

> *Marker note: a candidate who shows a different example where the two divergences differ (e.g., changing one probability) should receive full marks for part (c) even if they note equality here.*

---

### A6 — Cross-entropy, entropy, and KL divergence

**(a)** Cross-entropy $H(p, q) = -\sum_x p(x)\log_2 q(x)$, using $q$ to encode data from $p$:

| Outcome | $p(x)$ | $q(x)$ | $-\log_2 q(x)$ | $p(x)(-\log_2 q(x))$ |
|---------|--------|--------|-----------------|------------------------|
| $A$ | $1/2$ | $1/4$ | $2$ | $1/2 \times 2 = 1.0$ |
| $B$ | $1/4$ | $1/2$ | $1$ | $1/4 \times 1 = 0.25$ |
| $C$ | $1/4$ | $1/4$ | $2$ | $1/4 \times 2 = 0.5$ |

$$H(p, q) = 1.0 + 0.25 + 0.5 = \boxed{1.75 \text{ bits}}$$

**(b)** Entropy $H(p) = -\sum_x p(x)\log_2 p(x)$:

| Outcome | $p(x)$ | $-\log_2 p(x)$ | $p(x)(-\log_2 p(x))$ |
|---------|--------|-----------------|------------------------|
| $A$ | $1/2$ | $1$ | $0.5$ |
| $B$ | $1/4$ | $2$ | $0.5$ |
| $C$ | $1/4$ | $2$ | $0.5$ |

$$H(p) = 0.5 + 0.5 + 0.5 = \boxed{1.5 \text{ bits}}$$

**(c)** Verification:

$$H(p) + D_{\text{KL}}(p \| q) = 1.5 + 0.25 = 1.75 = H(p, q) \checkmark$$

The identity holds numerically.

**(d)** When the true label distribution is one-hot (as in multi-class classification), $H(p)$ is fixed at 0 and does not depend on model parameters. Therefore:
$$\min_\theta H(p, q_\theta) \equiv \min_\theta \big[H(p) + D_{\text{KL}}(p \| q_\theta)\big] \equiv \min_\theta D_{\text{KL}}(p \| q_\theta)$$
Minimising cross-entropy loss is exactly equivalent to minimising KL divergence between the true and predicted distributions.

---

### A7 — Joint entropy, conditional entropy, and mutual information

**(a)** Marginals (sum across rows / columns):
$$p(X=0) = \tfrac{1}{4} + \tfrac{1}{4} = \tfrac{1}{2}, \quad p(X=1) = \tfrac{1}{4} + \tfrac{1}{4} = \tfrac{1}{2}$$
$$p(Y=0) = \tfrac{1}{4} + \tfrac{1}{4} = \tfrac{1}{2}, \quad p(Y=1) = \tfrac{1}{4} + \tfrac{1}{4} = \tfrac{1}{2}$$

Both $X$ and $Y$ are fair coin flips: $p(X) = p(Y) = \text{Bernoulli}(1/2)$.

**(b)**
$$H(X) = -\tfrac{1}{2}\log_2\tfrac{1}{2} - \tfrac{1}{2}\log_2\tfrac{1}{2} = 1 \text{ bit}$$
$$H(Y) = 1 \text{ bit (same calculation)}$$

Joint entropy over 4 equally probable outcomes $(p = 1/4$ each$)$:
$$H(X,Y) = -4 \times \tfrac{1}{4}\log_2\tfrac{1}{4} = -4 \times \tfrac{1}{4} \times (-2) = 2 \text{ bits}$$

**(c)** Chain rule: $H(X,Y) = H(Y) + H(X|Y)$, so:
$$H(X|Y) = H(X,Y) - H(Y) = 2 - 1 = \boxed{1 \text{ bit}}$$

**(d)**
$$I(X;Y) = H(X) - H(X|Y) = 1 - 1 = \boxed{0 \text{ bits}}$$

**Interpretation:** $I(X;Y) = 0$ means $X$ and $Y$ are *statistically independent* — observing $Y$ gives absolutely no information about $X$. This is consistent with the joint distribution, which is the product of the marginals: $p(x,y) = p(x)p(y) = \frac{1}{4}$ for all combinations.
