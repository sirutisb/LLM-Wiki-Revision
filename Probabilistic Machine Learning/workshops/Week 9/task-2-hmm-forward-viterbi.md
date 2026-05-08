# Task 2 — HMM: Baum–Welch, Viterbi, and the Forward Algorithm

**Workshop tasks 1–5 (HMM section).** From a stream of letters, learn an HMM with two hidden states (vowel / consonant) using Baum–Welch, interpret the emission matrix, decode the most likely state sequence with Viterbi, and compute the observation likelihood with the Forward algorithm.

**Concepts:** [[hidden-markov-model]], [[forward-algorithm]], [[viterbi-algorithm]], [[lecture-w8]], [[supp-hmm-forward-viterbi]]

---

## What we're trying to do

We have a long English document. The **observations** $O_1, O_2, \dots, O_T$ are the letters we actually see (`a, b, c, ..., z`). The **hidden states** $q_t \in \{0, 1\}$ are not labelled in the data — but English letters cluster into two natural groups (vowels vs consonants), and an HMM should be able to discover this structure unsupervised.

An HMM is parameterised by $\lambda = (\boldsymbol{\pi}, A, B)$:

- $\boldsymbol{\pi}$ — **initial state distribution.** $\pi_i = P(q_1 = i)$. Length-2 vector here.
- $A$ — **transition matrix.** $A_{ij} = P(q_{t+1} = j \mid q_t = i)$. Shape $2 \times 2$.
- $B$ — **emission matrix.** $B_{i,k} = P(O_t = v_k \mid q_t = i)$. Shape $2 \times 26$ (one column per letter).

The workshop walks through the **three canonical HMM problems**:

1. **Learning** ($\lambda$ unknown, observations given) — Baum–Welch (Tasks 1–2).
2. **Decoding** (most likely hidden sequence given $\lambda$ and $O$) — Viterbi (Task 4).
3. **Evaluation** (likelihood of $O$ given $\lambda$) — Forward algorithm (Task 5).

Task 3 is just *interpreting* the learned $B$ to confirm the model has rediscovered the vowel/consonant split.

---

## Cell-by-cell walkthrough

### Cell 1 — Load the document into a flat list of letters

```python
import numpy as np, matplotlib.pyplot as plt, mchmm as mc

strings = []
with open('dict_eng.txt', 'r') as f:
    for line in f:
        for ch in line.lower():
            if ch.isalpha():
                strings.append(ch)
print(len(strings), strings[:30])
```

We strip everything except letters and lowercase them. The PDF says the result has **1743 alphabets** — that's our sanity check. `strings` is now a length-1743 list like `['n','e','w','j','e','r','s','e','y',...]`.

This is our observation sequence $O = (O_1, \dots, O_{1743})$ over the alphabet $V = \{a, b, \dots, z\}$.

### Cell 2 — Train an HMM with Baum–Welch

```python
a = mc.HiddenMarkovModel().from_baum_welch(strings, states=['0', '1'])

print('pi  =', a.pi)            # initial state probabilities
print('A   =', a.tp)            # transition matrix
print('B   =', a.ep)            # emission matrix

A_matrix = a.tp
B_matrix = a.ep
tab      = np.array(list(zip(a.observations, range(len(a.observations)))))
```

`mc.HiddenMarkovModel().from_baum_welch(...)` runs the **Baum–Welch (forward–backward) EM algorithm**:

- **E-step:** with the current $\lambda$, compute the forward variables $\alpha_t(i)$, backward variables $\beta_t(i)$, and the smoothed posteriors $\gamma_t(i) = P(q_t = i \mid O, \lambda)$ and pairwise posteriors $\xi_t(i, j) = P(q_t = i, q_{t+1} = j \mid O, \lambda)$.
- **M-step:** re-estimate
  $$
  \pi_i = \gamma_1(i), \quad A_{ij} = \frac{\sum_t \xi_t(i,j)}{\sum_t \gamma_t(i)}, \quad B_{i,k} = \frac{\sum_{t : O_t = v_k} \gamma_t(i)}{\sum_t \gamma_t(i)}.
  $$
- Repeat until log-likelihood converges.

The output is a *local* maximum of $P(O \mid \lambda)$. Because EM is non-convex, runs from different random inits can land on different solutions — sometimes state 0 = vowels, sometimes state 1 = vowels. That's fine; the *split* is the meaningful thing.

### Cell 3 — Interpret $B$

For each letter $v_k$ (column of $B$), look at which row has the bigger probability. If $B_{1, \text{a}} > B_{0, \text{a}}$ then state 1 emits 'a' more readily, so state 1 is the **vowel** state.

The letters `a, e, i, o, u` should all have their max in the same row; `b, c, d, f, g, ...` should have their max in the *other* row. That's the model rediscovering the vowel/consonant distinction with no supervision — which is the whole point of the exercise.

### Cell 4 — Visualisation

```python
max_index_col = np.argmax(np.transpose(B_matrix), axis=1)
plt.scatter(tab[:,0], max_index_col)
```

For each observation symbol (letter on the x-axis), plot which hidden state most likely emitted it (0 or 1 on the y-axis). You should see five letters cluster on one horizontal line and twenty-one on the other — the vowel/consonant split made visible.

### Cell 6 — Viterbi decoding (the most-probable hidden sequence)

```python
seq, log_prob = a.viterbi(strings)
print(seq[:50])
print('log P(O, q* | lambda) =', log_prob)
```

Viterbi answers: *what is the single most likely sequence of hidden states $q^* = \arg\max_q P(q \mid O, \lambda)$?* The recursion is
$$
\delta_t(j) = \max_{i} \big[\delta_{t-1}(i)\, A_{ij}\big]\, B_{j, O_t}, \qquad \delta_1(j) = \pi_j\, B_{j, O_1},
$$
with backpointers
$$
\psi_t(j) = \arg\max_{i} \big[\delta_{t-1}(i)\, A_{ij}\big].
$$
At the end, $q_T^* = \arg\max_j \delta_T(j)$ and we walk the backpointers backwards: $q_{t}^* = \psi_{t+1}(q_{t+1}^*)$.

**Key contrast with the Forward algorithm:** Forward uses a `sum` over previous states ($\alpha_t(j) = \sum_i \alpha_{t-1}(i) A_{ij} \cdot B_{j, O_t}$) — it computes a *marginal probability*. Viterbi uses a `max` and stores backpointers — it computes a *single best path*.

In practice both are run in **log-space** (replace products with sums of logs, replace `max(prod)` with `max(sum)`) to avoid underflow when $T$ is large. With $T = 1743$ this is essential.

For our document, the decoded sequence $q^*$ should alternate roughly the way real English does: consonants and vowels rarely chain into long blocks of the same kind, so you'll see frequent state switches. See [[viterbi-algorithm]] and [[supp-hmm-forward-viterbi]].

### Cell 7 — Visualise the Viterbi path

A simple way: scatter `t` against `q*[t]` for the first ~80 letters of the document. You'll see the model alternating between the two states tracking the actual vowel/consonant pattern of the text.

### Cell 8 — Forward algorithm (likelihood of the observation sequence)

```python
log_p_O = a.forward(strings)        # log P(O | lambda)
print('log-likelihood =', log_p_O)
```

The Forward algorithm computes
$$
P(O \mid \lambda) = \sum_{q_1, \dots, q_T} P(O, q \mid \lambda)
$$
*efficiently* via dynamic programming. The forward variable
$$
\alpha_t(i) = P(O_1, \dots, O_t,\; q_t = i \mid \lambda)
$$
satisfies
$$
\alpha_1(i) = \pi_i\, B_{i, O_1}, \qquad
\alpha_{t+1}(j) = \Big[\sum_{i=1}^N \alpha_t(i)\, A_{ij}\Big] B_{j, O_{t+1}},
$$
and the answer is the termination
$$
P(O \mid \lambda) = \sum_{i=1}^N \alpha_T(i).
$$

**Why this is non-trivial:** the brute-force sum has $N^T = 2^{1743}$ terms. The DP collapses it to $O(N^2 T)$ — for us, $\sim 2^2 \cdot 1743 \approx 7000$ operations.

The number you get back will be a large *negative* log-likelihood: $\log P(O \mid \lambda) \approx -1743 \cdot \log_2 26 \cdot \ln 2$ in the worst (uniform) case, and somewhat better than that for our trained model because it has learned structure.

---

## How the three algorithms fit together

| Problem | Question | Algorithm | Recursion uses | Output |
|---------|----------|-----------|----------------|--------|
| Evaluation | $P(O \mid \lambda) = ?$ | **Forward** | sum | scalar likelihood |
| Decoding | $\arg\max_q P(q \mid O, \lambda) = ?$ | **Viterbi** | max + backpointers | best state path |
| Learning | $\arg\max_\lambda P(O \mid \lambda) = ?$ | **Baum–Welch** (EM, uses Forward + Backward in E-step) | sum | trained $\lambda$ |

All three share the same DP skeleton — the only differences are (a) whether you sum or max over the previous state, and (b) whether you also run a backward pass.

---

## What to take away for the exam

- **HMM parameters:** $\lambda = (\pi, A, B)$. Memorise the shapes: $\pi \in \mathbb{R}^N$, $A \in \mathbb{R}^{N \times N}$, $B \in \mathbb{R}^{N \times M}$, where $N$ = number of states and $M$ = size of the observation alphabet. ⚠️ *No formula sheet.*
- **Three classic problems:** evaluation (Forward), decoding (Viterbi), learning (Baum–Welch). You should be able to state which algorithm solves which.
- **Forward recursion — write from memory:**
  $$
  \alpha_1(i) = \pi_i B_{i, O_1}, \quad \alpha_{t+1}(j) = \Big[\sum_i \alpha_t(i) A_{ij}\Big] B_{j, O_{t+1}}, \quad P(O \mid \lambda) = \sum_i \alpha_T(i).
  $$
- **Viterbi recursion — write from memory:**
  $$
  \delta_1(i) = \pi_i B_{i, O_1}, \quad \delta_{t+1}(j) = \max_i [\delta_t(i) A_{ij}]\, B_{j, O_{t+1}}, \quad \psi_{t+1}(j) = \arg\max_i [\delta_t(i) A_{ij}].
  $$
  Then $q_T^* = \arg\max_i \delta_T(i)$ and backtrack via $q_t^* = \psi_{t+1}(q_{t+1}^*)$.
- **Forward vs Viterbi in one line:** *same DP, sum vs max, plus backpointers in Viterbi.* Forward gives a probability; Viterbi gives a path.
- **Complexity:** $O(N^2 T)$ for both — this is the punchline of the dynamic programming trick. Naive marginalisation would be $O(N^T)$.
- **Numerical stability:** always implement in log-space (replace $\prod \to \sum$, $\max \prod \to \max \sum$). For Forward you also need the log-sum-exp trick.
- **Likely exam style:**
  - **Bookwork:** state the three problems and which algorithm each.
  - **Derivation:** derive $\alpha_t$ or $\delta_t$ recursion from the joint $P(O, q \mid \lambda) = \pi_{q_1} B_{q_1, O_1} \prod_t A_{q_{t-1}, q_t} B_{q_t, O_t}$.
  - **Worked numerical:** small HMM ($N=2$, $T=3$ or so), compute $\alpha$ table or run Viterbi by hand. See [[supp-hmm-forward-viterbi]] for the pattern.
- **Baum–Welch is EM:** E-step computes $\gamma_t(i), \xi_t(i,j)$ via Forward + Backward; M-step plugs in the closed-form re-estimates above. You don't need to derive it, but you should know that it's an EM algorithm and only finds a *local* optimum.
