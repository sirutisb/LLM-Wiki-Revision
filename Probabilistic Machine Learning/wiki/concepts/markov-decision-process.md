# Markov Decision Process (MDP)

**Type:** framework
**Week:** 9
**Related:** [[reinforcement-learning]], [[q-learning]], [[bellman-equation]], [[multi-armed-bandits]]
**Source:** [[lecture-w9]], [[lecture-w10]]

## Definition
A Markov Decision Process (MDP) is a mathematical framework for sequential decision-making under uncertainty, defined by a tuple $(\mathcal{S}, \mathcal{A}, P, R, \gamma)$.

## Motivation
Bandits have no state — but real problems have sequential dependencies (e.g. chess, robot navigation, game playing). MDPs formalise this: the agent's current state determines which actions are available and what future states are reachable.

## How it works

### MDP Tuple
- $\mathcal{S}$: state space.
- $\mathcal{A}$: action space.
- $P(s'|s, a)$: transition probability — probability of reaching $s'$ from $s$ after action $a$.
- $R(s, a)$: reward function — expected reward for taking action $a$ in state $s$.
- $\gamma \in [0,1)$: discount factor.

### Markov Property
$$P(s_{t+1}|s_t, a_t, s_{t-1}, a_{t-1}, \ldots) = P(s_{t+1}|s_t, a_t)$$
The future depends only on the current state and action, not the history.

### Value Functions
**State-value function** (under policy $\pi$):
$$V^\pi(s) = \mathbb{E}_\pi\left[\sum_{k=0}^\infty \gamma^k r_{t+k} \,\Big|\, s_t = s\right]$$

**Action-value function** (Q-function):
$$Q^\pi(s,a) = \mathbb{E}_\pi\left[\sum_{k=0}^\infty \gamma^k r_{t+k} \,\Big|\, s_t = s, a_t = a\right]$$

### Optimal Policy
$$\pi^*(s) = \arg\max_a Q^*(s,a)$$
The optimal policy takes the greedy action with respect to $Q^*$.

### Bellman Optimality Equations
$$V^*(s) = \max_a \left[R(s,a) + \gamma \sum_{s'} P(s'|s,a)V^*(s')\right]$$
$$Q^*(s,a) = R(s,a) + \gamma \sum_{s'} P(s'|s,a)\max_{a'} Q^*(s',a')$$

## Key derivation
The Bellman equation follows from the definition of $V^*$: the optimal value of state $s$ equals the best immediate reward plus the discounted optimal value of the next state.

## Parameters & intuition
- $\gamma$ close to 1: long-term planning; close to 0: myopic.
- $P$ unknown in model-free RL → must estimate from data (Q-learning does this implicitly).
- Deterministic MDP: $P(s'|s,a) = 1$ for one $s'$ (transition is certain).

## Connections
- [[reinforcement-learning]]: MDP is the formal framework for RL.
- [[bellman-equation]]: the recursive optimality condition for MDPs.
- [[q-learning]]: solves the MDP without knowing $P$ or $R$ explicitly.
- [[multi-armed-bandits]]: special case with one state; no transitions.

## Exam notes
- MDP components: ⚠️ **examinable** (must name and explain $\mathcal{S}, \mathcal{A}, P, R, \gamma$).
- Know the Markov property.
- Bellman equation for $Q^*$: ⚠️ **examinable** (used in Q-learning).
- Formula status: no formula sheet for Week 9 ⚠️; must know Bellman equation.
