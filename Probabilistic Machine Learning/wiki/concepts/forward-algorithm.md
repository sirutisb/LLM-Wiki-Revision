# Forward Algorithm

**Type:** algorithm
**Week:** 7 (exam numbering)
**Related:** [[hidden-markov-model]], [[viterbi-algorithm]]
**Source:** [[lecture-w8]], [[supp-hmm-forward-viterbi]]

## Definition
The Forward Algorithm efficiently computes the likelihood $P(O|\lambda)$ of an observation sequence $O$ given an HMM $\lambda$, using dynamic programming to avoid enumerating all $N^T$ hidden state sequences.

## Motivation
The naïve approach sums over all $N^T$ possible hidden state sequences — exponential in $T$. The forward algorithm stores intermediate probabilities at each time step and reuses them, reducing complexity to $O(N^2T)$.

## How it works

### Forward Variable
$$\alpha_t(i) = P(o_1, o_2, \ldots, o_t,\; s_t = i\;|\;\lambda)$$
"Probability of observing the first $t$ outputs AND being in state $i$ at time $t$."

### Algorithm

**Initialisation** ($t=1$):
$$\alpha_1(j) = \pi_j\,b_j(o_1)$$
(initial state probability × emission probability for first observation)

**Recursion** ($t = 2, \ldots, T$):
$$\alpha_t(j) = \left[\sum_{i=1}^N \alpha_{t-1}(i)\,a_{ij}\right] b_j(o_t)$$
(sum over all previous states, weighted by transition × current emission)

**Termination**:
$$P(O|\lambda) = \sum_{i=1}^N \alpha_T(i)$$
(sum forward variables at the last time step)

### Complexity
- $O(N^2T)$ vs naïve $O(N^T)$.
- For $N=5$, $T=100$: forward is $\sim 2500$ operations vs $10^{70}$.

## Key derivation

Full worked numerical example: [[supp-hmm-forward-viterbi]].

Summary of key steps for Weather example ($N=2$, $T=3$):
- $\alpha_1(R) = 0.06$, $\alpha_1(S) = 0.24$.
- $\alpha_2(R) = 0.0552$, $\alpha_2(S) = 0.0486$.
- $\alpha_3(R) = 0.02904$, $\alpha_3(S) = 0.004572$.
- $P(O|\lambda) = 0.02904 + 0.004572 = \mathbf{0.0336}$.

⚠️ *Must be able to reproduce this type of calculation in the exam.*

## Parameters & intuition
- $\alpha_t(i)$ is the "score" of all partial paths ending in state $i$ at time $t$.
- The recursion propagates these scores forward: each step multiplies by transition and emission probabilities.
- Summing all $\alpha_T(i)$ marginalises over hidden states → total likelihood.
- Compare with [[viterbi-algorithm]]: Viterbi replaces $\sum$ with $\max$ to find the single best path.

## Worked example sketch
*Step by step for $O = (\text{Walk}, \text{Shop}, \text{Clean})$, using parameters from the weather HMM.*
*See [[supp-hmm-forward-viterbi]] for all numerical values.*

## Connections
- Compare with [[viterbi-algorithm]]: same structure (init, recursion, termination) but $\max$ instead of $\sum$.
- Used in Baum–Welch (E-step computes $\alpha_t(i)$ as part of the Forward–Backward algorithm).
- [[hidden-markov-model]]: the model this algorithm operates on.

## Exam notes
- 🔒 **Guaranteed in May 2026 exam** (confirmed by lecturer, 2026-05-09). See [[likely-questions]].
- Examinable: can be asked to perform the full calculation. ⚠️
- Must memorise all three parts: initialisation, recursion, termination.
- **Key formula** (recursion):
$$\alpha_t(j) = \left[\sum_i \alpha_{t-1}(i)a_{ij}\right] b_j(o_t)$$
- No formulas given — must write from memory. ⚠️
- **Common pitfall**: don't confuse with Viterbi ($\sum$ vs $\max$).
- Formula status: algorithm must be known from memory ⚠️
