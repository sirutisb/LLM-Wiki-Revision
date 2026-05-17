# Week 7 Revision Plan - Hidden Markov Models

**Scope:** [[hidden-markov-model]], [[forward-algorithm]], [[viterbi-algorithm]], [[forward-vs-viterbi]]
**Source:** [[lecture-w8]], [[supp-hmm-forward-viterbi]], [[examinable-topics]], [[week7_questions]]
**Formula status:** No formula sheet for Week 7. Only Forward and Viterbi are examinable, but their definitions, recursions, termination steps, and Viterbi backtracking must be memorised.

Week 7 is high priority. The HMM source page is labelled [[lecture-w8]], but the exam overview labels HMMs as Week 7. Treat this topic as Week 7 for revision. The likely exam task is a numerical trellis calculation: either compute $P(O|\lambda)$ with Forward or decode the most likely state sequence with Viterbi.

---

## What To Know Cold

### HMM setup
- [ ] An HMM is $\lambda = (A, B, \pi)$.
- [ ] Hidden states: $s_t \in \{1,\ldots,N\}$.
- [ ] Observations: $o_t \in \{1,\ldots,M\}$.
- [ ] Transition matrix: $A \in \mathbb{R}^{N \times N}$, where $a_{ij} = P(s_t = j|s_{t-1}=i)$. Rows are "from"; columns are "to".
- [ ] Emission matrix: $B \in \mathbb{R}^{N \times M}$, where $b_j(o) = P(o_t=o|s_t=j)$.
- [ ] Initial distribution: $\pi \in \mathbb{R}^N$, where $\pi_j = P(s_1=j)$.
- [ ] Markov property:
$$
P(s_t|s_1,\ldots,s_{t-1}) = P(s_t|s_{t-1}).
$$
- [ ] Observation independence:
$$
P(o_t|s_1,\ldots,s_T,o_1,\ldots,o_{t-1}) = P(o_t|s_t).
$$
- [ ] Joint distribution:
$$
p(s_{1:T}, o_{1:T})
=
\pi_{s_1}
\prod_{t=2}^{T} a_{s_{t-1}s_t}
\prod_{t=1}^{T} b_{s_t}(o_t).
$$

### Three HMM problems
- [ ] Evaluation / likelihood: compute $P(O|\lambda)$ using the [[forward-algorithm]].
- [ ] Decoding: find the most likely hidden state sequence using the [[viterbi-algorithm]].
- [ ] Learning: estimate $\lambda$ using Baum-Welch / EM. This is not examinable, but you should be able to name it.
- [ ] Naive enumeration has $N^T$ state sequences; dynamic programming reduces Forward and Viterbi to $O(N^2T)$.

### Forward algorithm
- [ ] Forward variable:
$$
\alpha_t(j) = P(o_1,\ldots,o_t, s_t=j|\lambda).
$$
- [ ] Initialisation:
$$
\alpha_1(j) = \pi_j b_j(o_1).
$$
- [ ] Recursion:
$$
\alpha_t(j)
=
\left[\sum_{i=1}^{N} \alpha_{t-1}(i)a_{ij}\right] b_j(o_t),
\qquad t=2,\ldots,T.
$$
- [ ] Termination:
$$
P(O|\lambda) = \sum_{i=1}^{N} \alpha_T(i).
$$
- [ ] Interpretation: Forward sums over all hidden paths, so it computes total likelihood.

### Viterbi algorithm
- [ ] Viterbi variable:
$$
v_t(j)
=
\max_{s_1,\ldots,s_{t-1}}
P(s_1,\ldots,s_{t-1},s_t=j,o_1,\ldots,o_t|\lambda).
$$
- [ ] Initialisation:
$$
v_1(j) = \pi_j b_j(o_1).
$$
- [ ] Recursion:
$$
v_t(j)
=
\left[\max_{i=1}^{N} v_{t-1}(i)a_{ij}\right] b_j(o_t),
\qquad t=2,\ldots,T.
$$
- [ ] Backpointer:
$$
\psi_t(j) = \arg\max_i v_{t-1}(i)a_{ij}.
$$
- [ ] Termination:
$$
s_T^* = \arg\max_j v_T(j).
$$
- [ ] Backtracking:
$$
s_{t-1}^* = \psi_t(s_t^*),
\qquad t=T,T-1,\ldots,2.
$$
- [ ] Interpretation: Viterbi keeps only the best incoming path, so it outputs a state sequence, not just a score.

### Forward vs Viterbi
- [ ] Same initialisation: $\pi_j b_j(o_1)$.
- [ ] Same trellis shape and same $O(N^2T)$ complexity.
- [ ] Forward uses $\sum$ and outputs $P(O|\lambda)$.
- [ ] Viterbi uses $\max$, stores $\psi_t(j)$, and outputs $s_{1:T}^*$.
- [ ] At each trellis cell, $v_t(j) \le \alpha_t(j)$ because the best single path cannot exceed the sum of all paths ending in the same state.

---

## Revision Schedule

### Pass 1 - 35 minutes: memory setup
- [ ] Write $\lambda = (A,B,\pi)$ and define every component, including matrix dimensions.
- [ ] Write the two HMM independence assumptions from memory.
- [ ] Write the joint distribution $p(s_{1:T}, o_{1:T})$ from memory.
- [ ] Write the three HMM problems and their algorithms.
- [ ] Explain why naive enumeration costs $O(N^T)$ and Forward / Viterbi cost $O(N^2T)$.
- [ ] Draw a blank trellis with $T$ columns and $N$ rows.

### Pass 2 - 45 minutes: Forward mechanics
- [ ] Write the Forward variable definition from memory.
- [ ] Write initialisation, recursion, and termination without notes.
- [ ] Do [[week7_questions]] Q4 in full.
- [ ] Redo the Forward calculation from [[supp-hmm-forward-viterbi]] without looking until the end.
- [ ] For each cell, say aloud: "sum previous scores times transitions, then multiply by the current emission."
- [ ] Check that the final answer is a scalar likelihood, not a state sequence.

### Pass 3 - 60 minutes: Viterbi mechanics
- [ ] Write the Viterbi variable definition from memory.
- [ ] Write initialisation, recursion, backpointer, termination, and backtracking without notes.
- [ ] Do [[week7_questions]] Q5 in full.
- [ ] Redo the Viterbi calculation from [[supp-hmm-forward-viterbi]] without looking until the end.
- [ ] For every cell, list all candidate incoming values before taking the maximum.
- [ ] Store $\psi_t(j)$ immediately after each maximum; do not leave backpointers to the end.
- [ ] Backtrack from $s_T^*$ and report the full sequence in chronological order.

### Pass 4 - 30 minutes: comparison and exam wording
- [ ] Do [[week7_questions]] Q1, Q2, and Q3 verbally.
- [ ] Explain Forward vs Viterbi using the phrase "sum over all paths vs best single path."
- [ ] Explain why their first step is identical.
- [ ] Explain why Viterbi needs backpointers but Forward does not.
- [ ] State which parts are examinable: Forward and Viterbi only.
- [ ] State which part is not examinable: Baum-Welch, except as the named learning algorithm.

### Final 15-minute check
- [ ] From a blank page, reproduce all Forward formulas.
- [ ] From a blank page, reproduce all Viterbi formulas, including backtracking.
- [ ] Complete one $N=2$, $T=3$ Forward table without notes.
- [ ] Complete one $N=2$, $T=3$ Viterbi table without notes.
- [ ] Check every transition uses row = from state, column = to state.
- [ ] Check every recursion multiplies by the current emission $b_j(o_t)$.

---

## Worked Example 1 - Forward Algorithm

### Question

Use the Weather HMM from [[supp-hmm-forward-viterbi]].

Hidden states are $R$ = Rainy and $S$ = Sunny. The observation sequence is:
$$
O = (\text{Walk}, \text{Shop}, \text{Clean}).
$$

Initial probabilities:
$$
\pi_R=0.6,\qquad \pi_S=0.4.
$$

Transition probabilities:

| From / to | $R$ | $S$ |
|-----------|-----|-----|
| $R$ | 0.7 | 0.3 |
| $S$ | 0.4 | 0.6 |

Emission probabilities:

| State | Walk | Shop | Clean |
|-------|------|------|-------|
| $R$ | 0.1 | 0.4 | 0.5 |
| $S$ | 0.6 | 0.3 | 0.1 |

Compute $P(O|\lambda)$ using the Forward algorithm.

### Solution

Initialisation, for $o_1=\text{Walk}$:
$$
\alpha_1(R) = \pi_R b_R(\text{Walk}) = 0.6 \times 0.1 = 0.06.
$$
$$
\alpha_1(S) = \pi_S b_S(\text{Walk}) = 0.4 \times 0.6 = 0.24.
$$

Recursion, for $o_2=\text{Shop}$:
$$
\alpha_2(R)
=
[\alpha_1(R)a_{RR} + \alpha_1(S)a_{SR}]b_R(\text{Shop})
$$
$$
=
[(0.06)(0.7) + (0.24)(0.4)](0.4)
=
[0.042 + 0.096](0.4)
=
0.0552.
$$

$$
\alpha_2(S)
=
[\alpha_1(R)a_{RS} + \alpha_1(S)a_{SS}]b_S(\text{Shop})
$$
$$
=
[(0.06)(0.3) + (0.24)(0.6)](0.3)
=
[0.018 + 0.144](0.3)
=
0.0486.
$$

Recursion, for $o_3=\text{Clean}$:
$$
\alpha_3(R)
=
[(0.0552)(0.7) + (0.0486)(0.4)](0.5)
$$
$$
=
[0.03864 + 0.01944](0.5)
=
0.02904.
$$

$$
\alpha_3(S)
=
[(0.0552)(0.3) + (0.0486)(0.6)](0.1)
$$
$$
=
[0.01656 + 0.02916](0.1)
=
0.004572.
$$

Termination:
$$
P(O|\lambda)
=
\alpha_3(R)+\alpha_3(S)
=
0.02904 + 0.004572
=
0.033612.
$$

Summary:

| $t$ | Observation | $\alpha_t(R)$ | $\alpha_t(S)$ |
|-----|-------------|---------------|---------------|
| 1 | Walk | 0.0600 | 0.2400 |
| 2 | Shop | 0.0552 | 0.0486 |
| 3 | Clean | 0.02904 | 0.004572 |

Final answer:
$$
P(O|\lambda) = 0.033612 \approx 0.0336.
$$

---

## Worked Example 2 - Viterbi Algorithm

### Question

Use the same Weather HMM and observation sequence:
$$
O = (\text{Walk}, \text{Shop}, \text{Clean}).
$$

Find the most likely hidden state sequence using the Viterbi algorithm.

### Solution

Initialisation, for $o_1=\text{Walk}$:
$$
v_1(R) = \pi_R b_R(\text{Walk}) = 0.6 \times 0.1 = 0.06.
$$
$$
v_1(S) = \pi_S b_S(\text{Walk}) = 0.4 \times 0.6 = 0.24.
$$

Recursion, for $o_2=\text{Shop}$.

For current state $R$:
$$
v_1(R)a_{RR} = 0.06 \times 0.7 = 0.042,
\qquad
v_1(S)a_{SR} = 0.24 \times 0.4 = 0.096.
$$
The maximum is $0.096$, from previous state $S$, so:
$$
v_2(R) = 0.096 \times b_R(\text{Shop}) = 0.096 \times 0.4 = 0.0384,
\qquad
\psi_2(R)=S.
$$

For current state $S$:
$$
v_1(R)a_{RS} = 0.06 \times 0.3 = 0.018,
\qquad
v_1(S)a_{SS} = 0.24 \times 0.6 = 0.144.
$$
The maximum is $0.144$, from previous state $S$, so:
$$
v_2(S) = 0.144 \times b_S(\text{Shop}) = 0.144 \times 0.3 = 0.0432,
\qquad
\psi_2(S)=S.
$$

Recursion, for $o_3=\text{Clean}$.

For current state $R$:
$$
v_2(R)a_{RR} = 0.0384 \times 0.7 = 0.02688,
\qquad
v_2(S)a_{SR} = 0.0432 \times 0.4 = 0.01728.
$$
The maximum is $0.02688$, from previous state $R$, so:
$$
v_3(R) = 0.02688 \times b_R(\text{Clean}) = 0.02688 \times 0.5 = 0.01344,
\qquad
\psi_3(R)=R.
$$

For current state $S$:
$$
v_2(R)a_{RS} = 0.0384 \times 0.3 = 0.01152,
\qquad
v_2(S)a_{SS} = 0.0432 \times 0.6 = 0.02592.
$$
The maximum is $0.02592$, from previous state $S$, so:
$$
v_3(S) = 0.02592 \times b_S(\text{Clean}) = 0.02592 \times 0.1 = 0.002592,
\qquad
\psi_3(S)=S.
$$

Termination:
$$
s_3^*
=
\arg\max_j v_3(j)
=
\arg\max(0.01344,0.002592)
=
R.
$$

Backtracking:
$$
s_2^* = \psi_3(R) = R.
$$
$$
s_1^* = \psi_2(R) = S.
$$

Summary:

| $t$ | Observation | $v_t(R)$ | $\psi_t(R)$ | $v_t(S)$ | $\psi_t(S)$ |
|-----|-------------|----------|-------------|----------|-------------|
| 1 | Walk | 0.0600 | - | 0.2400 | - |
| 2 | Shop | 0.0384 | S | 0.0432 | S |
| 3 | Clean | 0.01344 | R | 0.002592 | S |

Final answer:
$$
s_{1:3}^* = (S,R,R).
$$

In words, the most likely hidden state sequence is Sunny, then Rainy, then Rainy.

---

## Worked Example 3 - Conceptual Mini Answer

### Question

Explain the difference between the Forward and Viterbi algorithms.

### Model answer

Both algorithms use dynamic programming on the same HMM trellis. They have the same initialisation, $\pi_j b_j(o_1)$, and both combine scores from time $t-1$ to compute scores at time $t$.

The Forward algorithm uses a sum:
$$
\alpha_t(j)
=
\left[\sum_i \alpha_{t-1}(i)a_{ij}\right]b_j(o_t).
$$
This marginalises over all hidden paths and outputs the total likelihood $P(O|\lambda)$.

The Viterbi algorithm uses a maximum:
$$
v_t(j)
=
\left[\max_i v_{t-1}(i)a_{ij}\right]b_j(o_t).
$$
This keeps only the best incoming path, stores backpointers, and outputs the most likely hidden state sequence.

---

## Extra Practice To Work On

### Drill A - Forward trace

Use the following two-state HMM.

States: $A,B$. Observations: $x,y$.

Initial distribution:
$$
\pi_A=0.7,\qquad \pi_B=0.3.
$$

Transitions:

| From / to | $A$ | $B$ |
|-----------|-----|-----|
| $A$ | 0.6 | 0.4 |
| $B$ | 0.2 | 0.8 |

Emissions:

| State | $x$ | $y$ |
|-------|-----|-----|
| $A$ | 0.5 | 0.5 |
| $B$ | 0.1 | 0.9 |

Observation sequence:
$$
O=(x,y,y).
$$

Tasks:
- [ ] Compute $\alpha_1(A)$ and $\alpha_1(B)$.
- [ ] Compute $\alpha_2(A)$ and $\alpha_2(B)$.
- [ ] Compute $\alpha_3(A)$ and $\alpha_3(B)$.
- [ ] Compute $P(O|\lambda)$.
- [ ] Check whether every recursion used a sum and multiplied by the current emission.

### Drill B - Viterbi trace

Use the same HMM and $O=(x,y,y)$.

Tasks:
- [ ] Compute $v_1(A)$ and $v_1(B)$.
- [ ] Compute $v_2(A)$, $v_2(B)$, $\psi_2(A)$, and $\psi_2(B)$.
- [ ] Compute $v_3(A)$, $v_3(B)$, $\psi_3(A)$, and $\psi_3(B)$.
- [ ] Determine $s_3^*$.
- [ ] Backtrack to recover $s_{1:3}^*$.
- [ ] Report the final answer as a state sequence, not only a probability.

### Drill C - Bookwork prompts

Answer each in two or three sentences:
- [ ] What does $\alpha_t(j)$ mean?
- [ ] What does $v_t(j)$ mean?
- [ ] Why is the initialisation identical for Forward and Viterbi?
- [ ] Why does Forward use a sum?
- [ ] Why does Viterbi use a maximum?
- [ ] Why does Viterbi need backpointers?
- [ ] What is Baum-Welch used for, and why is it not the focus here?
- [ ] Why is $O(N^2T)$ a major improvement over $O(N^T)$?

---

## Common Mistakes

- [ ] Using $\max$ in Forward. Forward must sum over all previous states.
- [ ] Using $\sum$ in Viterbi. Viterbi must keep the maximum incoming path.
- [ ] Forgetting to multiply by $b_j(o_t)$ at every time step, including $t=1$.
- [ ] Multiplying by the wrong emission, such as $b_i(o_t)$ instead of $b_j(o_t)$.
- [ ] Reversing transition indices. In this wiki, $a_{ij}$ means from state $i$ to state $j$.
- [ ] Treating rows as "to" states and columns as "from" states when reading $A$.
- [ ] Forgetting the Forward termination sum $\sum_i \alpha_T(i)$.
- [ ] Reporting the Viterbi terminal score but not backtracking to give the sequence.
- [ ] Storing Viterbi scores but not storing $\psi_t(j)$.
- [ ] Backtracking in the wrong direction. Start from $s_T^*$ and move backward.
- [ ] Writing the final Viterbi path backward. The final answer should be $s_1,\ldots,s_T$.
- [ ] Saying Baum-Welch is examinable. It is not, beyond naming it as the learning algorithm.

---

## Exam-Ready Checklist

You are Week 7-ready when you can:

- [ ] Define an HMM as $\lambda=(A,B,\pi)$ and explain each component.
- [ ] State the Markov and observation-independence assumptions.
- [ ] Write the joint distribution of states and observations.
- [ ] Map Evaluation to Forward, Decoding to Viterbi, and Learning to Baum-Welch.
- [ ] Reproduce the Forward variable, initialisation, recursion, and termination from memory.
- [ ] Reproduce the Viterbi variable, initialisation, recursion, backpointer, termination, and backtracking from memory.
- [ ] Complete a Forward table for a two-state, three-observation HMM.
- [ ] Complete a Viterbi table for a two-state, three-observation HMM, including backpointers.
- [ ] Explain the sum vs max distinction without looking at notes.
- [ ] Check arithmetic by confirming $v_t(j) \le \alpha_t(j)$ when both algorithms are run on the same HMM.
- [ ] State clearly that no formula sheet is provided for Week 7.
- [ ] Similar past-paper calibration: translate between $A$, $B$, $\pi$ and an HMM diagram, including row-sum checks for transition and emission matrices.
