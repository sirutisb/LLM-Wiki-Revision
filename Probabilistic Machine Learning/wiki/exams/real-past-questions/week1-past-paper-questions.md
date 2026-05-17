# Week 1 — Bayesian Inference: Past Paper Questions

**Source papers:** COM3023 May 2022, 2023, 2024, 2025
**Topic coverage:** uncertainty types, Bayesian vs Frequentist, MLE (binomial, Poisson regression), conjugate priors (Beta–Binomial, Gamma–Poisson), posterior mean/variance, prior types & entropy, BIC, role of likelihood × prior
**Formula sheet:** ✅ Distribution formulas will be provided in the exam

---

## COM3023 May 2022 — Question 1 (18 marks)

### Part (a) — 4 marks
What is a conjugate prior in Bayesian inference? State the advantage of using a conjugate prior.

### Part (b) — 6 marks
State two advantages and two disadvantages of using Bayesian inference.

### Part (c) — 8 marks
The likelihood of a data set $y = (y_1, \dots, y_n)$ is described with a Poisson distribution:
$$p(y|\lambda) \propto \prod_{i=1}^{n} \lambda^{y_i} e^{-\lambda}.$$
Assign a Gamma distribution as the prior on $\lambda$:
$$p(\lambda) \propto \lambda^{\alpha-1} e^{-\beta\lambda}.$$
In a Gamma distribution the mean is $\alpha/\beta$ and variance is $\alpha/\beta^2$.

**(i) — 4 marks**
Show that the Gamma distribution on $\lambda$ is the conjugate prior.

**(ii) — 4 marks**
Imagine you have only one data point $y = 10$. What is the mean and variance of the posterior distribution $p(\lambda|y)$ for $\alpha = 25$, $\beta = 3$?

---

## COM3023 May 2023 — Question 1 (20 marks)

### Part (a) — 4 marks
What are the two main types of uncertainty in Machine Learning? Where does the uncertainty come from?

### Part (b) — 4 marks
What is the main difference between Bayesian and Frequentist perspectives in probabilistic inference? What are three key terms needed in Bayesian inference?

### Part (c) — 12 marks
Denote $y$ be the number of successes from an experiment consisting of $n$ independent trials. The probability for getting a success is $\theta$, and thus $y$ follows a binomial distribution:
$$p(y|\theta) = \binom{n}{y} \theta^y (1-\theta)^{n-y}.$$

**(i) — 4 marks**
Find the parameter $\theta$ using maximum likelihood estimation.

**(ii) — 4 marks**
Assign a Beta distribution for $\theta$:
$$p(\theta) = \frac{\theta^{\alpha-1}(1-\theta)^{\beta-1}}{B(\alpha, \beta)}.$$
The mean for a Beta distribution is $\frac{\alpha}{\alpha + \beta}$. Show that the Beta distribution on $\theta$ is the conjugate prior.

**(iii) — 4 marks**
Imagine you have 70 successes from 100 independent trials. What is the mean of the posterior distribution, for $\alpha = 5$, $\beta = 5$?

---

## COM3023 May 2024 — Question 1 (selected parts — 9 marks)

### Part (a) — 5 marks
What is the main difference between a non-informative prior, a weakly-informative prior and an informative prior using normal distribution? Explain which kind of prior choice would result in the largest entropy.

### Part (c) — 2 marks
Can the product of likelihood and prior be used to make probabilistic statements? Explain the answer.

### Part (d) — 2 marks
What is the main use of Bayesian information criterion?

> *Note: Q1(b) from this paper (MLE for simple linear regression, 10 marks) appears in `week2-past-paper-questions.md`.*

---

## COM3023 May 2025 — Question 1 & Question 2 (selected parts — 11 marks)

### Q1(b) — Poisson regression MLE (selected sub-parts — 8 marks)
Derive the Maximum Likelihood Estimation (MLE) for a Poisson regression model in the univariate case. Given $n$ independent observations, each observation $y_i$ follows a Poisson distribution
$$p(y_i \mid \lambda_i) = \frac{\lambda_i^{y_i} e^{-\lambda_i}}{y_i!}$$
with mean $\lambda_i = \exp(w x_i)$, where $w$ is the model parameter to be estimated. Show all steps in the derivation, including:

**(i) — 4 marks**
Setting up the log-likelihood function.

**(ii) — 4 marks**
Differentiating the log-likelihood with respect to $w$.

> *Note: Q1(b)(iii) (why nonlinear optimisation is required) and Q1(b)(iv) (role of link function) sit under Week 2 — see `week2-past-paper-questions.md`.*

### Q2(a) — 3 marks
Describe how Bayesian inference incorporates uncertainty in machine learning.

---

## Pattern Analysis

| Paper | Marks in Week 1 | Conceptual | Numerical / derivation |
|-------|------------------|------------|------------------------|
| 2022 (Q1) | 18 | Conjugate prior; pros/cons of Bayesian inference | Show Gamma-Poisson conjugacy + posterior mean/variance |
| 2023 (Q1) | 20 | Uncertainty types; Bayesian vs Frequentist | MLE binomial + Beta-Binomial conjugacy + posterior mean |
| 2024 (Q1abcd) | 9 | Prior types + entropy ranking; BIC; product of likelihood × prior | — |
| 2025 (Q1b i–ii, Q2a) | 11 | Bayesian inference & uncertainty | Poisson regression log-likelihood + derivative |

**Consistent exam pattern:**
1. One short conceptual definition (~4–6 marks) — conjugate priors, uncertainty types, BIC, or Bayesian vs Frequentist
2. One full MLE / conjugacy derivation (~8–12 marks) — binomial, Poisson, Gamma–Poisson, or Beta–Binomial
3. A small numerical evaluation (~4 marks) — posterior mean or variance from given hyperparameters

**Must know (formula sheet provides distributions, but derivation steps are still expected):**
- MLE recipe: write likelihood → log → differentiate w.r.t. parameter → set to zero → solve
- Conjugate-prior recipe: posterior $\propto$ prior × likelihood; show the resulting kernel matches the same distribution family with updated hyperparameters
- Beta–Binomial update: $\alpha' = \alpha + y$, $\beta' = \beta + n - y$; posterior mean $= \frac{\alpha'}{\alpha' + \beta'}$
- Gamma–Poisson update: $\alpha' = \alpha + \sum y_i$, $\beta' = \beta + n$
- BIC = $-2 \log \hat{L} + k \log n$ — penalises parameter count; selects model with lowest BIC
- Largest entropy among normal priors comes from the **non-informative** (largest variance) prior
