# Task 1 — Laplace on the Beta-Bernoulli (sanity check against the closed form)

**Notebook:** `Coding_Template_laplace_bionorm.ipynb` / `solution_laplace_bionorm.ipynb`
**Goal:** Validate the [[laplace-approximation]] machinery on a model where we *already know* the exact posterior — the Beta-Bernoulli conjugate pair. If our Gaussian approximation looks reasonable next to the true Beta posterior, we can trust the same procedure on harder problems (Task 2).

> The notebook's filename says "binormal" but the model is Beta-Bernoulli — the bivariate flavour shows up only in Task 2 where we approximate a 2-D logistic regression posterior. Treat this task as the 1-D warm-up.

## What's being tested

The exam-relevant skill set is:

1. Recognise that a [[laplace-approximation]] replaces an awkward posterior $p(\theta\mid\mathcal{D})$ with a Gaussian $q(\theta) = \mathcal{N}(\theta_{\text{MAP}}, H^{-1})$ centred at the [[map]] estimate, with covariance equal to the inverse curvature of the *negative* log-posterior at that mode.
2. Compute the [[map]] of a posterior whose form you can write down.
3. Compute the second derivative of $\log p(\theta\mid\mathcal{D})$ analytically and convert it into a Laplace variance.
4. Compare the Gaussian to the truth and reason about *where* the approximation breaks (boundaries, skew, multi-modality).

> Formula status: the [[laplace-approximation]] formula is **not** on the exam formula sheet (Weeks 3-9 are unaided). You must be able to write $q(\theta) = \mathcal{N}(\theta_{\text{MAP}}, H^{-1})$ and explain where it comes from from memory.

## The model under test

We have a coin flipped $n=11$ times with $n_1=1$ head, $n_0=10$ tails. The conjugate Beta-Bernoulli model says:

$$
\theta \sim \mathrm{Beta}(\alpha_0, \beta_0), \qquad y_i \mid \theta \sim \mathrm{Bernoulli}(\theta)
$$

With a uniform prior $\alpha_0 = \beta_0 = 1$ the **exact** posterior is

$$
\theta \mid \mathbf{y} \sim \mathrm{Beta}(\alpha_0 + n_1,\; \beta_0 + n_0) = \mathrm{Beta}(2, 11)
$$

This posterior is sharply skewed toward $0$ — exactly the kind of shape a centred Gaussian struggles with. That's the point: we want to see *how badly* Laplace fails on a skewed, near-boundary target.

## Cell-by-cell walkthrough

### Imports and shim distributions

```python
class BetaDist:  # wraps jax.scipy.stats.beta
class BernoulliDist:  # wraps jnp manually
```

The notebook stubs out `BetaDist` and `BernoulliDist` because TensorFlow Probability's JAX substrate is broken on modern JAX. Nothing conceptual here — just a thin façade providing `.prob()`, `.log_prob()`, `.sample()`. The real work uses PyMC and SciPy.

### Data

```python
dataset = np.repeat([0, 1], (10, 1))   # 10 tails, 1 head
n_heads = dataset.sum()                # = 1
n_tails = n_samples - n_heads          # = 10
```

A deliberately small, lopsided sample. With only one success in eleven trials the likelihood pushes the posterior hard toward $\theta = 0$, so the mode sits near the boundary of the simplex $[0,1]$. That is where any Gaussian approximation is going to look ugly.

### Prior, likelihood, exact posterior plot

```python
exact_posterior = BetaDist(concentration1=a + n_heads,
                           concentration0=b + n_tails)  # Beta(2, 11)
```

This cell draws three curves on the same axes:

- **Prior** — flat $\mathrm{Beta}(1,1)$, a sanity reference.
- **Likelihood** $\theta^{n_1}(1-\theta)^{n_0}$ — peaks at the [[mle]] $\theta = 1/11 \approx 0.091$.
- **True posterior** — the Beta(2, 11) we just wrote down.

The picture is the *target* — Task 1 succeeds if our Laplace Gaussian (computed below) lands close to the green dashed line.

### Why the naive PyMC `find_hessian` shortcut is wrong

The commented-out block shows the seductive one-liner:

```python
# std_q = ((1 / pm.find_hessian(mean_q, vars=[theta])) ** 0.5)[0]
```

The notebook explicitly flags this as broken. Two reasons:

1. **Sign convention.** A Laplace covariance is $H^{-1}$ where $H = -\nabla^2 \log p(\theta\mid\mathcal{D})$ (note the minus sign — it makes $H$ positive at a maximum). PyMC's `find_hessian` does its own sign handling depending on version, so blindly inverting it can yield negative variances.
2. **Constrained variables.** PyMC silently transforms $\theta \in (0,1)$ to $\eta = \mathrm{logit}(\theta) \in \mathbb{R}$ before optimising. Its Hessian is therefore on the **unconstrained scale**, not the $\theta$-scale you want to plot. Without a Jacobian correction the units are simply wrong.

So instead of trusting the framework, we compute the curvature analytically.

### Closed-form Laplace ingredients (the markdown derivation cell)

The notebook walks through the algebra you must reproduce in the exam:

$$
\log p(\theta\mid \mathbf{y}) = (\alpha_{\text{post}}-1)\log\theta + (\beta_{\text{post}}-1)\log(1-\theta) + C
$$

Differentiate twice:

$$
\frac{d^2}{d\theta^2}\log p(\theta\mid\mathbf{y}) = -\frac{\alpha_{\text{post}}-1}{\theta^2} - \frac{\beta_{\text{post}}-1}{(1-\theta)^2}
$$

This is **always negative** at an interior mode (good — it confirms a maximum). The Laplace variance is

$$
\sigma^2_{\text{Lap}} = \left(-\frac{d^2}{d\theta^2}\log p(\theta\mid\mathbf{y}) \Big|_{\theta_{\text{MAP}}}\right)^{-1}
$$

This is the 1-D specialisation of the general $q(\theta) = \mathcal{N}(\theta_{\text{MAP}}, H^{-1})$.

The MAP is the mode of Beta$(\alpha_\text{post}, \beta_\text{post})$:

$$
\theta_{\text{MAP}} = \frac{\alpha_{\text{post}}-1}{\alpha_{\text{post}} + \beta_{\text{post}} - 2} = \frac{1}{11}
$$

### Computing the Gaussian numerically

```python
mean_q = pm.find_MAP()
loc    = float(mean_q["theta"])           # = 1/11
a_post = 1.0 + n_heads                    # = 2
b_post = 1.0 + n_tails                    # = 11
H_theta = -(a_post - 1)/loc**2 - (b_post - 1)/(1-loc)**2
std_q   = float(np.sqrt(1.0 / (-H_theta)))  # ≈ 0.0867
```

A few things worth registering:

- `pm.find_MAP()` is the *numerical* version of the analytical mode formula. It runs an optimiser (BFGS by default) to maximise $\log p(\theta\mid\mathcal{D})$. We use it because in Task 2 there is no analytical mode; here it just confirms we agree with the closed form.
- `H_theta` is the *signed* second derivative of the log-posterior — negative at a max — so `1/(-H_theta)` is the variance. Square root for the standard deviation.
- The result $\sigma_{\text{Lap}} \approx 0.0867$ is suspiciously close to the MAP value of $0.0909$. The Gaussian's left tail will spill into negative $\theta$ — territory the Beta cannot reach.

### Plotting Laplace vs exact posterior

```python
laplace_pdf = stats.norm.pdf(x_np, loc, std_q)
laplace_pdf /= np.trapezoid(laplace_pdf, x_np)   # renormalise on [0,1]
```

Renormalising on $[0,1]$ is a cosmetic fix. The Gaussian puts mass on $\theta < 0$, which is impossible. By dividing by the integral over $[0,1]$ we make a cleaner plot, but it does not fix the underlying mismatch.

The final figure (cell with `stats.beta.pdf(x, n_heads + 1, n_tails + 1)`) overlays the exact Beta(2, 11) and the Laplace Gaussian. You should see:

- Both curves agree at the mode and in its immediate neighbourhood.
- The Beta is **right-skewed** with a long tail toward $\theta = 1$. The Gaussian, being symmetric, can't capture this — it cuts off the tail too early.
- The Gaussian assigns probability mass to $\theta < 0$. The Beta cannot.
- Near $\theta = 0$ both densities rise sharply, but the Gaussian's slope is wrong because it doesn't know about the boundary.

That mismatch is exactly the lesson of the task. **Laplace is a *local* approximation around the mode.** It is good when the posterior is unimodal and roughly Gaussian; it is poor when the posterior is skewed, bounded, or multi-modal.

## What to take away for the exam

- **Memorise the formula:** $q(\theta) = \mathcal{N}(\theta_{\text{MAP}}, H^{-1})$ with $H = -\nabla^2 \log p(\theta\mid\mathcal{D})\big|_{\theta_{\text{MAP}}}$. Not on the formula sheet (Weeks 3-9 unaided).
- **Two ingredients only:** the [[map]] (where to centre) and the negative Hessian of the log-posterior (how wide). Everything else is plotting.
- **Sign conventions matter.** The Hessian of $\log p$ is negative at a maximum. The Hessian of $-\log p$ is positive. Many derivations and many libraries silently flip the sign — track which one you have before inverting.
- **Connection to other tools:** the same Hessian shows up in the [[bic]] penalty $-\tfrac{1}{2}\log\det H$ and in confidence intervals around the [[mle]]. They all measure how peaked the log-likelihood / log-posterior is at its mode.
- **When Laplace fails:** skewed posteriors (this task), multi-modal posteriors (mode-seeking, ignores other modes), and near-boundary modes (Gaussian leaks past the support). For those cases the course will introduce [[variational-inference]] and [[mcmc]].
- **Why we used a model with a closed form:** sanity check. Using Laplace on a Beta-Bernoulli is overkill in practice — but it lets us *see* the approximation error in a controlled setting before applying the same procedure to logistic regression in Task 2.

**Related pages:** [[laplace-approximation]], [[map]], [[bayesian-inference]], [[conjugate-priors]], [[mle]], [[bic]], [[lecture-w3]].
