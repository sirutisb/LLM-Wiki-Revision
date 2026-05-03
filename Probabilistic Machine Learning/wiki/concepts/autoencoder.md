# Autoencoder

**Type:** model
**Week:** 8 (exam numbering)
**Related:** [[variational-autoencoder]], [[variational-inference]], [[elbo]]
**Source:** [[lecture-w7]]

## Definition
An autoencoder is a neural network trained to reconstruct its input through a low-dimensional bottleneck, learning a compressed latent representation in the process.

## Motivation
High-dimensional data (images, audio) often lies on a lower-dimensional manifold. Autoencoders learn this manifold by compressing to a latent code $z$ and reconstructing — forcing the network to capture the essential structure, not noise.

## How it works

### Architecture
$$x \xrightarrow{\text{encoder}} z = f_\theta(x) \xrightarrow{\text{decoder}} \hat{x} = g_\phi(z)$$

- **Encoder** $f_\theta$: maps high-dim input $x$ to low-dim latent $z$.
- **Decoder** $g_\phi$: maps latent $z$ back to reconstruction $\hat{x}$.
- **Bottleneck**: $\dim(z) \ll \dim(x)$ forces compression.

### Training Objective
Minimise reconstruction loss:
$$\mathcal{L} = \|x - g_\phi(f_\theta(x))\|^2 \quad \text{(MSE loss)}$$
or binary cross-entropy for image data with pixel values in $[0,1]$.

### Latent Space
- Latent code $z = f_\theta(x)$ is **deterministic**.
- No probabilistic structure on $z$ — can encode any $x$, but points between encoded examples may decode to nonsense.
- Not a generative model: cannot sample meaningful $z$ without encoding a real $x$ first.

## Key derivation
No probabilistic derivation — AE is trained as a deterministic reconstruction network.

## Parameters & intuition
- Latent dimension $\dim(z)$: too small → poor reconstruction; too large → may just copy the input.
- Encoder/decoder depth: deeper networks capture more complex structure.
- Trained by backprop on reconstruction loss only.

## AE vs VAE

| Dimension | Autoencoder | Variational Autoencoder |
|-----------|------------|------------------------|
| Latent $z$ | Deterministic: $z = f_\theta(x)$ | Probabilistic: $z \sim q_\phi(z\|x)$ |
| Prior on $z$ | None | $p(z) = \mathcal{N}(0,I)$ |
| Objective | Reconstruction only | ELBO = reconstruction − KL |
| Can generate? | No (no way to sample $z$) | Yes (sample $z \sim \mathcal{N}(0,I)$) |
| Latent space | Irregular, potentially discontinuous | Smooth, structured |
| Application | Compression, denoising | Generation, interpolation |

## Connections
- [[variational-autoencoder]]: probabilistic generalisation; adds prior and KL regularisation.
- [[variational-inference]]: VAE applies VI; AE does not.
- [[elbo]]: VAE training objective; not used in plain AE.

## Exam notes
- AE vs VAE comparison: ⚠️ **examinable** (key conceptual question).
- Key distinction: AE = deterministic encoding, no generation; VAE = probabilistic encoding, can generate.
- Why can't AE generate? No structured prior on latent space.
- Formula status: no formula sheet ⚠️; AE concepts understood from description.
