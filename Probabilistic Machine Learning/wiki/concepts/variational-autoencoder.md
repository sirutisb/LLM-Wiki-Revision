# Variational Autoencoder (VAE)

**Type:** model
**Week:** 8 (exam numbering)
**Related:** [[autoencoder]], [[variational-inference]], [[elbo]], [[kl-divergence]]
**Source:** [[lecture-w7]]

## Definition
A Variational Autoencoder (VAE) is a generative latent-variable model that uses variational inference to learn a probabilistic encoder (approximate posterior) and decoder (generative model), trained jointly by maximising the ELBO.

## Motivation
Standard autoencoders learn a compressed representation but have no probabilistic structure in the latent space — you cannot sample meaningful new data. VAEs introduce a prior on the latent space and enforce a structured, continuous latent geometry, enabling generation of novel samples.

## How it works

### Generative Model
$$z \sim p(z) = \mathcal{N}(0, I), \qquad x \sim p_\theta(x|z)$$
- **Prior** $p(z)$: standard Gaussian in latent space.
- **Decoder** $p_\theta(x|z)$: neural network that maps latent code to observation distribution.
- **Marginal likelihood**: $p_\theta(x) = \int p_\theta(x|z)\,p(z)\,dz$ — intractable.

### Encoder (Approximate Posterior)
$$q_\phi(z|x) = \mathcal{N}(\mu_\phi(x),\; \sigma^2_\phi(x)I)$$
- Neural network outputs mean $\mu_\phi(x)$ and variance $\sigma^2_\phi(x)$ of the latent distribution.
- Approximates the true (intractable) posterior $p_\theta(z|x)$.

### VAE ELBO (Training Objective)
From the standard ELBO derivation applied to the latent variable model:
$$\log p_\theta(x) \geq \mathcal{L}_{\theta,\phi}(x) = \underbrace{\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)]}_{\text{reconstruction term}} - \underbrace{D_{\text{KL}}(q_\phi(z|x)\|p(z))}_{\text{regularisation term}}$$

**Term 1** (reconstruction): for Gaussian decoder, proportional to $-\|x - g_\theta(z)\|^2$. Encourages the decoder to reconstruct $x$ accurately.

**Term 2** (KL regulariser): forces the latent distribution $q_\phi(z|x)$ toward the standard Gaussian prior $\mathcal{N}(0,I)$. Prevents irregular latent space; ensures smooth interpolation.

### Reparameterization Trick
- Problem: sampling $z \sim q_\phi(z|x)$ is non-differentiable; cannot backpropagate.
- Solution: $z = \mu_\phi(x) + \sigma_\phi(x) \odot \epsilon$, $\epsilon \sim \mathcal{N}(0,I)$.
- Gradients flow through $\mu_\phi$ and $\sigma_\phi$ (deterministic functions of $\phi$).

## Key derivation
Same ELBO derivation as [[supp-elbo]], specialised to the latent variable model:
$$\log p_\theta(x) = \mathcal{L}_{\theta,\phi}(x) + D_{\text{KL}}(q_\phi(z|x)\|p_\theta(z|x))$$
Since KL $\geq 0$: ELBO is a lower bound. Maximising ELBO trains both $\theta$ and $\phi$.

For Gaussian prior and diagonal Gaussian $q_\phi$:
$$D_{\text{KL}}(q_\phi(z|x)\|p(z)) = \frac{1}{2}\sum_j\left[\mu_j^2 + \sigma_j^2 - 1 - \log\sigma_j^2\right]$$
(Closed-form KL between two Gaussians.)

## Parameters & intuition
- **Encoder** ($\phi$): inference network — compress $x$ to a distribution over $z$.
- **Decoder** ($\theta$): generative network — reconstruct $x$ from $z$.
- **KL weight**: balances reconstruction quality vs. latent space regularity.
- **Sampling** at inference: sample $z \sim \mathcal{N}(0,I)$, pass through decoder → generates new $x$.
- **Interpolation**: latent space is smooth → interpolating between two $z$ values gives plausible intermediate samples.

## Worked example sketch
*Compare AE vs VAE:*
- AE: $z = f_\theta(x)$ (deterministic); objective = reconstruction loss only.
- VAE: $z \sim q_\phi(z|x)$ (probabilistic); objective = ELBO (reconstruction − KL).
- VAE allows generation; AE does not.

## Connections
- [[autoencoder]]: VAE generalises AE from deterministic to probabilistic latent space.
- [[variational-inference]]: VAE trains the encoder via VI (ELBO objective).
- [[elbo]]: VAE uses the same lower bound derivation.
- [[kl-divergence]]: regularisation term is a KL to the prior.
- [[reparameterization-trick]]: makes VAE differentiable end-to-end.

## Exam notes
- AE vs VAE conceptual differences: **examinable**. ⚠️
- VAE ELBO structure (two terms): **examinable** conceptually. ⚠️
- Reparameterization trick: "why needed + how it works" — **examinable**. ⚠️
- Derivations NOT examinable.
- No formulas given. ⚠️
- Formula status: ELBO structure must be understood from memory ⚠️

## Complementary Material
https://www.youtube.com/watch?v=geH5HnRapRs - Visualised VAE's
https://www.youtube.com/watch?v=HBYQvKlaE0A - Deep dive into VAE derivations
https://www.youtube.com/watch?v=qJeaCHQ1k2w - Another explanation