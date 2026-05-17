# Week 9 Revision Plan - Reinforcement Learning

**Scope:** [[reinforcement-learning]], [[multi-armed-bandits]], [[q-learning]]
**Source:** [[lecture-w9]], [[lecture-w10]], [[week9_questions]]
**Formula status:** No formula sheet for Week 9. Know the bandit estimates, epsilon-greedy rule, TD error, and Q-learning update from memory.
**Confirmed exam item:** Q-learning update rule 🔒 — lecturer stated at [43:14] (Week 9 recording): *"that is often to be assessed in the final exam."* See [[likely-questions]] for the full guaranteed section.

Week 9 is lower priority than Weeks 1-4 and 7, but it is a compact topic and can be made exam-ready quickly. The likely questions are practical traces: update a bandit estimate table, identify exploration steps, or update a Q-table over a short trajectory.

---

## What To Know Cold

### Core definitions
- [ ] Reinforcement learning: an agent interacts with an environment, receives rewards, and learns a policy to maximise cumulative return.
- [ ] Agent, environment, state $s$, action $a$, reward $r$, policy $\pi$, value / action-value.
- [ ] Exploration: try uncertain or non-greedy actions to learn.
- [ ] Exploitation: choose the action currently believed to be best.
- [ ] Multi-armed bandit: stateless action selection; no transitions; only action-reward pairs.
- [ ] Q-learning: stateful, sequential, model-free, off-policy TD learning.

### Bandits
- [ ] True action value: $Q(a) = \mathbb{E}[r|a]$.
- [ ] Sample-average estimate:
$$
\hat{Q}(a) = \frac{\text{sum of rewards from arm }a}{\text{number of times arm }a\text{ selected}}.
$$
- [ ] Incremental sample-mean update, where $n$ is the count after the new pull:
$$
\hat{Q}_{\text{new}}(a)
=
\hat{Q}_{\text{old}}(a)
+ \frac{1}{n}\left(r - \hat{Q}_{\text{old}}(a)\right).
$$
- [ ] Greedy rule: choose $\arg\max_a \hat{Q}(a)$.
- [ ] Epsilon-greedy rule:
$$
a_t =
\begin{cases}
\arg\max_a \hat{Q}_t(a), & \text{with probability } 1-\varepsilon,\\
\text{a uniformly random action}, & \text{with probability } \varepsilon.
\end{cases}
$$
- [ ] If the selected action is not greedy, the step was definitely exploration.
- [ ] If the selected action is greedy, it could be exploitation or exploration, because the random exploration branch can also choose the greedy arm.

### Q-learning
- [ ] Q-table entry: $Q(s,a)$ estimates long-run discounted return from taking action $a$ in state $s$.
- [ ] TD target:
$$
r + \gamma \max_{a'} Q(s',a').
$$
- [ ] TD error:
$$
\delta = r + \gamma \max_{a'} Q(s',a') - Q(s,a).
$$
- [ ] Q-learning update:
$$
Q(s,a) \leftarrow Q(s,a) + \alpha\left[r + \gamma \max_{a'} Q(s',a') - Q(s,a)\right].
$$
- [ ] $\alpha$: learning rate. Small means slow updates; $\alpha=1$ fully replaces the old value with the target.
- [ ] $\gamma$: discount factor. $\gamma=0$ only values immediate reward; $\gamma$ close to 1 values future rewards strongly.
- [ ] Terminal next state: future value is 0, so the target is just the immediate reward.
- [ ] Off-policy: the update uses $\max_{a'}Q(s',a')$, regardless of the action actually taken next.

---

## Revision Schedule

### Pass 1 - 35 minutes: memory setup
- [ ] Write the epsilon-greedy rule from memory.
- [ ] Write the sample-average estimate from memory.
- [ ] Write the incremental mean update from memory.
- [ ] Write the TD error and Q-learning update from memory.
- [ ] Explain, without equations, why greedy bandits can get stuck.
- [ ] Explain, without equations, why Q-learning propagates reward backwards over repeated episodes.

### Pass 2 - 45 minutes: bandit mechanics
- [ ] Do [[week9_questions]] Q1 and Q2 verbally.
- [ ] Do [[week9_questions]] Q4 in full, including part (d).
- [ ] For every selected action in a trace, label it as definitely exploration, could be exploration or exploitation, or inconsistent with the stated rule.
- [ ] Recompute each arm estimate using both total/count and incremental update.

### Pass 3 - 60 minutes: Q-learning mechanics
- [ ] Do [[week9_questions]] Q3.
- [ ] Do [[week9_questions]] Q5 in full.
- [ ] For each transition, write: old value, next-state maximum, target, TD error, new value.
- [ ] Pay special attention to terminal states and delayed reward propagation.

### Final 15-minute check
- [ ] From a blank page, reproduce all four essential formulas.
- [ ] Explain bandits vs Q-learning in two differences.
- [ ] Explain $\alpha$, $\gamma$, and off-policy learning.
- [ ] Solve one two-step Q-learning update without looking at notes.

---

## Worked Example 1 - Bandit Trace

### Question

A 3-armed bandit uses $\varepsilon = 0.1$. Initial estimates are all zero. The following actions and rewards are observed:

| Step | Action | Reward |
|------|--------|--------|
| 1 | 1 | 2 |
| 2 | 2 | 0 |
| 3 | 1 | 4 |
| 4 | 3 | 5 |
| 5 | 3 | 1 |
| 6 | 2 | 3 |

1. Compute $\hat{Q}_6(1)$, $\hat{Q}_6(2)$, and $\hat{Q}_6(3)$.
2. At the start of step 4, the estimates are $\hat{Q}_3(1)=3$, $\hat{Q}_3(2)=0$, $\hat{Q}_3(3)=0$. The agent selects arm 3. Was this definitely exploration?
3. Which arm would a greedy agent choose at step 7?
4. Update arm 2 incrementally at step 6, given that before step 6 it had been selected once with estimate $0$.

### Solution

Arm 1 was selected at steps 1 and 3:
$$
\hat{Q}_6(1)=\frac{2+4}{2}=3.
$$

Arm 2 was selected at steps 2 and 6:
$$
\hat{Q}_6(2)=\frac{0+3}{2}=1.5.
$$

Arm 3 was selected at steps 4 and 5:
$$
\hat{Q}_6(3)=\frac{5+1}{2}=3.
$$

At the start of step 4, the greedy arm is arm 1 because $\hat{Q}_3(1)=3$ is largest. The agent selected arm 3, which is not greedy, so this was definitely exploration.

At step 7, arm 1 and arm 3 are tied with estimate 3. A greedy agent chooses one of the tied best arms, depending on the tie-breaking rule.

For the incremental update of arm 2 at step 6, the old estimate is $0$, the new reward is $3$, and the new count is $n=2$:
$$
\hat{Q}_{\text{new}}(2)
=
0 + \frac{1}{2}(3-0)
= 1.5.
$$

---

## Worked Example 2 - Q-Learning Trace

### Question

An agent has states $\{s_1,s_2\}$ and actions $\{a_1,a_2\}$. It uses Q-learning with $\alpha=0.5$ and $\gamma=0.9$. All Q-values start at zero.

Apply the update rule over the following transitions:

| Step | State | Action | Reward | Next state |
|------|-------|--------|--------|------------|
| 1 | $s_1$ | $a_1$ | 0 | $s_2$ |
| 2 | $s_2$ | $a_2$ | 4 | terminal |
| 3 | $s_1$ | $a_1$ | 0 | $s_2$ |

Compute the Q-table after each step.

### Solution

Initial table:

|       | $a_1$ | $a_2$ |
|-------|-------|-------|
| $s_1$ | 0 | 0 |
| $s_2$ | 0 | 0 |

Step 1: $(s_1,a_1,0,s_2)$.

The next-state maximum is:
$$
\max_{a'}Q(s_2,a')=\max(0,0)=0.
$$

Target:
$$
0 + 0.9 \times 0 = 0.
$$

Update:
$$
Q(s_1,a_1) \leftarrow 0 + 0.5(0-0)=0.
$$

Step 2: $(s_2,a_2,4,\text{terminal})$.

Because the next state is terminal, the future value is 0. Target:
$$
4 + 0 = 4.
$$

Update:
$$
Q(s_2,a_2) \leftarrow 0 + 0.5(4-0)=2.
$$

Table after step 2:

|       | $a_1$ | $a_2$ |
|-------|-------|-------|
| $s_1$ | 0 | 0 |
| $s_2$ | 0 | 2 |

Step 3: $(s_1,a_1,0,s_2)$.

Now the next-state maximum has changed:
$$
\max_{a'}Q(s_2,a')=\max(0,2)=2.
$$

Target:
$$
0 + 0.9 \times 2 = 1.8.
$$

Update:
$$
Q(s_1,a_1) \leftarrow 0 + 0.5(1.8-0)=0.9.
$$

Final table:

|       | $a_1$ | $a_2$ |
|-------|-------|-------|
| $s_1$ | 0.9 | 0 |
| $s_2$ | 0 | 2 |

This shows delayed reward propagation: $s_1,a_1$ only becomes valuable after $s_2,a_2$ has first received a positive value.

---

## Worked Example 3 - Conceptual Mini Answer

### Question

Explain two differences between a multi-armed bandit and Q-learning.

### Model answer

First, a multi-armed bandit is stateless: the agent repeatedly chooses among arms and receives rewards, but there is no changing state. Q-learning operates in an MDP, so the value of an action depends on the current state.

Second, bandit actions do not affect future situations; they only produce immediate rewards. In Q-learning, actions can move the agent into different future states, so the value of an action includes immediate reward plus discounted future value.

Strong answers may also say that bandits estimate $\hat{Q}(a)$, whereas Q-learning estimates $Q(s,a)$.

---

## Extra Practice To Work On

### Drill A - Bandit estimates

Use $\varepsilon=0.2$ and initial estimates $0$.

| Step | Action | Reward |
|------|--------|--------|
| 1 | 2 | 2 |
| 2 | 2 | 4 |
| 3 | 1 | 1 |
| 4 | 3 | 6 |
| 5 | 2 | 0 |
| 6 | 3 | 3 |
| 7 | 1 | 5 |

Tasks:
- [ ] Compute final estimates for all arms.
- [ ] Identify the greedy arm at the start of each step from step 2 onward.
- [ ] Identify which selected actions were definitely exploratory.
- [ ] Write the incremental update for arm 3 at step 6.

### Drill B - Q-learning trace

Use $\alpha=0.4$, $\gamma=0.5$, all initial Q-values zero.

| Step | State | Action | Reward | Next state |
|------|-------|--------|--------|------------|
| 1 | $s_2$ | $a_1$ | 5 | terminal |
| 2 | $s_1$ | $a_2$ | 0 | $s_2$ |
| 3 | $s_2$ | $a_1$ | 5 | terminal |
| 4 | $s_1$ | $a_2$ | 0 | $s_2$ |

Tasks:
- [ ] Compute the Q-table after every step.
- [ ] State the greedy action in $s_1$ after step 4.
- [ ] Explain why the value of $Q(s_1,a_2)$ changes only after $Q(s_2,a_1)$ becomes positive.

### Drill C - Parameters

Answer in one sentence each:
- [ ] What happens when $\varepsilon=0$?
- [ ] What happens when $\varepsilon$ is very large?
- [ ] What happens when $\alpha$ is close to 0?
- [ ] What happens when $\alpha=1$?
- [ ] What happens when $\gamma=0$?
- [ ] What happens when $\gamma$ is close to 1?

---

## Common Mistakes

- [ ] Forgetting that exploration can still randomly choose the greedy action.
- [ ] Treating bandits as stateful; bandits do not have transition dynamics.
- [ ] Updating every Q-table entry at each Q-learning step. Only update the visited $(s,a)$ entry.
- [ ] Using $Q(s',a)$ instead of $\max_{a'}Q(s',a')$ in Q-learning.
- [ ] Forgetting that terminal next states have future value 0.
- [ ] Mixing up $\alpha$ and $\gamma$: $\alpha$ controls update size; $\gamma$ controls future reward weighting.
- [ ] Saying Q-learning is on-policy. In this course, Q-learning is off-policy because the target uses a greedy next-state maximum.

---

## Exam-Style Completion Standard

You are Week 9-ready when you can:

- [ ] Reproduce the four essential formulas from memory.
- [ ] Complete a bandit trace without looking up the sample-average formula.
- [ ] Complete a Q-learning trace by writing old value, target, TD error, and new value at each step.
- [ ] Explain exploration vs exploitation with a fresh real-world example.
- [ ] Explain why Q-learning values can remain zero for one pass and become non-zero only in later passes.
- [ ] Similar past-paper calibration: extract a greedy policy from a Q-table and explain how changing $\gamma$ changes short-term versus long-term behaviour.
