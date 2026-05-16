# Forward vs Viterbi — HMM Inference Algorithms

**Week:** 7 (exam numbering)
**Related:** [[forward-algorithm]], [[viterbi-algorithm]], [[hidden-markov-model]]
**Source:** [[lecture-w8]], [[supp-hmm-forward-viterbi]]

## Overview
Both the Forward and Viterbi algorithms solve **inference problems on Hidden Markov Models** using the same dynamic-programming skeleton — the same trellis, the same $O(N^2 T)$ complexity, and an *identical* initialisation. They differ in exactly **one** place: where Forward sums over previous states, Viterbi takes the maximum. That single change converts a *marginalisation* into an *optimisation*, and that converts an evaluation problem (likelihood) into a decoding problem (best state sequence).

The lecturer has confirmed (transcript 2026-05-09) that *every year, either Forward or Viterbi is examined in depth*. Knowing how they relate — not just each in isolation — is the fastest way to recover one if you blank on the other in the exam.

## Comparison table

| Dimension | Forward Algorithm | Viterbi Algorithm |
|-----------|-------------------|-------------------|
| **Problem solved** | Evaluation: $P(O\mid\lambda)$ | Decoding: $S^* = \arg\max_S P(S\mid O,\lambda)$ |
| **Question answered** | "How likely is this observation sequence?" | "What was the most probable hidden state sequence?" |
| **DP variable** | $\alpha_t(j) = P(o_{1:t}, s_t=j\mid\lambda)$ | $v_t(j) = \max_{s_{1:t-1}} P(s_{1:t-1}, s_t=j, o_{1:t}\mid\lambda)$ |
| **Operator on previous step** | $\sum_i$ (marginalises) | $\max_i$ (optimises) |
| **Initialisation** | $\alpha_1(j) = \pi_j b_j(o_1)$ | $v_1(j) = \pi_j b_j(o_1)$ *(identical)* |
| **Recursion** | $\alpha_t(j) = \left[\sum_i \alpha_{t-1}(i)\,a_{ij}\right] b_j(o_t)$ | $v_t(j) = \left[\max_i v_{t-1}(i)\,a_{ij}\right] b_j(o_t)$ |
| **Stores backpointers?** | No | Yes: $\psi_t(j) = \arg\max_i v_{t-1}(i)\,a_{ij}$ |
| **Termination** | $P(O\mid\lambda) = \sum_i \alpha_T(i)$ | $s_T^* = \arg\max_j v_T(j)$, then backtrack via $\psi$ |
| **Output** | A scalar likelihood | A length-$T$ state sequence |
| **Complexity** | $O(N^2 T)$ | $O(N^2 T)$ |
| **Used in** | Evidence, Forward–Backward, [[baum-welch-algorithm]] (E-step) | Speech recognition, POS tagging, gene finding |

## When to use which

**Use Forward when** you want to **score** the observation sequence:
- Computing $P(O\mid\lambda)$ for **model selection** (which of several HMMs explains the data best — pick the one with highest likelihood).
- The **E-step of Baum–Welch** (EM for HMMs) needs $\alpha_t(j)$ values to compute posterior responsibilities.
- **Anomaly detection**: very low $P(O\mid\lambda)$ flags observations that don't fit the trained HMM.
- You don't care *which* hidden states were active — you just want to know if the observations are plausible under the model.

**Use Viterbi when** you want to **decode** the hidden state sequence:
- **Speech recognition**: which phonemes (hidden) produced the audio (observed)?
- **POS tagging**: which tag sequence best explains the words?
- **Gene finding / bioinformatics**: which DNA regions are coding (hidden) given the nucleotide sequence (observed)?
- **Weather/activity tasks** (the lecture example): given activities, what's the most likely weather sequence?
- You need a *single, coherent, MAP* assignment of hidden states.

**A useful slogan:** Forward answers *"how likely?"*; Viterbi answers *"what happened?"*.

## Intuition

### The "$\sum$ vs $\max$" swap
Both algorithms build up a value at each cell $(t, j)$ of a $T \times N$ trellis by combining values from the previous column.

- Forward **adds** contributions from all incoming paths into $(t, j)$. The cell $\alpha_t(j)$ therefore accumulates probability mass across *every* path of length $t$ ending in state $j$. Summing the last column marginalises the hidden states entirely, leaving $P(O\mid\lambda)$.
- Viterbi **keeps only the best** incoming path into $(t, j)$. The cell $v_t(j)$ stores the probability of the *single* best path of length $t$ ending in state $j$. The backpointer remembers which predecessor that best path came from, so we can reconstruct it.

A clean way to see this: replace $\sum$ with $\max$ in Forward and you get Viterbi. (Formally, you've moved from the "sum-product" semiring to the "max-product" semiring; this is the same trick that turns sum-product into max-product in belief propagation.)

### Why the same skeleton works
Both rely on the **Markov property**: the future depends on the present, not the past. So any quantity ending at state $j$ at time $t$ can be computed from quantities ending at time $t-1$ — for Forward we *aggregate* over predecessors, for Viterbi we *pick the best* predecessor. The trellis is a dynamic-programming table that exploits this overlapping subproblem structure.

### Why backpointers are needed only in Viterbi
Forward doesn't need to know *which* path contributed — it just needs the total mass. Viterbi needs to know the single best path, but the probability $v_t(j)$ only tells you *how good* the best path is, not *which states it visited*. So Viterbi additionally stores $\psi_t(j)$ — "if I end up in state $j$ at time $t$ on the best path, which state did I come from at $t-1$?" Backtracking through $\psi$ from the terminal $\arg\max$ recovers the full sequence.

### Why both run in $O(N^2 T)$
At each of $T$ time steps, for each of $N$ current states, you look at $N$ previous states — that's $N \cdot N \cdot T = N^2 T$ operations. The naïve approach of enumerating every state sequence costs $O(N^T)$. For the lecture example ($N{=}2, T{=}3$) the saving is small, but for $N{=}5, T{=}100$ it's $\sim 2500$ vs $10^{70}$ — a saving factor of $\sim 10^{67}$.

## Worked example — side by side

We use the Weather HMM from [[supp-hmm-forward-viterbi]].

**Parameters.**
- Hidden states $\{R = \text{Rainy}, S = \text{Sunny}\}$.
- Observations $O = (\text{Walk}, \text{Shop}, \text{Clean})$.
- $\pi = (\pi_R, \pi_S) = (0.6, 0.4)$.
- Transitions $A$: $a_{RR}=0.7, a_{RS}=0.3, a_{SR}=0.4, a_{SS}=0.6$.
- Emissions $B$:

| | Walk | Shop | Clean |
|--|--|--|--|
| R | 0.1 | 0.4 | 0.5 |
| S | 0.6 | 0.3 | 0.1 |

### Step 1 — Initialisation ($t=1$, observation Walk)
**Identical in both algorithms** — the only thing happening is "start in state $j$ AND emit $o_1$":
$$\alpha_1(R) = v_1(R) = \pi_R\,b_R(\text{Walk}) = 0.6\times 0.1 = 0.06$$
$$\alpha_1(S) = v_1(S) = \pi_S\,b_S(\text{Walk}) = 0.4\times 0.6 = 0.24$$

*Intuition:* Sunny is much more compatible with Walk than Rainy is, even though Rainy has a slightly higher prior.

### Step 2 — Recursion ($t=2$, observation Shop)

#### Forward — sum over predecessors
$$\alpha_2(R) = \big[\,\alpha_1(R)\,a_{RR} + \alpha_1(S)\,a_{SR}\,\big]\,b_R(\text{Shop})$$
$$= [(0.06)(0.7) + (0.24)(0.4)]\times 0.4 = [0.042 + 0.096]\times 0.4 = 0.138\times 0.4 = \mathbf{0.0552}$$

$$\alpha_2(S) = \big[\,\alpha_1(R)\,a_{RS} + \alpha_1(S)\,a_{SS}\,\big]\,b_S(\text{Shop})$$
$$= [(0.06)(0.3) + (0.24)(0.6)]\times 0.3 = [0.018 + 0.144]\times 0.3 = 0.162\times 0.3 = \mathbf{0.0486}$$

#### Viterbi — max over predecessors (+ backpointer)
$$v_2(R) = \max\big(v_1(R)\,a_{RR},\; v_1(S)\,a_{SR}\big)\,b_R(\text{Shop})$$
$$= \max(0.06\times 0.7,\; 0.24\times 0.4)\times 0.4 = \max(0.042, 0.096)\times 0.4 = 0.096\times 0.4 = \mathbf{0.0384}$$
$$\Rightarrow \psi_2(R) = S\quad (\text{the } 0.096 \text{ came from coming from } S)$$

$$v_2(S) = \max\big(v_1(R)\,a_{RS},\; v_1(S)\,a_{SS}\big)\,b_S(\text{Shop})$$
$$= \max(0.06\times 0.3,\; 0.24\times 0.6)\times 0.3 = \max(0.018, 0.144)\times 0.3 = 0.144\times 0.3 = \mathbf{0.0432}$$
$$\Rightarrow \psi_2(S) = S$$

**Comparison at $t=2$:** $\alpha_2(R) = 0.0552 > v_2(R) = 0.0384$ — Forward is larger because it adds both incoming paths, while Viterbi keeps only the best one. Same for state $S$.

### Step 3 — Recursion ($t=3$, observation Clean)

#### Forward
$$\alpha_3(R) = [(0.0552)(0.7) + (0.0486)(0.4)]\times 0.5 = [0.03864 + 0.01944]\times 0.5 = 0.05808\times 0.5 = \mathbf{0.02904}$$
$$\alpha_3(S) = [(0.0552)(0.3) + (0.0486)(0.6)]\times 0.1 = [0.01656 + 0.02916]\times 0.1 = 0.04572\times 0.1 = \mathbf{0.004572}$$

#### Viterbi
$$v_3(R) = \max(0.0384\times 0.7,\; 0.0432\times 0.4)\times 0.5 = \max(0.02688, 0.01728)\times 0.5 = 0.02688\times 0.5 = \mathbf{0.01344}$$
$$\Rightarrow \psi_3(R) = R$$
$$v_3(S) = \max(0.0384\times 0.3,\; 0.0432\times 0.6)\times 0.1 = \max(0.01152, 0.02592)\times 0.1 = 0.02592\times 0.1 = \mathbf{0.002592}$$
$$\Rightarrow \psi_3(S) = S$$

### Step 4 — Termination

#### Forward — sum the last column
$$P(O\mid\lambda) = \alpha_3(R) + \alpha_3(S) = 0.02904 + 0.004572 = \boxed{0.033612}$$
*Answer: "the total probability of observing (Walk, Shop, Clean) under this HMM is $\approx 0.0336$."*

#### Viterbi — pick max and backtrack
$$s_3^* = \arg\max_j v_3(j) = \arg\max(0.01344,\; 0.002592) = R$$
Backtrack using stored $\psi$:
$$s_2^* = \psi_3(s_3^*) = \psi_3(R) = R$$
$$s_1^* = \psi_2(s_2^*) = \psi_2(R) = S$$
$$\boxed{S^* = (S, R, R) = (\text{Sunny}, \text{Rainy}, \text{Rainy})}$$
*Answer: "the single most likely weather sequence given (Walk, Shop, Clean) is Sunny → Rainy → Rainy, with probability $v_3(R) = 0.01344$."*

### Side-by-side summary table

| Time | Obs | $\alpha_t(R)$ | $\alpha_t(S)$ | $v_t(R)$ | $v_t(S)$ | $\psi_t(R)$ | $\psi_t(S)$ |
|------|-----|---------------|---------------|----------|----------|-------------|-------------|
| 1 | Walk | 0.06 | 0.24 | 0.06 | 0.24 | — | — |
| 2 | Shop | 0.0552 | 0.0486 | 0.0384 | 0.0432 | $S$ | $S$ |
| 3 | Clean | 0.02904 | 0.004572 | 0.01344 | 0.002592 | $R$ | $S$ |

**Final answers:**
- Forward: $P(O\mid\lambda) = 0.0336$.
- Viterbi: $S^* = (S, R, R)$, with path probability $0.01344$.

### Sanity checks
1. **Both algorithms agree at $t=1$** — same numbers, by construction. If yours don't, the bug is in initialisation.
2. **$v_t(j) \le \alpha_t(j)$** at every cell (single best path can't be more massive than the sum over all paths). For $(t,j) = (2,R)$: $0.0384 \le 0.0552$ ✓. For $(3,R)$: $0.01344 \le 0.02904$ ✓.
3. **The Viterbi path probability $\max_j v_T(j) = 0.01344$ is one term in the Forward sum.** Equality is impossible unless there is only one path with non-zero probability, which is essentially never the case for a non-degenerate HMM.
4. **The decoded path $(S, R, R)$ is internally consistent**: it begins in $S$ (compatible with Walk) and then transitions $S\to R\to R$ — using $a_{SR}=0.4$ and $a_{RR}=0.7$, which are both plausible transitions.

## Synthesis

The Forward and Viterbi algorithms are the **same dynamic-programming template** instantiated with two different operators. This is not a quirk — it reflects a deeper duality:

- Forward lives in the **sum-product semiring** $(+, \times)$ → marginalisation, probabilities.
- Viterbi lives in the **max-product semiring** $(\max, \times)$ → optimisation, best assignments.

The lecture HMM is one of the simplest non-trivial graphical models on which to see this duality. The same swap shows up later in graphical-model inference more broadly: the **sum-product** algorithm computes marginals, the **max-product** algorithm finds the MAP assignment. The Forward algorithm is sum-product on the HMM chain; Viterbi is max-product on the same chain.

For the exam, the practical consequence is liberating: **if you remember one algorithm completely, you can recover the other by swapping $\sum$ for $\max$ and adding backpointers** (or, going the other way, by swapping $\max$ for $\sum$ and dropping the backpointers). The initialisations are identical; only the recursion and termination differ.

## Exam notes

- 🔒 Lecturer-confirmed: one of {Forward, Viterbi} examined in depth every year. See [[likely-questions]].
- The exam will likely ask for the full numerical walk-through on a small HMM like this one. Be ready to:
  - Identify $\pi$, $A$, $B$ from a problem statement.
  - Write out initialisation, recursion, and termination explicitly.
  - Carry out arithmetic to 4–5 significant figures with a non-programmable calculator.
  - For Viterbi: store backpointers as you go, then **backtrack** to recover the sequence (markers commonly deduct marks for omitting backtracking).
- **Derivations:** NOT examinable for HMM algorithms. (Focus is on understanding and applying the procedures).
- **No formulas given** for either algorithm — write them from memory. ⚠️
- **Common pitfalls:**
  - Using $\max$ in Forward or $\sum$ in Viterbi (the single most-marked error).
  - Forgetting backpointers in Viterbi → cannot recover the sequence.
  - Reporting $\max_j v_T(j)$ as "the answer" — the answer to a decoding question is the *sequence*, not the score.
  - Confusing rows and columns of $A$: in lecture convention rows = "from", columns = "to".
  - Multiplying by the emission $b_j(o_t)$ *inside* the $\sum/\max$ rather than factoring it out — algebraically equivalent but procedurally error-prone.
- **Diagram tip** (lecturer-encouraged): sketch the trellis and, for Viterbi, draw an arrow at each cell showing the surviving backpointer. It makes the decoded path visually obvious to the marker.
