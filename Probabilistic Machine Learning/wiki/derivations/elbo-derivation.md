# Derivation: Evidence Lower Bound (ELBO)

**Used in:** [[elbo]], [[variational-inference]], [[variational-autoencoder]], [[kl-divergence]]
**Source:** [[supp-elbo]], [[lecture-w4]]
**Exam status:** ⚠️ Must know — ELBO derivation is core examinable material (no formula sheet)

## Setup
We have an intractable marginal likelihood (evidence):
$$\log p(\mathcal{D}) = \log \int p(\mathcal{D}|\boldsymbol{\theta})\,p(\boldsymbol{\theta})\,d\boldsymbol{\theta}$$

We introduce an approximate posterior $q(\boldsymbol{\theta})$ from a tractable family.

Goal: derive a lower bound on $\log p(\mathcal{D})$ that is tractable to compute and optimise.

## Steps

### Derivation 1: Via Jensen's Inequality

$$\log p(\mathcal{D}) = \log \int p(\mathcal{D}|\boldsymbol{\theta})p(\boldsymbol{\theta})\,d\boldsymbol{\theta}$$
$$= \log \int q(\boldsymbol{\theta})\frac{p(\mathcal{D}|\boldsymbol{\theta})p(\boldsymbol{\theta})}{q(\boldsymbol{\theta})}\,d\boldsymbol{\theta}$$
$$= \log \mathbb{E}_{q}\left[\frac{p(\mathcal{D}|\boldsymbol{\theta})p(\boldsymbol{\theta})}{q(\boldsymbol{\theta})}\right]$$
$$\geq \mathbb{E}_{q}\left[\log\frac{p(\mathcal{D}|\boldsymbol{\theta})p(\boldsymbol{\theta})}{q(\boldsymbol{\theta})}\right] \quad \text{(Jensen: log is concave)}$$
$$= \underbrace{\mathbb{E}_q[\log p(\mathcal{D}|\boldsymbol{\theta})]}_{\text{expected log-likelihood}} - \underbrace{D_{\text{KL}}(q(\boldsymbol{\theta})\|p(\boldsymbol{\theta}))}_{\text{KL from prior}}$$

$$\boxed{\mathcal{L}(q) = \mathbb{E}_q[\log p(\mathcal{D}|\boldsymbol{\theta})] - D_{\text{KL}}(q(\boldsymbol{\theta})\|p(\boldsymbol{\theta})) \leq \log p(\mathcal{D})}$$

### Derivation 2: Via KL Decomposition (exact identity)

Introduce $q(\boldsymbol{\theta})$ by multiplying and dividing:
$$\log p(\mathcal{D}) = \log p(\mathcal{D}) \int q(\boldsymbol{\theta})\,d\boldsymbol{\theta}$$
$$= \int q(\boldsymbol{\theta})\log p(\mathcal{D})\,d\boldsymbol{\theta}$$
$$= \int q(\boldsymbol{\theta})\log\frac{p(\mathcal{D},\boldsymbol{\theta})}{p(\boldsymbol{\theta}|\mathcal{D})}\,d\boldsymbol{\theta}$$
$$= \int q(\boldsymbol{\theta})\log\frac{p(\mathcal{D},\boldsymbol{\theta})}{q(\boldsymbol{\theta})}\,d\boldsymbol{\theta} + \int q(\boldsymbol{\theta})\log\frac{q(\boldsymbol{\theta})}{p(\boldsymbol{\theta}|\mathcal{D})}\,d\boldsymbol{\theta}$$
$$= \mathcal{L}(q) + D_{\text{KL}}(q\|p(\boldsymbol{\theta}|\mathcal{D}))$$

Since $D_{\text{KL}} \geq 0$:
$$\mathcal{L}(q) \leq \log p(\mathcal{D})$$

with equality iff $q(\boldsymbol{\theta}) = p(\boldsymbol{\theta}|\mathcal{D})$.

## Result

### ELBO (Form 1)
$$\mathcal{L}(q) = \mathbb{E}_q[\log p(\mathcal{D}|\boldsymbol{\theta})] - D_{\text{KL}}(q(\boldsymbol{\theta})\|p(\boldsymbol{\theta}))$$

### ELBO (Form 2, equivalent)
$$\mathcal{L}(q) = \mathbb{E}_q[\log p(\mathcal{D},\boldsymbol{\theta})] - \mathbb{E}_q[\log q(\boldsymbol{\theta})]$$

### Key Identity
$$\log p(\mathcal{D}) = \mathcal{L}(q) + D_{\text{KL}}(q(\boldsymbol{\theta})\|p(\boldsymbol{\theta}|\mathcal{D}))$$

## Intuition
- Maximising ELBO simultaneously:
  - Increases expected likelihood (data fit).
  - Decreases KL from prior (regularisation / keeps $q$ close to prior).
- Since $\log p(\mathcal{D}) = \text{ELBO} + \text{KL}$ and evidence is fixed, maximising ELBO ≡ minimising KL from posterior.
- The "gap" between ELBO and log evidence = $D_{\text{KL}}(q\|p(\boldsymbol{\theta}|\mathcal{D}))$ — how far $q$ is from the true posterior.
