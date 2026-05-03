# Week 7 — Autoencoders & Variational Autoencoders

**File:** `raw/text/COM3031_2526_Week7.txt`
**Type:** lecture
**Week:** 7
**Concepts introduced:** [[autoencoder]], [[variational-autoencoder]], [[reparameterization-trick]]

> **Note on week labelling:** The exam overview (Week 10) lists Week 7 = Hidden Markov Models and Week 8 = VAEs. However, the lecture slides file `COM3031_2526_Week7.txt` contains the VAE/Autoencoder content, and `COM3031_2526_Week8.txt` contains HMM content. This source page describes the actual file content. For exam purposes, treat VAE content as "Week 8" per the official overview. See [[lecture-w8]] for HMMs.

## Summary
This lecture develops representation learning: why high-dimensional data has low-dimensional latent structure, and how to learn it unsupervised. Vanilla autoencoders (AE) learn a compressed representation by encoding and decoding; regularised variants (denoising, sparse) prevent trivial identity solutions. Variational Autoencoders (VAE) make the latent space probabilistic via variational inference, giving a generative model capable of producing new samples.

## Key content

### Representation Learning
- High-dimensional data (e.g. 784-pixel MNIST images) lies on a low-dimensional manifold.
- Goal: learn $x \to z = \phi_\theta(x) \to \hat{y} = g_\psi(z)$ where $z$ is a compact latent representation.
- Self-supervised learning signal: predict parts of the input from other parts (compression + reconstruction).

### Vanilla Autoencoder
$$x \xrightarrow{\text{encoder}} z = f_\theta(x) \xrightarrow{\text{decoder}} \hat{x} = g_\psi(z)$$
- Bottleneck: $\dim(z) < \dim(x)$.
- Objective: $\min_{\theta,\psi} \mathcal{L}(x, \hat{x})$ (reconstruction loss).
- Problem: if capacity is high, model learns the identity function — no useful structure.

### Regularised Autoencoders
$$\min_{\theta,\psi}\, \mathcal{L}(x,\hat{x}) + \lambda\Omega(z)$$
- **Denoising AE**: corrupt input $\tilde{x}$ with noise; reconstruct $x$ from $\tilde{x}$. Forces encoder to learn robust features, not just copy input.
- **Sparse AE**: penalise $\|z\|_1$ or use KL sparsity $\sum_j \text{KL}(\rho\|\hat{\rho}_j)$ to ensure most activations near zero.

### Limitations of AEs
- Deterministic latent space: each input maps to a single point in $z$.
- No probabilistic model for $z$ → cannot sample meaningful new data.
- Latent space may be irregular/discontinuous.

### Variational Autoencoder (VAE)
- Make latent variable **probabilistic**: $z \sim q_\phi(z|x)$ (probabilistic encoder).
- Generative model: $z \sim p(z) = \mathcal{N}(0,I)$, then $x \sim p_\theta(x|z)$ (decoder).
- True posterior $p_\theta(z|x) = \frac{p_\theta(x|z)p(z)}{p_\theta(x)}$ is intractable.
- Introduce approximate posterior: $q_\phi(z|x) = \mathcal{N}(\mu_\phi(x), \sigma_\phi^2(x)I)$.
- Encoder outputs $(\mu_\phi(x), \sigma_\phi^2(x))$.

### VAE ELBO
From the KL decomposition (same as Week 4 ELBO):
$$\log p_\theta(x) = \underbrace{\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)]}_{\text{reconstruction}} - \underbrace{D_{\text{KL}}(q_\phi(z|x)\|p(z))}_{\text{regularisation}} + D_{\text{KL}}(q_\phi(z|x)\|p_\theta(z|x))$$
VAE objective (ELBO):
$$\mathcal{L}_{\theta,\phi}(x) = \mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{\text{KL}}(q_\phi(z|x)\|p(z))$$
- Term 1 (reconstruction): for Gaussian decoder, $\propto -\|x - g_\theta(z)\|^2$.
- Term 2 (KL regulariser): forces latent distribution toward $\mathcal{N}(0,I)$; makes the latent space smooth and continuous.

### Reparameterization Trick
- Sampling $z \sim q_\phi(z|x)$ is non-differentiable; gradients cannot flow through.
- Solution: $z = \mu_\phi(x) + \sigma_\phi(x) \odot \epsilon$, $\epsilon \sim \mathcal{N}(0,I)$.
- Gradients now flow through $\mu$ and $\sigma$.

## Key takeaways
- AE learns a compression; VAE learns a probabilistic generative model.
- KL regulariser in VAE enforces a structured, continuous latent space.
- VAE = VI applied to a deep latent variable model.
- Reparameterisation makes the ELBO differentiable w.r.t. encoder parameters.

## Exam relevance
- AE vs VAE conceptual differences: **examinable**.
- VAE ELBO structure (reconstruction + KL): **examinable** conceptually.
- Reparameterization trick: **examinable** conceptually.
- Derivations NOT examinable (Week 8 in official exam numbering).
- No formulas given.

## Links to concepts
- [[autoencoder]]: introduced here
- [[variational-autoencoder]]: introduced here
- [[reparameterization-trick]]: introduced here
- [[elbo]]: applied here (same derivation as [[lecture-w4]])
- [[kl-divergence]]: used for regularisation
