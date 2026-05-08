# Task 2 — MLE for the Poisson (Prussian Horse Kicks)

## The question (paraphrased)

> Von Bortkiewicz counted the number of Prussian cavalrymen killed by horse kicks each year, per cavalry corps, from 1875 to 1894. Model the counts as $\mathbf{y} \sim \mathrm{Poisson}(\lambda)$ with
> $$ p(\mathbf{y}\mid\lambda) \propto \prod_{i=1}^n \lambda^{y_i} e^{-\lambda}, $$
> and write a script that estimates $\lambda$ by maximising the likelihood.

This is the famous Bortkiewicz dataset — one of the first real-world demonstrations that rare-event count data follow a Poisson distribution. Your job is to apply the same MLE recipe from Q1 to a *new* distribution and a *real* dataset.

The CSV (`Prussian-Horse-Kick-Data_Workshop.csv`) contains 280 numbers, each one the count of deaths for one corps in one year — values like $0, 0, 1, 0, 2, 1, \dots$.

Related wiki pages: [[mle]], [[bayesian-inference]], [[lecture-w1]].

---

## Cell-by-cell walkthrough

### Cell 0 — Optional Colab mount

```python
# from google.colab import drive
# drive.mount('/drive')
```

If you run this on Google Colab, you mount Drive so the CSV is reachable. Locally just point `np.loadtxt` at the file path directly.

### Cell 1 — Imports

`numpy`, `matplotlib`, and `scipy.optimize.minimize` again — same trio as Q1. The recipe is the same; only the distribution changes.

### Cell 2 — Load and visualise

```python
y = np.loadtxt('.../Prussian-Horse-Kick-Data_Workshop.csv')
plt.hist(y); plt.show()
```

Look at the histogram: a tall bar at $0$, smaller at $1$, even smaller at $2$, almost nothing past $3$ or $4$. That right-skewed staircase shape is the *signature* of a Poisson distribution with small $\lambda$. If you saw a bell curve instead, Poisson would be the wrong model — sanity-checking the histogram before fitting is a habit that catches a lot of mistakes.

### Cell 3 — Likelihood and log-likelihood (markdown)

The Poisson PMF is $p(y_i \mid \lambda) = \lambda^{y_i} e^{-\lambda} / y_i!$. For $n$ i.i.d. observations,

$$
p(\mathbf{y}\mid\lambda) = \prod_{i=1}^n \frac{\lambda^{y_i} e^{-\lambda}}{y_i!}
\;\propto\; \lambda^{\sum_i y_i} e^{-n\lambda}
$$

The $y_i!$ in the denominator is dropped because it does not depend on $\lambda$ — any constant multiplier of the likelihood vanishes when you differentiate $\log L$ with respect to $\lambda$. Taking logs:

$$
\log p(\mathbf{y}\mid\lambda) \;\propto\; \Big(\sum_{i=1}^n y_i\Big)\log\lambda \;-\; n\lambda
$$

This is the function we will hand to the optimiser.

### Cell 4 — Code the negative log-likelihood

```python
def likelihood(theta, *args):
    n = len(y)
    L = np.sum(y)*np.log(theta) - theta*n
    return -L
```

`theta` is a single scalar (well, a length-1 vector by scipy's convention) — the unknown $\lambda$. Two implementation points worth flagging:

- `np.sum(y)` is computed inside the function. For repeated calls this is wasteful — a faster version would compute it once outside and close over it. Fine here because `minimize` only calls the function a handful of times.
- We return `-L`. Same trick as Q1: minimise the negative to maximise the original.

### Cell 5 — Optimise with bounds

```python
bounds = [(0.0001, 100)]
x0 = [1]
results = minimize(likelihood, x0, args=(y,), bounds=bounds, method='L-BFGS-B')
```

The new ingredient is `bounds`. The Poisson rate must satisfy $\lambda > 0$ — feed the optimiser a non-positive value and `np.log(theta)` either explodes or returns `nan`. The lower bound $0.0001$ keeps the search in the feasible region. The upper bound $100$ is loose; it just prevents `L-BFGS-B` from wandering off to absurd values.

This is *also* why we picked `L-BFGS-B` rather than plain BFGS — the trailing "B" is for **bounded**.

### Cell 6 — Result

```python
print(results.x, results.fun)
# [0.7] 265.908...
```

The MLE is $\hat\lambda \approx 0.7$. That is, roughly *0.7 deaths per corps per year* on average.

You can verify by computing $\bar y = \sum y_i / n$ directly: with $\sum y_i = 196$ and $n = 280$ you get exactly $0.7$.

### Cell 7 — Closed-form derivation (markdown)

The reason $\hat\lambda = \bar y$ is no coincidence. Differentiating

$$
\log L(\lambda) = \Big(\sum_i y_i\Big)\log\lambda - n\lambda
$$

with respect to $\lambda$ and setting to zero:

$$
\frac{d}{d\lambda}\log L(\lambda) = \frac{\sum_i y_i}{\lambda} - n = 0
\;\;\Longrightarrow\;\;
\boxed{\hat\lambda_{\text{MLE}} = \frac{1}{n}\sum_{i=1}^n y_i = \bar y}
$$

Intuitively: the parameter $\lambda$ of a Poisson *is* its mean, so the MLE of the parameter is exactly the empirical mean. The numerical optimiser and the analytic formula agree — exactly the same pattern as Q1.

⚠️ *Poisson formulas are unlikely to be on the exam formula sheet from Week 3 onwards*; learn the steps. The derivation is short — three lines — and is the cleanest possible illustration of the MLE recipe.

---

## What to take away for the exam

- **The MLE recipe is universal.** Same six steps as Q1: write the PDF/PMF, take the product, take the log, drop $\lambda$-independent constants, differentiate, set to zero. Only the algebra in the middle changes.
- **Drop constants early.** Anything that doesn't depend on the parameter being estimated (here, $y_i!$) can be dropped before differentiating. This often slashes the algebra dramatically.
- **Closed form.** $\hat\lambda_{\text{MLE}} = \bar y$. The Poisson rate parameter and the Poisson mean are the same thing, so the empirical mean is the MLE.
- **Bounds matter.** Whenever a parameter is constrained ($\lambda > 0$, $p \in (0,1)$, $\sigma > 0$), use a bounded optimiser like `L-BFGS-B`. Forgetting this is a common source of `nan` errors.
- **Recognising the model.** Right-skewed histogram of non-negative integers concentrated near zero $\Rightarrow$ Poisson is a good first guess. The lecturer told you which distribution to use here, but Q3 makes you choose.
- **Numerical $\approx$ analytic.** Always cross-check. If they disagree, either the code or the algebra is wrong.
