# Task 1 — Minimising KL Divergence (Forward vs Reverse)

## The question (paraphrased)

> Use the Jupyter notebook to study how minimising the Kullback–Leibler divergence between a target $p$ and a parametric $q$ behaves.
>
> (a) Compare *forward* KL ($KL(p \| q)$) and *reverse* KL ($KL(q \| p)$) as optimisation objectives.
> (b) Investigate the effect of the number of optimisation iterations.
> (c) Investigate the effect of the initial parameters of $q$.

The concept being tested is **the asymmetry of KL divergence** and what that asymmetry *does* in practice. KL is not a distance — swap the arguments and you get a different objective with a different geometry. One choice gives you a "cover-everything" approximation; the other gives you a "find-the-best-mode" approximation. Variational Inference (next task) is built on the second choice, so understanding *why* matters.

Related wiki pages: [[kl-divergence]], [[entropy]], [[cross-entropy]], [[variational-inference]], [[mean-field-vi]], [[lecture-w6]], [[lecture-w4]].

---

## Recap: the two KL divergences

For continuous variables:

$$
D_{KL}(p \| q) = \int p(x)\,\log\frac{p(x)}{q(x)}\,dx \quad\text{(forward / "moment-matching")}
$$

$$
D_{KL}(q \| p) = \int q(x)\,\log\frac{q(x)}{p(x)}\,dx \quad\text{(reverse / "mode-seeking")}
$$

Both are non-negative and equal zero only when $p = q$ almost everywhere — but they punish disagreement in opposite directions:

- **Forward KL** weights by $p$. If $p(x) > 0$ but $q(x) \approx 0$, the integrand $\log(p/q)$ blows up and the loss explodes. So $q$ must put mass *everywhere* $p$ does. **Mode-covering.**
- **Reverse KL** weights by $q$. Wherever $q(x) > 0$ but $p(x) \approx 0$, $\log(q/p)$ explodes. So $q$ must avoid putting mass where $p$ is small. **Mode-seeking.**

That asymmetry is the entire moral of this task.

---

## Part 1 — Discrete KL warm-up

### Cells 1–2: define two discrete distributions

```python
events = ['red', 'green', 'blue']
p = [0.10, 0.40, 0.50]
q = [0.80, 0.15, 0.05]
```

A toy categorical example. The point is to make the asymmetry concrete with a calculator before doing anything fancy.

### Cell 3: visualise

A quick bar chart of $p$ and $q$. The two distributions clearly disagree — $p$ favours blue, $q$ favours red — so we expect both KLs to be large but **different**.

### Cell 6: implement KL

```python
def kl_divergence(p, q):
    p = np.array(p); q = np.array(q)
    return np.sum(p * np.log2(p / q))
```

This is the discrete formula

$$D_{KL}(p \| q) = \sum_i p_i \log_2 \frac{p_i}{q_i}$$

Using $\log_2$ gives the answer in **bits** (a nod to information theory: KL is the expected number of *extra* bits needed to encode samples from $p$ if you used a code optimised for $q$).

### Cell 7: numerical check

```
KL(P || Q): 1.927 bits
KL(Q || P): 2.022 bits
```

Same two distributions, two different numbers. **KL is not symmetric.** This is the simplest possible demonstration of the headline fact, and it sets up the rest of the task.

---

## Part 2 — Continuous KL via gradient descent on a Gaussian $q$

This part fits a single Gaussian $q(x) = \mathcal{N}(\mu, \sigma^2)$ to a *bimodal* target $p$ by optimising $(\mu, \sigma)$. Because $q$ has only one mode and $p$ has two, $q$ literally cannot fit $p$ exactly — the optimiser is forced to compromise, and the *form* of the compromise is what reveals the asymmetry.

### Cell 8: build the target $p$

```python
ptrue = distrax.MixtureSameFamily(
    mixture_distribution=distrax.Categorical(probs=[0.5, 0.5]),
    components_distribution=distrax.Normal(loc=[1, 10], scale=[1, 1.5]),
)
```

A 50/50 mixture:

$$p(x) = 0.5\,\mathcal{N}(1, 1^2) + 0.5\,\mathcal{N}(10, 1.5^2)$$

Two well-separated modes near $x=1$ and $x=10$. A *single* Gaussian cannot reproduce this — perfect for stress-testing the two KL objectives.

### Cell 9: Monte Carlo estimators of both KLs

```python
def kl_sampling_inverse(params, p, samples=100000):  # KL(q || p)
    q = distrax.Normal(loc=params[0], scale=params[1])
    sample_set = q.sample(seed=key, sample_shape=samples)
    return jnp.mean(q.log_prob(sample_set) - p.log_prob(sample_set))

def kl_sampling(params, p, samples=100000):          # KL(p || q)
    q = distrax.Normal(loc=params[0], scale=params[1])
    sample_set = p.sample(seed=key, sample_shape=samples)
    return jnp.mean(p.log_prob(sample_set) - q.log_prob(sample_set))
```

Two key things are happening here.

**Why sampling at all?** The KL integral $\int p \log(p/q)\,dx$ has no closed form when $p$ is a mixture of Gaussians and $q$ is a single Gaussian. So we use the Monte Carlo identity

$$
\mathbb{E}_{x \sim r}[f(x)] \approx \frac{1}{N}\sum_{i=1}^N f(x_i),\quad x_i \sim r
$$

with $f(x) = \log r(x) - \log s(x)$ to estimate $D_{KL}(r \| s)$.

**Why does the sampling distribution differ between the two functions?**

- Forward KL $D_{KL}(p \| q)$ is an expectation under $p$ — so we sample from $p$.
- Reverse KL $D_{KL}(q \| p)$ is an expectation under $q$ — so we sample from $q$.

This is exactly the point: in real Variational Inference you can sample from your variational $q$ but *not* from the true posterior $p$, which is one practical reason reverse KL is the workhorse objective.

### Cell 10: the training loop

```python
def fit(params, optimizer, loss_fun, n_itr):
    opt_state = optimizer.init(params)
    loss = []
    for i in range(n_itr):
        loss_value, grads = jax.value_and_grad(loss_fun)(params, ptrue, 100000)
        updates, opt_state = optimizer.update(grads, opt_state, params)
        params = optax.apply_updates(params, updates)
        loss.append(loss_value)
    return params, loss
```

Standard JAX gradient descent. `jax.value_and_grad` differentiates the (Monte-Carlo-estimated) loss with respect to the variational parameters $(\mu, \sigma)$, and Adam takes a step. Nothing fancy — this is just a vehicle to see the optimum each objective converges to.

### Cell 11: run both objectives from the *same* starting point

```python
optimizer = optax.adam(learning_rate=0.05)
n_itr = 400
params_one = jnp.array([5.0, 8.0])  # forward KL run
optimized_params_one, loss_one = fit(params=params_one, optimizer=optimizer,
                                     loss_fun=kl_sampling, n_itr=n_itr)
params_two = jnp.array([5.0, 8.0])  # reverse KL run
optimized_params_two, loss_two = fit(params=params_two, optimizer=optimizer,
                                     loss_fun=kl_sampling_inverse, n_itr=n_itr)
```

Identical initialisation $(\mu_0, \sigma_0) = (5, 8)$ — picked deliberately *between* the two modes with an inflated $\sigma$ so neither answer is favoured a priori. Same optimiser, same number of steps. The only thing that varies is the loss function.

### Cells 12–13: the punchline plots

The first figure is the **loss curve** (decreasing in both cases — gradient descent is working). The second figure is the *fitted $q$* overlaid on $p$:

- **Green curve — forward KL $\min_q D_{KL}(p \| q)$**: a wide, flat Gaussian that *straddles both modes*. Its mean lands near the midpoint of the two modes and its variance is huge to make sure $q$ has mass wherever $p$ does. Result: $q$ puts a lot of probability *between* the modes where $p$ has almost none — a poor approximation if you cared about high-probability regions, but it never assigns near-zero probability where $p$ has mass.
- **Orange curve — reverse KL $\min_q D_{KL}(q \| p)$**: a narrow Gaussian sitting *on one of the modes*. The other mode is completely ignored. This is "mode-seeking" or "mode-locking": $q$ is happy to miss half the truth provided everything it *does* claim is in a high-density region of $p$.

The mathematical reason in one line each:

- Forward: $D_{KL}(p \| q) = \int p \log(p/q)\,dx$ — penalises $q \approx 0$ where $p > 0$, so $q$ refuses to be narrow.
- Reverse: $D_{KL}(q \| p) = \int q \log(q/p)\,dx$ — penalises $q > 0$ where $p \approx 0$, so $q$ refuses to spread into the valley between modes.

---

## Parts (b) and (c) — what to vary

The notebook gives you the rig; the questions ask you to play with it.

### (b) Number of iterations

Re-run with `n_itr` set to something small (say 10, 50) and something large (1000+). What you should see:

- Too few iterations: $q$ has not finished moving from the initialisation — the loss curve is still steep at the end and the fitted $q$ is somewhere between init and the optimum.
- Enough iterations: loss curve flattens; $q$ sits at a (local) optimum.
- More than enough: the parameters jitter around the optimum because the Monte Carlo estimator is *stochastic* — each step uses a fresh sample. The loss does not go monotonically to zero; it plateaus around the minimum-achievable KL between a single Gaussian and a bimodal mixture.

### (c) Initial parameters

This is where reverse KL's mode-seeking nature really bites. Try:

- Initialise $(\mu_0, \sigma_0) = (1, 1)$ (near the left mode). Reverse KL locks onto mode 1.
- Initialise $(\mu_0, \sigma_0) = (10, 1)$ (near the right mode). Reverse KL locks onto mode 2.
- Initialise $(\mu_0, \sigma_0) = (5, 8)$ (the default). Either mode is reachable; which one the optimiser picks depends on the random seed and exact gradient noise.

Forward KL is much less sensitive — its objective surface is roughly convex in $\mu$, $\sigma$ for this setup, so most starting points converge to the same wide-fit answer.

The takeaway: **reverse KL has multiple local optima** when $p$ is multimodal. This is a practical headache for VI — your variational posterior depends on initialisation. Forward KL is more forgiving but is rarely the objective you can actually optimise (you'd need samples from $p$, which is the thing you don't have in Bayesian inference).

---

## What to take away for the exam

- **KL is asymmetric.** $D_{KL}(p \| q) \neq D_{KL}(q \| p)$ in general. Two different objectives with two different geometries. ⚠️ *Formula not given* — be ready to write either one down from memory.
- **Forward KL = mode-covering / "zero-avoiding".** Penalises $q$ for being small where $p$ is large; produces wide approximations that smear over multiple modes.
- **Reverse KL = mode-seeking / "zero-forcing".** Penalises $q$ for being large where $p$ is small; produces narrow approximations that lock onto one mode.
- **Why VI uses reverse KL.** You can sample from $q$ but not from the unknown posterior $p$, so only $D_{KL}(q \| p)$ is computable. This is set up here and exploited in [[task-2-variational-inference]].
- **Why the integral is estimated by sampling.** Closed forms are rarely available; Monte Carlo with $z_i \sim q$ gives the standard $\frac{1}{N}\sum (\log q(z_i) - \log p(z_i))$ estimator.
- **Multimodality + reverse KL = local optima.** Initialisation matters. A good exam answer will mention this when discussing limitations of mean-field VI.
- See [[kl-divergence]] for the full concept page and its links to [[entropy]] and [[cross-entropy]] (KL = cross-entropy minus entropy).
