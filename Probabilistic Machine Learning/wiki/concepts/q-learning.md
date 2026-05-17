# Q-Learning

**Type:** algorithm
**Week:** 9
**Related:** [[reinforcement-learning]], [[markov-decision-process]], [[bellman-equation]], [[multi-armed-bandits]]
**Source:** [[lecture-w9]], [[lecture-w10]]

## Definition
Q-learning is a model-free, off-policy temporal difference (TD) algorithm that learns the optimal action-value function $Q^*(s,a)$ directly from experience, without requiring a model of the environment.

## Motivation
In an MDP, the agent does not know the transition probabilities or reward function. It must learn them from experience. Q-learning provides a principled way to update estimates of $Q(s,a)$ after each interaction, converging to the optimal policy.

## How it works

### Q-Function (Action-Value Function)
$$Q(s,a) = \text{expected cumulative discounted reward from taking action } a \text{ in state } s \text{ and following the optimal policy thereafter}$$

**Bellman equation for Q**:
$$Q^*(s,a) = r(s,a) + \gamma\max_{a'} Q^*(s',a')$$
where $s'$ is the next state after taking action $a$ in state $s$.

**Optimal policy**: $\pi^*(s) = \arg\max_a Q^*(s,a)$.

### Temporal Difference (TD) Error
After observing transition $(s, a, r, s')$:
$$\text{TD}(s,a) = \underbrace{r(s,a) + \gamma\max_{a'} Q(s',a')}_{\text{target}} - \underbrace{Q(s,a)}_{\text{current estimate}}$$
- TD $> 0$: action was better than expected → increase $Q(s,a)$.
- TD $< 0$: action was worse than expected → decrease $Q(s,a)$.

### Q-Learning Update Rule
$$Q_t(s,a) = Q_{t-1}(s,a) + \alpha \cdot \text{TD}(s,a)$$
$$Q_t(s,a) = Q_{t-1}(s,a) + \alpha\left[r(s,a) + \gamma\max_{a'} Q_{t-1}(s',a') - Q_{t-1}(s,a)\right]$$

**Parameters**:
- $\alpha \in (0,1]$: learning rate (how fast Q-values are updated).
- $\gamma \in [0,1)$: discount factor (how much future rewards matter).

### Algorithm
1. Initialise Q-table: $Q(s,a) = 0$ for all $s, a$.
2. Observe current state $s$.
3. Choose action $a$ (e.g. $\varepsilon$-greedy).
4. Execute $a$, observe reward $r$ and next state $s'$.
5. Update: $Q(s,a) \leftarrow Q(s,a) + \alpha[r + \gamma\max_{a'} Q(s',a') - Q(s,a)]$.
6. Repeat until convergence.

## Key derivation
Q-learning derives from the Bellman equation. The TD error measures how far the current Q-value is from satisfying the Bellman equation. Q-learning is "off-policy" — the update uses $\max_{a'} Q(s',a')$, not the action actually taken next.

## Parameters & intuition
- $\alpha = 1$: fully trust the new estimate.
- $\alpha \approx 0$: barely update (slow convergence).
- $\gamma = 0$: only immediate reward matters (myopic).
- $\gamma \approx 1$: far-future rewards matter equally (long-sighted).
- Large Q-table for many states/actions → DQN (deep Q-network) uses a neural net.

## Worked example sketch
*From [[lecture-w10]] past exam*: $\alpha = 0.6$, $\gamma = 0.4$.

Step 1 (transition $s_3 \to a_1$, $r=5$): $Q(s_3, a_1) = 0 + 0.6[5 + 0.4\times 0 - 0] = 3$.

Step 2 (transition $s_2 \to a_2$, $r=-5$, next state $s_3$):
$Q(s_2, a_2) = 0 + 0.6[-5 + 0.4\times 3 - 0] = 0.6\times(-5+1.2) = 0.6\times(-3.8) = -2.28$.

(Continue updating Q-table step by step.)

## Connections
- [[markov-decision-process]]: Q-learning solves MDPs without knowing $P$ or $R$.
- [[bellman-equation]]: Q-learning's target is derived from the Bellman equation.
- [[multi-armed-bandits]]: simpler RL problem (stateless); Q-learning extends to states.
- [[reinforcement-learning]]: Q-learning is the core value-based RL algorithm in this course.

## Exam notes
- **🔒 Confirmed by lecturer [43:14, Week 9]:** *"that is often to be assessed in the final exam"* — said directly while presenting the TD-error update rule. See [[likely-questions]] for the full section.
- Both forms of the update rule must be known from memory: compact ($Q_{t-1} + \alpha\cdot\text{TD}$) and expanded. ⚠️ No formula sheet.
- Expect a numerical Q-table trace: given $\alpha$, $\gamma$, initial Q-values (usually zero), and a short trajectory, update each $Q(s,a)$ step by step.
- Must state: TD error interpretation, parameter roles ($\alpha$, $\gamma$), off-policy property, terminal-state treatment (future value = 0).
- Common pitfall: using $Q(s',a_{\text{taken}})$ instead of $\max_{a'}Q(s',a')$ in the target.
