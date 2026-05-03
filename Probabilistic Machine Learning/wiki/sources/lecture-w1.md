# Week 1 — Introduction + Bayesian Inference

**File:** `raw/text/COM3031_2526_W1.txt`
**Type:** lecture
**Week:** 1
**Concepts introduced:** [[bayesian-inference]], [[mle]], [[map]], [[conjugate-priors]], [[likelihood]]

## Summary
Week 1 motivates probabilistic ML through the need to quantify uncertainty, introduces the key distinction between aleatoric (irreducible) and epistemic (reducible) uncertainty, and builds the full Bayesian inference pipeline: likelihood → prior → posterior → predictive distribution. MLE and MAP are introduced as point-estimate alternatives to full posterior inference. Conjugate priors are introduced as a tractable special case.

## Key content

### Why Probabilistic ML
- Real-world decisions require quantified uncertainty (e.g. R-number for COVID).
- Neural networks are often **over-confident** — Bayesian methods fix this.
- **Aleatoric uncertainty**: inherent randomness in the data (coin flip). Cannot be reduced.
- **Epistemic uncertainty**: lack of knowledge about the model. Can be reduced with data.

### Probabilistic Modelling
- Model: parameters $\boldsymbol{\theta}$, observations $\mathbf{y}$ drawn from $p(\mathbf{y}|\boldsymbol{\theta})$.
- Common choice: Gaussian, $p(y_i|\boldsymbol{\theta}) \sim \mathcal{N}(\mu, \sigma^2)$.
- **Likelihood function**: once data are observed, $L(\boldsymbol{\theta}) = p(\mathbf{y}|\boldsymbol{\theta}) = \prod_{i=1}^n p(y_i|\theta)$.

### Maximum Likelihood Estimation (MLE)
$$\hat{\boldsymbol{\theta}}_{\text{MLE}} = \arg\max_{\boldsymbol{\theta}}\, \log L(\boldsymbol{\theta})$$
- Taking log converts products to sums (numerically stable, same argmax).
- For Gaussian: $\hat{\mu}_{\text{MLE}} = \bar{y}$ (sample mean).
- For Binomial: $\hat{\theta}_{\text{MLE}} = y/n$ (sample proportion).

### Bayesian Inference
$$p(\theta|\mathbf{y}) = \frac{p(\mathbf{y}|\theta)\,p(\theta)}{p(\mathbf{y})} \propto p(\mathbf{y}|\theta)\,p(\theta)$$
- **Prior** $p(\theta)$: beliefs before data. Types: non-informative (large variance), weakly informative, informative.
- **Posterior** $p(\theta|\mathbf{y})$: updated belief after seeing data.
- **Marginal likelihood** (evidence): $p(\mathbf{y}) = \int p(\mathbf{y}|\theta)p(\theta)\,d\theta$ — normalising constant, often intractable.
- **Predictive distribution**: $p(y'|\mathbf{y}) = \int p(y'|\theta)p(\theta|\mathbf{y})\,d\theta$ — averages over parameter uncertainty.

### Maximum A Posteriori (MAP)
$$\hat{\theta}_{\text{MAP}} = \arg\max_{\theta}\,[\log p(\mathbf{y}|\theta) + \log p(\theta)]$$
- MAP ≠ full posterior; it is a point estimate at the posterior mode.
- The product $p(\mathbf{y}|\theta)p(\theta)$ is not a normalised density — cannot be used for probabilistic statements alone.

### Conjugate Priors
- A prior $p(\theta)$ is conjugate to a likelihood if the posterior is in the same family as the prior.
- **Beta–Binomial**: Beta prior + Binomial likelihood → Beta posterior (closed form).
- Advantages: closed-form posterior, avoids expensive integration, fast inference.

## Key takeaways
- Bayesian inference is about inferring a *distribution* over parameters, not a single value.
- MAP is a computationally cheap approximation to full Bayesian inference.
- When exact inference is unavailable, use: Laplace approximation, variational methods, MCMC.
- Formula sheet: Wk1 distribution formulas **will be given** in the exam.

## Exam relevance
- MLE derivation (univariate) is **examinable**.
- MAP derivation (univariate) via conjugate prior is **examinable**.
- Proving conjugacy is **examinable**.
- Predictive distribution: conceptual understanding required.
- Multivariate derivations are NOT examinable.

## Links to concepts
- [[mle]]: introduced here — MLE for Gaussian and Binomial
- [[map]]: introduced here — MAP as argmax of log-posterior
- [[bayesian-inference]]: core framework for the whole course
- [[conjugate-priors]]: Beta–Binomial example introduced here
- [[likelihood]]: defined here
