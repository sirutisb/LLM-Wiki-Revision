# Task 1 — VAE on MNIST

## The question (paraphrased)

> Train a Variational Autoencoder on MNIST using the ELBO objective.
> (a) Identify the reconstruction term and the KL term in the code.
> (b) Visualise reconstructions on held-out digits.
> (c) Generate new samples by drawing $z \sim \mathcal{N}(0, I)$ and decoding.
> (d) Interpolate in latent space between two digits and comment on what changes smoothly.

This is the headline workshop of the module: a fully-working generative model whose loss is the ELBO you derived in Week 4. By the end you should be able to point at every line of code and say "this is the encoder $q_\phi(z\mid x)$", "this is the reparameterization trick", "this is $\mathrm{KL}(q_\phi \,\|\, p)$", "this is the reconstruction term".

Related wiki pages: [[variational-autoencoder]], [[autoencoder]], [[reparameterization-trick]], [[elbo]], [[elbo-derivation]], [[kl-divergence]], [[variational-inference]].

---

## What we are building (and why)

A plain autoencoder ([[autoencoder]]) learns to compress an image $x$ into a latent code $z$ and decompress it back. That is great for reconstruction but useless for *generation* — there is no rule about where good codes live in latent space, so picking a random $z$ and decoding it usually produces noise.

A VAE fixes this by demanding that the *distribution of codes* matches a known prior, almost always $p(z) = \mathcal{N}(0, I)$. Then sampling $z \sim \mathcal{N}(0, I)$ and decoding gives a brand-new digit.

We pay for this property with two changes versus an AE:

1. The encoder no longer outputs a single $z$. It outputs the parameters $\mu(x), \log \sigma^2(x)$ of an *approximate posterior* $q_\phi(z\mid x) = \mathcal{N}(\mu, \sigma^2 I)$.
2. The loss is no longer just reconstruction. It is the **negative ELBO**:

$$
\mathcal{L}_{\text{VAE}}(x) \;=\; \underbrace{-\mathbb{E}_{q_\phi}[\log p_\theta(x\mid z)]}_{\text{reconstruction}} \;+\; \beta\,\underbrace{\mathrm{KL}\big(q_\phi(z\mid x)\,\|\,p(z)\big)}_{\text{regulariser pulling }q\text{ toward the prior}}
$$

Reconstruction wants the decoder to recreate $x$. The KL term punishes the encoder if it places its mass anywhere far from $\mathcal{N}(0, I)$. Balancing the two is what makes the latent space *both* informative *and* sample-able.

---

## Cell-by-cell walkthrough

### Cell 0 — Setup and hyperparameters

```python
latent_dim = 16
batch_size = 128
lr = 1e-3
train_subset = 10000
epochs_vae = 5
beta = 1.0
```

Three knobs you will revisit:

- `latent_dim = 16` — high enough to encode a digit, low enough that the model is forced to compress.
- `beta = 1.0` — coefficient on the KL term. $\beta=1$ is the original VAE; larger $\beta$ disentangles more aggressively at the cost of reconstruction.
- `train_subset = 10000` — only 10k of the 60k MNIST training images, to keep the workshop fast on CPU.

### Cell 1 — Data

Standard MNIST loading. The only nuance is `transforms.ToTensor()` which scales pixels into $[0, 1]$. This is essential because the decoder ends in `Sigmoid` and the reconstruction loss will be binary cross-entropy — both assume pixels in $[0, 1]$.

### Cell 2 — The VAE class

```python
class VAE(nn.Module):
    def __init__(self, latent_dim):
        super().__init__()
        self.enc = nn.Sequential(nn.Flatten(), nn.Linear(784, 512), nn.ReLU(),
                                 nn.Linear(512, 256), nn.ReLU())
        self.fc_mu     = nn.Linear(256, latent_dim)
        self.fc_logvar = nn.Linear(256, latent_dim)
        self.dec = nn.Sequential(nn.Linear(latent_dim, 256), nn.ReLU(),
                                 nn.Linear(256, 512), nn.ReLU(),
                                 nn.Linear(512, 784), nn.Sigmoid())
```

Three blocks, in three sub-modules:

1. **Encoder body** (`self.enc`): a small MLP that maps a flattened image to a 256-d hidden representation. This is the *shared* trunk.
2. **Two heads** (`fc_mu`, `fc_logvar`): from the same hidden vector, a linear layer outputs $\mu(x)$ and another outputs $\log \sigma^2(x)$. Two heads, not one — because the encoder describes a Gaussian, not a point.
3. **Decoder** (`self.dec`): mirrors the encoder, ending in `Sigmoid` so outputs are valid pixel intensities.

> Why output **log-variance** and not variance directly? Variance must be strictly positive. If we predicted $\sigma^2$ directly, a single negative output would crash the loss. Predicting $\log \sigma^2 \in \mathbb{R}$ lets the network use any real number, and we recover $\sigma = \exp(0.5\,\log \sigma^2)$ which is automatically positive.

### Cell 2 (continued) — `reparameterize`: the heart of the VAE

```python
def reparameterize(self, mu, logvar):
    std = torch.exp(0.5 * logvar)
    eps = torch.randn_like(std)
    return mu + std * eps
```

This is the [[reparameterization-trick]]. The problem it solves is purely a *gradient* problem.

We need samples $z \sim \mathcal{N}(\mu, \sigma^2 I)$ to feed the decoder. The naive thing — `z = torch.normal(mu, std)` — works in the forward pass but kills backprop: PyTorch cannot push a gradient through "sample from a distribution whose parameters are $\mu, \sigma$". The randomness sits between the encoder parameters $\phi$ and the loss, blocking the chain rule.

The trick rewrites the sample as a *deterministic* function of $\mu, \sigma$ and an external noise variable:

$$z \;=\; \mu \;+\; \sigma \odot \epsilon, \qquad \epsilon \sim \mathcal{N}(0, I).$$

Now $\epsilon$ is the only stochastic node, and crucially it has no parameters — gradients flow cleanly through $\mu$ and $\sigma$ as if $z$ were any other deterministic tensor. This single line is what makes VAEs trainable end-to-end.

### Cell 2 (continued) — `forward`

```python
def forward(self, x):
    mu, logvar = self.encode(x)
    z          = self.reparameterize(mu, logvar)
    x_hat      = self.decode(z)
    return x_hat, mu, logvar, z
```

Notice the function returns four things. We need `mu` and `logvar` for the KL term, `x_hat` for the reconstruction term, and `z` is exposed for downstream visualisation.

### Cell 3 — The ELBO loss

```python
def vae_loss(x_hat, x, mu, logvar, beta=1.0):
    recon = F.binary_cross_entropy(x_hat, x, reduction="sum")
    kl    = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    bs = x.size(0)
    return recon/bs, kl/bs, (recon + beta*kl)/bs
```

Two lines, two terms of the [[elbo-derivation]]:

**Reconstruction term.** `binary_cross_entropy(x_hat, x)` is the negative log-likelihood under a Bernoulli likelihood $p_\theta(x\mid z) = \prod_i \mathrm{Bern}(x_i; \hat{x}_i)$. For pixels in $[0, 1]$ this is the standard choice. Minimising BCE is exactly maximising $\log p_\theta(x \mid z)$.

**KL term.** Because both $q_\phi(z\mid x) = \mathcal{N}(\mu, \sigma^2 I)$ and $p(z) = \mathcal{N}(0, I)$ are diagonal Gaussians, the KL has a clean closed form:

$$
\mathrm{KL}\big(\mathcal{N}(\mu, \sigma^2 I)\,\big\|\,\mathcal{N}(0, I)\big) \;=\; -\tfrac{1}{2}\sum_{j=1}^{d}\big(1 + \log \sigma_j^2 - \mu_j^2 - \sigma_j^2\big)
$$

The line `-0.5 * sum(1 + logvar - mu**2 - logvar.exp())` is *literally* this formula. ⚠️ *No formula given in exam* — derive or memorise it.

**Why divide by batch size?** The two `sum`s aggregate over both the latent dim and the batch. Dividing by `bs` puts the loss on a "per-image" scale so that the printed numbers are comparable across batch sizes and you can sensibly say "average reconstruction loss is 130 nats per image".

### Cell 4 — Training and evaluation loops

Standard PyTorch boilerplate: zero gradients, forward, backward, step. The print statement reports `recon`, `kl`, and total loss separately so you can watch each term:

```
[VAE] Epoch 01 | recon 232.617 | kl 2.108
[VAE] Epoch 02 | recon 188.365 | kl 3.710
[VAE] Epoch 05 | recon 130.652 | kl 12.612
```

Watch the dynamics carefully — they are exam-relevant intuition:

- Reconstruction starts high and falls — the decoder is learning to reproduce digits.
- KL starts near zero and *rises* — initially $q_\phi$ is essentially the prior (the network has not learned to use $z$ yet). As training progresses the encoder uses more latent capacity to encode digit identity, which pushes $q_\phi$ away from $p(z)$ and increases the KL.
- The two terms balance: a healthy VAE has both moderate. KL stuck at 0 is **posterior collapse** — the decoder is ignoring $z$ and the KL term has bullied $q_\phi$ all the way back to the prior.

### Cell 5 — Loss curves

Two plots: total train/test loss and `recon` vs `kl`. The recon-vs-kl plot is the diagnostic one — it reveals whether your VAE is balancing the two terms or drifting toward posterior collapse.

### Cell 6 — Reconstructions on held-out digits

```python
x_hat, _, _, _ = model(x)
```

We pass test images through encode → reparameterize → decode and plot original above reconstruction. Expect **slightly blurry** copies of the input digits. The blur is intrinsic to VAEs: the decoder must produce something plausible *for an entire neighbourhood* of $z$ (because of the reparameterization noise and the KL pressure to spread out), so it averages over local variation and you get smoothed pixels.

### Cell 7 — Generation: sample from the prior

```python
z = torch.randn(n, latent_dim, device=device)   # z ~ N(0, I)
x_gen = model.decode(z)
```

This is the moment the VAE pays off. We bypass the encoder entirely. We draw $z$ from the prior and feed it to the decoder. Because training pulled $q_\phi(z\mid x)$ toward $\mathcal{N}(0, I)$, a random $z$ from the prior is "in distribution" for the decoder — it produces a recognisable digit, not noise.

This only works because of the KL term. Compare with the AE in Task 2 to see the difference.

### Cell 8 — Latent interpolation

```python
mu_a, _ = model.encode(xa)
mu_b, _ = model.encode(xb)
z = (1 - alpha) * mu_a + alpha * mu_b
x_gen = model.decode(z)
```

Encode two images of different digits to get $\mu_a, \mu_b$. Linearly interpolate between them, decode at each step. You should see a smooth morph — say a 3 gradually thickening, reshaping, and curling into an 8 — *not* a fade between two ghost images.

The smoothness is evidence that the decoder is well-defined on the entire region between $\mu_a$ and $\mu_b$, which in turn is a consequence of the KL term making the latent space *connected* and *filled in*. An AE has no such guarantee, and Task 2 will show its interpolations are jumpier or hit dead zones.

What changes smoothly? Stroke thickness, curvature, position of loops, slant — global digit attributes. This is the visual signature of a well-regularised latent space.

---

## What to take away for the exam

- A VAE is an autoencoder whose latent space is **regularised toward a known prior** $p(z) = \mathcal{N}(0, I)$. That single change is what turns it into a generative model.
- The encoder outputs **two vectors**: $\mu(x)$ and $\log \sigma^2(x)$, parameters of $q_\phi(z\mid x) = \mathcal{N}(\mu, \sigma^2 I)$.
- The **reparameterization trick** $z = \mu + \sigma \odot \epsilon, \epsilon \sim \mathcal{N}(0, I)$ exists *only* to let gradients flow through the sampling step. Be ready to explain this in words.
- The **ELBO** decomposes into reconstruction $-\mathbb{E}_q[\log p_\theta(x\mid z)]$ plus $\mathrm{KL}(q_\phi \,\|\, p)$. The $\beta$ coefficient trades the two off.
- For diagonal Gaussian $q$ and standard normal prior, $\mathrm{KL} = -\tfrac{1}{2}\sum_j (1 + \log\sigma_j^2 - \mu_j^2 - \sigma_j^2)$. ⚠️ *Not given in exam* — know how to write it.
- Generation works by sampling $z \sim \mathcal{N}(0, I)$ and decoding. This is *only* meaningful because the KL term pulled $q_\phi$ toward the prior during training.
- **Posterior collapse** = KL stays near zero, decoder ignores $z$. Symptom: random samples all look the same.
- VAE reconstructions are **slightly blurry** by design — the decoder is averaging over a neighbourhood in $z$-space.
- Latent interpolation produces **smooth morphs between digits**, which is direct visual evidence that the latent space is connected.
