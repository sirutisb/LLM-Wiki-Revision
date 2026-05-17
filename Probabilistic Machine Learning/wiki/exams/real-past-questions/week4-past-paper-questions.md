# Week 4 — Variational Approximation / ELBO: Past Paper Questions

**Source papers:** COM3023 May 2024, 2025
**Topic coverage:** comparison of Laplace / variational / MCMC; reverse vs forward KL; optimisation methods for VI; full ELBO derivation from $\log p(x)$; ELBO ⇔ KL equivalence; ELBO decomposition into data term + regulariser
**Formula sheet:** ⚠️ None provided — ELBO derivation must be reproduced from memory

---

## COM3023 May 2024 — Question 2(b) and Question 3(a) (10 marks)

### Q2(b) — 5 marks
Explain the key differences between Laplace approximation, variational approximation and Markov Chain Monte Carlo approximation.

### Q3(a) — 5 marks
What is the difference between reverse and forward Kullback–Leibler divergence? State two methods to perform optimisation for variational approximation.

> *Note: this paper has no further variational-specific numerical question; Q3(b) (max-entropy distribution) sits under Week 6.*

---

## COM3023 May 2025 — Question 3(a) (13 marks)

Consider a Bayesian model with a posterior distribution $p(\theta \mid x)$ that is intractable to compute directly. To approximate the posterior, we use a variational distribution $q(\theta)$ and the Evidence Lower Bound (ELBO) as the objective function.

### Q3(a)(i) — 7 marks
Derive the ELBO starting from the marginal log-likelihood $\log p(x)$, and show how it relates to the KL divergence $\mathrm{KL}(q(\theta) \,\|\, p(\theta \mid x))$.

### Q3(a)(ii) — 2 marks
Explain why maximizing the ELBO is equivalent to minimizing the KL divergence between $q(\theta)$ and $p(\theta \mid x)$.

### Q3(a)(iii) — 4 marks
The ELBO can be expressed as two components: the data term and the regulariser. Write the ELBO in this form and explain the significance of each term in variational inference.

> *Note: Q3(b) (rejection sampling) is out-of-scope for the new module.*

---

## Pattern Analysis

| Paper | Marks in Week 4 | Conceptual | Derivation |
|-------|------------------|------------|------------|
| 2024 (Q2b, Q3a) | 10 | Compare Laplace / VI / MCMC; forward vs reverse KL; two optimisation methods | — |
| 2025 (Q3a i–iii) | 13 | ELBO ↔ KL equivalence; data term vs regulariser interpretation | Full ELBO derivation from $\log p(x)$ |

**Consistent exam pattern:**
1. A comparison question (~5 marks) — either between approximation methods or between forward vs reverse KL
2. A full ELBO derivation question (~7 marks) — the only Week 4 derivation explicitly listed as examinable
3. A short follow-up (~2–4 marks) interpreting the ELBO (data + regulariser form) or its relation to KL

**Must know from memory (no formula sheet):**
- **ELBO derivation:**
$$\log p(x) = \log \int p(x, \theta)\, d\theta = \log \int q(\theta) \frac{p(x, \theta)}{q(\theta)} d\theta \ge \mathbb{E}_{q}\left[\log \frac{p(x, \theta)}{q(\theta)}\right] = \mathrm{ELBO}(q)$$
  (Jensen's inequality on $\log$)
- **Equivalent identity:** $\log p(x) = \mathrm{ELBO}(q) + \mathrm{KL}(q(\theta) \,\|\, p(\theta \mid x))$. Since $\log p(x)$ is fixed and $\mathrm{KL} \ge 0$, maximising ELBO ≡ minimising KL.
- **Two-term form:** $\mathrm{ELBO}(q) = \underbrace{\mathbb{E}_{q}[\log p(x \mid \theta)]}_{\text{data term (expected log-likelihood)}} - \underbrace{\mathrm{KL}(q(\theta) \,\|\, p(\theta))}_{\text{regulariser (prior-matching)}}$
- **Reverse KL** $\mathrm{KL}(q \,\|\, p)$ — used in standard VI; **zero-forcing / mode-seeking** (q underestimates p's support). **Forward KL** $\mathrm{KL}(p \,\|\, q)$ — **moment-matching / mean-seeking** (q covers all of p's mass).
- **VI optimisation methods:** coordinate-ascent VI (CAVI), stochastic VI (SVI), gradient-based VI (e.g. reparameterisation trick / black-box VI)
- **Laplace vs VI vs MCMC:** Laplace = local Gaussian fit at MAP, fast but unimodal & analytic-derivative needed; VI = optimisation, deterministic, biased but scalable; MCMC = sampling, asymptotically exact but slow/diagnostics-heavy
