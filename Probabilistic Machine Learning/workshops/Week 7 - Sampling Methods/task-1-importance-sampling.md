# Task 1 — Importance Sampling

**Workshop tasks 1–2.** Implement importance sampling, then repeat with a different proposal $q(x)$ and observe the effect on the approximation.

**Concepts:** [[importance-sampling]], [[monte-carlo-integration]], [[lecture-w5]]

---

## What we're trying to do

We want to estimate an expectation
$$
\mathbb{E}_p[f(x)] = \int f(x)\,p(x)\,dx
$$
where $p(x)$ is a target distribution and $f(x)$ is some function of interest.

If we could draw samples from $p$ directly, plain Monte Carlo would do it:
$$
\mathbb{E}_p[f(x)] \approx \frac{1}{n}\sum_{i=1}^n f(x_i), \qquad x_i \sim p(x).
$$

But often $p$ is hard to sample from (no closed-form sampler, or only known up to a normalising constant). So we sample from an *easier* distribution $q(x)$ — the **proposal** — and **reweight** to undo the sampling bias:
$$
\mathbb{E}_p[f(x)] = \int f(x)\,\frac{p(x)}{q(x)}\,q(x)\,dx \;\approx\; \frac{1}{n}\sum_{i=1}^{n} f(x_i)\,\underbrace{\frac{p(x_i)}{q(x_i)}}_{\text{importance weight}}, \quad x_i \sim q.
$$

The factor $w(x_i) = p(x_i)/q(x_i)$ corrects each sample: regions where $q$ over-samples relative to $p$ get down-weighted, and vice versa.

The toy problem in the notebook uses
$$
f(x) = \sigma(x) = \frac{1}{1 + e^{-x}}, \qquad p(x) = \mathcal{N}(3.5,\,1).
$$

---

## Cell-by-cell walkthrough

### Cells 1–4 — Imports and define $f(x)$

```python
def f_x(x):
    return 1/(1 + np.exp(-x))
```

The sigmoid. We choose this just to have a simple bounded function whose expectation under a Gaussian is non-trivial. Plotting it from 0 to 4 shows it climbing from $\sigma(0)=0.5$ to $\sigma(4)\approx 0.98$.

### Cells 5–7 — Define $p$ and $q$, plot them

```python
mu_target, sigma_target = 3.5, 1   # p(x) = N(3.5, 1)
mu_appro,  sigma_appro  = 3,   1   # q(x) = N(3,   1)
p_x = stats.norm(mu_target, sigma_target)
q_x = stats.norm(mu_appro,  sigma_appro)
```

`p_x` is a scipy frozen normal — we use its `.pdf` to evaluate $p(x)$ at any point. The proposal $q$ is a Gaussian shifted slightly (mean 3 vs 3.5) with the same width. They overlap heavily, so this is a **good** proposal: every region of high $p$-mass is also covered by $q$.

### Cell 8 — Direct Monte Carlo (the "ground truth")

```python
s = 0
for i in range(n):
    x_i = np.random.normal(mu_target, sigma_target)   # x_i ~ p
    s += f_x(x_i)
print("simulate value", s/n)
```

This samples from $p$ directly and averages $f(x_i)$. Because $p$ has mean 3.5 (already in the saturating tail of the sigmoid), the answer comes out near $0.96$. This number is our reference.

### Cell 9 — Importance sampling estimator (the missing code)

```python
value_list = []
for i in range(n):
    x_i = np.random.normal(mu_appro, sigma_appro)         # x_i ~ q
    value = f_x(x_i) * (p_x.pdf(x_i) / q_x.pdf(x_i))      # weighted f
    value_list.append(value)
print("average {} variance {}".format(np.mean(value_list), np.var(value_list)))
```

Now we draw from $q$ instead of $p$ and multiply each $f(x_i)$ by the importance weight $w_i = p(x_i)/q(x_i)$. The mean of the weighted values approximates $\mathbb{E}_p[f]$.

With $q = \mathcal{N}(3,1)$ very close to $p = \mathcal{N}(3.5,1)$, the result is $\approx 0.959$ — essentially matches the direct estimator. **Variance $\approx 0.29$** — modest.

### Cells 10–12 — A *bad* proposal: $q = \mathcal{N}(1, 1)$

```python
n = 5000
mu_appro = 1            # bad proposal — far from p
```

Now $q$ is centred at 1 while $p$ is centred at 3.5. Their overlap is poor: most samples from $q$ land where $p$ has tiny density, so weights $w_i = p(x_i)/q(x_i)$ are mostly near zero — but a few rare samples that drift right into the tail of $q$ but the bulk of $p$ get **enormous** weights.

The output:
```
average 0.892, variance 55.5
```

The mean is still roughly correct (importance sampling is unbiased for any $q$ that covers $p$'s support), but the **variance has exploded by 200×**. This is the pathology of importance sampling: a poor proposal gives a few outlier samples that dominate the average. We needed 5× more samples and still got worse results.

### Why this happens (intuition)

Picture $p$ at 3.5 and $q$ at 1. A typical sample from $q$ is around $x \approx 1$, where $p(x)$ is tiny — weight is tiny, contribution is tiny. Occasionally $q$ produces an $x \approx 3$ — there $p(x)$ is large but $q(x)$ is tiny, so $w = p/q$ is huge. The estimator becomes a near-zero-baseline punctuated by spikes — high variance.

Mathematically the variance of the IS estimator scales with $\mathbb{E}_q[w(x)^2 f(x)^2]$, which blows up whenever $p$ has mass where $q$ doesn't.

---

## What to take away for the exam

- **The identity:** $\mathbb{E}_p[f] = \mathbb{E}_q\!\left[f(x)\,p(x)/q(x)\right]$ — write this from memory; it follows from multiplying and dividing by $q(x)$ inside the integral. ⚠️ *No formula sheet from Week 3 onwards.*
- **Importance weight:** $w(x) = p(x)/q(x)$. Estimator $\hat\mu = \tfrac{1}{n}\sum_i f(x_i)\,w(x_i)$ with $x_i \sim q$.
- **Unbiasedness:** holds for any $q$ whose support contains $\{x : p(x)f(x) \neq 0\}$.
- **Variance is the trap:** if $q$ has thinner tails than $p$ (or is shifted away from $p$'s mass), weights become extreme and variance explodes — even though the mean is still correct.
- **Rule of thumb for a good $q$:** $q$ should resemble $|f(x)|\,p(x)$ — heavier-tailed than $p$ if anything, never thinner.
- **Diagnostic — effective sample size:** $\mathrm{ESS} = \left(\sum w_i\right)^2 / \sum w_i^2$. The notebook's later MCMC-comparison cell computes this; ESS $\ll n$ signals weight degeneracy.
- **Conceptual exam question style:** "Why might importance sampling give a high-variance estimate? What property of $q$ matters?" — answer with the support / tail-thickness argument.
