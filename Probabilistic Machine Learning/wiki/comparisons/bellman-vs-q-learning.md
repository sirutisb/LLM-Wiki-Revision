# Bellman Equation vs Q-Learning

## Overview
The Bellman equation is a **theoretical condition** — a self-consistency constraint on what optimal Q-values must satisfy. Q-learning is an **algorithm** that uses the Bellman equation as its learning signal. Understanding the difference clarifies *why* the Q-learning update works.

---

## The Q-Function

Both share the same object: the **action-value function** $Q(s,a)$.

$$Q(s,a) = \mathbb{E}\left[\sum_{t=0}^{\infty} \gamma^t r_t \;\bigg|\; s_0=s,\, a_0=a,\, \text{then follow } \pi^*\right]$$

This is the expected total discounted reward from taking action $a$ in state $s$, then acting optimally forever after. Neither algorithm changes what $Q^*$ *is* — they differ in how we obtain it.

---

## The Equations Side-by-Side

| | **Bellman Equation** | **Q-Learning Update** |
|---|---|---|
| **Role** | Defines $Q^*$ implicitly | Incrementally estimates $Q^*$ |
| **Form** | $Q^*(s,a) = R(s,a) + \gamma\displaystyle\sum_{s'} P(s'\|s,a)\max_{a'} Q^*(s',a')$ | $Q(s,a) \leftarrow Q(s,a) + \alpha\!\left[r + \gamma\max_{a'} Q(s',a') - Q(s,a)\right]$ |
| **Requires $P$?** | Yes (expectation over $s'$) | No — uses the observed $s'$ directly |
| **When satisfied** | When $Q = Q^*$ everywhere | At convergence, the update becomes zero |
| **Nature** | Static equation | Iterative stochastic approximation |

---

## Intuition: From Equation to Algorithm

**The Bellman equation says:** if you already knew $Q^*$, the value of $(s,a)$ would equal the immediate reward plus the discounted best-case value of the next state. This is a fixed-point condition:

$$Q^*(s,a) = \mathcal{T} Q^*(s,a)$$

where $\mathcal{T}$ is the Bellman operator. Finding $Q^*$ = finding the fixed point.

**Q-learning says:** we don't know $Q^*$, so bootstrap. After seeing one real transition $(s, a, r, s')$, form a **Bellman target**:

$$\text{target} = r + \gamma \max_{a'} Q(s', a')$$

The **TD error** measures how wrong the current estimate is:

$$\text{TD error} = \underbrace{r + \gamma\max_{a'} Q(s',a')}_{\text{Bellman target}} - \underbrace{Q(s,a)}_{\text{current estimate}}$$

The update nudges $Q(s,a)$ by a fraction $\alpha$ of this error. If TD error $> 0$: the action was better than expected, so increase $Q(s,a)$. If $< 0$: decrease it.

**Key insight:** Q-learning replaces the expectation $\sum_{s'} P(s'|s,a)(\cdots)$ with a single sampled transition. This makes it **model-free** — no need to know $P$. The stochastic updates still converge to the true $Q^*$ (under mild conditions on $\alpha$).

---

## What "Off-Policy" Means

Q-learning is **off-policy**: the target always uses $\max_{a'} Q(s',a')$ — the greedy action — regardless of what action the agent *actually* took next. This is exactly the Bellman optimality condition, so Q-learning is directly chasing the optimal $Q^*$ even when the agent explores.

This contrasts with on-policy methods (e.g. SARSA) that use the action actually taken next.

---

## Convergence

At convergence ($Q \to Q^*$):
- Every Q-learning update has TD error $\approx 0$.
- The Bellman equation is satisfied: $Q^*(s,a) = r + \gamma\max_{a'} Q^*(s',a')$ for every observed transition.
- The optimal policy is then read off: $\pi^*(s) = \arg\max_a Q^*(s,a)$.

---

## Comparison Table

| Dimension | Bellman Equation | Q-Learning |
|-----------|-----------------|------------|
| Type | Theoretical fixed-point equation | Model-free RL algorithm |
| Inputs | $R$, $P$, $\gamma$ | Observed transitions $(s,a,r,s')$, $\alpha$, $\gamma$ |
| Requires model? | Yes | No |
| Output | $Q^*$ (exact, if solved) | Approximate $Q^*$ (iterative) |
| How used | Defines what we want | Drives the update rule |
| Analogy | The *target* | The *gradient step* toward the target |

---

## Exam Notes
- The Bellman equation for $Q^*$ and the Q-learning update rule must both be known from memory: ⚠️ **no formulas given**.
- Be able to state: "Q-learning converges to $Q^*$, the solution to the Bellman optimality equation."
- In a numerical question: apply the update rule step by step — the Bellman equation is not used directly, only its single-sample approximation (the target $r + \gamma\max_{a'}Q(s',a')$).
- Do not confuse the Bellman equation (exact, with $\sum_{s'} P(\cdot)$) with the Q-learning target (sampled, no $P$ needed).
