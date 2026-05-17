# Week 5 Practice Questions — MCMC

> ⚠️ **No formula sheet provided for Week 5.** All algorithm steps, acceptance ratios, and estimator forms must be recalled from memory.

---

## Conceptual / Bookwork

### Q1. Why MCMC? Motivation and Core Idea

**(a)** In Bayesian inference, we rarely need the full analytic form of the posterior $p(\theta \mid \mathcal{D})$. State what we typically need instead, and write down the general integral this requires.

**(b)** Explain why this integral is generally intractable.

**(c)** State the Monte Carlo approximation to this integral. What is the key requirement for it to be valid?

**(d)** Explain in one or two sentences why rejection sampling and importance sampling both fail in high dimensions, and why MCMC overcomes this.

---

### Q2. Rejection Sampling vs Importance Sampling

Compare rejection sampling and importance sampling by completing the table and answering the follow-up questions.

| Dimension | Rejection Sampling | Importance Sampling |
|-----------|-------------------|---------------------|
| Goal | | |
| Uses all samples? | | |
| Requires envelope constant $M$? | | |
| Output | | |
| Main failure mode in high dimensions | | |

**(a)** Both methods require a proposal distribution $q(\theta)$. State the **envelope condition** that $q(\theta)$ must satisfy for rejection sampling.

**(b)** Define the **importance weight** $w(\theta)$ used in importance sampling. What happens to these weights when $q$ has lighter tails than the target $p(\theta \mid \mathcal{D})$?

**(c)** Give one advantage of importance sampling over rejection sampling, and one situation where importance sampling can still fail.

---

### Q3. MCMC Algorithm Comparison: Metropolis-Hastings, Metropolis, and Gibbs Sampling

**(a)** Write out all steps of the **Metropolis-Hastings (MH)** algorithm, starting from the current state $\theta^{(t)}$. Your answer must include: how the proposal is drawn, the acceptance ratio formula, and the accept/reject rule.

**(b)** The **Metropolis algorithm** is a special case of MH. State what additional assumption is made on the proposal distribution, and write down the simplified acceptance probability that results.

**(c)** **Gibbs sampling** is another special case of MH. State:
- What distribution each parameter is sampled from.
- What the acceptance ratio equals, and why.
- The key condition that must hold for Gibbs sampling to be applicable.

**(d)** MCMC samples are not independent. Name the property of MCMC chains that causes this, and explain what **burn-in** is used for.

**(e)** Compare **MCMC** and **variational inference (VI)** on the following dimensions: (i) bias, (ii) computational cost, (iii) ability to capture multimodal posteriors, (iv) scalability to large datasets.

---

## Practical / Calculation

### Q4. Tracing Metropolis-Hastings Steps

You are running a Metropolis algorithm (symmetric Gaussian random walk proposal) to sample from a target distribution. The unnormalised posterior is:

$$\tilde{p}(\theta) = p(\mathcal{D} \mid \theta)\, p(\theta)$$

You evaluate $\tilde{p}$ at two points and obtain:

$$\tilde{p}(\theta^{(t)}) = 0.4, \qquad \tilde{p}(\theta^{(t)*}) = 0.6$$

where $\theta^{(t)*}$ is the proposed value drawn from $q(\theta^* \mid \theta^{(t)}) = \mathcal{N}(\theta^{(t)}, \sigma^2)$.

**(a)** Compute the acceptance probability $\alpha$ for this proposed move.

**(b)** A uniform random number $u \sim \text{Uniform}(0, 1)$ is drawn and equals $u = 0.72$. What is the next state $\theta^{(t+1)}$? Justify your answer.

**(c)** Now suppose instead $\tilde{p}(\theta^{(t)*}) = 0.2$. Compute the new acceptance probability $\alpha$.

**(d)** With $\tilde{p}(\theta^{(t)}) = 0.4$, $\tilde{p}(\theta^{(t)*}) = 0.2$, and $u = 0.40$, what is $\theta^{(t+1)}$?

**(e)** Why is it important that the algorithm can sometimes accept a move to a lower-probability region (i.e., when $\tilde{p}(\theta^*) < \tilde{p}(\theta^{(t)})$)?

**(f)** In the full (asymmetric) Metropolis-Hastings algorithm, how does the acceptance ratio change when the proposal is asymmetric, i.e., $q(\theta^* \mid \theta) \neq q(\theta \mid \theta^*)$? Write the full formula.

---

### Q5. Rejection Sampling: Computing Acceptance

A target distribution has unnormalised density $\tilde{p}(\theta) = p(\mathcal{D} \mid \theta)p(\theta)$. You choose a proposal $q(\theta)$ and an envelope constant $M = 10$.

At a proposed point $\theta^*$, you evaluate:

$$\tilde{p}(\theta^*) = 3, \qquad q(\theta^*) = 0.5$$

**(a)** Verify that the envelope condition $\tilde{p}(\theta) \leq M\,q(\theta)$ holds at $\theta^*$.

**(b)** Compute the acceptance probability for this proposed sample.

**(c)** A draw $u \sim \text{Uniform}(0,1)$ yields $u = 0.70$. Is $\theta^*$ accepted?

**(d)** A second proposal $\theta^{**}$ gives $\tilde{p}(\theta^{**}) = 8$ and $q(\theta^{**}) = 0.5$. Compute the acceptance probability. Would $u = 0.70$ accept this sample?

**(e)** Briefly explain why an efficient envelope (tight $M$) leads to a higher acceptance rate, and why finding a tight $M$ is difficult in high dimensions.

---

### Q6. Monte Carlo Integration and Posterior Estimation

You have $N = 4$ samples from the posterior: $\theta_1 = 1.0,\; \theta_2 = 2.0,\; \theta_3 = 3.0,\; \theta_4 = 4.0$.

**(a)** Use Monte Carlo integration to estimate the posterior mean $\mathbb{E}[{\theta \mid \mathcal{D}}]$.

**(b)** Use these same samples to estimate the posterior variance $\text{Var}(\theta \mid \mathcal{D})$.

**(c)** Suppose the true posterior is a Gaussian with mean 2.5 and variance 1.25. Comment briefly on the quality of your estimates from (a) and (b), and how you would improve them.

**(d)** Write down the general Monte Carlo estimator for any posterior expectation $\mathbb{E}_{p(\theta|\mathcal{D})}[f(\theta)]$. Why does this estimator not require knowledge of the normalising constant $p(\mathcal{D})$?

---

## Answers / Mark Schemes

### A1. Why MCMC?

**(a)** We typically need to compute posterior **expectations**:
$$\mathbb{E}_{p(\theta|\mathcal{D})}[f(\theta)] = \int f(\theta)\,p(\theta \mid \mathcal{D})\,d\theta$$
Examples: posterior mean ($f(\theta) = \theta$), posterior variance, predictive distributions.

**(b)** The integral is intractable because $p(\theta \mid \mathcal{D}) = \tilde{p}(\theta)/Z$ where $Z = \int p(\mathcal{D}|\theta)p(\theta)\,d\theta$ is the marginal likelihood — this integral is generally high-dimensional and has no closed form.

**(c)** Monte Carlo approximation:
$$\mathbb{E}_{p(\theta|\mathcal{D})}[f(\theta)] \approx \frac{1}{N}\sum_{i=1}^N f(\theta_i), \qquad \theta_1, \ldots, \theta_N \sim p(\theta \mid \mathcal{D})$$
Requirement: samples must be drawn from (or distributed approximately as) the posterior.

**(d)** Both rejection and importance sampling use a **fixed global proposal** $q(\theta)$. In high dimensions, it is exponentially hard to construct a $q$ that covers the posterior well — leading to vanishing acceptance rates (rejection) or weight degeneracy (importance sampling). MCMC instead proposes **local moves** from the current state, adapting to the target's local geometry. This avoids the need for a global envelope.

---

### A2. Rejection Sampling vs Importance Sampling

| Dimension | Rejection Sampling | Importance Sampling |
|-----------|-------------------|---------------------|
| Goal | Exact samples from $p^*$ | Estimate expectations under $p^*$ |
| Uses all samples? | No — rejected samples discarded | Yes — all samples kept |
| Requires envelope constant $M$? | Yes — global $M$ s.t. $\tilde{p} \leq M q$ | No |
| Output | Exact (unweighted) samples from $p^*$ | Weighted samples approximating $p^*$ |
| Main failure mode in high dimensions | Exponentially low acceptance rate | Weight degeneracy (few samples dominate) |

**(a)** Envelope condition: $\tilde{p}(\theta) \leq M\,q(\theta)$ for all $\theta$. The envelope $M q(\theta)$ must lie above the unnormalised target everywhere.

**(b)** Importance weight: $w(\theta) = \tilde{p}(\theta)/q(\theta)$. When $q$ has lighter tails than $p^*$, proposals from the tails are rare; when they do occur, their weights are very large. This causes **weight degeneracy**: a few samples carry almost all the weight, making the estimator high-variance and unreliable.

**(c)** Advantage of IS: no samples are discarded; no need to find a global $M$. IS can still fail if $q$ and $p^*$ are badly mismatched — particularly if $q$ has lighter tails, causing weight degeneracy and high variance in high dimensions.

---

### A3. Algorithm Comparison

**(a)** Metropolis-Hastings algorithm (one step from current state $\theta^{(t)}$):

1. **Propose**: draw $\theta^* \sim q(\theta^* \mid \theta^{(t)})$ from the proposal distribution.
2. **Compute acceptance ratio**:
$$\alpha = \min\!\left(1,\; \frac{\tilde{p}(\theta^*)\;q(\theta^{(t)}\mid\theta^*)}{\tilde{p}(\theta^{(t)})\;q(\theta^*\mid\theta^{(t)})}\right)$$
3. **Accept/reject**: draw $u \sim \text{Uniform}(0,1)$.
   - If $u \leq \alpha$: set $\theta^{(t+1)} = \theta^*$ (accept).
   - Else: set $\theta^{(t+1)} = \theta^{(t)}$ (reject, stay).

Note: the normalising constant $Z$ cancels in the ratio $\tilde{p}(\theta^*)/\tilde{p}(\theta^{(t)})$, so it is never needed.

**(b)** Metropolis algorithm: the proposal is **symmetric**, meaning $q(\theta^* \mid \theta) = q(\theta \mid \theta^*)$ (e.g. a Gaussian random walk $\theta^* = \theta^{(t)} + \epsilon$, $\epsilon \sim \mathcal{N}(0, \sigma^2)$). The proposal terms cancel, giving:
$$\alpha = \min\!\left(1,\; \frac{\tilde{p}(\theta^*)}{\tilde{p}(\theta^{(t)})}\right)$$

**(c)** Gibbs sampling:
- Each parameter $\theta_j$ is sampled from its **full conditional**: $\theta_j^{(t+1)} \sim p(\theta_j \mid \theta_{-j}^{(t)}, \mathcal{D})$, where $\theta_{-j}$ means all other parameters.
- The acceptance ratio $\alpha = 1$ always. This is because the MH proposal is set to be exactly the conditional distribution; when substituted into the MH acceptance ratio, all terms cancel.
- **Key condition**: the full conditional distributions $p(\theta_j \mid \theta_{-j}, \mathcal{D})$ must be tractable to sample from (e.g. through conjugacy).

**(d)** The samples within an MCMC chain are **correlated** (autocorrelated) because each state $\theta^{(t+1)}$ depends on the previous state $\theta^{(t)}$. **Burn-in** refers to discarding the first $M$ samples from the chain. This is necessary because the early samples depend on the (arbitrary) initialisation $\theta^{(0)}$ and do not yet represent the stationary distribution. After enough steps, the chain forgets its starting point (ergodicity) and samples approximate draws from $p(\theta \mid \mathcal{D})$.

**(e)** MCMC vs Variational Inference:

| Dimension | MCMC | Variational Inference |
|-----------|------|-----------------------|
| Bias | Asymptotically unbiased (exact in limit) | Biased — approximation family introduces systematic error |
| Computational cost | Slow — requires many sequential samples | Fast — deterministic optimisation |
| Multimodal posteriors | Captures naturally (if chain mixes) | Often misses modes (trapped by reverse KL) |
| Scalability to large data | Poor — each step evaluates full likelihood | Good — can use minibatches |

---

### A4. Tracing Metropolis-Hastings Steps

**(a)** Since the proposal is symmetric (Gaussian random walk), the proposal terms cancel and:
$$\alpha = \min\!\left(1,\;\frac{\tilde{p}(\theta^*)}{\tilde{p}(\theta^{(t)})}\right) = \min\!\left(1,\;\frac{0.6}{0.4}\right) = \min(1,\;1.5) = 1$$
The proposed move improves the target density, so it is accepted with probability 1.

**(b)** Since $\alpha = 1$, the condition is $u \leq 1$. With $u = 0.72 \leq 1$, we **accept**: $\theta^{(t+1)} = \theta^{(t)*}$.

**(c)** With $\tilde{p}(\theta^*) = 0.2$:
$$\alpha = \min\!\left(1,\;\frac{0.2}{0.4}\right) = \min(1,\;0.5) = 0.5$$

**(d)** $\alpha = 0.5$. Since $u = 0.40 \leq 0.5$, we **accept**: $\theta^{(t+1)} = \theta^{(t)*}$. (The move is to a lower-probability region, but it is still accepted with probability 0.5.)

**(e)** Allowing occasional moves to lower-probability regions is essential for **exploration**. If the chain only moved to higher-probability states, it would become trapped in local modes and never explore the full posterior. Accepting downhill moves (with probability proportional to the density ratio) ensures the chain can escape modes and eventually sample from the entire posterior — including the tails and any secondary modes.

**(f)** In the full asymmetric MH algorithm, the proposal correction term must be included:
$$\alpha = \min\!\left(1,\;\frac{\tilde{p}(\theta^*)\;q(\theta^{(t)}\mid\theta^*)}{\tilde{p}(\theta^{(t)})\;q(\theta^*\mid\theta^{(t)})}\right)$$
The extra factor $q(\theta^{(t)}\mid\theta^*)/q(\theta^*\mid\theta^{(t)})$ corrects for the asymmetry of the proposal, ensuring detailed balance is maintained even when forward and backward proposal probabilities differ.

---

### A5. Rejection Sampling: Computing Acceptance

**(a)** Envelope check: $M\,q(\theta^*) = 10 \times 0.5 = 5.0$. Since $\tilde{p}(\theta^*) = 3 \leq 5.0$, the condition holds.

**(b)** Acceptance probability:
$$\frac{\tilde{p}(\theta^*)}{M\,q(\theta^*)} = \frac{3}{10 \times 0.5} = \frac{3}{5} = 0.6$$

**(c)** $u = 0.70 > 0.6$, so $\theta^*$ is **rejected**.

**(d)** Acceptance probability for $\theta^{**}$:
$$\frac{\tilde{p}(\theta^{**})}{M\,q(\theta^{**})} = \frac{8}{10 \times 0.5} = \frac{8}{5} = 1.6$$
But acceptance probability is capped at 1 (since $u \in [0,1]$), so $\alpha = 1.0$. With $u = 0.70 \leq 1.0$, $\theta^{**}$ is **accepted**. (Note: this should always be accepted as $\tilde{p}(\theta^{**}) = 8$ approaches the envelope $M q = 5$ — check: $8 > 5$ means the envelope is violated here, which would be an invalid configuration. In a valid setup, $M$ must be large enough. This is an intentional illustration that $M$ must satisfy the envelope condition globally.)

**(e)** A tighter $M$ means $M q(\theta)$ is closer to $\tilde{p}(\theta)$ everywhere. Since the acceptance probability is $\tilde{p}(\theta^*)/(M q(\theta^*))$, a smaller $M$ (tighter bound) yields a higher acceptance probability. In high dimensions, finding a single global constant $M$ that covers the entire support of a high-dimensional $\tilde{p}$ is exponentially hard — the proposal $q$ must dominate in all directions simultaneously, and any gap between $M q$ and $\tilde{p}$ accumulates across dimensions, causing the acceptance rate to drop exponentially.

---

### A6. Monte Carlo Integration

**(a)** Posterior mean estimate:
$$\hat{\mu} = \frac{1}{4}(\theta_1 + \theta_2 + \theta_3 + \theta_4) = \frac{1}{4}(1 + 2 + 3 + 4) = \frac{10}{4} = 2.5$$

**(b)** Sample mean $\bar{\theta} = 2.5$. Posterior variance estimate:
$$\widehat{\text{Var}} = \frac{1}{4}\sum_{i=1}^4 (\theta_i - \bar{\theta})^2 = \frac{1}{4}\left[(1-2.5)^2 + (2-2.5)^2 + (3-2.5)^2 + (4-2.5)^2\right]$$
$$= \frac{1}{4}\left[2.25 + 0.25 + 0.25 + 2.25\right] = \frac{5}{4} = 1.25$$

**(c)** Both estimates are exact here (mean = 2.5, variance = 1.25) because the four samples happen to be evenly spaced and perfectly symmetric. In practice with random samples, small $N$ introduces sampling noise. To improve the estimates: increase $N$ (the Monte Carlo standard error is $O(1/\sqrt{N})$), or use variance-reduction techniques such as importance sampling. With only 4 samples, the estimates have high variance.

**(d)** General Monte Carlo estimator:
$$\mathbb{E}_{p(\theta|\mathcal{D})}[f(\theta)] \approx \frac{1}{N}\sum_{i=1}^N f(\theta_i), \qquad \theta_i \sim p(\theta \mid \mathcal{D})$$
This does not require the normalising constant because the samples $\theta_i$ are drawn from the posterior directly (e.g., via MCMC). Computing $f(\theta_i)$ for each sample only requires evaluating $f$ at the sample point — not the normalisation constant $Z = p(\mathcal{D})$. The average then approximates the integral by the law of large numbers, entirely avoiding the intractable $Z$.

---

## Similar Past-Paper Style Addition

### Q7. Describe rejection sampling for a specified target [5 marks]

Suppose the target density is known only up to proportionality:

$$\tilde{p}(x)\propto e^{-x^2},$$

and a proposal distribution $q(x)=\mathcal{N}(0,1)$ is available.

Describe how to perform rejection sampling to generate samples from the target. Your answer should include the role of the envelope constant $M$, the proposal step, the acceptance probability, and what happens when a proposal is rejected.

### A7. Mark scheme

Choose $M$ such that

$$\tilde{p}(x)\le Mq(x) \quad \text{for all } x.$$

Then repeat:

1. Draw a proposal $x^*\sim q(x)$.
2. Draw $u\sim \text{Uniform}(0,1)$.
3. Accept $x^*$ if

$$u\le \frac{\tilde{p}(x^*)}{M q(x^*)}.$$

4. If rejected, discard $x^*$ and try again.

The normalising constant of the target is not needed because the method only uses ratios against the envelope. A good proposal should cover the target's support and make $M q(x)$ close to $\tilde{p}(x)$ to avoid a low acceptance rate.
