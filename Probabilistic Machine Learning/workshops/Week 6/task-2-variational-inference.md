# Task 2 — Variational Inference via the ELBO

## The question (paraphrased)

> Optimise a variational distribution $q(z)$ by **maximising the ELBO**, which is equivalent to **minimising the reverse KL** $D_{KL}(q(z) \| p(z \mid x))$. Implement and run the full pipeline in the notebook: log-likelihood, Monte Carlo KL, ELBO, and the gradient-based optimiser.

This is the practical payoff of [[task-1-kl-divergence]]. Reverse KL is the right objective for posterior approximation — but $p(z \mid x)$ is intractable, so we cannot evaluate it directly. The ELBO is the trick that lets us optimise reverse KL *without ever computing the posterior*.

VI/ELBO is an exam-priority topic and ⚠️ **no formulas are given on the formula sheet from Week 3 onwards**. You need the ELBO derivation in your head.

Related wiki pages: [[variational-inference]], [[elbo]], [[mean-field-vi]], [[kl-divergence]], [[bayesian-inference]], [[elbo-derivation]], [[lecture-w4]], [[supp-elbo]].

---

## Why the ELBO exists at all

The Bayesian inference setup:

$$
p(z \mid x) = \frac{p(x \mid z)\,p(z)}{p(x)}, \qquad p(x) = \int p(x \mid z)\,p(z)\,dz
$$

The denominator $p(x)$ — the **evidence** — is usually a high-dimensional integral that we can't compute. So the posterior $p(z \mid x)$ is "known up to a constant" but not directly usable.

VI sidesteps this by picking a tractable family $q(z; \phi)$ (e.g. a Gaussian) and tuning $\phi$ to make $q$ close to the posterior. The natural objective is

$$
\min_\phi D_{KL}\!\left(q(z) \,\big\|\, p(z \mid x)\right)
$$

but this still depends on $p(z \mid x)$ which we can't compute.

**The trick.** Expand the KL using $p(z \mid x) = p(x, z)/p(x)$:

$$
\begin{aligned}
D_{KL}(q \| p(z\mid x))
&= \mathbb{E}_q[\log q(z) - \log p(z \mid x)] \\
&= \mathbb{E}_q[\log q(z) - \log p(x, z) + \log p(x)] \\
&= \underbrace{-\big(\mathbb{E}_q[\log p(x, z)] - \mathbb{E}_q[\log q(z)]\big)}_{-\mathcal{L}(q)} + \log p(x).
\end{aligned}
$$

Rearranging:

$$
\log p(x) = \mathcal{L}(q) + D_{KL}(q \| p(z \mid x))
$$

Since $\log p(x)$ is a constant (it does not depend on $q$) and KL is non-negative, $\mathcal{L}(q) \le \log p(x)$ — hence "Evidence Lower BOund". And since $\log p(x)$ is fixed, **maximising $\mathcal{L}(q)$ is equivalent to minimising $D_{KL}(q \| p(z \mid x))$**, which is exactly the reverse KL we wanted.

The form actually used in code is the **likelihood–KL split**:

$$
\boxed{\mathcal{L}(q) \;=\; \mathbb{E}_{q(z)}[\log p(x \mid z)] \;-\; D_{KL}\!\big(q(z)\,\|\,p(z)\big)}
$$

This drops the intractable $p(z \mid x)$ and replaces it with two things we *can* compute: the (per-sample) likelihood $p(x \mid z)$ and the KL between $q$ and the **prior** $p(z)$ — both of which are designed by us. Full derivation lives in [[elbo-derivation]] / [[supp-elbo]].

---

## The setup the notebook builds

| Symbol | What it is in this notebook |
|---|---|
| $z$ | The latent variable. Continuous. |
| $p(z)$ | A bimodal Gaussian mixture, $0.5\,\mathcal{N}(1,1) + 0.5\,\mathcal{N}(10,1.5^2)$ — used as the **prior**. |
| $p(x \mid z)$ | $\mathcal{N}(x \mid z,\,0.5^2)$ — Gaussian likelihood centred at $z$. |
| $q(z; \phi)$ | $\mathcal{N}(\mu, \sigma^2)$ — the variational distribution we will fit. |
| $\phi$ | Variational parameters $(\mu, \log\sigma)$ that we optimise. |
| $x_{\text{obs}}$ | Four observations $\{1.5, 2.0, 3.0, 4.5\}$ — clustered near the *left* prior mode. |

Because the data sits near $z \approx 2$, the true posterior $p(z \mid x)$ should concentrate on the **left** mode of the prior — and we'll see $q$ discover this.

---

## Cell-by-cell walkthrough

### Cell 4: define $p(z)$ (the prior)

```python
ptrue = distrax.MixtureSameFamily(
    mixture_distribution=distrax.Categorical(probs=[0.5, 0.5]),
    components_distribution=distrax.Normal(loc=[1, 10], scale=[1, 1.5]),
)
```

This is the same bimodal mixture as Task 1 — but here it has a different role. In Task 1 it was the *target* for KL minimisation. Here it is the **prior** $p(z)$ over the latent. The posterior $p(z \mid x)$ is what we actually want to approximate, and that posterior depends on the data $x_{\text{obs}}$.

### Cell 4 (cont): the log-likelihood

```python
likelihood_std = 0.5
def log_likelihood(x, z):
    return distrax.Normal(z, likelihood_std).log_prob(x)
```

A direct encoding of $p(x \mid z) = \mathcal{N}(x \mid z, 0.5^2)$. The `log_prob` returns $\log p(x \mid z)$ — exactly the quantity that goes inside the ELBO's first expectation.

The narrow likelihood width ($\sigma = 0.5$) matters: it means each observation $x$ is fairly informative about $z$, so the posterior will be sharp and clearly favour one of the two prior modes.

### Cell 4 (cont): Monte Carlo reverse KL

```python
def kl_sampling_inverse(params, p, samples=100000):
    q = distrax.Normal(loc=params[0], scale=params[1])
    sample_set = q.sample(seed=jax.random.PRNGKey(0), sample_shape=samples)
    return jnp.mean(q.log_prob(sample_set) - p.log_prob(sample_set))
```

This estimates

$$
D_{KL}(q \| p) \approx \frac{1}{N}\sum_{i=1}^N \big(\log q(z_i) - \log p(z_i)\big),\quad z_i \sim q
$$

Note we sample from $q$, *not* from $p$ (compare with forward KL in Task 1). This is what makes reverse KL practically computable — we always know how to sample from our own variational distribution.

### Cell 4 (cont): the ELBO

```python
def elbo(params, x_batch, samples=1000):
    mu, log_sigma = params
    sigma = jnp.exp(log_sigma)
    q_z = distrax.Normal(mu, sigma)

    # Sample from q(z)
    z_samples = q_z.sample(seed=jax.random.PRNGKey(0), sample_shape=(samples,))

    # E_q[log p(x | z)] over a batch of x
    log_lik = jnp.mean(jax.vmap(log_likelihood, in_axes=(0, None))(x_batch, z_samples))

    # KL(q || prior)
    kl = kl_sampling_inverse(params, ptrue, samples)

    return log_lik - kl
```

Three things to notice:

**1. The reparameterisation: $\sigma = \exp(\log\sigma)$.** We optimise `log_sigma` rather than `sigma` directly so that $\sigma > 0$ is automatically enforced — gradient steps on `log_sigma` can never push $\sigma$ negative. Standard trick for any positive parameter.

**2. The mean-field assumption.** `q_z = distrax.Normal(mu, sigma)` is a *single, factorised* Gaussian. Mean-field VI assumes

$$q(z_1, z_2, \dots, z_d) = \prod_i q(z_i)$$

i.e. the variational posterior treats latents as independent. Here $z$ is one-dimensional so this is trivial — but the *form* (one independent Gaussian per latent) is the mean-field commitment. See [[mean-field-vi]].

**3. The two terms.**
- `log_lik` is the Monte-Carlo estimate of $\mathbb{E}_{q(z)}[\log p(x \mid z)]$ — the "data fit" term. It rewards $q$ for placing mass on $z$-values that explain the observations $x$.
- `kl` is $D_{KL}(q \| p(z))$ — the "regulariser". It punishes $q$ for drifting away from the prior $p(z)$.

ELBO $=$ data fit $-$ regulariser. This is the same trade-off you see everywhere in Bayesian ML: the data pulls the posterior towards values that fit; the prior pulls it back. The optimum balances the two.

### Cell 4 (cont): the optimisation loop

```python
def fit_vi(params, optimizer, n_itr, x_batch):
    opt_state = optimizer.init(params)
    loss = []
    for i in range(n_itr):
        loss_value, grads = jax.value_and_grad(lambda p: -elbo(p, x_batch))(params)
        updates, opt_state = optimizer.update(grads, opt_state, params)
        params = optax.apply_updates(params, updates)
        loss.append(-loss_value)  # store +ELBO for plotting
    return params, loss
```

We **maximise** ELBO, but optax minimises — so we hand the optimiser $-\mathcal{L}$ and flip the sign back when storing the loss history. Same `value_and_grad` recipe as Task 1.

This is *gradient ascent on the ELBO* — sometimes called **stochastic VI** because the gradient is computed from Monte Carlo samples and is therefore noisy. Closed-form alternative: **CAVI** (coordinate ascent VI) updates each $q(z_i)$ analytically when the model is conjugate; we don't use that here because we're staying generic.

### Cell 4 (cont): training and visualisation

```python
x_obs = jnp.array([1.5, 2.0, 3.0, 4.5])
params = jnp.array([5.0, 1.0])  # initial (mu, log_sigma)
optimizer = optax.adam(learning_rate=0.01)
n_itr = 400
opt_params, loss_history = fit_vi(params, optimizer, n_itr, x_obs)
```

Initial $\mu_0 = 5$ sits *between* the two prior modes. Adam at lr $0.01$, 400 iterations.

Two plots come out:

**Left panel — ELBO vs iteration.** Should rise rapidly then plateau. A healthy ELBO curve goes **up** and stabilises:

- Up: the optimiser is finding better $q$.
- Stabilises: $q$ has reached a local maximum of the ELBO.
- Bad signs the notebook flags: decreasing, wildly oscillating, flat from step 1, or NaN.

**Right panel — $q(z)$ vs prior $p(z)$.** The prior is the bimodal mixture (dashed). The fitted $q$ is a single narrow Gaussian, and you should see $\mu_{\text{opt}} \approx 2.7$ — sitting on the **left** mode of the prior, near the mean of the observations.

That's the right answer. The data $\{1.5, 2.0, 3.0, 4.5\}$ has likelihood concentrated near $z \approx 2.7$ (the data mean), and the prior already has a mode near $z = 1$. So the posterior — which combines them — sits on the left mode and ignores the right mode entirely. Reverse KL's mode-seeking behaviour from Task 1 makes $q$ commit fully to that left mode rather than smearing over both.

### What this demonstrates end-to-end

1. We never computed the posterior $p(z \mid x)$ directly. We never computed the evidence $p(x)$.
2. We used only $\log p(x \mid z)$ (designed by us), $\log p(z)$ (the prior, designed by us), and samples from $q(z)$ (which is in our variational family).
3. By gradient-ascending the ELBO, we obtained $q^* \approx p(z \mid x)$ — a working approximation to the posterior.

That's variational inference.

---

## What to take away for the exam

- **The ELBO formula** ⚠️ *not given*:

  $$\mathcal{L}(q) = \mathbb{E}_{q(z)}[\log p(x \mid z)] - D_{KL}\!\big(q(z) \,\|\, p(z)\big)$$

  Be ready to write this from memory and identify the two terms ("expected log-likelihood" and "KL to prior").

- **The identity** ⚠️ *must memorise*:

  $$\log p(x) = \mathcal{L}(q) + D_{KL}\!\big(q(z) \,\|\, p(z \mid x)\big)$$

  Three consequences in one breath: (1) the ELBO is a lower bound on the log-evidence; (2) the bound is tight iff $q$ equals the true posterior; (3) maximising ELBO $\equiv$ minimising reverse KL to the posterior. See [[elbo-derivation]] for the full chain of equalities.

- **Why ELBO and not direct KL?** $D_{KL}(q \| p(z\mid x))$ requires the intractable $p(z \mid x)$. ELBO replaces it with $p(x, z) = p(x \mid z)p(z)$, which we have closed forms for.

- **Mean-field assumption.** $q(z) = \prod_i q(z_i)$ — independent factor per latent. Tractable and scalable but cannot represent posterior correlations between latents. See [[mean-field-vi]].

- **The data fit / regulariser trade-off.** Look for it in any Bayesian ML question. ELBO = $\mathbb{E}_q[\log p(x \mid z)]$ (data) $-$ $D_{KL}(q \| p(z))$ (prior pull-back). Higher likelihood width $\Rightarrow$ data dominates; tighter prior $\Rightarrow$ prior dominates.

- **Reverse KL is mode-seeking** (Task 1). With multimodal posteriors, mean-field VI commits to one mode and underestimates posterior variance — a textbook limitation worth one or two sentences in any "discuss VI" answer.

- **Mechanics for short-answer questions.** "Why is VI used?" $\to$ posterior is intractable. "How is it optimised?" $\to$ maximise ELBO via gradient ascent (or CAVI when conjugate). "What does it return?" $\to$ a tractable $q$ that approximates the posterior. "Trade-offs?" $\to$ biased (mean-field cannot model correlations, mode-seeking) but fast and deterministic, in contrast to MCMC which is unbiased asymptotically but slow ([[mcmc]]).

- See [[elbo]], [[variational-inference]], [[mean-field-vi]] for the concept pages, and [[supp-elbo]] / [[elbo-derivation]] for the full derivation.
