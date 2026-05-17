# PML Wiki — Log

*Append-only. Each entry: `## [YYYY-MM-DD] type | title`*
*Types: `ingest`, `query`, `lint`*

---

## [2026-05-03] setup | Wiki initialised

Scaffolded wiki base for COM3031 Probabilistic Machine Learning.
Created: `CLAUDE.md`, `wiki/overview.md`, `wiki/index.md`, `wiki/log.md`.
Directories: `wiki/concepts/`, `wiki/sources/`, `wiki/comparisons/`, `wiki/derivations/`.
18 source files ready in `raw/text/` (10 weekly lectures + 8 supplementary derivation notes).
No sources ingested yet.

## [2026-05-03] ingest | Full ingest — all 18 source files, Weeks 1–10

Ingested all 18 source files from `raw/text/`. Created 10 lecture source pages, 8 supplementary source pages, 37 concept pages, and 9 derivation pages.

**Source pages created (18):**
- `lecture-w1` through `lecture-w10` (all weekly lectures)
- `supp-beta-binomial`, `supp-map-gaussian`, `supp-mle-binomial`, `supp-mle-gaussian`
- `supp-mle-simple-linear-regression`, `supp-mle-multiple-linear-regression`
- `supp-elbo`, `supp-hmm-forward-viterbi`

**Concept pages created (37):**
Bayesian core: `bayesian-inference`, `mle`, `map`, `conjugate-priors`
Week 2: `linear-regression`, `logistic-regression`, `bayesian-linear-regression`, `generalised-linear-models`, `naive-bayes`, `generative-vs-discriminative`
Week 3: `laplace-approximation`, `bic`
Week 4: `variational-inference`, `elbo`, `kl-divergence`, `mean-field-vi`
Week 5: `mcmc`, `metropolis-hastings`, `gibbs-sampling`, `rejection-sampling`, `importance-sampling`, `monte-carlo-integration`
Week 6: `entropy`, `mutual-information`, `cross-entropy`, `maximum-entropy-principle`
Week 7/8: `hidden-markov-model`, `forward-algorithm`, `viterbi-algorithm`, `autoencoder`, `variational-autoencoder`, `reparameterization-trick`
Week 9: `reinforcement-learning`, `markov-decision-process`, `bellman-equation`, `q-learning`, `multi-armed-bandits`

**Derivation pages created (9):**
`mle-gaussian`, `mle-binomial`, `map-gaussian`, `beta-binomial-posterior`,
`mle-simple-linear-regression`, `mle-multiple-linear-regression`,
`elbo-derivation`, `forward-algorithm`, `viterbi-algorithm`

**Note:** Week 7/8 file labeling discrepancy observed — `COM3031_2526_Week7.txt` contains VAE content and `Week8.txt` contains HMM content (files appear swapped vs CLAUDE.md naming). Source pages reflect actual file content; concept pages use official exam week numbering per `lecture-w10` exam spec.

`index.md` fully populated with all 5 sections.

## [2026-05-09] query | Forward + Viterbi confirmed for May 2026 exam

Lecturer told the user that the Forward algorithm and Viterbi algorithm **will** appear on the exam. Created `wiki/likely-questions.md` to track guaranteed / highly-likely / possible questions, with full Forward + Viterbi rehearsal material (steps, Weather HMM worked example, common pitfalls, question-type list). Linked from `index.md` and flagged `🔒 Guaranteed` on `concepts/forward-algorithm.md`, `concepts/viterbi-algorithm.md`, and `sources/lecture-w10.md`.

## [2026-05-09] ingest | Create exams folder and restructure exam docs
- Created `wiki/exams/` directory.
- Created `wiki/exams/topics-and-formulas.md` with detailed formula policy and revision priorities.
- Moved `wiki/likely-questions.md` to `wiki/exams/likely-questions.md`.
- Updated `wiki/index.md` to reflect the new structure.
- Integrated specific "derive from scratch" requirements for Weeks 3-4 (Laplace, ELBO, Mean-field).

## [2026-05-09] ingest | Create practice questions directory
- Created `wiki/exams/practice-questions/` directory for active revision.
- Added first practice question: `w1-beta-binomial.md` (Reliability Analysis).
- Updated `wiki/index.md` with the new section.

## [2026-05-09] query | Compare MLE vs MAP for Linear Regression
- Created `wiki/comparisons/mle-vs-map.md` comparing point estimation methods.
- Detailed the OLS vs Ridge Regression connection.
- Updated `wiki/index.md` Comparisons section.

## [2026-05-09] query | Add Poisson regression and link functions synthesis
- Created `wiki/concepts/poisson-regression.md` to comprehensively explain the model for count data.
- Expanded `wiki/concepts/generalised-linear-models.md` with a narrative explanation of why link functions matter.
- Updated `wiki/index.md` with the new concept.

## [2026-05-09] query | Create practice question for Poisson MLE
- Created `wiki/exams/practice-questions/w2-poisson-regression-mle.md` focusing on Poisson GLM, link functions, and deriving the log-likelihood.
- Updated `wiki/index.md` with the new practice question.

## [2026-05-09] query | Synthesise Generative vs Discriminative Comparison
- Created `wiki/comparisons/generative-vs-discriminative.md` based on detailed user query.
- Moved and expanded content from the `concepts/` directory to the `comparisons/` directory for better structural alignment.
- Updated `wiki/index.md` and deleted redundant `wiki/concepts/generative-vs-discriminative.md`.

## [2026-05-09] query | Closed-form vs Iterative Solutions Synthesis
- Created `wiki/comparisons/closed-form-vs-iterative.md` detailing which models have exact analytical solutions and which require numerical optimisation/approximation.
- Updated `wiki/index.md` to track the new comparison page.

## [2026-05-09] query | Gaussian Naive Bayes & Variants
- Responded to query about GNB and its link to general NB.
- Created [[gaussian-naive-bayes]].
- Created [[naive-bayes-variants]] comparison.
- Updated [[index]] and [[overview]].

## [2026-05-09] query | Add Laplace approximation for Gamma distribution
- Created `wiki/derivations/laplace-gamma.md` based on Week 3 lecture worked exercise.
- Linked new derivation from `wiki/index.md` and `wiki/concepts/laplace-approximation.md`.

## [2026-05-10] query | Compare Forward vs Reverse KL divergence
- Created `wiki/comparisons/forward-vs-reverse-kl.md` comparing formulas, intuition (mode-seeking vs mass-covering), and use cases (VI vs MLE).
- Linked it to exams (highly examinable conceptual question).
- Updated `wiki/index.md` to include the new comparison page.


## [2026-05-10] query | Compare Importance Sampling vs Rejection Sampling
- Created `wiki/comparisons/importance-vs-rejection-sampling.md` comparing their core mechanisms, and discussing their shared failure mode in high dimensions.
- Updated `wiki/index.md` to link the new comparison.

## [2026-05-10] query | Compare MCMC Algorithms
- Created `wiki/comparisons/mcmc-algorithms.md` to provide a synthesis of Metropolis-Hastings, Metropolis, and Gibbs Sampling.
- Updated `wiki/index.md` to track the new comparison.

## [2026-05-15] query | Compare Forward vs Viterbi algorithms
- Created `wiki/comparisons/forward-vs-viterbi.md` synthesising both algorithms: same DP skeleton, $\sum$ vs $\max$ operator, when to use each, side-by-side worked Weather HMM example with sanity checks.
- Added cross-links from [[forward-algorithm]] and [[viterbi-algorithm]] concept pages.
- Updated `wiki/index.md` to track the new comparison.

## [2026-05-17] query | Create Week 9 RL revision plan
- Created `wiki/exams/week9-revision-plan.md` with a focused checklist, revision schedule, worked bandit example, worked Q-learning trace, conceptual model answer, and extra drills.
- Added `AGENTS.md` so Codex-style agents have a repo-specific instruction entry point while preserving the shared `CLAUDE.md` / `GEMINI.md` conventions.
- Updated `wiki/index.md` to link the new Week 9 revision page.

## [2026-05-17] query | Create Week 1-8 revision plans
- Created `wiki/exams/week1-revision-plan.md` for Bayesian inference, MLE, MAP, and conjugate priors, with formula-policy notes and derivation/practice priorities.
- Created `wiki/exams/week2-revision-plan.md` for linear regression and classification, covering simple and multiple linear regression, Bayesian/ridge links, GLMs, logistic regression, and Naive Bayes.
- Created `wiki/exams/week3-revision-plan.md` for Laplace approximation, including 1D Taylor derivation targets, MAP curvature checks, BIC/model comparison, and practice priorities.
- Created `wiki/exams/week4-revision-plan.md` for variational approximation, including ELBO derivation targets, reverse-KL intuition, mean-field/CAVI checks, and practice priorities.
- Created `wiki/exams/week5-revision-plan.md` for MCMC, with memorised algorithm/formula targets, worked Monte Carlo, rejection sampling, importance sampling, and Metropolis-Hastings examples.
- Created `wiki/exams/week6-revision-plan.md` for information theory, distinguishing provided formulas from required interpretation and calculation skills.
- Created `wiki/exams/week7-revision-plan.md` for HMMs, focused on memorising Forward and Viterbi recursions, termination, and backtracking.
- Created `wiki/exams/week8-revision-plan.md` for VAEs, focused on the generative model, approximate posterior, ELBO, reparameterization trick, and Gaussian KL.
- Updated `wiki/index.md` to link the new Week 1-8 revision pages.
- Created `wiki/exams/week1-revision-plan.md` for Bayesian inference, MLE, MAP, and conjugate priors, with formula-policy notes and derivation/practice priorities.
- Created `wiki/exams/week2-revision-plan.md` for linear regression and classification, covering simple and multiple linear regression, Bayesian/ridge links, GLMs, logistic regression, and Naive Bayes.
- Created `wiki/exams/week3-revision-plan.md` for Laplace approximation, including 1D Taylor derivation targets, MAP curvature checks, BIC/model comparison, and practice priorities.
- Created `wiki/exams/week4-revision-plan.md` for variational approximation, including ELBO derivation targets, reverse-KL intuition, mean-field/CAVI checks, and practice priorities.
- Updated `wiki/index.md` to link the new Week 1-4 revision pages.
