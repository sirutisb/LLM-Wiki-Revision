# Task 2 — Laplace approximation for Bayesian logistic regression

**Notebook:** `Tempalte_Laplace_Bayesian_Logistic_Regression.ipynb` / `Solution of Laplace_Bayesian_Logistic_Regression.ipynb`
**Goal:** Use the [[laplace-approximation]] machinery from Task 1 on a problem where there is **no closed-form posterior** — Bayesian [[logistic-regression]]. Find the [[map]] of the parameters $b$, build the Gaussian $q(b) = \mathcal{N}(b_{\text{MAP}}, H^{-1})$, and visualise it against the true (numerically evaluated) posterior surface.

## What's being tested

Three things show up here that the exam likes:

1. **Why the logistic regression posterior is intractable.** The likelihood mixes a sigmoid into the prior — the resulting product is *not* in any standard family, so we cannot integrate it.
2. **Reducing intractable Bayes to optimisation + linear algebra.** Laplace says: optimise to find the mode (BFGS), compute the Hessian (the optimiser already estimates this), invert it for the covariance.
3. **Reading uncertainty off the Hessian.** The diagonal of $H^{-1}$ tells you how confident you are in each parameter; the off-diagonals tell you which parameters are correlated.

> Formula status: same as Task 1 — Laplace is **not on the formula sheet**. You should be able to derive $q(b) = \mathcal{N}(b_{\text{MAP}}, H^{-1})$ from a 2nd-order Taylor expansion of the log-posterior on demand.

## The model

Two-feature binary classification with sigmoid link:

$$
P(y_i = 1 \mid X_i, b) = \sigma(X_i b) = \frac{1}{1 + e^{-X_i b}}
$$

A standard Gaussian prior on the weights:

$$
P(b) = \mathcal{N}(0, I)
$$

Combining via Bayes' rule:

$$
\log P(b \mid X, y) = \underbrace{\sum_i \big[y_i \log \sigma(X_i b) + (1-y_i)\log(1-\sigma(X_i b))\big]}_{\text{log-likelihood}} \;\underbrace{- \tfrac{1}{2} b^\top b}_{\text{log-prior}} + C
$$

### Why this posterior is intractable

The Gaussian prior is conjugate to a *Gaussian* likelihood, but the [[logistic-regression]] likelihood is Bernoulli with a sigmoid — that's a non-conjugate pairing. Concretely, the integrand of the marginal $\int p(y\mid X, b) p(b)\,db$ contains $\prod_i \sigma(X_i b)^{y_i}(1-\sigma(X_i b))^{1-y_i}$ multiplied by a Gaussian. There is no analytical expression for this integral. So we cannot normalise the posterior, sample from it, or compute predictive distributions in closed form.

Laplace fixes this by *replacing* the awkward posterior with a tractable Gaussian centred at its mode.

## Cell-by-cell walkthrough

### Generating data

```python
from sklearn.datasets import make_blobs
X, y = make_blobs(n_samples=100, centers=2, n_features=2,
                  random_state=42, cluster_std=6)
```

Two Gaussian blobs in 2-D with binary labels. The deliberately large `cluster_std=6` means the blobs *overlap* — the classifier will be uncertain about points in the overlap region, which is exactly when posterior uncertainty matters.

The parameter vector $b \in \mathbb{R}^2$ is two-dimensional. That's small enough to plot a posterior contour map — you couldn't do this for a real-world model with 1000s of weights, which is why we look at a toy 2-D case here.

### `log_posterior` — the function we want to maximise

```python
def log_posterior(b, y, X):
    N = len(b)
    prior_mean = np.zeros(N)
    prior_covariance = np.eye(N)
    pi = 1/(1 + np.exp(-X.dot(b)))     # sigmoid σ(Xb)
    prior = -0.5 * (b - prior_mean).dot(np.linalg.inv(prior_covariance)).dot(b - prior_mean)
    likelihood = np.sum(y * np.log(pi) + (1-y)*np.log(1-pi))
    return -prior - likelihood          # NOTE: returns NEGATIVE log-posterior
```

Two intuitions:

- **Why return the *negative* log-posterior?** `scipy.optimize.minimize` *minimises*. We want to *maximise* the log-posterior to find the [[map]]. Negate, then minimise.
- **Why use logs at all?** Three reasons: (1) the exponential in the likelihood becomes a sum, which is numerically stable; (2) the Gaussian prior becomes a quadratic, which is the same form as the second-order Taylor expansion we'll do in a moment; (3) optimisers behave better on log-scale objectives.

### `laplace_approx` — evaluate $q(b)$ at any point

```python
def laplace_approx(b, b_mode, H):
    detH = np.linalg.det(H)
    constant = np.sqrt(detH)/(2*np.pi)**(2.0/2.0)
    density = np.exp(-0.5 * (b-b_mode).dot(H).dot(b-b_mode))
    return constant * density
```

This is the multivariate normal density of $\mathcal{N}(b_{\text{MAP}}, H^{-1})$ written in *precision form* (using $H$ directly rather than $\Sigma = H^{-1}$):

$$
q(b) = \frac{\sqrt{\det H}}{(2\pi)^{N/2}} \exp\!\Big(-\tfrac{1}{2}(b - b_{\text{MAP}})^\top H (b - b_{\text{MAP}})\Big)
$$

Why precision form? Because we already have $H$ from the optimiser (or its inverse, which we invert back). Computing once and re-using both $H$ and $\det H$ is cleaner than carrying $\Sigma$ around.

### Finding the MAP

```python
from scipy.optimize import minimize, brute
initial_guess = [1, 1]
results = minimize(log_posterior, initial_guess, args=(y, X), method='BFGS')
b_mode  = results.x        # MAP
hessian = np.linalg.inv(results.hess_inv)   # H, not H^{-1}
```

What's happening:

- **`minimize(..., method='BFGS')`** — BFGS is a quasi-Newton method that *also estimates* the inverse Hessian as a by-product of the optimisation. That's exactly what Laplace needs, so we get the covariance "for free" without a second pass.
- **`results.x` is $b_{\text{MAP}}$.** Around 0.32 and -0.09 for this dataset — the values that maximise log-likelihood + log-prior. They define the **decision boundary** of the classifier.
- **`results.hess_inv` is the *estimated* posterior covariance** $\Sigma \approx H^{-1}$. The diagonal entries (0.0042, 0.0011) are *small*, meaning we are reasonably confident about both weights. The off-diagonal (-0.00054) is small and negative — a tiny anti-correlation.
- **Why invert it back?** Our `laplace_approx` function is written in precision form, so it wants $H$, not $\Sigma$. One `np.linalg.inv` fixes that.

> A subtlety BFGS gets right: at the optimum, the gradient of the log-posterior is zero. So in the second-order Taylor expansion, the linear term vanishes and only the quadratic term (the Hessian) survives. That's why a *second-order* Taylor expansion gives a Gaussian — the Hessian *is* the Gaussian's precision.

### The grid evaluation — `brute`

```python
rranges = (slice(-7, 7, 0.1), slice(-7, 7, 0.1))
grid_sol = brute(log_posterior, rranges, args=(y, X), full_output=True)
b_i0, b_i1, log_posterior_surface = grid_sol[2][0], grid_sol[2][1], grid_sol[3]

laplace_surface = brute(laplace_approx, rranges, args=(b_mode, hessian),
                        full_output=True)
neg_log_laplace = -np.log(laplace_surface[3])
```

We are not actually using `brute` to optimise — we're abusing it to **evaluate the function on a regular $140\times 140$ grid** so we can contour-plot it. Once we have

- the negative log-posterior at every grid point, and
- the negative log of the Laplace approximation at every grid point,

a side-by-side contour comparison shows whether the Gaussian captures the posterior's shape.

### Reading the contour plots

```python
fig, ax = plt.subplots(1, 2, sharey=True)
# Left: true negative log-posterior
# Right: negative log of the Laplace approximation
```

Three things to look for:

1. **Mode location.** Both plots should peak (lowest contour value) at the red dot $b_{\text{MAP}}$. If they didn't, the optimiser would have failed.
2. **Local curvature.** Right at the mode, the elliptical contours of *both* surfaces should look similar — same orientation, same scale. That is the *guarantee* of Laplace: we match curvature exactly at the mode, by construction.
3. **Far-field behaviour.** Move away from the mode and the contours diverge:
   - The **true posterior** has whatever shape the data plus prior produces — possibly elongated, possibly with a tail that flattens because of how the sigmoid saturates.
   - The **Laplace approximation** is forced into perfect concentric ellipses — Gaussians are quadratic in log-space everywhere.
   The mismatch you see in the outer contours *is* the Laplace approximation error.

### What the inverse Hessian tells us about uncertainty

```python
results.hess_inv =
    [[ 0.00419  -0.00054]
     [-0.00054   0.00115]]
```

The Laplace posterior is $q(b) = \mathcal{N}(b_{\text{MAP}}, H^{-1})$, so this matrix *is* the (approximate) posterior covariance:

- $\mathrm{Var}(b_0) \approx 0.0042 \Rightarrow$ standard deviation $\approx 0.065$.
- $\mathrm{Var}(b_1) \approx 0.0011 \Rightarrow$ standard deviation $\approx 0.034$.
- $\mathrm{Cov}(b_0, b_1) < 0$ — knowing $b_0$ tells you something about $b_1$ (slightly).

This is what makes the approach **Bayesian** rather than just MLE-with-a-Gaussian-prior. The point estimate $b_{\text{MAP}}$ is the same as a regularised logistic regression. What you *gain* is the covariance — and from that, predictive distributions, credible intervals, and a way to detect when the model is uncertain about a new $x_*$.

## Predictions with uncertainty (the conceptual extension)

The notebook stops at visualising the posterior, but the natural exam-style follow-up is: how do you predict for a new point $x_*$?

$$
P(y_* = 1 \mid x_*, X, y) = \int \sigma(x_*^\top b) \, q(b) \, db
$$

That integral has no closed form either, but two cheap approximations work:

- **Monte Carlo.** Sample $b^{(s)} \sim \mathcal{N}(b_{\text{MAP}}, H^{-1})$ and average $\sigma(x_*^\top b^{(s)})$. Easy because Gaussians sample trivially.
- **Probit approximation.** Let $\mu_a = x_*^\top b_{\text{MAP}}$ and $\sigma_a^2 = x_*^\top H^{-1} x_*$. Then $P(y_*=1) \approx \sigma\!\left(\mu_a / \sqrt{1 + \pi\sigma_a^2/8}\right)$. This deterministic formula appears in standard textbooks (Bishop §4.5).

The point: once you have $q(b)$, *every* downstream quantity becomes either an analytic Gaussian integral or a Monte Carlo average. The intractability has been moved from "the posterior" to "an integral against a Gaussian" — much friendlier territory.

## What to take away for the exam

- **Laplace formula:** $q(b) = \mathcal{N}(b_{\text{MAP}}, H^{-1})$, $H = -\nabla^2 \log p(b\mid\mathcal{D})\big|_{b_{\text{MAP}}}$. Memorise — not on the formula sheet (Weeks 3-9 are unaided).
- **Recipe:** (1) write down $\log p(b\mid\mathcal{D})$, (2) numerically maximise with BFGS to get the [[map]], (3) take (or invert from) the optimiser's Hessian, (4) plug into the Gaussian.
- **Why it works:** a 2nd-order Taylor expansion of $\log p(b\mid\mathcal{D})$ at the mode has zero linear term (gradient is zero at a max) and quadratic term equal to $-\tfrac12(b-b_\text{MAP})^\top H(b-b_\text{MAP})$. Exponentiating gives a Gaussian — a *consequence*, not an assumption, of doing a quadratic expansion of a log density.
- **Where uncertainty lives:** the diagonal of $H^{-1}$ gives per-parameter variance; off-diagonals give parameter correlations. Reading these is a likely conceptual exam question.
- **Why logistic regression is the canonical example:** the prior is Gaussian, the [[map]] is the standard regularised classifier you already know, and the Hessian comes for free from BFGS. So Laplace adds Bayesian uncertainty quantification at almost zero extra cost.
- **Limitations to mention:** mode-seeking (only captures one mode if the posterior is multi-modal), forces symmetry (bad for skewed posteriors — see Task 1), assumes the log-posterior is well-approximated by a quadratic *globally*. When that fails the course will introduce [[variational-inference]] and [[mcmc]].

**Related pages:** [[laplace-approximation]], [[map]], [[logistic-regression]], [[bayesian-inference]], [[bic]], [[lecture-w3]].
