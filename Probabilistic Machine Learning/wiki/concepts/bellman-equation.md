# Bellman Equation

**Type:** principle
**Week:** 9
**Related:** [[markov-decision-process]], [[q-learning]], [[reinforcement-learning]]
**Source:** [[lecture-w9]], [[lecture-w10]]

## Definition
The Bellman equation is a recursive relationship expressing the value of a state (or state-action pair) as the immediate reward plus the discounted value of the next state, under the optimal policy.

## Motivation
Solving for the optimal policy in an MDP requires knowing the value of every state. The Bellman equation turns this into a self-consistent system of equations — the value of each state is defined in terms of other states' values, enabling iterative solution.

## How it works

### Bellman Optimality Equation for $V^*$
$$V^*(s) = \max_a \left[R(s,a) + \gamma \sum_{s'} P(s'|s,a) V^*(s')\right]$$

### Bellman Optimality Equation for $Q^*$
$$Q^*(s,a) = R(s,a) + \gamma \sum_{s'} P(s'|s,a) \max_{a'} Q^*(s',a')$$

In model-free RL with deterministic transitions ($s' = T(s,a)$):
$$Q^*(s,a) = R(s,a) + \gamma \max_{a'} Q^*(s',a')$$

### Bellman Equation for Policy $\pi$ (not optimal)
$$Q^\pi(s,a) = R(s,a) + \gamma \sum_{s'} P(s'|s,a) Q^\pi(s', \pi(s'))$$

### Q-Learning Connection
Q-learning estimates $Q^*(s,a)$ by minimising the **Temporal Difference (TD) error**:
$$\text{TD}(s,a) = \underbrace{R(s,a) + \gamma\max_{a'} Q(s',a')}_{\text{Bellman target}} - Q(s,a)$$
At convergence: TD error → 0, and $Q \to Q^*$ (satisfies Bellman equation).

## Key derivation
⚠️ *No formula given in exam*

From the definition of $V^*(s) = \max_\pi \mathbb{E}_\pi[G_t|s_t = s]$ and one-step lookahead:
$$V^*(s) = \max_a \mathbb{E}[r_t + \gamma V^*(s_{t+1}) | s_t = s, a_t = a]$$
$$= \max_a \left[R(s,a) + \gamma \sum_{s'} P(s'|s,a)V^*(s')\right]$$

## Parameters & intuition
- $\gamma$: trades off immediate vs future rewards; $\gamma = 0$ → $V^*(s) = \max_a R(s,a)$.
- $P(s'|s,a)$: if known (model-based), can solve Bellman equations exactly via value iteration.
- Q-learning does not need $P$ — uses observed transitions to estimate the expectation.

## Connections
- [[markov-decision-process]]: Bellman equation is the optimality condition for MDPs.
- [[q-learning]]: uses Bellman equation as the TD learning target.
- [[reinforcement-learning]]: Bellman equation is the theoretical foundation of value-based RL.

## Exam notes
- Know the Bellman equation for $Q^*$: ⚠️ **examinable** (within the context of Q-learning).
- Derivations for Week 9 are **not examinable**.
- Understand what "TD error" measures (deviation from Bellman condition).
- Can be asked: "What does Q-learning converge to?" → $Q^*$ satisfying the Bellman equation.
- Formula status: ⚠️ *No formula given in exam*; Bellman equation must be known from memory.
