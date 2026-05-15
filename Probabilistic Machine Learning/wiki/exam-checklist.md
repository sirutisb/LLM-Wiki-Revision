# COM3031 — Exam Checklist

**Exam:** 2-hour closed-book written exam | May 2026 | Answer all questions | Calculator permitted

**How to use:** Check each box once you can reproduce it cold (no notes). Prioritise top-to-bottom — order matches exam weight.

**Legend:** 🔒 Guaranteed · ⚠️ Highly likely · 🟡 Possible · ✅ Formula given · 📝 No formula given — must know

---

## Week 1 — Bayesian Inference ✅ Formulas given

### Conceptual
- [x] State the four components of Bayesian inference: prior $p(\theta)$, likelihood $p(D|\theta)$, posterior $p(\theta|D)$, predictive distribution $p(y'|D)$
- [x] Explain aleatoric uncertainty vs epistemic uncertainty (with examples)
- [x] Explain frequentist vs Bayesian perspectives on inference
- [ ] Define a conjugate prior and state **one advantage** of using one ⚠️ Past exam Q
- [x] Name three types of prior: non-informative, informative, weakly informative
- [x] State what MLE does: $\hat\theta = \arg\max_\theta \log p(D|\theta)$
- [x] State what MAP does: $\hat\theta = \arg\max_\theta [\log p(D|\theta) + \log p(\theta)]$

### Derivations — must reproduce from scratch ⚠️
- [x] **MLE for univariate Gaussian** — derive $\hat\mu = \bar{x}$ and $\hat\sigma^2 = \frac{1}{n}\sum(x_i - \bar{x})^2$ (biased) via log-likelihood
- [x] **MLE for Binomial** — derive $\hat\theta = y/n$ by differentiating log-likelihood
- [x] **MAP for univariate Gaussian** with Gaussian prior — derive weighted-average result:
$$\hat\mu_{\text{MAP}} = \frac{\sigma_0^{-2}\,\mu_0 + n\sigma^{-2}\bar{x}}{\sigma_0^{-2} + n\sigma^{-2}}$$
- [x] **Beta-Binomial conjugate update** — show posterior is Beta with $\alpha_{\text{new}} = \alpha + y$, $\beta_{\text{new}} = \beta + (n-y)$; interpret pseudo-counts
- [x] **Gamma-Poisson conjugate update** ⚠️ Week 10 worked example — given $n=1, y=10, \alpha=25, \beta=3$: posterior $\text{Gamma}(35, 4)$; $\mathbb{E}[\lambda|y] = 35/4 = 8.75$

### Calculations
- [ ] Given prior and data, compute posterior parameters for Beta-Binomial
- [ ] Given prior and data, compute posterior parameters for Gamma-Poisson
- [ ] Compute posterior mean and variance from posterior parameters

---

## Week 2 — Linear Regression & Classification ✅ Formulas given

### Conceptual
- [ ] Explain the Gaussian noise model for linear regression: $y = \mathbf{x}^T\mathbf{w} + \epsilon$, $\epsilon \sim \mathcal{N}(0, \sigma^2)$
- [x] State that MLE for linear regression = OLS (Ordinary Least Squares)
- [x] State that MAP with Gaussian prior = ridge regression
- [x] Explain GLMs: linear predictor + link function + exponential-family distribution
- [ ] Explain why logarithm is not a suitable link function for logistic regression ⚠️ Past exam Q
  *(Log maps $(-\infty,\infty) \to (-\infty,0)$ — cannot produce probabilities in $(0,1)$)*
- [ ] State the difference between **generative** and **discriminative** models with one example each ⚠️ Past exam Q
- [ ] Explain what is "naïve" about Naïve Bayes: conditional independence assumption $p(x|y) = \prod_j p(x_j|y)$ ⚠️ Past exam Q
- [ ] State the three variants of Naïve Bayes: Gaussian, Bernoulli, Multinomial and when each applies

### Derivations — must reproduce ⚠️
- [x] **MLE for simple linear regression** — derive $\hat{w} = \frac{\sum x_i y_i}{\sum x_i^2}$ (zero-intercept case; more generally $\hat{w}_1 = \frac{S_{xy}}{S_{xx}}$)
- [ ] **Normal Equations for multiple linear regression** — derive $\hat{\mathbf{w}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$ via matrix calculus

### Calculations
- [ ] Given data points, compute $\hat{w}$ for simple linear regression
- [ ] State the Poisson regression model (GLM for count data; log link; $y \sim \text{Poisson}(\lambda)$, $\lambda = e^{\mathbf{x}^T\mathbf{w}}$)
- [ ] Compute MLE for Poisson regression log-likelihood

---

## Week 3 — Laplace Approximation 📝 No formulas given

### Conceptual
- [x] State the core idea: fit a Gaussian at the MAP estimate using local curvature
- [x] State the formula: $q(\theta) = \mathcal{N}(\theta \mid \hat\theta, \sigma^2)$ where $\hat\theta$ = MAP and $\sigma^2 = -\left(\frac{d^2}{d\theta^2}\log p(\theta|D)\right)^{-1}$ at $\hat\theta$
- [x] State **one limitation** of Laplace approximation ⚠️ Past exam Q
  *(Captures only one peak; forces symmetry; fails for skewed or multimodal posteriors)*
- [ ] State the main use ⚠️ Past exam Q *(Approximate intractable posteriors with a Gaussian; also used to derive BIC)*
- [ ] Explain BIC: $\text{BIC} = -2\log p(D|\hat\theta) + k\log n$ — penalises model complexity

### Derivation — must reproduce from scratch ⚠️
- [x] **Laplace procedure (3 steps):**
  1. Log-transform the (unnormalised) posterior
  2. Find the mode by setting the first derivative to zero → MAP estimate $\hat\theta$
  3. Compute the second derivative (curvature) at $\hat\theta$; variance $= -(\text{second derivative})^{-1}$
- [x] **Worked Laplace example** ⚠️ Past exam Q: $p(\theta|y) \propto \theta^y(1-\theta)^{n-y}$
  - Mode: $\hat\theta = y/n$
  - Variance: $\sigma^2 = \frac{y(n-y)}{n^3}$

### Calculations
- [ ] Apply the 3-step Laplace procedure to a given unnormalised distribution
- [ ] Interpret the Gaussian approximation: sharper peak ⟹ smaller variance

---

## Week 4 — Variational Inference 📝 No formulas given

### Conceptual
- [x] State the goal of VI: approximate intractable posterior $p(\theta|D) \approx q(\theta)$
- [x] State the VI objective: $q^* = \arg\min_q \text{KL}(q(\theta) \| p(\theta|D))$ (reverse KL)
- [x] Explain why reverse KL is mode-seeking / mass-covering (see [[forward-vs-reverse-kl]])
- [ ] State what mean-field VI assumes: $q(\theta) = \prod_i q_i(\theta_i)$ (fully factorised)
- [ ] Explain CAVI (Coordinate Ascent VI): update one factor at a time, holding others fixed
- [ ] State one limitation of mean-field VI: underestimates posterior variance; can miss modes

### Derivation — **ELBO is the only examinable derivation** ⚠️
- [ ] **ELBO from KL decomposition:**
$$\log p(x) = \underbrace{\mathbb{E}_q[\log p(x,\theta)] - \mathbb{E}_q[\log q(\theta)]}_{\text{ELBO}} + \text{KL}(q\|\,p(\theta|x))$$
  Since $\text{KL} \geq 0$: $\text{ELBO} \leq \log p(x)$
- [ ] **ELBO rewritten as:**
$$\text{ELBO} = \mathbb{E}_q[\log p(x|\theta)] - \text{KL}(q(\theta)\|p(\theta))$$
  (reconstruction term − complexity penalty)
- [x] Show that maximising ELBO ≡ minimising $\text{KL}(q\|p_{\text{posterior}})$
- [ ] State Jensen's inequality path: $\log p(x) = \log \int p(x,\theta)d\theta \geq \mathbb{E}_q[\log p(x,\theta)/q(\theta)]$

### Calculations
- [ ] Given $q$ and $p$, compute ELBO or identify which term dominates
- [ ] Recognise the two-term structure of ELBO in the VAE setting

---

## Week 5 — MCMC 📝 No formulas given (derivations NOT examinable)

### Conceptual
- [x] Explain why exact Bayesian inference is often intractable (normalising constant)
- [ ] Explain the Monte Carlo estimator: $\mathbb{E}_p[f(\theta)] \approx \frac{1}{S}\sum_{s=1}^S f(\theta^{(s)})$; convergence $O(1/\sqrt{S})$
- [x] Explain rejection sampling: sample from proposal $q$, accept with probability $\tilde{p}(\theta^*)/Mq(\theta^*)$
- [x] Explain importance sampling: reweight proposal samples by $w(\theta) = \tilde{p}(\theta)/q(\theta)$
- [ ] State **one limitation of rejection and importance sampling each** ⚠️ Past exam Q
  *(Rejection: needs global envelope M; wastes many samples in high-D. Importance: weight degeneracy in high-D)*
- [ ] State the key difference between rejection and importance sampling ⚠️ Past exam Q
  *(Rejection discards; importance keeps all and reweights)*
- [x] Explain why MCMC is needed: fixed proposals fail in high dimensions; MCMC uses local proposals
- [ ] State the Metropolis-Hastings algorithm steps: propose $\theta^* \sim q(\theta^*|\theta^{(t)})$; accept with $A = \min\left(1, \frac{p(\theta^*)q(\theta^{(t)}|\theta^*)}{p(\theta^{(t)})q(\theta^*|\theta^{(t)})}\right)$
- [ ] Explain Metropolis as a special case of MH: symmetric proposal → $q$ terms cancel
- [ ] Explain Gibbs sampling: sample each variable from its full conditional; always accepts
- [ ] Compare Laplace / VI / MCMC ⚠️ Past exam Q — see [[mcmc-algorithms]]

### No derivations examinable

---

## Week 6 — Information Theory ✅ Formulas given (derivations NOT examinable)

### Conceptual + Formulas (given in exam)
- [x] **Information content:** $I(x) = -\log p(x)$ — rare events are more surprising
- [x] **Discrete entropy:** $H(X) = -\sum_x p(x)\log p(x)$ — average uncertainty
- [ ] **Differential entropy:** $H(X) = -\int p(x)\log p(x)\,dx$
- [ ] **Gaussian entropy:** $H = \frac{1}{2}\log(2\pi e\sigma^2)$ — depends only on $\sigma^2$
- [ ] **KL divergence:** $\text{KL}(p\|q) = \sum_x p(x)\log\frac{p(x)}{q(x)}$ — non-negative, asymmetric
- [ ] **Cross-entropy:** $H(p,q) = H(p) + \text{KL}(p\|q) = -\sum_x p(x)\log q(x)$
- [ ] **Conditional entropy:** $H(X|Y) = -\sum_{x,y} p(x,y)\log p(x|y)$
- [ ] **Mutual information:** $I(X;Y) = H(X) - H(X|Y) = \text{KL}(p(x,y)\|p(x)p(y))$
- [x] **Maximum entropy principle:** no constraints → Uniform; fixed mean+variance → Gaussian ⚠️
- [ ] Explain what KL divergence measures ⚠️ Past exam Q *(extra surprise / information lost when using $q$ instead of $p$)*
- [ ] Compare entropy of two Gaussians: entropy increases with $\sigma^2$; mean does not affect entropy ⚠️ Past exam Q

### Calculations
- [ ] Compute entropy given a distribution
- [ ] Compute KL divergence between two distributions
- [ ] Verify $H(p,q) = H(p) + \text{KL}(p\|q)$

---

## Week 7 — Hidden Markov Models 📝 No formulas given 🔒 GUARANTEED

> **Confirmed by lecturer:** "Every year, either the Viterbi or the Forward algorithm will be examined in depth." Prepare both to equal standard.

### HMM Structure — must know cold
- [x] State the HMM triple $\lambda = (A, B, \pi)$: transition matrix, emission matrix, initial distribution
- [ ] State the Markov assumption: $p(s_t | s_{t-1}, \ldots, s_1) = p(s_t | s_{t-1})$
- [ ] State output independence: $p(o_t | s_t, \ldots) = p(o_t | s_t)$
- [x] State the three HMM problems: Likelihood (Forward), Decoding (Viterbi), Learning (Baum-Welch — **NOT examinable**)
- [x] Read $A$, $B$, $\pi$ from a diagram / description and write them as matrices

### Forward Algorithm 🔒
- [ ] **Initialisation:** $\alpha_1(j) = \pi_j \cdot b_j(o_1)$
- [ ] **Recursion:** $\alpha_t(j) = \left[\sum_{i=1}^N \alpha_{t-1}(i)\,a_{ij}\right] b_j(o_t)$
- [ ] **Termination:** $P(O|\lambda) = \sum_{i=1}^N \alpha_T(i)$
- [ ] State complexity: $O(N^2 T)$ vs naïve $O(N^T)$ — explain why DP saves computation
- [ ] Complete a full numerical worked example (2-state, 3-observation) showing all $\alpha_t$ values

### Viterbi Algorithm 🔒
- [ ] **Initialisation:** $v_1(j) = \pi_j \cdot b_j(o_1)$
- [ ] **Recursion:** $v_t(j) = \left[\max_i\, v_{t-1}(i)\,a_{ij}\right] b_j(o_t)$; store backpointer $\psi_t(j) = \arg\max_i\, v_{t-1}(i)\,a_{ij}$
- [ ] **Termination:** $s_T^* = \arg\max_j\, v_T(j)$
- [ ] **Backtracking:** $s_{t-1}^* = \psi_t(s_t^*)$ for $t = T, T-1, \ldots, 2$
- [ ] Complete a full numerical worked example showing all $v_t$, $\psi_t$, and the backtracked path

### Forward vs Viterbi comparison
- [ ] $\sum$ (Forward, marginalise) vs $\max$ (Viterbi, select best path)
- [ ] Viterbi stores backpointers; Forward does not
- [ ] Both have $O(N^2 T)$ complexity; same initialisation

### Weather HMM reference — memorise structure
- [ ] $S=\{R,S\}$, $O=(\text{Walk, Shop, Clean})$, $\pi=(0.6, 0.4)$
- [ ] $P(O|\lambda) = 0.0336$ via Forward; best path $S\to R\to R$ via Viterbi

### Pitfalls to avoid
- [ ] Do not confuse $\sum$ and $\max$ in the recursion
- [ ] Always record backpointers $\psi_t$ during Viterbi — needed for backtracking
- [ ] Factor $b_j(o_t)$ outside the sum/max (it does not depend on $i$)
- [ ] Row = from, column = to when reading transition matrix $A$

---

## Week 8 — Variational Autoencoders 📝 No formulas given (derivations NOT examinable)

### Conceptual
- [x] Explain the vanilla autoencoder: $z = f_\theta(x)$, $\hat{x} = g_\phi(z)$; deterministic; no generative model
- [x] Explain the key problem with standard autoencoders: irregular latent space; cannot sample new data
- [ ] State the VAE model: encoder $q_\phi(z|x)$ (approximate posterior), decoder $p_\theta(x|z)$ (generative), prior $p(z) = \mathcal{N}(0,I)$
- [ ] State the VAE objective (ELBO):
$$\mathcal{L} = \mathbb{E}_{q_\phi}[\log p_\theta(x|z)] - \text{KL}(q_\phi(z|x)\|p(z))$$
- [ ] Explain the two terms: reconstruction loss + KL regulariser towards prior
- [ ] Explain the reparameterisation trick: $z = \mu + \sigma \odot \varepsilon$, $\varepsilon \sim \mathcal{N}(0,I)$ — makes sampling differentiable for backprop
- [ ] Distinguish AE (learn a representation) vs VAE (learn a probabilistic generative model)

---

## Week 9 — Reinforcement Learning 📝 No formulas given (derivations NOT examinable)

> Only **multi-armed bandits** and **Q-learning** are examinable.

### Conceptual
- [ ] State the five RL components: state $s$, action $a$, reward $r$, policy $\pi$, value $v$
- [ ] Explain exploration vs exploitation trade-off
- [ ] Explain the multi-armed bandit problem: stateless; no state transitions; goal = maximise cumulative reward
- [ ] State $\varepsilon$-greedy rule: with probability $\varepsilon$ explore (random action), else exploit (greedy)
- [ ] State the sample-average estimate: $Q_t(a) = \frac{\sum_{i=1}^{t-1} r_i \cdot \mathbf{1}[a_i=a]}{\sum_{i=1}^{t-1} \mathbf{1}[a_i=a]}$
- [ ] Define an MDP: $(S, A, P, R, \gamma)$ tuple; Markov property
- [ ] State the Bellman optimality equation: $Q^*(s,a) = r(s,a) + \gamma \sum_{s'} P(s'|s,a)\max_{a'} Q^*(s',a')$
- [ ] State the Q-learning update rule:
$$Q_t(s,a) = Q_{t-1}(s,a) + \alpha\left[r(s,a) + \gamma\max_{a'} Q(s',a') - Q_{t-1}(s,a)\right]$$
- [ ] Explain TD error: $\delta = r + \gamma\max_{a'} Q(s',a') - Q(s,a)$

### Calculations ⚠️
- [ ] **Bandit sample-average table** — given action/reward history, compute $Q_t(a)$ for each time step and identify when $\varepsilon$-greedy definitely explored
- [ ] **Q-learning update** — apply update rule step-by-step with given $\alpha$, $\gamma$; update Q-table entry by entry *(Week 10 example: $\alpha=0.6$, $\gamma=0.4$)*

---

## Cross-Cutting — Must Know

### Three approximation methods compared ⚠️ Past exam Q
- [x] **Laplace:** local Gaussian at MAP; fast; only one peak; assumes near-Gaussian shape
- [x] **Variational Inference:** global optimisation over a family; deterministic; can miss modes; underestimates variance
- [x] **MCMC:** samples from true posterior; no shape assumptions; slow; needs burn-in

### Generative vs Discriminative ⚠️ Past exam Q
- [ ] Generative: model $p(x,y)$; classify via Bayes' rule; examples — Naïve Bayes, HMM, VAE
- [ ] Discriminative: model $p(y|x)$ directly; examples — logistic regression, SVM, neural networks

### MLE vs MAP
- [x] MLE: maximises likelihood; no regularisation; OLS in regression
- [x] MAP: maximises likelihood + log-prior; regularisation; ridge regression with Gaussian prior

### KL Divergence — forward vs reverse
- [x] Forward KL $\text{KL}(p\|q)$: mass-covering; used in MLE
- [x] Reverse KL $\text{KL}(q\|p)$: mode-seeking; used in VI; explains underestimation of variance

---

## Quick-Reference: Formula Status Summary

| Week | Topic | Formula Status |
|------|-------|---------------|
| 1 | Bayesian inference, MLE, MAP | ✅ Distribution formulas given |
| 2 | Linear regression, classification | ✅ Distribution formulas given |
| 3 | Laplace approximation | 📝 Nothing given — know the 3 steps |
| 4 | Variational inference, ELBO | 📝 Nothing given — derive ELBO |
| 5 | MCMC, sampling methods | 📝 Nothing given — conceptual only |
| 6 | Information theory | ✅ Formulas given |
| 7 | HMMs (Forward + Viterbi only) | 📝 Nothing given — know recursions cold |
| 8 | VAEs | 📝 Nothing given — no derivations needed |
| 9 | Bandits + Q-learning only | 📝 Nothing given — know update rule |

---

## Derivations That May Be Directly Tested

| Derivation | Status | Key Result |
|------------|--------|-----------|
| MLE for Gaussian ($\mu$ and $\sigma^2$) | ⚠️ Highly likely | $\hat\mu = \bar{x}$, $\hat\sigma^2 = \frac{1}{n}\sum(x_i-\bar\mu)^2$ |
| MLE for Binomial | ⚠️ Highly likely | $\hat\theta = y/n$ |
| MAP for Gaussian (Gaussian prior) | ⚠️ Highly likely | Weighted average of prior mean and sample mean |
| Beta-Binomial conjugate update | ⚠️ Highly likely | $\alpha' = \alpha + y$, $\beta' = \beta + (n-y)$ |
| MLE for simple linear regression | ⚠️ Highly likely | $\hat{w} = \sum x_i y_i / \sum x_i^2$ |
| Normal Equations (multiple regression) | ⚠️ | $\hat{\mathbf{w}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$ |
| Laplace approximation procedure | ⚠️ Highly likely | Mode + second-derivative curvature |
| ELBO derivation | ⚠️ Highly likely | Via KL decomposition or Jensen's inequality |
| Forward algorithm recursion | 🔒 Guaranteed | $\alpha_t(j) = [\sum_i \alpha_{t-1}(i)\,a_{ij}]\,b_j(o_t)$ |
| Viterbi algorithm recursion | 🔒 Guaranteed | $v_t(j) = [\max_i v_{t-1}(i)\,a_{ij}]\,b_j(o_t)$ + backpointers |
| Q-learning update | ⚠️ Highly likely | $Q_t = Q_{t-1} + \alpha[\text{TD error}]$ |
