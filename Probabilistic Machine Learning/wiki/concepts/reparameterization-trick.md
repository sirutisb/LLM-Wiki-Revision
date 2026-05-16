# Reparameterization Trick

**Type:** algorithm
**Week:** 8 (exam numbering)
**Related:** [[variational-autoencoder]], [[variational-inference]], [[elbo]]
**Source:** [[lecture-w7]]

## Definition
The reparameterization trick rewrites a stochastic sample $z \sim q_\phi(z|x)$ as a deterministic function of the parameters and a noise variable $\epsilon$, making the sampling operation differentiable with respect to $\phi$.

## Motivation
Training a VAE requires backpropagating gradients through the sampling step $z \sim q_\phi(z|x)$. Standard sampling is non-differentiable — the gradient $\partial z / \partial \phi$ does not exist. The reparameterization trick separates the stochasticity from the parameters, enabling gradient flow.

## How it works

### Problem
To maximise the ELBO, we need:
$$\nabla_\phi \mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)]$$
Taking the gradient inside the expectation fails because the distribution depends on $\phi$.

### Solution (Gaussian Case)
For $q_\phi(z|x) = \mathcal{N}(\mu_\phi(x), \sigma^2_\phi(x)I)$:

**Instead of**: sample $z \sim \mathcal{N}(\mu_\phi(x), \sigma^2_\phi(x)I)$ (non-differentiable w.r.t. $\phi$)

**Use**: $z = \mu_\phi(x) + \sigma_\phi(x) \odot \epsilon$, where $\epsilon \sim \mathcal{N}(0, I)$

Now $z$ is a deterministic function of $\phi$ (via $\mu_\phi$ and $\sigma_\phi$) plus independent noise $\epsilon$.

### Gradient Estimator
$$\nabla_\phi \mathbb{E}_{q_\phi}[f(z)] = \mathbb{E}_{\epsilon \sim \mathcal{N}(0,I)}\left[\nabla_\phi f(\mu_\phi + \sigma_\phi \odot \epsilon)\right]$$
The gradient passes through $\mu_\phi$ and $\sigma_\phi$ by the chain rule.

### Monte Carlo Estimate
$$\nabla_\phi \mathbb{E}_{q_\phi}[f(z)] \approx \frac{1}{S}\sum_{s=1}^S \nabla_\phi f(z^{(s)}), \quad z^{(s)} = \mu_\phi + \sigma_\phi \odot \epsilon^{(s)}, \quad \epsilon^{(s)} \sim \mathcal{N}(0,I)$$
In practice, $S=1$ (single sample) works well with minibatch training.

### Requirement
The distribution must be **reparameterisable**: expressible as $z = g(\phi, \epsilon)$ for some deterministic $g$ and noise $\epsilon$ with fixed distribution. Works for Gaussian, Uniform, and other location-scale families.

## Key derivation
⚠️ *Derivation not examinable*

The identity $\mathbb{E}_{z \sim \mathcal{N}(\mu,\sigma^2)}[f(z)] = \mathbb{E}_{\epsilon \sim \mathcal{N}(0,1)}[f(\mu + \sigma\epsilon)]$ holds by change of variables. Differentiating the right-hand side with respect to $\mu, \sigma$ is now valid since the expectation distribution ($\mathcal{N}(0,1)$) does not depend on $\mu, \sigma$.

## Parameters & intuition
- Moves randomness out of the parameters and into an independent noise source.
- Enables low-variance gradient estimates vs REINFORCE (score function estimator).
- The trick applies whenever we need $\nabla_\phi \mathbb{E}_{q_\phi}[\cdot]$ and $q_\phi$ is reparameterisable.

## Connections
- [[variational-autoencoder]]: reparameterization trick is the key ingredient enabling end-to-end backprop through the encoder.
- [[variational-inference]]: also used in parametric VI when gradients of ELBO are needed.
- [[elbo]]: the reconstruction term of the ELBO requires differentiating through the sampling step.

## Exam notes
- "Why is the reparameterization trick needed?" — sampling is non-differentiable. ⚠️ **examinable**.
- "How does it work?" — write $z = \mu_\phi + \sigma_\phi \odot \epsilon$, $\epsilon \sim \mathcal{N}(0,I)$. ⚠️
- Both conceptual and formulaic aspects are examinable.
- Formula status: no formula sheet ⚠️; the reparameterization equation must be known.
