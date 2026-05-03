# Mean-Field Variational Inference

**Type:** algorithm
**Week:** 4
**Related:** [[variational-inference]], [[elbo]], [[kl-divergence]], [[bayesian-inference]]
**Source:** [[lecture-w4]]

## Definition
Mean-field variational inference (MFVI) approximates the posterior $p(\boldsymbol{\theta}|\mathcal{D})$ by a fully factorised distribution $q(\boldsymbol{\theta}) = \prod_j q_j(\theta_j)$, assuming all parameters are independent under $q$.

## Motivation
The full posterior $p(\boldsymbol{\theta}|\mathcal{D})$ is intractable for most models. MFVI restricts the variational family to factorised distributions — tractable to work with — and finds the best factorised approximation by maximising the ELBO.

## How it works

### Mean-Field Assumption
$$q(\boldsymbol{\theta}) = \prod_{j=1}^d q_j(\theta_j)$$
Each factor $q_j$ is optimised independently, ignoring correlations between parameters.

### Coordinate Ascent VI (CAVI)
The ELBO-maximising update for each factor $q_j$ (holding all others fixed) is:
$$\log q_j^*(\theta_j) = \mathbb{E}_{q_{-j}}[\log p(\mathcal{D}, \boldsymbol{\theta})] + \text{const}$$
where the expectation is over all factors except $j$.

This is an unnormalised log-density for $q_j^*$ — normalise to get the distribution.

### Iterative Optimisation
1. Initialise all $q_j$.
2. For each $j$: update $q_j$ using the CAVI formula (hold others fixed).
3. Repeat until ELBO converges.
This is coordinate ascent — each step increases the ELBO.

### Properties
- CAVI update for $q_j$ is exact in exponential family models with conjugate priors.
- Each factor $q_j$ is typically in the same exponential family as the corresponding prior.
- ELBO is non-decreasing under CAVI updates → guaranteed convergence to local maximum.

## Key derivation
Taking the functional derivative $\delta \mathcal{L} / \delta q_j = 0$ subject to $\int q_j = 1$:
$$q_j^*(\theta_j) \propto \exp\left(\mathbb{E}_{q_{-j}}[\log p(\mathcal{D}, \boldsymbol{\theta})]\right)$$
This is the general CAVI formula.

## Parameters & intuition
- The factorisation assumption forces $q$ to represent correlations with marginals rather than joints.
- MFVI tends to **underestimate variance**: the mode-seeking KL penalty shrinks the approximation.
- Computationally cheap: each update is a tractable integral (in exponential family models).

## Connections
- [[variational-inference]]: MFVI is the most common form of VI.
- [[elbo]]: MFVI maximises the ELBO within the factorised family.
- [[kl-divergence]]: minimises reverse KL($q \| p$) by maximising ELBO.
- [[gibbs-sampling]]: structurally similar — both iterate over conditional updates; Gibbs samples, MFVI optimises.

## Exam notes
- Mean-field factorisation assumption: ⚠️ **examinable**.
- Know CAVI update formula conceptually.
- Key limitation: ignores posterior correlations → underestimates uncertainty.
- Compare MFVI with Laplace approximation (both approximate posterior; Laplace uses Gaussian, MFVI uses factorised family).
- Formula status: no formula sheet for Week 4 ⚠️
