# Deriving the MAP estimate of a univariate Gaussian (known variance)

**Used in:** [[map]], [[bayesian-inference]]
**Source:** [[supp-map-gaussian]]
**Exam status:** ⚠️ Must know

**Derivation was made by Claude Opus 4.7 using Adaptive Thinking**

## Step 1 — From Bayes' rule to a proportionality

By Bayes' theorem:

$$p(\mu \mid y) = \frac{p(y \mid \mu)\, p(\mu)}{p(y)}$$

The denominator $p(y)$ (the marginal likelihood / "evidence") is just a normalising constant — it does **not** depend on $\mu$. So when we're optimising over $\mu$, we can drop it:

$$p(\mu \mid y) \;\propto\; p(y \mid \mu)\, p(\mu)$$

Therefore:

$$\mu_{\text{MAP}} \;=\; \arg\max_\mu \; p(\mu \mid y) \;=\; \arg\max_\mu \; p(y \mid \mu)\, p(\mu)$$

This is the key insight you asked for: maximising the posterior is equivalent to maximising likelihood × prior.

## Step 2 — Take the log

Logarithm is strictly monotonic, so $\arg\max$ is preserved:

$$\mu_{\text{MAP}} \;=\; \arg\max_\mu \; \big[\log p(y \mid \mu) + \log p(\mu)\big]$$

## Step 3 — Write the log-likelihood

Assuming the $y_i$ are conditionally i.i.d. given $\mu$:

$$p(y \mid \mu) \;=\; \prod_{i=1}^n \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left(-\frac{(y_i - \mu)^2}{2\sigma^2}\right)$$

$$\log p(y \mid \mu) \;=\; -\frac{n}{2}\log(2\pi\sigma^2) \;-\; \frac{1}{2\sigma^2}\sum_{i=1}^n (y_i - \mu)^2$$

## Step 4 — Write the log-prior

$$p(\mu) \;=\; \frac{1}{\sqrt{2\pi\sigma_0^2}} \exp\!\left(-\frac{(\mu - \mu_0)^2}{2\sigma_0^2}\right)$$

$$\log p(\mu) \;=\; -\frac{1}{2}\log(2\pi\sigma_0^2) \;-\; \frac{(\mu - \mu_0)^2}{2\sigma_0^2}$$

## Step 5 — Combine and drop $\mu$-independent constants

Let $J(\mu) = \log p(y \mid \mu) + \log p(\mu)$. Dropping anything that doesn't involve $\mu$ (since it vanishes under differentiation):

$$J(\mu) \;=\; -\frac{1}{2\sigma^2}\sum_{i=1}^n (y_i - \mu)^2 \;-\; \frac{(\mu - \mu_0)^2}{2\sigma_0^2} \;+\; \text{const}$$

## Step 6 — Differentiate w.r.t. $\mu$

For the likelihood term, using the chain rule on $(y_i-\mu)^2$:

$$\frac{d}{d\mu}\left[-\frac{1}{2\sigma^2}\sum_i (y_i - \mu)^2\right] \;=\; -\frac{1}{2\sigma^2}\sum_i 2(y_i-\mu)(-1) \;=\; \frac{1}{\sigma^2}\sum_i (y_i - \mu)$$

For the prior term:

$$\frac{d}{d\mu}\left[-\frac{(\mu-\mu_0)^2}{2\sigma_0^2}\right] \;=\; -\frac{\mu - \mu_0}{\sigma_0^2}$$

Combining:

$$\frac{dJ}{d\mu} \;=\; \frac{1}{\sigma^2}\sum_{i=1}^n (y_i - \mu) \;-\; \frac{\mu - \mu_0}{\sigma_0^2}$$

## Step 7 — Set to zero and solve

$$\frac{1}{\sigma^2}\sum_{i=1}^n (y_i - \mu) \;=\; \frac{\mu - \mu_0}{\sigma_0^2}$$

Expand the sum and multiply both sides by $\sigma^2\sigma_0^2$:

$$\sigma_0^2 \sum_{i=1}^n y_i \;-\; n\sigma_0^2 \mu \;=\; \sigma^2 \mu \;-\; \sigma^2 \mu_0$$

Collect $\mu$ terms on the right:

$$\sigma_0^2 \sum_{i=1}^n y_i \;+\; \sigma^2 \mu_0 \;=\; \mu\,(\sigma^2 + n\sigma_0^2)$$

$$\boxed{\;\mu_{\text{MAP}} \;=\; \frac{\sigma_0^2 \sum_{i=1}^n y_i \;+\; \sigma^2 \mu_0}{\sigma^2 + n\sigma_0^2}\;}$$

## Step 8 — Rewrite in the "precision-weighted average" form

Divide numerator and denominator by $\sigma^2 \sigma_0^2$, and let $\bar{y} = \frac{1}{n}\sum_i y_i$:

$$\mu_{\text{MAP}} \;=\; \frac{\dfrac{n}{\sigma^2}\,\bar{y} \;+\; \dfrac{1}{\sigma_0^2}\,\mu_0}{\dfrac{n}{\sigma^2} \;+\; \dfrac{1}{\sigma_0^2}}$$

This form is the more illuminating one, so let me unpack the intuition.

## Intuition — what does this formula actually say?

Define **precision** as the reciprocal of variance, $\tau = 1/\sigma^2$. Two quantities show up:

- The data: average $\bar{y}$, with precision $n/\sigma^2$ (more samples ⇒ more confident).
- The prior: mean $\mu_0$, with precision $1/\sigma_0^2$.

Then:

$$\mu_{\text{MAP}} \;=\; \frac{\tau_{\text{data}} \,\bar{y} \;+\; \tau_{\text{prior}}\,\mu_0}{\tau_{\text{data}} + \tau_{\text{prior}}}$$

which is just a **weighted average where the weights are how confident each source is**. Whoever has higher precision pulls the answer toward themselves.

**Concrete example.** Suppose you're estimating the mean download latency $\mu$ of a server.

- Prior belief: $\mu_0 = 100$ ms, $\sigma_0^2 = 25$ ms² (precision $= 1/25 = 0.04$)
- You measure $n=4$ pings with mean $\bar{y} = 120$ ms, known noise $\sigma^2 = 100$ ms² (data precision $= 4/100 = 0.04$)

Both sources have equal precision, so:

$$\mu_{\text{MAP}} \;=\; \frac{0.04 \cdot 120 + 0.04 \cdot 100}{0.04 + 0.04} \;=\; 110 \text{ ms}$$

It sits exactly in the middle. Now collect $n=400$ pings instead — data precision becomes $4$, swamping the prior's $0.04$, and $\mu_{\text{MAP}} \approx \bar{y} = 120$. The data has overwhelmed the prior. Conversely, if you had a razor-sharp prior ($\sigma_0^2 \to 0$), nothing the data says will move you off $\mu_0$.

**Two limiting cases worth remembering:**

- $\sigma_0^2 \to \infty$ (uninformative prior): $\mu_{\text{MAP}} \to \bar{y}$, the MLE. The Bayesian update collapses to the frequentist estimate.
- $n \to \infty$ (lots of data): $\mu_{\text{MAP}} \to \bar{y}$ as well. Data drowns out any finite prior.

This is also where the link to L2 regularisation comes from — a Gaussian prior on $\mu$ is mathematically identical to adding a quadratic penalty $\frac{(\mu-\mu_0)^2}{2\sigma_0^2}$ to the negative log-likelihood, which is exactly ridge regression's penalty term. MAP with a Gaussian prior *is* L2-regularised MLE.