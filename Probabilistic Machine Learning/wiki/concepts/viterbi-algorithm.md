# Viterbi Algorithm

**Type:** algorithm
**Week:** 7 (exam numbering)
**Related:** [[hidden-markov-model]], [[forward-algorithm]]
**Source:** [[lecture-w8]], [[supp-hmm-forward-viterbi]]

## Definition
The Viterbi Algorithm finds the single most likely hidden state sequence $S^* = \arg\max_S P(S|O,\lambda)$ given an observation sequence $O$ and HMM $\lambda$, using dynamic programming.

## Motivation
Naïve decoding enumerates all $N^T$ state sequences — exponential. Viterbi uses dynamic programming with a "max" operation to track the best path incrementally, achieving $O(N^2T)$ complexity.

## How it works

### Viterbi Variable
$$v_t(j) = \max_{s_1,\ldots,s_{t-1}} P(s_1,\ldots,s_{t-1},\; s_t=j,\; o_1,\ldots,o_t\;|\;\lambda)$$
"Probability of the best (most likely) path ending in state $j$ at time $t$."

### Algorithm

**Initialisation** ($t=1$):
$$v_1(j) = \pi_j\,b_j(o_1)$$

**Recursion** ($t = 2, \ldots, T$):
$$v_t(j) = \left[\max_{i=1}^N v_{t-1}(i)\,a_{ij}\right] b_j(o_t)$$
Store **backpointer**: $\psi_t(j) = \arg\max_i v_{t-1}(i)\,a_{ij}$ (which previous state gave the best path).

**Termination**:
$$s_T^* = \arg\max_j v_T(j)$$

**Backtracking**: recover full optimal sequence by following backpointers:
$$s_{t-1}^* = \psi_t(s_t^*), \quad t = T, T-1, \ldots, 2$$

## Key derivation

Full worked numerical example: [[supp-hmm-forward-viterbi]].

Summary for Weather example ($N=2$, $T=3$):
- $v_1(R) = 0.06$, $v_1(S) = 0.24$.
- $v_2(R) = 0.0384$ ($\psi_2(R) = S$), $v_2(S) = 0.0432$ ($\psi_2(S) = S$).
- $v_3(R) = 0.01344$ ($\psi_3(R) = R$), $v_3(S) = 0.002592$ ($\psi_3(S) = S$).
- $s_3^* = R$ (arg max of $v_3$). Backtrack: $s_2^* = \psi_3(R) = R$, $s_1^* = \psi_2(R) = S$.
- **Most likely sequence**: Sunny → Rainy → Rainy.

⚠️ *Must be able to reproduce this type of calculation.*

## Parameters & intuition
- $v_t(j)$ is the "score" of the best partial path ending in state $j$ at time $t$.
- Recursion: at each step, evaluate all incoming transitions and keep only the best.
- Backpointers store which state to "come from" at each step — needed for recovery.
- Max path probability at termination: $\max_j v_T(j)$.

### Forward vs Viterbi (Critical Comparison)
| | Forward Algorithm | Viterbi Algorithm |
|--|--|--|
| Goal | Total likelihood $P(O|\lambda)$ | Best state sequence $S^*$ |
| Operator | $\sum_i$ (sum) | $\max_i$ (maximum) |
| Stores | $\alpha_t(j)$ only | $v_t(j)$ + backpointers $\psi_t(j)$ |
| Initialisation | $\pi_j b_j(o_1)$ | $\pi_j b_j(o_1)$ (identical) |
| Recursion factor | $\sum_i \alpha_{t-1}(i) a_{ij}$ | $\max_i v_{t-1}(i) a_{ij}$ |

## Worked example sketch
*Exam-type question*: Given matrices $A, B, \pi$ and observation sequence $O$, compute Viterbi scores and backpointers step by step, then report the most likely hidden state sequence.

## Connections
- Compare with [[forward-algorithm]]: same DP structure; $\sum$ (Forward) vs $\max$ (Viterbi).
- [[hidden-markov-model]]: the model this algorithm operates on.

## Exam notes
- Examinable: full numerical calculation. ⚠️
- Must memorise: init, recursion with $\max$, backpointer storage, termination, backtracking.
- **Key formula** (recursion):
$$v_t(j) = \left[\max_i v_{t-1}(i)a_{ij}\right] b_j(o_t), \qquad \psi_t(j) = \arg\max_i v_{t-1}(i)a_{ij}$$
- Backtracking is easy to forget — practice it!
- No formulas given. ⚠️
- **Common pitfall**: forgetting to store and use backpointers; confusing $\sum$ (Forward) with $\max$ (Viterbi).
- Formula status: algorithm must be known from memory ⚠️
