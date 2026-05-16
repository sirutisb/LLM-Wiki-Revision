# Reinforcement Learning

**Type:** framework
**Week:** 9
**Related:** [[markov-decision-process]], [[q-learning]], [[multi-armed-bandits]], [[bellman-equation]]
**Source:** [[lecture-w9]], [[lecture-w10]]

## Definition
Reinforcement learning (RL) is a learning paradigm in which an agent learns to make decisions by interacting with an environment, receiving rewards, and maximising cumulative expected return.

## Motivation
Supervised learning requires labelled data; unsupervised learning finds structure without feedback. RL addresses a third setting: sequential decision-making where feedback (reward) is delayed and the agent must learn through trial and error.

## How it works

### Core Components
- **Agent**: the learner/decision-maker.
- **Environment**: everything external to the agent.
- **State** $s$: agent's current situation.
- **Action** $a$: choice made by the agent.
- **Reward** $r$: scalar feedback from the environment.
- **Policy** $\pi(a|s)$: agent's decision rule (probability of action given state).

### Interaction Loop
At each step $t$:
1. Agent observes state $s_t$.
2. Agent selects action $a_t \sim \pi(\cdot|s_t)$.
3. Environment transitions to $s_{t+1} \sim P(s'|s_t, a_t)$.
4. Agent receives reward $r_t = R(s_t, a_t)$.

### Goal
Maximise expected cumulative discounted reward:
$$G_t = \sum_{k=0}^\infty \gamma^k r_{t+k}, \qquad \gamma \in [0,1)$$

### RL Problem Hierarchy (Course Scope)
| Problem | State | Sequential? |
|---------|-------|------------|
| Multi-armed bandit | None (stateless) | No |
| MDP + Q-learning | Yes | Yes |

### Key Concepts
- **Exploration vs exploitation**: try new actions (learn) vs use best known action (earn).
- **Model-free vs model-based**: learn $Q$ from experience vs learn transition model $P$.
- **On-policy vs off-policy**: learn from policy being followed vs any policy (Q-learning is off-policy).

## Parameters & intuition
- $\gamma$ (discount factor): 0 = myopic; close to 1 = long-horizon planning.
- Policy: deterministic $\pi(s) = a$, or stochastic $\pi(a|s)$.
- The trade-off between exploration and exploitation is the central challenge.

## Connections
- [[multi-armed-bandits]]: simplest RL (stateless, single step).
- [[markov-decision-process]]: formalises the RL problem with states and transitions.
- [[q-learning]]: model-free algorithm for solving MDPs.
- [[bellman-equation]]: recursive relationship that Q-learning solves.

## Exam notes
- **Scope restriction:** Only multi-armed bandits and Q-learning are examinable.
- Derivations: Not examinable for Week 9.
- Know the RL framework components: state, action, reward, policy.
- Distinguish bandit (stateless) from MDP (stateful).
- Exploration vs exploitation: can be asked to define and give examples.
- Formula status: no formula sheet for Week 9 ⚠️
