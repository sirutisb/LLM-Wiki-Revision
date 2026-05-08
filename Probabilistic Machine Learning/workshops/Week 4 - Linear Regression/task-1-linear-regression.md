# Task 1 — (Bayesian) Linear Regression on SAT/GPA

**Notebook:** `Q1_solution_linear_regression.ipynb`
**Data:** `SAT_data.csv` — three columns `math_SAT, verb_SAT, univ_GPA`. The notebook uses `math_SAT` as the predictor $x$ and `univ_GPA` as the response $y$.
**Concept tested:** [[linear-regression]] via [[mle]], then the Bayesian extension via [[mcmc]] — a four-part progression from frequentist point estimate to a full posterior over both slope and noise.

## The question (paraphrased from the workshop PDF)

We model
$$
y_i = b x_i + \varepsilon, \qquad \varepsilon \sim \mathcal{N}(0,\sigma^2),\quad i = 1,\dots,n.
$$

Note there is **no intercept** in this model — only a slope $b$. The line is forced through the origin. (See the markdown cell in the notebook: "$\varepsilon$ is *not* the intercept; it is a random error/noise term.")

The four parts walk you up the Bayesian ladder:

| Part | Unknowns | Method | What you get |
|---|---|---|---|
| Q1.1 | $b$ only ($\sigma=0.445$ given) | MLE | a single $\hat b$ |
| Q1.2 | $b$ only ($\sigma=0.445$ given) | MCMC with $\mathcal{N}(0,10^2)$ prior on $b$ | posterior $p(b\mid y)$ |
| Q1.3 | $b$ and $\sigma$ | MLE | $(\hat b, \hat\sigma)$ |
| Q1.4 | $b$ and $\sigma$ | MCMC ($b$ Normal, $\sigma$ HalfNormal) | joint posterior $p(b,\sigma\mid y)$ |

## Why this dataset suits a (Bayesian) linear model

- **Continuous response:** `univ_GPA` lies on a real-valued scale (~2.0 to ~3.8), so a Gaussian noise model is natural — the conditional density $p(y_i\mid x_i)$ is well approximated by a bell curve around the line.
- **One continuous predictor:** `math_SAT` (~480–730) makes a 2-D scatter plot meaningful; we can *see* whether a straight line is a reasonable summary.
- **Sample size matters for "MLE vs Bayesian":** the dataset has ~100 students, plenty for the likelihood to dominate the prior. So the posterior mean and the MLE will land on essentially the same number — and indeed they do, $b \approx 0.0051$. The point of doing both is not the difference in *means*, but that Bayesian inference also gives you a *spread* (uncertainty) for free.

## Cell-by-cell walkthrough

### Imports and data loading

```python
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
from scipy.optimize import minimize

data = np.loadtxt('SAT_data.csv', delimiter=',', skiprows=1)
X = data[:, 0]   # math_SAT
y = data[:, 2]   # univ_GPA
plt.scatter(X, y)
```

Three packages, three roles:

- `scipy.optimize.minimize` → numerical optimiser for MLE (Q1.1, Q1.3).
- `pymc` → probabilistic-programming framework that runs MCMC for us (Q1.2, Q1.4).
- `matplotlib` → diagnostics (scatter, histogram of residuals, trace plots).

The scatter plot is the very first sanity check: is there *something roughly linear* between SAT and GPA? Yes — a positive slope is visible.

---

### Q1.1 — MLE for $b$ with $\sigma$ fixed

#### The likelihood

For each observation, $y_i \mid x_i \sim \mathcal{N}(bx_i, \sigma^2)$, so

$$
p(y_i\mid x_i, b) = \frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left(-\frac{(y_i - b x_i)^2}{2\sigma^2}\right).
$$

Assuming i.i.d. samples, the log-likelihood for the whole dataset is

$$
\ell(b) = \sum_{i=1}^{n} \left[\log\frac{1}{\sqrt{2\pi\sigma^2}} - \frac{(y_i - b x_i)^2}{2\sigma^2}\right].
$$

The first term does not depend on $b$ — it is a constant. The second term is a sum of squares. Maximising $\ell(b)$ in $b$ is therefore equivalent to **minimising the sum of squared residuals** $\sum (y_i - b x_i)^2$. This is the headline result: **MLE under Gaussian noise = Ordinary Least Squares (OLS)**. See [[mle-simple-linear-regression]] for the full derivation.

#### The code

```python
def likelihood(theta, *args):
    b = theta
    L = np.sum(np.log(1/np.sqrt(2*np.pi*sigma_y**2))
               - 1/(2*sigma_y**2)*(y - b*X)**2)
    return -L
```

`scipy.optimize.minimize` *minimises*, so we return the **negative** log-likelihood. Then:

```python
sigma_y = 0.445
results = minimize(likelihood, [1], bounds=[(-10,10)], method='L-BFGS-B')
b_mle = float(results.x)   # ≈ 0.005095
```

`L-BFGS-B` is a quasi-Newton method with bound constraints — overkill here (the problem is convex with a closed form $\hat b = \sum x_i y_i / \sum x_i^2$), but a useful pattern for harder problems where no closed form exists.

The fitted slope $\hat b \approx 0.0051$ looks tiny because of the *units*: a 100-point bump in SAT raises predicted GPA by $\approx 0.51$, which is sensible.

#### Residual diagnostics

```python
residuals = y - b_mle * X
plt.hist(residuals, bins=30)            # raw residuals
plt.hist(residuals / sigma_y, bins=30)  # standardised
```

The Gaussian assumption is checkable *after* fitting: residuals should look approximately normal with standard deviation $\sigma$. The standardised histogram should be roughly $\mathcal{N}(0,1)$. If it has fat tails or is skewed, the linear-Gaussian model is misspecified.

---

### Q1.2 — MCMC posterior for $b$ with $\sigma$ fixed

The Bayesian recipe (lecture-w1):

$$
p(b\mid y, X) \;\propto\; p(y\mid X, b)\,p(b),
$$

with prior $b \sim \mathcal{N}(0, 10^2)$. The prior is wide (sd 10) compared to where the data place the slope ($\sim 0.005$), so it is *uninformative* — it tells the model "I have no idea, but probably not enormous". This means the posterior is essentially the likelihood, and we expect the posterior mean to match the MLE.

```python
with pm.Model() as base_model:
    b = pm.Normal('b', 0, sigma=10)
    likelihood = pm.Normal('y', mu=b*X, sigma=0.445, observed=y)
    trace = pm.sample(1000)
```

What is happening under the hood:

1. PyMC builds a computation graph encoding $\log p(b) + \log p(y\mid b)$.
2. `pm.sample` runs the **No-U-Turn Sampler** (NUTS), a self-tuning variant of [[metropolis-hastings|Hamiltonian Monte Carlo]] — see [[mcmc]].
3. After warm-up it returns 1000 samples per chain, approximately drawn from $p(b\mid y)$.

The posterior summary shows mean ≈ 0.005, sd ≈ 0.0001 — a tight posterior, exactly because we have ~100 data points pinning the slope down. The "many plausible regression lines from the posterior" plot makes the Bayesian payoff visual: every line is a *different* draw from $p(b\mid y)$, and their fan width represents our remaining uncertainty about the slope. With this much data, the fan is narrow.

---

### Q1.3 — MLE for both $b$ and $\sigma$

Now $\sigma$ is also unknown, so the likelihood becomes

$$
\ell(b,\sigma) = -\frac{n}{2}\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}\sum_{i=1}^n (y_i - b x_i)^2.
$$

Taking $\partial\ell/\partial b = 0$ and $\partial\ell/\partial \sigma = 0$ gives the standard joint MLE: the same $\hat b$ as before, plus

$$
\hat\sigma^2 = \frac{1}{n}\sum_{i=1}^n (y_i - \hat b x_i)^2.
$$

In other words, the residuals from the OLS fit *define* the noise scale. This is why we get $\hat\sigma \approx 0.334$ — that is the empirical RMS of the residuals at the MLE slope.

```python
def likelihood_(theta, *args):
    b, sigma_y = theta
    L = np.sum(np.log(1/np.sqrt(2*np.pi*sigma_y**2))
               - 1/(2*sigma_y**2)*(y - b*X)**2)
    return -L

bounds = [(-10, 10), (0.0001, 10)]   # sigma must be positive
results = minimize(likelihood_, [1, 3], bounds=bounds, method='L-BFGS-B')
```

Two things to notice:

- **Bounds on $\sigma$:** $\sigma$ is a standard deviation, so the lower bound is strictly positive. Without it, the optimiser could try $\sigma \le 0$ and the log blows up.
- **Initial guess:** $(1, 3)$ is just somewhere in the bounded box. For a convex problem the start does not matter.

The "noise as residuals" plot at the end of this section draws a vertical line from each point to the fitted line — visualising what $\varepsilon_i = y_i - \hat b x_i$ actually *is*.

---

### Q1.4 — MCMC posterior for $b$ and $\sigma$ jointly

```python
with pm.Model() as base_model:
    b = pm.Normal('b', 0, sigma=10)
    sigma_y = pm.HalfNormal('sigma_y', sigma=4)
    likelihood = pm.Normal('y', mu=b*X, sigma=sigma_y, observed=y)
    trace = pm.sample(1000)
```

Two priors now:

- $b \sim \mathcal{N}(0,10^2)$ — same wide prior as before.
- $\sigma \sim \text{HalfNormal}(4)$ — a Normal restricted to $\sigma \ge 0$. This is the standard "reasonable but uninformative" prior on a scale parameter; it does not need to be conjugate because MCMC does not require conjugacy (contrast with [[conjugate-priors]]).

The posterior summary is

| param | mean | sd | 94% HDI |
|---|---|---|---|
| `b` | 0.005 | ~0.0001 | (0.005, 0.005) |
| `sigma_y` | 0.339 | 0.023 | (0.297, 0.382) |

So the joint MCMC recovers basically the MLE point estimates, **plus** a credible interval on $\sigma$ — we now see that the noise scale itself is uncertain to ±0.02 or so. That is information OLS cannot give you without extra (frequentist) machinery.

---

## What to take away for the exam

1. **MLE under Gaussian noise = least squares.** Always be ready to drop a constant and turn the log-likelihood into a sum of squared residuals — this is bookwork. ⚠️ *Not on the formula sheet from W3 onward, but the linear-regression derivation is so standard it is fair game from W2.*
2. **The likelihood $p(y\mid x,b) = \mathcal{N}(bx, \sigma^2)$** is the thing to memorise — every part of Q1 starts from it.
3. **Closed form vs numerical:** simple linear regression has a closed-form MLE ($\hat b = \sum x_i y_i/\sum x_i^2$ for the no-intercept model). The notebook uses `scipy.minimize` to *demonstrate* the principle, but in an exam derivation just take derivatives and set to zero — see [[mle-simple-linear-regression]] and [[mle-multiple-linear-regression]].
4. **Bayesian = uncertainty for free.** The MCMC posterior gives you the same point estimate as MLE *plus* a credible interval. That credible interval shrinks as $n$ grows.
5. **Choice of priors:**
   - Wide Normal on a real-valued parameter ($b$) is a sensible default.
   - HalfNormal (or Inverse-Gamma) on a scale parameter ($\sigma$) — anything that respects $\sigma > 0$.
6. **MCMC is the workhorse when conjugacy fails.** Even when a closed-form posterior exists (e.g. Bayesian linear regression with conjugate Normal-Inverse-Gamma prior, see [[bayesian-linear-regression]]), MCMC is the model-agnostic fallback. It scales to *any* likelihood/prior combination — you saw this generality in Q1.2 and Q1.4.
7. **Diagnostics, always:** residual histogram, trace plots, posterior histograms. Without them, you are doing inference blind.

## Connections

- Builds on: [[mle]], [[linear-regression]], [[mle-simple-linear-regression]], [[supp-mle-simple-linear-regression]].
- Bayesian counterpart with closed form (using conjugate priors): [[bayesian-linear-regression]].
- The MCMC machinery used in Q1.2/Q1.4 lives in [[mcmc]] and [[metropolis-hastings]].
- Compare with: the Q2 walkthrough (`task-2-generalised-linear-model.md`) where the response is *binary* and OLS is no longer applicable, motivating [[generalised-linear-models]].
- Source: [[lecture-w2]].
