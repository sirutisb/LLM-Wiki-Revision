# Week 4 — Variational Inference & ELBO

**File:** `raw/text/COM3031_2526_Week4.txt`
**Type:** lecture
**Week:** 4
**Concepts introduced:** [[variational-inference]], [[kl-divergence]], [[elbo]], [[mean-field-vi]]

## Summary
Week 4 introduces variational inference (VI) as a global, optimisation-based alternative to the local Laplace approximation. The key idea: replace intractable posterior $p(\theta|\mathcal{D})$ with a tractable approximating distribution $q(\theta)$ by minimising KL divergence. The KL divergence (properties, forward vs reverse) is studied in detail. Because direct KL minimisation is still intractable (depends on the unknown posterior), we derive the ELBO — a computable surrogate. Maximising the ELBO is equivalent to minimising KL. Mean-field and parametric VI are introduced as practical strategies.

## Key content

### Limitations of Laplace Approximation
- Local only: captures one peak; fails for multimodal or skewed posteriors.
- Assumes near-Gaussian shape; forces symmetry.

### Variational Inference Framework
$$q^* = \arg\min_{q \in \mathcal{Q}}\,\text{KL}(q(\theta)\|p(\theta|\mathcal{D}))$$
- Choose $q$ from a family $\mathcal{Q}$ (e.g. Gaussians, factorised distributions).
- VI is **global**: $q$ is fitted across the whole posterior, not just near one mode.

### KL Divergence
$$\text{KL}(q\|p) = \int q(\theta)\log\frac{q(\theta)}{p(\theta)}\,d\theta = \mathbb{E}_q[\log q(\theta) - \log p(\theta)]$$
- Non-negative: $\text{KL}(q\|p) \geq 0$, with equality iff $q = p$.
- Asymmetric: $\text{KL}(q\|p) \neq \text{KL}(p\|q)$.
- **Reverse KL** $\text{KL}(q\|p)$: zero-forcing / mode-seeking. $q$ avoids regions where $p$ is small → underestimates uncertainty; used in VI.
- **Forward KL** $\text{KL}(p\|q)$: zero-avoiding / mass-covering. $q$ must cover all of $p$ → overestimates uncertainty; impractical (needs $p$).

### ELBO Derivation
From Bayes' rule, $p(\theta|\mathcal{D}) = \frac{p(\mathcal{D}|\theta)p(\theta)}{p(\mathcal{D})}$. Substitute into KL:
$$\text{KL}(q\|p(\theta|\mathcal{D})) = \mathbb{E}_q[\log q(\theta)] - \mathbb{E}_q[\log p(\mathcal{D}|\theta)] - \mathbb{E}_q[\log p(\theta)] + \log p(\mathcal{D})$$
Rearranging:
$$\log p(\mathcal{D}) = \underbrace{\mathbb{E}_q[\log p(\mathcal{D}|\theta)] - \text{KL}(q(\theta)\|p(\theta))}_{\mathcal{L}(q)\;\text{ELBO}} + \text{KL}(q\|p(\theta|\mathcal{D}))$$
Since $\text{KL} \geq 0$: $\mathcal{L}(q) \leq \log p(\mathcal{D})$ — hence *lower bound* on the log evidence.

**Key result**: $\arg\max_q \mathcal{L}(q) \Leftrightarrow \arg\min_q \text{KL}(q\|p(\theta|\mathcal{D}))$.

### ELBO Interpretation
$$\mathcal{L}(q) = \underbrace{\mathbb{E}_q[\log p(\mathcal{D}|\theta)]}_{\text{expected log-likelihood (data fit)}} - \underbrace{\text{KL}(q(\theta)\|p(\theta))}_{\text{complexity penalty (prior regularisation)}}$$

### Mean-Field Variational Inference
- Assume $q(\theta) = \prod_{k=1}^K q_k(\theta_k)$ (fully factorised, independent factors).
- Optimal factor update (with all other factors fixed):
$$\log q_k^*(\theta_k) = \mathbb{E}_{q_{-k}}[\log p(\mathcal{D}, \theta)] + \text{const}$$
$$q_k^*(\theta_k) \propto \exp\!\left(\mathbb{E}_{q_{-k}}[\log p(\mathcal{D}, \theta)]\right)$$
- **Block coordinate ascent**: update each factor in turn until ELBO converges.
- Closed-form updates exist in conjugate/exponential-family models.

### Parametric Variational Inference
- Fix a parametric family (e.g. $q(\theta|\lambda) = \mathcal{N}(\theta|\mu,\Sigma)$, $\lambda = (\mu,\Sigma)$).
- Maximise ELBO over variational parameters $\lambda$ using gradient ascent.
- Diagonal Gaussian: $q(\theta|\lambda) = \mathcal{N}(\theta|\mu, \text{diag}(\sigma^2))$ — fewer parameters, common in deep learning.

## Key takeaways
- VI turns intractable Bayesian inference into a tractable optimisation problem.
- ELBO is the objective: maximise it ≡ minimise KL to the true posterior.
- ELBO = expected log-likelihood − KL to prior (data fit vs complexity).
- Reverse KL is mode-seeking; this explains why VI can underestimate posterior uncertainty.
- Mean-field assumes independence; parametric VI fixes a form and optimises parameters.
- Only ELBO-related derivations are examinable.

## Exam relevance
- ELBO derivation: **examinable** (from KL → log p(D) decomposition).
- "Maximising ELBO ≡ minimising KL": **examinable**.
- Mean-field update rule: conceptual understanding.
- No formulas given for Week 4.
- Past exam: deriving/explaining the ELBO.

## Links to concepts
- [[variational-inference]]: core topic of this week
- [[kl-divergence]]: central tool
- [[elbo]]: derived here
- [[mean-field-vi]]: introduced here
- [[laplace-approximation]]: previous approach ([[lecture-w3]])
- [[mcmc]]: next approach ([[lecture-w5]])
