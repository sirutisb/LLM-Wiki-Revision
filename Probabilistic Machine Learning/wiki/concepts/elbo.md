# Evidence Lower Bound (ELBO)

**Type:** principle
**Week:** 4
**Related:** [[variational-inference]], [[kl-divergence]], [[bayesian-inference]], [[variational-autoencoder]]
**Source:** [[lecture-w4]], [[supp-elbo]]

## Definition
The Evidence Lower Bound (ELBO) is a computable lower bound on the log marginal likelihood (log evidence) $\log p(\mathcal{D})$, used as the variational inference objective.

## Motivation
In variational inference, we want to minimise $\text{KL}(q\|p(\theta|\mathcal{D}))$, but this requires the intractable posterior $p(\theta|\mathcal{D})$. The ELBO is derived by rearranging the KL identity so that all terms are tractable (depend only on $q$, the likelihood, and the prior).

## How it works

**Full derivation** (from [[supp-elbo]]):
$$\text{KL}(q\|p(\theta|\mathcal{D})) = \log p(\mathcal{D}) - \mathcal{L}(q)$$

where the ELBO is:
$$\mathcal{L}(q) = \mathbb{E}_q[\log p(\mathcal{D},\theta)] - \mathbb{E}_q[\log q(\theta)] = \mathbb{E}_q\!\left[\log\frac{p(\mathcal{D},\theta)}{q(\theta)}\right]$$

**Lower bound property**: since $\text{KL} \geq 0$:
$$\mathcal{L}(q) \leq \log p(\mathcal{D})$$
with equality iff $q(\theta) = p(\theta|\mathcal{D})$.

**Equivalent forms**:
$$\mathcal{L}(q) = \mathbb{E}_q[\log p(\mathcal{D}|\theta)] - \text{KL}(q(\theta)\|p(\theta))$$
- **Term 1**: expected log-likelihood (data fit; higher is better).
- **Term 2**: KL divergence from $q$ to the prior (complexity penalty; lower is better — don't deviate too far from the prior).

**Key consequence**: maximising ELBO ≡ minimising $\text{KL}(q\|p(\theta|\mathcal{D}))$.

## Key derivation
$$\text{KL}(q\|p(\theta|\mathcal{D})) = \mathbb{E}_q\!\left[\log\frac{q(\theta)}{p(\theta|\mathcal{D})}\right] = \mathbb{E}_q[\log q(\theta)] - \mathbb{E}_q[\log p(\mathcal{D},\theta)] + \log p(\mathcal{D})$$
Rearranging:
$$\log p(\mathcal{D}) = \mathcal{L}(q) + \text{KL}(q\|p(\theta|\mathcal{D}))$$
Since $\text{KL} \geq 0$ and $\log p(\mathcal{D})$ is constant w.r.t. $q$:
$$\max_q \mathcal{L}(q) \Leftrightarrow \min_q \text{KL}(q\|p(\theta|\mathcal{D}))$$

⚠️ *This derivation is examinable.*

## Parameters & intuition
- ELBO is a **lower bound** on the log evidence — maximising it tightens the bound.
- The gap $\log p(\mathcal{D}) - \mathcal{L}(q)$ equals the KL divergence from $q$ to the true posterior.
- When $q$ perfectly matches the posterior: ELBO = log evidence (gap = 0).
- In practice: ELBO is the objective function in VI; we maximise it w.r.t. variational parameters.

## Worked example sketch
*In the VAE (Week 8 per exam)*: ELBO = reconstruction loss − KL$(q_\phi(z|x)\|p(z))$. Maximising the ELBO trains both encoder and decoder jointly.

## Connections
- Derived from [[kl-divergence]]: ELBO makes the intractable KL tractable.
- Used in [[variational-inference]] as the optimisation objective.
- The same ELBO structure appears in [[variational-autoencoder]].
- In [[bayesian-model-comparison]], Laplace approximation approximates log$\,p(\mathcal{D}|\mathcal{M}) \approx$ ELBO at MAP.

## Exam notes
- ELBO derivation: ⚠️ **the only examinable derivation from Week 4**.
- Must be able to go from KL definition → log$\,p(\mathcal{D})$ decomposition → ELBO.
- Two forms of ELBO must be known: $\mathbb{E}_q[\log p(\mathcal{D},\theta)] - \mathbb{E}_q[\log q(\theta)]$ and $\mathbb{E}_q[\log p(\mathcal{D}|\theta)] - \text{KL}(q\|p(\theta))$.
- No formulas given. ⚠️
- Formula status: must derive from scratch ⚠️
