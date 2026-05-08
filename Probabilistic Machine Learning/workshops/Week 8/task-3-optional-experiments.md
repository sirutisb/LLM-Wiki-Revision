# Task 3 — Optional Experiments: $\beta$ and Latent Dimension

## The question (paraphrased)

> (a) Change $\beta$ (e.g. 0.1, 1, 4) and compare reconstructions vs samples.
> (b) Change the latent dimension and compare samples and interpolations.

These are knob-twiddling experiments that build *intuition* for the two main hyperparameters of a VAE. There is no new code to write — we re-run Task 1 with a different setting and look at what changes. The exam has previously asked "what does $\beta$ do?" and "why pick a small latent dimension?", so the qualitative observations here are directly examinable.

Related wiki pages: [[variational-autoencoder]], [[elbo]], [[kl-divergence]], [[autoencoder]].

---

## Part (a) — The $\beta$ knob

### What $\beta$ does

The objective is

$$
\mathcal{L}_{\text{VAE}}(x) \;=\; \mathrm{Recon}(x, \hat x) \;+\; \beta\,\mathrm{KL}\big(q_\phi(z\mid x)\,\|\,p(z)\big).
$$

$\beta$ scales the KL term. Mechanically it is a Lagrange-multiplier-like dial that decides which term wins when they disagree:

- **$\beta \to 0$**: the KL term vanishes; the model becomes a (slightly noisy) plain autoencoder. It will reconstruct beautifully and refuse to be sample-able.
- **$\beta \to \infty$**: the KL term dominates; the encoder is forced to make $q_\phi(z\mid x) \approx \mathcal{N}(0, I)$ for every input, throwing away all information about $x$. The decoder gets a near-prior $z$ regardless of input — *posterior collapse*. Reconstructions become average digits, samples become random average digits.

Useful values to try, as the workshop suggests:

| $\beta$ | Reconstruction | Random samples | Interpolation |
|---|---|---|---|
| $0.1$ | sharper, near-AE quality | worse — codes drift from prior | jumpier |
| $1.0$ | the standard trade-off | recognisable digits | smooth |
| $4.0$ | blurrier, more "averaged" | crisper *and* more diverse, but loses fine detail | smoothest, most "disentangled" |

### How to actually run the experiment

Edit one line in the setup cell:

```python
beta = 0.1   # or 1.0, or 4.0
```

then re-run the VAE training, reconstruction, and sampling cells. Watch the printed `recon` and `kl` per epoch — you will see the trade-off explicitly:

- At $\beta = 0.1$: `kl` rises high (encoder uses a lot of capacity), `recon` falls fast.
- At $\beta = 4.0$: `kl` stays small (encoder is held close to the prior), `recon` plateaus higher.

### What to observe in the images

Lay out three rows of reconstructions and three rows of random samples, one per $\beta$ value:

- **Reconstructions**: monotonically blurrier as $\beta$ grows.
- **Samples**: at $\beta = 0.1$ samples often look "off" — slightly noisy, sometimes implausible — because the encoder did not respect the prior. At $\beta = 4$ samples are "cleaner" but also more averaged.

This is the **$\beta$-VAE trade-off**: reconstruction fidelity versus latent regularity. Higher $\beta$ also tends to give more *disentangled* latent dimensions (each dimension controlling one factor of variation), at the cost of reconstruction.

### Why this is a useful experiment

It makes the role of the KL term visible. With $\beta = 0$ a VAE *is* an AE; with $\beta = \infty$ the decoder ignores its input entirely. Real VAEs live somewhere on that spectrum, and $\beta = 1$ is one principled point on it (the place where the loss is exactly the negative ELBO).

---

## Part (b) — The latent dimension knob

### What `latent_dim` does

The latent dimension controls how much information the encoder is *allowed* to pass to the decoder:

$$
z \in \mathbb{R}^{d}, \qquad q_\phi(z\mid x) = \mathcal{N}(\mu(x), \sigma^2(x) I) \in \mathbb{R}^d.
$$

Three regimes, each with a different visual signature:

- **$d = 2$**: extreme bottleneck. Reconstruction is poor — the encoder cannot squeeze a 28×28 digit into two numbers without losing identity. *But* you can plot the entire latent space directly: scatter $\mu(x_i)$ coloured by digit class on the 2-D plane and see how digits cluster. Interpolation is constrained to a 2-D plane and tends to be very smooth.
- **$d = 16$** (the default): the sweet spot for MNIST. Enough capacity to preserve digit identity; small enough that the decoder must generalise across $z$.
- **$d = 64+$**: lots of capacity. Reconstructions improve. **But** if the KL is loose (small $\beta$), many dimensions become *unused* — the encoder just sets $\mu_j \approx 0, \log\sigma_j^2 \approx 0$ for those dimensions and ignores them. You can detect this by inspecting per-dimension KL contribution after training.

### How to run the experiment

```python
latent_dim = 2     # or 8, or 16, or 64
```

Re-run the model definition, training, and visualisation cells.

### What to observe

- **Random samples** (decode $z \sim \mathcal{N}(0, I)$): with very small $d$ the model "uses" all of its dimensions, so samples vary along all of them and look diverse-but-blurry. With very large $d$, samples vary along the *active* subset and look sharper.
- **Interpolation**: linear interpolation in low-$d$ space passes through fewer points — the morph is forced to take the shortest path through a small space, so the transitions are very smooth but limited in variety. In high-$d$ space, there are more directions to wander; interpolations can pass through more interesting intermediate digits.
- **Latent-space scatter** (only meaningful at $d = 2$): plot $\mu(x_i)$ for a held-out batch with colour by class. Distinct digit clusters that overlap at the seams are a hallmark of a healthy 2-D VAE.

### Why this is a useful experiment

It exposes a tension hidden in the architecture choice:

- Latent dim too small ⇒ underfitting; reconstructions lose digit identity.
- Latent dim too large with $\beta = 1$ ⇒ unused dimensions, possible posterior collapse on those dimensions; the *effective* latent dim is smaller than `latent_dim`.

Together with $\beta$, the latent dimension determines the **information capacity** the VAE allocates per image. A useful mental rule: capacity is roughly "active dimensions × $\log$(spread allowed by KL)".

---

## What to take away for the exam

- $\beta$ in $\beta$-VAE controls the **trade-off between reconstruction and latent regularity**. Larger $\beta$ ⇒ blurrier reconstruction but more sample-able and more disentangled latent space.
- $\beta = 0$ recovers a **plain autoencoder**. $\beta \to \infty$ causes **posterior collapse**: $q_\phi$ becomes the prior, the decoder stops using $z$.
- The standard VAE corresponds to $\beta = 1$ — the value at which the loss is the actual negative ELBO. Other values are a principled deviation, not the original ELBO.
- The latent dimension determines how much information per image the encoder can transmit. Too small ⇒ blurry / wrong-identity reconstructions. Too large with insufficient KL pressure ⇒ unused dimensions.
- Two diagnostic signals from training logs:
  - `kl ≈ 0` after a few epochs ⇒ posterior collapse.
  - `recon` plateauing very high ⇒ bottleneck is too tight (raise `latent_dim` or lower $\beta$).
- For exam-style "what would happen if we increased $\beta$?" questions, the safe answer is: KL falls, reconstruction term rises, samples become cleaner but more average, eventually leading to posterior collapse.
