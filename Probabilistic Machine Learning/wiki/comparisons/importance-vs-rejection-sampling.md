# Importance Sampling vs Rejection Sampling

## Overview
Both Importance Sampling (IS) and Rejection Sampling (RS) are Monte Carlo techniques that allow us to work with complex or unnormalised target distributions $p^*(\theta)$ by drawing samples from a simpler, tractable proposal distribution $q(\theta)$. The core difference lies in how they correct for the mismatch between the proposal $q(\theta)$ and the target $p^*(\theta)$: RS discards samples, while IS keeps all samples but reweights them. Understanding this distinction, and why both fail in high dimensions, is a key exam topic for Week 5.

## Comparison table
| Dimension | Importance Sampling | Rejection Sampling |
|-----------|---------------------|--------------------|
| **Core Mechanism** | Reweights all drawn samples using importance weights $w = p^*/q$. | Accepts/rejects samples based on probability $\frac{\tilde{p}}{Mq}$. |
| **Output** | Weighted samples; directly estimates expectations $\mathbb{E}[f(\theta)]$. | Exact, independent samples drawn from $p^*$. |
| **Requirement on $q$** | $q(\theta) > 0$ wherever $p^*(\theta)f(\theta) > 0$. Needs heavier tails than $p^*$. | Requires a global upper bound $M$ such that $\tilde{p}(\theta) \leq M q(\theta)$. |
| **Wastefulness** | Never discards samples (every sample is used). | Discards rejected samples (low acceptance rate is wasteful). |
| **Handling Unnormalised** | Yes, via self-normalised estimator (normalises weights to sum to 1). | Yes, automatically (the bound $M$ shapes the rejection). |
| **Performance Metric** | Effective Sample Size (ESS). | Acceptance Rate. |
| **High Dimensions ($d$)**| Fails. Weights degenerate (most weights near 0, few huge). | Fails. Acceptance rate drops exponentially as bounding $M$ explodes. |

## When to use which
- **Use Rejection Sampling when:**
  - You strictly need **exact, independent samples** from the target distribution.
  - The dimension $d$ is very low (e.g., 1D or 2D).
  - You can easily find a tight envelope $M$ that bounds the target tightly.
- **Use Importance Sampling when:**
  - Your primary goal is to **estimate an expectation** or integral, rather than generating unweighted samples.
  - Rejection sampling's acceptance rate is too low, making it computationally wasteful.
  - (With caution) the dimension is moderate, but still low enough to avoid complete weight degeneracy.

## Synthesis
Both methods try to solve the same problem—sampling from an intractable distribution using a tractable one—but take different paths to correct the bias. Rejection sampling forces the output to strictly follow $p^*$ by throwing away the "excess" proposals, which guarantees independence but wastes computation. Importance sampling embraces the bias by keeping everything and correcting the expectation with weights, which avoids waste but introduces variance. 

For any simple proposal $q(\theta)$ in high dimensions, it will concentrate its mass in regions where the target $p^*(\theta)$ has almost none. For Rejection Sampling, this means the required envelope $M$ becomes astronomically large, leading to near-zero acceptance rates. For Importance Sampling, this means almost all samples get near-zero weights, while one or two samples dominate the entire estimate (weight degeneracy). Because of this shared failure mode in high dimensions, both methods are typically superseded by **Markov Chain Monte Carlo (MCMC)** methods like Metropolis-Hastings or Gibbs Sampling.

## Exam notes
- Compare the two based on what they do with "bad" proposals (reject vs down-weight).
- Be prepared to explain *why* both fail in high dimensions (curse of dimensionality affecting the proposal mismatch).
- Remember that neither method requires knowing the normalisation constant $Z$ of the target distribution.
