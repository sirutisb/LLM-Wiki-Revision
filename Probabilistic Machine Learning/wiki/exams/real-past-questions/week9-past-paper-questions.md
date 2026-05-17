# Week 9 — Reinforcement Learning: Past Paper Questions

**Source papers:** COM3023 May 2023, 2024, 2025
**Topic coverage:** Q-learning, multi-armed bandits, MDP, ε-greedy, Bellman equation
**Formula sheet:** ⚠️ None provided — all equations must be recalled from memory

---

## COM3023 May 2023 — Question 4 (18 marks)

### Part (a) — 4 marks
What is the main difference between Reinforcement Learning and supervised/unsupervised learning? How does Q-learning generate data?

### Part (b) — 12 marks
Assume a system with four actions (a1, a2, a3, a4) and four states (s1, s2, s3, s4). The rewards and state transitions corresponding to actions at different time steps are provided below.

| Time step | Current state | Reward | Action | Transition state |
|-----------|--------------|--------|--------|-----------------|
| 1 | s3 | +5 | a1 | s3 → s2 |
| 2 | s2 | −5 | a2 | s2 → s3 |
| 3 | s3 | +8 | a1 | s3 → s2 |
| 4 | s2 | −10 | a3 | s2 → s1 |
| 5 | s1 | +3 | a4 | s1 → s2 |
| 6 | s2 | −8 | a3 | s2 → s1 |

Apply Q-learning to get the Q-values with **learning rate α = 0.6** and **discount factor γ = 0.4** for each step. Initialise all Q-table entries to zero. (2 marks for each correct step.)

**Q-learning update rule:**
$$Q_t(s,a) = Q_{t-1}(s,a) + \alpha \left[ r + \gamma \max_{a'} Q_{t-1}(s', a') - Q_{t-1}(s,a) \right]$$

### Part (c) — 2 marks
What is the aim of using the ε-greedy algorithm?

---

## COM3023 May 2024 — Question 5 (22 marks)

### Part (a) — 5 marks
Explain the meaning of the five key terms in reinforcement learning: **action**, **state**, **reward**, **policy**, and **value**.

### Part (b)(i) — 12 marks
Consider a k-armed bandit problem with **k = 3** actions denoted as x, y, z. A sequence of actions and rewards are given below:

| t | Action | Reward |
|---|--------|--------|
| 1 | x | 2 |
| 2 | x | 2 |
| 3 | z | 3 |
| 4 | y | 1 |
| 5 | x | 2 |
| 6 | z | 3 |

Given that the initial value estimates $Q_0(a) = 0$ for all actions, estimate $Q_t(a)$ for all actions using the **sample-average technique** and find the **optimal action** at each time step $t = 1, 2, 3, 4, 5, 6$.

**Sample-average update:**
$$\hat{Q}_t(a) = \frac{\text{total reward from action } a \text{ up to time } t}{\text{number of times } a \text{ was selected up to time } t}$$

### Part (b)(ii) — 5 marks
Was an ε-greedy action selection applied in the above problem? Explain your answer.

---

## COM3023 May 2025 — Question 5 (22 marks)

### Part (a) — 6 marks
Explain the concept of a **Markov Decision Process (MDP)**. How does it relate to reinforcement learning?

### Part (b)(i) — 10 marks
Consider an agent navigating a grid environment. The agent can take two actions (a1: move up, a2: move right). Below are the rewards and state transitions:

| Time Step | Current State | Reward | Action | Transition State |
|-----------|--------------|--------|--------|-----------------|
| 1 | s1 | +3 | a2 | s1 → s2 |
| 2 | s2 | +5 | a1 | s2 → s3 |
| 3 | s3 | −2 | a2 | s3 → s4 |
| 4 | s4 | +10 | a1 | s4 → s1 |

Q-learning parameters:
- Initial Q-values = 0 for all state-action pairs
- **Learning rate α = 0.8**
- **Discount factor γ = 0.9**

Using the Q-learning update rule, compute the Q-values for all state-action pairs after four time steps and draw the updated Q-table.

### Part (b)(ii) — 6 marks
The agent is tasked with identifying the optimal policy based on the Q-values from part (i). The policy selects the action with the highest Q-value for each state.

Explain **conceptually** (without recalculating) how reducing the discount factor from γ = 0.9 to γ = 0.5 would affect the agent's policy and decision-making focus.

---

## Pattern Analysis

| Paper | Marks | Conceptual part | Numerical part |
|-------|-------|----------------|----------------|
| 2023 (Q4) | 18 | RL vs supervised learning; Q-learning data generation; ε-greedy purpose | Q-learning table (α=0.6, γ=0.4, 6 steps) |
| 2024 (Q5) | 22 | 5 key RL terms | Multi-armed bandit sample-average + ε-greedy identification |
| 2025 (Q5) | 22 | MDP definition and relation to RL | Q-learning table (α=0.8, γ=0.9, 4 steps) + discount factor effect |

**Consistent exam pattern:**
1. One conceptual/definition question (~5–6 marks)
2. One numerical step-through calculation (~10–12 marks) — either Q-learning update table or bandit sample-average
3. One short explanatory question (~2–6 marks) — ε-greedy, exploration, or policy effects

**Must know from memory (no formula sheet):**
- Q-learning update rule: $Q_t(s,a) \leftarrow Q_{t-1}(s,a) + \alpha[r + \gamma\max_{a'}Q_{t-1}(s',a') - Q_{t-1}(s,a)]$
- Sample-average estimate: $\hat{Q}_t(a) = \frac{\sum r_i \text{ for action } a}{N_t(a)}$
- ε-greedy rule: exploit (greedy) with probability $1-\varepsilon$, explore (random) with probability $\varepsilon$
- Bellman optimality: $Q^*(s,a) = r(s,a) + \gamma\max_{a'}Q^*(s',a')$
