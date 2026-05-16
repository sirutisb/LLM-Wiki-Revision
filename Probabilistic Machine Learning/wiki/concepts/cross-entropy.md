# Cross-Entropy

**Type:** principle
**Week:** 6
**Related:** [[entropy]], [[kl-divergence]], [[mutual-information]], [[logistic-regression]], [[mle]]
**Source:** [[lecture-w6]]

## Definition
The cross-entropy $H(p, q)$ between distributions $p$ and $q$ is the expected number of bits needed to encode data from $p$ using a code optimised for $q$.

## Motivation
Cross-entropy appears in two contexts: (1) information theory — measuring the cost of using the wrong distribution $q$ to encode data from $p$; (2) machine learning — the standard loss function for classification, connecting MLE to information theory.

## How it works

### Cross-Entropy (Discrete)
$$H(p, q) = -\sum_x p(x)\log q(x) = \mathbb{E}_p[-\log q(x)]$$

### Decomposition
$$H(p, q) = H(p) + D_{\text{KL}}(p \| q)$$

Where:
- $H(p)$: entropy of $p$ (irreducible cost — minimum possible code length).
- $D_{\text{KL}}(p \| q)$: extra bits wasted by using $q$ instead of the optimal code for $p$.

So $H(p,q) \geq H(p)$, with equality iff $p = q$.

### Cross-Entropy Loss in ML
For binary classification with true labels $y_i \in \{0,1\}$ and predicted probabilities $\hat{p}_i$:
$$\mathcal{L} = -\frac{1}{n}\sum_{i=1}^n \left[y_i\log\hat{p}_i + (1-y_i)\log(1-\hat{p}_i)\right]$$

This is the **negative log-likelihood** of the Bernoulli model = cross-entropy between the empirical label distribution and the predicted probabilities.

### Connection to MLE
Minimising cross-entropy loss ≡ maximising log-likelihood ≡ minimising KL from empirical distribution to model:
$$\arg\min_q H(\hat{p}_{\text{data}}, q) = \arg\min_q D_{\text{KL}}(\hat{p}_{\text{data}} \| q) = \arg\max_q \sum_i \log q(x_i)$$

## Key derivation
✅ *Formula sheet provided*

$H(p,q) = H(p) + D_{\text{KL}}(p\|q)$:
$$H(p,q) = -\sum_x p(x)\log q(x) = -\sum_x p(x)\log p(x) + \sum_x p(x)\log\frac{p(x)}{q(x)} = H(p) + D_{\text{KL}}(p\|q)$$

## Parameters & intuition
- **"Wasted bits" intuition:** Cross-entropy literally asks, *"How many bits would I waste encoding reality using this model?"*
  - **Good model:** Suppose the truth is "cat". The model predicts cat ($0.99$). The surprise/cost is tiny: $-\log(0.99) \approx 0$.
  - **Bad model:** The truth is "cat", but the model predicts cat ($0.01$). The surprise/cost is huge: $-\log(0.01)$. 
  - The loss is just the information-theoretic penalty for allocating a long bit-code to an event that actually happens frequently in reality.
- $H(p,q)$ is not symmetric: $H(p,q) \neq H(q,p)$ in general.
- Good model $q \approx p$: KL $\approx 0$, cross-entropy $\approx H(p)$.
- Bad model: extra bits wasted proportional to KL.

## Connections
- [[entropy]]: $H(p,q) = H(p) + D_{\text{KL}}(p\|q)$.
- [[kl-divergence]]: cross-entropy = entropy + KL; minimising cross-entropy ≡ minimising forward KL.
- [[logistic-regression]]: trained by minimising binary cross-entropy = maximising Bernoulli log-likelihood.
- [[mle]]: MLE objective is equivalent to minimising cross-entropy.

## Exam notes
- Cross-entropy decomposition $H(p,q) = H(p) + D_{\text{KL}}$ derivation: **NOT examinable**.
- Connection between cross-entropy loss and MLE: conceptually examinable.
- Know: minimising CE loss = maximising likelihood.
- Formula status: information theory formulas given ✅ (Week 6 covered by formula sheet).
