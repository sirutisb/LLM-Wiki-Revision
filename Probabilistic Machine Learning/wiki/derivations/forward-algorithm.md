# Derivation: HMM Forward Algorithm

**Used in:** [[forward-algorithm]], [[hidden-markov-model]]
**Source:** [[supp-hmm-forward-viterbi]], [[lecture-w8]]
**Exam status:** ⚠️ Formulas NOT given | Derivation NOT examinable (Numerical application only)

## Setup
HMM: $\lambda = (\mathbf{A}, \mathbf{B}, \boldsymbol{\pi})$
- $\mathbf{A}$: transition matrix, $A_{ij} = P(q_{t+1}=j|q_t=i)$.
- $\mathbf{B}$: emission matrix, $B_{j}(o_t) = P(o_t|q_t=j)$.
- $\boldsymbol{\pi}$: initial state distribution.

Observation sequence: $O = (o_1, o_2, \ldots, o_T)$.

**Problem**: compute $P(O|\lambda)$ — the probability of the observation sequence.

## Naive Approach (Exponential Cost)
Sum over all state sequences $Q = (q_1,\ldots,q_T)$:
$$P(O|\lambda) = \sum_Q P(O,Q|\lambda) = \sum_{q_1,\ldots,q_T} \pi_{q_1}\prod_{t=1}^T B_{q_t}(o_t)\prod_{t=1}^{T-1} A_{q_t q_{t+1}}$$
Cost: $O(N^T \cdot T)$ — exponential in $T$. Intractable.

## Forward Variable
Define:
$$\alpha_t(j) = P(o_1, o_2, \ldots, o_t, q_t = j \mid \lambda)$$
The probability of seeing the first $t$ observations AND being in state $j$ at time $t$.

## Recursion (Dynamic Programming)

### Initialisation ($t=1$)
$$\alpha_1(j) = \pi_j \cdot B_j(o_1) \quad \text{for } j = 1,\ldots,N$$

### Recursion ($t = 2, \ldots, T$)
$$\alpha_t(j) = \left[\sum_{i=1}^N \alpha_{t-1}(i)\,A_{ij}\right]\cdot B_j(o_t)$$

Interpretation: sum over all previous states $i$ the probability of being in $i$ at $t-1$ and transitioning to $j$, then multiply by the emission probability of $o_t$ from state $j$.

### Termination
$$P(O|\lambda) = \sum_{j=1}^N \alpha_T(j)$$

## Complexity
Each $\alpha_t(j)$ requires summing over $N$ states: $O(N^2)$ operations per time step.
Total: $O(N^2 T)$ — polynomial in $T$ (vs exponential for naive).

## Worked Example (Weather HMM)

States: Sunny ($S$), Rainy ($R$). Observations: Happy ($H$), Sad ($V$).

Parameters:
$$\mathbf{A} = \begin{pmatrix}0.8 & 0.2 \\ 0.4 & 0.6\end{pmatrix}, \quad \mathbf{B} = \begin{pmatrix}0.6 & 0.4 \\ 0.1 & 0.9\end{pmatrix}, \quad \boldsymbol{\pi} = (0.7, 0.3)$$

Observation: $O = (H, V, V)$

**$t=1$** ($o_1 = H$):
$$\alpha_1(S) = 0.7 \times 0.6 = 0.42, \quad \alpha_1(R) = 0.3 \times 0.1 = 0.03$$

**$t=2$** ($o_2 = V$):
$$\alpha_2(S) = (0.42\times0.8 + 0.03\times0.4)\times0.4 = (0.336+0.012)\times0.4 = 0.1392$$
$$\alpha_2(R) = (0.42\times0.2 + 0.03\times0.6)\times0.9 = (0.084+0.018)\times0.9 = 0.0918$$

**$t=3$** ($o_3 = V$):
$$\alpha_3(S) = (0.1392\times0.8 + 0.0918\times0.4)\times0.4 = (0.1114+0.0367)\times0.4 = 0.0592$$
$$\alpha_3(R) = (0.1392\times0.2 + 0.0918\times0.6)\times0.9 = (0.0278+0.0551)\times0.9 = 0.0746$$

**Result**:
$$P(O|\lambda) = \alpha_3(S) + \alpha_3(R) = 0.0592 + 0.0746 \approx 0.1338$$

(Note: the supplementary note example gets 0.0336 with different parameters — the worked example here is illustrative.)
