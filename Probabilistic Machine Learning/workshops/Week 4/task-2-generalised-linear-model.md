# Task 2 — Generalised Linear Model: Logistic Regression for Rain Prediction

**Notebook:** `Q2_solution_Generalised_Linear_Model.ipynb`
**Data:** `rain_data.csv` — two columns `humidity, rain`. The header is commented out (`# humidity,rain`), so `np.loadtxt(..., skiprows=1)` skips it cleanly.
**Concept tested:** [[generalised-linear-models]] — specifically [[logistic-regression]], which is the GLM you get when the response is Bernoulli and the link function is the logit.

## The question (paraphrased from the workshop PDF)

We have $\{(x_i, y_i)\}$ with $y_i \in \{0,1\}$ (no rain / rain) and $x_i$ the humidity. The Bernoulli likelihood is

$$
p(y_i\mid p_i) = p_i^{y_i}(1-p_i)^{1-y_i},
$$

where $p_i = \mathbb{P}(\text{rain}\mid x_i)$. The five sub-parts are:

1. **What is the link function** $\eta_i$ that lets us relate $y_i$ and $x_i$ *linearly*?
2. **Express $p_i$ in terms of $\eta_i$.**
3. **Derive the log-likelihood.**
4. **Maximise it numerically** (find the MLE of the link-function parameters).
5. **Bayesian version:** put Normal priors on the parameters and run MCMC.

## Why we cannot just use linear regression

Look at the scatter of $(x, y)$: humidity on the x-axis, points stacked at $y=0$ and $y=1$. If we fit $y = b_0 + b_1 x$ via OLS we run into three problems:

1. **The output is unbounded.** A linear fit will give $\hat y < 0$ for low humidity and $\hat y > 1$ for high humidity. But $y$ is supposed to be a probability — it must live in $[0,1]$.
2. **The Gaussian noise model is wrong.** Residuals from a 0/1 response are not bell-shaped; they are bimodal, and their variance depends on $p_i$ (Bernoulli variance is $p_i(1-p_i)$, not constant).
3. **MLE under Gaussian noise minimises squared error**, but for Bernoulli data the MLE objective is the *cross-entropy* / log-likelihood, which weights mistakes very differently near $p=0$ or $p=1$.

A GLM solves all three at once: keep the linear predictor $\eta_i = b_0 + b_1 x_i$, but transform it through a **link function** so the result lives in the valid range, and use the *correct* likelihood (Bernoulli) to score it.

## Mathematical setup (sub-parts 1–3)

### Sub-part 1 — the link function

Probabilities live in $(0,1)$. The **logit** stretches that range out to all of $\mathbb{R}$, which is exactly the range a linear function $b_0 + b_1 x$ can produce:

$$
\eta_i = \operatorname{logit}(p_i) = \log\frac{p_i}{1-p_i}, \qquad \eta_i \in \mathbb{R}.
$$

So the linearity assumption — that $\eta$ is linear in $x$ — is

$$
\eta_i = b_0 + b_1 x_i.
$$

### Sub-part 2 — invert the link

The *inverse* of the logit is the **sigmoid** (logistic) function:

$$
p_i = \sigma(\eta_i) = \frac{1}{1+e^{-\eta_i}} = \frac{1}{1 + e^{-(b_0 + b_1 x_i)}}.
$$

This is what guarantees $p_i \in (0,1)$ for any real $\eta_i$. The bottom-of-notebook plots of sigmoid and logit make this concrete: sigmoid maps $\mathbb{R} \to (0,1)$, logit is its inverse.

### Sub-part 3 — the log-likelihood

Plug the Bernoulli pmf into a sum of logs (independent samples):

$$
\ell(b_0, b_1) = \sum_{i=1}^n \big[ y_i \log p_i + (1-y_i)\log(1-p_i) \big],
$$

with $p_i = \sigma(b_0 + b_1 x_i)$. This is the **negative cross-entropy** (see [[cross-entropy]]) — minimising negative log-likelihood is exactly minimising the binary cross-entropy loss familiar from neural networks. There is *no* closed-form solution for $\hat b_0, \hat b_1$ here (unlike linear regression), which is why the notebook turns to numerical optimisation.

## Cell-by-cell walkthrough

### Imports and data loading

```python
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
from scipy.optimize import minimize

data = np.loadtxt('rain_data.csv', delimiter=',', skiprows=1)
x = data[:, 0]   # humidity
y = data[:, 1]   # 0/1 rain indicator
plt.scatter(x, y)
```

The scatter is the diagnostic that *justifies* a GLM: y-values are stacked at 0 and 1, with rain becoming more common as humidity rises. A logistic fit should pass low for small $x$ and tend toward 1 for large $x$.

---

### Sub-part 4 — MLE via `scipy.optimize.minimize`

```python
def likelihood(theta, *args):
    b0, b1 = theta[0], theta[1]
    eta = b0 + b1 * x                  # linear predictor in R
    pi = 1 / (1 + np.exp(-eta))        # sigmoid -> probability in (0,1)
    return -np.sum(y*np.log(pi) + (1-y)*np.log(1-pi))   # negative log-lik
```

Three lines, three GLM concepts:

1. **`eta = b0 + b1*x`** — the linear predictor. Unbounded.
2. **`pi = 1/(1+exp(-eta))`** — the inverse link. Maps $\eta$ to a probability.
3. **`-np.sum(y*log(pi) + (1-y)*log(1-pi))`** — the Bernoulli negative log-likelihood.

```python
results = minimize(likelihood, [1, 1], method='BFGS')
b0_opt, b1_opt = results.x   # ≈ -2.44, 0.44
```

**Why BFGS?** The objective is smooth and unconstrained (the sigmoid handles the constraint $p \in (0,1)$ implicitly), so a quasi-Newton method without bounds is appropriate. BFGS approximates the Hessian from gradient information — this is essentially what `sklearn.linear_model.LogisticRegression(solver='lbfgs')` does internally.

The fitted values $\hat b_0 \approx -2.44, \hat b_1 \approx 0.44$ tell us:

- At $x=0$ humidity, $\eta = -2.44 \Rightarrow p \approx 0.08$ — low chance of rain.
- The 50% threshold is at $\eta = 0$, i.e. $x = -b_0/b_1 \approx 5.5$ — about midway through the humidity range.
- Each unit of humidity multiplies the *odds* of rain by $e^{0.44} \approx 1.55$ (this is what the slope means in log-odds units).

The two diagnostic plots that follow show:

- the fitted **probability curve** $\hat p(x) = \sigma(b_0 + b_1 x)$ overlaid on the (jittered) data — a clean S-curve;
- the **predicted probabilities** for each observed $x$, separated by true label — at high humidity the $y=1$ points have higher $\hat p$ than the $y=0$ points. The model is doing what we hoped.

---

### Sub-part 5 — Bayesian version with MCMC

```python
with pm.Model() as base_model:
    b0 = pm.Normal('b0', 0, sigma=4)
    b1 = pm.Normal('b1', 0, sigma=2)
    eta = b0 + b1 * x
    pi = 1 / (1 + np.exp(-eta))
    likelihood = pm.Bernoulli('y', p=pi, observed=y)
    trace = pm.sample(1000)
```

What changed from Q1's MCMC?

- The **likelihood node is `pm.Bernoulli`**, not `pm.Normal` — because the response is binary.
- The **link** $p_i = \sigma(\eta_i)$ is built explicitly inside the model graph; PyMC differentiates through it automatically.
- The **priors are independent Normals** on $b_0$ (sd 4) and $b_1$ (sd 2). These are weakly informative — they say "I expect coefficients of order 1, not 100", which keeps the sampler well-behaved without dominating the data.

Why is this not just MLE again? Because:

- We can read off **credible intervals** on $b_0$ and $b_1$ from the posterior — uncertainty quantification you do not get from `minimize`.
- We can **propagate uncertainty into predictions**: the posterior-predictive band in the final plot shows the 95% range for $p(\text{rain}\mid x)$ at every humidity level. The band is wider where data are sparse — exactly where you should be less confident — and narrower where data are dense.

Under the hood, PyMC again uses NUTS ([[mcmc]], [[metropolis-hastings]]). Note that there is *no closed-form posterior* for logistic regression — so unlike conjugate priors for Beta-Binomial or Normal-Normal, here MCMC (or [[laplace-approximation]], or [[variational-inference]]) is genuinely necessary.

---

## What to take away for the exam

1. **Three ingredients of a GLM** — memorise:
   - **Random component:** distribution of $y$ from the [exponential family](#) (Bernoulli here).
   - **Systematic component:** linear predictor $\eta = X\beta$.
   - **Link function:** invertible $g$ with $\eta = g(\mathbb{E}[y])$. For Bernoulli, $g$ is the logit.
2. **Why a link is needed:** the response's mean has a constrained range (e.g. $p\in(0,1)$) but a linear predictor is unbounded. The link bridges them. ⚠️ *Not on the formula sheet — be ready to write down the logit and sigmoid from memory.*
3. **The Bernoulli log-likelihood**
   $$\ell(\beta) = \sum_i y_i\log p_i + (1-y_i)\log(1-p_i),\quad p_i = \sigma(x_i^\top\beta)$$
   is the **binary cross-entropy** up to a sign. This identity is examinable in both the GLM topic and the [[cross-entropy]] topic.
4. **No closed form** for the logistic MLE — must be solved iteratively (Newton/IRLS, BFGS). Contrast with linear regression, which has $\hat\beta = (X^\top X)^{-1}X^\top y$.
5. **MLE = MAP with a flat prior**, and as the prior becomes wider, the **MCMC posterior mean → MLE**. Q2 demonstrates this: $b_0 \approx -2.4$ and $b_1 \approx 0.44$ from MLE, and the same values appear at the mean of the posteriors in part 5.
6. **Logit slope interpretation:** $b_1$ is a log-odds-ratio; $e^{b_1}$ is the multiplicative effect on the *odds* of $y=1$ for a one-unit increase in $x$. Examiners love this.
7. **Why the workshop puts MLE *and* MCMC side-by-side:** to show that the *model* (Bernoulli + logit link + linear predictor) is the same regardless of inference method. MLE gives a point estimate; MCMC gives a posterior. Choosing between them depends on whether you need uncertainty quantification.

## Connections

- Builds on: [[generalised-linear-models]], [[logistic-regression]], [[mle]].
- Shares inference machinery with Q1: [[mcmc]], [[metropolis-hastings]].
- Contrast with linear regression in `task-1-linear-regression.md` — same template (linear predictor + likelihood + optional Bayesian wrapper), but the link function and the likelihood family change.
- Compare with: [[laplace-approximation]] — an alternative to MCMC for approximating the same posterior $p(b_0, b_1\mid y)$, used in the Week 5 workshop on Bayesian logistic regression.
- The cross-entropy-as-negative-log-likelihood identity links to [[cross-entropy]] and [[kl-divergence]] in the information-theory topic.
- Source: [[lecture-w2]].
