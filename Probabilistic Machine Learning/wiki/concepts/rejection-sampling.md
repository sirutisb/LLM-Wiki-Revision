# Rejection Sampling

**Type:** algorithm
**Week:** 5
**Related:** [[mcmc]], [[importance-sampling]], [[monte-carlo-integration]], [[bayesian-inference]]
**Source:** [[lecture-w5]]

## Definition
Rejection sampling generates exact independent samples from a target distribution $p^*(\theta)$ by sampling from a tractable proposal distribution $q(\theta)$ and accepting proposals with probability proportional to the importance ratio.

## Motivation
When direct sampling from $p^*$ is impossible (e.g., unnormalised posterior), rejection sampling provides exact samples. It avoids MCMC's correlation between samples — every accepted sample is independent.

## How it works

### Setup
- Target: $p^*(\theta) \propto \tilde{p}(\theta)$ (unnormalised, but evaluable).
- Proposal: $q(\theta)$ — easy to sample from.
- Bound: find constant $M$ such that $\tilde{p}(\theta) \leq M \cdot q(\theta)$ for all $\theta$.

### Algorithm
1. Sample $\theta' \sim q(\theta)$.
2. Sample $u \sim \text{Uniform}(0, 1)$.
3. If $u \leq \frac{\tilde{p}(\theta')}{M \cdot q(\theta')}$: accept $\theta'$ as a sample from $p^*$.
4. Else: reject and go to step 1.

### Acceptance Rate
$$\text{Acceptance rate} = \frac{1}{M}\int \tilde{p}(\theta)\,d\theta = \frac{Z}{M}$$
where $Z = \int \tilde{p}(\theta)d\theta$ (normalisation constant).

- Tight bound ($M$ close to $Z$): high acceptance rate, efficient.
- Loose bound (large $M$): low acceptance rate, wasteful.

### High-Dimensional Problem
In $d$ dimensions, the bound $M$ must cover the entire support of $\tilde{p}$. As $d$ increases, a good proposal becomes exponentially harder to construct — most of the proposal mass falls outside the target's support. Acceptance rate drops exponentially.

## Key derivation
Accepted samples are distributed as $p^*$ because:
$$p(\text{accept} | \theta') = \frac{\tilde{p}(\theta')}{Mq(\theta')}$$
$$p(\theta' \text{ accepted}) \propto q(\theta') \cdot \frac{\tilde{p}(\theta')}{Mq(\theta')} = \frac{\tilde{p}(\theta')}{M} \propto p^*(\theta')$$

## Parameters & intuition
- **$M$ (The Envelope Condition):** must be chosen to satisfy $\tilde{p}(\theta) \leq M q(\theta)$ everywhere. It scales the proposal distribution to provide a global upper bound for our unnormalised target. Tighter $M$ → more efficient.
- **Geometric Intuition:** The algorithm effectively samples points uniformly from the area under the envelope curve $M q(\theta)$. The accept/reject step discards points above $\tilde{p}(\theta)$, leaving samples uniformly distributed under the true target. This mechanism naturally shapes the distribution without ever needing to calculate the normalisation constant $Z$.
- **$q$:** should approximate $p^*$'s shape to maximise acceptance rate.
- Rejected samples are completely discarded (unlike importance sampling, which reweights them).

## Connections
- [[importance-sampling]]: reweights proposal samples rather than rejecting; more efficient in high dimensions.
- [[mcmc]]: does not require independent proposals; handles high dimensions via Markov chain.
- [[monte-carlo-integration]]: rejection sampling produces samples for Monte Carlo estimates.
- [[metropolis-hastings]]: also uses accept/reject but for Markov chains, not independent samples.

## Exam notes
- Know the rejection sampling algorithm and acceptance criterion.
- Know why it fails in high dimensions (curse of dimensionality).
- Compare with importance sampling and MCMC.
- Formula status: no formula sheet for Week 5 ⚠️
