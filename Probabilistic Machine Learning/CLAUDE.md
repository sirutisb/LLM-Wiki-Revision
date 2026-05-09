# PML Wiki — Schema & Conventions

## What this is
A personal revision wiki for **COM3031 – Probabilistic Machine Learning** at the University of Exeter (Term 2, 2025-2026), taught by Dr Zeyu Fu. The wiki is built and maintained by Claude; the human curates sources and asks questions.

**Exam:** 2-hour closed-book written exam in May 2026 (70% of grade). Answer all questions. Scientific calculators permitted. Three question types: conceptual/bookwork, selected derivations, practical problem-solving.

**Formula sheet policy (critical for exam notes):**
- Week 1–2: distribution formulas *will* be given
- Weeks 3–9: *no* formulas given — must know derivations and results from memory

## Directory layout

```
raw/                   # Immutable source PDFs + extracted text (never modify)
  text/                # One .txt per PDF — page boundaries as "--- page N ---"
wiki/                  # LLM-generated markdown (you own this entirely)
  index.md             # Master catalog — updated on every ingest
  log.md               # Append-only chronological record
  overview.md          # High-level module map and topic relationships
  concepts/            # One page per algorithm, model, or concept
  sources/             # One page per lecture or supplementary note
  comparisons/         # Cross-cutting comparisons and synthesis pages
  derivations/         # Step-by-step derivations for exam-critical results
CLAUDE.md              # This file — conventions and workflows
```

## Source files

### Weekly lecture slides (main content)
| File | Topic |
|------|-------|
| `COM3031_2526_W1.txt` | Intro + Bayesian Inference |
| `COM3031_2526_week2.txt` | Linear Regression & Classification |
| `COM3031_2526_Week3.txt` | Laplace Approximation |
| `COM3031_2526_Week4.txt` | Variational Approximation |
| `COM3031_2526_Week5.txt` | MCMC |
| `COM3031_2526_Week6.txt` | Information Theory |
| `COM3031_2526_Week7.txt` | Hidden Markov Models |
| `COM3031_2526_Week8.txt` | Variational Autoencoders |
| `COM3031_2526_Week9.txt` | Reinforcement Learning |
| `COM3031_2526_Week10_Summary.txt` | Exam prep + course review |

### Supplementary derivation notes (detailed worked maths)
| File | Topic |
|------|-------|
| `COM3031_W1_Beta_Binomial.txt` | Beta-Binomial conjugate pair |
| `COM3031_W1_MAP4Gaussian.txt` | MAP for Gaussian |
| `COM3031_W1_MLE4Binomial.txt` | MLE for Binomial |
| `COM3031_W1_MLE4Gaussian.txt` | MLE for Gaussian |
| `COM3031_W2_MLE4Simple_linear_regression.txt` | MLE for simple linear regression |
| `COM3031_W2_MLE4Multiple_linear_regression.txt` | MLE for multiple linear regression |
| `COM3031_W4_ELBO.txt` | ELBO derivation |
| `COM3031_W8_HMM_Forward and Viterbi Algorithms.txt` | HMM forward and Viterbi algorithms |

## Page formats

### Concept page (`concepts/*.md`)
```
# [Concept Name]

**Type:** model | algorithm | principle | approximation method | framework
**Week:** N
**Related:** [[other-concept]], [[another-concept]]
**Source:** [[lecture-wN]], [[supp-filename]]

## Definition
One precise sentence.

## Motivation
The problem it addresses; why simpler approaches fail.

## How it works
Core mechanism, key equations in LaTeX. For generative models: specify the generative process.

## Key derivation
The main mathematical result — set up, key steps, final form.
Flag as: ⚠️ *No formula given in exam* or ✅ *Formula sheet provided*.

## Parameters & intuition
What each parameter/hyperparameter controls. How to set or interpret them.

## Worked example sketch
A brief concrete example or the type of numerical question that appears in the exam.

## Connections
- Builds on [[concept]]
- Compare with [[concept]]
- Generalised by [[concept]]

## Exam notes
- What is likely to be asked (derivation vs conceptual vs calculation)
- Common exam pitfalls
- Formula status: given / not given
```

### Source page (`sources/*.md`)
```
# [Week N — Title] (or: Supp — Title)

**File:** `raw/text/[filename].txt`
**Type:** lecture | supplementary-note
**Week:** N
**Concepts introduced:** [[concept-1]], [[concept-2]]

## Summary
2–4 sentences on the lecture's main contribution.

## Key content
### [Section heading]
Concise notes with equations where needed.

## Key takeaways
Bullet points — the things to remember.

## Exam relevance
What from this source is explicitly examinable, and in what question type.

## Links to concepts
- [[concept-1]]: introduced here
- [[concept-2]]: expanded from [[lecture-wN]]
```

### Derivation page (`derivations/*.md`)
```
# Derivation: [Result Name]

**Used in:** [[concept-1]]
**Source:** [[supp-filename]] or [[lecture-wN]]
**Exam status:** ⚠️ Must know / ✅ Formula given

## Setup
State the problem and what we're deriving.

## Steps
Numbered steps with full LaTeX. Explain each non-obvious move.

## Result
The final expression, boxed or highlighted.

## Intuition
Why the result makes sense — geometric, probabilistic, or limiting-case intuition.
```

### Comparison page (`comparisons/*.md`)
```
# [A] vs [B]  (or: [Topic] — Synthesis)

## Overview
What is being compared and why it matters for the exam.

## Comparison table
| Dimension | A | B |
|-----------|---|---|

## When to use which
...

## Synthesis
The deeper insight the comparison reveals.
```

## Index conventions
`index.md` has six sections: Exam Prep, Concepts, Sources — Lectures, Sources — Supplementary Notes, Derivations, Comparisons & Synthesis. Each entry is one line: `- [[filename]] — one-line summary`.

## Log conventions
Each log entry starts with `## [YYYY-MM-DD] type | title` where type is `ingest`, `query`, or `lint`. Greppable with `grep "^## \["`.

## Ingest workflow
1. Read the source `.txt` file from `raw/text/`
2. Create a source page in `sources/`
3. Create or update affected concept pages in `concepts/`
4. For supplementary derivation notes: also create a page in `derivations/`
5. Update `index.md`
6. Append to `log.md`

Ingest supplementary notes alongside their parent lecture (e.g. ingest all W1 files together).

## Query workflow
1. Read `index.md` to find relevant pages
2. Read the relevant concept/source/derivation/comparison pages
3. Synthesise an answer with citations to wiki pages
4. If the answer is broadly useful (a comparison, a synthesis, a practice question with solution), file it as a new page

## Lint checklist
- Orphan pages (no inbound links)
- Concept pages missing "Exam notes" or "Key derivation" sections
- Missing formula-status flags (⚠️ / ✅)
- Broken `[[wikilinks]]`
- Concepts mentioned in source pages but lacking their own concept page

## Wikilinks
Use `[[filename-without-extension]]` for internal links. Filenames: lowercase hyphenated. Lecture sources: `lecture-w1`, `lecture-w2`, … Supplementary sources: `supp-beta-binomial`, `supp-mle-gaussian`, etc.

## Equations
Use `$...$` for inline and `$$...$$` for display math. Align multi-line derivations with `\begin{align}...\end{align}`.

## Revision priority
Ordered by exam weight (derived from Week 10 exam overview):
1. Bayesian inference (MLE, MAP, conjugate priors) — Week 1
2. Linear regression & classification — Week 2
3. Variational inference & ELBO — Week 4
4. HMMs (forward + Viterbi only) — Week 7
5. Laplace approximation — Week 3
6. MCMC — Week 5
7. Information theory — Week 6
8. VAEs — Week 8
9. Reinforcement learning (bandits + Q-learning only) — Week 9
orward + Viterbi only) — Week 7
5. Laplace approximation — Week 3
6. MCMC — Week 5
7. Information theory — Week 6
8. VAEs — Week 8
9. Reinforcement learning (bandits + Q-learning only) — Week 9
