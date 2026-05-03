# Mutual Information

**Type:** principle
**Week:** 6
**Related:** [[entropy]], [[kl-divergence]], [[cross-entropy]], [[bayesian-inference]]
**Source:** [[lecture-w6]]

## Definition
Mutual information $I(X; Y)$ measures the amount of information shared between two random variables — equivalently, the reduction in uncertainty about $X$ given knowledge of $Y$.

## Motivation
Entropy measures uncertainty about one variable; mutual information measures how much two variables are related. It is the information-theoretic measure of dependence, generalising correlation to arbitrary (non-linear) relationships.

## How it works

### Definition
$$I(X;Y) = \sum_{x,y} p(x,y)\log\frac{p(x,y)}{p(x)p(y)} = D_{\text{KL}}(p(x,y) \| p(x)p(y))$$

For continuous variables:
$$I(X;Y) = \int\int p(x,y)\log\frac{p(x,y)}{p(x)p(y)}\,dx\,dy$$

### Relationship to Entropy
$$I(X;Y) = H(X) - H(X|Y) = H(Y) - H(Y|X) = H(X) + H(Y) - H(X,Y)$$

Where:
- $H(X)$: uncertainty about $X$ before observing $Y$.
- $H(X|Y)$: remaining uncertainty about $X$ after observing $Y$.
- $I(X;Y)$: reduction in uncertainty = information gained.

### Properties
- **Non-negative**: $I(X;Y) \geq 0$ (KL divergence is non-negative).
- **Zero iff independent**: $I(X;Y) = 0 \iff p(x,y) = p(x)p(y)$.
- **Symmetric**: $I(X;Y) = I(Y;X)$.
- **Upper bound**: $I(X;Y) \leq \min(H(X), H(Y))$.

### Conditional Entropy
$$H(X|Y) = -\sum_{x,y} p(x,y)\log p(x|y)$$
$$= \sum_y p(y) H(X|Y=y)$$
Average uncertainty about $X$ when $Y$ is known.

## Key derivation
$I(X;Y) = H(X) - H(X|Y)$:
$$H(X) - H(X|Y) = -\sum_x p(x)\log p(x) + \sum_{x,y}p(x,y)\log p(x|y)$$
Substituting $p(x|y) = p(x,y)/p(y)$ and rearranging gives the KL form.

## Parameters & intuition
- $I(X;Y) = 0$: $X$ and $Y$ carry no shared information (independent).
- $I(X;Y) = H(X)$: knowing $Y$ completely determines $X$ (maximum dependence).
- Measured in bits (log base 2) or nats (natural log).

## Connections
- [[entropy]]: MI = marginal entropy minus conditional entropy.
- [[kl-divergence]]: MI is the KL divergence between joint and product-of-marginals.
- [[cross-entropy]]: related via $H(p,q) = H(p) + D_{\text{KL}}(p\|q)$.

## Exam notes
- Know the definition and the entropy relation $I(X;Y) = H(X) - H(X|Y)$.
- Know that $I(X;Y) = 0$ iff $X \perp Y$.
- Conditional entropy definition: ⚠️ may be asked to compute from a joint table.
- Formula status: information theory formulas given ✅ (Week 6 is covered by formula sheet).
