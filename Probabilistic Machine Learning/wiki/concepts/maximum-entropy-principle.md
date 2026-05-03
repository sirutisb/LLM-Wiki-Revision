# Maximum Entropy Principle

**Type:** principle
**Week:** 6
**Related:** [[entropy]], [[bayesian-inference]], [[conjugate-priors]]
**Source:** [[lecture-w6]]

## Definition
The maximum entropy principle states that, given known constraints (e.g. mean, variance), the distribution that best represents current knowledge is the one with the highest entropy — making the fewest additional assumptions.

## Motivation
When only partial information is known (e.g. the mean of a distribution), there are infinitely many distributions consistent with that constraint. Maximum entropy selects the "most uncertain" one — the one that commits as little as possible beyond the stated constraints.

## How it works

### Principle
$$\text{Choose } p^* = \arg\max_p H(p) \quad \text{subject to constraints } \mathbb{E}_p[f_k(x)] = \mu_k$$

Where the constraints encode the known information (e.g. $\mathbb{E}[x] = \mu$, $\text{Var}[x] = \sigma^2$).

### Key Maximum Entropy Results

| Constraints | MaxEnt Distribution |
|-------------|---------------------|
| Support $[0,1]$, nothing else | Uniform: $\text{Uniform}(0,1)$ |
| Mean $\mu$ fixed, support $[0,\infty)$ | Exponential: $\text{Exp}(1/\mu)$ |
| Mean $\mu$ and variance $\sigma^2$ fixed | Gaussian: $\mathcal{N}(\mu, \sigma^2)$ |
| Bounded support $[a,b]$, nothing else | Uniform: $\text{Uniform}(a,b)$ |

### Why Maximum Entropy?
- Introducing extra structure beyond known constraints is unjustified — it implies knowledge we don't have.
- MaxEnt is the most conservative (highest uncertainty) choice.
- Bayesian connection: MaxEnt priors are maximally non-informative given the stated constraints.
- Information theory connection: high entropy = least informative distribution.

### Derivation Sketch (Gaussian case)
Maximise $H(p) = -\int p(x)\log p(x)\,dx$ subject to:
- $\int p(x)dx = 1$ (normalisation)
- $\int xp(x)dx = \mu$ (mean constraint)
- $\int (x-\mu)^2 p(x)dx = \sigma^2$ (variance constraint)

Using Lagrange multipliers → the solution is Gaussian.

## Parameters & intuition
- More constraints → lower maximum entropy (more structure forced).
- No constraints (except normalisation) → uniform distribution (maximum entropy on finite support).
- The Gaussian is the continuous distribution with maximum entropy for given mean and variance.

## Connections
- [[entropy]]: MaxEnt maximises entropy.
- [[bayesian-inference]]: MaxEnt provides a principled way to choose priors.
- [[conjugate-priors]]: some conjugate priors (e.g. Gaussian) arise from MaxEnt reasoning.

## Exam notes
- Know which distribution maximises entropy under which constraints (especially Gaussian). ⚠️
- Conceptual rationale: why maximum entropy = least informative choice.
- "What distribution has maximum entropy given mean and variance?" → Gaussian. ⚠️
- Formula status: entropy formula given ✅ (Week 6); specific results should be known ⚠️
