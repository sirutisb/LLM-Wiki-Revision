# Week 8 Practice Questions — Variational Autoencoders

> **Formula policy:** ⚠️ No formula sheet provided for Week 8. All equations must be recalled from memory.
> **Derivation scope:** No specific derivations are examinable. Focus on conceptual understanding, architecture, and the ability to write down and interpret key expressions.

---

## Conceptual / Bookwork

### Q1 — Standard Autoencoder: Architecture and Limitation
⚠️ *No formula given*

**(a)** Describe the architecture of a standard autoencoder. In your answer, define the roles of the encoder, decoder, and bottleneck, and write down the training objective.

**(b)** Explain why a standard autoencoder cannot be used as a generative model — that is, why you cannot use it to sample new, realistic data points. Your answer should refer to the structure of the latent space.

**(c)** What is meant by saying that the latent space of a standard autoencoder is "discontinuous" or "irregular"? Give a brief concrete example of the problem this causes.

---

### Q2 — VAE Generative Model and Inference Model
⚠️ *No formula given*

A Variational Autoencoder defines two components: a **generative model** and an **inference model**.

**(a)** Write down the generative model of a VAE. State the prior distribution $p(z)$, and describe what the decoder $p_\theta(x|z)$ represents. Why is the marginal likelihood $p_\theta(x) = \int p_\theta(x|z)\,p(z)\,dz$ intractable?

**(b)** Write down the inference model (approximate posterior) $q_\phi(z|x)$ for a VAE, and state the parametric form it typically takes. What role does the encoder neural network play in specifying this distribution?

**(c)** Why must we introduce an approximate posterior $q_\phi(z|x)$ rather than using the true posterior $p_\theta(z|x)$ directly during training?

---

### Q3 — The ELBO in the VAE Context
⚠️ *No formula given*

The VAE is trained by maximising the Evidence Lower Bound (ELBO).

**(a)** Write down the VAE ELBO $\mathcal{L}_{\theta,\phi}(x)$, identifying each of its two terms.

**(b)** Explain in words what each term represents and what it encourages during training:
  - (i) The **reconstruction term** $\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)]$
  - (ii) The **regularisation term** $-D_{\text{KL}}(q_\phi(z|x)\|p(z))$

**(c)** What would happen to the latent space if the KL regularisation term were removed from the objective (i.e., if we trained the VAE with reconstruction loss only)? How would this affect the model's ability to generate new samples?

**(d)** Explain why the ELBO is a lower bound on $\log p_\theta(x)$. You do not need to derive this from scratch — a one-sentence justification referencing the KL divergence is sufficient.

---

### Q4 — Reparameterization Trick
⚠️ *No formula given*

**(a)** During VAE training, gradients of the ELBO must be computed with respect to the encoder parameters $\phi$. Explain precisely why naive sampling $z \sim q_\phi(z|x)$ blocks gradient backpropagation.

**(b)** State the reparameterization trick for the Gaussian case $q_\phi(z|x) = \mathcal{N}(\mu_\phi(x), \sigma^2_\phi(x)I)$. Write the expression for $z$ and specify the distribution of the auxiliary noise variable $\epsilon$.

**(c)** Explain how the reparameterization resolves the problem from part (a). Specifically: where does the randomness now reside, and through which quantities do gradients flow?

**(d)** In one sentence, state what property a distribution must have for the reparameterization trick to be applicable.

---

### Q5 — VAE vs Standard Autoencoder (Comparison)
⚠️ *No formula given*

Complete the following comparison between a standard autoencoder (AE) and a Variational Autoencoder (VAE). For each dimension, give a concise answer for both models.

| Dimension | Standard AE | VAE |
|-----------|-------------|-----|
| Nature of latent code $z$ | | |
| Prior on $z$ | | |
| Training objective | | |
| Can generate new samples? | | |
| Latent space structure | | |
| Primary application | | |

After completing the table, answer: *Why does the VAE's KL regularisation term lead to a more structured and interpolable latent space compared to the standard AE?*

---

## Practical / Calculation

### Q6 — Computing the KL Term in the VAE ELBO
⚠️ *No formula given*

For a VAE with a one-dimensional latent space, suppose the encoder outputs:
$$q_\phi(z|x) = \mathcal{N}(\mu, \sigma^2), \qquad \text{with } \mu = 1.0, \quad \sigma^2 = 2.0$$

The prior is $p(z) = \mathcal{N}(0, 1)$.

The closed-form KL divergence between two univariate Gaussians is:
$$D_{\text{KL}}\!\left(\mathcal{N}(\mu, \sigma^2)\,\|\,\mathcal{N}(0,1)\right) = \frac{1}{2}\left(\mu^2 + \sigma^2 - 1 - \log \sigma^2\right)$$

**(a)** Compute $D_{\text{KL}}(q_\phi(z|x)\|p(z))$ for the values above. Show your working.

**(b)** The reconstruction term for this data point is estimated (via the reparameterization trick) as $\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] \approx -3.2$. Write down the ELBO value for this data point.

**(c)** Suppose we change the encoder output to $\mu = 0, \sigma^2 = 1$. Without computing, state what the KL term becomes and explain why this corresponds to the encoder having "collapsed" to the prior. What is the consequence for the reconstruction term?

**(d)** For a $d$-dimensional latent space with diagonal Gaussian $q_\phi$, write down (from memory) the general closed-form expression for the KL divergence between $q_\phi(z|x) = \mathcal{N}(\boldsymbol{\mu}, \text{diag}(\boldsymbol{\sigma}^2))$ and $p(z) = \mathcal{N}(\mathbf{0}, I)$.

---

### Q7 — Interpreting ELBO Components
⚠️ *No formula given*

During training of a VAE on image data, two different runs produce the following behaviours:

- **Run A:** Reconstruction quality is high (sharp images), but samples from $z \sim \mathcal{N}(0,I)$ passed through the decoder produce blurry, unrealistic images.
- **Run B:** The KL divergence $D_{\text{KL}}(q_\phi(z|x)\|p(z))$ is nearly zero for all data points, but reconstruction quality is poor.

**(a)** For Run A, diagnose what has gone wrong in terms of the ELBO. Which term has been optimised at the expense of which? What does this suggest about the latent space geometry?

**(b)** For Run B, diagnose the problem. What is meant by "posterior collapse"? Why does a near-zero KL indicate that the encoder has failed?

**(c)** Sketch how the ELBO objective naturally balances these two failure modes. Why is the trade-off between reconstruction and regularisation sometimes described as a tension?

---

## Answers / Mark Schemes

---

### A1 — Standard Autoencoder

**(a)** Architecture:
- **Encoder** $f_\theta$: maps input $x \in \mathbb{R}^D$ to a low-dimensional latent code $z = f_\theta(x) \in \mathbb{R}^d$, $d \ll D$.
- **Bottleneck**: the dimension $d$ of $z$ forces the network to compress.
- **Decoder** $g_\phi$: maps $z$ back to reconstruction $\hat{x} = g_\phi(z) \in \mathbb{R}^D$.
- **Objective:** minimise reconstruction loss, e.g. $\mathcal{L} = \|x - g_\phi(f_\theta(x))\|^2$ (MSE).

**(b)** A standard AE cannot generate because there is **no prior distribution over** $z$. The encoder is deterministic — it maps each $x$ to a single point $z = f_\theta(x)$. To generate, one would need to sample $z$ from some distribution, but there is no principled way to define which $z$ values are valid. Sampling an arbitrary point in latent space may land in an untrained region, producing garbage output from the decoder.

**(c)** "Irregular" means that the latent codes of different data points may be clustered in disconnected regions, with empty space in between. Example: if training images of cats encode to $z \approx (5, 3)$ and dogs to $z \approx (-4, -2)$, then $z = (0, 0)$ — the midpoint — lies in an untrained region and decodes to a meaningless image, not a plausible cat/dog hybrid.

---

### A2 — VAE Generative and Inference Models

**(a)** Generative model:
$$z \sim p(z) = \mathcal{N}(\mathbf{0}, I), \qquad x \sim p_\theta(x|z)$$
- **Prior** $p(z) = \mathcal{N}(0,I)$: a standard Gaussian over the latent space.
- **Decoder** $p_\theta(x|z)$: a neural network parameterised by $\theta$ that maps a latent code $z$ to the distribution over observations.
- **Marginal** $p_\theta(x) = \int p_\theta(x|z)\,p(z)\,dz$ is **intractable** because the integral is over a high-dimensional continuous space; the decoder is a nonlinear neural network so no closed form exists.

**(b)** The inference model (encoder / approximate posterior):
$$q_\phi(z|x) = \mathcal{N}(\boldsymbol{\mu}_\phi(x),\; \sigma^2_\phi(x)I)$$
The encoder neural network takes $x$ as input and outputs the **mean** $\boldsymbol{\mu}_\phi(x)$ and **variance** $\boldsymbol{\sigma}^2_\phi(x)$ of the latent distribution. These two outputs define $q_\phi(z|x)$; one can then sample $z$ from this distribution.

**(c)** The true posterior $p_\theta(z|x) = p_\theta(x|z)p(z)/p_\theta(x)$ requires computing $p_\theta(x)$, which is intractable (see above). The approximate posterior $q_\phi(z|x)$ sidesteps this by having $\phi$ parameterise a tractable Gaussian family, avoiding the need to evaluate $p_\theta(x)$ directly.

---

### A3 — ELBO in the VAE Context

**(a)** VAE ELBO:
$$\mathcal{L}_{\theta,\phi}(x) = \underbrace{\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)]}_{\text{(i) reconstruction term}} - \underbrace{D_{\text{KL}}(q_\phi(z|x)\|p(z))}_{\text{(ii) regularisation term}}$$

**(b)**
- **(i) Reconstruction term:** Expected log-likelihood of $x$ given samples from the encoder. Encourages the decoder to reconstruct the input accurately — equivalent to minimising the reconstruction error. A Gaussian decoder makes this proportional to $-\|x - \hat{x}\|^2$.
- **(ii) Regularisation (KL) term:** Penalises how far the encoder's approximate posterior $q_\phi(z|x)$ deviates from the prior $\mathcal{N}(0,I)$. Encourages the latent distribution to be close to the prior, producing a smooth, structured latent space that supports generation.

**(c)** Without the KL term, the encoder is free to map each $x$ to any region of latent space with no regularity constraints — equivalent to training a standard AE with a stochastic encoder. The latent space becomes fragmented with no meaningful structure near the prior $\mathcal{N}(0,I)$. Sampling $z \sim \mathcal{N}(0,I)$ and decoding produces poor samples because most prior samples land in untrained regions.

**(d)** Since $D_{\text{KL}} \geq 0$ always:
$$\log p_\theta(x) = \mathcal{L}_{\theta,\phi}(x) + D_{\text{KL}}(q_\phi(z|x)\|p_\theta(z|x)) \geq \mathcal{L}_{\theta,\phi}(x)$$
The KL divergence from the approximate to the true posterior is always non-negative, so the ELBO is always $\leq \log p_\theta(x)$.

---

### A4 — Reparameterization Trick

**(a)** The reconstruction term of the ELBO requires $\nabla_\phi\,\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)]$. The expectation is taken over a distribution that itself depends on $\phi$, so we cannot simply move the gradient inside. The sampling operation $z \sim q_\phi(z|x)$ is **non-differentiable** with respect to $\phi$: there is no deterministic path from $\phi$ to $z$ through which gradients can flow.

**(b)** Reparameterization: instead of sampling $z$ directly, write
$$z = \boldsymbol{\mu}_\phi(x) + \boldsymbol{\sigma}_\phi(x) \odot \epsilon, \qquad \epsilon \sim \mathcal{N}(\mathbf{0}, I)$$
where $\odot$ denotes element-wise multiplication.

**(c)** The randomness is moved into $\epsilon$, whose distribution does **not** depend on $\phi$. Now $z$ is a **deterministic, differentiable** function of $\phi$ (through $\boldsymbol{\mu}_\phi$ and $\boldsymbol{\sigma}_\phi$) plus independent noise. Gradients flow through $\boldsymbol{\mu}_\phi$ and $\boldsymbol{\sigma}_\phi$ via ordinary backpropagation, making end-to-end training possible.

**(d)** The distribution must be **reparameterisable** — expressible as $z = g(\phi, \epsilon)$ for a deterministic function $g$ and a noise variable $\epsilon$ whose distribution is independent of $\phi$ (e.g., location-scale families such as Gaussian, Uniform).

---

### A5 — VAE vs Standard Autoencoder

| Dimension | Standard AE | VAE |
|-----------|-------------|-----|
| Nature of latent code $z$ | Deterministic: $z = f_\theta(x)$ | Probabilistic: $z \sim q_\phi(z|x)$ |
| Prior on $z$ | None | $p(z) = \mathcal{N}(\mathbf{0}, I)$ |
| Training objective | Reconstruction loss only: $\|x - \hat{x}\|^2$ | ELBO = reconstruction $-$ KL |
| Can generate new samples? | No (no principled sampling of $z$) | Yes (sample $z \sim \mathcal{N}(0,I)$, decode) |
| Latent space structure | Irregular, potentially discontinuous | Smooth, structured, continuous |
| Primary application | Compression, denoising, anomaly detection | Generation, interpolation, representation learning |

**KL regularisation and latent structure:** The KL term $-D_{\text{KL}}(q_\phi(z|x)\|p(z))$ penalises the encoder for placing the posterior of any given $x$ far from $\mathcal{N}(0,I)$, and also for making the posterior too narrow (certain). This forces different data points to share overlapping regions of latent space, filling in the space around the origin and creating a **continuous** geometry. Interpolating between two latent codes therefore passes through regions associated with valid data, giving meaningful intermediate samples — unlike AE where the gap between two clusters may be empty and undefined.

---

### A6 — Computing the KL Term

**(a)** Given $\mu = 1.0$, $\sigma^2 = 2.0$:
$$D_{\text{KL}} = \frac{1}{2}\!\left(\mu^2 + \sigma^2 - 1 - \log \sigma^2\right) = \frac{1}{2}\!\left(1 + 2 - 1 - \log 2\right) = \frac{1}{2}(2 - \log 2)$$
$$= \frac{1}{2}(2 - 0.693) = \frac{1}{2}(1.307) \approx 0.654$$

**(b)** ELBO $= \mathbb{E}_{q_\phi}[\log p_\theta(x|z)] - D_{\text{KL}} \approx -3.2 - 0.654 = -3.854$.

**(c)** With $\mu = 0$, $\sigma^2 = 1$:
$$D_{\text{KL}} = \frac{1}{2}(0 + 1 - 1 - \log 1) = \frac{1}{2}(0) = 0$$
The KL is exactly zero, meaning $q_\phi(z|x) = p(z)$: the encoder has ignored $x$ entirely and collapsed to the prior. The latent code $z$ carries no information about $x$, so the decoder cannot reconstruct it — the reconstruction term will be poor (large negative value).

**(d)** For a $d$-dimensional diagonal Gaussian:
$$D_{\text{KL}}\!\left(\mathcal{N}(\boldsymbol{\mu}, \text{diag}(\boldsymbol{\sigma}^2))\,\|\,\mathcal{N}(\mathbf{0}, I)\right) = \frac{1}{2}\sum_{j=1}^{d}\!\left(\mu_j^2 + \sigma_j^2 - 1 - \log \sigma_j^2\right)$$

---

### A7 — Interpreting ELBO Components

**(a) Run A — irregular latent space despite good reconstruction:**
The KL term has been insufficiently weighted or the model has effectively minimised reconstruction loss while allowing the encoder to map data to widely separated, arbitrary regions of latent space (not aligned with the prior). The ELBO has been improved mainly through Term 1 (reconstruction) at the expense of Term 2 (KL regularisation). The latent space is irregular: the encoder posteriors are not close to $\mathcal{N}(0,I)$, so samples from the prior fall in untrained regions, producing poor generated images. This is the AE-like failure mode within a VAE.

**(b) Run B — posterior collapse:**
**Posterior collapse** occurs when the encoder ignores the input ($q_\phi(z|x) \approx p(z)$ for all $x$) and the decoder learns to reconstruct $x$ from no information in $z$ (or produces a blurry average). A near-zero KL means $q_\phi(z|x) \approx \mathcal{N}(0,I)$ for every $x$ — the encoder has "collapsed" and $z$ carries no information about $x$. Since $z$ is uninformative, the decoder cannot produce accurate reconstructions. The model has found a degenerate solution where only the KL term is minimised.

**(c) Natural balance in the ELBO:**
The ELBO $= \mathbb{E}_{q_\phi}[\log p_\theta(x|z)] - D_{\text{KL}}(q_\phi\|p)$ directly trades off the two terms. Increasing the encoder's specificity (sharper posterior, more information about $x$ in $z$) improves reconstruction but increases the KL (more deviation from the prior). Conversely, a posterior close to the prior (low KL) reduces the information $z$ carries about $x$, hurting reconstruction. The tension arises because the reconstruction term rewards specificity and the regularisation term rewards generality. Successful training finds a balance where $z$ encodes just enough information about $x$ while remaining structured enough that prior samples decode meaningfully.
