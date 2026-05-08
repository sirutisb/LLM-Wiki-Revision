# Task 1 — MLE for the Gaussian (Normal) Distribution

## The question (paraphrased)

> Assume a data vector $\mathbf{y} = (y_1, \dots, y_n)^T$ is normally distributed. Write a script to recover the mean and variance by maximising the likelihood.

The lecturer hands you this one as a *demonstration*. You already know the closed-form answers — the sample mean and the (biased) sample variance — but the point is to wire up the full machinery:

1. Generate data with known ground-truth parameters.
2. Write down the log-likelihood.
3. Hand it to a numerical optimiser and check it recovers the true values.
4. Compare the optimiser's answer against the analytic MLE formulas.

This is your first contact with the workflow you'll repeat in Q2 and Q3, so the goal is to internalise the *recipe*, not just the answer.

Related wiki pages: [[mle]], [[mle-gaussian]], [[supp-mle-gaussian]], [[lecture-w1]].

---

## Cell-by-cell walkthrough

### Cell 1 — Imports

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
```

`numpy` for vectorised maths, `matplotlib` for the sanity-check histogram, and `scipy.optimize.minimize` to do the heavy lifting. Note that scipy only *minimises* — to maximise a likelihood we will minimise its negative.

### Cell 3 — Generate synthetic data

```python
mu = 2
sigma = 3
y = np.random.normal(mu, sigma, 100000)
```

We *fix* the true parameters $\mu = 2$, $\sigma = 3$ and draw $n = 100{,}000$ samples from $\mathcal{N}(2, 3^2)$. Why so many? Because MLE is a *consistent* estimator: with more data the estimate concentrates on the true value. Using a huge sample size lets us check the optimiser is correct to several decimal places.

### Cell 5 — Histogram

```python
plt.hist(y); plt.show()
```

Always look at the data first. A bell-shaped histogram centred near 2 with most mass between $-7$ and $11$ is a visual confirmation that (a) the data look Gaussian and (b) `np.random.normal` did what we expected. In a real workshop you would skip this check at your peril — fitting a Gaussian to non-Gaussian data is the canonical "garbage in, garbage out" failure.

### Cell 6 — The log-likelihood (markdown)

For $n$ i.i.d. observations $y_1, \dots, y_n \sim \mathcal{N}(\mu, \sigma^2)$, the joint density is the product of individual Gaussian PDFs. Taking $\log$ turns the product into a sum and gives:

$$
\mathcal{L}(\mu, \sigma^2) = -\frac{n}{2}\log(2\pi) - \frac{n}{2}\log(\sigma^2) - \frac{1}{2\sigma^2}\sum_{i=1}^n (y_i - \mu)^2
$$

Why log-likelihood instead of likelihood?

1. **Numerics.** A product of $10^5$ small probabilities underflows to zero. Adding logs is stable.
2. **Algebra.** Sums are easier to differentiate than products — crucial when we derive the closed-form result.
3. **Monotonicity.** $\log$ is strictly increasing, so $\arg\max \mathcal{L} = \arg\max \log \mathcal{L}$. We lose nothing by switching.

Full derivation lives in [[mle-gaussian]].

### Cell 7 — Encode the (negative) log-likelihood

```python
def likelihood(theta, *args):
    n = len(y)
    mu = theta[0]
    sigma = theta[1]
    L = -(n/2)*np.log(2*np.pi) - (n/2)*np.log(sigma**2) - (1/(2*sigma**2))*np.sum((y-mu)**2)
    return -L
```

Two things to notice:

- `theta` packs the unknowns $(\mu, \sigma)$ into a single vector — this is the calling convention `scipy.optimize.minimize` expects.
- The function returns `-L`, not `L`. We're using a *minimiser*, so flipping the sign turns "maximise the log-likelihood" into "minimise the negative log-likelihood" (NLL). This trick is universal — every MLE you ever code in Python will look like this.

### Cell 8 — Optimise

```python
x0 = [1, 1]
results = minimize(likelihood, x0, args=(y,), bounds=None, method="L-BFGS-B")
```

- `x0 = [1, 1]` is the initial guess. The likelihood surface here is convex (after suitable reparameterisation) so the starting point doesn't matter much — but in messier problems, a bad `x0` lands you in a local minimum.
- `L-BFGS-B` is a quasi-Newton method that approximates the Hessian from successive gradients. The "B" means it supports box bounds (we don't use them here, but we will in Q2 and Q3 because parameters there are constrained to $\lambda > 0$ or $p \in (0,1)$).

### Cell 9 — Inspect

```python
print(results.x)
# [2.00930045 3.00137758]
```

The optimiser returns $\hat\mu \approx 2.009$ and $\hat\sigma \approx 3.001$ — within $0.01$ of the true $(2, 3)$. Reassuring.

### Cells 10–11 — Direct (analytic) MLE

```python
n = len(y)
mu = sum(y) / n
sigma = np.sqrt(sum((yi - mu)**2 for yi in y) / n)
```

This is the closed-form result you should know by heart for the exam. Setting the derivatives of $\mathcal{L}$ to zero gives:

$$
\hat\mu_{\text{MLE}} = \frac{1}{n}\sum_{i=1}^n y_i, \qquad
\hat\sigma^2_{\text{MLE}} = \frac{1}{n}\sum_{i=1}^n (y_i - \hat\mu)^2
$$

The numerical and analytic answers agree to many decimal places — exactly what a correct implementation should produce. ⚠️ *Formulas not given in the exam from Week 3 onwards*; the Gaussian formulas may be on the formula sheet for Week 1–2 material, but learn the derivation regardless.

Note the variance formula divides by $n$, not $n-1$. The MLE is the **biased** estimator. Bessel's correction ($n-1$) gives the unbiased estimator but is *not* the MLE.

---

## What to take away for the exam

- **The recipe.** Likelihood $\to$ log-likelihood $\to$ negate $\to$ minimise. This pattern repeats for every MLE problem in the module.
- **Why log.** Numerics, algebra, monotonicity. Be ready to state these in a one-line justification.
- **Closed form.** $\hat\mu$ is the sample mean; $\hat\sigma^2$ is the average squared deviation about $\hat\mu$, dividing by $n$ (not $n-1$). The biased-vs-unbiased distinction is a classic gotcha.
- **Two routes, same answer.** Numerical optimisation and analytic differentiation must agree — a useful sanity check on either approach.
- **Derivation.** You should be able to derive both estimators from $\frac{\partial \mathcal{L}}{\partial \mu} = 0$ and $\frac{\partial \mathcal{L}}{\partial \sigma^2} = 0$. See [[mle-gaussian]] for the full working.
