# Supp — ELBO Derivation in Variational Inference

**File:** `raw/text/COM3031_W4_ELBO.txt`
**Type:** supplementary-note
**Week:** 4
**Concepts introduced:** [[elbo]], [[variational-inference]], [[kl-divergence]]

## Summary
Formally derives the Evidence Lower Bound (ELBO) from the KL divergence. Shows step-by-step that minimising KL$(q\|p(\theta|\mathcal{D}))$ is equivalent to maximising the ELBO, and that the ELBO is always a lower bound on the log evidence. Also presents the ELBO in the "expected likelihood − KL to prior" form.

## Key content

### Setup
- Joint model: $p(\mathcal{D}, \theta) = p(\mathcal{D}|\theta)p(\theta)$.
- Posterior: $p(\theta|\mathcal{D}) = p(\mathcal{D},\theta)/p(\mathcal{D})$.
- Goal: approximate $p(\theta|\mathcal{D})$ with tractable $q(\theta)$ by minimising $\text{KL}(q\|p(\theta|\mathcal{D}))$.

### Derivation
Start from the KL definition:
$$\text{KL}(q\|p(\theta|\mathcal{D})) = \mathbb{E}_q\!\left[\log\frac{q(\theta)}{p(\theta|\mathcal{D})}\right]$$
Substitute Bayes' rule $p(\theta|\mathcal{D}) = p(\mathcal{D},\theta)/p(\mathcal{D})$:
$$= \mathbb{E}_q[\log q(\theta) + \log p(\mathcal{D}) - \log p(\mathcal{D},\theta)]$$
$$= \log p(\mathcal{D}) + \mathbb{E}_q[\log q(\theta)] - \mathbb{E}_q[\log p(\mathcal{D},\theta)]$$

Rearranging to isolate $\log p(\mathcal{D})$:
$$\log p(\mathcal{D}) = \underbrace{\mathbb{E}_q[\log p(\mathcal{D},\theta)] - \mathbb{E}_q[\log q(\theta)]}_{\mathcal{L}(q)\ \text{(ELBO)}} + \text{KL}(q\|p(\theta|\mathcal{D}))$$

### Lower Bound Property
Since $\text{KL} \geq 0$:
$$\mathcal{L}(q) \leq \log p(\mathcal{D})$$
Equality holds iff $q(\theta) = p(\theta|\mathcal{D})$.

### Equivalence of Objectives
$\log p(\mathcal{D})$ is constant w.r.t. $q$, so:
$$\arg\max_q \mathcal{L}(q) \Longleftrightarrow \arg\min_q \text{KL}(q\|p(\theta|\mathcal{D}))$$

### Alternative Form (Data fit − Complexity)
Using $p(\mathcal{D},\theta) = p(\mathcal{D}|\theta)p(\theta)$:
$$\mathcal{L}(q) = \mathbb{E}_q[\log p(\mathcal{D}|\theta)] + \mathbb{E}_q[\log p(\theta)] - \mathbb{E}_q[\log q(\theta)]$$
$$= \mathbb{E}_q[\log p(\mathcal{D}|\theta)] - \text{KL}(q(\theta)\|p(\theta))$$
- Term 1: **expected log-likelihood** (data fit).
- Term 2: **KL to prior** (complexity penalty — penalises $q$ that deviates from the prior).

## Exam notes
- ELBO derivation is the **only** Week 4 derivation that is examinable. ⚠️
- Must be able to derive from KL definition to the log-evidence decomposition.
- Key result: $\log p(\mathcal{D}) = \mathcal{L}(q) + \text{KL}(q\|p(\theta|\mathcal{D}))$.
- No formulas given for Week 4.

## Links to concepts
- [[elbo]]: defined and derived here
- [[variational-inference]]: context
- [[kl-divergence]]: used throughout
- [[bayesian-inference]]: ELBO is a lower bound on the log marginal likelihood
