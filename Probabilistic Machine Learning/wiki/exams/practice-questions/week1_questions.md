# Week 1 Practice Questions — Bayesian Inference

**Scope:** MLE (Binomial, Gaussian univariate), MAP estimation (Gaussian with known variance), conjugate priors, Beta–Binomial posterior, Bayes' rule.
**Formula policy:** ✅ Distribution formulas (Gaussian pdf, Binomial pmf, Beta pdf) *will* be given in the exam.
**Derivation scope:** Univariate only. Multivariate / matrix derivations are NOT examinable.

---

## Conceptual / Bookwork

### Q1. Likelihood, prior, and posterior

**(a)** State Bayes' rule for parameter inference. Define each term — likelihood, prior, posterior, and marginal likelihood — and give the role of each in probabilistic inference. [4 marks]

**(b)** Explain why the marginal likelihood $p(\mathcal{D})$ can be dropped when computing the posterior up to proportionality, and why this is useful in practice. [2 marks]

**(c)** A student writes:
> "The product $p(\mathcal{D}|\theta)p(\theta)$ is our posterior distribution and can be used directly to make probability statements about $\theta$."

Identify the error in this statement and correct it. [2 marks]

---

### Q2. MLE vs MAP vs full Bayesian inference

**(a)** Compare MLE and MAP estimation. In what sense is MLE a special case of MAP? [3 marks]

**(b)** State one advantage of full Bayesian inference over MAP estimation. [1 mark]

**(c)** Describe what happens to the MAP estimate as the number of observations $n \to \infty$, and explain why this is expected. [2 marks]

---

### Q3. Conjugate priors

**(a)** Define a conjugate prior. State one key computational advantage of using a conjugate prior. [2 marks]

**(b)** For a Binomial likelihood, state the conjugate prior family and write down the posterior distribution, clearly showing how the prior hyperparameters are updated. [3 marks]

**(c)** Interpret the hyperparameters $\alpha$ and $\beta$ of a $\text{Beta}(\alpha, \beta)$ prior in terms of prior pseudo-counts. What does a $\text{Beta}(1, 1)$ prior represent? [2 marks]

**(d)** For a Gaussian likelihood with known variance, state the conjugate prior family for the mean. Write down the name of the posterior distribution family. [2 marks]

---

## Derivations

### Q4. MLE for a Gaussian (univariate, $\sigma^2$ known)

Let $y_1, y_2, \ldots, y_N$ be i.i.d. observations from $\mathcal{N}(\mu, \sigma^2)$, where $\sigma^2$ is known. ✅ *The Gaussian pdf will be given.*

**(a)** Write down the log-likelihood $\ell(\mu)$ for this model. You may leave $\sigma^2$ as a constant. [2 marks]

**(b)** Derive the MLE estimate $\hat{\mu}_{\text{MLE}}$ by differentiating the log-likelihood and setting the derivative to zero. Show all steps. [4 marks]

**(c)** Briefly justify that this stationary point is a maximum, not a minimum. [1 mark]

**(d)** Now suppose $\sigma^2$ is also unknown. State (without full re-derivation) the MLE estimate $\hat{\sigma}^2_{\text{MLE}}$. Comment on whether this estimate is biased or unbiased. [2 marks]

---

### Q5. MAP estimation for a Gaussian mean

Let $y_1, \ldots, y_n$ be i.i.d. observations from $\mathcal{N}(\mu, \sigma^2)$ with $\sigma^2$ known. Place a Gaussian prior on the mean: $\mu \sim \mathcal{N}(\mu_0, \sigma_0^2)$. ✅ *The Gaussian pdf will be given.*

**(a)** Write down the log-posterior $\log p(\mu | \mathbf{y})$ up to an additive constant, as a sum of the log-likelihood and log-prior terms. [2 marks]

**(b)** Differentiate with respect to $\mu$ and set the derivative to zero. Rearrange to solve for $\hat{\mu}_{\text{MAP}}$. Show all steps. [5 marks]

**(c)** Express $\hat{\mu}_{\text{MAP}}$ in the form of a weighted average of the sample mean $\bar{y}$ and the prior mean $\mu_0$, clearly stating the weights. [2 marks]

**(d)** Verify the two limiting cases: (i) $n = 0$; (ii) $n \to \infty$. State the intuition behind each. [2 marks]

---

## Practical / Calculation

### Q6. Binomial MLE — coin flipping

A coin is flipped 20 times and 14 heads are observed. Let $\theta$ denote the probability of heads. ✅ *The Binomial pmf will be given.*

**(a)** Write down the log-likelihood $\ell(\theta)$ for this model. You may ignore additive constants that do not depend on $\theta$. [2 marks]

**(b)** Derive the MLE estimate $\hat{\theta}_{\text{MLE}}$ for this specific dataset. Show your working. [3 marks]

**(c)** Compute the log-likelihood at $\theta = 0.5$ and at $\hat{\theta}_{\text{MLE}}$. Which is larger, and why is this expected? [2 marks]

---

### Q7. Beta–Binomial posterior updating

A coin is flipped $n = 10$ times and $y = 3$ heads are observed. A Beta prior $\theta \sim \text{Beta}(2, 2)$ is placed on the probability of heads. ✅ *The Beta pdf and Binomial pmf will be given.*

**(a)** Write down the posterior distribution $p(\theta | y)$ using conjugacy. State the updated hyperparameters explicitly. [3 marks]

**(b)** Compute the posterior mean $\mathbb{E}[\theta | y]$. [1 mark]

**(c)** Compute the MLE estimate $\hat{\theta}_{\text{MLE}}$. Compare it to the posterior mean and explain the difference in terms of the role of the prior. [3 marks]

**(d)** Suppose the experiment is repeated and an additional 10 flips yield 6 heads (so cumulatively: $n_{\text{total}} = 20$ flips, $y_{\text{total}} = 9$ heads). Update the posterior from part **(a)** to incorporate this new data. State the final posterior distribution. [2 marks]

---

### Q8. MAP for a Gaussian mean — numerical

A researcher observes the following five measurements:
$$y = (2.0,\ 3.5,\ 2.5,\ 4.0,\ 3.0)$$
She models them as i.i.d. $\mathcal{N}(\mu, \sigma^2)$ with known variance $\sigma^2 = 1$. Her prior belief is $\mu \sim \mathcal{N}(3.5,\ \sigma_0^2 = 0.25)$. ✅ *The Gaussian pdf will be given.*

**(a)** Compute the sample mean $\bar{y}$. [1 mark]

**(b)** Using the MAP formula:
$$\hat{\mu}_{\text{MAP}} = \frac{n\sigma_0^2}{n\sigma_0^2 + \sigma^2}\,\bar{y} + \frac{\sigma^2}{n\sigma_0^2 + \sigma^2}\,\mu_0$$
compute $\hat{\mu}_{\text{MAP}}$. Show your arithmetic clearly. [3 marks]

**(c)** Compute the MLE estimate $\hat{\mu}_{\text{MLE}}$. Is $\hat{\mu}_{\text{MAP}}$ closer to $\bar{y}$ or to $\mu_0$? Explain why, given the relative values of $\sigma^2$ and $n\sigma_0^2$. [3 marks]

---

## Answers / Mark Schemes

---

### A1. Likelihood, prior, and posterior

**(a)** Bayes' rule:
$$p(\theta|\mathcal{D}) = \frac{p(\mathcal{D}|\theta)\,p(\theta)}{p(\mathcal{D})}$$

| Term | Role |
|---|---|
| $p(\mathcal{D}\|\theta)$ — **Likelihood** | Probability of the data given parameters; measures how well $\theta$ explains the observations |
| $p(\theta)$ — **Prior** | Beliefs about $\theta$ before seeing data; encodes domain knowledge |
| $p(\theta\|\mathcal{D})$ — **Posterior** | Updated distribution over $\theta$ after observing $\mathcal{D}$ |
| $p(\mathcal{D}) = \int p(\mathcal{D}\|\theta)p(\theta)\,d\theta$ — **Marginal likelihood / evidence** | Normalising constant; ensures posterior integrates to 1 |

*[1 mark: correct statement of Bayes' rule; 3 marks: one mark per term correctly defined]*

**(b)** Because $p(\mathcal{D})$ does not depend on $\theta$, it is a constant with respect to the parameter. Therefore:
$$p(\theta|\mathcal{D}) \propto p(\mathcal{D}|\theta)\,p(\theta)$$
This is practically important because computing $p(\mathcal{D}) = \int p(\mathcal{D}|\theta)p(\theta)\,d\theta$ is usually analytically intractable; dropping it allows inference without evaluating the integral. *[2 marks]*

**(c)** The error is that $p(\mathcal{D}|\theta)p(\theta)$ is an **unnormalised** quantity — it does not integrate to 1 over $\theta$, so it is NOT a probability distribution and cannot be used directly for probabilistic statements. The correct posterior requires dividing by $p(\mathcal{D})$. The MAP estimate (the mode of the unnormalised product) is valid as an optimiser but the product itself is not a probability distribution. *[1 mark: identifying error; 1 mark: correct explanation]*

---

### A2. MLE vs MAP vs full Bayesian inference

**(a)** MLE finds $\hat{\theta} = \arg\max_\theta p(\mathcal{D}|\theta)$ — it treats $\theta$ as fixed and unknown and uses only the likelihood. MAP finds $\hat{\theta} = \arg\max_\theta [p(\mathcal{D}|\theta)p(\theta)]$ — it incorporates a prior as an additional term. MLE is a special case of MAP with a **flat (uniform) prior**: when $p(\theta) = \text{const}$, the log-prior contributes nothing to the objective and MAP reduces to MLE. *[3 marks]*

**(b)** Full Bayesian inference returns the entire posterior distribution $p(\theta|\mathcal{D})$, which provides uncertainty quantification (credible intervals, posterior predictive distributions). MAP returns only a single point estimate with no measure of uncertainty. *[1 mark: any valid advantage, e.g., posterior predictive, credible intervals, model checking]*

**(c)** As $n \to \infty$, $\hat{\theta}_{\text{MAP}} \to \hat{\theta}_{\text{MLE}}$ (the sample mean for Gaussian, or the sample proportion for Binomial). The intuition is that the likelihood term grows with $n$ while the log-prior remains fixed, so the prior is eventually "washed out" by the data. *[1 mark: correct limit; 1 mark: correct intuition]*

---

### A3. Conjugate priors

**(a)** A prior $p(\theta)$ is **conjugate** to a likelihood $p(\mathcal{D}|\theta)$ if the resulting posterior $p(\theta|\mathcal{D})$ belongs to the **same parametric family** as the prior. Key advantage: the posterior is available in **closed form** — no numerical integration required; inference reduces to a simple hyperparameter update. *[1 mark: definition; 1 mark: advantage]*

**(b)** Conjugate prior for a Binomial likelihood: **Beta distribution**. Starting from $\theta \sim \text{Beta}(\alpha, \beta)$ and observing $y$ heads in $n$ trials:
$$\theta | y \sim \text{Beta}(\alpha + y,\; \beta + (n - y))$$
The $\alpha$ parameter is incremented by the number of observed successes; $\beta$ is incremented by the number of observed failures. *[1 mark: correct prior family; 2 marks: correct posterior with update rule shown]*

**(c)** $\alpha$ acts as a prior count of **successes** (heads); $\beta$ acts as a prior count of **failures** (tails). Together $\alpha + \beta$ represents the "prior sample size" — how confident the prior is. A $\text{Beta}(1, 1)$ is a **uniform prior**: every value of $\theta \in [0, 1]$ is equally likely before seeing data. *[1 mark: pseudo-count interpretation; 1 mark: Beta(1,1) = uniform]*

**(d)** For a Gaussian likelihood with known variance, the conjugate prior for $\mu$ is a **Gaussian (Normal) distribution**. The posterior is also Gaussian. *[1 mark each]*

---

### A4. MLE for a Gaussian (univariate, $\sigma^2$ known)

**(a)** The log-likelihood for $N$ i.i.d. observations is:
$$\ell(\mu) = \sum_{i=1}^N \log p(y_i|\mu, \sigma^2) = -\frac{N}{2}\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}\sum_{i=1}^N (y_i - \mu)^2$$
Since the first term does not depend on $\mu$, the effective objective is:
$$\ell(\mu) \propto -\frac{1}{2\sigma^2}\sum_{i=1}^N (y_i - \mu)^2$$
*[1 mark: correct form; 1 mark: identifying the constant term]*

**(b)** Differentiating with respect to $\mu$:
$$\frac{d\ell}{d\mu} = \frac{1}{\sigma^2}\sum_{i=1}^N (y_i - \mu) = \frac{1}{\sigma^2}\left(\sum_{i=1}^N y_i - N\mu\right)$$
Setting to zero:
$$\sum_{i=1}^N y_i - N\mu = 0$$
$$N\mu = \sum_{i=1}^N y_i$$
$$\boxed{\hat{\mu}_{\text{MLE}} = \frac{1}{N}\sum_{i=1}^N y_i}$$
*[1 mark: correct derivative; 1 mark: setting to zero; 2 marks: correct algebraic solution]*

**(c)** The second derivative is $\frac{d^2\ell}{d\mu^2} = -\frac{N}{\sigma^2} < 0$, confirming the stationary point is a maximum. *[1 mark]*

**(d)** The MLE for the variance is:
$$\hat{\sigma}^2_{\text{MLE}} = \frac{1}{N}\sum_{i=1}^N (y_i - \hat{\mu})^2$$
This estimate is **biased**: it divides by $N$ rather than $N-1$ (the unbiased sample variance). On average it underestimates the true population variance. *[1 mark: correct formula; 1 mark: biased, correct explanation]*

---

### A5. MAP estimation for a Gaussian mean

**(a)** By Bayes' rule, $\log p(\mu|\mathbf{y}) \propto \log p(\mathbf{y}|\mu) + \log p(\mu)$. Dropping constants:
$$\log p(\mu|\mathbf{y}) \propto -\frac{1}{2\sigma^2}\sum_{i=1}^n(y_i - \mu)^2 - \frac{1}{2\sigma_0^2}(\mu - \mu_0)^2$$
*[1 mark: correct structure; 1 mark: both terms correctly written]*

**(b)** Differentiating with respect to $\mu$:
$$\frac{\partial}{\partial\mu}\log p(\mu|\mathbf{y}) = \frac{1}{\sigma^2}\left(\sum_{i=1}^n y_i - n\mu\right) + \frac{\mu_0 - \mu}{\sigma_0^2}$$
Setting to zero:
$$\frac{1}{\sigma^2}\sum_{i=1}^n y_i - \frac{n\mu}{\sigma^2} + \frac{\mu_0}{\sigma_0^2} - \frac{\mu}{\sigma_0^2} = 0$$
Collecting $\mu$ terms on the left:
$$\mu\left(\frac{n}{\sigma^2} + \frac{1}{\sigma_0^2}\right) = \frac{1}{\sigma^2}\sum_{i=1}^n y_i + \frac{\mu_0}{\sigma_0^2}$$
$$\boxed{\hat{\mu}_{\text{MAP}} = \frac{\frac{1}{\sigma^2}\sum_{i=1}^n y_i + \frac{\mu_0}{\sigma_0^2}}{\frac{n}{\sigma^2} + \frac{1}{\sigma_0^2}}}$$
*[1 mark: correct derivatives; 2 marks: correct rearrangement; 1 mark: solving for $\mu$; 1 mark: correct final expression]*

**(c)** Multiplying numerator and denominator by $\frac{\sigma^2\sigma_0^2}{n\sigma_0^2 + \sigma^2}$:
$$\hat{\mu}_{\text{MAP}} = \underbrace{\frac{n\sigma_0^2}{n\sigma_0^2 + \sigma^2}}_{\text{weight on }\bar{y}}\,\bar{y} + \underbrace{\frac{\sigma^2}{n\sigma_0^2 + \sigma^2}}_{\text{weight on }\mu_0}\,\mu_0$$
where $\bar{y} = \frac{1}{n}\sum_{i=1}^n y_i$. Note the weights sum to 1. *[1 mark: weighted average form; 1 mark: correct weights stated]*

**(d)**
- **(i)** $n = 0$: both the weight on $\bar{y}$ → 0 and weight on $\mu_0$ → 1, so $\hat{\mu}_{\text{MAP}} = \mu_0$. Intuition: with no data, the estimate equals the prior belief.
- **(ii)** $n \to \infty$: weight on $\bar{y}$ → 1, weight on $\mu_0$ → 0, so $\hat{\mu}_{\text{MAP}} \to \bar{y} = \hat{\mu}_{\text{MLE}}$. Intuition: with infinite data, the prior becomes negligible and the estimate equals the sample mean. *[1 mark per limiting case with intuition]*

---

### A6. Binomial MLE — coin flipping

**(a)** With $y = 14$ heads in $n = 20$ flips, the log-likelihood is:
$$\ell(\theta) = y\log\theta + (n - y)\log(1 - \theta) + \text{const} = 14\log\theta + 6\log(1-\theta) + \text{const}$$
(The $\log\binom{n}{y}$ term does not depend on $\theta$ and is treated as a constant.) *[2 marks]*

**(b)** Differentiating:
$$\frac{d\ell}{d\theta} = \frac{14}{\theta} - \frac{6}{1 - \theta}$$
Setting to zero:
$$\frac{14}{\theta} = \frac{6}{1-\theta} \implies 14(1-\theta) = 6\theta \implies 14 = 20\theta$$
$$\boxed{\hat{\theta}_{\text{MLE}} = \frac{14}{20} = 0.7}$$
*[1 mark: correct derivative; 1 mark: setting to zero and rearranging; 1 mark: correct answer]*

**(c)** At $\theta = 0.5$:
$$\ell(0.5) = 14\log(0.5) + 6\log(0.5) = 20\log(0.5) \approx 20 \times (-0.693) = -13.86$$
At $\hat{\theta}_{\text{MLE}} = 0.7$:
$$\ell(0.7) = 14\log(0.7) + 6\log(0.3) \approx 14\times(-0.357) + 6\times(-1.204) = -5.00 - 7.22 = -12.22$$
$\ell(0.7) > \ell(0.5)$, as expected: the MLE is defined as the parameter that **maximises** the log-likelihood, so no other value can give a higher log-likelihood. *[1 mark: correct computations; 1 mark: correct explanation]*

---

### A7. Beta–Binomial posterior updating

**(a)** Prior: $\theta \sim \text{Beta}(\alpha, \beta) = \text{Beta}(2, 2)$. Observed: $y = 3$ heads, $n - y = 7$ tails. By conjugacy:
$$\theta | y \sim \text{Beta}(\alpha + y,\; \beta + (n - y)) = \text{Beta}(2 + 3,\; 2 + 7) = \text{Beta}(5, 9)$$
*[2 marks: correct update; 1 mark: explicit hyperparameter values]*

**(b)** Posterior mean:
$$\mathbb{E}[\theta | y] = \frac{\alpha'}{\alpha' + \beta'} = \frac{5}{5 + 9} = \frac{5}{14} \approx 0.357$$
*[1 mark]*

**(c)** $\hat{\theta}_{\text{MLE}} = \frac{y}{n} = \frac{3}{10} = 0.3$. The posterior mean ($\approx 0.357$) is pulled away from the MLE toward the prior mean. The prior $\text{Beta}(2,2)$ has mean $\frac{2}{4} = 0.5$, so it acts as a regulariser, pulling the estimate toward 0.5. With only 10 flips the prior has a noticeable effect; as $n \to \infty$ the posterior mean would converge to the MLE. *[1 mark: MLE; 1 mark: comparison; 1 mark: explanation of prior regularisation]*

**(d)** The posterior after the first experiment, $\text{Beta}(5, 9)$, becomes the new prior for the second experiment ($y_2 = 6$ heads, $n_2 - y_2 = 4$ tails):
$$\theta | y_{\text{total}} \sim \text{Beta}(5 + 6,\; 9 + 4) = \text{Beta}(11, 13)$$
(Equivalently: starting from the original prior $\text{Beta}(2,2)$ with cumulative data $y_{\text{total}} = 9$, $n_{\text{total}} = 20$: $\text{Beta}(2+9, 2+11) = \text{Beta}(11, 13)$.) *[2 marks: correct final posterior; method must be shown]*

---

### A8. MAP for a Gaussian mean — numerical

**(a)** $\bar{y} = \frac{2.0 + 3.5 + 2.5 + 4.0 + 3.0}{5} = \frac{15.0}{5} = 3.0$ *[1 mark]*

**(b)** Given: $n = 5$, $\sigma^2 = 1$, $\sigma_0^2 = 0.25$, $\bar{y} = 3.0$, $\mu_0 = 3.5$.

Compute the weights:
$$n\sigma_0^2 = 5 \times 0.25 = 1.25$$
$$n\sigma_0^2 + \sigma^2 = 1.25 + 1 = 2.25$$
$$w_{\bar{y}} = \frac{1.25}{2.25} = \frac{5}{9} \approx 0.556 \qquad w_{\mu_0} = \frac{1}{2.25} = \frac{4}{9} \approx 0.444$$

$$\hat{\mu}_{\text{MAP}} = \frac{5}{9} \times 3.0 + \frac{4}{9} \times 3.5 = \frac{15.0}{9} + \frac{14.0}{9} = \frac{29.0}{9} \approx 3.22$$
*[1 mark: correct weight computation; 1 mark: correct arithmetic; 1 mark: correct final answer]*

**(c)** $\hat{\mu}_{\text{MLE}} = \bar{y} = 3.0$. The MAP estimate (3.22) lies between $\bar{y} = 3.0$ and $\mu_0 = 3.5$, and is closer to $\bar{y}$. Since $n\sigma_0^2 = 1.25 > \sigma^2 = 1$, the data weight ($\approx 0.556$) exceeds the prior weight ($\approx 0.444$), so the MAP is pulled more toward the sample mean than the prior mean. If $\sigma^2$ were larger or $n$ smaller, the prior would dominate more. *[1 mark: MLE; 1 mark: closer to $\bar{y}$ with reasoning; 1 mark: comparing $n\sigma_0^2$ vs $\sigma^2$]*
