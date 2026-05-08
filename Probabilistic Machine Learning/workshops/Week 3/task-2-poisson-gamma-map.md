# Task 2 — MAP for the Poisson Rate (Gamma prior, Prussian Horse-Kick Data)

**Source:** `3031_MAP_Workshop.pdf` Q2, `Solution Q2.ipynb`, `Prussian-Horse-Kick-Data_Workshop.csv`
**Concepts tested:** [[map]], [[mle]], [[bayesian-inference]], [[conjugate-priors]], [[mcmc]]
**Related:** [[beta-binomial-posterior]] (analogous conjugate story for binomial data)

---

## The question (paraphrased)

Von Bortkiewicz famously counted the number of Prussian cavalrymen killed by horse kicks each year, 1875–1894. The data file holds these counts. Each yearly count is modelled as Poisson:
$$
y_i \sim \text{Poisson}(\lambda), \quad \lambda > 0, \qquad
p(\mathbf{y} \mid \lambda) \propto \prod_{i=1}^n \lambda^{y_i} e^{-\lambda}.
$$

(a) Estimate $\lambda$ by MLE.

(b) Place a Gamma prior $\lambda \sim \text{Gamma}(\alpha, \beta)$ with $p(\lambda) \propto \lambda^{\alpha-1} e^{-\beta\lambda}$. Compute the posterior $p(\lambda \mid \mathbf{y})$ either analytically or by MCMC.

(c) Study how $\alpha$ and $\beta$ control the posterior. Use the Gamma facts $\mathbb{E}[\lambda] = \alpha/\beta$ and $\text{sd}(\lambda) = \sqrt{\alpha/\beta^2}$ to design informative vs vague priors and compare.

This is the second canonical conjugate pair students must know: **Gamma prior + Poisson likelihood $\Rightarrow$ Gamma posterior**. It mirrors the Beta–Binomial story in [[supp-beta-binomial]] / [[beta-binomial-posterior]].

---

## Why MAP rather than MLE?

The MLE here is just $\bar y$ (the sample mean of the counts). It has two limitations:

1. **It says nothing about uncertainty.** A point estimate of $0.7$ kicks/year tells us nothing about how confident we should be.
2. **It cannot incorporate prior knowledge.** Suppose we knew from other regiments that horse-kick deaths average about $0.5$ per year with little spread — MLE has no way to use this.

Under the [[bayesian-inference]] view, $\lambda$ is a random variable with a prior. The Gamma prior is chosen for two reasons:
- $\lambda > 0$ and the Gamma distribution lives on $(0,\infty)$ — no probability mass on impossible values.
- It is the **conjugate prior** for the Poisson rate, so the posterior is again Gamma and we get a clean analytical update.

---

## Cell-by-cell walkthrough

### Cells 1–2 — imports and load data

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
y = np.loadtxt('.../Prussian-Horse-Kick-Data_Workshop.csv')
```

The data is a 1D array of counts (mostly $0$s, some $1$s and $2$s). $n = 280$ observations. The mean is around $0.7$ — most years saw no deaths.

### Cell 3 — markdown of the log-likelihood

Starting from
$$
p(\mathbf{y} \mid \lambda) \propto \prod_{i=1}^n \lambda^{y_i} e^{-\lambda} = \lambda^{\sum_i y_i} e^{-n\lambda},
$$
take logs to get
$$
\log p(\mathbf{y} \mid \lambda) \propto \left(\sum_i y_i\right) \log \lambda - n\lambda.
$$
We optimise the log-likelihood (sums are friendlier than products and avoid numerical underflow).

### Cell 4 — likelihood function for SciPy

```python
def likelihood(theta, *args):
    n = len(y)
    L = np.sum(y) * np.log(theta) - theta * n
    return -L
```

`theta` plays the role of $\lambda$. We return the *negative* log-likelihood because `scipy.optimize.minimize` minimises by default — minimising $-\log L$ maximises $\log L$.

### Cell 5–6 — run optimiser

```python
results = minimize(likelihood, x0=[1], bounds=[(0.0001, 100)], args=(y,), method='L-BFGS-B')
print(results.x, results.fun)
# -> [0.70000005] 265.91
```

Bounds enforce $\lambda > 0$. The optimiser returns $\hat\lambda_{\text{MLE}} \approx 0.7$. That should equal $\bar y$ exactly: differentiating the log-likelihood and setting it to zero gives
$$
\frac{\sum_i y_i}{\lambda} - n = 0 \;\Rightarrow\; \hat\lambda_{\text{MLE}} = \bar y.
$$
We use the optimiser instead of writing $\bar y$ directly to demonstrate the general MLE recipe (set up $-\log L$, hand it to a minimiser).

### Cell 7 — MCMC posterior with PyMC

```python
basic_model = pm.Model()
with basic_model:
    lam = pm.Gamma('lambda', alpha=0.25, beta=0.5)             # Prior
    Y_obs = pm.distributions.discrete.Poisson('Y', mu=lam, observed=y)  # Likelihood
    trace = pm.sample(1000)
```

What this is doing:

1. Declares $\lambda \sim \text{Gamma}(\alpha=0.25, \beta=0.5)$. Prior mean $= 0.25/0.5 = 0.5$, prior std $= \sqrt{0.25/0.25} = 1$ — a fairly vague prior on a positive quantity.
2. Declares $y_i \sim \text{Poisson}(\lambda)$, clamped to the observed counts.
3. Asks NUTS (an MCMC algorithm — see [[mcmc]]) to draw 1000 samples from $p(\lambda \mid \mathbf{y})$.

`pm.plot_trace(trace)` shows the posterior density and the chain. With $n=280$ and a vague prior, posterior mean $\approx 0.7$ — almost identical to the MLE.

### Cell 8–9 — markdown: the analytical posterior

By conjugacy:
$$
p(\lambda \mid \mathbf{y}) \propto p(\mathbf{y} \mid \lambda)\, p(\lambda)
\propto \lambda^{\sum_i y_i} e^{-n\lambda} \cdot \lambda^{\alpha - 1} e^{-\beta\lambda}
= \lambda^{\alpha + \sum_i y_i - 1} e^{-(\beta + n)\lambda},
$$
which is the kernel of a Gamma distribution. Therefore
$$
\boxed{\;\lambda \mid \mathbf{y} \;\sim\; \text{Gamma}\!\left(\alpha + \sum_{i=1}^n y_i,\; \beta + n\right).\;}
$$

**Intuition for the update.**
- The shape parameter $\alpha$ acts like "pseudo-counts" of horse-kick events the prior carries; we *add* the actual observed total $\sum y_i$ to it.
- The rate parameter $\beta$ acts like "pseudo-years" of observation; we *add* the actual number of years $n$.

So the prior pretends we have already seen $\beta$ years that produced $\alpha$ events; observing real data just augments those pseudo-observations.

The posterior mode (MAP estimate) of a $\text{Gamma}(a, b)$ is $(a-1)/b$ for $a \geq 1$, so:
$$
\hat\lambda_{\text{MAP}} = \frac{\alpha + \sum_i y_i - 1}{\beta + n}.
$$
Compare with $\hat\lambda_{\text{MLE}} = \bar y = \sum_i y_i / n$. As $\alpha, \beta \to 0$ (an improper "Jeffreys-like" prior), MAP $\to$ MLE.

### Cell 10 — playing with prior parameters

The solution parametrises the prior via mean $m$ and "strength" $k$:
$$
\alpha = m \cdot k, \qquad \beta = k.
$$
Then prior mean $= \alpha/\beta = m$ and prior variance $= \alpha/\beta^2 = m/k$, so larger $k$ means a tighter (more informative) prior centred at $m$.

Three regimes:

| Setting | $m$ | $k$ | Prior strength | Posterior mean |
|---|---|---|---|---|
| Weak prior | $\bar y \approx 0.7$ | $1$ | Vague | Close to $0.7$ — data dominate |
| Strong & accurate | $\bar y \approx 0.7$ | $1000$ | Tight, correct | Stays near $0.7$, very narrow |
| Strong & wrong | $0.2$ | $1000$ | Tight, conflicting | Pulled toward $0.2$ even though data say $0.7$ |

The third row is the lesson: **a strong wrong prior biases the MAP estimate**. This is why prior choice matters and why "uninformative" priors are often a safe default when prior knowledge is weak.

```python
alpha_new = alpha + np.sum(y)
beta_new  = beta + n
mu_lambda    = alpha_new / beta_new
sigma_lambda = np.sqrt(alpha_new / beta_new**2)
```

These compute the posterior mean and std using the closed-form Gamma update. Plotting `stats.gamma.pdf(lam_samples, alpha_new, scale=1/beta_new)` then draws the analytical posterior.

> **SciPy parameterisation gotcha.** `scipy.stats.gamma` uses *shape* and *scale* (where scale $= 1/\beta$). The lecture uses shape and *rate* $\beta$. Hence `scale=1/beta_new` in the call. This trips people up in coursework.

---

## Effect of the prior — the conceptual punchline

- **Vague prior** ($k$ small): posterior $\approx$ likelihood. Bayesian and frequentist agree.
- **Informative & accurate prior**: posterior is sharper than likelihood — Bayesian wins on uncertainty quantification.
- **Informative but wrong prior**: posterior is biased away from the truth; you need lots of data to wash this out. Use only when prior knowledge is genuinely trustworthy.

In all three cases, as $n \to \infty$, the data overwhelm the prior and MAP $\to$ MLE.

---

## What to take away for the exam

- **Conjugate pair:** Gamma prior + Poisson likelihood $\Rightarrow$ Gamma posterior. Memorise the update rule:
  $$
  \alpha_{\text{post}} = \alpha + \sum_i y_i, \qquad \beta_{\text{post}} = \beta + n.
  $$
  This is a standard exam derivation in the same family as [[beta-binomial-posterior]].
- **Pseudo-count interpretation:** $\alpha$ acts like prior events, $\beta$ like prior observation time.
- **MAP estimator:** for $\text{Gamma}(a, b)$, mode $= (a-1)/b$ (for $a \ge 1$), giving
  $$
  \hat\lambda_{\text{MAP}} = \frac{\alpha + \sum_i y_i - 1}{\beta + n}.
  $$
- **MLE limit:** $\hat\lambda_{\text{MLE}} = \bar y$. MAP collapses to MLE as the prior becomes flat or as $n \to \infty$.
- **Prior parameterisation:** be able to convert between $(\alpha, \beta)$ and (mean, variance/std). Mean $= \alpha/\beta$, std $= \sqrt{\alpha/\beta^2}$. Examiners often specify a prior by its mean and strength rather than $(\alpha, \beta)$ directly.
- **Identify the kernel:** the trick of the derivation is recognising $\lambda^{a-1} e^{-b\lambda}$ as the Gamma kernel — practise spotting kernels for Beta, Gamma, and Gaussian, because this is the engine of every conjugate-prior derivation. See [[conjugate-priors]].
- **Be ready to discuss limits in words:** "What happens to the posterior as $\alpha, \beta \to 0$?" $\Rightarrow$ approaches an improper flat prior; MAP $\to$ MLE. "What happens as $n \to \infty$?" $\Rightarrow$ data dominate; MAP $\to$ MLE regardless of prior. These are favourite short-answer prompts.
