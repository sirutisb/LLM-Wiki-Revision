# Week 2 — Linear Regression & Classification: Past Paper Questions

**Source papers:** COM3023 May 2023, 2024, 2025
**Topic coverage:** link functions, BIC, MLE for simple linear regression, Naive Bayes (generative vs discriminative; "naive" assumption; when to prefer over logistic regression), exact Bayesian inference in linear/logistic regression, link choice for Poisson regression, why MLE requires nonlinear optimisation in GLMs
**Formula sheet:** ✅ Distribution formulas will be provided in the exam

---

## COM3023 May 2023 — Question 2 (selected parts — 12 marks)

### Part (a) — 4 marks
What is the main use of link function? What is the main use of Bayesian information criterion?

### Part (b) — 4 marks
Is Naive Bayes classifier a discriminative model or a generative model? Explain the answer. State one advantage of Naive Bayes.

### Part (c) — 4 marks
Can we use exact Bayesian inference for logistic regression and linear regression? Explain the answer.

> *Note: Q2(d) (Laplace approximation, 10 marks) sits under Week 3 — see `week3-past-paper-questions.md`.*

---

## COM3023 May 2024 — Question 1(b), Question 2 (selected parts) (17 marks)

### Q1(b) — 10 marks
Given a simple linear regression model, $y_i = w x_i + \epsilon$, for $i = 1, \dots, n$, where $\epsilon \sim \mathcal{N}(0, \sigma^2)$, derive $w$ and $\sigma^2$ via maximum likelihood estimation.

*Hint: an example Gaussian distribution is given as*
$$f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{1}{2\sigma^2}(x - \mu)^2\right).$$

### Q2(a) — 4 marks
Is the Naïve Bayes classifier a Bayesian method? Explain your answer. What is the meaning of 'naïve' in Naive Bayes classifier?

### Q2(d) — 3 marks
For logistic regression, explain why a logarithmic function is not a suitable choice for the link function?

---

## COM3023 May 2025 — Question 1(b) (parts iii, iv) and Question 2(b) (12 marks)

### Q1(b)(iii) — 4 marks
*(Continuing the Poisson regression MLE derivation from Week 1.)* Explain why solving the resulting equation for $w$ requires nonlinear optimization.

### Q1(b)(iv) — 4 marks
Briefly explain the role of link functions in Poisson regression and explain why $\log(\lambda_i) = w x_i$ is a suitable choice.

### Q2(b) — 4 marks
For a binary classification problem, explain when you might prefer a Naive Bayes model over a Logistic Regression model.

---

## Pattern Analysis

| Paper | Marks in Week 2 | Conceptual | Numerical / derivation |
|-------|------------------|------------|------------------------|
| 2023 (Q2 a–c) | 12 | Link function + BIC use; Naive Bayes (gen vs disc); exact Bayes feasibility | — |
| 2024 (Q1b, Q2a, Q2d) | 17 | Naive Bayes definition; log-link unsuitability | MLE for simple linear regression (full derivation) |
| 2025 (Q1b iii–iv, Q2b) | 12 | Why nonlinear opt is needed; link-function role; NB vs Logistic | — |

**Consistent exam pattern:**
1. A short conceptual question on Naïve Bayes (~3–4 marks) — generative/discriminative status, the "naïve" assumption, or when to prefer it over logistic regression
2. A link-function question (~3–4 marks) — purpose, why log isn't suitable for logistic, why log is suitable for Poisson
3. Either a full MLE derivation for a regression model (~10 marks) OR conceptual discussion of why exact Bayes fails / why nonlinear optimisation is needed

**Must know (formula sheet provides distributions; derivations still required):**
- Simple linear regression MLE: $\hat{w} = \frac{\sum x_i y_i}{\sum x_i^2}$, $\hat{\sigma}^2 = \frac{1}{n}\sum (y_i - \hat{w}x_i)^2$
- Link function purpose: maps the linear predictor $\eta = w^\top x$ to the natural parameter / mean of the response distribution
- Logistic link (logit): $g(\mu) = \log\frac{\mu}{1-\mu}$ — maps $[0,1] \to \mathbb{R}$, unlike a log link
- Poisson link (log): $g(\mu) = \log(\mu)$ — ensures $\lambda_i > 0$ for any real $w x_i$
- Naïve Bayes: **generative** model; assumes feature independence given the class; prefer over logistic when training data is small or features approximately satisfy the independence assumption
- Exact Bayesian inference is **closed-form** only for conjugate cases (e.g., Gaussian-Gaussian linear regression with known $\sigma^2$); logistic regression has no conjugate prior so requires approximation (Laplace / VI / MCMC)
- GLMs with non-identity links produce log-likelihoods whose score equations are nonlinear in $w$, requiring iterative methods (Newton–Raphson, IRLS, gradient ascent)
