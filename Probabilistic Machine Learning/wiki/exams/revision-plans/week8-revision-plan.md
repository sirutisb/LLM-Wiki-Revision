# Week 8 Revision Plan - Variational Autoencoders

**Scope:** [[autoencoder]], [[variational-autoencoder]], [[reparameterization-trick]], [[elbo]], [[variational-inference]], [[kl-divergence]]
**Source:** [[lecture-w7]], [[examinable-topics]], [[week8_questions]]
**Formula status:** No formula sheet for Week 8. Memorise the VAE generative model, approximate posterior, VAE ELBO, reparameterization equation, and diagonal-Gaussian KL to the standard normal.

Week 8 is lower priority than Weeks 1-4 and 7, but it is a compact topic. The likely questions are conceptual/bookwork rather than long derivations: compare AE and VAE, explain the ELBO terms, explain the reparameterization trick, and diagnose reconstruction-vs-KL failure modes.

For exam numbering, treat VAEs as Week 8 even though the source page is [[lecture-w7]].

---

## What To Know Cold

### Scope and source status
- [ ] Week 8 examinable topic: Variational Autoencoders.
- [ ] Source page: [[lecture-w7]] contains the VAE material despite the lecture-file label.
- [ ] Related Week 4 material: [[elbo]], [[variational-inference]], [[kl-divergence]].
- [ ] No formula sheet: the key expressions below must be recalled from memory.
- [ ] Derivations: the Week 8 VAE-specific derivations are not the main target, but the ELBO identity and its interpretation must be understood because it is reused from Week 4.

### Core definitions
- [ ] Autoencoder: deterministic encoder-decoder trained to reconstruct the input through a bottleneck.
- [ ] Encoder: maps $x$ to latent representation $z$.
- [ ] Decoder: maps latent representation $z$ to reconstruction $\hat{x}$ or to a distribution over $x$.
- [ ] Bottleneck: low-dimensional latent code that forces compression.
- [ ] VAE: probabilistic latent-variable model trained by maximising an ELBO.
- [ ] Prior: $p(z) = \mathcal{N}(0,I)$.
- [ ] Approximate posterior: $q_\phi(z|x)$, produced by the encoder.
- [ ] True posterior: $p_\theta(z|x)$, intractable because it depends on the marginal likelihood $p_\theta(x)$.

### Standard autoencoder
- [ ] Architecture:
$$
x \xrightarrow{\text{encoder}} z=f_\theta(x) \xrightarrow{\text{decoder}} \hat{x}=g_\psi(z).
$$
- [ ] Reconstruction objective:
$$
\min_{\theta,\psi}\; \mathcal{L}(x,\hat{x}),
$$
often mean squared error $\|x-g_\psi(f_\theta(x))\|^2$ for continuous data.
- [ ] A plain AE is not a generative model because there is no prior over $z$.
- [ ] A plain AE can have an irregular latent space: arbitrary samples or interpolations in $z$ may decode to nonsense.
- [ ] If the bottleneck is too wide or the model too powerful, the AE can learn a near-identity map instead of useful structure.

### VAE model components
- [ ] Generative model:
$$
z \sim p(z)=\mathcal{N}(0,I), \qquad x \sim p_\theta(x|z).
$$
- [ ] Marginal likelihood:
$$
p_\theta(x)=\int p_\theta(x|z)p(z)\,dz.
$$
- [ ] Why intractable: the integral is over the latent space and the decoder is nonlinear, so there is usually no closed-form solution.
- [ ] Inference model:
$$
q_\phi(z|x)=\mathcal{N}(\mu_\phi(x),\sigma_\phi^2(x)I).
$$
- [ ] Encoder output: mean $\mu_\phi(x)$ and variance $\sigma_\phi^2(x)$, or log-variance in implementations.
- [ ] Decoder output: parameters of $p_\theta(x|z)$, such as a Gaussian mean for continuous data or Bernoulli probabilities for binary image pixels.

### VAE objective to memorise
- [ ] VAE ELBO:
$$
\mathcal{L}_{\theta,\phi}(x)
=
\underbrace{\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)]}_{\text{reconstruction term}}
-
\underbrace{D_{\text{KL}}(q_\phi(z|x)\|p(z))}_{\text{regularisation term}}.
$$
- [ ] Reconstruction term: encourages accurate reconstruction of the observed input.
- [ ] KL term: keeps $q_\phi(z|x)$ close to the prior $p(z)=\mathcal{N}(0,I)$.
- [ ] The objective is maximised, not minimised. Equivalently, many implementations minimise negative ELBO.
- [ ] Gaussian decoder link: maximising the reconstruction log-likelihood is equivalent to minimising squared reconstruction error up to constants.
- [ ] Lower-bound identity:
$$
\log p_\theta(x)
=
\mathcal{L}_{\theta,\phi}(x)
+
D_{\text{KL}}(q_\phi(z|x)\|p_\theta(z|x)).
$$
- [ ] Because KL divergence is non-negative, $\mathcal{L}_{\theta,\phi}(x) \leq \log p_\theta(x)$.

### Reparameterization trick to memorise
- [ ] Naive sampling $z \sim q_\phi(z|x)$ blocks ordinary backpropagation through the encoder parameters.
- [ ] Gaussian reparameterization:
$$
z=\mu_\phi(x)+\sigma_\phi(x)\odot\epsilon,\qquad \epsilon\sim\mathcal{N}(0,I).
$$
- [ ] Randomness is moved into $\epsilon$, whose distribution does not depend on $\phi$.
- [ ] Gradients flow through $\mu_\phi(x)$ and $\sigma_\phi(x)$ because $z$ is now a differentiable deterministic function of those quantities plus fixed-distribution noise.
- [ ] The distribution must be reparameterisable: expressible as $z=g(\phi,\epsilon)$ with $\epsilon$ independent of $\phi$.

### KL formula to memorise
- [ ] For diagonal Gaussian $q_\phi(z|x)=\mathcal{N}(\boldsymbol{\mu},\operatorname{diag}(\boldsymbol{\sigma}^2))$ and prior $p(z)=\mathcal{N}(0,I)$:
$$
D_{\text{KL}}(q_\phi(z|x)\|p(z))
=
\frac{1}{2}\sum_{j=1}^{d}
\left(\mu_j^2+\sigma_j^2-1-\log\sigma_j^2\right).
$$
- [ ] In one dimension:
$$
D_{\text{KL}}(\mathcal{N}(\mu,\sigma^2)\|\mathcal{N}(0,1))
=
\frac{1}{2}(\mu^2+\sigma^2-1-\log\sigma^2).
$$
- [ ] The KL is zero exactly when $\mu=0$ and $\sigma^2=1$, meaning the approximate posterior equals the prior.

### Concepts vs derivations
- [ ] Concepts to explain fluently: AE vs VAE, latent-space regularisation, generation, interpolation, posterior collapse, reconstruction-KL trade-off.
- [ ] Expressions to reproduce from memory: VAE generative model, approximate posterior, ELBO, reparameterization trick, Gaussian KL to the prior.
- [ ] Derivations to understand rather than fully reproduce for Week 8: why the ELBO is a lower bound and why reparameterization permits gradients.
- [ ] Week 4 ELBO derivation remains independently examinable under Week 4, so do not confuse "VAE derivations not emphasised" with "ELBO derivation never examinable".

---

## Revision Schedule

### Pass 1 - 35 minutes: memory setup
- [ ] Write the AE architecture from memory.
- [ ] Write the VAE generative model from memory.
- [ ] Write the approximate posterior from memory.
- [ ] Write the VAE ELBO from memory and label both terms.
- [ ] Write the reparameterization equation from memory.
- [ ] Write the diagonal-Gaussian KL formula from memory.
- [ ] Explain in words why the true posterior $p_\theta(z|x)$ is intractable.

### Pass 2 - 45 minutes: conceptual comparisons
- [ ] Do [[week8_questions]] Q1 and Q5 without notes.
- [ ] Build a six-row AE vs VAE comparison table from memory.
- [ ] Explain why a plain AE cannot generate new samples.
- [ ] Explain how the KL term makes the VAE latent space smoother.
- [ ] Give one example of an irregular latent space and why interpolation can fail.
- [ ] Give one example of meaningful VAE generation: sample $z \sim \mathcal{N}(0,I)$, decode to $x$.

### Pass 3 - 45 minutes: ELBO interpretation
- [ ] Do [[week8_questions]] Q2 and Q3.
- [ ] For each ELBO term, write what it rewards and what failure happens if it dominates.
- [ ] Explain why removing the KL term turns the model into an AE-like reconstruction system.
- [ ] Explain why too much KL pressure can lead to posterior collapse.
- [ ] State the lower-bound identity and the non-negative KL argument in one sentence.

### Pass 4 - 45 minutes: reparameterization and KL mechanics
- [ ] Do [[week8_questions]] Q4 and Q6.
- [ ] For the reparameterization trick, write: problem, equation, where randomness goes, where gradients flow.
- [ ] Compute a one-dimensional Gaussian KL by hand.
- [ ] Compute an ELBO value from a reconstruction estimate and a KL value.
- [ ] State what happens when $q_\phi(z|x)=p(z)$ exactly.

### Final 15-minute check
- [ ] From a blank page, reproduce all five essential expressions.
- [ ] Explain AE vs VAE in two differences.
- [ ] Explain the ELBO in two sentences.
- [ ] Explain reparameterization in two sentences.
- [ ] Diagnose one reconstruction-dominant failure mode and one KL-dominant failure mode.

---

## Worked Example 1 - AE vs VAE Comparison

### Question

Complete the comparison and explain why the VAE can generate new samples while the standard AE cannot.

| Dimension | Standard AE | VAE |
|-----------|-------------|-----|
| Latent code | | |
| Prior | | |
| Objective | | |
| Sampling | | |
| Latent space | | |

### Solution

| Dimension | Standard AE | VAE |
|-----------|-------------|-----|
| Latent code | Deterministic: $z=f_\theta(x)$ | Probabilistic: $z\sim q_\phi(z|x)$ |
| Prior | None | $p(z)=\mathcal{N}(0,I)$ |
| Objective | Reconstruction loss only | ELBO = reconstruction term minus KL term |
| Sampling | No principled way to sample valid $z$ | Sample $z\sim\mathcal{N}(0,I)$ and decode |
| Latent space | May be irregular or discontinuous | Regularised toward a smooth Gaussian latent space |

A standard AE can reconstruct inputs because it learns an encoder-decoder map, but it does not define which latent points are likely. Sampling arbitrary latent points can land in regions the decoder was never trained on. A VAE solves this by imposing the prior $p(z)=\mathcal{N}(0,I)$ and penalising $D_{\text{KL}}(q_\phi(z|x)\|p(z))$, so samples from the prior are encouraged to land in meaningful regions of latent space.

---

## Worked Example 2 - VAE ELBO Interpretation

### Question

A VAE is trained with objective:
$$
\mathcal{L}_{\theta,\phi}(x)
=
\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)]
-
D_{\text{KL}}(q_\phi(z|x)\|p(z)).
$$

1. What does each term encourage?
2. What happens if the KL term is effectively ignored?
3. What happens if the KL term is pushed almost to zero for every data point?

### Solution

The reconstruction term encourages the decoder to assign high probability to the observed input after sampling $z$ from the encoder. For a Gaussian decoder, this behaves like a negative squared reconstruction error, so increasing this term improves reconstructions.

The KL term penalises deviation between the encoder posterior $q_\phi(z|x)$ and the prior $p(z)=\mathcal{N}(0,I)$. It encourages a structured latent space that supports sampling and interpolation.

If the KL term is ignored, the model can reconstruct well but place latent codes in arbitrary disconnected regions. This gives an AE-like failure mode: good reconstructions for encoded training inputs, but poor generation from prior samples.

If the KL term is nearly zero for every data point, then $q_\phi(z|x)\approx p(z)$ for all $x$. The latent variable carries little or no information about the input. This is posterior collapse, and reconstructions usually become poor because the decoder receives uninformative latent samples.

---

## Worked Example 3 - KL and ELBO Calculation

### Question

For a one-dimensional VAE latent variable:
$$
q_\phi(z|x)=\mathcal{N}(\mu,\sigma^2),\qquad \mu=1,\quad \sigma^2=2,
$$
with prior $p(z)=\mathcal{N}(0,1)$.

1. Compute $D_{\text{KL}}(q_\phi(z|x)\|p(z))$.
2. If the reconstruction estimate is $\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)]\approx -3.2$, compute the ELBO.

### Solution

Use:
$$
D_{\text{KL}}(\mathcal{N}(\mu,\sigma^2)\|\mathcal{N}(0,1))
=
\frac{1}{2}(\mu^2+\sigma^2-1-\log\sigma^2).
$$

Substitute $\mu=1$ and $\sigma^2=2$:
$$
D_{\text{KL}}
=
\frac{1}{2}(1^2+2-1-\log 2)
=
\frac{1}{2}(2-\log 2).
$$

Using $\log 2\approx 0.693$:
$$
D_{\text{KL}}\approx \frac{1}{2}(1.307)=0.654.
$$

The ELBO is reconstruction minus KL:
$$
\mathcal{L}_{\theta,\phi}(x)\approx -3.2-0.654=-3.854.
$$

---

## Worked Example 4 - Reparameterization Trick

### Question

For $q_\phi(z|x)=\mathcal{N}(\mu_\phi(x),\sigma_\phi^2(x)I)$, explain why the reparameterization trick is needed and write the reparameterized sample.

### Solution

The VAE objective contains an expectation over $z\sim q_\phi(z|x)$, and $q_\phi$ depends on encoder parameters $\phi$. If we sample $z$ directly from this distribution, the sampling step is not an ordinary differentiable operation through which backpropagation can pass gradients to $\phi$.

Instead write:
$$
z=\mu_\phi(x)+\sigma_\phi(x)\odot\epsilon,\qquad \epsilon\sim\mathcal{N}(0,I).
$$

The randomness is now isolated in $\epsilon$, whose distribution is independent of $\phi$. The sampled $z$ is a differentiable function of $\mu_\phi(x)$ and $\sigma_\phi(x)$, so gradients can flow through the encoder.

---

## Extra Practice To Work On

### Drill A - Blank-page formulas

Write from memory:
- [ ] AE architecture and reconstruction objective.
- [ ] VAE generative model.
- [ ] Approximate posterior.
- [ ] VAE ELBO with labelled terms.
- [ ] Lower-bound identity involving the true posterior KL.
- [ ] Reparameterization equation.
- [ ] Diagonal-Gaussian KL formula.

### Drill B - Conceptual short answers

Answer in three sentences or fewer:
- [ ] Why does a standard AE not define a generative model?
- [ ] Why is the VAE true posterior intractable?
- [ ] What does the reconstruction term reward?
- [ ] What does the KL term penalise?
- [ ] Why does the KL term help interpolation?
- [ ] What is posterior collapse?
- [ ] Why does the reparameterization trick make training possible?

### Drill C - ELBO failure diagnosis

For each case, name the likely failure and the ELBO imbalance:
- [ ] Sharp reconstructions but poor samples from $z\sim\mathcal{N}(0,I)$.
- [ ] Near-zero KL for all data points and poor reconstructions.
- [ ] Encoder outputs very large $|\mu|$ values and very small variances.
- [ ] Decoder ignores $z$ and produces average-looking outputs.

### Drill D - KL calculations

Compute the one-dimensional KL and ELBO for each case. Use reconstruction estimate $R=-2.5$.

| Case | $\mu$ | $\sigma^2$ |
|------|-------|------------|
| 1 | 0 | 1 |
| 2 | 1 | 1 |
| 3 | 0 | 2 |
| 4 | 2 | 0.5 |

Tasks:
- [ ] Compute $D_{\text{KL}}$.
- [ ] Compute $\mathcal{L}=R-D_{\text{KL}}$.
- [ ] Identify which case has zero KL.
- [ ] Explain which cases deviate from the prior through the mean and which through the variance.

---

## Common Mistakes

- [ ] Saying a VAE is just an AE with noise. The key addition is a probabilistic latent-variable model trained with an ELBO.
- [ ] Forgetting the prior $p(z)=\mathcal{N}(0,I)$.
- [ ] Mixing up the encoder and decoder: $q_\phi(z|x)$ is the encoder/inference model; $p_\theta(x|z)$ is the decoder/generative model.
- [ ] Writing the ELBO with the wrong sign on the KL term. The KL is subtracted when maximising the ELBO.
- [ ] Saying the KL term improves reconstruction directly. It regularises the latent space; reconstruction is handled by the expected log-likelihood term.
- [ ] Treating a low KL as always good. KL near zero for every input can mean posterior collapse.
- [ ] Forgetting that $\sigma$ appears in the reparameterization equation, while $\sigma^2$ appears in the Gaussian variance and KL formula.
- [ ] Writing $\epsilon\sim\mathcal{N}(\mu,\sigma^2)$ in the reparameterization trick. The noise is standard normal: $\epsilon\sim\mathcal{N}(0,I)$.
- [ ] Confusing the true posterior $p_\theta(z|x)$ with the approximate posterior $q_\phi(z|x)$.
- [ ] Claiming Week 8 has formulas provided. Week 8 has no formula sheet.
- [ ] Over-preparing long VAE derivations while under-preparing the memorised objective, model components, and explanations.

---

## Exam-Ready Checklist

You are Week 8-ready when you can:

- [ ] Reproduce the VAE generative model, approximate posterior, ELBO, reparameterization equation, and Gaussian KL formula from memory.
- [ ] Explain AE vs VAE in a comparison table without notes.
- [ ] Explain why AEs reconstruct but do not generate in a principled way.
- [ ] Explain why VAEs can generate by sampling from $p(z)=\mathcal{N}(0,I)$ and decoding.
- [ ] Label the reconstruction and KL terms in the VAE ELBO and explain the role of each.
- [ ] Explain why the ELBO is a lower bound using the non-negativity of KL divergence.
- [ ] Explain the reparameterization trick as problem, equation, and gradient-flow solution.
- [ ] Compute a one-dimensional Gaussian KL and a simple ELBO value.
- [ ] Diagnose reconstruction-dominant failure, poor sampling, and posterior collapse.
- [ ] State clearly that Week 8 has no formula sheet and that VAE-specific derivations are less central than concepts and memorised expressions.
