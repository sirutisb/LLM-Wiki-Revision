# Task 3 — MLE for the Binomial (Coin Flips)

## The question (paraphrased)

> You flip a coin $N$ times and observe $y$ heads. What distribution describes the data? Write a script that maximises the likelihood and estimates the probability $p$ of heads. Pick any values you like for $N$ and $y$.

This question deliberately leaves the modelling choice to you — unlike Q2, the lecturer doesn't say "use this distribution". You have to reason: a fixed number of independent Bernoulli trials, each with the same success probability, with the total count of successes being the observed quantity. That's the **Binomial distribution**.

The solution uses $N = 500$ and $y = 300$ heads — so we *expect* $\hat p \approx 0.6$. Let's see whether the MLE recovers that.

Related wiki pages: [[mle]], [[mle-binomial]], [[supp-mle-binomial]], [[conjugate-priors]] (the Beta-Binomial conjugate pair extends this), [[lecture-w1]].

---

## Cell-by-cell walkthrough

### Cell 0 — Imports

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
```

Same trio. We won't actually plot anything in this question — there's only a single observation $(N, y)$, so there's nothing to histogram.

### Cell 1 — Choose $N$ and $y$

```python
y = 300   # number of heads observed
n = 500   # number of trials
```

Note this is *not* a vector dataset like Q1 and Q2. A binomial experiment is a *single* compound observation: "out of 500 flips, 300 came up heads". The likelihood depends only on the totals $N$ and $y$, not on the individual flip outcomes. (Equivalently: 500 i.i.d. Bernoulli outcomes have the same likelihood for $p$ as one Binomial$(500, p)$ outcome with the same head count — the $\binom{N}{y}$ multiplier doesn't depend on $p$.)

### Cell 2 — The log-likelihood (markdown)

The Binomial PMF is

$$
p(y \mid N, p) = \binom{N}{y} p^{y} (1-p)^{N-y}
$$

Taking the log and dropping the binomial coefficient (which doesn't depend on $p$):

$$
\log L(p) \;\propto\; y \log p + (N - y)\log(1 - p)
$$

That is the function we will minimise the negative of.

Why drop $\binom{N}{y}$? Because we are maximising over $p$, and any factor independent of $p$ shifts $\log L$ by a constant — it does not change the location of the maximum. This is the same trick as dropping $y_i!$ in the Poisson question.

### Cell 3 — Code the negative log-likelihood

```python
def binomial(theta, *args):
    return -(np.log(theta)*y + (n - y)*np.log(1 - theta))
```

`theta` is the scalar parameter $p$. The `-(...)` flips the sign so we can minimise. Note `y` and `n` are read from the enclosing scope — the `*args` is unused but kept to match scipy's signature.

A quick mental sanity check on the formula: when $p \to 0$, $\log p \to -\infty$ so the log-likelihood is huge and negative if $y > 0$ — correct, you cannot have $y$ heads with a coin that never lands heads. Symmetrically $p \to 1$ blows up if $y < N$.

### Cell 4 — Optimise with bounds

```python
bounds = [(0.0000001, 0.9999999)]
results = minimize(binomial, 0.1, args=(n, y), bounds=bounds, method='L-BFGS-B')
print(results.x, float(results.fun))
# [0.6] 336.5...
```

- `bounds = [(0.0000001, 0.9999999)]` keeps $p$ strictly inside $(0, 1)$. Hitting either endpoint makes a `log(0)` blow up and the optimiser fails.
- Initial guess $0.1$ — deliberately far from the true value. Try changing it; the optimiser still lands at $0.6$. The Binomial log-likelihood is *strictly concave* in $p$, so there is one global maximum and gradient methods cannot get stuck.
- `L-BFGS-B` again — same bounded quasi-Newton choice as Q2.

The output `[0.6]` is exactly $y/N = 300/500$.

### Closed-form result (not in the notebook, but worth knowing)

Differentiating $\log L(p) = y \log p + (N-y)\log(1-p)$ with respect to $p$ and setting to zero:

$$
\frac{d}{dp}\log L(p) = \frac{y}{p} - \frac{N-y}{1-p} = 0
\;\;\Longrightarrow\;\;
\boxed{\hat p_{\text{MLE}} = \frac{y}{N}}
$$

The MLE for a Binomial probability is the empirical success rate — the fraction of heads. As with the Gaussian and Poisson, the analytic answer matches the numerical one. ⚠️ *No formula given in the exam from Week 3 onwards*; the full derivation is in [[mle-binomial]] / [[supp-mle-binomial]].

---

## Connection to Bayesian inference

This is the same likelihood that underlies the **Beta-Binomial** conjugate model in [[conjugate-priors]]. With a $\mathrm{Beta}(\alpha, \beta)$ prior on $p$, the posterior is $\mathrm{Beta}(\alpha + y, \beta + N - y)$, and the posterior mean

$$
\mathbb{E}[p \mid y] = \frac{\alpha + y}{\alpha + \beta + N}
$$

reduces to the MLE $y/N$ as the prior pseudo-counts $\alpha, \beta \to 0$ (or, equivalently, as $N$ grows large). MLE is the data-only special case; [[bayesian-inference]] adds the prior. See [[beta-binomial-posterior]] for the full derivation.

---

## What to take away for the exam

- **Recognising the model.** "Fixed number of independent yes/no trials, count the successes" $\Rightarrow$ Binomial. If the lecturer leaves the choice of distribution open, this kind of identification is the first step.
- **Closed form.** $\hat p_{\text{MLE}} = y/N$ — the empirical success rate. Derived by setting $d\log L / dp = 0$ and solving a single linear-in-$p$ equation after multiplying through by $p(1-p)$.
- **Single observation, not a vector.** The Binomial likelihood depends on the totals $(N, y)$, not the individual outcomes — handy if a question gives you summary statistics rather than raw flips.
- **Bounded optimisation.** $p \in (0, 1)$ — always pass bounds when the parameter is a probability.
- **Drop $p$-independent constants.** $\binom{N}{y}$ vanishes from the working as soon as you log-and-differentiate. Same idea as $y_i!$ in Poisson.
- **Bridge to Bayes.** The Binomial likelihood is half of the Beta-Binomial conjugate pair. Knowing the MLE is one short step from understanding the full posterior — useful framing for Week 1 conceptual questions.
- **Three distributions, one recipe.** Gaussian (Q1), Poisson (Q2), Binomial (Q3): different algebra, same six-step procedure. If you can do these three, you can do MLE for any single-parameter or two-parameter family the exam throws at you.
