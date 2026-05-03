# Multi-Armed Bandits

**Type:** framework
**Week:** 9
**Related:** [[reinforcement-learning]], [[q-learning]], [[markov-decision-process]]
**Source:** [[lecture-w9]], [[lecture-w10]]

## Definition
The multi-armed bandit problem is a stateless reinforcement learning scenario where an agent repeatedly chooses among $K$ actions ("arms"), each yielding rewards from an unknown distribution, to maximise total reward.

## Motivation
Bandits isolate the **exploration vs exploitation** trade-off in its purest form — no state transitions, no sequential dependence. Understanding bandits provides the foundation for full MDPs and RL algorithms like Q-learning.

## How it works

### Setup
- $K$ arms; at each step $t$: choose action $a_t \in \{1,\ldots,K\}$, receive reward $r_t \sim \mathcal{R}_{a_t}$.
- **Action value**: $Q(a) = \mathbb{E}[r|a]$ (true expected reward, unknown).
- **Optimal action**: $a^* = \arg\max_a Q(a)$, optimal value $V^* = Q(a^*)$.
- **Sample-average estimate**: $\hat{Q}_t(a) = \frac{\text{total reward from }a}{\text{number of times }a\text{ chosen}}$.

### Regret
- Instantaneous regret: $l_t = V^* - Q(a_t)$ — reward lost by not choosing the best action.
- Total regret: $L_T = \sum_{t=1}^T (V^* - Q(a_t))$.
- Goal: maximise cumulative reward ≡ minimise total regret.

### Greedy Algorithm
$$a_t = \arg\max_a \hat{Q}_t(a)$$
- Exploits current best estimate.
- Problem: commits to a suboptimal arm if early samples are noisy; never explores.

### $\varepsilon$-Greedy Algorithm
$$a_t = \begin{cases}\arg\max_a \hat{Q}_t(a) & \text{with probability } 1-\varepsilon \\ \text{random action} & \text{with probability } \varepsilon\end{cases}$$
- $\varepsilon$: exploration probability (typically small, e.g. 0.1).
- Balances exploitation (most of the time) with exploration (occasionally).
- All arms are eventually tried → discovers better arms over time.

## Key derivation
No formal derivation — the key insight is the trade-off argument:
- Only exploiting: risk missing better arms if early estimates are noisy.
- Only exploring: wastes time on suboptimal arms even when we know the best.

## Parameters & intuition
- Small $\varepsilon$: mostly exploit; good when estimates are reliable.
- Large $\varepsilon$: mostly explore; good early on when all estimates are uncertain.
- As $t \to \infty$ with fixed $\varepsilon$: $\hat{Q}_t(a) \to Q(a)$ for all $a$ (law of large numbers).

## Worked example sketch
*3-armed bandit, $\varepsilon = 0.2$. At $t=1$: all estimates 0 → random choice.*

*See [[lecture-w10]] for the detailed step-by-step exam example:*
- Track estimated values $\hat{Q}_t$ for each action.
- At $\varepsilon$-greedy exploration steps: selected action ≠ greedy action.
- "At which time steps did $\varepsilon$ definitely occur?" — look for selected $\neq$ greedy action.

## Connections
- [[reinforcement-learning]]: bandits are the simplest RL problem (no states).
- [[markov-decision-process]]: generalises bandits by adding state transitions.
- [[q-learning]]: extends the bandit's action-value updates to state-dependent Q-values.

## Exam notes
- $\varepsilon$-greedy action selection: ⚠️ **examinable**.
- Sample-average estimate calculation: ⚠️ **examinable**.
- "At which time steps did $\varepsilon$-greedy definitely explore?" — past exam question. ⚠️
- Must know $\hat{Q}_t(a) = \text{sum of rewards}/\text{number of selections}$.
- No formulas given. ⚠️
- Formula status: definition must be known from memory ⚠️
