# Supp — HMM Forward and Viterbi Algorithms (Worked Example)

**File:** `raw/text/COM3031_W8_HMM_Forward and Viterbi Algorithms.txt`
**Type:** supplementary-note
**Week:** 8 (exam: Week 7)
**Concepts introduced:** [[forward-algorithm]], [[viterbi-algorithm]]

## Summary
Provides a fully worked numerical example of both the Forward Algorithm and Viterbi Algorithm using the Weather–Activity HMM. Initialisation, recursion, and termination steps are shown with exact numbers.

## Key content

### HMM Parameters (Weather Example)
- Hidden states: $S = \{\text{Rainy (R)}, \text{Sunny (S)}\}$.
- Observations: $O = (\text{Walk}, \text{Shop}, \text{Clean})$.
- Initial distribution: $\pi = (0.6_R,\, 0.4_S)$.
- Transition matrix $A$:
$$A = \begin{pmatrix}0.7 & 0.3 \\ 0.4 & 0.6\end{pmatrix}\quad (\text{row = from, col = to})$$
- Emission matrix $B$:
$$B = \begin{array}{r|ccc} & \text{Walk} & \text{Shop} & \text{Clean}\\\hline \text{Rainy} & 0.1 & 0.4 & 0.5 \\ \text{Sunny} & 0.6 & 0.3 & 0.1\end{array}$$

### Forward Algorithm — Full Calculation

**Initialisation** ($o_1 = \text{Walk}$):
$$\alpha_1(R) = \pi_R\,b_R(\text{Walk}) = 0.6\times0.1 = 0.06$$
$$\alpha_1(S) = \pi_S\,b_S(\text{Walk}) = 0.4\times0.6 = 0.24$$

**Recursion** ($o_2 = \text{Shop}$):
$$\alpha_2(R) = [\alpha_1(R)a_{RR} + \alpha_1(S)a_{SR}]\,b_R(\text{Shop}) = [(0.06)(0.7) + (0.24)(0.4)]\times0.4 = 0.138\times0.4 = 0.0552$$
$$\alpha_2(S) = [\alpha_1(R)a_{RS} + \alpha_1(S)a_{SS}]\,b_S(\text{Shop}) = [(0.06)(0.3) + (0.24)(0.6)]\times0.3 = 0.162\times0.3 = 0.0486$$

**Recursion** ($o_3 = \text{Clean}$):
$$\alpha_3(R) = [(0.0552)(0.7) + (0.0486)(0.4)]\times0.5 = [0.03864 + 0.01944]\times0.5 = 0.02904$$
$$\alpha_3(S) = [(0.0552)(0.3) + (0.0486)(0.6)]\times0.1 = [0.01656 + 0.02916]\times0.1 = 0.004572$$

**Termination**:
$$P(O|\lambda) = \alpha_3(R) + \alpha_3(S) = 0.02904 + 0.004572 = 0.0336$$

### Viterbi Algorithm — Full Calculation

**Initialisation** ($o_1 = \text{Walk}$):
$$v_1(R) = 0.6\times0.1 = 0.06,\quad v_1(S) = 0.4\times0.6 = 0.24$$

**Recursion** ($o_2 = \text{Shop}$):
$$v_2(R) = 0.4\times\max(0.06\times0.7,\; 0.24\times0.4) = 0.4\times\max(0.042, 0.096) = 0.4\times0.096 = 0.0384,\quad \psi_2(R) = S$$
$$v_2(S) = 0.3\times\max(0.06\times0.3,\; 0.24\times0.6) = 0.3\times\max(0.018, 0.144) = 0.3\times0.144 = 0.0432,\quad \psi_2(S) = S$$

**Recursion** ($o_3 = \text{Clean}$):
$$v_3(R) = 0.5\times\max(0.0384\times0.7,\; 0.0432\times0.4) = 0.5\times\max(0.02688, 0.01728) = 0.5\times0.02688 = 0.01344,\quad \psi_3(R) = R$$
$$v_3(S) = 0.1\times\max(0.0384\times0.3,\; 0.0432\times0.6) = 0.1\times\max(0.01152, 0.02592) = 0.1\times0.02592 = 0.002592,\quad \psi_3(S) = S$$

**Termination & Backtracking**:
$$s_3^* = \arg\max(0.01344, 0.002592) = R$$
$$s_2^* = \psi_3(R) = R$$
$$s_1^* = \psi_2(R) = S$$

**Most likely state sequence**: $S \to R \to R$ (Sunny → Rainy → Rainy).

## Exam notes
- Both Forward and Viterbi algorithms are **examinable** with numerical examples. ⚠️
- Key difference: Forward uses $\sum$ (sum over all paths); Viterbi uses $\max$ (best path only).
- Both use same initialisation: $\pi_j b_j(o_1)$.
- Viterbi additionally stores backpointers $\psi_t(j)$.
- No formulas given; algorithm steps must be known from memory.

## Links to concepts
- [[forward-algorithm]]: worked example here
- [[viterbi-algorithm]]: worked example here
- [[hidden-markov-model]]: the model these algorithms operate on
