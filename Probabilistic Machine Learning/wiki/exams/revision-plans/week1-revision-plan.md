# Week 1 Revision Plan - Bayesian Inference

**Scope:** [[bayesian-inference]], [[likelihood]], [[mle]], [[map]], [[conjugate-priors]], [[mle-binomial]], [[mle-gaussian]], [[map-gaussian]], [[beta-binomial-posterior]]
**Source:** [[lecture-w1]], [[supp-mle-binomial]], [[supp-mle-gaussian]], [[supp-map-gaussian]], [[supp-beta-binomial]], [[examinable-topics]], [[topics-and-formulas]], [[week1_questions]]
**Formula status:** ✅ Week 1 distribution formulas will be provided in the exam: Gaussian pdf, Binomial pmf, and Beta pdf. ⚠️ The formulas being provided does not remove the need to derive MLE/MAP/conjugate posterior results from scratch. Univariate derivations are examinable; multivariate derivations are not examinable.

Week 1 is the highest-priority revision block: Bayesian inference, MLE, MAP, and conjugate priors are explicitly listed as top-priority examinable material. Expect a mix of conceptual bookwork, selected derivations, and practical calculations. The main exam skill is moving cleanly between likelihood, log-likelihood, prior, posterior, and point estimate without confusing normalised distributions with optimisation objectives.

---

## What To Know Cold

### Bayesian inference framework
- [ ] Bayes' rule for parameter inference:
$$
p(\theta|\mathcal{D})
=
\frac{p(\mathcal{D}|\theta)p(\theta)}{p(\mathcal{D})}.
$$
- [ ] Posterior proportionality:
$$
p(\theta|\mathcal{D}) \propto p(\mathcal{D}|\theta)p(\theta).
$$
- [ ] Evidence / marginal likelihood:
$$
p(\mathcal{D}) = \int p(\mathcal{D}|\theta)p(\theta)\,d\theta.
$$
- [ ] Posterior predictive distribution:
$$
p(y'|\mathcal{D}) = \int p(y'|\theta)p(\theta|\mathcal{D})\,d\theta.
$$
- [ ] Define likelihood, prior, posterior, evidence, and posterior predictive in one sentence each.
- [ ] Explain why $p(\mathcal{D})$ can be dropped for optimisation over $\theta$ but is required to make the posterior a normalised probability distribution.
- [ ] Explain the difference between aleatoric uncertainty and epistemic uncertainty.
- [ ] State why full Bayesian inference is richer than MLE/MAP: it keeps the whole posterior, not just one parameter value.

### Likelihood and log-likelihood
- [ ] For i.i.d. observations:
$$
L(\theta)=p(\mathcal{D}|\theta)=\prod_{i=1}^{n}p(y_i|\theta).
$$
- [ ] Log-likelihood:
$$
\ell(\theta)=\log L(\theta)=\sum_{i=1}^{n}\log p(y_i|\theta).
$$
- [ ] Taking logs preserves the argmax and converts products into sums.
- [ ] Terms not depending on the parameter can be dropped when differentiating.
- [ ] The likelihood is a function of $\theta$; it is not automatically a probability distribution over $\theta$.

### MLE
- [ ] Definition:
$$
\hat{\theta}_{\text{MLE}}
=
\arg\max_{\theta}p(\mathcal{D}|\theta)
=
\arg\max_{\theta}\ell(\theta).
$$
- [ ] Standard method: write likelihood, take logs, drop constants, differentiate, set equal to zero, solve, check maximum.
- [ ] Binomial MLE:
$$
\hat{\theta}_{\text{MLE}}=\frac{y}{n}.
$$
- [ ] Gaussian mean MLE:
$$
\hat{\mu}_{\text{MLE}}=\bar{y}=\frac{1}{n}\sum_{i=1}^{n}y_i.
$$
- [ ] Gaussian variance MLE:
$$
\hat{\sigma}^{2}_{\text{MLE}}
=
\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{\mu})^2.
$$
- [ ] The variance MLE divides by $n$, not $n-1$, so it is biased.
- [ ] MLE is a special case of MAP with a flat / uniform prior.

### MAP
- [ ] Definition:
$$
\hat{\theta}_{\text{MAP}}
=
\arg\max_{\theta}p(\theta|\mathcal{D})
=
\arg\max_{\theta}\left[\log p(\mathcal{D}|\theta)+\log p(\theta)\right].
$$
- [ ] MAP uses the likelihood plus the prior, but it still returns only a point estimate.
- [ ] MAP is the posterior mode, not the full posterior.
- [ ] Gaussian likelihood with Gaussian prior:
$$
y_i|\mu \sim \mathcal{N}(\mu,\sigma^2),
\qquad
\mu \sim \mathcal{N}(\mu_0,\sigma_0^2).
$$
- [ ] MAP estimate for the Gaussian mean:
$$
\hat{\mu}_{\text{MAP}}
=
\frac{n\sigma_0^2}{n\sigma_0^2+\sigma^2}\bar{y}
+
\frac{\sigma^2}{n\sigma_0^2+\sigma^2}\mu_0.
$$
- [ ] Equivalent precision form:
$$
\hat{\mu}_{\text{MAP}}
=
\frac{\frac{n}{\sigma^2}\bar{y}+\frac{1}{\sigma_0^2}\mu_0}
{\frac{n}{\sigma^2}+\frac{1}{\sigma_0^2}}.
$$
- [ ] Interpret the weights: more data / lower observation variance pulls toward $\bar{y}$; stronger prior / lower prior variance pulls toward $\mu_0$.
- [ ] Limiting cases: $n=0$ gives the prior mean; $n\to\infty$ gives the MLE; $\sigma_0^2\to\infty$ gives the MLE; $\sigma_0^2\to0$ gives the prior mean.

### Conjugate priors
- [ ] Definition: a prior is conjugate to a likelihood when the posterior is in the same family as the prior.
- [ ] Main advantage: closed-form posterior update; avoids explicit integration over $p(\mathcal{D})$.
- [ ] Beta-Binomial model:
$$
y|\theta \sim \text{Binomial}(n,\theta),
\qquad
\theta \sim \text{Beta}(\alpha,\beta).
$$
- [ ] Posterior update:
$$
\theta|y \sim \text{Beta}(\alpha+y,\ \beta+n-y).
$$
- [ ] Posterior mean:
$$
\mathbb{E}[\theta|y]
=
\frac{\alpha+y}{\alpha+\beta+n}.
$$
- [ ] Beta posterior MAP / mode, when the mode formula is valid:
$$
\hat{\theta}_{\text{MAP}}
=
\frac{\alpha+y-1}{\alpha+\beta+n-2}.
$$
- [ ] Interpret $\alpha$ as prior successes and $\beta$ as prior failures; $\alpha+\beta$ controls prior strength.
- [ ] Beta$(1,1)$ is uniform over $\theta\in[0,1]$.
- [ ] As $n\to\infty$, posterior mean and MAP are dominated by the data and move toward the MLE.

### MLE vs MAP vs full Bayesian inference
- [ ] MLE: likelihood only, point estimate.
- [ ] MAP: likelihood plus prior, point estimate.
- [ ] Full Bayesian inference: full posterior distribution and posterior predictive distribution.
- [ ] MLE can overfit in small datasets because it has no prior regularisation.
- [ ] MAP regularises but still loses posterior uncertainty.
- [ ] Bayesian prediction averages over parameter uncertainty rather than plugging in one estimate.

---

## Derivations To Master

### Derivation 1 - Binomial MLE
**Source:** [[supp-mle-binomial]], [[mle-binomial]]
**Exam status:** ⚠️ Must know; Binomial pmf provided.

- [ ] Start with:
$$
p(y|\theta,n)=\binom{n}{y}\theta^y(1-\theta)^{n-y}.
$$
- [ ] Drop $\log\binom{n}{y}$ as constant w.r.t. $\theta$:
$$
\ell(\theta)=y\log\theta+(n-y)\log(1-\theta)+\text{const}.
$$
- [ ] Differentiate:
$$
\frac{d\ell}{d\theta}
=
\frac{y}{\theta}
-
\frac{n-y}{1-\theta}.
$$
- [ ] Set to zero and solve:
$$
\frac{y}{\theta}=\frac{n-y}{1-\theta}
\implies
y(1-\theta)=(n-y)\theta
\implies
\hat{\theta}_{\text{MLE}}=\frac{y}{n}.
$$
- [ ] Check maximum:
$$
\frac{d^2\ell}{d\theta^2}
=
-\frac{y}{\theta^2}
-
\frac{n-y}{(1-\theta)^2}<0.
$$

### Derivation 2 - Gaussian MLE
**Source:** [[supp-mle-gaussian]], [[mle-gaussian]]
**Exam status:** ⚠️ Must know univariate derivation; Gaussian pdf provided.

- [ ] Write the i.i.d. log-likelihood:
$$
\ell(\mu,\sigma^2)
=
-\frac{n}{2}\log(2\pi)
-\frac{n}{2}\log\sigma^2
-\frac{1}{2\sigma^2}\sum_{i=1}^{n}(y_i-\mu)^2.
$$
- [ ] Differentiate w.r.t. $\mu$:
$$
\frac{\partial \ell}{\partial \mu}
=
\frac{1}{\sigma^2}\sum_{i=1}^{n}(y_i-\mu)=0
\implies
\hat{\mu}_{\text{MLE}}=\bar{y}.
$$
- [ ] Differentiate w.r.t. $v=\sigma^2$:
$$
\frac{\partial \ell}{\partial v}
=
-\frac{n}{2v}
+
\frac{1}{2v^2}\sum_{i=1}^{n}(y_i-\hat{\mu})^2=0.
$$
- [ ] Solve:
$$
\hat{\sigma}^{2}_{\text{MLE}}
=
\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{\mu})^2.
$$
- [ ] State the bias issue: MLE variance uses $n$; unbiased sample variance uses $n-1$.

### Derivation 3 - Gaussian MAP for the Mean
**Source:** [[supp-map-gaussian]], [[map-gaussian]], [[map-univariate-gaussian]]
**Exam status:** ⚠️ Must know univariate derivation; Gaussian pdf provided.

- [ ] Start from:
$$
\log p(\mu|\mathbf{y})
\propto
\log p(\mathbf{y}|\mu)+\log p(\mu).
$$
- [ ] Write the log-posterior up to constants:
$$
\log p(\mu|\mathbf{y})
\propto
-\frac{1}{2\sigma^2}\sum_{i=1}^{n}(y_i-\mu)^2
-\frac{1}{2\sigma_0^2}(\mu-\mu_0)^2.
$$
- [ ] Differentiate:
$$
\frac{\partial}{\partial\mu}\log p(\mu|\mathbf{y})
=
\frac{1}{\sigma^2}\left(\sum_{i=1}^{n}y_i-n\mu\right)
+
\frac{\mu_0-\mu}{\sigma_0^2}.
$$
- [ ] Set to zero and collect $\mu$ terms:
$$
\mu\left(\frac{n}{\sigma^2}+\frac{1}{\sigma_0^2}\right)
=
\frac{1}{\sigma^2}\sum_{i=1}^{n}y_i
+
\frac{\mu_0}{\sigma_0^2}.
$$
- [ ] Solve and rewrite as a weighted average:
$$
\hat{\mu}_{\text{MAP}}
=
\frac{\frac{n}{\sigma^2}\bar{y}+\frac{1}{\sigma_0^2}\mu_0}
{\frac{n}{\sigma^2}+\frac{1}{\sigma_0^2}}
=
\frac{n\sigma_0^2}{n\sigma_0^2+\sigma^2}\bar{y}
+
\frac{\sigma^2}{n\sigma_0^2+\sigma^2}\mu_0.
$$
- [ ] Explain why the result lies between $\bar{y}$ and $\mu_0$.

### Derivation 4 - Beta-Binomial Posterior
**Source:** [[supp-beta-binomial]], [[beta-binomial-posterior]]
**Exam status:** ⚠️ Must know proof of conjugacy; Beta and Binomial formulas provided.

- [ ] Start with Bayes' rule up to proportionality:
$$
p(\theta|y)\propto p(y|\theta)p(\theta).
$$
- [ ] Substitute the likelihood and prior:
$$
p(\theta|y)
\propto
\theta^y(1-\theta)^{n-y}
\theta^{\alpha-1}(1-\theta)^{\beta-1}.
$$
- [ ] Combine exponents:
$$
p(\theta|y)
\propto
\theta^{(\alpha+y)-1}
(1-\theta)^{(\beta+n-y)-1}.
$$
- [ ] Match the Beta functional form:
$$
\theta|y \sim \text{Beta}(\alpha+y,\ \beta+n-y).
$$
- [ ] State the update in words: add successes to $\alpha$, add failures to $\beta$.

---

## Revision Schedule

### Pass 1 - 45 minutes: framework and definitions
- [ ] Read [[lecture-w1]], [[bayesian-inference]], and [[likelihood]].
- [ ] From memory, write Bayes' rule, posterior proportionality, evidence, and posterior predictive distribution.
- [ ] Define likelihood, prior, posterior, evidence, posterior predictive, MLE, MAP, and conjugate prior.
- [ ] Write a two-column comparison of aleatoric vs epistemic uncertainty.
- [ ] Write a three-column comparison of MLE, MAP, and full Bayesian inference.
- [ ] Do [[week1_questions]] Q1 and Q2.

### Pass 2 - 60 minutes: MLE derivations
- [ ] Read [[supp-mle-binomial]], [[supp-mle-gaussian]], [[mle-binomial]], and [[mle-gaussian]].
- [ ] Derive the Binomial MLE from a blank page.
- [ ] Derive the Gaussian mean MLE from a blank page.
- [ ] Derive the Gaussian variance MLE from a blank page.
- [ ] For each derivation, explicitly mark which terms are constants and why they can be dropped.
- [ ] Do [[week1_questions]] Q4 and Q6.
- [ ] Check that every derivative sign is correct before solving.

### Pass 3 - 60 minutes: MAP derivation
- [ ] Read [[supp-map-gaussian]], [[map-gaussian]], and [[map-univariate-gaussian]].
- [ ] Derive the Gaussian MAP estimate from a blank page.
- [ ] Rewrite the result in both variance-weighted and precision-weighted forms.
- [ ] Practise explaining the limiting cases: $n=0$, $n\to\infty$, $\sigma_0^2\to0$, and $\sigma_0^2\to\infty$.
- [ ] Do [[week1_questions]] Q5 and Q8.
- [ ] Check that the weight on $\bar{y}$ is $\frac{n\sigma_0^2}{n\sigma_0^2+\sigma^2}$ and the weight on $\mu_0$ is $\frac{\sigma^2}{n\sigma_0^2+\sigma^2}$.

### Pass 4 - 50 minutes: conjugacy and posterior updating
- [ ] Read [[supp-beta-binomial]], [[conjugate-priors]], and [[beta-binomial-posterior]].
- [ ] Prove Beta-Binomial conjugacy from a blank page.
- [ ] Practise updating Beta hyperparameters for one batch of data and then for sequential batches.
- [ ] Compute posterior mean and compare it to the MLE.
- [ ] Compute the Beta posterior MAP when asked for the mode, and distinguish it from the posterior mean.
- [ ] Do [[week1_questions]] Q3 and Q7.
- [ ] Explain pseudo-counts without notes.

### Pass 5 - 35 minutes: mixed exam rehearsal
- [ ] Do one conceptual question, one derivation question, and one numerical question under timed conditions.
- [ ] For every calculation, write the model assumption first: likelihood, prior if present, observed data, target quantity.
- [ ] Practise deciding whether the question asks for MLE, MAP, posterior distribution, posterior mean, or posterior predictive.
- [ ] Redo any question where you used a formula without being able to explain where it came from.
- [ ] Summarise Week 1 on one page: definitions, four derivations, core results, pitfalls.

### Final 20-minute check
- [ ] Reproduce Bayes' rule and define every term.
- [ ] Reproduce Binomial MLE.
- [ ] Reproduce Gaussian mean and variance MLE.
- [ ] Reproduce Gaussian MAP for known variance.
- [ ] Reproduce Beta-Binomial posterior update and posterior mean.
- [ ] State exactly what formulas are given and what derivations still need to be known.
- [ ] List five common pitfalls and how to avoid them.

---

## Practice Question Priorities

| Priority | Question | Why it matters |
|----------|----------|----------------|
| 1 | [[week1_questions]] Q5 | Core Gaussian MAP derivation; high-yield selected derivation. |
| 2 | [[week1_questions]] Q4 | Core Gaussian MLE derivation; tests log-likelihood differentiation. |
| 3 | [[week1_questions]] Q7 | Beta-Binomial posterior update; tests conjugacy plus numerical interpretation. |
| 4 | [[week1_questions]] Q1 | Bayes' rule, definitions, and unnormalised posterior pitfall. |
| 5 | [[week1_questions]] Q6 | Fast Binomial MLE calculation and log-likelihood comparison. |
| 6 | [[week1_questions]] Q3 | Conjugate prior definition and pseudo-count interpretation. |
| 7 | [[week1_questions]] Q8 | Numerical Gaussian MAP; tests correct use of weights. |
| 8 | [[week1_questions]] Q2 | MLE vs MAP vs full Bayesian inference conceptual comparison. |

After first completion:
- [ ] Redo Q5 without looking at the provided MAP formula.
- [ ] Redo Q4 with different symbols, e.g. $x_i$ instead of $y_i$, to ensure the derivation is understood rather than memorised visually.
- [ ] Redo Q7 as a sequential update: use the posterior from the first batch as the prior for the second batch.
- [ ] For Q1, practise saying why $p(\mathcal{D}|\theta)p(\theta)$ is enough for MAP but not enough for probability statements.

---

## Common Mistakes

- [ ] Saying the likelihood is a probability distribution over $\theta$. It is a function of $\theta$ and need not integrate to 1.
- [ ] Treating $p(\mathcal{D}|\theta)p(\theta)$ as a normalised posterior. It is only proportional to the posterior until divided by $p(\mathcal{D})$.
- [ ] Forgetting that $p(\mathcal{D})$ can be dropped for optimisation but not for full Bayesian probability statements.
- [ ] Confusing MAP with full Bayesian inference. MAP is a point estimate; Bayesian inference keeps the posterior distribution.
- [ ] Forgetting the log-prior term in MAP and accidentally doing MLE.
- [ ] Forgetting that MLE is MAP with a flat prior.
- [ ] Dropping terms that do depend on the parameter, especially $\log\sigma^2$ in Gaussian variance MLE.
- [ ] Getting the sign wrong when differentiating $\log(1-\theta)$ in the Binomial MLE.
- [ ] Forgetting to check the second derivative or at least state why the stationary point is a maximum.
- [ ] Using $n-1$ for the Gaussian variance MLE. The MLE uses $n$; $n-1$ is the unbiased estimator.
- [ ] Swapping the Gaussian MAP weights: the data weight contains $n\sigma_0^2$, while the prior-mean weight contains $\sigma^2$.
- [ ] Saying a strong prior has large variance. A strong Gaussian prior has small variance / high precision.
- [ ] Confusing posterior mean with MAP for the Beta posterior.
- [ ] Updating Beta parameters as $\alpha+n$ and $\beta+y$. Correct update is $\alpha+y$, $\beta+n-y$.
- [ ] Forgetting that $\alpha$ and $\beta$ behave like pseudo-counts, but the exact "prior sample size" interpretation depends on convention.
- [ ] Assuming multivariate derivations are examinable. Week 1 derivations are univariate only.

---

## Exam-Ready Checklist

You are Week 1-ready when you can:

- [ ] State Bayes' rule, posterior proportionality, and evidence from memory.
- [ ] Define likelihood, prior, posterior, evidence, posterior predictive, MLE, MAP, and conjugate prior clearly.
- [ ] Explain why Bayesian inference quantifies uncertainty better than MLE or MAP.
- [ ] Compare MLE, MAP, and full Bayesian inference without notes.
- [ ] Derive the Binomial MLE $\hat{\theta}=y/n$ from the Binomial pmf.
- [ ] Derive the Gaussian MLEs $\hat{\mu}=\bar{y}$ and $\hat{\sigma}^2=\frac{1}{n}\sum_i(y_i-\bar{y})^2$.
- [ ] Derive the Gaussian MAP estimate for a mean with known variance and Gaussian prior.
- [ ] Explain the Gaussian MAP result as a weighted average of sample mean and prior mean.
- [ ] Prove Beta-Binomial conjugacy by matching the posterior kernel to the Beta functional form.
- [ ] Update a Beta prior after one or more batches of Binomial data.
- [ ] Compute a posterior mean and compare it to the MLE.
- [ ] Distinguish posterior mean, posterior mode / MAP, and MLE.
- [ ] Complete a numerical Gaussian MAP question with correct weights and arithmetic.
- [ ] State that Week 1 distribution formulas are provided, but derivations still need to be known.
- [ ] State that multivariate derivations are not examinable for Week 1.
- [ ] Avoid using an unnormalised posterior for direct probability statements.
- [ ] Similar past-paper calibration: answer short questions on aleatoric vs epistemic uncertainty, Bayesian vs frequentist parameter treatment, and weak/informative/non-informative Gaussian priors.
