# Variational Inference (VI)

**Type:** approximation method
**Week:** 4
**Related:** [[elbo]], [[kl-divergence]], [[mean-field-vi]], [[laplace-approximation]], [[mcmc]], [[variational-autoencoder]]
**Source:** [[lecture-w4]], [[supp-elbo]], [[lecture-w10]]

## Definition
Variational inference approximates an intractable posterior $p(\theta|\mathcal{D})$ by solving an optimisation problem: find the distribution $q(\theta)$ from a tractable family $\mathcal{Q}$ that minimises the KL divergence to the true posterior.

## Motivation
The Laplace approximation is local (Gaussian near the MAP only) and fails for multimodal or skewed posteriors. VI is a **global** approximation: it searches over an entire family of distributions to find the one closest to the true posterior. Unlike MCMC, it produces a deterministic, differentiable approximation that scales well to large datasets.

## How it works

**Objective**: minimise the reverse KL divergence:
$$q^* = \arg\min_{q \in \mathcal{Q}}\,\text{KL}(q(\theta)\|p(\theta|\mathcal{D}))$$

**Problem**: the KL depends on $p(\theta|\mathcal{D})$, which is intractable. Substitute Bayes' rule to get the ELBO decomposition:
$$\log p(\mathcal{D}) = \underbrace{\mathbb{E}_q[\log p(\mathcal{D}|\theta)] - \text{KL}(q(\theta)\|p(\theta))}_{\mathcal{L}(q)\ \text{(ELBO)}} + \text{KL}(q\|p(\theta|\mathcal{D}))$$

Since $\log p(\mathcal{D})$ is constant w.r.t. $q$:
$$\arg\max_q \mathcal{L}(q) \Longleftrightarrow \arg\min_q \text{KL}(q\|p(\theta|\mathcal{D}))$$

**VI in practice**: maximise the ELBO $\mathcal{L}(q)$, which only depends on the likelihood, prior, and $q$ (all tractable).

## Key derivation
Full ELBO derivation: [[supp-elbo]].

The ELBO can be interpreted as:
$$\mathcal{L}(q) = \underbrace{\mathbb{E}_q[\log p(\mathcal{D}|\theta)]}_{\text{data fit}} - \underbrace{\text{KL}(q(\theta)\|p(\theta))}_{\text{complexity penalty}}$$

⚠️ *ELBO derivation examinable.*

## Parameters & intuition

### Why Reverse KL (Mode-Seeking)?
- Reverse KL: $\text{KL}(q\|p)$ is computed under $q$.
- $q$ avoids regions where $p$ is near zero (if $q(\theta) > 0$ but $p(\theta) \approx 0$, the log ratio explodes).
- Result: $q$ "seeks" one mode of $p$. May underestimate posterior uncertainty/spread.
- Forward KL $\text{KL}(p\|q)$: mass-covering; $q$ must cover all of $p$. Impractical (requires evaluating $p$, which is intractable).

### Mean-Field VI
- Assume factorised $q(\theta) = \prod_k q_k(\theta_k)$.
- Update rule for each factor: $q_k^*(\theta_k) \propto \exp(\mathbb{E}_{q_{-k}}[\log p(\mathcal{D}, \theta)])$.
- Block coordinate ascent: update one factor at a time.
- Closed-form updates exist in conjugate models.

### Parametric VI
- Fix form: $q(\theta|\lambda)$ (e.g. $\mathcal{N}(\mu, \Sigma)$).
- Maximise ELBO over variational parameters $\lambda$ using gradient ascent.
- Diagonal Gaussian: $q(\theta|\lambda) = \mathcal{N}(\mu, \text{diag}(\sigma^2))$ — fast, scalable.

## Worked example sketch
*Bayesian linear regression*: Gaussian prior on $\mathbf{w}$, Gaussian likelihood → exact posterior (conjugate). VI would reproduce it exactly (in the mean-field Gaussian family). This shows VI can be exact when the posterior matches the variational family.

## Connections
- VI extends [[laplace-approximation]] from local to global (but still biased — the approximating family may not contain the true posterior).
- [[elbo]] is the VI objective; derived from [[kl-divergence]].
- [[variational-autoencoder]]: VI applied to a deep latent variable model; same ELBO.
- Compare with [[mcmc]]: MCMC is asymptotically exact but slow; VI is fast but approximate.

## Exam notes
- "ELBO derivation": ⚠️ **examinable** (only this derivation from Week 4).
- "Differences between Laplace, VI, MCMC": ⚠️ **past exam question**.
- Mean-field update rule: conceptual understanding.
- Mode-seeking behaviour of reverse KL: **conceptual** exam question.
- No formulas given for Week 4. ⚠️
- Formula status: ELBO formula must be known from memory ⚠️
