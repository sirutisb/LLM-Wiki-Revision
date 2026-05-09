# Practice Question: Beta–Binomial Reliability Analysis

**Topic:** Bayesian Inference / Conjugate Priors
**Week:** 1
**Difficulty:** ⭐ (Introductory)
**Status:** 🟢 Solved

---
## The Problem: Reliability Analysis

Suppose you are developing a new high-frequency data ingestion module. You want to estimate $\theta$, the probability that a specific packet is processed within a 10-microsecond window.

### 1. The Likelihood

You assume the number of packets $y$ processed within the time limit out of $n$ total packets follows a **Binomial distribution**:

$$p(y|\theta) = \binom{n}{y} \theta^y (1-\theta)^{n-y}$$

### 2. The Prior

Before running any tests, you choose a **Beta distribution** as your prior for $\theta$. You decide to use a "Flat" or **Uniform prior**, which corresponds to $Beta(\alpha=1, \beta=1)$.

### 3. The Data

You run a test batch of $n = 50$ packets. You observe that $y = 42$ of them were successfully processed within the 10-microsecond window.

---

### Your Tasks:

1. **Identify the Posterior:** State the name of the posterior distribution and provide its updated hyperparameters, namely $\alpha_{post}$ and $\beta_{post}$.
2. **Calculate the Point Estimate:** Based on the properties of the Beta distribution, calculate the **posterior mean** for $\theta$.
3. **The Intuition Check:** In the context of "pseudo-counts," what do the original prior hyperparameters ($\alpha=1, \beta=1$) represent regarding your "prior knowledge" before you saw the 50 packets?

How would you like to proceed with the derivation?

---

## Solution Space
We start with the likelihood of the data given the parameters and combine it with our prior.

$$p(y|\theta) = \binom{n}{y} \theta^y (1-\theta)^{n-y}$$

$$p(\theta) \propto \theta^{\alpha-1} (1-\theta)^{\beta-1}$$

According to Bayes' Theorem, the posterior is proportional to the product of these two functions:

$$p(\theta|y) \propto \theta^y (1-\theta)^{n-y} \cdot \theta^{\alpha-1} (1-\theta)^{\beta-1}$$

$$p(\theta|y) \propto \theta^{y+\alpha-1} (1-\theta)^{n-y+\beta-1}$$

This confirms that the posterior is also a Beta distribution, specifically $Beta(y+\alpha, n-y+\beta)$.

### The Shorthand Rule
A convenient way to remember Bayesian updating for this conjugate pair is:
- **Successes ($y$):** Add to $\alpha$
- **Failures ($n-y$):** Add to $\beta$

**Iterative Formula:**
$$\alpha \leftarrow \alpha + y$$
$$\beta \leftarrow \beta + (n - y)$$

### Summary of Results
Using $n=50, y=42, \alpha=1, \beta=1$:
1. **Posterior Distribution:** $Beta(43, 9)$
2. **Posterior Mean:** $\mathbb{E}[\theta|y] = \frac{\alpha_{post}}{\alpha_{post} + \beta_{post}} = \frac{43}{52} \approx 0.827$
3. **Intuition (Pseudo-counts):** A $Beta(1,1)$ prior represents having observed **1 success and 1 failure** before the current batch of data. Because these counts are small and balanced, it creates a "Flat" or Uniform prior that doesn't strongly bias the result.

---

## Derivation: Finding the MAP (Mode)
To find the mode (MAP), it is mathematically simpler to maximise the log of the posterior:

$$\mathcal{L}(\theta) = \ln[p(\theta|y)] = (y+\alpha-1)\ln\theta + (n-y+\beta-1)\ln(1-\theta) + \text{const}$$


We take the derivative with respect to $\theta$ and set it to zero.

$$\frac{d\mathcal{L}}{d\theta} = \frac{y+\alpha-1}{\theta} - \frac{n-y+\beta-1}{1-\theta} = 0$$

We cross-multiply to solve for our estimate:

$$(y+\alpha-1)(1-\theta) = \theta(n-y+\beta-1)$$

$$y+\alpha-1 - \theta(y+\alpha-1) = \theta n - \theta y + \theta \beta - \theta$$

By expanding the left side and collecting all terms involving $\theta$ on the right, we get:

$$y+\alpha-1 = \theta n - \theta y + \theta \beta - \theta + \theta y + \theta \alpha - \theta$$

Notice that the $-\theta y$ and $+\theta y$ terms cancel out. We are then left with:

$$y+\alpha-1 = \theta(n + \alpha + \beta - 2)$$

Dividing through gives us the final formula for the MAP estimate:

$$\hat{\theta}_{MAP} = \frac{y + \alpha - 1}{n + \alpha + \beta - 2}$$

---

### Verification with your numbers

If we plug in your specific test case ($n=50, y=42, \alpha=1, \beta=1$):

$$\hat{\theta}_{MAP} = \frac{42 + 1 - 1}{50 + 1 + 1 - 2} = \frac{42}{50} = 0.84$$

In this specific case where the prior is flat, the MAP estimate is exactly equal to the **Maximum Likelihood Estimate (MLE)** because the prior adds no extra "pseudo-counts" to the numerator or denominator.

And from a high-level this is just the frequentist's calculation of success/failures (42/50).

---
**Related:** [[concepts/conjugate-priors]], [[concepts/bayesian-inference]], [[derivations/beta-binomial-posterior]]
