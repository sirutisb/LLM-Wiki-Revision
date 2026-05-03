# Supp — Beta-Binomial Conjugate Model

**File:** `raw/text/COM3031_W1_Beta_Binomial.txt`
**Type:** supplementary-note
**Week:** 1
**Concepts introduced:** [[conjugate-priors]], [[bayesian-inference]]

## Summary
Derives the posterior distribution for the coin-flip (Binomial likelihood + Beta prior) model, demonstrating Bayesian conjugacy: the posterior is Beta with updated parameters. Shows that posterior inference reduces to a simple parameter update — no optimisation or integration required.

## Key content

### Model
- Likelihood: $p(y|\theta) = \binom{n}{y}\theta^y(1-\theta)^{n-y}$ (Binomial).
- Prior: $\theta \sim \text{Beta}(\alpha, \beta)$, with $p(\theta) = \frac{\theta^{\alpha-1}(1-\theta)^{\beta-1}}{B(\alpha,\beta)}$.

### Posterior (Conjugacy)
By Bayes' rule, ignoring constants w.r.t. $\theta$:
$$p(\theta|y) \propto \theta^y(1-\theta)^{n-y} \cdot \theta^{\alpha-1}(1-\theta)^{\beta-1} = \theta^{(\alpha+y)-1}(1-\theta)^{(\beta+n-y)-1}$$
This is proportional to $\text{Beta}(\alpha', \beta')$ with:
$$\alpha' = \alpha + y, \qquad \beta' = \beta + (n - y)$$

### Posterior Mean
$$\mathbb{E}[\theta|y] = \frac{\alpha'}{\alpha'+\beta'} = \frac{\alpha + y}{\alpha + \beta + n}$$

### Interpretation
- Prior counts: $\alpha$ = prior "heads", $\beta$ = prior "tails".
- Posterior: add observed heads and tails to prior counts.
- Posterior mean interpolates between prior mean $\frac{\alpha}{\alpha+\beta}$ and MLE $\frac{y}{n}$.
- As $n \to \infty$, posterior mean $\to$ MLE; prior is overwhelmed by data.

## Exam notes
- Must know how to derive the posterior (identify functional form, match to Beta). ⚠️
- Proof of conjugacy: show posterior has same functional form as prior. ⚠️
- Formula sheet: Beta pdf **will be given** (Week 1).

## Links to concepts
- [[conjugate-priors]]: this is the canonical conjugate pair example
- [[bayesian-inference]]: Bayesian inference by parameter update
- [[mle]]: MLE limit when $n \to \infty$
