# Markov Chain Monte Carlo (MCMC)

**Type:** approximation method
**Week:** 5
**Related:** [[metropolis-hastings]], [[gibbs-sampling]], [[rejection-sampling]], [[importance-sampling]], [[variational-inference]], [[bayesian-inference]]
**Source:** [[lecture-w5]], [[lecture-w10]]

## Definition
MCMC is a class of sampling algorithms that construct a Markov chain whose stationary distribution equals the target posterior, allowing approximate posterior expectations to be computed via sample averages.

## Motivation
Variational inference makes approximations that introduce bias; rejection/importance sampling are inefficient in high dimensions. MCMC makes **no distributional assumptions** about the posterior shape and is asymptotically exact: given enough samples, estimates converge to the true posterior expectations.

## How it works

### Monte Carlo Integration
$$\mathbb{E}_{p(\theta|\mathcal{D})}[f(\theta)] \approx \frac{1}{N}\sum_{i=1}^N f(\theta^i), \qquad \theta^1,\ldots,\theta^N \sim p(\theta|\mathcal{D})$$
No need for the normalising constant $p(\mathcal{D})$ — only the unnormalised posterior $\tilde{p}(\theta) = p(\mathcal{D}|\theta)p(\theta)$ is needed.

### Markov Chains
- A Markov chain is a sequence $\theta^0 \to \theta^1 \to \cdots$ where $\theta^{m+1}$ depends only on $\theta^m$.
- **Stationary distribution** $p^*$: a distribution invariant under the transition kernel $T$:
$$p^*(\theta') = \int p^*(\theta)T(\theta'|\theta)\,d\theta$$
- **Ergodicity**: for large $m$, chain distribution $\to p^*$ regardless of initialisation.
- **Detailed balance** (sufficient for stationarity):
$$p^*(\theta)T(\theta'|\theta) = p^*(\theta')T(\theta|\theta')$$
- **Burn-in**: early samples depend on the initial state $\theta^0$; discard them.

### Direct Sampling Methods (Simpler but Limited)
| Method | Idea | Limitation |
|--------|------|-----------|
| Rejection sampling | Accept/reject from proposal using envelope | Low acceptance rate in high $d$ |
| Importance sampling | Reweight samples from proposal | Weight degeneracy in high $d$ |

### Core MCMC Algorithms

**Metropolis–Hastings (MH)** — general framework:
1. Propose $\theta' \sim q(\theta'|\theta^m)$.
2. $\alpha = \min\!\left(1,\, \frac{\tilde{p}(\theta')\,q(\theta^m|\theta')}{\tilde{p}(\theta^m)\,q(\theta'|\theta^m)}\right)$ — unknown constant $Z$ cancels.
3. Set $\theta^{m+1} = \theta'$ with prob $\alpha$, else $\theta^{m+1} = \theta^m$.

**Metropolis** — special case with symmetric proposal $q(\theta'|\theta) = q(\theta|\theta')$ (e.g. Gaussian random walk):
$$\alpha = \min\!\left(1,\, \frac{\tilde{p}(\theta')}{\tilde{p}(\theta^m)}\right)$$

**Gibbs Sampling** — cycle through conditionals:
$$\theta_k^{m+1} \sim p(\theta_k|\theta_{-k}^m, \mathcal{D})$$
- Special case of MH with acceptance rate = 1.
- Requires tractable conditional distributions.

## Key derivation
MH satisfies detailed balance: for symmetric proposal $q$,
$$p^*(\theta)\,T(\theta'|\theta) = p^*(\theta)\,q(\theta'|\theta)\,\min\!\left(1,\frac{p^*(\theta')}{p^*(\theta)}\right) = \min(p^*(\theta'), p^*(\theta))\,q(\theta'|\theta)$$
which is symmetric in $\theta, \theta'$ (since $q$ is symmetric), verifying stationarity.

## Parameters & intuition
- **Proposal width**: large step → explores fast but low acceptance; small step → high acceptance but slow mixing.
- **Burn-in**: discard the first $M$ samples (chain hasn't mixed yet).
- **Autocorrelation**: MCMC samples are correlated; effective sample size < number of iterations.
- **Convergence diagnostics**: R-hat statistic, trace plots.

## Worked example sketch
*Gaussian posterior*: Metropolis with Gaussian random walk. Propose $\theta' = \theta^m + \epsilon$, $\epsilon \sim \mathcal{N}(0, s^2)$. Accept with probability $\min(1, p(\theta'|\mathcal{D})/p(\theta^m|\mathcal{D}))$.

## Connections
- Compare with [[variational-inference]]: VI is fast/deterministic but biased; MCMC is asymptotically exact but slow.
- Compare with [[laplace-approximation]]: Laplace is a one-shot Gaussian; MCMC explores the full posterior.
- [[gibbs-sampling]] and [[metropolis-hastings]] are specific MCMC algorithms.
- [[rejection-sampling]] and [[importance-sampling]] are simpler alternatives that don't use Markov chains.

## Exam notes
- "Key differences between Laplace, VI, MCMC": ⚠️ **past exam question**.
- "Difference between rejection and importance sampling + one limitation each": ⚠️ **past exam question**.
- MH algorithm steps: **conceptual** understanding required.
- Gibbs sampling: "proposal = exact conditional → acceptance = 1" — must know this.
- Derivations NOT examinable (Week 5).
- No formulas given. ⚠️
- Formula status: algorithm steps must be known from memory ⚠️

## Complementary Material

https://www.youtube.com/watch?v=yApmR-c_hKU - Mathematical Deep dive into motivation and intuition how it works & proof of detailed balance condition

https://www.youtube.com/watch?v=nndtTssgtZE - Visualisation of MCMC
https://www.youtube.com/watch?v=gpsfjDbSnAw - Comprehensive deep dive into MCMC and other approaches like rejection, importance sampling and real worked example
https://www.youtube.com/watch?v=3qodjHRUxAo - Another visualisation of MCMC