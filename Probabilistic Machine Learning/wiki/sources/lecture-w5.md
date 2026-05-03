# Week 5 — Markov Chain Monte Carlo (MCMC)

**File:** `raw/text/COM3031_2526_Week5.txt`
**Type:** lecture
**Week:** 5
**Concepts introduced:** [[mcmc]], [[metropolis-hastings]], [[gibbs-sampling]], [[rejection-sampling]], [[importance-sampling]], [[monte-carlo-integration]]

## Summary
Week 5 introduces sampling-based inference as an alternative to VI. Instead of approximating the posterior's *shape*, we approximate *expectations* under the posterior using sample averages (Monte Carlo integration). Simple methods — rejection sampling and importance sampling — are introduced and their limitations in high dimensions are shown. This motivates MCMC: construct a Markov chain whose stationary distribution is the target posterior, then use its long-run samples.

## Key content

### From VI to Sampling
- VI: replace $p(\theta|\mathcal{D})$ with a tractable $q(\theta)$; fast but depends on the chosen family.
- Sampling: draw $\theta^1, \ldots, \theta^N \sim p(\theta|\mathcal{D})$, then:
$$\mathbb{E}_{p(\theta|\mathcal{D})}[f(\theta)] \approx \frac{1}{N}\sum_{i=1}^N f(\theta^i)$$
- No assumption about posterior shape; naturally captures multimodality and correlations.

### Monte Carlo Integration
- Posterior mean: $\mathbb{E}[\theta|\mathcal{D}] \approx \frac{1}{N}\sum_i \theta^i$.
- Posterior variance: $\text{Var}(\theta|\mathcal{D}) \approx \frac{1}{N}\sum_i (\theta^i - \bar{\theta})^2$.
- No need for the normalising constant $p(\mathcal{D})$.

### Rejection Sampling
- Envelope condition: find proposal $q(\theta)$ and constant $M$ such that $\tilde{p}(\theta) \leq Mq(\theta)$.
- Algorithm: sample $\theta^* \sim q(\theta)$, $u \sim \text{Uniform}(0,1)$. Accept if $u \leq \frac{\tilde{p}(\theta^*)}{Mq(\theta^*)}$.
- Accepted samples are exact draws from $p(\theta|\mathcal{D}) \propto \tilde{p}(\theta)$.
- Limitation: acceptance rate can be very low; finding good $M$ and $q$ is hard in high dimensions.

### Importance Sampling
- Keep all samples, assign weights: $w(\theta) = \frac{\tilde{p}(\theta)}{q(\theta)}$.
- Self-normalised estimator (cancels unknown $Z = \int\tilde{p}(\theta)\,d\theta$):
$$\mathbb{E}[f(\theta)] \approx \frac{\sum_i f(\theta^i)w(\theta^i)}{\sum_i w(\theta^i)}$$
- Key condition: $q(\theta) > 0$ wherever $p(\theta|\mathcal{D}) > 0$ (support matching).
- Limitation: **weight degeneracy** when $q$ has lighter tails than $p$ — a few samples dominate.

### Why MCMC: Markov Chains
- Both rejection and importance sampling use a fixed global proposal — fails in high dimensions.
- Instead: move *locally* from current sample using a Markov chain $\theta^0 \to \theta^1 \to \cdots$.
- **Stationary distribution**: $p^*(\theta')$ is stationary if $p^*(\theta') = \int p^*(\theta)T(\theta'|\theta)\,d\theta$.
- **Ergodicity**: chain eventually forgets initial state; long-run distribution converges to $p^*$.
- **Detailed balance** (sufficient for stationarity): $p^*(\theta)T(\theta'|\theta) = p^*(\theta')T(\theta|\theta')$.

### Metropolis–Hastings (MH)
Given current state $\theta^m$:
1. Propose: $\theta' \sim q(\theta'|\theta^m)$.
2. Acceptance probability:
$$\alpha = \min\!\left(1,\, \frac{\tilde{p}(\theta')q(\theta^m|\theta')}{\tilde{p}(\theta^m)q(\theta'|\theta^m)}\right)$$
3. Accept/reject: $\theta^{m+1} = \theta'$ with prob $\alpha$, else $\theta^{m+1} = \theta^m$.
- Unknown constant $Z$ cancels in the ratio.
- **Metropolis** (special case): symmetric proposal $q(\theta'|\theta) = q(\theta|\theta')$ (e.g. Gaussian random walk) → $\alpha = \min(1, \tilde{p}(\theta')/\tilde{p}(\theta^m))$.

### Gibbs Sampling
- For multi-dimensional $\theta = (\theta_1, \ldots, \theta_K)$: update one component at a time from its exact conditional:
$$\theta_k^{m+1} \sim p(\theta_k|\theta_{-k}^m, \mathcal{D})$$
- Special case of MH where proposal = exact conditional → acceptance rate = 1, no rejection.
- Works well when conditionals are easy to sample from (conjugate models, closed-form conditionals).

## Key takeaways
- Sampling methods make no distributional assumption about the posterior shape.
- Rejection sampling gives exact samples but is inefficient; importance sampling is more efficient but can suffer from weight degeneracy.
- MCMC constructs a chain whose stationary distribution is the posterior — samples become approximately i.i.d. after burn-in.
- MH is the general framework; Metropolis uses symmetric proposals; Gibbs uses exact conditionals.
- Burn-in: discard early samples before the chain has mixed.

## Exam relevance
- "Key difference between importance sampling and rejection sampling; one limitation of each": **past exam question**.
- "Differences between Laplace, VI, MCMC": **past exam question**.
- Rejection sampling algorithm: conceptually **examinable**.
- MH algorithm: conceptually **examinable**.
- Derivations are NOT examinable (Week 5).
- No formulas given for Week 5.

## Links to concepts
- [[mcmc]]: core topic
- [[metropolis-hastings]]: derived here
- [[gibbs-sampling]]: derived here
- [[rejection-sampling]]: introduced here
- [[importance-sampling]]: introduced here
- [[monte-carlo-integration]]: foundation
- [[variational-inference]]: previous approach ([[lecture-w4]])
