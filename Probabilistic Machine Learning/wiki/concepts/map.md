# Maximum A Posteriori Estimation (MAP)

**Type:** algorithm
**Week:** 1
**Related:** [[mle]], [[bayesian-inference]], [[conjugate-priors]], [[laplace-approximation]]
**Source:** [[lecture-w1]], [[supp-map-gaussian]], [[supp-beta-binomial]]

## Definition
MAP finds the mode of the posterior distribution — the single parameter value that maximises $p(\theta|\mathcal{D})$.

## Motivation
MLE ignores prior knowledge and can overfit with limited data. MAP incorporates a prior as a regulariser while remaining computationally cheap (just optimisation, no integration). It is the bridge between MLE and full Bayesian inference.

## How it works
$$\hat{\theta}_{\text{MAP}} = \arg\max_\theta p(\theta|\mathcal{D}) = \arg\max_\theta [p(\mathcal{D}|\theta)\,p(\theta)]$$

Taking logs (monotone transformation, same argmax):
$$\hat{\theta}_{\text{MAP}} = \arg\max_\theta [\log p(\mathcal{D}|\theta) + \log p(\theta)]$$

Note: $p(\mathcal{D})$ does not depend on $\theta$ so it can be dropped.

## Key derivation

**Gaussian likelihood, Gaussian prior** (derivation: [[supp-map-gaussian]]):
$$\hat{\mu}_{\text{MAP}} = \frac{n\sigma_0^2}{n\sigma_0^2 + \sigma^2}\bar{y} + \frac{\sigma^2}{n\sigma_0^2 + \sigma^2}\mu_0$$
- Weighted average of sample mean $\bar{y}$ and prior mean $\mu_0$.
- Weights depend on data variance $\sigma^2$ and prior variance $\sigma_0^2$.

**Binomial likelihood, Beta prior** → MAP is the mode of the Beta posterior:
$$\hat{\theta}_{\text{MAP}} = \frac{\alpha + y - 1}{\alpha + \beta + n - 2}$$
(different from the posterior mean; MAP uses the mode of Beta$(\alpha', \beta')$).

✅ *Formula sheet provided.* Univariate MAP derivation examinable; multivariate NOT.

## Parameters & intuition
- **No data** ($n=0$): MAP = prior mode.
- **Infinite data** ($n \to \infty$): MAP → MLE (prior negligible).
- **Strong prior** (small $\sigma_0^2$): MAP strongly pulled toward $\mu_0$.
- **Weak prior** (large $\sigma_0^2$): MAP ≈ MLE.

### MAP as Regularisation
With a Gaussian prior $p(\mathbf{w}) = \mathcal{N}(0, \frac{1}{\lambda}I)$:
$$\hat{\mathbf{w}}_{\text{MAP}} = \arg\min_\mathbf{w} \left[\sum_i (y_i - \mathbf{w}^\top\mathbf{x}_i)^2 + \lambda\|\mathbf{w}\|^2\right]$$
MAP with Gaussian prior ≡ L2-regularised (ridge) regression. The prior variance controls the regularisation strength.

## Worked example sketch
*Past exam (Poisson-Gamma):* $\lambda \sim \text{Gamma}(25, 3)$, observe $y=10$ ($n=1$). Posterior: Gamma$(35, 4)$. Posterior mean $= 35/4 = 8.75$. (MAP would be the mode = $(35-1)/4 = 8.5$.)

## Connections
- MAP is a **point estimate** of the posterior mode — not the full posterior.
- The unnormalised posterior $p(\mathcal{D}|\theta)p(\theta)$ is NOT normalised; MAP extracts only the mode.
- Laplace approximation ([[laplace-approximation]]) builds on MAP: fits a Gaussian centred at the MAP with curvature-derived variance.
- Full Bayesian inference ([[bayesian-inference]]) uses the entire posterior, not just the mode.

## Exam notes
- MAP derivation (Gaussian–Gaussian): examinable.
- Conjugate posterior MAP: examinable.
- **Key formula**: $\hat{\theta}_{\text{MAP}} = \arg\max[\log p(\mathcal{D}|\theta) + \log p(\theta)]$ must be known.
- **Common pitfall**: MAP is not a probability distribution. The product $p(\mathcal{D}|\theta)p(\theta)$ cannot be used for probabilistic statements directly (it's unnormalised).
- Formula status: ✅ Formula sheet provided.
