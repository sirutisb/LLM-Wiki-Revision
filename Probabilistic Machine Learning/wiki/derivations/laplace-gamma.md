# Derivation: Laplace Approximation for Gamma Distribution

**Used in:** [[laplace-approximation]]
**Source:** [[lecture-w3]]
**Exam status:** ⚠️ Must know (No formulas given for Week 3)

## Setup
We want to approximate an unnormalised density that is proportional to a Gamma distribution using a Gaussian distribution via the Laplace approximation.

The unnormalised density is given by:
$$ p(\theta) \propto \theta^{\alpha-1} \exp(-\beta \theta), \quad \theta > 0 $$

with parameters $\alpha > 0$ and $\beta > 0$. We want to find:
$$ p(\theta) \approx \mathcal{N}(\theta \mid \hat{\theta}, \sigma^2) $$

## Steps
1. **Define the log unnormalised posterior:**
   $$ g(\theta) = \log p(\theta) = \log(\theta^{\alpha-1} \exp(-\beta \theta)) $$
   $$ g(\theta) = (\alpha - 1) \log \theta - \beta \theta $$

2. **Find the mode (MAP estimate) $\hat{\theta}$:**
   Take the first derivative of $g(\theta)$ with respect to $\theta$:
   $$ g'(\theta) = \frac{\alpha - 1}{\theta} - \beta $$
   Set the derivative to zero and solve for $\hat{\theta}$:
   $$ \frac{\alpha - 1}{\hat{\theta}} - \beta = 0 $$
   $$ \hat{\theta} = \frac{\alpha - 1}{\beta} $$
   *(Note: This requires $\alpha > 1$ for a valid mode where $\theta > 0$)*

3. **Compute the second derivative (curvature):**
   Take the second derivative of $g(\theta)$:
   $$ g''(\theta) = -\frac{\alpha - 1}{\theta^2} $$

4. **Evaluate the negative curvature $A$ at the mode:**
   $$ A = -g''(\hat{\theta}) = \frac{\alpha - 1}{\hat{\theta}^2} $$
   Substitute $\hat{\theta} = \frac{\alpha - 1}{\beta}$:
   $$ A = \frac{\alpha - 1}{\left(\frac{\alpha - 1}{\beta}\right)^2} = \frac{\alpha - 1}{\frac{(\alpha - 1)^2}{\beta^2}} = \frac{\beta^2}{\alpha - 1} $$

5. **Determine the variance:**
   The variance $\sigma^2$ is the inverse of the negative curvature $A$:
   $$ \sigma^2 = A^{-1} = \frac{\alpha - 1}{\beta^2} $$

## Result
The Laplace approximation for the unnormalised Gamma density is a Gaussian distribution with mean $\hat{\theta}$ and variance $\sigma^2$:

$$ p(\theta) \approx \mathcal{N}\left( \theta \;\middle|\; \frac{\alpha - 1}{\beta}, \frac{\alpha - 1}{\beta^2} \right) $$

## Intuition
The Laplace approximation fits a Gaussian at the mode (peak) of the unnormalised posterior. For a Gamma distribution, as the shape parameter $\alpha$ becomes large, the distribution becomes more symmetric and bell-shaped, making the Gaussian approximation increasingly accurate. The variance $\frac{\alpha-1}{\beta^2}$ matches the local curvature of the log-Gamma density at its peak. Note that the true mean of a Gamma is $\alpha/\beta$ and true variance is $\alpha/\beta^2$, which are asymptotically close to our approximation for large $\alpha$.
