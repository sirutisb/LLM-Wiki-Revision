# Week 8 — Hidden Markov Models

**File:** `raw/text/COM3031_2526_Week8.txt`
**Type:** lecture
**Week:** 8
**Concepts introduced:** [[hidden-markov-model]], [[forward-algorithm]], [[viterbi-algorithm]], [[baum-welch-algorithm]]

> **Note on week labelling:** The exam overview (Week 10) lists Week 7 = Hidden Markov Models. However, the lecture slides file `COM3031_2526_Week8.txt` contains the HMM content. This source page describes the actual file content. For exam purposes, treat HMM content as "Week 7" per the official overview. See [[lecture-w7]] for VAEs.

## Summary
This lecture extends the Bayesian latent variable framework to sequential data. A Markov chain models temporal dependence; Hidden Markov Models (HMMs) add hidden (unobservable) states that generate observations. Three fundamental problems are defined: likelihood evaluation (Forward algorithm), decoding (Viterbi algorithm), and parameter learning (Baum–Welch). Only the Forward and Viterbi algorithms are examinable.

## Key content

### Sequential Data and the Markov Assumption
- i.i.d. assumption breaks for sequential data (speech, text, finance, weather).
- **First-order Markov assumption**: $p(o_t|o_1,\ldots,o_{t-1}) = p(o_t|o_{t-1})$.
- Joint distribution: $p(o_1,\ldots,o_T) = p(o_1)\prod_{t=2}^T p(o_t|o_{t-1})$.
- **Homogeneous chain**: transition probabilities time-invariant.

### HMM Definition
A Hidden Markov Model $\lambda = (A, B, \pi)$:
- **Hidden states**: $s_t \in \{1,\ldots,N\}$, not directly observable.
- **Observations**: $o_t \in \{1,\ldots,M\}$, generated from hidden state.
- **$A$** (transition matrix): $a_{ij} = P(s_t = j|s_{t-1} = i)$; rows sum to 1.
- **$B$** (emission matrix): $b_j(o) = P(o_t = o|s_t = j)$; rows sum to 1.
- **$\pi$** (initial distribution): $\pi_i = P(s_1 = i)$; sums to 1.

Key assumptions:
- Hidden states are mutually exclusive (one active per time step).
- Observations are conditionally independent given the current hidden state.

Joint distribution:
$$p(s_{1:T}, o_{1:T}) = \pi_{s_1}\prod_{t=2}^T a_{s_{t-1}s_t}\prod_{t=1}^T b_{s_t}(o_t)$$

### Three Fundamental Problems

**Problem 1 — Likelihood (Forward Algorithm)**
- Goal: compute $P(O|\lambda)$ for observation sequence $O = o_1,\ldots,o_T$.
- Naïve: enumerate all $N^T$ state sequences — exponential.
- **Forward variable**: $\alpha_t(i) = P(o_1,\ldots,o_t, s_t=i|\lambda)$.
- Initialisation: $\alpha_1(j) = \pi_j b_j(o_1)$.
- Recursion: $\alpha_t(j) = \left[\sum_i \alpha_{t-1}(i)a_{ij}\right] b_j(o_t)$.
- Termination: $P(O|\lambda) = \sum_i \alpha_T(i)$.
- Complexity: $O(N^2T)$ vs naïve $O(N^T)$.

**Problem 2 — Decoding (Viterbi Algorithm)**
- Goal: find most likely hidden state sequence $S^* = \arg\max_S P(S|O,\lambda)$.
- **Viterbi variable**: $v_t(j) = \max_{s_1,\ldots,s_{t-1}} P(s_1,\ldots,s_{t-1}, s_t=j, o_1,\ldots,o_t|\lambda)$.
- Initialisation: $v_1(j) = \pi_j b_j(o_1)$.
- Recursion: $v_t(j) = \left[\max_i v_{t-1}(i)a_{ij}\right] b_j(o_t)$.
- Backpointer: $\psi_t(j) = \arg\max_i v_{t-1}(i)a_{ij}$.
- Termination: $s_T^* = \arg\max_j v_T(j)$; backtrack via $\psi$.
- Difference from Forward: max instead of sum.

**Problem 3 — Learning (Baum–Welch)**
- Goal: estimate $\lambda = (A,B,\pi)$ from observations only (hidden states unknown).
- Special case of EM (Expectation-Maximisation).
- E-step: compute $\gamma_t(i) = P(s_t=i|O,\lambda)$ and $\xi_t(i,j) = P(s_t=i, s_{t+1}=j|O,\lambda)$ using Forward–Backward.
- M-step: update $a_{ij}$, $b_j(o)$, $\pi_i$ using expected counts.
- **NOT examinable**.

## Key takeaways
- HMM = latent variable model for sequential data with Markov structure.
- Forward algorithm (sum over all paths) vs Viterbi (max over all paths) — both use dynamic programming.
- Forward: sums over all possible hidden sequences to compute total likelihood.
- Viterbi: uses max and backpointers to find the single best hidden sequence.
- Both have complexity $O(N^2T)$ via dynamic programming.

## Exam relevance
- Forward and Viterbi algorithms: **examinable** (can be asked to compute).
- Numerical worked examples with small HMMs: **examinable** (past exam questions).
- Transition/emission/initial matrices: **examinable**.
- Baum–Welch: NOT examinable.
- Derivations: NOT examinable.
- No formulas given; but the algorithm steps must be known from memory.

## Links to concepts
- [[hidden-markov-model]]: introduced here
- [[forward-algorithm]]: derived here
- [[viterbi-algorithm]]: derived here
- [[baum-welch-algorithm]]: introduced (not examinable)
- [[mcmc]]: Markov chains from [[lecture-w5]] extended here
- [[variational-autoencoder]]: previous latent variable model ([[lecture-w7]])
