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

✅ *Formula sheet provided.* (Derivations not examinable)

**Entropy of uniform distribution** over $K$ outcomes:
$$H(X) = -K \cdot \frac{1}{K}\log\frac{1}{K} = \log K$$

**Differential entropy of Gaussian** $\mathcal{N}(\mu, \sigma^2)$:
$$h(X) = \frac{1}{2}\log(2\pi\sigma^2) + \frac{1}{2} = \frac{1}{2}\log(2\pi e\sigma^2)$$
(Uses $\mathbb{E}[(X-\mu)^2] = \sigma^2$.)

## Parameters & intuition
- Entropy depends only on the shape of $p$, not the values of $x$.
- For Gaussian: entropy depends only on $\sigma^2$ (not $\mu$). Wider → more uncertain → higher entropy.
- Two Gaussians with the same $\sigma^2$ have the same entropy, regardless of their means.

### Intuition: Bits as Repeated Yes/No Questions
Think of bits as repeated yes/no questions.
- **Uniform distribution (8 equally likely):** Need 3 binary questions: *Is it in first half? Which quarter? Which eighth?* Always 3 bits.
- **Non-uniform distribution:** Suppose Cat is 50%, and others split the remaining 50%. First question: *Is it cat?* Half the time you're already done after ONE question. Only sometimes do you continue asking more. Average questions decrease.

Entropy measures the **expected number of binary decisions needed.**
If outcomes are predictable: fewer questions needed, fewer bits needed, lower entropy.
If outcomes are unpredictable: more questions needed, more bits needed, higher entropy.
That is the real meaning behind “average surprise.”

### Intuition: Generalized Entropy Coding
The “store only rare indexes” trick is a special case for extremely skewed distributions. For general distributions, the idea becomes: **assign shorter bit patterns to more probable symbols and longer bit patterns to rarer symbols.** Instead of storing rare indexes explicitly, you continuously allocate bit lengths according to probability. The general rule becomes: optimal code length $\approx -\log_2 p(x)$. This is exactly what prefix-free codes and Huffman coding do.

## Worked example sketch
*Past exam question*: "Which distribution has larger entropy: $\mathcal{N}(0,1)$ or $\mathcal{N}(0, 2.5^2)$?"
Answer: $\mathcal{N}(0, 2.5^2)$ — larger variance → larger entropy. Mean irrelevant.

*Discrete example: Prefix-Free Codes*
Suppose we have 4 animals: Cat ($0.5$), Dog ($0.25$), Bird ($0.125$), Fish ($0.125$).
Entropy $H(X) = \sum p(x)(-\log_2 p(x))$.
Compute bits per symbol:
- Cat: 1 bit ($-\log_2 0.5 = 1$)
- Dog: 2 bits ($-\log_2 0.25 = 2$)
- Bird: 3 bits ($-\log_2 0.125 = 3$)
- Fish: 3 bits ($-\log_2 0.125 = 3$)

Now actually encode them. We design binary codes:
- Cat: `0`
- Dog: `10`
- Bird: `110`
- Fish: `111`

Notice: common things get shorter codes, rare things get longer codes.
Why does this still decode correctly? Because the code is **prefix-free**. No code starts another code. You can read left-to-right greedily.
Example stream: `010110111`
Decode:
`0` → Cat
`10` → Dog
`110` → Bird
`111` → Fish

Now compute average bits (expected storage cost):
$0.5(1) + 0.25(2) + 0.125(3) + 0.125(3) = 1.75$ bits.

So even though there are 4 classes, we use LESS than 2 bits on average. That is compression using probabilities. Wasting long codes on cats is inefficient because they appear constantly, so we make cats cheap. Rare events can afford long codes because they barely occur.

## Connections
- [[cross-entropy]]: $H(p,q) = H(p) + D_{\text{KL}}(p\|q)$.
- [[kl-divergence]]: $D_{\text{KL}}(p\|q) = H(p,q) - H(p)$.
- [[mutual-information]]: $I(X;Y) = H(X) - H(X|Y)$.
- [[maximum-entropy-principle]]: uses entropy as objective to choose the least-biased distribution.

## Exam notes
- "Which distribution has larger entropy and why?": ⚠️ **past exam question**.
- Discrete entropy calculation: **examinable**.
- Gaussian differential entropy: $h = \frac{1}{2}\log(2\pi e\sigma^2)$ — formula given ✅.
- Entropy of uniform: $\log K$ — formula given ✅.
- **Key insight**: entropy of a Gaussian depends only on $\sigma^2$, not $\mu$.
- **Derivations**: derivations for Week 6 are **not examinable**.
- Formula status: formulas for Week 6 **will be given** ✅
