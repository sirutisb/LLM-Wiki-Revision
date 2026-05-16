# Metropolis-Hastings Algorithm

**Type:** algorithm
**Week:** 5
**Related:** [[mcmc]], [[bayesian-inference]], [[gibbs-sampling]]
**Source:** [[lecture-w5]]

## Definition
Metropolis-Hastings (MH) is a Markov chain Monte Carlo algorithm that constructs a Markov chain with stationary distribution $p^*(\theta)$ by accepting or rejecting proposed moves with a carefully chosen acceptance probability.

## Motivation
We want samples from $p^*(\theta) \propto \tilde{p}(\theta)$ (e.g., the unnormalised posterior), but cannot sample directly. MH uses an easy-to-sample proposal distribution and corrects for the mismatch via an accept/reject step, ensuring detailed balance.

## How it works

### Algorithm
1. Initialise $\theta^{(0)}$ arbitrarily.
2. At iteration $t$: propose $\theta' \sim q(\theta'|\theta^{(t-1)})$.
3. Compute acceptance ratio:
$$A = \frac{\tilde{p}(\theta')\, q(\theta^{(t-1)}|\theta')}{\tilde{p}(\theta^{(t-1)})\, q(\theta'|\theta^{(t-1)})}$$
4. Accept: set $\theta^{(t)} = \theta'$ with probability $\min(1, A)$.
5. Reject: set $\theta^{(t)} = \theta^{(t-1)}$ with probability $1 - \min(1, A)$.
6. Repeat.

### Why $\min(1, A)$?
The acceptance ratio $A$ ensures **detailed balance**: the rate of moving from $\theta$ to $\theta'$ equals the rate of moving back. This guarantees $p^*$ is the stationary distribution.

### Acceptance Ratio Intuition
$$A = \underbrace{\frac{\tilde{p}(\theta')}{\tilde{p}(\theta^{(t-1)})}}_{\text{target ratio}} \times \underbrace{\frac{q(\theta^{(t-1)}|\theta')}{q(\theta'|\theta^{(t-1)})}}_{\text{proposal correction}}$$
- If proposal is symmetric $q(\theta'|\theta) = q(\theta|\theta')$: correction = 1 → simplifies to **Metropolis**.
- If proposed $\theta'$ has higher target probability → likely accept.
- If lower → accept with probability proportional to the ratio (sometimes accept bad moves to explore).

### Metropolis Algorithm
Special case with symmetric proposal (e.g. Gaussian random walk $\theta' = \theta + \epsilon$, $\epsilon \sim \mathcal{N}(0, \sigma^2)$):
$$A = \frac{\tilde{p}(\theta')}{\tilde{p}(\theta^{(t-1)})}$$

### Practical Considerations
- **Burn-in**: discard initial samples before chain reaches stationarity.
- **Thinning**: keep every $k$th sample to reduce autocorrelation.
- **Proposal tuning**: $\sigma$ too small → slow exploration; $\sigma$ too large → high rejection rate.
- **Target acceptance rate**: ~23% optimal in high dimensions; ~44% in 1D.

## Key derivation
⚠️ *Derivation not examinable*

Detailed balance condition: $p^*(\theta)q(\theta'|\theta)\min(1, A(\theta \to \theta')) = p^*(\theta')q(\theta|\theta')\min(1, A(\theta' \to \theta))$. Substituting the definition of $A$ proves this holds.

## Parameters & intuition
- Proposal $q$: any distribution we can sample from; shape determines efficiency.
- $A$: prevents the chain from moving to low-probability regions too often.
- $\tilde{p}$ need only be known up to normalisation — MH never needs $Z = \int \tilde{p}(\theta)d\theta$.

## Connections
- [[mcmc]]: MH is the general MCMC method; Gibbs and Metropolis are special cases.
- [[gibbs-sampling]]: samples exactly from conditionals; acceptance = 1 always.
- [[bayesian-inference]]: MH used to sample from intractable posteriors.

## Exam notes
- Write out the MH algorithm step by step: ⚠️ **examinable**.
- Know the acceptance probability formula.
- Understand why normalisation constant is not needed.
- Distinguish MH (asymmetric $q$) vs Metropolis (symmetric $q$).
- Formula status: no formula sheet for Week 5 ⚠️; acceptance ratio must be known.
