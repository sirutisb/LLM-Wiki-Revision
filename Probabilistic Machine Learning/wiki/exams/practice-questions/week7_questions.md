# Week 7 Practice Questions — Hidden Markov Models

> ⚠️ **No formula sheet provided for Week 7.** All algorithm steps (initialisation, recursion, termination, backtracking) must be recalled from memory.
>
> **Exam context:** Every year, *either* the Forward algorithm *or* the Viterbi algorithm is examined in depth. Both are prepared here to equal standard. The other typically appears as a shorter conceptual or comparison question.

---

## Conceptual / Bookwork

### Q1 — HMM Structure [4 marks]

An HMM is defined by the triple $\lambda = (A, B, \pi)$.

**(a)** State precisely what each of $A$, $B$, and $\pi$ represents, including the dimensions of each matrix or vector for a model with $N$ hidden states and $M$ distinct observation symbols. [3 marks]

**(b)** HMMs rest on two key conditional independence assumptions. State both assumptions. [2 marks]

**(c)** Write down the joint distribution $p(s_{1:T},\, o_{1:T})$ in terms of $A$, $B$, and $\pi$. [2 marks]

---

### Q2 — Three Problems of HMMs [3 marks]

HMMs give rise to three fundamental computational problems.

**(a)** Complete the table below.

| Problem                 | Informal goal                              | Algorithm used |
| ----------------------- | ------------------------------------------ | -------------- |
| Evaluation / Likelihood | Compute $P(O \mid \lambda)$                | ???            |
| Decoding                | Find $\arg\max_S\, P(S \mid O, \lambda)$   | ???            |
| Learning                | Estimate $\lambda$ from observed sequences | ???            |

**(b)** Of the three algorithms named above, which two are examinable in COM3031? Which one is **not** examinable (though you should be able to name it)? [1 mark]

**(c)** Why is it computationally infeasible to solve the Evaluation or Decoding problems by brute-force enumeration of all state sequences? Give the complexity of the naïve approach versus the dynamic-programming solution. [2 marks]

---

### Q3 — Forward vs Viterbi: Conceptual Comparison [5 marks]

**(a)** Define the forward variable $\alpha_t(i)$ in words and as a probability expression. [2 marks]

**(b)** Define the Viterbi variable $v_t(j)$ in words and as a probability expression. [2 marks]

**(c)** Both algorithms share the same initialisation formula. State it, and explain in one sentence why the initialisation is identical despite the two algorithms having different goals. [2 marks]

**(d)** The recursion steps of the two algorithms differ by a single mathematical operation. Identify the operation that differs, explain what it computes in each case, and state why that difference leads to different outputs. [3 marks]

**(e)** Viterbi requires an additional data structure that the Forward algorithm does not. Name this structure and explain why it is needed. [2 marks]

---

## Practical / Calculation

> **Setup for Q4 and Q5 — Coin-Flip HMM**
>
> A statistician models a sequence of coin flips as an HMM with two hidden states:
> $S = \{F,\, U\}$ (Fair coin, Unfair coin)
>
> and two observation symbols: $O = \{H,\, T\}$ (Heads, Tails).
>
> The model parameters are:
>
> **Initial distribution:**
> $$\pi_F = 0.5, \quad \pi_U = 0.5$$
>
> **Transition matrix** (rows = from, columns = to):
>
> |   | F | U |
> |---|---|---|
> | **F** | 0.8 | 0.2 |
> | **U** | 0.3 | 0.7 |
>
> So $a_{FF} = 0.8$, $a_{FU} = 0.2$, $a_{UF} = 0.3$, $a_{UU} = 0.7$.
>
> **Emission matrix** (rows = state, columns = observation):
>
> |   | H | T |
> |---|---|---|
> | **F** | 0.5 | 0.5 |
> | **U** | 0.9 | 0.1 |
>
> So $b_F(H) = 0.5$, $b_F(T) = 0.5$, $b_U(H) = 0.9$, $b_U(T) = 0.1$.
>
> **Observation sequence:** $O = (H, H, T)$

---

### Q4 — Forward Algorithm [12 marks]

⚠️ *No formulas given — you must recall all steps.*

**(a)** State the three steps of the Forward algorithm (initialisation, recursion, termination) in full, using standard notation. Do not yet substitute numbers. [4 marks]

**(b)** Compute the forward variables $\alpha_1(F)$ and $\alpha_1(U)$ for the first observation $o_1 = H$. Show all working. [2 marks]

**(c)** Compute the forward variables $\alpha_2(F)$ and $\alpha_2(U)$ for $o_2 = H$. Show all working. [3 marks]

**(d)** Compute the forward variables $\alpha_3(F)$ and $\alpha_3(U)$ for $o_3 = T$. Show all working. [3 marks]

**(e)** Hence compute $P(O \mid \lambda)$, the probability of observing the sequence $(H, H, T)$. [1 mark]

**(f)** Summarise your results in the table format below:

| $t$ | Observation | $\alpha_t(F)$ | $\alpha_t(U)$ |
|-----|-------------|--------------|--------------|
| 1 | H | | |
| 2 | H | | |
| 3 | T | | |

---

### Q5 — Viterbi Algorithm [14 marks]

⚠️ *No formulas given — you must recall all steps including backtracking.*

Use the same Coin-Flip HMM and observation sequence $O = (H, H, T)$ as Q4.

**(a)** State the four steps of the Viterbi algorithm (initialisation, recursion, termination, backtracking) in full, using standard notation. Include the formula for the backpointer $\psi_t(j)$. Do not yet substitute numbers. [5 marks]

**(b)** Compute the Viterbi variables $v_1(F)$ and $v_1(U)$ for $o_1 = H$. [2 marks]

**(c)** Compute $v_2(F)$, $v_2(U)$, $\psi_2(F)$, and $\psi_2(U)$ for $o_2 = H$. Show the candidate values for each maximisation explicitly. [4 marks]

**(d)** Compute $v_3(F)$, $v_3(U)$, $\psi_3(F)$, and $\psi_3(U)$ for $o_3 = T$. [4 marks]

**(e)** Determine $s_3^*$ from the termination step. [1 mark]

**(f)** Perform backtracking to recover the full optimal state sequence $s_{1:3}^*$. State the final answer clearly as a sequence of state labels. [2 marks]

**(g)** Summarise your results in the table below:

| $t$ | Obs | $v_t(F)$ | $\psi_t(F)$ | $v_t(U)$ | $\psi_t(U)$ |
|-----|-----|----------|-------------|----------|-------------|
| 1 | H | | — | | — |
| 2 | H | | | | |
| 3 | T | | | | |

---

## Answers / Mark Schemes

### A1 — HMM Structure

**(a)**
- $A \in \mathbb{R}^{N \times N}$: the **transition matrix**, where $a_{ij} = P(s_t = j \mid s_{t-1} = i)$. Each row sums to 1.
- $B \in \mathbb{R}^{N \times M}$: the **emission matrix**, where $b_j(o) = P(o_t = o \mid s_t = j)$. Each row sums to 1.
- $\pi \in \mathbb{R}^N$: the **initial distribution**, where $\pi_i = P(s_1 = i)$. Sums to 1.

**(b)**
1. **Markov property**: the current hidden state depends only on the immediately preceding state:
$$P(s_t \mid s_1, \ldots, s_{t-1}) = P(s_t \mid s_{t-1})$$
2. **Observation independence**: the current observation depends only on the current hidden state, not on any other states or observations:
$$P(o_t \mid s_1, \ldots, s_T,\, o_1, \ldots, o_{t-1}) = P(o_t \mid s_t)$$

**(c)**
$$p(s_{1:T},\, o_{1:T}) = \pi_{s_1} \prod_{t=2}^{T} a_{s_{t-1}, s_t} \prod_{t=1}^{T} b_{s_t}(o_t)$$

---

### A2 — Three Problems of HMMs

**(a)**

| Problem | Informal goal | Algorithm used |
|---------|---------------|----------------|
| Evaluation / Likelihood | Compute $P(O \mid \lambda)$ | **Forward algorithm** |
| Decoding | Find $\arg\max_S\, P(S \mid O, \lambda)$ | **Viterbi algorithm** |
| Learning | Estimate $\lambda$ from observed sequences | **Baum–Welch (EM)** |

**(b)** The Forward algorithm and Viterbi algorithm are examinable. Baum–Welch is **not** examinable (but students should be able to name it and identify it as the learning algorithm).

**(c)** With $N$ hidden states and a sequence of length $T$, there are $N^T$ possible hidden state sequences. For $N = 2$, $T = 100$ this is $2^{100} \approx 10^{30}$ — computationally infeasible. Dynamic programming (Forward / Viterbi) reduces the complexity to $O(N^2 T)$ by reusing intermediate results, making it tractable.

---

### A3 — Forward vs Viterbi: Conceptual Comparison

**(a)** The forward variable $\alpha_t(i)$ is the joint probability of observing the partial sequence $o_1, \ldots, o_t$ **and** being in hidden state $i$ at time $t$:
$$\alpha_t(i) = P(o_1, o_2, \ldots, o_t,\; s_t = i \mid \lambda)$$

**(b)** The Viterbi variable $v_t(j)$ is the probability of the **most likely** path (over states $s_1, \ldots, s_{t-1}$) that ends in state $j$ at time $t$, consistent with observations $o_1, \ldots, o_t$:
$$v_t(j) = \max_{s_1, \ldots, s_{t-1}} P(s_1, \ldots, s_{t-1},\; s_t = j,\; o_1, \ldots, o_t \mid \lambda)$$

**(c)** Shared initialisation:
$$\alpha_1(j) = v_1(j) = \pi_j\, b_j(o_1)$$
The initialisation is identical because at $t = 1$ there is no previous state to sum over or maximise over — the score of the (unique, trivial) length-1 path is simply the initial state probability times the emission probability.

**(d)** The differing operation is in the recursion:
- **Forward**: $\alpha_t(j) = \left[\displaystyle\sum_i \alpha_{t-1}(i)\, a_{ij}\right] b_j(o_t)$ — uses $\sum$ (summation / marginalisation). This totals the probability of arriving in state $j$ via **any** previous state, computing a total likelihood by integrating over all possible histories.
- **Viterbi**: $v_t(j) = \left[\displaystyle\max_i v_{t-1}(i)\, a_{ij}\right] b_j(o_t)$ — uses $\max$ (maximisation). This keeps only the **single best** incoming path, discarding all sub-optimal partial paths. The result is the probability of the single most likely path to state $j$ at time $t$.

The $\sum$ vs $\max$ difference directly produces different outputs: Forward gives the total marginal likelihood $P(O \mid \lambda)$; Viterbi gives the probability and identity of the best hidden state sequence.

**(e)** Viterbi stores **backpointers** $\psi_t(j) = \arg\max_i v_{t-1}(i)\, a_{ij}$. These record, for each state $j$ at time $t$, which state $i$ at time $t-1$ produced the maximum in the recursion. After the termination step identifies $s_T^*$, the optimal sequence is recovered by following backpointers backward from $t = T$ to $t = 1$. Without backpointers, Viterbi can compute the *score* of the best path but cannot recover the actual *sequence* of states.

---

### A4 — Forward Algorithm (Full Working)

#### Step (a) — Algorithm steps

**Initialisation** ($t = 1$):
$$\alpha_1(j) = \pi_j\, b_j(o_1) \quad \text{for all states } j$$

**Recursion** ($t = 2, \ldots, T$):
$$\alpha_t(j) = \left[\sum_{i} \alpha_{t-1}(i)\, a_{ij}\right] b_j(o_t) \quad \text{for all states } j$$

**Termination**:
$$P(O \mid \lambda) = \sum_{i} \alpha_T(i)$$

---

#### Step (b) — Initialisation ($t=1$, $o_1 = H$)

$$\alpha_1(F) = \pi_F \cdot b_F(H) = 0.5 \times 0.5 = \mathbf{0.25}$$

$$\alpha_1(U) = \pi_U \cdot b_U(H) = 0.5 \times 0.9 = \mathbf{0.45}$$

---

#### Step (c) — Recursion ($t=2$, $o_2 = H$)

$$\alpha_2(F) = \bigl[\alpha_1(F)\cdot a_{FF} + \alpha_1(U)\cdot a_{UF}\bigr] \cdot b_F(H)$$
$$= \bigl[(0.25)(0.8) + (0.45)(0.3)\bigr] \times 0.5$$
$$= \bigl[0.200 + 0.135\bigr] \times 0.5 = 0.335 \times 0.5 = \mathbf{0.1675}$$

$$\alpha_2(U) = \bigl[\alpha_1(F)\cdot a_{FU} + \alpha_1(U)\cdot a_{UU}\bigr] \cdot b_U(H)$$
$$= \bigl[(0.25)(0.2) + (0.45)(0.7)\bigr] \times 0.9$$
$$= \bigl[0.050 + 0.315\bigr] \times 0.9 = 0.365 \times 0.9 = \mathbf{0.3285}$$

---

#### Step (d) — Recursion ($t=3$, $o_3 = T$)

$$\alpha_3(F) = \bigl[\alpha_2(F)\cdot a_{FF} + \alpha_2(U)\cdot a_{UF}\bigr] \cdot b_F(T)$$
$$= \bigl[(0.1675)(0.8) + (0.3285)(0.3)\bigr] \times 0.5$$
$$= \bigl[0.13400 + 0.09855\bigr] \times 0.5 = 0.23255 \times 0.5 = \mathbf{0.116275}$$

$$\alpha_3(U) = \bigl[\alpha_2(F)\cdot a_{FU} + \alpha_2(U)\cdot a_{UU}\bigr] \cdot b_U(T)$$
$$= \bigl[(0.1675)(0.2) + (0.3285)(0.7)\bigr] \times 0.1$$
$$= \bigl[0.03350 + 0.22995\bigr] \times 0.1 = 0.26345 \times 0.1 = \mathbf{0.026345}$$

---

#### Step (e) — Termination

$$P(O \mid \lambda) = \alpha_3(F) + \alpha_3(U) = 0.116275 + 0.026345 = \mathbf{0.14262}$$

---

#### Step (f) — Summary table

| $t$ | Observation | $\alpha_t(F)$ | $\alpha_t(U)$ |
|-----|-------------|--------------|--------------|
| 1 | H | 0.2500 | 0.4500 |
| 2 | H | 0.1675 | 0.3285 |
| 3 | T | 0.116275 | 0.026345 |

$$\boxed{P(O \mid \lambda) = 0.14262}$$

---

### A5 — Viterbi Algorithm (Full Working)

#### Step (a) — Algorithm steps

**Initialisation** ($t = 1$):
$$v_1(j) = \pi_j\, b_j(o_1) \quad \text{for all states } j$$
(No backpointer at $t=1$.)

**Recursion** ($t = 2, \ldots, T$):
$$v_t(j) = \left[\max_{i}\; v_{t-1}(i)\, a_{ij}\right] b_j(o_t)$$
$$\psi_t(j) = \arg\max_{i}\; v_{t-1}(i)\, a_{ij}$$

**Termination**:
$$s_T^* = \arg\max_{j}\; v_T(j)$$

**Backtracking** (recover full sequence):
$$s_{t-1}^* = \psi_t(s_t^*), \quad \text{for } t = T, T-1, \ldots, 2$$

---

#### Step (b) — Initialisation ($t=1$, $o_1 = H$)

$$v_1(F) = \pi_F \cdot b_F(H) = 0.5 \times 0.5 = \mathbf{0.25}$$

$$v_1(U) = \pi_U \cdot b_U(H) = 0.5 \times 0.9 = \mathbf{0.45}$$

(Identical to Forward step (b), as expected.)

---

#### Step (c) — Recursion ($t=2$, $o_2 = H$)

**For state $F$:**

Candidates: $v_1(F)\cdot a_{FF} = 0.25 \times 0.8 = 0.200$ and $v_1(U)\cdot a_{UF} = 0.45 \times 0.3 = 0.135$

$$\max(0.200,\; 0.135) = 0.200 \quad \Rightarrow \quad \psi_2(F) = F$$

$$v_2(F) = 0.200 \times b_F(H) = 0.200 \times 0.5 = \mathbf{0.1000}$$

**For state $U$:**

Candidates: $v_1(F)\cdot a_{FU} = 0.25 \times 0.2 = 0.050$ and $v_1(U)\cdot a_{UU} = 0.45 \times 0.7 = 0.315$

$$\max(0.050,\; 0.315) = 0.315 \quad \Rightarrow \quad \psi_2(U) = U$$

$$v_2(U) = 0.315 \times b_U(H) = 0.315 \times 0.9 = \mathbf{0.2835}$$

---

#### Step (d) — Recursion ($t=3$, $o_3 = T$)

**For state $F$:**

Candidates: $v_2(F)\cdot a_{FF} = 0.1000 \times 0.8 = 0.0800$ and $v_2(U)\cdot a_{UF} = 0.2835 \times 0.3 = 0.08505$

$$\max(0.0800,\; 0.08505) = 0.08505 \quad \Rightarrow \quad \psi_3(F) = U$$

$$v_3(F) = 0.08505 \times b_F(T) = 0.08505 \times 0.5 = \mathbf{0.042525}$$

**For state $U$:**

Candidates: $v_2(F)\cdot a_{FU} = 0.1000 \times 0.2 = 0.0200$ and $v_2(U)\cdot a_{UU} = 0.2835 \times 0.7 = 0.19845$

$$\max(0.0200,\; 0.19845) = 0.19845 \quad \Rightarrow \quad \psi_3(U) = U$$

$$v_3(U) = 0.19845 \times b_U(T) = 0.19845 \times 0.1 = \mathbf{0.019845}$$

---

#### Step (e) — Termination

$$s_3^* = \arg\max\bigl(v_3(F),\; v_3(U)\bigr) = \arg\max(0.042525,\; 0.019845) = \mathbf{F}$$

The most likely final state is **Fair**.

---

#### Step (f) — Backtracking

Follow backpointers from $t=3$ backwards:

$$s_3^* = F$$
$$s_2^* = \psi_3(s_3^*) = \psi_3(F) = U$$
$$s_1^* = \psi_2(s_2^*) = \psi_2(U) = U$$

**Most likely hidden state sequence:**

$$\boxed{s_{1:3}^* = (U,\; U,\; F) \quad \text{i.e. Unfair} \to \text{Unfair} \to \text{Fair}}$$

*Interpretation:* The model infers that the first two coin flips (both Heads) were most likely produced by the unfair coin (which emits Heads with probability 0.9), and the Tails on the third flip prompted a transition to the fair coin.

---

#### Step (g) — Summary table

| $t$ | Obs | $v_t(F)$ | $\psi_t(F)$ | $v_t(U)$ | $\psi_t(U)$ |
|-----|-----|----------|-------------|----------|-------------|
| 1 | H | 0.2500 | — | 0.4500 | — |
| 2 | H | 0.1000 | F | 0.2835 | U |
| 3 | T | 0.042525 | U | 0.019845 | U |

Termination: $\arg\max(0.042525,\; 0.019845) = F$, so $s_3^* = F$.

Backtrack: $s_2^* = \psi_3(F) = U$; $s_1^* = \psi_2(U) = U$.

**Optimal sequence: Unfair → Unfair → Fair**

---

## Examiner's Notes (for self-assessment)

**Mark scheme hints:**
- In Forward recursion: award method marks even if arithmetic slips, provided the formula structure (sum, multiply by emission) is correct.
- In Viterbi: **always credit backpointers separately** — a student who computes all $v_t$ correctly but omits backpointers and cannot backtrack should lose marks only on the backtracking steps.
- The Forward and Viterbi initialisation steps are identical — a correct statement of both earns full marks without restating the formula twice.
- The key distinction examiners look for: Forward uses $\sum$, Viterbi uses $\max$. This must be explicit in any comparison answer.

**Common errors to watch for:**
- Confusing $a_{ij}$ (from $i$ to $j$) with $a_{ji}$ — always state "row = from state, column = to state" and double-check against the given matrix.
- Forgetting to multiply by $b_j(o_t)$ at each recursion step.
- In Viterbi: computing the final probability (the score) but failing to backtrack to produce the state sequence.
- In Forward termination: summing only one forward variable instead of all $N$.
