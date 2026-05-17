# Week 7 — Hidden Markov Models: Past Paper Questions

**Source papers:** COM3023 May 2022, 2023, 2024, 2025
**Topic coverage:** Markov process definition; "hidden" in HMMs; three problems of interest; reading $\pi$, $A$, $B$ from a diagram; drawing transition diagrams; enumerating state sequences; **Forward algorithm** for likelihood; **Viterbi algorithm** for most-likely path; stationary vs non-stationary sequential data
**Formula sheet:** ⚠️ None provided — Forward and Viterbi recurrences must be recalled from memory (only Forward + Viterbi are examinable for the new module)

---

## COM3023 May 2022 — Question 3 (25 marks)

### Part (a) — 4 marks
What is a Markov process?

### Part (b) — 2 marks
What is hidden in hidden Markov models?

### Part (c) — 6 marks
What are three main problems of interest in hidden Markov models?

### Part (d) — 4 marks
Name two methods for estimating the likelihood of all possible state sequences in hidden Markov models.

### Part (e) — 4 marks
What is the transition probability matrix for the hidden Markov model shown in Figure 2?

*Figure 2 details: States $s_1, s_2$; observations $o_1, o_2, o_3$. Initial: $\text{start} \to s_1 = 0.6$, $\text{start} \to s_2 = 0.4$. Transitions: $s_1 \to s_1 = 0.0$, $s_1 \to s_2 = 1.0$; $s_2 \to s_1 = 0.3$, $s_2 \to s_2 = 0.7$. Emissions: $s_1 \to o_1 = 0.8$, $s_1 \to o_2 = 0.1$, $s_1 \to o_3 = 0.1$; $s_2 \to o_1 = 0.2$, $s_2 \to o_2 = 0.3$, $s_2 \to o_3 = 0.5$.*

### Part (f) — 5 marks
In the hidden Markov model shown in Figure 3, the observation sequence is (Shopping, Cleaning). How many state sequences are possible? State all possible state sequences.

*Figure 3 details: States: Rainy, Sunny. Initial: $\text{start} \to \text{Rainy} = 0.3$, $\text{start} \to \text{Sunny} = 0.7$. Transitions: Rainy → Rainy = 0.7, Rainy → Sunny = 0.3; Sunny → Rainy = 0.6, Sunny → Sunny = 0.4. Emissions: Rainy → Shopping = 0.1, Rainy → Cleaning = 0.9; Sunny → Shopping = 0.8, Sunny → Cleaning = 0.2.*

---

## COM3023 May 2023 — Question 3 (22 marks)

### Part (a) — 8 marks
A hidden Markov model can be represented as $\lambda = (S, O, A, B, \pi)$, where $S = (s_1, \dots, s_n)$ are the states, $O = (o_1, \dots, o_t)$ are the observations, $A$ is the transition probability matrix, $B$ is the emission probability matrix and $\pi$ is the initial probability (or start) vector. For the following information given about the hidden Markov model, draw a transition diagram.

- $S = (s_1, s_2)$
- $O = (o_1, o_2, o_3)$
- $A = \begin{bmatrix} 0.2 & 0.8 \\ 0.3 & 0.7 \end{bmatrix}$
- $B = \begin{bmatrix} 0.8 & 0.1 & 0.1 \\ 0.2 & 0.3 & 0.5 \end{bmatrix}$
- $\pi = [0.5,\ 0.5]$

### Part (b) — 14 marks
For the observation sequence $(o_1 \to o_2 \to o_3)$, use the **forward algorithm** to estimate the likelihood of the hidden Markov model in the previous question. Show your calculations in different steps of the forward algorithm. You can show the answers up to four decimal places.

---

## COM3023 May 2024 — Question 4 (18 marks)

A hidden Markov model can be represented as $\lambda = (S, O, A, B, \pi)$, where $S = (s_1, \dots, s_n)$ are the states, $O = (o_1, \dots, o_t)$ are the observations, $A$ is the transition probability matrix, $B$ is the emission probability matrix and $\pi$ is the initial probability vector. *Figure 1 (in the original paper) shows a partially drawn diagram of a hidden Markov model in which $s_1$ and $s_2$ are states.*

### Part (a) — 4 marks
For the model shown in Figure 1, what are the initial probability vector $\pi$ and the transition probability matrix $A$?

### Part (b) — 4 marks
Complete the above transition diagram given the emission probability matrix
$$B = \begin{bmatrix} 0.7 & 0.3 \\ 0.9 & 0.1 \end{bmatrix}.$$

### Part (c) — 10 marks
For the observation sequence $(o_1 \to o_2)$, use the **Viterbi algorithm** to estimate the likelihood of the hidden Markov model in the previous question. Show your calculations at each step of the Viterbi algorithm. Give your answers up to four decimal places.

---

## COM3023 May 2025 — Question 4 (19 marks)

### Part (a) — 5 marks
Define sequential data and explain the difference between stationary and non-stationary sequential data. Provide one example for each type.

### Part (b) — 14 marks
Consider an HMM modeling the behavior of a robot navigating a building. The robot's states represent its location: $S = \{\text{Room1}, \text{Room2}\}$, and its observations correspond to actions: $O = \{\text{MoveForward}, \text{TurnLeft}, \text{PickUpItem}\}$. The parameters of the HMM are:

- **Transition matrix:** $A = \begin{bmatrix} 0.8 & 0.2 \\ 0.3 & 0.7 \end{bmatrix}$
- **Emission matrix:** $B = \begin{bmatrix} 0.3 & 0.4 & 0.3 \\ 0.2 & 0.6 & 0.2 \end{bmatrix}$
- **Initial probabilities:** $\pi = [0.5,\ 0.5]$

Use the **Forward algorithm** to calculate the likelihood $P(O \mid \lambda)$ for the observation sequence $O = \{\text{MoveForward}, \text{TurnLeft}, \text{PickUpItem}\}$. Show your calculations (up to four decimal places) step by step.

---

## Pattern Analysis

| Paper | Marks in Week 7 | Conceptual / reading-diagram | Algorithm-trace |
|-------|------------------|-------------------------------|-----------------|
| 2022 (Q3) | 25 | Markov process; "hidden"; three problems; two likelihood methods; read $A$ from diagram; enumerate state sequences | — (no algorithm trace, but lots of structural questions) |
| 2023 (Q3) | 22 | Draw transition diagram from $\lambda$ | Forward algorithm, 3-symbol sequence, 4 d.p. |
| 2024 (Q4) | 18 | Read $\pi$ + $A$; complete diagram with $B$ | Viterbi algorithm, 2-symbol sequence, 4 d.p. |
| 2025 (Q4) | 19 | Sequential data; stationary vs non-stationary | Forward algorithm, 3-symbol sequence, 4 d.p. |

**Consistent exam pattern:**
1. **Conceptual / diagrammatic warm-up** (~4–10 marks) — Markov process definition, what's hidden, reading $\pi/A/B$ off a diagram, or drawing one from given matrices
2. **Algorithm trace** (~10–14 marks) — either Forward (sequence likelihood) or Viterbi (most-likely state sequence), almost always answered to **four decimal places**
3. Forward has appeared in 2023 & 2025; Viterbi in 2024 → both are equally likely. **22May has no algorithm trace** — instead it tests structural understanding (enumerating sequences, naming methods)

**Must know from memory (no formula sheet):**
- **HMM tuple:** $\lambda = (S, O, A, B, \pi)$ with $A_{ij} = P(s_t = j \mid s_{t-1} = i)$, $B_{jk} = P(o_t = k \mid s_t = j)$, $\pi_i = P(s_1 = i)$
- **Three classical problems:** (1) **Evaluation** — likelihood $P(O \mid \lambda)$ → Forward; (2) **Decoding** — most-likely state sequence → Viterbi; (3) **Learning** — estimate parameters → Baum–Welch
- **Forward recursion:**
  - Init: $\alpha_1(i) = \pi_i\, b_i(o_1)$
  - Recursion: $\alpha_{t+1}(j) = \left[\sum_i \alpha_t(i)\, a_{ij}\right] b_j(o_{t+1})$
  - Termination: $P(O \mid \lambda) = \sum_i \alpha_T(i)$
- **Viterbi recursion:**
  - Init: $\delta_1(i) = \pi_i\, b_i(o_1)$, $\psi_1(i) = 0$
  - Recursion: $\delta_{t+1}(j) = \max_i [\delta_t(i)\, a_{ij}]\, b_j(o_{t+1})$; $\psi_{t+1}(j) = \arg\max_i [\delta_t(i)\, a_{ij}]$
  - Termination: $P^* = \max_i \delta_T(i)$; backtrack via $\psi$ to recover the best state sequence
- **Forward vs Viterbi:** Forward **sums** over paths (likelihood); Viterbi **maxes** over paths (decoding)
- **Stationary sequential data:** statistical properties (mean, variance, transition probabilities) are time-invariant — e.g., HMM with fixed $A, B$. **Non-stationary:** properties change over time — e.g., financial time series with regime changes
- Number of possible state sequences for $T$ observations with $|S|$ states $= |S|^T$ (2022 Q3(f): $|S|=2, T=2 \Rightarrow 4$ sequences)
