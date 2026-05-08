# Task 3 — MCMC via Metropolis–Hastings (and IS vs RS vs MH comparison)

**Workshop tasks 6–8.** Implement Metropolis–Hastings (MH) in PyMC to draw samples from the target. Plot the trace, plot a histogram of post-burn-in samples against the target density, report the acceptance rate. Compare IS, RS, and MH on the same target.

**Concepts:** [[mcmc]], [[metropolis-hastings]], [[gibbs-sampling]], [[importance-sampling]], [[rejection-sampling]], [[monte-carlo-integration]], [[lecture-w5]]

---

## What we're trying to do

Importance sampling and rejection sampling both need a proposal $q(x)$ that resembles the target $p(x)$ globally. In high dimensions or when $p$ is awkward, finding such a $q$ — let alone a tight envelope $k\,q \ge p$ — is hopeless.

**MCMC** sidesteps the problem entirely. Instead of trying to draw independent samples from $p$, we build a **Markov chain** $x^{(0)}, x^{(1)}, x^{(2)}, \dots$ whose **stationary distribution** is $p$. Run it long enough and the states it visits behave like (correlated) samples from $p$. Crucially, we only need to evaluate $p$ up to a normalising constant — we never need to integrate it.

**Metropolis–Hastings** is the canonical MCMC scheme. From the current state $x$:

1. Propose a candidate $x' \sim q(x' \mid x)$ (a *transition* proposal — depends on the current state, unlike the global proposals in IS/RS).
2. Compute the acceptance probability
$$
A(x \to x') = \min\!\left(1,\; \frac{p(x')\,q(x \mid x')}{p(x)\,q(x' \mid x)}\right).
$$
3. With probability $A$ set $x_{\text{new}} = x'$; otherwise stay: $x_{\text{new}} = x$.

If $q$ is symmetric ($q(x' \mid x) = q(x \mid x')$, e.g. a Gaussian random walk), the formula simplifies to the **Metropolis** ratio
$$
A = \min\!\left(1,\; \frac{p(x')}{p(x)}\right).
$$
Notice $p$ appears as a ratio — any normalising constant cancels.

**Why it works (detailed balance):** the acceptance rule was constructed precisely so that
$$
p(x)\,T(x\to x') = p(x')\,T(x'\to x),
$$
where $T$ is the chain's transition kernel. Detailed balance $\Rightarrow$ $p$ is a stationary distribution of the chain. Together with irreducibility and aperiodicity, the chain converges to $p$.

**Burn-in:** the early samples reflect the (arbitrary) starting point, not $p$. Discard the first chunk to let the chain "forget" its initialisation.

The notebook reuses the same bimodal mixture target as the rejection-sampling section:
$$
p(x) \propto \mathcal{N}(x;\,30,\,10) + \mathcal{N}(x;\,80,\,20).
$$

---

## Cell-by-cell walkthrough

### Cell 24 — Normalised target for plotting

```python
def p_pdf(x):
    return p(x) / 2.0
```

The unnormalised mixture from the rejection-sampling section integrates to 2 (sum of two normalised Gaussians). MH only needs unnormalised $p$ — but for overlaying a *normalised* density on a `density=True` histogram, we divide by 2.

### Cell 25 — Build and run the MH sampler in PyMC

```python
def logp_target(x):
    logp1 = pm.logp(pm.Normal.dist(mu=30.0, sigma=10.0), x)
    logp2 = pm.logp(pm.Normal.dist(mu=80.0, sigma=20.0), x)
    return pm.math.logaddexp(logp1, logp2)
```

This returns $\log p(x)$ for the mixture. `logaddexp(a, b) = log(exp(a) + exp(b))` is the numerically stable way to add the two component densities in log space — naively exponentiating would underflow in the tails.

```python
with pm.Model() as model:
    x_mcmc = pm.Flat("x")                       # improper uniform "prior"
    pm.Potential("target", logp_target(x_mcmc)) # adds logp_target to the joint log density
    step = pm.Metropolis()
    idata = pm.sample(draws=20000, tune=2000, step=step, chains=1, cores=1, random_seed=42)
```

Two PyMC tricks:
- **`pm.Flat`** declares $x$ with no prior — log-density 0 everywhere. Combined with the `Potential`, the joint log-density that PyMC sees is exactly `logp_target(x)`. So we're directly targeting our $p$.
- **`pm.Potential`** adds an arbitrary term to the log-joint. This is the mechanism for plugging in a custom unnormalised log-density.
- **`pm.Metropolis()`** is the random-walk MH step (Gaussian proposal, scale auto-tuned during the `tune=2000` warmup phase).
- `draws=20000` post-tuning samples; `tune=2000` is the burn-in/warmup PyMC discards by default for *adaptation* — but we also keep our own `burn_in = tune` to discard from the *returned* samples to be safe.

```python
mh_samples = idata.posterior["x"].values.reshape(-1)
mh_post = mh_samples[burn_in:]
```

`mh_samples` is the full chain; `mh_post` drops the first 2000 to remove any residual burn-in transient.

### Cell 26 — Acceptance rate

```python
mh_acc = float(idata.sample_stats["accepted"].values.mean())
print("MH acceptance rate =", mh_acc)
```

About **0.42** in the solution. Folklore optimum for random-walk MH on smooth low-dim targets is around $0.234$–$0.44$ (Roberts & Rosenthal). Too high (e.g. $> 0.7$) means proposals are tiny and the chain barely moves — bad mixing. Too low ($< 0.1$) means proposals are too bold and almost everything gets rejected — chain stuck. PyMC's tuning targets a sensible regime.

### Cell 27 — Trace plot

```python
plt.plot(mh_samples, linewidth=0.6)
plt.axvline(burn_in, linestyle="--")
```

The trace should look like a hairy band that hovers around values consistent with the target — flipping between the two modes (~30 and ~80). Things to look for in your own runs:
- **No drift** — the band shouldn't be wandering off; that signals non-convergence.
- **Mode-switching** — for a bimodal target, the chain should visit both modes; a chain stuck in one is a failure mode of vanilla random-walk MH.
- **Burn-in transient** — early values often slope toward the typical region.

### Cell 28 — Histogram vs target pdf

```python
plt.hist(mh_post, bins=80, density=True, alpha=0.6, label="MH samples")
plt.plot(xs, p_pdf(xs), linewidth=2.0, label="target pdf")
```

Empirical histogram of the chain (after burn-in) should track the bimodal shape of $p_{\text{pdf}}$. Bumps near 30 and 80, with the right relative heights.

### Cell 29 — Importance sampling on the same target (for comparison)

```python
N = 10000
x_prop = np.random.normal(50, 30, size=N)        # same q as RS
w = p(x_prop) / (q(x_prop) + 1e-300)             # importance weights
w = w / w.sum()                                  # self-normalised IS

idx = np.random.choice(np.arange(N), size=N, replace=True, p=w)
is_samples = x_prop[idx]                         # SIR resampled draws

ess = 1.0 / np.sum(w**2)
print("IS ESS =", ess)                           # ~7517 / 10000
```

This is **self-normalised IS** followed by **sampling-importance-resampling (SIR)** — resample from $\{x_{\text{prop}}\}$ with probabilities proportional to the weights, to get an unweighted set of draws roughly distributed as $p$. The **effective sample size** $\mathrm{ESS} = 1/\sum w_i^2$ measures how many of the $N$ weighted samples we're "really" using; here $\sim 7500/10000$, indicating a healthy proposal.

### Cell 30 — Side-by-side comparison

The final plot overlays the normalised target with histograms from all three samplers (IS-resampled, RS-accepted, MH post-burn-in). All three should track the bimodal target — they're three different routes to the same destination.

---

## Summary table (from the solution notebook)

| Method | Output | Pros | Main drawbacks | Key check |
|---|---|---|---|---|
| **IS** | estimate $\mathbb{E}_p[f]$ via weights | simple, fast in low-D, reuse samples | weight degeneracy if $q$ misses $p$ | ESS of weights |
| **RS** | i.i.d. samples $\sim p$ | exact i.i.d. samples | need envelope $k\,q$; acceptance $\to 0$ in high-D | acceptance rate $= 1/k$ |
| **MH (MCMC)** | samples $\sim p$ (correlated) | no $k$, no normaliser, scales to high-D | burn-in + autocorrelation; tuning, mixing | trace plot + acceptance rate |

---

## What to take away for the exam

⚠️ **MCMC and Metropolis–Hastings are core Week 5 examinable material — no formula sheet provided.**

- **MH acceptance probability** (general): $A(x \to x') = \min\!\left(1,\, \dfrac{p(x')\,q(x \mid x')}{p(x)\,q(x' \mid x)}\right)$. Memorise this.
- **Symmetric proposal (Metropolis):** $A = \min(1, p(x')/p(x))$. The normaliser of $p$ cancels — this is *the* reason MCMC works for unnormalised posteriors.
- **Detailed balance:** $p(x)\,T(x \to x') = p(x')\,T(x' \to x)$. Be able to verify the MH kernel satisfies it (sub in the acceptance rule and the proposal density, both directions cancel).
- **Stationarity from detailed balance:** if detailed balance holds for $p$ then $p$ is invariant under $T$. Combined with irreducibility + aperiodicity gives convergence.
- **Burn-in:** discard the early correlated-with-initialisation samples; only post-burn-in samples are used for estimates.
- **Acceptance rate as a tuning diagnostic:** ~0.234 is asymptotically optimal for high-dimensional random-walk MH; ~0.4 is a reasonable target in 1D. Too high $\Rightarrow$ proposals too small; too low $\Rightarrow$ proposals too large.
- **MCMC vs IS vs RS:**
  - IS/RS need a global $q$ that covers $p$; MH only needs a *local* proposal $q(x' \mid x)$.
  - IS/RS give independent samples (or weighted estimates); MH samples are correlated — effective sample size is much less than chain length.
  - Only MH gracefully extends to high-dimensional / unnormalised posteriors, which is why it dominates Bayesian inference in practice.
- **Likely exam question shapes:**
  - Derive / state the MH acceptance probability and explain each term.
  - "Why does MCMC only need $p$ up to a normalising constant?" — the constant cancels in the ratio $p(x')/p(x)$.
  - Sketch a trace plot and identify burn-in / poor mixing / multi-modal trapping.
  - Contrast with rejection sampling: when does each fail, and why does MCMC scale better?
