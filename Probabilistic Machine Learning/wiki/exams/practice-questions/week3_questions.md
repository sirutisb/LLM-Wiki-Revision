# Week 3 Practice Questions — Laplace Approximation

> ⚠️ **No formulas will be given in the exam for Week 3.** All results — the Taylor expansion, the variance formula, the BIC formula — must be recalled from memory.

---

## Conceptual / Bookwork

### Q1. Why approximate inference? [5 marks]

**(a)** Write down Bayes' rule for the posterior $p(\theta \mid \mathcal{D})$. Identify the term that makes exact inference intractable and explain why it is problematic. [2 marks]

**(b)** Give one concrete example (from the course) of a model where exact posterior inference is tractable and briefly explain why. Give a second example where exact inference breaks down and explain what goes wrong. [3 marks]

---

### Q2. The Laplace approximation — concept and limitations [6 marks]

**(a)** State, in one sentence, the core idea of the Laplace approximation. What family of distributions does it use to approximate the posterior, and where is that approximating distribution centred? [2 marks]

**(b)** Explain the role of the **second derivative** (curvature) of the log-posterior in the Laplace approximation. Why does a sharper peak lead to a smaller variance in the Gaussian approximation? [2 marks]

**(c)** State **two** conditions under which the Laplace approximation works well, and **two** conditions under which it works poorly. For each failure case, give a brief reason. [2 marks]

---

### Q3. Bayesian model comparison and BIC [5 marks]

**(a)** What is the **model evidence** $p(\mathcal{D} \mid \mathcal{M})$? Write it as an integral and explain in words what it measures — why does it automatically penalise unnecessarily complex models (Occam's razor)? [3 marks]

**(b)** Write down the BIC formula (in the form where lower BIC is better). Identify each term and state what it represents. [2 marks]

---

## Derivations

### Q4. Derive the 1D Laplace approximation [10 marks]

Let $\tilde{p}(\theta) = p(\mathcal{D} \mid \theta)\, p(\theta)$ be the unnormalised posterior, and define

$$g(\theta) = \log \tilde{p}(\theta).$$

**(a)** Write down the second-order Taylor expansion of $g(\theta)$ around the mode $\hat{\theta}$. Show clearly why the first-order term in the expansion vanishes. [3 marks]

**(b)** Define the positive curvature $A$ in terms of $g''(\hat{\theta})$. State the sign of $g''(\hat{\theta})$ and justify it. [2 marks]

**(c)** Exponentiate the approximation from part (a) to obtain $\tilde{p}(\theta) \approx \exp\!\big(g(\hat{\theta})\big)\exp\!\left(-\tfrac{A}{2}(\theta - \hat{\theta})^2\right)$. Hence identify the Gaussian approximation $q(\theta)$, stating its mean and variance explicitly. [3 marks]

**(d)** Briefly explain why the normalisation constant $Z = \int \tilde{p}(\theta)\, d\theta$ was not needed in order to find the mean and variance of $q(\theta)$. [2 marks]

---

### Q5. Laplace approximation for a Beta-Binomial posterior [8 marks]

Suppose we observe $y$ successes in $n$ Bernoulli trials and use a **uniform prior** $p(\theta) = 1$ on $\theta \in (0, 1)$. The unnormalised posterior is then:

$$\tilde{p}(\theta \mid y, n) \propto \theta^{y}(1-\theta)^{n-y}.$$

**(a)** Write down $g(\theta) = \log \tilde{p}(\theta \mid y, n)$. [1 mark]

**(b)** Find the MAP estimate $\hat{\theta}$ by setting $g'(\theta) = 0$. [2 marks]

**(c)** Compute $g''(\theta)$ and evaluate it at $\hat{\theta}$ to find the curvature $A = -g''(\hat{\theta})$. Simplify your answer. [3 marks]

**(d)** State the Laplace approximation $q(\theta) = \mathcal{N}(\hat{\theta},\, \sigma^2)$, giving $\sigma^2$ explicitly in terms of $y$ and $n$. [2 marks]

---

## Practical / Calculation

### Q6. Laplace approximation for a Gamma-shaped density [10 marks]

An unnormalised density (proportional to a Gamma distribution) is given by:

$$p(\theta) \propto \theta^{\alpha - 1} e^{-\beta \theta}, \qquad \theta > 0,$$

with $\alpha = 5$ and $\beta = 2$.

**(a)** Write down $g(\theta) = \log p(\theta)$ (dropping constants). [1 mark]

**(b)** Find the MAP estimate $\hat{\theta}$ by differentiating $g(\theta)$ and setting $g'(\theta) = 0$. State the constraint on $\alpha$ needed for a valid interior mode. [3 marks]

**(c)** Compute the second derivative $g''(\theta)$ and evaluate $A = -g''(\hat{\theta})$. [3 marks]

**(d)** Write down the Gaussian approximation $q(\theta) = \mathcal{N}(\hat{\theta},\, \sigma^2)$, giving numerical values for $\hat{\theta}$ and $\sigma^2$. [2 marks]

**(e)** The true mean of a Gamma$(\alpha, \beta)$ distribution is $\alpha/\beta$. Compare this to $\hat{\theta}$. Under what circumstances does the Laplace approximation become more accurate? [1 mark]

---

### Q7. BIC for model selection [6 marks]

A researcher fits two models to a dataset of $n = 50$ observations:

| Model | Parameters ($k$) | Log-likelihood at MLE |
|-------|------------------|-----------------------|
| $\mathcal{M}_1$ | 2 | $-38.0$ |
| $\mathcal{M}_2$ | 5 | $-33.5$ |

**(a)** Write down the BIC formula (where lower BIC is better). [1 mark]

**(b)** Compute the BIC score for each model. Use $\log 50 \approx 3.91$. Show your working. [3 marks]

**(c)** Which model does BIC select? Explain in one sentence what the BIC penalty term is doing here. [2 marks]

---

### Q8. MAP and Laplace for Bayesian logistic regression [8 marks]

In Bayesian logistic regression, the log-posterior (for a single parameter $w \in \mathbb{R}$, one data point) is:

$$g(w) = y \log \sigma(w) + (1-y)\log(1 - \sigma(w)) - \frac{1}{2\tau^2} w^2,$$

where $\sigma(w) = \frac{1}{1+e^{-w}}$ is the sigmoid function, $y \in \{0, 1\}$ is the observed label, and $\tau^2$ is the prior variance.

Use the fact that $\sigma'(w) = \sigma(w)(1-\sigma(w))$.

**(a)** Explain briefly why the posterior of Bayesian logistic regression cannot be computed in closed form (even in this simplified 1D case). [2 marks]

**(b)** Find $g'(w)$ and write down the equation that must be satisfied by the MAP estimate $\hat{w}$. (You do not need to solve it algebraically — just state the equation.) [3 marks]

**(c)** Compute $g''(w)$ and hence write down the Laplace approximation $q(w) = \mathcal{N}(\hat{w},\, \sigma^2)$, expressing the variance in terms of $\hat{w}$ and $\tau^2$. [3 marks]

---

## Answers / Mark Schemes

---

### A1. Mark scheme

**(a)** Bayes' rule:

$$p(\theta \mid \mathcal{D}) = \frac{p(\mathcal{D} \mid \theta)\, p(\theta)}{p(\mathcal{D})}, \qquad p(\mathcal{D}) = \int p(\mathcal{D} \mid \theta)\, p(\theta)\, d\theta.$$

The denominator $p(\mathcal{D})$ (model evidence / marginal likelihood) is intractable because it requires integrating over all parameter values. This integral is high-dimensional and usually has no closed form. [2 marks]

**(b)**
- **Tractable:** Bayesian linear regression with Gaussian prior and Gaussian likelihood. Gaussian–Gaussian conjugacy means the posterior is also Gaussian with an analytically computable mean and covariance. [1.5 marks]
- **Intractable:** Bayesian logistic regression. The Bernoulli (sigmoid) likelihood is non-Gaussian, destroying conjugacy; the posterior has no closed-form normalising constant and cannot be integrated analytically. [1.5 marks]

---

### A2. Mark scheme

**(a)** The Laplace approximation approximates the posterior with a **Gaussian** centred at the **MAP estimate** (posterior mode), using the local curvature of the log-posterior to set the variance. [2 marks]

**(b)** The second derivative $g''(\hat{\theta})$ measures how quickly the log-posterior curves downward at the mode. A sharper peak means $|g''(\hat{\theta})|$ is large, so $A = -g''(\hat{\theta})$ is large, and the variance $\sigma^2 = A^{-1} = 1/A$ is small — the Gaussian is narrow. A flatter peak gives small $A$ and large $\sigma^2$. [2 marks]

**(c)**

| Works well | Works poorly |
|------------|--------------|
| Posterior is **unimodal** | Posterior is **multimodal** — Laplace only sees one peak |
| Posterior is approximately **symmetric** | Posterior is **highly skewed** — Gaussian is symmetric so asymmetry is lost |
| Moderate to large dataset size | Deep neural networks / strong non-linearities — log-posterior far from quadratic |

[2 marks — 1 mark per column, accept any two from each]

---

### A3. Mark scheme

**(a)** The model evidence is the marginal likelihood:

$$p(\mathcal{D} \mid \mathcal{M}) = \int p(\mathcal{D} \mid \theta, \mathcal{M})\, p(\theta \mid \mathcal{M})\, d\theta.$$

It averages the likelihood over all parameter values under the prior. Complex models spread their prior probability mass thinly over many parameter configurations; most of those configurations do not fit the data well, so the average is low. Simple models concentrate their mass, giving higher evidence if they fit reasonably — automatic Occam's razor. [3 marks]

**(b)** BIC (lower is better):

$$\text{BIC} = -2\log p(\mathcal{D} \mid \hat{\theta}) + k \log n.$$

- $-2\log p(\mathcal{D} \mid \hat{\theta})$: **data fit** (lower = better fit).
- $k \log n$: **complexity penalty** — penalises models with more parameters, scaled by the log of the dataset size. [2 marks]

---

### A4. Mark scheme

**(a)** Second-order Taylor expansion of $g(\theta)$ around $\hat{\theta}$:

$$g(\theta) \approx g(\hat{\theta}) + g'(\hat{\theta})(\theta - \hat{\theta}) + \frac{1}{2}g''(\hat{\theta})(\theta - \hat{\theta})^2.$$

Since $\hat{\theta}$ is the **mode** (maximum) of $g$, it satisfies $g'(\hat{\theta}) = 0$. The linear term therefore vanishes, leaving:

$$g(\theta) \approx g(\hat{\theta}) + \frac{1}{2}g''(\hat{\theta})(\theta - \hat{\theta})^2.$$

[3 marks — 1 for writing full expansion, 1 for stating why $g'(\hat{\theta})=0$, 1 for simplified form]

**(b)** Define $A = -g''(\hat{\theta})$. Since $\hat{\theta}$ is a **maximum**, $g''(\hat{\theta}) < 0$, so $A > 0$. The approximation becomes:

$$g(\theta) \approx g(\hat{\theta}) - \frac{A}{2}(\theta - \hat{\theta})^2.$$

[2 marks]

**(c)** Exponentiating:

$$\tilde{p}(\theta) \approx \exp(g(\hat{\theta})) \cdot \exp\!\left(-\frac{A}{2}(\theta - \hat{\theta})^2\right).$$

This is proportional to a Gaussian in $\theta$. Therefore:

$$q(\theta) = \mathcal{N}(\theta \mid \hat{\theta},\, A^{-1}).$$

Mean $= \hat{\theta}$, Variance $= A^{-1} = -1/g''(\hat{\theta})$. [3 marks — 1 for exponentiating, 1 for recognising Gaussian form, 1 for stating mean and variance]

**(d)** The mean and variance of a Gaussian are determined entirely by the **exponent** — specifically the location of the peak and the coefficient of the quadratic term. The overall scale $\exp(g(\hat{\theta}))$ and the unknown $Z$ both drop out as normalising constants. We identify the Gaussian parameters purely from the shape of the quadratic in the exponent. [2 marks]

---

### A5. Mark scheme

**(a)**
$$g(\theta) = y \log \theta + (n - y)\log(1 - \theta).$$
[1 mark]

**(b)**
$$g'(\theta) = \frac{y}{\theta} - \frac{n-y}{1-\theta} = 0$$
$$y(1-\theta) = (n-y)\theta \implies y - y\theta = n\theta - y\theta \implies y = n\theta$$
$$\hat{\theta} = \frac{y}{n}.$$
[2 marks — 1 for differentiating, 1 for solving]

**(c)**
$$g''(\theta) = -\frac{y}{\theta^2} - \frac{n-y}{(1-\theta)^2}.$$

Evaluate at $\hat{\theta} = y/n$, so $1 - \hat{\theta} = (n-y)/n$:

$$g''(\hat{\theta}) = -\frac{y}{(y/n)^2} - \frac{n-y}{((n-y)/n)^2} = -\frac{yn^2}{y^2} - \frac{(n-y)n^2}{(n-y)^2} = -\frac{n^2}{y} - \frac{n^2}{n-y}.$$

$$g''(\hat{\theta}) = -n^2 \cdot \frac{n}{y(n-y)} = -\frac{n^3}{y(n-y)}.$$

$$A = -g''(\hat{\theta}) = \frac{n^3}{y(n-y)}.$$

[3 marks — 1 for $g''$, 1 for substituting $\hat{\theta}$, 1 for simplifying $A$]

**(d)**
$$\sigma^2 = A^{-1} = \frac{y(n-y)}{n^3}.$$

$$q(\theta) = \mathcal{N}\!\left(\frac{y}{n},\; \frac{y(n-y)}{n^3}\right).$$

[2 marks]

---

### A6. Mark scheme

**(a)**
$$g(\theta) = (\alpha - 1)\log\theta - \beta\theta = 4\log\theta - 2\theta \quad (\text{with } \alpha=5,\ \beta=2).$$
[1 mark]

**(b)**
$$g'(\theta) = \frac{\alpha - 1}{\theta} - \beta = 0 \implies \hat{\theta} = \frac{\alpha - 1}{\beta} = \frac{4}{2} = 2.$$

For a valid mode with $\theta > 0$ we need $\alpha > 1$ (otherwise the density has no finite interior maximum). [3 marks — 1 for differentiating, 1 for solving, 1 for constraint]

**(c)**
$$g''(\theta) = -\frac{\alpha - 1}{\theta^2}.$$

At $\hat{\theta} = 2$:

$$g''(\hat{\theta}) = -\frac{4}{4} = -1.$$

$$A = -g''(\hat{\theta}) = 1. \quad \left(\text{or: } A = \frac{\beta^2}{\alpha-1} = \frac{4}{4} = 1\right).$$

[3 marks — 1 for $g''$, 1 for evaluating, 1 for $A$]

**(d)**
$$\sigma^2 = A^{-1} = 1.$$

$$q(\theta) = \mathcal{N}(\theta \mid 2,\, 1).$$

[2 marks]

**(e)** True Gamma mean $= \alpha/\beta = 5/2 = 2.5$, whereas $\hat{\theta} = 2$. The MAP (mode) is less than the mean because the Gamma distribution is right-skewed. The approximation becomes more accurate when $\alpha$ is large (the Gamma becomes more symmetric and bell-shaped near its mode). [1 mark]

---

### A7. Mark scheme

**(a)**
$$\text{BIC} = -2\log p(\mathcal{D} \mid \hat{\theta}) + k\log n.$$
[1 mark]

**(b)**

Model $\mathcal{M}_1$: $k=2$, $\log$-likelihood $= -38.0$, $n = 50$:
$$\text{BIC}_1 = -2 \times (-38.0) + 2 \times 3.91 = 76.0 + 7.82 = 83.82.$$

Model $\mathcal{M}_2$: $k=5$, $\log$-likelihood $= -33.5$, $n = 50$:
$$\text{BIC}_2 = -2 \times (-33.5) + 5 \times 3.91 = 67.0 + 19.55 = 86.55.$$

[3 marks — 1 per correct substitution per model, 1 for arithmetic]

**(c)** BIC selects $\mathcal{M}_1$ (lower BIC $= 83.82$). The penalty term $k\log n$ penalises $\mathcal{M}_2$'s three extra parameters enough to outweigh its improved log-likelihood, preventing overfitting. [2 marks]

---

### A8. Mark scheme

**(a)** The sigmoid function makes the likelihood Bernoulli (non-Gaussian). Gaussian prior times non-Gaussian likelihood does not yield a recognisable conjugate family; the posterior has no closed-form normalising constant and cannot be integrated analytically, even in 1D. [2 marks]

**(b)** Using $\frac{d}{dw}\log\sigma(w) = 1 - \sigma(w)$ and $\frac{d}{dw}\log(1-\sigma(w)) = -\sigma(w)$:

$$g'(w) = y(1 - \sigma(w)) - (1-y)\sigma(w) - \frac{w}{\tau^2} = y - \sigma(w) - \frac{w}{\tau^2}.$$

The MAP estimate $\hat{w}$ satisfies:

$$y - \sigma(\hat{w}) - \frac{\hat{w}}{\tau^2} = 0.$$

(This has no closed-form algebraic solution; it is solved numerically.) [3 marks — 1 for differentiating log-likelihood term, 1 for differentiating prior term, 1 for combining]

**(c)** Differentiating $g'(w)$:

$$g''(w) = -\sigma'(w) - \frac{1}{\tau^2} = -\sigma(w)(1-\sigma(w)) - \frac{1}{\tau^2}.$$

At $\hat{w}$:

$$A = -g''(\hat{w}) = \sigma(\hat{w})(1 - \sigma(\hat{w})) + \frac{1}{\tau^2} > 0.$$

The Laplace approximation is:

$$q(w) = \mathcal{N}\!\left(\hat{w},\; \left[\sigma(\hat{w})(1-\sigma(\hat{w})) + \frac{1}{\tau^2}\right]^{-1}\right).$$

[3 marks — 1 for $g''$, 1 for $A$, 1 for stating $q(w)$ with correct mean and variance]
