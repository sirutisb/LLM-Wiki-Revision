# Week 3 Revision Plan - Laplace Approximation

**Scope:** [[laplace-approximation]], [[bayesian-model-comparison]], [[bic]], [[map]], [[bayesian-inference]], [[variational-inference]], [[mcmc]], [[laplace-gamma]]
**Source:** [[lecture-w3]], [[lecture-w10]], [[examinable-topics]], [[topics-and-formulas]], [[week3_questions]]
**Formula status:** ⚠️ No formula sheet for Week 3. The 1D Taylor expansion, MAP-centred Gaussian form, curvature definition, variance formula, model evidence integral, and BIC formula must be known from memory. The multivariate Laplace result should be understood conceptually, but the multivariate derivation is not examinable.

Week 3 is a medium-priority but high-yield exam topic: it is smaller than Weeks 1, 2, 4, and 7, but it is very easy to turn into a derivation or calculation question. The likely exam tasks are: state the purpose and limitation of Laplace approximation, derive the 1D approximation from a Taylor expansion, apply the method to a given unnormalised density, explain Bayesian model evidence, and compute BIC for model selection.

---

## What To Know Cold

### Why approximate inference is needed
- [ ] Bayes' rule for parameters:
$$
p(\theta|\mathcal{D})
=
\frac{p(\mathcal{D}|\theta)p(\theta)}
{p(\mathcal{D})}.
$$
- [ ] The evidence / normalising constant:
$$
p(\mathcal{D})
=
\int p(\mathcal{D}|\theta)p(\theta)\,d\theta.
$$
- [ ] The intractable part is usually the integral over all parameter values.
- [ ] Bayesian linear regression is tractable because Gaussian likelihood plus Gaussian prior gives Gaussian conjugacy.
- [ ] Bayesian logistic regression is intractable because the sigmoid Bernoulli likelihood is non-Gaussian and breaks conjugacy.
- [ ] Approximate inference families:
  - [[laplace-approximation]]: local Gaussian approximation at the MAP.
  - [[variational-inference]]: optimisation over a tractable distribution family.
  - [[mcmc]]: sampling from a Markov chain with the posterior as its stationary distribution.

### Core Laplace idea
- [ ] The Laplace approximation fits a Gaussian to the posterior at its mode:
$$
q(\theta)
=
\mathcal{N}(\theta|\hat{\theta}, A^{-1}).
$$
- [ ] The centre is the MAP estimate:
$$
\hat{\theta}
=
\arg\max_\theta p(\theta|\mathcal{D})
=
\arg\max_\theta p(\mathcal{D}|\theta)p(\theta).
$$
- [ ] Work with the log unnormalised posterior:
$$
g(\theta)
=
\log \tilde{p}(\theta)
=
\log p(\mathcal{D}|\theta)+\log p(\theta).
$$
- [ ] The evidence $p(\mathcal{D})$ is not needed to locate the MAP because it does not depend on $\theta$.
- [ ] The unknown normalising constant is also not needed to identify the Gaussian's mean and variance because the quadratic exponent determines the shape.

### The 1D derivation
- [ ] Start with the second-order Taylor expansion around $\hat{\theta}$:
$$
g(\theta)
\approx
g(\hat{\theta})
+ g'(\hat{\theta})(\theta-\hat{\theta})
+ \frac{1}{2}g''(\hat{\theta})(\theta-\hat{\theta})^2.
$$
- [ ] At the mode, $g'(\hat{\theta})=0$, so the linear term vanishes:
$$
g(\theta)
\approx
g(\hat{\theta})
+ \frac{1}{2}g''(\hat{\theta})(\theta-\hat{\theta})^2.
$$
- [ ] Since $\hat{\theta}$ is a maximum, $g''(\hat{\theta})<0$.
- [ ] Define positive curvature:
$$
A=-g''(\hat{\theta})>0.
$$
- [ ] Rewrite the approximation:
$$
g(\theta)
\approx
g(\hat{\theta})
- \frac{A}{2}(\theta-\hat{\theta})^2.
$$
- [ ] Exponentiate:
$$
\tilde{p}(\theta)
\approx
\exp(g(\hat{\theta}))
\exp\!\left[-\frac{A}{2}(\theta-\hat{\theta})^2\right].
$$
- [ ] Recognise the Gaussian form:
$$
q(\theta)
=
\mathcal{N}(\theta|\hat{\theta}, A^{-1}),
\qquad
\sigma^2=A^{-1}=-\frac{1}{g''(\hat{\theta})}.
$$

### Curvature intuition
- [ ] Large $A$ means a sharp peak, so the Gaussian variance $A^{-1}$ is small.
- [ ] Small $A$ means a flat peak, so the Gaussian variance $A^{-1}$ is large.
- [ ] The second derivative is taken on the log posterior, not directly on the posterior density.
- [ ] Use negative curvature $A=-g''(\hat{\theta})$, not $g''(\hat{\theta})$ itself.

### Multivariate result
- [ ] Know the result conceptually:
$$
p(\boldsymbol{\theta}|\mathcal{D})
\approx
\mathcal{N}(\boldsymbol{\theta}|\hat{\boldsymbol{\theta}}, \mathbf{H}^{-1}),
\qquad
\mathbf{H}
=
-\nabla^2 g(\boldsymbol{\theta})\big|_{\boldsymbol{\theta}=\hat{\boldsymbol{\theta}}}.
$$
- [ ] Interpret $\mathbf{H}$ as the negative Hessian of the log posterior at the MAP.
- [ ] Interpret $\mathbf{H}^{-1}$ as the covariance matrix.
- [ ] Strong curvature directions have smaller posterior uncertainty.
- [ ] ⚠️ Do not spend time memorising the multivariate Taylor/Hessian derivation: it is not examinable.

### When Laplace works and fails
- [ ] Works well when the posterior is unimodal.
- [ ] Works well when the posterior is approximately symmetric and bell-shaped near the mode.
- [ ] Works better with moderate to large datasets, where posteriors often become more concentrated.
- [ ] Fails for multimodal posteriors because it captures only one mode.
- [ ] Fails for strongly skewed posteriors because the Gaussian approximation is symmetric.
- [ ] Fails for heavy-tailed or highly nonlinear posteriors because local curvature does not represent the global shape.
- [ ] Main limitation phrasing: "Laplace is local; it only uses information near the MAP."

### Bayesian model comparison
- [ ] Model posterior:
$$
p(\mathcal{M}|\mathcal{D})
\propto
p(\mathcal{D}|\mathcal{M})p(\mathcal{M}).
$$
- [ ] Model evidence:
$$
p(\mathcal{D}|\mathcal{M})
=
\int p(\mathcal{D}|\theta,\mathcal{M})p(\theta|\mathcal{M})\,d\theta.
$$
- [ ] With equal model priors, choose the model with larger evidence.
- [ ] Evidence implements Occam's razor because it averages likelihood over the parameter space rather than only evaluating the best parameter.
- [ ] Complex models are penalised because they spread prior probability mass across many parameter settings, many of which fit the data poorly.

### BIC
- [ ] Know the lower-is-better form used in [[week3_questions]]:
$$
\mathrm{BIC}
=
-2\log p(\mathcal{D}|\hat{\theta})
+ k\log n.
$$
- [ ] $-2\log p(\mathcal{D}|\hat{\theta})$ is the data-fit term; lower is better.
- [ ] $k\log n$ is the complexity penalty; more parameters increase BIC.
- [ ] In this form, choose the model with the lower BIC.
- [ ] Also recognise the log-evidence form from [[bic]]:
$$
\mathrm{BIC}_{\log}
=
\log p(\mathcal{D}|\hat{\theta})
- \frac{k}{2}\log n.
$$
- [ ] In the log-evidence form, choose the model with the higher value.
- [ ] Always check which sign convention the question uses before deciding "higher" or "lower".
- [ ] BIC is derived by applying Laplace to the evidence integral, but the full multivariate derivation is not examinable.

---

## Derivations To Master

### Derivation 1 - generic 1D Laplace approximation
- [ ] Define $\tilde{p}(\theta)$ and $g(\theta)=\log\tilde{p}(\theta)$.
- [ ] State that $\hat{\theta}$ is the mode / MAP.
- [ ] Write the second-order Taylor expansion.
- [ ] Cancel the first-order term using $g'(\hat{\theta})=0$.
- [ ] Define $A=-g''(\hat{\theta})>0$.
- [ ] Exponentiate and identify the Gaussian.
- [ ] Finish with:
$$
q(\theta)=\mathcal{N}(\theta|\hat{\theta}, A^{-1}).
$$

### Derivation 2 - Beta-Binomial-style posterior
- [ ] Start from:
$$
\tilde{p}(\theta|y,n)
\propto
\theta^y(1-\theta)^{n-y}.
$$
- [ ] Log posterior:
$$
g(\theta)=y\log\theta+(n-y)\log(1-\theta).
$$
- [ ] First derivative:
$$
g'(\theta)
=
\frac{y}{\theta}
- \frac{n-y}{1-\theta}.
$$
- [ ] MAP:
$$
\hat{\theta}=\frac{y}{n}.
$$
- [ ] Second derivative:
$$
g''(\theta)
=
-\frac{y}{\theta^2}
-\frac{n-y}{(1-\theta)^2}.
$$
- [ ] Curvature:
$$
A=-g''(\hat{\theta})
=
\frac{n^3}{y(n-y)}.
$$
- [ ] Variance:
$$
\sigma^2=A^{-1}
=
\frac{y(n-y)}{n^3}.
$$
- [ ] Final approximation:
$$
q(\theta)
=
\mathcal{N}\!\left(\frac{y}{n}, \frac{y(n-y)}{n^3}\right).
$$

### Derivation 3 - Gamma-shaped density
- [ ] Use [[laplace-gamma]] as the full worked derivation.
- [ ] Start from:
$$
p(\theta)
\propto
\theta^{\alpha-1}e^{-\beta\theta},
\qquad
\theta>0.
$$
- [ ] Log density:
$$
g(\theta)
=
(\alpha-1)\log\theta-\beta\theta.
$$
- [ ] MAP:
$$
\hat{\theta}
=
\frac{\alpha-1}{\beta},
\qquad
\alpha>1.
$$
- [ ] Curvature:
$$
A
=
\frac{\beta^2}{\alpha-1}.
$$
- [ ] Variance:
$$
\sigma^2
=
\frac{\alpha-1}{\beta^2}.
$$
- [ ] Final approximation:
$$
q(\theta)
=
\mathcal{N}\!\left(\frac{\alpha-1}{\beta}, \frac{\alpha-1}{\beta^2}\right).
$$

### Derivation 4 - 1D Bayesian logistic regression setup
- [ ] Be able to explain why the posterior is not closed form: non-Gaussian sigmoid likelihood plus Gaussian prior is not conjugate.
- [ ] For:
$$
g(w)
=
y\log\sigma(w)
+(1-y)\log(1-\sigma(w))
-\frac{1}{2\tau^2}w^2,
$$
know:
$$
g'(w)
=
y-\sigma(w)-\frac{w}{\tau^2}.
$$
- [ ] MAP condition:
$$
y-\sigma(\hat{w})-\frac{\hat{w}}{\tau^2}=0.
$$
- [ ] Second derivative:
$$
g''(w)
=
-\sigma(w)(1-\sigma(w))
-\frac{1}{\tau^2}.
$$
- [ ] Laplace variance:
$$
\sigma_w^2
=
\left[
\sigma(\hat{w})(1-\sigma(\hat{w}))
+\frac{1}{\tau^2}
\right]^{-1}.
$$

---

## Revision Schedule

### Pass 1 - 35 minutes: memory setup
- [ ] Read [[lecture-w3]] summary and [[laplace-approximation]].
- [ ] From a blank page, write the 1D Laplace derivation without notes.
- [ ] From memory, write $g(\theta)$, $\hat{\theta}$, $A$, and $\sigma^2$ for the Beta-Binomial-style example.
- [ ] From memory, write the lower-is-better BIC formula and identify every term.
- [ ] State the multivariate result and explicitly mark the derivation as not examinable.
- [ ] Write two strengths and three limitations of Laplace approximation.

### Pass 2 - 45 minutes: derivation fluency
- [ ] Do [[week3_questions]] Q4 without looking at the answer.
- [ ] Mark the solution against the scheme and check whether the Taylor expansion is complete.
- [ ] Redo any missed step immediately, especially $g'(\hat{\theta})=0$ and $A=-g''(\hat{\theta})$.
- [ ] Do [[week3_questions]] Q5.
- [ ] Re-derive $\frac{y(n-y)}{n^3}$ until it can be produced without algebra slips.
- [ ] Do [[week3_questions]] Q6 or [[laplace-gamma]] as a second distribution-shape drill.

### Pass 3 - 40 minutes: model comparison and BIC
- [ ] Read [[bayesian-model-comparison]] and [[bic]].
- [ ] Do [[week3_questions]] Q3.
- [ ] Do [[week3_questions]] Q7.
- [ ] Practise the decision rule for both BIC sign conventions:
  - lower-is-better: $-2\log L + k\log n$.
  - higher-is-better: $\log L - \frac{k}{2}\log n$.
- [ ] Explain Occam's razor using the phrase "average likelihood over parameter space", not only "penalty".
- [ ] Write one sentence explaining why likelihood alone favours more complex models.

### Pass 4 - 45 minutes: practical and conceptual synthesis
- [ ] Do [[week3_questions]] Q1 and Q2.
- [ ] Do [[week3_questions]] Q8 for Bayesian logistic regression.
- [ ] Compare [[laplace-approximation]], [[variational-inference]], and [[mcmc]] in terms of approximation type, speed, bias, and posterior shape.
- [ ] Explain why Laplace can be fast but misleading.
- [ ] Explain why BIC is connected to Laplace approximation but does not require doing a full posterior approximation in an exam calculation.

### Final 15-minute check
- [ ] Reproduce the 1D Laplace derivation from memory.
- [ ] Reproduce the Beta-Binomial Laplace approximation from memory.
- [ ] Reproduce the Gamma Laplace approximation from memory.
- [ ] Reproduce the lower-is-better BIC formula from memory.
- [ ] State: "Week 3 has no formula sheet; multivariate derivation is not examinable."
- [ ] Answer in one sentence: "What is the main use of Laplace approximation?"
- [ ] Answer in one sentence: "What is one key limitation of Laplace approximation?"

---

## Worked Example 1 - Generic 1D Laplace Template

### Question

Given an unnormalised posterior $\tilde{p}(\theta)$, define $g(\theta)=\log\tilde{p}(\theta)$. Suppose $\hat{\theta}$ maximises $g$ and $g''(\hat{\theta})<0$. Derive the Laplace approximation.

### Solution

Taylor expand around $\hat{\theta}$:
$$
g(\theta)
\approx
g(\hat{\theta})
+g'(\hat{\theta})(\theta-\hat{\theta})
+\frac{1}{2}g''(\hat{\theta})(\theta-\hat{\theta})^2.
$$

Because $\hat{\theta}$ is the mode, $g'(\hat{\theta})=0$, so:
$$
g(\theta)
\approx
g(\hat{\theta})
+\frac{1}{2}g''(\hat{\theta})(\theta-\hat{\theta})^2.
$$

Define $A=-g''(\hat{\theta})>0$:
$$
g(\theta)
\approx
g(\hat{\theta})
-\frac{A}{2}(\theta-\hat{\theta})^2.
$$

Exponentiating gives:
$$
\tilde{p}(\theta)
\approx
\exp(g(\hat{\theta}))
\exp\!\left[-\frac{A}{2}(\theta-\hat{\theta})^2\right].
$$

The shape is Gaussian, so:
$$
q(\theta)
=
\mathcal{N}(\theta|\hat{\theta}, A^{-1}).
$$

---

## Worked Example 2 - BIC Selection

### Question

Two models are fitted to $n=100$ observations:

| Model | Parameters $k$ | Log-likelihood $\log p(\mathcal{D}|\hat{\theta})$ |
|-------|----------------|----------------------------------------------------|
| $\mathcal{M}_1$ | 3 | $-120$ |
| $\mathcal{M}_2$ | 6 | $-114$ |

Using $\log 100 \approx 4.61$, compute the lower-is-better BIC and choose a model.

### Solution

Use:
$$
\mathrm{BIC}
=
-2\log p(\mathcal{D}|\hat{\theta})
+k\log n.
$$

For $\mathcal{M}_1$:
$$
\mathrm{BIC}_1
=
-2(-120)+3(4.61)
=
240+13.83
=
253.83.
$$

For $\mathcal{M}_2$:
$$
\mathrm{BIC}_2
=
-2(-114)+6(4.61)
=
228+27.66
=
255.66.
$$

Choose $\mathcal{M}_1$ because it has the lower BIC. Although $\mathcal{M}_2$ has better log-likelihood, its extra parameters are penalised enough to make it worse under BIC.

---

## Practice Priorities

### Highest priority
- [ ] [[week3_questions]] Q4: generic 1D Laplace derivation.
- [ ] [[week3_questions]] Q5: Beta-Binomial-style Laplace calculation.
- [ ] [[week3_questions]] Q6: Gamma-shaped density calculation.
- [ ] [[week3_questions]] Q7: BIC calculation.

### Medium priority
- [ ] [[week3_questions]] Q2: concept and limitations.
- [ ] [[week3_questions]] Q3: model evidence and Occam's razor.
- [ ] [[week3_questions]] Q8: Bayesian logistic regression setup and curvature.

### Lower priority but useful synthesis
- [ ] [[week3_questions]] Q1: why approximate inference is needed.
- [ ] Compare Laplace with [[variational-inference]] and [[mcmc]].
- [ ] Explain why Laplace gives uncertainty while plain [[map]] gives only a point estimate.

---

## Common Pitfalls

- [ ] Forgetting that no formulas are given for Week 3.
- [ ] Memorising only the final Gaussian form without being able to derive it from Taylor expansion.
- [ ] Forgetting that the first derivative term vanishes because $g'(\hat{\theta})=0$.
- [ ] Using $g''(\hat{\theta})$ as the variance. The variance is $A^{-1}$, where $A=-g''(\hat{\theta})$.
- [ ] Losing the minus sign in $A=-g''(\hat{\theta})$.
- [ ] Taking derivatives of $\tilde{p}(\theta)$ instead of $g(\theta)=\log\tilde{p}(\theta)$.
- [ ] Forgetting that $\hat{\theta}$ must be a maximum, so $g''(\hat{\theta})<0$ in the 1D case.
- [ ] Saying Laplace approximates the likelihood only. It approximates the posterior, usually via the unnormalised posterior.
- [ ] Saying the mean is always the posterior mean. In Laplace, the Gaussian mean is the MAP / mode; for skewed true posteriors this can differ from the true mean.
- [ ] Treating a multimodal posterior as safe for Laplace. A single Gaussian centred at one mode misses other modes.
- [ ] Confusing Laplace approximation with Laplace smoothing in Naive Bayes.
- [ ] Confusing the two BIC sign conventions.
- [ ] Choosing the model with higher lower-is-better BIC.
- [ ] Forgetting that $k$ is the number of parameters and $n$ is the number of data points.
- [ ] Spending revision time on the multivariate derivation. Know the result and Hessian interpretation only.

---

## Exam-Ready Checklist

You are Week 3-ready when you can:

- [ ] State why approximate inference is needed and identify the evidence integral as the difficult term.
- [ ] Define the Laplace approximation in one sentence.
- [ ] Write the MAP objective used by Laplace.
- [ ] Derive the 1D Laplace approximation from Taylor expansion without notes.
- [ ] Explain why the first-order Taylor term vanishes.
- [ ] Explain why $A=-g''(\hat{\theta})$ is positive.
- [ ] Convert curvature into variance using $\sigma^2=A^{-1}$.
- [ ] Complete a Beta-Binomial-style Laplace calculation without notes.
- [ ] Complete a Gamma-shaped Laplace calculation without notes.
- [ ] Explain why Bayesian logistic regression needs approximate inference.
- [ ] State the multivariate Laplace result and say the derivation is not examinable.
- [ ] Give two conditions where Laplace works well and two where it fails.
- [ ] Define model evidence and explain the Occam's razor effect.
- [ ] Compute lower-is-better BIC and choose the correct model.
- [ ] Recognise the higher-is-better log-evidence BIC convention.
- [ ] Compare Laplace, VI, and MCMC at a conceptual level.
- [ ] State that Week 3 has no formula sheet and that the multivariate derivation is not examinable.
- [ ] Similar past-paper calibration: practise Laplace on an arbitrary unnormalised 1D density by taking logs, differentiating, solving for the mode, and computing curvature.
