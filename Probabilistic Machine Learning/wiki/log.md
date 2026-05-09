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
