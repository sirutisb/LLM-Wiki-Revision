# Task 2 — Rejection Sampling

**Workshop tasks 3–5.** Implement rejection sampling, calculate the acceptance ratio, and investigate the effect of changing $k$ and the total number of samples.

**Concepts:** [[rejection-sampling]], [[monte-carlo-integration]], [[lecture-w5]]

---

## What we're trying to do

Importance sampling reweights samples to estimate an expectation. **Rejection sampling** does something stronger — it produces actual i.i.d. samples from the target $p(x)$, by drawing from a proposal $q(x)$ and throwing some away.

The recipe:

1. Pick a proposal $q$ we *can* sample from, and a constant $k$ such that
$$
p(x) \le k\,q(x) \quad \text{for all } x.
$$
The curve $k\,q$ is an **envelope** sitting above $p$ everywhere.

2. Draw $x \sim q$ and an independent $u \sim \mathrm{Uniform}(0,1)$.

3. **Accept** $x$ if
$$
u \le \frac{p(x)}{k\,q(x)},
$$
otherwise **reject** and try again.

Geometrically: we sample uniformly under the envelope $k\,q$; we keep the points that also fall under $p$. The accepted points are exactly i.i.d. draws from $p$.

The **acceptance probability** is
$$
\Pr(\text{accept}) = \frac{1}{k}\int p(x)\,dx = \frac{1}{k}
$$
(when $p$ is normalised). So $k$ is *exactly* the inverse efficiency: $k=2$ means we keep half our proposals, $k=10$ means we keep one in ten.

In the notebook, the target is an unnormalised Gaussian mixture
$$
p(x) = \mathcal{N}(x;\,30,\,10) + \mathcal{N}(x;\,80,\,20)
$$
(integrates to 2, not 1 — handled later via $p/2$ for plotting), and the proposal is $q(x) = \mathcal{N}(x;\,50,\,30)$.

---

## Cell-by-cell walkthrough

### Cells 14–17 — Define $p$, $q$, plot

```python
def p(x): return norm.pdf(x, 30, 10) + norm.pdf(x, 80, 20)
def q(x): return norm.pdf(x, 50, 30)
```

The target is bimodal (peaks near 30 and 80). The proposal is a single broad Gaussian centred between the two modes with large $\sigma=30$, so it covers the whole region where $p$ has mass. **Wide and flat is what you want from $q$ in rejection sampling.**

### Cell 18 — Compute the envelope constant $k$

```python
k = max(p(x) / q(x))
```

We want the smallest $k$ such that $k\,q(x) \ge p(x)$ everywhere — i.e. $k = \sup_x p(x)/q(x)$. The notebook approximates the supremum by evaluating $p/q$ on a grid `x = arange(-50, 151)` and taking the max. (A comment notes "better to use supremum" — analytically this would be exact.)

If we pick $k$ too small, the envelope dips below $p$ and the algorithm is invalid. If we pick $k$ too large, the envelope is too loose and we waste proposals.

### Cell 19 — Verify the envelope visually

Plotting $p(x)$ and $k\,q(x)$ together: the scaled proposal sits just above $p$, touching it at the tightest point. That's the picture to keep in your head.

### Cell 20 — The sampler

```python
def sample(size):
    xs = np.random.normal(50, 30, size=size)        # x_i ~ q
    cs = np.random.uniform(0, 1, size=size)         # u_i ~ U(0,1)
    mask = p(xs) / (k * q(xs)) >= cs                # accept if u <= p/(kq)
    return xs[mask]
```

A vectorised one-pass implementation. Note this returns *fewer than `size`* samples — it does one batch of proposals and keeps the survivors. The function is named `sample(size)` but `size` is the number of *proposals*, not the number of accepted draws.

### Cell 21 — Acceptance ratio

```python
n_samples = 10000
accept_ratios = len(sample(n_samples)) / n_samples
print(accept_ratios)   # ≈ 0.52
```

About 52% of proposals accepted. Cross-check: $1/k$ should equal this (with the normalised $p/2$, since the unnormalised $p$ integrates to 2, the effective acceptance is $2/k$). The number 0.52 says $k \approx 3.85$ for the normalised target — reasonable for a single-Gaussian envelope around a bimodal target.

### Cell 22 — Histogram the accepted samples

```python
sns.distplot(sample(n_samples))
```

The empirical density of accepted points has the bimodal shape of $p$ — the two bumps near 30 and 80 reappear automatically, even though we never sampled from $p$ directly.

---

## Effect of $k$ (task 4)

- **$k$ exactly equal to $\sup_x p(x)/q(x)$** — tightest valid envelope, highest acceptance, most efficient.
- **$k$ larger than necessary** — still valid (envelope still covers $p$), but the gap between $kq$ and $p$ grows, so more proposals fall in the "envelope but not under $p$" region and get rejected. Acceptance ratio shrinks proportionally to $1/k$.
- **$k$ smaller than $\sup p/q$** — the envelope dips below $p$ in some region; the ratio $p(x)/(kq(x))$ exceeds 1 there, so the accept condition $u \le p/(kq)$ is *always* true — those regions are over-sampled, and the output is no longer distributed as $p$. **The algorithm is broken.**

So $k$ is a knife-edge: as small as possible without ever violating $kq \ge p$.

## Effect of total samples (task 5)

More proposals $\Rightarrow$ more accepted samples $\Rightarrow$ smoother histogram approximation of $p$. Acceptance *ratio* itself doesn't change with sample count (it's a property of $p, q, k$); only the Monte Carlo noise on the histogram shrinks like $1/\sqrt{N_{\text{accepted}}}$.

---

## What to take away for the exam

- **Setup condition:** find $k$ with $k\,q(x) \ge p(x)$ everywhere; ideally $k = \sup_x p(x)/q(x)$. ⚠️ *No formula sheet.*
- **Algorithm:** draw $x \sim q$, $u \sim U(0,1)$; accept iff $u \le p(x)/(k\,q(x))$. Accepted samples are i.i.d. from $p$.
- **Acceptance probability $= 1/k$** when $p$ is normalised. This is the efficiency — the fraction of proposals you keep.
- **Why it works (geometric argument):** $(x, u\,k\,q(x))$ is uniform under the curve $k\,q$; the accept condition restricts to the region under $p$, and uniform-under-$p$ has marginal density $\propto p(x)$.
- **Failure modes:**
  - $q$ doesn't cover the support of $p$ → some regions never sampled → biased.
  - $q$ much narrower / has thinner tails than $p$ → $\sup p/q$ huge → $k$ huge → acceptance dies.
  - In high dimensions, $k$ typically grows exponentially with dimension — rejection sampling becomes useless.
- **Compared to importance sampling:** RS gives genuine i.i.d. samples (good for plotting, downstream estimators); IS only gives weighted estimates of expectations. Both need a good $q$, but RS additionally needs a *bound* $k$ — which is much more demanding than "low variance weights".
- **Compared to MCMC:** RS produces independent samples (great); MCMC samples are correlated. But MCMC scales to high dimensions where RS doesn't.
