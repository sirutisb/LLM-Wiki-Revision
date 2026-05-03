# Derivation: HMM Viterbi Algorithm

**Used in:** [[viterbi-algorithm]], [[hidden-markov-model]]
**Source:** [[supp-hmm-forward-viterbi]], [[lecture-w8]]
**Exam status:** ⚠️ Must know — numerical Viterbi is examinable (no formula sheet)

## Setup
Same HMM $\lambda = (\mathbf{A}, \mathbf{B}, \boldsymbol{\pi})$ as Forward algorithm.

**Problem**: find the most probable state sequence $Q^* = \arg\max_Q P(Q|O, \lambda)$.

## Key Difference from Forward Algorithm
- Forward: sums over all state paths ($\sum$) → marginal probability $P(O|\lambda)$.
- Viterbi: takes the max over all state paths ($\max$) → most probable path $Q^*$.

## Viterbi Variable
$$v_t(j) = \max_{q_1,\ldots,q_{t-1}} P(q_1,\ldots,q_{t-1},q_t=j,o_1,\ldots,o_t|\lambda)$$

The probability of the most probable path ending in state $j$ at time $t$.

Also track: $\psi_t(j)$ = the state at time $t-1$ on the most probable path ending in $j$ at $t$ (backpointer).

## Recursion

### Initialisation ($t=1$)
$$v_1(j) = \pi_j \cdot B_j(o_1), \qquad \psi_1(j) = 0$$

### Recursion ($t = 2, \ldots, T$)
$$v_t(j) = \max_i\left[v_{t-1}(i)\cdot A_{ij}\right]\cdot B_j(o_t)$$
$$\psi_t(j) = \arg\max_i\left[v_{t-1}(i)\cdot A_{ij}\right]$$

Note: **max** replaces **sum** vs the Forward recursion. Emission $B_j(o_t)$ is applied after the max (over transitions).

### Termination
$$P^* = \max_j v_T(j), \qquad q_T^* = \arg\max_j v_T(j)$$

### Backtracking
For $t = T-1, T-2, \ldots, 1$:
$$q_t^* = \psi_{t+1}(q_{t+1}^*)$$

The backpointers trace the most probable path backwards.

## Worked Example (Weather HMM)

Same parameters as Forward algorithm derivation page.
Observation: $O = (H, V, V)$

**$t=1$** ($o_1 = H$):
$$v_1(S) = 0.7\times0.6 = 0.42, \quad v_1(R) = 0.3\times0.1 = 0.03$$

**$t=2$** ($o_2 = V$, emission $B_S(V)=0.4$, $B_R(V)=0.9$):
For $j=S$: $\max(0.42\times0.8,\; 0.03\times0.4) = \max(0.336,\; 0.012) = 0.336$
$$v_2(S) = 0.336\times0.4 = 0.1344, \quad \psi_2(S) = S$$

For $j=R$: $\max(0.42\times0.2,\; 0.03\times0.6) = \max(0.084,\; 0.018) = 0.084$
$$v_2(R) = 0.084\times0.9 = 0.0756, \quad \psi_2(R) = S$$

**$t=3$** ($o_3 = V$):
For $j=S$: $\max(0.1344\times0.8,\; 0.0756\times0.4) = \max(0.1075,\; 0.0302) = 0.1075$
$$v_3(S) = 0.1075\times0.4 = 0.0430, \quad \psi_3(S) = S$$

For $j=R$: $\max(0.1344\times0.2,\; 0.0756\times0.6) = \max(0.0269,\; 0.0454) = 0.0454$
$$v_3(R) = 0.0454\times0.9 = 0.0408, \quad \psi_3(R) = R$$

**Termination**: $q_3^* = \arg\max(0.0430, 0.0408) = S$

**Backtrack**: $q_2^* = \psi_3(S) = S$; $q_1^* = \psi_2(S) = S$

**Most probable path**: $S \to S \to S$

## Complexity
$O(N^2 T)$ — same as Forward algorithm.

## Forward vs Viterbi Comparison

| Aspect | Forward | Viterbi |
|--------|---------|---------|
| Operation | Sum ($\sum$) | Max ($\max$) |
| Output | $P(O\|\lambda)$ | Most probable path $Q^*$ |
| Backpointers | Not needed | Required for backtracking |
| Purpose | Evaluation | Decoding |
