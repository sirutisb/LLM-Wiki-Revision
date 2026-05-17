# Week 9 — Reinforcement Learning

**File:** `raw/text/COM3031_2526_Week9.txt`
**Type:** lecture
**Week:** 9
**Concepts introduced:** [[reinforcement-learning]], [[multi-armed-bandits]], [[markov-decision-process]], [[q-learning]], [[bellman-equation]]

## Summary
Week 9 extends probabilistic ML to sequential decision-making under uncertainty. Reinforcement Learning (RL) is introduced: an agent learns by interacting with an environment, receiving rewards. The multi-armed bandit problem introduces exploration vs exploitation in a stateless setting. Markov Decision Processes (MDPs) formalise sequential decision-making with states. Q-learning is the core value-based algorithm for learning optimal policies without a model.

## Key content

### What Makes RL Different
- No supervisor: only a reward signal.
- Delayed feedback: actions may influence rewards much later.
- Sequential decisions: not i.i.d. — past actions influence future states.
- Agent's behaviour changes the data it receives.

### Key RL Terminology
- **State** ($s$): current situation of the agent.
- **Action** ($a$): choices the agent can make.
- **Reward** ($r$): immediate feedback from environment.
- **Policy** ($\pi$): strategy mapping states to actions.
- **Value** ($V$): expected long-term return (discounted), as opposed to immediate reward.
- Interaction loop: $s_t \to a_t \to r_{t+1}, s_{t+1}$.

### Exploration vs Exploitation
- **Exploitation**: use what is currently known to maximise immediate reward.
- **Exploration**: try new actions to discover potentially better strategies.
- Only exploiting → miss better actions; only exploring → inefficient.

### Multi-Armed Bandits
- $K$ "arms" (actions), each yielding rewards from an unknown distribution.
- Action value: $Q(a) = \mathbb{E}[r|a]$ (expected reward).
- Optimal action: $a^* = \arg\max_a Q(a)$, optimal value $V^* = Q(a^*)$.
- Regret: $l_t = V^* - Q(a_t)$. Total regret: $L_T = \sum_{t=1}^T (V^* - Q(a_t))$.
- **Greedy**: always pick $\arg\max_a \hat{Q}(a)$; stops exploring too early.
- **$\varepsilon$-greedy**: with prob $1-\varepsilon$ exploit (greedy), with prob $\varepsilon$ explore (random action). Balances exploration and exploitation.
- Sample-average estimate: $\hat{Q}_t(a) = \frac{\text{sum of rewards from } a}{\text{number of times } a \text{ chosen}}$.

![[Pasted image 20260517140916.png]]

### Markov Decision Process (MDP)
- MDP defined by $(S, A, P, R, \gamma)$:
  - $S$: state space; $A$: action space.
  - $P(s'|s,a)$: transition probabilities.
  - $R(s,a)$: reward function.
  - $\gamma \in [0,1)$: discount factor.
- **Value function** under policy $\pi$:
$$V^\pi(s) = \mathbb{E}_\pi\left[\sum_{k=0}^\infty \gamma^k r_{t+k+1}\,\Big|\, s_t = s\right]$$
- $\gamma = 0$: only immediate reward matters; $\gamma \approx 1$: future rewards matter equally.

### Bellman Equation
$$V(s) = \max_a\left[r(s,a) + \gamma V(s')\right]$$
- Recursive relationship: value of a state = best immediate reward + discounted value of next state.
- Optimal policy: $\pi^* = \arg\max_\pi V^\pi(s)$.

### Q-function (Action-Value Function)
$$Q(s,a) = r(s,a) + \gamma\max_{a'} Q(s',a')$$
- Expected cumulative reward from taking action $a$ in state $s$ and then following the optimal policy.
- Optimal action: $\pi(s) = \arg\max_a Q(s,a)$.

### Temporal Difference (TD) Error
$$\text{TD}(s,a) = r(s,a) + \gamma\max_{a'} Q(s',a') - Q(s,a)$$
- Measures how much the Q-value should change.
- TD > 0: action was better than expected. TD < 0: worse than expected.

### Q-Learning Update
$$Q_t(s,a) = Q_{t-1}(s,a) + \alpha\cdot\text{TD}(s,a)$$
$$Q_t(s,a) = Q_{t-1}(s,a) + \alpha\left[r(s,a) + \gamma\max_{a'} Q(s',a') - Q_{t-1}(s,a)\right]$$
- $\alpha$: learning rate (controls update speed).
- Q-values converge to optimal $Q^*$ over many interactions.

## Key takeaways
- RL learns from sparse reward signals without labelled supervision.
- Multi-armed bandits: stateless exploration vs exploitation.
- $\varepsilon$-greedy is the simplest balance strategy.
- MDPs generalise bandits to state-dependent sequential decisions.
- Bellman equation: recursive value decomposition. Q-learning approximates it from experience.
- Q-table update formula must be known for numerical exam questions.

## Exam relevance
- Multi-armed bandits (ε-greedy): **examinable** (past worked example with Q-table updates).
- Q-learning update formula: **examinable** (calculate Q-values step by step).
- Bellman equation: conceptual understanding.
- Exploration vs exploitation: **examinable** conceptually.
- Derivations NOT examinable (Week 9).
- No formulas given; Q-learning update rule must be known from memory.

## Links to concepts
- [[reinforcement-learning]]: introduced here
- [[multi-armed-bandits]]: introduced here
- [[markov-decision-process]]: introduced here
- [[q-learning]]: introduced here
- [[bellman-equation]]: introduced here
- [[hidden-markov-model]]: previous sequential model ([[lecture-w8]])
