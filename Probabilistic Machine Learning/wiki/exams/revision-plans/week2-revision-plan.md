# Week 2 Revision Plan - Linear Regression and Classification

**Scope:** [[linear-regression]], [[bayesian-linear-regression]], [[generalised-linear-models]], [[logistic-regression]], [[naive-bayes]], [[gaussian-naive-bayes]], [[poisson-regression]], [[generative-vs-discriminative]]
**Source:** [[lecture-w2]], [[supp-mle-simple-linear-regression]], [[supp-mle-multiple-linear-regression]], [[mle-simple-linear-regression]], [[mle-multiple-linear-regression]], [[examinable-topics]], [[topics-and-formulas]], [[week2_questions]]
**Formula status:** Week 2 distribution formulas will be provided. The Gaussian pdf and sigmoid/logistic function may be quoted in exam-style questions, but the simple linear regression MLE derivation, the link-function logic, the logistic regression likelihood, the Naive Bayes classification rule, and the normal-equation result must still be understood and reproducible.
**Derivation status:** Simple univariate linear regression derivations are examinable. Multiple linear regression derivations are not examinable, but the matrix result $\hat{\mathbf{w}}_{\text{MLE}}=(X^\top X)^{-1}X^\top\mathbf{y}$ is expected knowledge.

Week 2 is the second-highest priority topic after Week 1. The likely exam shape is a mixture of derivation and short applied calculations: derive the simple linear regression MLE, connect Gaussian noise to least squares, apply the normal equations to a small matrix, explain MAP/ridge regularisation, derive the sigmoid from the logit link, compare generative and discriminative classifiers, and classify a point using Gaussian Naive Bayes log-scores.

---

## What To Know Cold

### Probabilistic linear regression
- [ ] Model assumption:
$$
y_i = wx_i + \epsilon_i,
\qquad
\epsilon_i \sim \mathcal{N}(0,\sigma^2).
$$
- [ ] Conditional likelihood:
$$
p(y_i|x_i,w,\sigma^2)=\mathcal{N}(y_i|wx_i,\sigma^2).
$$
- [ ] Full log-likelihood:
$$
\ell(w,\sigma^2)
=
-\frac{n}{2}\log(2\pi\sigma^2)
-\frac{1}{2\sigma^2}\sum_{i=1}^{n}(y_i-wx_i)^2.
$$
- [ ] MLE for the slope in the no-intercept simple model:
$$
\hat{w}_{\text{MLE}}
=
\frac{\sum_i x_i y_i}{\sum_i x_i^2}.
$$
- [ ] MLE for the noise variance:
$$
\hat{\sigma}^2_{\text{MLE}}
=
\frac{1}{n}\sum_i(y_i-\hat{w}x_i)^2.
$$
- [ ] Maximising the Gaussian log-likelihood is equivalent to minimising the residual sum of squares because the only $w$-dependent term is $-\sum_i(y_i-wx_i)^2/(2\sigma^2)$.
- [ ] The MLE variance uses denominator $n$ in this course's derivation, not $n-1$.

### Multiple linear regression
- [ ] Matrix model:
$$
\mathbf{y}=X\mathbf{w}+\boldsymbol{\epsilon},
\qquad
\boldsymbol{\epsilon}\sim\mathcal{N}(\mathbf{0},\sigma^2 I).
$$
- [ ] Normal equations:
$$
X^\top X\hat{\mathbf{w}} = X^\top \mathbf{y}.
$$
- [ ] Closed-form MLE when $X^\top X$ is invertible:
$$
\hat{\mathbf{w}}_{\text{MLE}}
=
(X^\top X)^{-1}X^\top\mathbf{y}.
$$
- [ ] Know how to compute $X^\top X$, $X^\top\mathbf{y}$, a $2\times2$ inverse, and the final weight vector by hand.
- [ ] Know the invertibility condition: $X^\top X$ fails when features are perfectly collinear or there is insufficient independent information.
- [ ] Multivariate derivation is not examinable, but the result and its use are examinable.

### Bayesian linear regression and ridge
- [ ] Prior and likelihood:
$$
\mathbf{w}\sim\mathcal{N}(\mathbf{w}_0,S_0),
\qquad
\mathbf{y}|X,\mathbf{w}\sim\mathcal{N}(X\mathbf{w},\sigma^2I).
$$
- [ ] Posterior is Gaussian because Gaussian prior and Gaussian likelihood are conjugate:
$$
p(\mathbf{w}|X,\mathbf{y})=\mathcal{N}(\mathbf{w}_N,S_N).
$$
- [ ] Posterior precision and mean:
$$
S_N^{-1}=S_0^{-1}+\frac{1}{\sigma^2}X^\top X,
\qquad
\mathbf{w}_N
=
S_N\left(S_0^{-1}\mathbf{w}_0+\frac{1}{\sigma^2}X^\top\mathbf{y}\right).
$$
- [ ] With isotropic prior $\mathbf{w}\sim\mathcal{N}(\mathbf{0},\tau^2I)$, MAP equals ridge regression:
$$
\hat{\mathbf{w}}_{\text{MAP}}
=
\left(X^\top X+\frac{\sigma^2}{\tau^2}I\right)^{-1}X^\top\mathbf{y}.
$$
- [ ] Smaller prior variance $\tau^2$ means stronger shrinkage because $\lambda=\sigma^2/\tau^2$ is larger.
- [ ] Bayesian linear regression gives a distribution over weights and predictions; MLE gives only a point estimate.

### GLMs and link functions
- [ ] A GLM has three pieces: response distribution, linear predictor $\eta_i=\mathbf{w}^\top\mathbf{x}_i$, and link function $g(\mu_i)=\eta_i$.
- [ ] Linear regression: Gaussian response, identity link.
- [ ] Logistic regression: Bernoulli response, logit link.
- [ ] Poisson regression: Poisson response, log link.
- [ ] Link functions exist because the linear predictor is unbounded, while means/probabilities/rates often have restricted ranges.
- [ ] For count data, the log link gives $\log\lambda_i=\mathbf{w}^\top\mathbf{x}_i$ and inverse link $\lambda_i=\exp(\mathbf{w}^\top\mathbf{x}_i)>0$.
- [ ] For most non-Gaussian GLMs, MLE has no closed form and needs iterative optimisation.

### Logistic regression
- [ ] Binary output:
$$
y_i\in\{0,1\},
\qquad
y_i\sim\mathrm{Bernoulli}(\theta_i).
$$
- [ ] Logit link:
$$
\log\frac{\theta_i}{1-\theta_i}
=
\eta_i
=
\mathbf{w}^\top\mathbf{x}_i.
$$
- [ ] Inverse link / sigmoid:
$$
\theta_i
=
\sigma(\eta_i)
=
\frac{1}{1+e^{-\eta_i}}.
$$
- [ ] Derive sigmoid from logit:
$$
\frac{\theta}{1-\theta}=e^\eta
\Rightarrow
\theta=e^\eta(1-\theta)
\Rightarrow
\theta(1+e^\eta)=e^\eta
\Rightarrow
\theta=\frac{e^\eta}{1+e^\eta}
=\frac{1}{1+e^{-\eta}}.
$$
- [ ] Prediction rule: classify as 1 if $\theta_i\geq0.5$, equivalently if $\eta_i\geq0$.
- [ ] Log-likelihood:
$$
\ell(\mathbf{w})
=
\sum_{i=1}^{n}
\left[
y_i\log\theta_i+(1-y_i)\log(1-\theta_i)
\right].
$$
- [ ] Maximising logistic log-likelihood is the same as minimising binary cross-entropy because cross-entropy is the negative log-likelihood.
- [ ] Logistic regression has no closed-form MLE; use iterative methods such as gradient ascent or Newton-Raphson.
- [ ] A plain log link is unsuitable for binary classification because its inverse gives a positive number, not a probability constrained to $(0,1)$.

### Generative vs discriminative classification
- [ ] Generative classifiers learn $p(\mathbf{x}|y)$ and $p(y)$, hence the joint model:
$$
p(\mathbf{x},y)=p(\mathbf{x}|y)p(y).
$$
- [ ] Prediction uses Bayes' rule:
$$
\hat{y}
=
\arg\max_y p(y|\mathbf{x})
=
\arg\max_y p(\mathbf{x}|y)p(y).
$$
- [ ] Discriminative classifiers learn $p(y|\mathbf{x})$ directly or learn the decision boundary directly.
- [ ] Example pair: [[naive-bayes]] is generative; [[logistic-regression]] is discriminative.
- [ ] Generative models can be data-efficient and can model/simulate features; discriminative models usually focus more directly on predictive accuracy.

### Naive Bayes and Gaussian Naive Bayes
- [ ] Naive Bayes assumption:
$$
p(\mathbf{x}|y=k)=\prod_{j=1}^{d}p(x_j|y=k).
$$
- [ ] MAP classification rule:
$$
\hat{y}
=
\arg\max_k
\left[
\log\pi_k+\sum_{j=1}^{d}\log p(x_j|y=k)
\right].
$$
- [ ] For Gaussian Naive Bayes:
$$
p(x_j|y=k)
=
\mathcal{N}(x_j|\mu_{jk},\sigma_{jk}^2).
$$
- [ ] Log-Gaussian score contribution:
$$
\log p(x_j|y=k)
=
-\frac{1}{2}\log(2\pi\sigma_{jk}^2)
-\frac{(x_j-\mu_{jk})^2}{2\sigma_{jk}^2}.
$$
- [ ] Use log-scores instead of raw products to avoid numerical underflow and to turn products into sums.
- [ ] "Naive" means conditionally independent features given the class, not independent labels or independent observations.

---

## Derivations To Master

### Derivation 1 - MLE for simple linear regression weight
- [ ] Start from $y_i|x_i,w,\sigma^2\sim\mathcal{N}(wx_i,\sigma^2)$.
- [ ] Write the likelihood as a product over i.i.d. observations.
- [ ] Take logs and simplify to:
$$
\ell(w)
=
C-\frac{1}{2\sigma^2}\sum_i(y_i-wx_i)^2.
$$
- [ ] Differentiate:
$$
\frac{\partial \ell}{\partial w}
=
\frac{1}{\sigma^2}\sum_i x_i(y_i-wx_i).
$$
- [ ] Set to zero and solve:
$$
\sum_i x_iy_i-w\sum_i x_i^2=0
\Rightarrow
\hat{w}_{\text{MLE}}=\frac{\sum_i x_iy_i}{\sum_i x_i^2}.
$$
- [ ] State the equivalence to OLS explicitly.

### Derivation 2 - MLE for simple linear regression noise variance
- [ ] Let $v=\sigma^2$ to avoid chain-rule confusion.
- [ ] Differentiate:
$$
\frac{\partial \ell}{\partial v}
=
-\frac{n}{2v}
+\frac{1}{2v^2}\sum_i(y_i-\hat{w}x_i)^2.
$$
- [ ] Set to zero and solve:
$$
-nv+\sum_i(y_i-\hat{w}x_i)^2=0
\Rightarrow
\hat{\sigma}^2_{\text{MLE}}
=
\frac{1}{n}\sum_i(y_i-\hat{w}x_i)^2.
$$
- [ ] Interpret as mean squared residual.

### Derivation 3 - Logit to sigmoid
- [ ] Start from:
$$
\log\frac{\theta_i}{1-\theta_i}=\eta_i.
$$
- [ ] Exponentiate and rearrange to obtain:
$$
\theta_i=\frac{1}{1+e^{-\eta_i}}.
$$
- [ ] Explain why this maps every real-valued $\eta_i$ to a valid probability.

### Derivation 4 - Naive Bayes decision rule
- [ ] Start from Bayes' rule:
$$
p(y=k|\mathbf{x})
=
\frac{p(\mathbf{x}|y=k)p(y=k)}{p(\mathbf{x})}.
$$
- [ ] Drop $p(\mathbf{x})$ because it is constant across classes.
- [ ] Apply conditional independence:
$$
p(\mathbf{x}|y=k)=\prod_jp(x_j|y=k).
$$
- [ ] Take logs:
$$
\hat{y}
=
\arg\max_k
\left[
\log\pi_k+\sum_j\log p(x_j|y=k)
\right].
$$

### Not examinable as full derivations
- [ ] Multiple linear regression matrix derivation: not examinable, but know and apply $\hat{\mathbf{w}}=(X^\top X)^{-1}X^\top\mathbf{y}$.
- [ ] Bayesian linear regression posterior derivation by completing the square: not examinable in multivariate detail, but know why the posterior is Gaussian and why MAP becomes ridge.
- [ ] Logistic regression gradient derivation: understand the result and cross-entropy connection; do not prioritise a full multivariate proof over simple LR and Naive Bayes.

---

## Revision Schedule

### Pass 1 - 45 minutes: linear regression derivation
- [ ] Read [[lecture-w2]] linear regression section.
- [ ] Read [[supp-mle-simple-linear-regression]] and [[mle-simple-linear-regression]].
- [ ] From a blank page, derive $\hat{w}_{\text{MLE}}$ without looking.
- [ ] From a blank page, derive $\hat{\sigma}^2_{\text{MLE}}$ without looking.
- [ ] Do [[week2_questions]] Q4 and Q5.
- [ ] Mark every missing algebra step, especially signs in the derivative.

### Pass 2 - 45 minutes: normal equations and matrix calculations
- [ ] Read [[supp-mle-multiple-linear-regression]] and [[mle-multiple-linear-regression]].
- [ ] Memorise the normal equations and closed-form matrix result.
- [ ] Practise computing $X^\top X$ and $X^\top\mathbf{y}$ for a small design matrix.
- [ ] Do [[week2_questions]] Q6.
- [ ] Explain why the matrix derivation is not examinable but the result is still expected.

### Pass 3 - 40 minutes: Bayesian linear regression and ridge
- [ ] Read [[bayesian-linear-regression]].
- [ ] Write the prior, likelihood, posterior form, and MAP/ridge formula.
- [ ] Explain in words why Gaussian prior + Gaussian likelihood gives a Gaussian posterior.
- [ ] Explain the correspondence $\lambda=\sigma^2/\tau^2$.
- [ ] Do [[week2_questions]] Q3.
- [ ] Answer: "What changes when we move from MLE to Bayesian linear regression?"

### Pass 4 - 50 minutes: GLMs and logistic regression
- [ ] Read [[generalised-linear-models]], [[logistic-regression]], and [[poisson-regression]].
- [ ] Derive the sigmoid from the logit link.
- [ ] Write the logistic regression likelihood and log-likelihood from memory.
- [ ] Explain why log is suitable for Poisson regression but not for logistic regression.
- [ ] Do [[week2_questions]] Q2 and Q8.
- [ ] Practise computing $\eta=w_0+w_1x$, $\sigma(\eta)$, and the decision boundary $\eta=0$.

### Pass 5 - 45 minutes: classification comparison and Naive Bayes
- [ ] Read [[naive-bayes]], [[gaussian-naive-bayes]], and [[generative-vs-discriminative]].
- [ ] Build the generative vs discriminative comparison table from memory.
- [ ] Derive the Naive Bayes log-score rule from Bayes' rule.
- [ ] Do [[week2_questions]] Q1 and Q7.
- [ ] Practise one Gaussian Naive Bayes classification using log priors and log Gaussian likelihoods.
- [ ] Explain what is "naive" about Naive Bayes in one precise sentence.

### Final 20-minute check
- [ ] Reproduce the simple LR log-likelihood, $\hat{w}_{\text{MLE}}$, and $\hat{\sigma}^2_{\text{MLE}}$.
- [ ] Reproduce the normal equation result.
- [ ] Derive sigmoid from logit.
- [ ] State the logistic log-likelihood and cross-entropy relationship.
- [ ] State the Naive Bayes log-score rule.
- [ ] Compare Naive Bayes and logistic regression in four dimensions: learned distribution, prediction rule, assumptions, and example.
- [ ] Complete one small numerical normal-equation calculation and one logistic probability calculation.

---

## Practice Priorities

### Highest priority
- [ ] [[week2_questions]] Q4: simple linear regression MLE for $w$.
- [ ] [[week2_questions]] Q5: simple linear regression MLE for $\sigma^2$.
- [ ] [[week2_questions]] Q6: normal equations calculation.
- [ ] [[week2_questions]] Q1: generative vs discriminative classification.
- [ ] [[week2_questions]] Q2: logit link and sigmoid derivation.

### Medium priority
- [ ] [[week2_questions]] Q3: Bayesian linear regression and ridge.
- [ ] [[week2_questions]] Q7: Gaussian Naive Bayes hand classification.
- [ ] [[week2_questions]] Q8: logistic regression probabilities, decision boundary, cross-entropy.

### Extra drills
- [ ] Given three no-intercept points, compute $\hat{w}$ and $\hat{\sigma}^2$ by hand.
- [ ] Given a $2\times2$ $X^\top X$, invert it and compute $\hat{\mathbf{w}}$.
- [ ] Given $w_0,w_1,x$, compute $\eta$, $\sigma(\eta)$, predicted class, and decision boundary.
- [ ] Given class priors, means, variances, and one test point, compute Gaussian Naive Bayes log-scores.
- [ ] Write a four-row table comparing linear regression, Poisson regression, logistic regression, and Naive Bayes.

---

## Worked Example 1 - Simple Linear Regression MLE

### Question

Use the no-intercept model $y_i=wx_i+\epsilon_i$. For data:
$$
(x_1,y_1)=(1,2),
\qquad
(x_2,y_2)=(2,3),
\qquad
(x_3,y_3)=(3,5),
$$
compute $\hat{w}_{\text{MLE}}$.

### Solution

Use:
$$
\hat{w}_{\text{MLE}}
=
\frac{\sum_i x_i y_i}{\sum_i x_i^2}.
$$

Compute the numerator:
$$
\sum_i x_i y_i
=
1\cdot2+2\cdot3+3\cdot5
=
23.
$$

Compute the denominator:
$$
\sum_i x_i^2
=
1^2+2^2+3^2
=
14.
$$

Therefore:
$$
\hat{w}_{\text{MLE}}=\frac{23}{14}\approx1.64.
$$

---

## Worked Example 2 - Logistic Probability

### Question

A logistic regression model has $w_0=-2$ and $w_1=1$. Compute $p(y=1|x=3)$ and identify the decision boundary.

### Solution

The linear predictor is:
$$
\eta=w_0+w_1x=-2+1\cdot3=1.
$$

The probability is:
$$
p(y=1|x=3)
=
\sigma(1)
=
\frac{1}{1+e^{-1}}
\approx0.731.
$$

The decision boundary occurs when $p(y=1|x)=0.5$, equivalently $\eta=0$:
$$
-2+x=0
\Rightarrow
x=2.
$$

---

## Worked Example 3 - Gaussian Naive Bayes Score

### Question

For one feature $x^*=80$, compare two classes:

| Class | $\pi_k$ | $\mu_k$ | $\sigma_k^2$ |
|-------|---------|---------|--------------|
| 0 | 0.7 | 50 | 100 |
| 1 | 0.3 | 200 | 900 |

Use log-scores:
$$
s_k=\log\pi_k-\frac{1}{2}\log(2\pi\sigma_k^2)-\frac{(x^*-\mu_k)^2}{2\sigma_k^2}.
$$

### Solution

Class 0:
$$
s_0
=
\log0.7-\frac{1}{2}\log(2\pi\cdot100)-\frac{(80-50)^2}{2\cdot100}
\approx
-0.357-3.221-4.5
=
-8.078.
$$

Class 1:
$$
s_1
=
\log0.3-\frac{1}{2}\log(2\pi\cdot900)-\frac{(80-200)^2}{2\cdot900}
\approx
-1.204-4.320-8
=
-13.524.
$$

Since $s_0>s_1$, classify as class 0.

---

## Common Mistakes

- [ ] Thinking "formulas are provided" means the derivations do not need to be known. Simple linear regression derivations are examinable.
- [ ] Forgetting that the simple LR derivation in this course is no-intercept unless an intercept column is explicitly included.
- [ ] Dropping the negative sign incorrectly when differentiating $(y_i-wx_i)^2$.
- [ ] Using $n-1$ for the MLE of $\sigma^2$. The MLE uses $n$.
- [ ] Writing the normal equation as $XX^\top$ instead of $X^\top X$.
- [ ] Forgetting that $(X^\top X)^{-1}$ exists only when $X^\top X$ is invertible.
- [ ] Treating Bayesian linear regression as just "regular regression with uncertainty" without naming the Gaussian prior, Gaussian likelihood, and Gaussian posterior.
- [ ] Saying MAP is ridge without explaining that the Gaussian prior creates an L2 penalty.
- [ ] Confusing the log link and logit link. Log link is for positive rates; logit link is for probabilities.
- [ ] Saying logistic regression is generative. It is discriminative because it models $p(y|\mathbf{x})$ directly.
- [ ] Saying Naive Bayes models $p(y|\mathbf{x})$ directly. It models $p(\mathbf{x}|y)$ and $p(y)$, then uses Bayes' rule.
- [ ] Multiplying many Naive Bayes probabilities directly instead of using log-scores.
- [ ] Forgetting the class prior $\pi_k$ in a Naive Bayes calculation.
- [ ] Calling the Naive Bayes features independent unconditionally. The assumption is conditional independence given the class.
- [ ] Claiming logistic regression has a closed-form MLE. It requires iterative optimisation.
- [ ] Comparing generative and discriminative models only by examples, without stating joint versus conditional modelling.

---

## Exam-Ready Checklist

You are Week 2-ready when you can:

- [ ] Derive $\hat{w}_{\text{MLE}}=\sum_i x_iy_i/\sum_i x_i^2$ from the Gaussian log-likelihood without notes.
- [ ] Derive $\hat{\sigma}^2_{\text{MLE}}=n^{-1}\sum_i(y_i-\hat{w}x_i)^2$ without notes.
- [ ] Explain why Gaussian noise leads to least squares.
- [ ] Apply $\hat{\mathbf{w}}=(X^\top X)^{-1}X^\top\mathbf{y}$ to a small matrix problem.
- [ ] State the prior, likelihood, and posterior form for Bayesian linear regression.
- [ ] Explain why MAP with a Gaussian prior is ridge regression.
- [ ] Define a GLM and identify the distribution/link pairs for linear, logistic, and Poisson regression.
- [ ] Derive the sigmoid from the logit link.
- [ ] Write the logistic regression log-likelihood and connect it to cross-entropy.
- [ ] Compute logistic probabilities and decision boundaries by hand.
- [ ] Define generative and discriminative models using $p(\mathbf{x}|y)p(y)$ versus $p(y|\mathbf{x})$.
- [ ] Give Naive Bayes as the generative example and logistic regression as the discriminative example.
- [ ] Derive and apply the Naive Bayes log-score classification rule.
- [ ] Complete a Gaussian Naive Bayes classification problem using priors, means, variances, and log-scores.
- [ ] State clearly that Week 2 distribution formulas are provided, but the simple linear regression derivation is still examinable.
