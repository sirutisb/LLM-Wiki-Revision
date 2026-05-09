# Likely Exam Questions — COM3031

**Purpose:** running tracker of question types that are confirmed, near-confirmed, or strongly hinted to appear in the May 2026 exam. Read alongside [[lecture-w10]] (the official exam spec) and the per-concept "Exam notes" sections.

**Legend:**
- 🔒 **Guaranteed** — confirmed by lecturer / explicitly flagged "will be in the exam".
- ⚠️ **Highly likely** — flagged in Week 10 review or appeared in past papers with a worked solution.
- 🟡 **Possible** — listed as examinable but not heavily hinted.

---

## 🔒 Guaranteed — HMM Forward / Viterbi (Week 7)

> **Confirmed by lecturer (Week 7 lecture transcript, reviewed 2026-05-09).** Direct exam statements (timestamps from the recording):
> - **[15:52–16:19]** *"these algorithms [are] examinable in the final exam."*
> - **[24:38–25:17]** *"every year, either the Viterbi algorithm or the forward algorithm will be examined in depth in the final exam paper."* + *"you are allowed to use non-programmable calculators in the final exam."*
> - **[44:05–44:20]** *"in the final exam you can be asked either to perform Viterbi algorithm or the forward algorithm."*
>
> Indirect but useful exam hints:
> - **[25:49–26:09]** detailed recursive calculations are uploaded — confirms [[supp-hmm-forward-viterbi]] is the canonical worked example to memorise.
> - **[26:35–26:40]** *"if you cannot understand this transformation then it's very less likely you can implement the forward [algorithm]"* — reinforces that converting $A, B, \pi$ ↔ transition diagram is a prerequisite skill, not an optional one.
> - **[53:21–53:25]** *"next week, the workshop, you're going to perform the forward algorithm…"* — workshop drills Forward end-to-end. This does **not** lower Viterbi's exam probability; the lecturer's "either…or" wording at 24:38 and 44:05 still governs.

**Read the wording carefully:** *either … or* — historically **one** of the two appears in depth each year, **not both**. Since the choice is unknown until exam day, **prepare both algorithms to the same standard**.

Closed-book, **no formulas given** — algorithm steps must be reproduced from memory ⚠️. Expect a **full numerical worked example** in the style of the Weather HMM (see [[supp-hmm-forward-viterbi]]) with steps explicitly labelled *initialisation → recursion → termination* (and *backtracking* for Viterbi).

### The three HMM problems (memorise this framing)

| Problem | Goal | Algorithm | Examinable? |
|---------|------|-----------|-------------|
| **Likelihood** | $P(O\mid\lambda)$ | Forward | 🔒 in depth (one of two) |
| **Decoding** | $\arg\max_S P(S\mid O, \lambda)$ | Viterbi | 🔒 in depth (one of two) |
| **Learning** | Estimate $\lambda$ from $O$ | Baum–Welch (EM) | ❌ not examinable |

### What to be able to do under exam conditions

1. **State the HMM components.** Given a description or diagram, write down $\lambda = (A, B, \pi)$:
   - $\pi$ — initial state distribution.
   - $A$ — transition matrix, $a_{ij} = P(s_{t+1} = j \mid s_t = i)$.
   - $B$ — emission matrix, $b_j(o) = P(o \mid s_t = j)$.
   - State the Markov assumption and output-independence assumption.

2. **Forward algorithm — reproduce all three steps:**
   - Initialisation: $\alpha_1(j) = \pi_j\, b_j(o_1)$.
   - Recursion: $\alpha_t(j) = \left[\sum_{i=1}^N \alpha_{t-1}(i)\, a_{ij}\right] b_j(o_t)$.
   - Termination: $P(O \mid \lambda) = \sum_{i=1}^N \alpha_T(i)$.
   - Complexity: $O(N^2 T)$, vs naïve $O(N^T)$.

3. **Viterbi algorithm — reproduce all four steps (incl. backtracking):**
   - Initialisation: $v_1(j) = \pi_j\, b_j(o_1)$.
   - Recursion: $v_t(j) = \left[\max_{i} v_{t-1}(i)\, a_{ij}\right] b_j(o_t)$, with backpointer $\psi_t(j) = \arg\max_i v_{t-1}(i)\, a_{ij}$.
   - Termination: $s_T^* = \arg\max_j v_T(j)$.
   - Backtracking: $s_{t-1}^* = \psi_t(s_t^*)$ for $t = T, T-1, \ldots, 2$.

4. **Numerical calculation.** Carry the arithmetic on a 2-state HMM over 3 observations without skipping intermediate values — graders expect to see each $\alpha_t(j)$ / $v_t(j)$ written out. ⚠️ *Backpointers must be recorded explicitly during Viterbi.*

5. **Compare Forward vs Viterbi.** $\sum$ vs $\max$; same initialisation; Viterbi additionally stores backpointers; Forward gives total likelihood, Viterbi gives the most-probable path. Be ready to **explain *why*** Forward sums (marginalising over hidden states) while Viterbi maxes (selecting one path).

6. **Draw the transition / trellis diagram.** Lecturer at [26:35] flagged the matrix↔diagram conversion as a **prerequisite** for being able to run the algorithm (*"if you cannot understand this transformation then it's very less likely you can implement the forward [algorithm]"*). Be able to convert $A$, $B$, $\pi$ into a state-transition diagram (nodes = states, labelled arrows = $a_{ij}$ and emission probs) and into a $T \times N$ trellis with arrows showing the DP updates. Drawing the trellis on the exam script keeps bookkeeping visible and earns method marks even if the arithmetic slips.

### Reference worked example (memorise the structure)

**Weather HMM:** $S=\{R,S\}$, $O=(\text{Walk}, \text{Shop}, \text{Clean})$, $\pi=(0.6, 0.4)$,
$$A=\begin{pmatrix}0.7 & 0.3\\ 0.4 & 0.6\end{pmatrix},\qquad B=\begin{array}{c|ccc} & W & Sh & C\\\hline R & 0.1 & 0.4 & 0.5\\ S & 0.6 & 0.3 & 0.1\end{array}$$

| Step | Forward $\alpha_t$ | Viterbi $v_t$ (with $\psi_t$) |
|------|--------------------|------------------------------|
| $t=1$ | $\alpha_1(R)=0.06$, $\alpha_1(S)=0.24$ | $v_1(R)=0.06$, $v_1(S)=0.24$ |
| $t=2$ | $\alpha_2(R)=0.0552$, $\alpha_2(S)=0.0486$ | $v_2(R)=0.0384\;[\psi=S]$, $v_2(S)=0.0432\;[\psi=S]$ |
| $t=3$ | $\alpha_3(R)=0.02904$, $\alpha_3(S)=0.004572$ | $v_3(R)=0.01344\;[\psi=R]$, $v_3(S)=0.002592\;[\psi=S]$ |
| **End** | $P(O\mid\lambda)=\mathbf{0.0336}$ | best path: $\mathbf{S \to R \to R}$ |

Full arithmetic: [[supp-hmm-forward-viterbi]]. Concept pages: [[forward-algorithm]], [[viterbi-algorithm]].

### Common pitfalls

- Confusing $\sum$ (Forward) with $\max$ (Viterbi) in the recursion.
- Forgetting to record backpointers during Viterbi → cannot recover the sequence.
- Re-multiplying $b_j(o_t)$ inside the sum/max instead of factoring it out (it does not depend on $i$).
- Reading $A$ in the wrong direction — fix the convention "row = from, col = to" once and stick with it.
- Skipping the termination/backtracking step and reporting only the score.

### Question types to rehearse

- **Bookwork:** "State the forward variable $\alpha_t(j)$ in words and give the recursion." (3-4 marks)
- **Bookwork:** "Explain how the Viterbi algorithm differs from the Forward algorithm." (2-3 marks)
- **Calculation:** Given $A$, $B$, $\pi$ and a 3-step observation sequence, compute $P(O\mid\lambda)$ via Forward. (8-10 marks)
- **Calculation:** Same setup, find the most likely state sequence via Viterbi, showing $v_t$, $\psi_t$, and backtracking. (8-12 marks)
- **Conceptual:** "Why does the algorithm reduce $O(N^T)$ to $O(N^2 T)$?" — DP reuse of $\alpha_{t-1}(i)$.

---

## ⚠️ Highly likely — based on Week 10 review and past papers

These were either walked through in [[lecture-w10]] as worked exam solutions, or explicitly flagged as examinable derivations.

### Week 1 — Bayesian inference
- Derive **MLE for univariate Gaussian** (mean and biased variance) from scratch. ⚠️ no formulas given for the *steps* — see [[mle-gaussian]].
- Derive **MAP for univariate Gaussian** with Gaussian prior; state the weighted-average result. See [[map-gaussian]], [[map-univariate-gaussian]].
- "What is a conjugate prior? State one advantage." Bookwork — see [[conjugate-priors]].
- **Poisson–Gamma update** (Week 10 worked example): given $n=1, y=10, \alpha=25, \beta=3$, find posterior parameters and $\mathbb{E}[\lambda \mid y]$.

### Week 2 — Regression & classification
- Derive **MLE for simple linear regression**: $\hat{w} = \sum x_i y_i / \sum x_i^2$. See [[mle-simple-linear-regression]].
- "Why is $\log$ not a suitable link function for logistic regression?" Bookwork — see [[logistic-regression]].
- Generative vs discriminative comparison; Naïve Bayes assumption — see [[generative-vs-discriminative]], [[naive-bayes]].

### Week 3 — Laplace approximation
- "Main use and one limitation of Laplace approximation." Bookwork — see [[laplace-approximation]].
- **Worked Laplace example** (Week 10): given $p(\theta\mid y) \propto \theta^y(1-\theta)^{n-y}$, find MAP $\hat{\theta}=y/n$ and Laplace variance $\sigma^2 = y(n-y)/n^3$.

### Week 4 — Variational inference
- Derive the **ELBO** from KL decomposition; state ELBO = $\mathbb{E}_q[\log p(x \mid z)] - \mathrm{KL}(q\Vert p)$. See [[elbo-derivation]], [[supp-elbo]].
- "Why does maximising ELBO equal minimising KL$(q\Vert p)$?" — show $\log p(x) = \mathrm{ELBO} + \mathrm{KL}(q\Vert p_{\text{posterior}})$.

### Week 6 — Information theory
- Compute / compare entropy of two given distributions. ✅ formulas given.
- Show $H(p,q) = H(p) + \mathrm{KL}(p\Vert q)$. See [[cross-entropy]].

### Week 9 — Reinforcement learning
- **Q-learning update** numerical example (Week 10 walkthrough): with $\alpha=0.6$, $\gamma=0.4$, update Q-table from given transitions.
- $\varepsilon$-greedy action selection; sample-average bandit estimates — see [[multi-armed-bandits]].

---

## 🟡 Possible — examinable but lighter hints

- **Week 5 (MCMC):** Compare Laplace / VI / MCMC. Rejection vs importance sampling — one limitation each. MH algorithm steps conceptually. Derivations *not* examinable.
- **Week 8 (VAE):** AE vs VAE; ELBO structure; reparameterisation trick conceptually. No derivations examinable.

---

## How to use this page during revision

1. Treat 🔒 items as **must-pass under timed conditions**. Do the Weather HMM worked example with paper and pen, no notes, until you can reach $0.0336$ and $S\to R\to R$ without hesitation.
2. Treat ⚠️ items as core revision targets — every one has a derivation page or worked example linked above.
3. Treat 🟡 items as conceptual filler — make sure you can describe them in two or three sentences each.

## Update log
- **2026-05-09** — page created. Forward + Viterbi confirmed as guaranteed by lecturer.
- **2026-05-09** — refined HMM section after re-reading lecture transcript: "every year, **either** Viterbi **or** Forward will be examined in depth" → one of the two per paper, both must be prepared. Added three-problems framing (Likelihood / Decoding / Learning), trellis-diagram skill, and direct lecturer quotes.
- **2026-05-09** — added timestamp citations (15:52, 24:38, 26:35, 44:05, 53:21) so each lecturer quote is auditable against the recording. Noted that the Week 8 workshop drills Forward; this does not bias the exam choice — "either…or" still governs.
