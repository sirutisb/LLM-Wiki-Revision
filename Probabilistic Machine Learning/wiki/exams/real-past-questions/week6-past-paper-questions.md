# Week 6 — Information Theory: Past Paper Questions

**Source papers:** COM3023 May 2022, 2024, 2025
**Topic coverage:** Kullback–Leibler divergence interpretation; entropy comparison of Gaussians; maximum-entropy distribution on a discrete set via Lagrange multipliers; differential entropy of a Gaussian; entropy as uncertainty quantification
**Formula sheet:** ✅ Information-theory formulas will be provided in the exam (but derivation-style use of entropy formulas is still expected)

---

## COM3023 May 2022 — Question 2 (selected parts — 7 marks)

### Q2(c) — 3 marks
What is measured by the Kullback–Leibler divergence between two distributions?

### Q2(d) — 4 marks
For the two normal distributions shown in Figure 1, which distribution has the larger entropy and why?

*Figure 1 details: $p(x)$ on the left has mean $= 0$, $\sigma = 2.5$; $q(x)$ on the right has mean $= 0$, $\sigma = 0.5$.*

---

## COM3023 May 2024 — Question 3(b) (10 marks)

### Q3(b) — 10 marks
Show that the maximum entropy distribution over a finite (discrete) set $\{m, m+1, \dots, n-1, n\}$ with $m < n$ is a uniform distribution.

*Hint: use Lagrange multipliers.*

---

## COM3023 May 2025 — Question 2(c) (12 marks)

A sensor in a manufacturing plant measures the temperature of a reactor, modelled as a Gaussian random variable $T$ with mean $\mu = 100\,^{\circ}\mathrm{C}$ and variance $\sigma^2$. The following formulas and constraints are given to guide your derivation.

**Differential entropy:**
$$H[T] = -\int_{-\infty}^{\infty} p(t) \ln p(t)\, dt$$

**Gaussian distribution:**
$$p(t) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left(-\frac{(t-\mu)^2}{2\sigma^2}\right)$$

**Constraints:**
$$\int_{-\infty}^{\infty} p(t)\, dt = 1, \quad \int_{-\infty}^{\infty} (t-\mu)^2 p(t)\, dt = \sigma^2$$

### Q2(c)(i) — 9 marks
Derive the entropy $H[T]$ explicitly, and explain how $H[T]$ depends on $\sigma^2$.

### Q2(c)(ii) — 3 marks
Conclude the findings in part (i) by discussing its implications in the context of temperature measurement uncertainty.

---

## Pattern Analysis

| Paper | Marks in Week 6 | Conceptual | Derivation / numerical |
|-------|------------------|------------|------------------------|
| 2022 (Q2c, Q2d) | 7 | What KL measures; entropy ranking of two Gaussians by $\sigma$ | — |
| 2024 (Q3b) | 10 | — | Show uniform = max-entropy on a finite set (Lagrange multipliers) |
| 2025 (Q2c i–ii) | 12 | Implications of $H[T]$ for measurement uncertainty | Gaussian differential entropy derivation |

**Consistent exam pattern:**
- A **conceptual interpretation** question on KL or entropy (~3–4 marks)
- A **maximum-entropy derivation** (~9–10 marks) — either discrete (uniform) via Lagrange multipliers, or continuous (Gaussian) via the integral
- A short **implications** question (~3 marks) interpreting entropy as uncertainty

**Must know (formulas provided, but be ready to apply them):**
- KL divergence: $\mathrm{KL}(p \,\|\, q) = \int p(x) \log \frac{p(x)}{q(x)} dx$ — measures the **extra information cost** of using $q$ to encode samples actually drawn from $p$; $\ge 0$ with equality iff $p = q$; **asymmetric** ($\mathrm{KL}(p\|q) \ne \mathrm{KL}(q\|p)$)
- Shannon entropy (discrete): $H[X] = -\sum_x p(x) \log p(x)$
- Differential entropy (continuous): $H[X] = -\int p(x) \log p(x)\, dx$
- Gaussian differential entropy: $H[\mathcal{N}(\mu, \sigma^2)] = \frac{1}{2} \log(2\pi e \sigma^2)$ — **independent of $\mu$**, monotonically increasing in $\sigma^2$
- **Max-entropy under constraints** (Lagrange):
  - Only normalisation constraint, discrete finite set → **uniform**
  - Mean + variance constraint, continuous on $\mathbb{R}$ → **Gaussian**
  - Mean constraint, continuous on $[0, \infty)$ → **exponential**
- 2022 Q2(d): $p$ with $\sigma = 2.5$ has the larger entropy than $q$ with $\sigma = 0.5$, because Gaussian entropy grows with $\sigma$ — wider distribution ⇒ more uncertainty
- 2025 Q2(c) interpretation: larger $\sigma^2$ ⇒ higher entropy ⇒ greater uncertainty in temperature reading; reducing measurement noise lowers entropy and tightens the confidence about $T$
