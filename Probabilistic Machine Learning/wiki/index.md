# PML Wiki — Master Index

*Updated on every ingest. Read this first when answering queries.*

---

## Exam Prep

- [[topics-and-formulas]] — **Read this first.** Breakdown of what to know, formula status (⚠️ vs ✅), and revision priorities.
- [[likely-questions]] — running tracker of guaranteed / highly-likely / possible exam questions. **🔒 Forward + Viterbi confirmed by lecturer.**
- [[w1-beta-binomial]] — **Beta–Binomial Reliability.** Week 1 practice on conjugacy and point estimates.
- [[w2-poisson-regression-mle]] — **Poisson Regression MLE.** Week 2 practice on GLMs, link functions, and log-likelihood.

---

## Concepts

- [[autoencoder]] — Deterministic encoder-decoder neural network; no generative capability
- [[baum-welch-algorithm]] — EM algorithm for unsupervised learning of HMM parameters
- [[bayesian-inference]] — Core framework: prior × likelihood → posterior; four components
- [[bayesian-linear-regression]] — Gaussian prior on weights; closed-form posterior; MAP = ridge regression
- [[bayesian-model-comparison]] — Framework to select models via marginal likelihood, penalising complexity
- [[bellman-equation]] — Recursive optimality condition for MDPs; foundation of Q-learning
- [[bic]] — Bayesian Information Criterion: Laplace approximation to log model evidence; penalises parameters
- [[conjugate-priors]] — Prior/likelihood pairs with closed-form posteriors; Beta-Binomial, Gaussian-Gaussian
- [[cross-entropy]] — H(p,q) = H(p) + KL(p||q); CE loss = negative log-likelihood for classification
- [[elbo]] — Evidence Lower Bound: ELBO = E_q[log likelihood] − KL(q||prior); maximising ELBO ≡ VI
- [[entropy]] — Measure of uncertainty; discrete, differential, and Gaussian forms
- [[forward-algorithm]] — HMM algorithm for P(O|λ) via dynamic programming; O(N²T)
- [[gaussian-naive-bayes]] — Extension of NB for continuous features using Gaussian PDFs
- [[generalised-linear-models]] — Linear predictor + link function + exponential-family distribution; unifies regression models
- [[gibbs-sampling]] — MCMC via exact conditionals; always accepts; requires tractable full conditionals
- [[hidden-markov-model]] — λ = (A, B, π); forward algorithm, Viterbi; evaluation and decoding problems
- [[importance-sampling]] — Reweight proposal samples by importance ratio; fails in high dimensions
- [[information-content]] — Measure of surprise for an event: I(x) = -log P(x)
- [[kl-divergence]] — KL(q||p) = reverse (mode-seeking, used in VI); asymmetric; non-negative
- [[laplace-approximation]] — Fit Gaussian at MAP via Hessian curvature; BIC derived from this
- [[likelihood]] — Probability of data given parameters, P(D|θ); building block of MLE/MAP
- [[linear-regression]] — Gaussian noise model; MLE = OLS; Normal Equations for multiple regression
- [[logistic-regression]] — Bernoulli GLM with logit link; trained by MLE (no closed form)
- [[map]] — Posterior mode; MAP with Gaussian prior = ridge regression; weighted average result
- [[markov-decision-process]] — (S, A, P, R, γ) tuple; Markov property; Bellman optimality equations
- [[maximum-entropy-principle]] — Choose distribution with highest entropy given known constraints; Gaussian maximises entropy for fixed mean+variance
- [[mcmc]] — Markov chain Monte Carlo: MH, Metropolis, Gibbs; samples from intractable posteriors
- [[mean-field-vi]] — Fully factorised q; CAVI updates; underestimates posterior variance
- [[metropolis-hastings]] — MCMC with accept/reject; A = target ratio × proposal correction; detailed balance
- [[mle]] — Maximum likelihood: argmax log p(D|θ); results for Gaussian, Binomial, linear regression
- [[monte-carlo-integration]] — Sample-average estimator; O(1/√S) convergence; dimension-independent
- [[multi-armed-bandits]] — Stateless RL; ε-greedy exploration; sample-average estimates; regret minimisation
- [[mutual-information]] — I(X;Y) = H(X) − H(X|Y) = KL between joint and product of marginals
- [[naive-bayes]] — Generative classifier; conditional independence assumption; p(y)∏p(xj|y)
- [[poisson-regression]] — GLM for count data using the Poisson distribution and log link function
- [[q-learning]] — Model-free off-policy RL; TD error update rule; converges to Q* via Bellman equation
- [[reinforcement-learning]] — Framework: agent, environment, state, action, reward, policy; exploration vs exploitation
- [[rejection-sampling]] — Accept proposal with probability ∝ target/proposal; fails in high dimensions
- [[reparameterization-trick]] — z = μ + σ⊙ε; enables backprop through sampling in VAE
- [[variational-autoencoder]] — Generative model: encoder q_φ(z|x), decoder p_θ(x|z); trained via ELBO
- [[variational-inference]] — Approximate posterior by optimising ELBO; reverse KL minimisation
- [[viterbi-algorithm]] — HMM decoding: most probable state sequence via max DP + backtracking

---

## Sources — Lectures

- [[lecture-w1]] — Week 1: Bayesian inference, MLE, MAP, conjugate priors (Beta-Binomial, Gaussian)
- [[lecture-w2]] — Week 2: Linear regression, logistic regression, Naive Bayes, GLMs, generative vs discriminative
- [[lecture-w3]] — Week 3: Laplace approximation, BIC, Bayesian model comparison
- [[lecture-w4]] — Week 4: Variational inference, KL divergence, ELBO, mean-field VI
- [[lecture-w5]] — Week 5: MCMC, Monte Carlo integration, rejection sampling, importance sampling, MH, Gibbs
- [[lecture-w6]] — Week 6: Information theory — entropy, mutual information, KL divergence, cross-entropy, max entropy
- [[lecture-w7]] — Week 7 file: autoencoders and VAEs (file content; exam calls this Week 8)
- [[lecture-w8]] — Week 8 file: HMMs, forward algorithm, Viterbi (file content; exam calls this Week 7)
- [[lecture-w9]] — Week 9: Reinforcement learning, multi-armed bandits, MDPs, Q-learning
- [[lecture-w10]] — Week 10: Exam specification, examinable topics, worked past-exam solutions

---

## Sources — Supplementary Notes

- [[supp-beta-binomial]] — Beta-Binomial conjugate posterior derivation; posterior mean interpretation
- [[supp-map-gaussian]] — MAP for Gaussian likelihood with Gaussian prior; weighted-average result
- [[supp-mle-binomial]] — MLE for Binomial: θ̂ = y/n
- [[supp-mle-gaussian]] — MLE for Gaussian: μ̂ = sample mean, σ̂² = biased sample variance
- [[supp-mle-simple-linear-regression]] — MLE for simple linear regression: ŵ = Σxᵢyᵢ/Σxᵢ²
- [[supp-mle-multiple-linear-regression]] — MLE for multiple linear regression: Normal Equations ŵ = (X'X)⁻¹X'y
- [[supp-elbo]] — ELBO derivation via Jensen's inequality and KL decomposition
- [[supp-hmm-forward-viterbi]] — HMM forward and Viterbi algorithms with full numerical Weather HMM example

---

## Derivations

- [[beta-binomial-posterior]] — Beta-Binomial conjugate update; pseudo-counts interpretation
- [[elbo-derivation]] — ELBO from Jensen and from KL decomposition; two equivalent forms
- [[forward-algorithm]] — HMM forward variable recursion; O(N²T) derivation + worked example
- [[laplace-gamma]] — Laplace approximation for a Gamma distribution; Week 3 worked exercise
- [[map-gaussian]] — MAP for Gaussian mean; weighted average of sample mean and prior mean
- [[mle-binomial]] — MLE for Binomial: differentiate log-likelihood, solve θ̂ = y/n
- [[mle-gaussian]] — MLE for Gaussian: μ̂ and σ̂² (biased); full step-by-step
- [[mle-multiple-linear-regression]] — Normal Equations via matrix calculus; result (X'X)⁻¹X'y
- [[mle-simple-linear-regression]] — OLS derivation for simple LR; ŵ = Σxᵢyᵢ/Σxᵢ²; worked example
- [[viterbi-algorithm]] — Viterbi variable; max DP + backtracking; worked Weather HMM example

---

## Comparisons & Synthesis

- [[importance-vs-rejection-sampling]] — Importance Sampling vs Rejection Sampling; how they handle proposal mismatch and why both fail in high dimensions.
- [[forward-vs-reverse-kl]] — Forward (mass-covering) vs Reverse (mode-seeking, used in VI) KL divergence.
- [[generative-vs-discriminative]] — Differences in p(x,y) vs p(y|x); Naive Bayes vs Logistic Regression
- [[mle-vs-map]] — MLE (OLS) vs MAP (Ridge Regression); pros, cons, and when to use each.
- [[naive-bayes-variants]] — Comparison of Gaussian, Bernoulli, and Multinomial Naive Bayes.
- [[closed-form-vs-iterative]] — Models with analytical solutions vs those requiring numerical approximation.

