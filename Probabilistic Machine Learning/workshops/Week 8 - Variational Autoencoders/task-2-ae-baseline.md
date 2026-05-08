# Task 2 — Plain Autoencoder Baseline

## The question (paraphrased)

> (a) Train a plain autoencoder and compare reconstruction quality to the VAE.
> (b) Compare three "generation" strategies for the AE:
>     (i) sample $z \sim \mathcal{N}(0, I)$ then decode,
>     (ii) encode a real image then decode,
>     (iii) (optional) fit a Gaussian to encoded training latents and sample from it.
> (c) Compare AE vs VAE interpolation behaviour qualitatively.

The point of this question is **not** to learn how an AE works — the architecture is essentially the VAE with the stochastic middle removed. The point is to *empirically expose the gap* between an AE and a VAE: an AE is great at memorising, and useless at generating. Doing the comparison side-by-side is what makes the regularising role of the KL term real.

Related wiki pages: [[autoencoder]], [[variational-autoencoder]], [[kl-divergence]], [[reparameterization-trick]].

---

## What we are building (and why)

A plain autoencoder ([[autoencoder]]) has two networks, encoder and decoder, joined at a low-dimensional bottleneck $z$. It is trained with one loss only: pixel reconstruction. Compare with the VAE objective:

$$
\mathcal{L}_{\text{AE}} = \mathrm{Recon}(x, \hat{x}), \qquad
\mathcal{L}_{\text{VAE}} = \mathrm{Recon}(x, \hat{x}) + \beta\,\mathrm{KL}(q_\phi \,\|\, p).
$$

Same architecture (more or less), one missing term. The missing term changes what the latent space looks like, and therefore changes what happens when you try to *sample* from it.

| | VAE | AE |
|---|---|---|
| Latent distribution | regularised toward $\mathcal{N}(0, I)$ | wherever the network puts it |
| Sampling $z \sim \mathcal{N}(0, I)$ then decoding | gives a digit | gives garbage |
| Reconstruction quality | slightly blurry | crisper |
| Interpolation | smooth morphs | often hits dead zones |

This task makes those rows of the table real.

---

## Cell-by-cell walkthrough

### Cell 1 — The AE class

```python
class AE(nn.Module):
    def __init__(self, latent_dim):
        super().__init__()
        self.encoder = nn.Sequential(nn.Flatten(),
                                     nn.Linear(784, 512), nn.ReLU(),
                                     nn.Linear(512, 256), nn.ReLU(),
                                     nn.Linear(256, latent_dim))
        self.decoder = nn.Sequential(nn.Linear(latent_dim, 256), nn.ReLU(),
                                     nn.Linear(256, 512), nn.ReLU(),
                                     nn.Linear(512, 784), nn.Sigmoid())
```

Compare line for line with the VAE encoder from Task 1:

- VAE: encoder body → two heads (`fc_mu`, `fc_logvar`).
- AE: encoder body → **one head** producing $z$ directly.

There is no $\mu$, no $\log \sigma^2$, no `reparameterize`. The encoder produces a single deterministic point in latent space.

```python
def forward(self, x):
    z = self.encode(x)
    x_hat = self.decode(z)
    return x_hat, z
```

That's it — encode, decode, return. No noise, no KL, no four-tuple.

### Cell 2 — Training

```python
def train_ae_one_epoch(model, loader, optim):
    for x, _ in loader:
        x_hat, _ = model(x)
        loss = F.binary_cross_entropy(x_hat, x, reduction="mean")
        loss.backward(); optim.step()
```

Single-term loss: BCE between input and reconstruction. The optimiser drives the encoder and decoder to memorise the dataset as faithfully as the bottleneck allows. There is no force telling the encoder to *spread out* its codes — it is free to put all images into a sliver of latent space if that minimises reconstruction.

The AE is trained for only `epochs_ae = 2` because the focus is the VAE. Two epochs is plenty to see the qualitative behaviours.

### Cell 3 — Reconstructions

```python
x_hat, _ = model(x)
```

You should find that AE reconstructions are **sharper** than the VAE's. There are two reasons:

1. No KL pressure means the encoder can use a tighter, more "memorisation-like" code for each image.
2. No reparameterization noise means the decoder receives the exact code the encoder produced — no averaging over a neighbourhood.

This is the AE's win and the VAE's deliberate trade-off. A VAE pays a small reconstruction cost in exchange for a sample-able latent space.

### Cell 4 — Generation strategy 1: sample $z \sim \mathcal{N}(0, I)$ and decode

```python
z = torch.randn(n, latent_dim, device=device)
x_gen = model.decode(z)
```

This is the same line that worked beautifully for the VAE in Task 1. With the AE it produces noise — possibly with a faint digit-like ghost, but generally garbage.

**Why?** Because there was no constraint pushing the AE's latent codes to look like $\mathcal{N}(0, I)$. The encoder might have placed all its codes in a thin shell around the origin, in a single quadrant, on a low-dimensional manifold inside $\mathbb{R}^{16}$ — anywhere it likes. A random $z$ from $\mathcal{N}(0, I)$ is overwhelmingly likely to land somewhere the decoder has never been trained to interpret. The decoder has no idea what to draw, so it outputs the average of whatever it half-remembers from training.

This is the moment the KL term earns its keep. Without it, there is no shared coordinate system between the prior and the latent codes, and sampling from the prior is meaningless.

### Cell 5 — Generation strategy 2: encode a real image, then decode

```python
z = model.encode(x)
x_gen = model.decode(z)
```

This is just reconstruction in disguise — we encode then decode, which by definition gives back something close to $x$. It is included to make a point: **the only thing an AE generates "well" is what it has just been shown**. There is no novelty here — calling this "generation" would be like calling a JPEG decoder a generative model.

### Cell 6 — Generation strategy 3 (optional): fit a Gaussian to encoded latents

```python
Z = []
for x, _ in loader:
    Z.append(model.encode(x).cpu().numpy())
Z = np.concatenate(Z, axis=0)
mu_hat = Z.mean(axis=0)
Sigma_hat = np.cov(Z, rowvar=False) + 1e-4*np.eye(Z.shape[1])

z = np.random.multivariate_normal(mu_hat, Sigma_hat, size=n)
x_gen = model.decode(z)
```

A pragmatic hack. The idea is: if we don't know where the AE put its latents, *let us measure*. Pass the training set through the encoder, fit a multivariate Gaussian $\mathcal{N}(\hat\mu, \hat\Sigma)$ to the resulting cloud of codes, and sample from *that* instead of the standard normal.

Two notes:

- The `+ 1e-4*np.eye(...)` adds a tiny ridge to the covariance to keep it numerically positive-definite — `np.random.multivariate_normal` will raise if the matrix has near-zero eigenvalues.
- This sometimes works (samples vaguely resemble digits), and sometimes does not. It only works if the latent cloud actually *is* approximately Gaussian — if the encoder has placed the codes on a curled manifold, fitting a Gaussian to it is wishful thinking.

The deeper lesson: in a VAE we did not need this hack, because the KL term made the cloud of $\mu(x)$ already approximately Gaussian *by construction*. We baked the sampling distribution into training rather than trying to recover it after the fact.

### Cell 7 — AE latent interpolation

```python
za = model.encode(xa)
zb = model.encode(xb)
z = (1 - alpha) * za + alpha * zb
x_gen = model.decode(z)
```

Same code as the VAE interpolation, applied to AE codes. The qualitative behaviour is different and that difference is the point of the exercise:

- AE interpolations often pass through **dead zones**: regions of latent space the encoder has not visited during training, where the decoder produces blurry mush or implausible shapes.
- The transition between digits can be **abrupt**: a sharp 3 followed by junk followed by a sharp 8, instead of a smooth morph.

The VAE's smoother interpolation is direct evidence that the KL term has filled in the latent space and made it *connected* — neighbouring points in $z$-space decode to neighbouring digits, even between training examples.

### Cell 8 — Side-by-side comparison

```python
def compare_random_generation(vae, ae, n=12):
    z = torch.randn(n, latent_dim, device=device)
    x_vae = vae.decode(z)
    x_ae  = ae.decode(z)
```

The same random $z$ goes into both decoders. Top row: recognisable digits. Bottom row: noise. This single image is the workshop's punchline.

---

## What to take away for the exam

- A plain AE has **no constraint** on where latent codes live. The KL term is what makes a VAE different.
- AE reconstructions are typically **sharper** than VAE reconstructions; VAE reconstructions are deliberately blurred by the reparameterization noise and KL pressure.
- AE generation by sampling $z \sim \mathcal{N}(0, I)$ produces **garbage**, because the AE never agreed to put its codes in $\mathcal{N}(0, I)$.
- The "fit a Gaussian to encoded latents" hack is a workaround for missing the KL term. A VAE makes it unnecessary.
- AE interpolations often hit dead zones; VAE interpolations are smoother. This is the *visible* manifestation of the KL term making the latent space connected.
- One-sentence answer for "AE vs VAE": **the AE is a deterministic compressor, the VAE is a probabilistic generator** — and the only architectural difference is the stochastic Gaussian latent and the KL term that regularises it.
