# Gibbs Sampling

**Type:** algorithm
**Week:** 5
**Related:** [[mcmc]], [[metropolis-hastings]], [[bayesian-inference]], [[variational-inference]]
**Source:** [[lecture-w5]]

## Definition
Gibbs sampling is an MCMC algorithm that samples from the joint distribution $p(\theta_1, \ldots, \theta_d)$ by iteratively sampling each variable from its full conditional distribution, keeping all others fixed.

## Motivation
For many Bayesian models (especially with conjugate priors), the full conditional $p(\theta_j | \theta_{-j}, \mathcal{D})$ is tractable even when the joint posterior is not. Gibbs sampling exploits this structure without requiring a proposal distribution or accept/reject step.

## How it works

### Algorithm
1. Initialise $\boldsymbol{\theta}^{(0)} = (\theta_1^{(0)}, \ldots, \theta_d^{(0)})$.
2. At iteration $t$, for each $j = 1, \ldots, d$:
$$\theta_j^{(t)} \sim p(\theta_j \mid \theta_1^{(t)}, \ldots, \theta_{j-1}^{(t)}, \theta_{j+1}^{(t-1)}, \ldots, \theta_d^{(t-1)}, \mathcal{D})$$
(use the most recently sampled values of all other variables.)
3. Collect $\boldsymbol{\theta}^{(t)} = (\theta_1^{(t)}, \ldots, \theta_d^{(t)})$.
4. Repeat until convergence.

### Key Property: Always Accepts
The Gibbs move is a special case of MH where the acceptance ratio $A = 1$. Sampling from the exact conditional guarantees acceptance — no wasted proposals.

### Full Conditional
$$p(\theta_j | \boldsymbol{\theta}_{-j}, \mathcal{D}) \propto p(\boldsymbol{\theta}, \mathcal{D}) = p(\mathcal{D}|\boldsymbol{\theta})p(\boldsymbol{\theta})$$
with all variables except $\theta_j$ treated as constants.

For conjugate models, this often simplifies to a known distribution (e.g. Gaussian, Beta, Dirichlet).

## Key derivation
Gibbs sampling satisfies detailed balance for each coordinate update. Since the stationary distribution of each conditional is $p(\theta_j|\boldsymbol{\theta}_{-j})$, the joint stationary distribution is $p(\boldsymbol{\theta})$.

## Parameters & intuition
- **Mixing**: slow if variables are highly correlated — samples move in axis-aligned steps.
- **No proposal tuning needed**: unlike MH, no $\sigma$ to adjust.
- **Requires tractable conditionals**: the practical constraint — not always available.
- **Blocked Gibbs**: group correlated variables and sample jointly.

## Worked example sketch
*Bayesian linear regression* with Gaussian prior on $\mathbf{w}$ and unknown noise $\sigma^2$:
- Conditional $p(\mathbf{w}|\sigma^2, \mathcal{D})$: Gaussian (conjugate).
- Conditional $p(\sigma^2|\mathbf{w}, \mathcal{D})$: Inverse-Gamma (conjugate).
→ Alternate sampling from these two tractable conditionals.

## Connections
- [[mcmc]]: Gibbs is a special case of MCMC (and of MH with acceptance = 1).
- [[metropolis-hastings]]: general case; Gibbs avoids rejections by sampling exact conditionals.
- [[bayesian-inference]]: Gibbs used for posterior inference in conjugate hierarchical models.
- [[variational-inference]]: VI is an alternative when conditionals are intractable.

## Exam notes
- Gibbs sampling algorithm: ⚠️ **examinable** (conceptual description).
- Key advantage: acceptance always 1 (no rejected samples).
- Key limitation: requires tractable full conditionals.
- Distinguish Gibbs (exact conditionals, $A=1$) from MH (general proposal, $A \leq 1$).
- Formula status: no formula sheet for Week 5 ⚠️
