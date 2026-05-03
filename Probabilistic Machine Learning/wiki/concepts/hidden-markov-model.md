# Hidden Markov Model (HMM)

**Type:** model
**Week:** 7 (exam numbering)
**Related:** [[forward-algorithm]], [[viterbi-algorithm]], [[baum-welch-algorithm]], [[mcmc]]
**Source:** [[lecture-w8]], [[supp-hmm-forward-viterbi]]

## Definition
A Hidden Markov Model (HMM) is a probabilistic model for sequential data where an unobservable (hidden) Markov chain generates observable outputs according to state-dependent emission distributions.

## Motivation
Many real-world sequences have temporal dependence (speech, language, finance, biology). A simple Markov chain models sequences of *observable* states, but often the true state is hidden — we only observe noisy emissions. HMMs explicitly model this latent structure and allow inference over the hidden states.

## How it works

### Model Components
An HMM is defined by $\lambda = (A, B, \pi)$:
- **State space**: $S = \{1,\ldots,N\}$ — discrete hidden states $s_t$.
- **Observation space**: $O = \{1,\ldots,M\}$ — discrete observations $o_t$.
- **Transition matrix** $A \in \mathbb{R}^{N\times N}$: $a_{ij} = P(s_t = j|s_{t-1} = i)$, rows sum to 1.
- **Emission matrix** $B \in \mathbb{R}^{N\times M}$: $b_j(o) = P(o_t = o|s_t = j)$, rows sum to 1.
- **Initial distribution** $\pi \in \mathbb{R}^N$: $\pi_i = P(s_1 = i)$, sums to 1.

### Key Assumptions
1. **Markov property**: $P(s_t|s_1,\ldots,s_{t-1}) = P(s_t|s_{t-1})$.
2. **Observation independence**: $P(o_t|s_1,\ldots,s_T, o_1,\ldots,o_{t-1}) = P(o_t|s_t)$.

### Joint Distribution
$$p(s_{1:T}, o_{1:T}) = \pi_{s_1}\prod_{t=2}^T a_{s_{t-1}s_t}\prod_{t=1}^T b_{s_t}(o_t)$$

### Three Fundamental Problems
| Problem | Goal | Algorithm |
|---------|------|-----------|
| Likelihood (Evaluation) | Compute $P(O|\lambda)$ | Forward algorithm |
| Decoding | Find $\arg\max_S P(S|O,\lambda)$ | Viterbi algorithm |
| Learning | Estimate $\lambda$ from $O$ | Baum–Welch (EM) |

## Key derivation

### Why Dynamic Programming?
Naïve likelihood: sum over all $N^T$ state sequences — exponential in $T$.
Dynamic programming reuses intermediate probabilities:
- **Forward**: $\alpha_t(i) = P(o_1,\ldots,o_t, s_t=i|\lambda)$ — probability of partial observation up to time $t$, ending in state $i$.

See [[forward-algorithm]] and [[viterbi-algorithm]] for full algorithms.

⚠️ *Both algorithms are examinable.*

## Parameters & intuition

**Weather example** (from lectures):
- Hidden states: {Rainy, Sunny}.
- Observations: {Walk, Shop, Clean}.
- Transition: $P(\text{Rainy}|\text{Rainy}) = 0.7$, $P(\text{Sunny}|\text{Rainy}) = 0.3$, etc.
- Emissions: on a Rainy day, Walk with prob 0.1, Shop 0.4, Clean 0.5.

**Applications**: speech recognition, POS tagging, biological sequence modelling (DNA/protein), activity recognition, NLP.

## Worked example sketch
Given $\lambda = (A, B, \pi)$ and $O = (\text{Walk}, \text{Shop}, \text{Clean})$:
- Forward algorithm computes $P(O|\lambda) = 0.0336$ (see [[supp-hmm-forward-viterbi]]).
- Viterbi finds most likely sequence $= (\text{Sunny}, \text{Rainy}, \text{Rainy})$.

## Connections
- Generalises [[mcmc]] Markov chains to include hidden states.
- [[variational-autoencoder]] is also a latent variable model but for non-sequential data.
- Baum–Welch algorithm is a special case of the EM algorithm.

## Exam notes
- Forward and Viterbi algorithms: ⚠️ **examinable** (numerical questions).
- Matrix notation ($A, B, \pi$) must be known. ⚠️
- Baum–Welch: NOT examinable.
- Past exam: identify matrices from a diagram; enumerate state sequences.
- No formulas given. ⚠️ Algorithm steps must be memorised.
- **Common pitfall**: Forward uses $\sum$ (total probability); Viterbi uses $\max$ (best path). Don't mix them up.
- Formula status: algorithm initialisation, recursion, termination steps must be known ⚠️
