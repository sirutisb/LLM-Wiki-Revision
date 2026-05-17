# Week 3 — Laplace Approximation: Past Paper Questions

**Source papers:** COM3023 May 2022, 2023, 2024
**Topic coverage:** Laplace approximation main use and limitations; mean & variance of approximated posteriors via Taylor expansion around the mode; numerical evaluation of MAP + curvature
**Formula sheet:** ⚠️ None provided — derivation steps (find mode, second derivative, Gaussian fit) must be recalled from memory

---

## COM3023 May 2022 — Question 2 (selected parts — 11 marks)

### Part (a) — 4 marks
What is the main use of the Laplace approximation in Bayesian statistics? State one limitation of using the Laplace approximation.

### Part (b) — 7 marks
The distribution of a random variable $\theta$ is given by:
$$p(\theta \mid y) = \theta^y (1 - \theta)^{n - y}.$$
Estimate the mean and variance using the Laplace approximation. Show your approach in estimating the mean and variance.

> *Note: Q2(c) and Q2(d) from this paper (KL divergence + entropy comparison) sit under Week 6 — see `week6-past-paper-questions.md`.*

---

## COM3023 May 2023 — Question 2(d) (10 marks)

### Q2(d) — 10 marks
The conditional distribution of a variable $y$ is given as:
$$p(y \mid \lambda) \propto \exp(-\lambda)\, \lambda^y,$$
and the prior distribution for $\lambda$ is
$$p(\lambda) = \frac{1}{\lambda}.$$
Find the mean and variance of the posterior $p(\lambda \mid y)$ using the Laplace approximation.

---

## COM3023 May 2024 — Question 2(c) (9 marks)

### Q2(c) — 9 marks
The distribution of a random variable $\theta$ is given by:
$$p(\theta \mid m, n, j) = \theta^{m+1} (\theta + 1 + n)^j,$$
where $m, n, j$ are constants. Find the Laplace approximation of the distribution shown above for $m = 4$, $n = 6$, $j = 20$. Give your answers up to two decimal places.

---

## Pattern Analysis

| Paper | Marks in Week 3 | Conceptual | Numerical / derivation |
|-------|------------------|------------|------------------------|
| 2022 (Q2 a–b) | 11 | Laplace use + one limitation | Mean & variance of $\theta^y(1-\theta)^{n-y}$ via Laplace |
| 2023 (Q2d) | 10 | — | Mean & variance of posterior with Poisson-like likelihood + improper prior $1/\lambda$ |
| 2024 (Q2c) | 9 | — | Laplace approx with concrete $m=4, n=6, j=20$, to two decimal places |

**Consistent exam pattern:**
- Every paper includes a **numerical Laplace approximation** worth 7–10 marks where you must:
  1. Take $\log p(\theta)$ (or $\log p(\theta \mid y)$)
  2. Differentiate w.r.t. the parameter; set to zero → find the **mode** $\theta_*$ (this is the approximated **mean**)
  3. Take the **second derivative**; evaluate at $\theta_*$; the negative of this is the **precision**
  4. Approximated **variance** $= -1 \,/\, \frac{d^2 \log p}{d\theta^2}\Big|_{\theta_*}$
- 2022 also asks a 4-mark conceptual on the use/limitation
- 2024 explicitly asks for two-decimal-place numerical answers — be ready to compute

**Must know from memory (no formula sheet):**
- Laplace approximation: $p(\theta \mid y) \approx \mathcal{N}(\theta_*, \, A^{-1})$ where $\theta_* = \arg\max \log p(\theta \mid y)$ and $A = -\frac{d^2 \log p(\theta \mid y)}{d\theta^2}\Big|_{\theta_*}$
- **Use:** approximate intractable posteriors with a Gaussian centred at the MAP; gives a closed-form approximation of the marginal likelihood (basis for BIC)
- **Limitations:** assumes the posterior is **unimodal** and well-approximated by a Gaussian near its mode; fails for skewed, multimodal, or heavy-tailed posteriors; quality degrades for low-dimensional / high-curvature regions
- Multivariate version (not examinable here): replace second derivative with the Hessian; covariance $= H^{-1}$
- The mode is invariant to the normalising constant — so you can work with $\log p(\theta) + \log p(y \mid \theta)$ (unnormalised)
