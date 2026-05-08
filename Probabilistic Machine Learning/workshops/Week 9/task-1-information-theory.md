# Task 1 — Information Theory: Self-Information & Entropy

**Workshop tasks 1–4 (Information Theory section).** Compute self-information for simple events, plot how information shrinks as probability grows, evaluate Shannon entropy by hand and via `scipy`, then explore how entropy behaves over a binary distribution $[p, 1-p]$.

**Concepts:** [[entropy]], [[mutual-information]], [[cross-entropy]], [[kl-divergence]], [[maximum-entropy-principle]], [[lecture-w6]]

---

## What we're trying to do

Information theory gives us a quantitative answer to two related questions:

1. **How surprising is a single outcome?** — that's *self-information* $I(x) = -\log_2 p(x)$.
2. **How uncertain is a whole distribution?** — that's *Shannon entropy* $H(X) = -\sum_x p(x)\log_2 p(x)$, the *expected* self-information.

The point of these four little exercises is to build numerical intuition for both quantities before we start using them as building blocks for KL divergence, cross-entropy, mutual information, and (next week) the ELBO.

The unit is **bits** because we use $\log_2$. (Switching to $\ln$ would give *nats*; the shape of every plot is unchanged, only the vertical scale rescales by $\ln 2$.)

---

## Cell-by-cell walkthrough

### Cell 2 — Self-information of a fair coin flip

```python
from math import log2
p = 0.5
h = -log2(p)
print('p(x)=%.3f, information: %.3f bits' % (p, h))
```

Plug $p=0.5$ into $I(x) = -\log_2 p$. You get exactly **1 bit** — which is the textbook definition of a bit: the information delivered by resolving one fair binary choice. This is why a single yes/no question, asked optimally, can carry 1 bit of information.

### Cell 3 — Self-information of a fair die roll

```python
p = 1.0 / 6.0
h = -log2(p)
```

$-\log_2(1/6) = \log_2 6 \approx 2.585$ bits. Less probable outcome ($1/6 < 1/2$) $\Rightarrow$ *more* information when it occurs. Intuition: rare events tell you more because they were less expected. Equivalently, you'd need ~2.6 yes/no questions on average to identify a die outcome (and exactly $\lceil\log_2 6\rceil = 3$ in the worst case).

### Cell 4 — Probability vs self-information curve

```python
probs = [0.1, 0.2, ..., 1.0]
info = [-log2(p) for p in probs]
pyplot.plot(probs, info, marker='.')
```

The list comprehension just maps $p \mapsto -\log_2 p$. The plot you should see:

- Diverges to $\infty$ as $p \to 0$ — vanishingly rare events carry unbounded information.
- Hits **0 at $p=1$** — a certain event carries zero information (you already knew it would happen).
- Strictly *decreasing* and *convex*.

This is precisely the shape required by the three axioms Shannon used to derive $-\log p$:
$I$ is non-negative, $I(p=1)=0$, and $I$ is additive on independent events ($I(p_1 p_2) = I(p_1) + I(p_2)$).

### Cell 5 — Entropy of a fair six-sided die (by hand)

```python
n = 6
p = 1.0 / n
entropy = -sum([p * log2(p) for _ in range(n)])  # equivalently: -n * p * log2(p)
```

Apply Shannon's formula
$$
H(X) = -\sum_{x} p(x)\log_2 p(x).
$$
Every face has $p = 1/6$, so each term is $-(1/6)\log_2(1/6)$ and there are 6 of them:
$$
H = -6 \cdot \tfrac{1}{6}\log_2\tfrac{1}{6} = \log_2 6 \approx 2.585 \text{ bits}.
$$
For any **uniform** distribution over $n$ outcomes, $H = \log_2 n$ — the maximum entropy possible on $n$ outcomes (by the [[maximum-entropy-principle]]).

### Cell 6 — Same result via `scipy.stats.entropy`

```python
from scipy.stats import entropy
p = [1/6]*6
e = entropy(p, base=2)   # don't forget base=2 to get bits!
```

`scipy.stats.entropy(p, base=2)` computes the same sum. **Watch out:** `entropy` defaults to natural log (nats); pass `base=2` to match the manual answer of 2.585. Without it you'd get $\ln 6 \approx 1.792$ nats.

### Cell 7 — Entropy of a binary distribution $[p, 1-p]$

```python
def entropy(events, ets=1e-15):
    return -sum([p * log2(p + ets) for p in events])

probs = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
dists = [[p, 1.0 - p] for p in probs]
ents  = [entropy(d) for d in dists]
```

For each $p$ we build the distribution $[p, 1-p]$ and compute
$$
H_b(p) = -p\log_2 p - (1-p)\log_2(1-p).
$$
This is the **binary entropy function** $H_b(p)$. The `ets=1e-15` term avoids `log2(0)` when $p=0$ (since $0 \cdot \log 0 = 0$ by convention but the code would otherwise crash).

Reading the plot:

| $p$  | $H_b(p)$ | Interpretation |
|------|----------|----------------|
| 0.0  | 0 bits   | Certain outcome — no uncertainty |
| 0.1  | 0.469    | Highly skewed coin — usually predictable |
| 0.3  | 0.881    | Getting closer to fair |
| 0.5  | **1.0**  | Fair coin — maximum uncertainty |

The function is symmetric about $p=0.5$ (the plot only shows $p \in [0, 0.5]$ but the right half mirrors it) and **concave** with peak at $p=1/2$.

### Why entropy peaks at uniform

Two complementary ways to see it:

1. **Calculus.** Differentiate $H_b(p) = -p\log_2 p - (1-p)\log_2(1-p)$:
   $$
   \frac{dH_b}{dp} = -\log_2 p + \log_2(1-p) = \log_2\!\frac{1-p}{p}.
   $$
   Set to zero $\Rightarrow p = 1/2$. Second derivative is negative everywhere, so it's a maximum.

2. **Coding/intuition.** Entropy = expected number of bits needed to encode an outcome. If the coin is biased ($p=0.1$), you can use a short codeword for the common outcome and a long one for the rare one — you save bits on average. Only when both outcomes are equally likely is there nothing to exploit, and you need a full bit per draw.

This is exactly the [[maximum-entropy-principle]]: among all distributions on a finite set with no constraints, the uniform distribution has maximum entropy.

---

## What to take away for the exam

- **Self-information:** $I(x) = -\log_2 p(x)$. Less probable $\Rightarrow$ more information. ✅ *Formula given in Week 1–2 only — by Week 6 you should know it.*
- **Shannon entropy:** $H(X) = -\sum_x p(x)\log_2 p(x) = \mathbb{E}_p[-\log_2 p(X)]$.
- **Units depend on log base:** $\log_2 \to$ bits, $\ln \to$ nats, $\log_{10} \to$ hartleys. Stick with bits unless told otherwise.
- **Bounds for a discrete RV with $n$ outcomes:** $0 \le H(X) \le \log_2 n$.
  - Lower bound (0) hit by a deterministic $p$ (one outcome with probability 1).
  - Upper bound ($\log_2 n$) hit by the uniform distribution — this is the [[maximum-entropy-principle]].
- **Binary entropy function:** $H_b(p) = -p\log_2 p - (1-p)\log_2(1-p)$, peaks at 1 bit when $p=1/2$, symmetric about 1/2, concave.
- **Convention:** $0 \cdot \log 0 := 0$ (continuity). The `ets` trick in the notebook is just numerical hygiene.
- **Connections to the rest of the module:** entropy is the building block for [[cross-entropy]] $H(p,q) = -\sum p\log q$, [[kl-divergence]] $D_{\mathrm{KL}}(p\,\|\,q) = H(p,q) - H(p)$, [[mutual-information]] $I(X;Y) = H(X) - H(X|Y)$, and the negative ELBO (see [[elbo]]). Knowing the discrete computation cold makes those derivations much faster.
- **Likely exam style:** "Compute the entropy of [a small distribution]" (calculation), or "State and justify the maximum-entropy property of the uniform distribution" (conceptual).
