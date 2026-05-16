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

![[Pasted image 20260510225657.png]]

### Why Maximum Entropy?
- Introducing extra structure beyond known constraints is unjustified — it implies knowledge we don't have.
- MaxEnt is the most conservative (highest uncertainty) choice.
- Bayesian connection: MaxEnt priors are maximally non-informative given the stated constraints.
- Information theory connection: high entropy = least informative distribution.

## Key derivation

*Note: This derivation is not examinable.*

### Derivation Sketch (Gaussian case)
Maximise $H(p) = -\int p(x)\log p(x)\,dx$ subject to:
- $\int p(x)dx = 1$ (normalisation)
- $\int xp(x)dx = \mu$ (mean constraint)
- $\int (x-\mu)^2 p(x)dx = \sigma^2$ (variance constraint)

Using Lagrange multipliers → the solution is Gaussian.

## Parameters & Deep Intuition
- More constraints → lower maximum entropy (more structure forced).
- No constraints (except normalisation) → uniform distribution (maximum entropy on finite support).
- The Gaussian is the continuous distribution with maximum entropy for given mean and variance.

To understand the Maximum Entropy Principle, we have to return to the core intuition of what entropy actually measures: **uncertainty**, or how many "binary questions" we need to resolve a state. 

### Why do we choose the *most* entropy?

At first glance, it feels backwards. In machine learning, we usually want to *minimize* uncertainty (entropy) to make good predictions. So why would we deliberately choose the distribution with the *maximum* entropy?

The answer is: **Honesty.** 

Choosing the maximum entropy distribution means being completely honest about what we *don't* know. It is the mathematical equivalent of saying, *"I will commit to the facts I know, and I will assume absolutely nothing else."*

#### The "Least Entropy" Trap (Why we don't choose it)

What if we chose the distribution with the *least* entropy? 
The lowest possible entropy is **0**. An entropy of 0 means absolute certainty—no binary questions needed. 

Imagine I hand you a 6-sided die. I tell you absolutely nothing about it. 
*   **Least Entropy Approach:** You assume the die will roll a `4` with 100% probability, and the other sides have 0% probability. 
    *   *The problem:* You just hallucinated information. You have no justification for assuming the die is completely rigged to land on a `4`. You made a massive, biased assumption.
*   **Maximum Entropy Approach:** You distribute the probability evenly. You assume a $1/6$ chance for every side (the Uniform distribution). 
    *   *The result:* The Uniform distribution has the absolute highest entropy possible for 6 outcomes. By maximizing the uncertainty, you ensured you weren't injecting any personal bias or fake knowledge into the model.

### Adding Constraints (The "Principle" part)

The true power of the Maximum Entropy Principle comes into play when we *do* know something, but not everything. 

The rule is: **Match the known constraints, then spread the remaining probability as evenly (as highly entropic) as possible.**

#### Example: The Loaded Die
Suppose I give you a 6-sided die, and I tell you just one fact: *"The average (mean) roll is 4.5"* (a fair die averages 3.5, so this one is loaded towards the higher numbers).

There are *infinitely* many probability distributions that result in a mean of 4.5. 
*   You could assume it rolls `3` half the time and `6` half the time (Mean = 4.5).
*   You could assume it rolls `4` half the time and `5` half the time (Mean = 4.5).

Both of these are relatively **low entropy**. If you choose them, you are making strict, unjustified assumptions about the die (like assuming it *never* rolls a `1` or `2`).

The **Maximum Entropy Principle** solves this mathematically. You set up an equation that says:
1.  The probabilities must sum to 1.
2.  The expected value (mean) must equal 4.5.
3.  *Maximize the entropy function subject to those two rules.*

The result will be a smooth, exponential-looking curve that gives a little bit of probability to `1`, slightly more to `2`, more to `3`, etc., peaking at `6`. It is the smoothest, least biased way to rig a die so that it averages 4.5 without accidentally assuming any face is impossible.

### The Most Famous Result: The Gaussian (Normal) Distribution

This principle is actually the deep reason why the Gaussian (Normal) distribution is everywhere in nature and machine learning.

If I give you a set of data and tell you exactly two facts:
1.  The **Mean** ($\mu$)
2.  The **Variance** ($\sigma^2$)

And I ask you: *"What is the most unbiased, Maximum Entropy distribution you can draw that fits this mean and variance?"*

The mathematical answer is exactly the **Gaussian distribution**.

Whenever we use a Gaussian prior in Bayesian inference, or assume Gaussian noise in Linear Regression, we are actually invoking the Maximum Entropy Principle. We are saying, *"I know the data has a certain center and spread, but beyond that, I am making the most conservative, uncertain, least-biased assumption possible."*

## Connections
- [[entropy]]: MaxEnt maximises entropy.
- [[bayesian-inference]]: MaxEnt provides a principled way to choose priors.
- [[conjugate-priors]]: some conjugate priors (e.g. Gaussian) arise from MaxEnt reasoning.

## Exam notes
- Know which distribution maximises entropy under which constraints (especially Gaussian). ⚠️
- Conceptual rationale: why maximum entropy = least informative choice.
- "What distribution has maximum entropy given mean and variance?" → Gaussian. ⚠️
- Formula status: entropy formula given ✅ (Week 6); specific results should be known ⚠️
