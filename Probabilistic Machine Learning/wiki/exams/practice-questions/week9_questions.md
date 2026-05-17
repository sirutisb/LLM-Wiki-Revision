# Week 9 Practice Questions — Reinforcement Learning

> **Scope:** Multi-armed bandits and Q-learning only. MDPs and the Bellman equation are background for Q-learning; prepare definitions and policy/Q-table interpretation, but not full Bellman derivations.
> ⚠️ **No formula sheet provided for Week 9. All update rules and algorithms must be recalled from memory.**

---

## Conceptual / Bookwork

### Q1 — Exploration vs Exploitation Trade-off [5 marks]
⚠️ *No formula given — conceptual recall required.*

Define the **exploration–exploitation trade-off** in the context of multi-armed bandits.

(a) Explain what it means for an agent to *exploit* its current knowledge. What is the risk of pure exploitation? [2]

(b) Explain what it means for an agent to *explore*. What is the risk of pure exploration? [2]

(c) Give one concrete real-world example (not from a casino) that illustrates this trade-off. [1]

---

### Q2 — $\varepsilon$-Greedy Strategy [5 marks]
⚠️ *No formula given — must recall action selection rule from memory.*

(a) Write down the $\varepsilon$-greedy action selection rule precisely, including the probability of each case. [2]

(b) Explain why the greedy algorithm (pure exploitation, $\varepsilon = 0$) is insufficient for learning the optimal arm in a multi-armed bandit. Illustrate your answer with reference to a 3-armed bandit where Arm 2 happens to give a reward of 1 on the very first pull. [2]

(c) How does the choice of $\varepsilon$ affect the long-run behaviour of the agent? Compare $\varepsilon = 0.01$ and $\varepsilon = 0.5$. [1]

---

### Q3 — Bandits vs Q-Learning [6 marks]
⚠️ *No formula given — must recall structural differences from memory.*

(a) State **two** key structural differences between the multi-armed bandit problem and Q-learning (as applied to an MDP). [2]

(b) In Q-learning, what do the terms *learning rate* $\alpha$ and *discount factor* $\gamma$ each control? What happens in the limiting cases $\alpha \to 0$, $\alpha = 1$, $\gamma = 0$, and $\gamma \to 1$? [3]

(c) Q-learning is described as *off-policy*. Briefly explain what this means in terms of the update rule. [1]

---

## Practical / Calculation

### Q4 — $\varepsilon$-Greedy Trace [8 marks]
⚠️ *No formula given — must recall sample-mean estimate and action selection rule from memory.*

A 3-armed bandit ($K = 3$) is run with $\varepsilon = 0.2$. The table below shows the first 8 steps. All initial estimates are $\hat{Q}_0(a) = 0$ for $a \in \{1, 2, 3\}$.

| $t$ | Selected action $a_t$ | Reward $r_t$ |
|-----|-----------------------|--------------|
| 1   | 2                     | 1            |
| 2   | 1                     | 0            |
| 3   | 2                     | 3            |
| 4   | 3                     | 0            |
| 5   | 2                     | 2            |
| 6   | 1                     | 0            |
| 7   | 2                     | 4            |
| 8   | 3                     | 1            |

The **sample-mean estimate** after $n$ selections of arm $a$ is:
$$\hat{Q}_t(a) = \frac{\text{sum of rewards from arm } a}{\text{number of times arm } a \text{ selected}}$$

(a) Compute $\hat{Q}_8(1)$, $\hat{Q}_8(2)$, and $\hat{Q}_8(3)$ after all 8 steps. [3]

(b) At step $t = 4$, the current estimated values are $\hat{Q}_3(1) = 0$, $\hat{Q}_3(2) = 2$, $\hat{Q}_3(3) = 0$. The agent selects arm 3. Is this consistent with $\varepsilon$-greedy? Explain whether this step was *definitely* an exploratory step. [2]

(c) Which arm would the greedy agent (with $\varepsilon = 0$) choose at step $t = 9$, based on the estimates from part (a)? [1]

(d) Write down the **incremental update rule** for the sample-mean estimate when arm $a$ is selected for the $n$-th time and yields reward $r$. This rule avoids storing all past rewards. [2]

---

### Q5 — Q-Learning Trace [10 marks]
⚠️ *No formula given — must recall the Q-learning update rule from memory.*

Consider a 3-state MDP with states $\{s_1, s_2, s_3\}$ and 2 actions $\{a_1, a_2\}$. The agent uses Q-learning with **learning rate $\alpha = 0.5$** and **discount factor $\gamma = 0.8$**.

All Q-values are initialised to zero: $Q(s, a) = 0$ for all $s, a$.

The agent executes the following trajectory (each row is one step):

| Step | State $s$ | Action $a$ | Reward $r$ | Next state $s'$ |
|------|-----------|-----------|-----------|----------------|
| 1    | $s_1$     | $a_1$     | $0$       | $s_2$           |
| 2    | $s_2$     | $a_1$     | $0$       | $s_3$           |
| 3    | $s_3$     | $a_2$     | $10$      | $s_3$ (terminal)|
| 4    | $s_1$     | $a_1$     | $0$       | $s_2$           |
| 5    | $s_2$     | $a_1$     | $0$       | $s_3$           |

Apply the update rule
$$Q(s,a) \leftarrow Q(s,a) + \alpha\!\left[r + \gamma \max_{a'} Q(s',a') - Q(s,a)\right]$$
after each step in order.

(a) Compute the Q-table after **Steps 1–3** (the first pass through the trajectory). Show your working for each update. [6]

(b) Compute the Q-table after **Steps 4–5** (the second pass). Show your working for each update. [4]

(c) After Step 5, which action would the agent take in state $s_2$ under the greedy policy? [1]

(d) Qualitatively: why does the value of $Q(s_1, a_1)$ remain zero even after Step 4, and what would cause it to become non-zero in a later episode? [2]

---

## Answers / Mark Schemes

---

### A1 — Exploration vs Exploitation Trade-off

**(a) Exploitation** [2]: The agent selects the action that currently has the highest estimated value — i.e., the action that appears best given its accumulated experience. The risk of pure exploitation is that early noisy observations may cause the agent to commit to a suboptimal action permanently, never discovering better alternatives.

**(b) Exploration** [2]: The agent deliberately tries actions that are not currently estimated to be the best, in order to gather more information about their true value. The risk of pure exploration is inefficiency: the agent wastes time (and reward) on suboptimal arms even after it has accumulated enough evidence to identify the best arm.

**(c) Example** [1]: Any one of the following (or equivalent) is acceptable:
- *Restaurant selection*: exploit = always go to your favourite restaurant; explore = try a new restaurant that might be better but could also disappoint.
- *Web advertising*: exploit = always show the advert with the highest known click rate; explore = show a new advert to estimate its click rate.
- *Oil drilling*: exploit = drill at the most promising known site; explore = test a new site that might contain more oil.

---

### A2 — $\varepsilon$-Greedy Strategy

**(a) Action selection rule** [2]:

$$a_t = \begin{cases} \arg\max_a \hat{Q}_t(a) & \text{with probability } 1 - \varepsilon \quad \text{(exploit)} \\ \text{uniformly random action} & \text{with probability } \varepsilon \quad \text{(explore)} \end{cases}$$

Both cases and probabilities must be stated for full marks.

**(b) Failure of pure greedy** [2]: If Arm 2 receives reward 1 on the first pull, its estimated value immediately becomes $\hat{Q}_1(2) = 1$, while Arm 1 and Arm 3 remain at 0. The greedy algorithm will select Arm 2 for every subsequent step. Even if Arm 1 or Arm 3 has a true mean reward of, say, 5, they are never selected, so their estimates never improve. The agent gets locked into a suboptimal choice due to lucky early sampling noise. (Award 1 mark for the general argument; 1 mark for illustrating how Arm 2's early reward causes lock-in.)

**(c) Effect of $\varepsilon$** [1]: 
- $\varepsilon = 0.01$: the agent explores only 1% of the time and largely exploits; converges quickly but risks missing better arms.
- $\varepsilon = 0.5$: the agent explores half the time; slower convergence and lower cumulative reward, but much less likely to get stuck on a suboptimal arm. A smaller $\varepsilon$ is typically preferable once estimates are reasonably accurate.

---

### A3 — Bandits vs Q-Learning

**(a) Two structural differences** [2]:

1. **State**: bandits have no state (stateless / single-context); Q-learning operates in an MDP with multiple distinct states $s \in S$ and state transitions.
2. **Sequential dependence**: in bandits, each action choice is independent (reward depends only on the chosen arm, not on any prior history of states); in Q-learning, actions change the state, so past actions influence future observations and rewards.

(Also acceptable: bandits learn $Q(a)$, Q-learning learns $Q(s,a)$; bandits have no transition dynamics to consider.)

**(b) $\alpha$ and $\gamma$** [3]:

- **$\alpha$ (learning rate)**: controls how much weight is given to the new TD target versus the old estimate. $\alpha \to 0$: the estimate is barely updated — extremely slow convergence. $\alpha = 1$: fully replace the old estimate with the new target — fast but noisy.
- **$\gamma$ (discount factor)**: controls how much future rewards are valued relative to immediate reward. $\gamma = 0$: only immediate reward matters — the agent is completely myopic. $\gamma \to 1$: future rewards count almost as much as immediate rewards — long-sighted but slower convergence and less numerically stable.

**(c) Off-policy** [1]: Q-learning is off-policy because the update uses $\max_{a'} Q(s', a')$ — the *best possible* action in the next state — regardless of which action the agent actually takes next. The policy used to collect data (e.g. $\varepsilon$-greedy) can differ from the policy being evaluated (greedy). This allows Q-learning to converge to the optimal policy even when exploring.

---

### A4 — $\varepsilon$-Greedy Trace

**(a) Estimated values after 8 steps** [3]:

Arm 1 was selected at $t = 2, 6$: total reward $= 0 + 0 = 0$, selected 2 times.
$$\hat{Q}_8(1) = \frac{0}{2} = 0$$

Arm 2 was selected at $t = 1, 3, 5, 7$: total reward $= 1 + 3 + 2 + 4 = 10$, selected 4 times.
$$\hat{Q}_8(2) = \frac{10}{4} = 2.5$$

Arm 3 was selected at $t = 4, 8$: total reward $= 0 + 1 = 1$, selected 2 times.
$$\hat{Q}_8(3) = \frac{1}{2} = 0.5$$

**(b) Step $t = 4$ — was it an exploratory step?** [2]:

At the start of step 4, the estimates are $\hat{Q}_3(1) = 0$, $\hat{Q}_3(2) = 2$, $\hat{Q}_3(3) = 0$. The greedy action is Arm 2 (highest estimate = 2). The agent selected Arm 3, which is not the greedy action. Therefore this step was *definitely* an exploratory step — the agent must have been in the explore branch of $\varepsilon$-greedy (the $\varepsilon$ event occurred). (Award 1 mark for identifying greedy = Arm 2; 1 mark for concluding this was definitely exploration.)

**(c) Greedy choice at $t = 9$** [1]:

$\hat{Q}_8(2) = 2.5$ is the highest estimate. The greedy agent selects **Arm 2**.

**(d) Incremental update rule** [2]:

Let $n$ be the number of times arm $a$ has been selected after the current pull. Then:

$$\hat{Q}_{\text{new}}(a) = \hat{Q}_{\text{old}}(a) + \frac{1}{n}\!\left(r - \hat{Q}_{\text{old}}(a)\right)$$

This is equivalent to the sample mean but requires storing only the current estimate and the count $n$, not all past rewards. The term $(r - \hat{Q}_{\text{old}}(a))$ is the **prediction error** (analogous to the TD error in Q-learning).

---

### A5 — Q-Learning Trace

**Q-learning update rule** (must be recalled from memory):
$$Q(s,a) \leftarrow Q(s,a) + \alpha\!\left[r + \gamma \max_{a'} Q(s',a') - Q(s,a)\right]$$

Parameters: $\alpha = 0.5$, $\gamma = 0.8$.

**Initial Q-table** (all zeros):

|       | $a_1$ | $a_2$ |
|-------|-------|-------|
| $s_1$ | 0     | 0     |
| $s_2$ | 0     | 0     |
| $s_3$ | 0     | 0     |

---

**(a) Steps 1–3** [6]:

**Step 1:** $(s = s_1,\ a = a_1,\ r = 0,\ s' = s_2)$

$$\max_{a'} Q(s_2, a') = \max(0, 0) = 0$$

$$Q(s_1, a_1) \leftarrow 0 + 0.5\left[0 + 0.8 \times 0 - 0\right] = 0$$

Q-table unchanged. (Award mark for showing the working even though the result is 0.)

---

**Step 2:** $(s = s_2,\ a = a_1,\ r = 0,\ s' = s_3)$

$$\max_{a'} Q(s_3, a') = \max(0, 0) = 0$$

$$Q(s_2, a_1) \leftarrow 0 + 0.5\left[0 + 0.8 \times 0 - 0\right] = 0$$

Q-table unchanged.

---

**Step 3:** $(s = s_3,\ a = a_2,\ r = 10,\ s' = s_3\ \text{terminal})$

At a terminal state, future reward is 0, so $\max_{a'} Q(s_3, a') = 0$.

$$Q(s_3, a_2) \leftarrow 0 + 0.5\left[10 + 0.8 \times 0 - 0\right] = 0.5 \times 10 = \mathbf{5}$$

**Q-table after Step 3:**

|       | $a_1$ | $a_2$ |
|-------|-------|-------|
| $s_1$ | 0     | 0     |
| $s_2$ | 0     | 0     |
| $s_3$ | 0     | **5** |

---

**(b) Steps 4–5** [4]:

**Step 4:** $(s = s_1,\ a = a_1,\ r = 0,\ s' = s_2)$

$$\max_{a'} Q(s_2, a') = \max(Q(s_2, a_1), Q(s_2, a_2)) = \max(0, 0) = 0$$

$$Q(s_1, a_1) \leftarrow 0 + 0.5\left[0 + 0.8 \times 0 - 0\right] = 0$$

Q-table unchanged.

---

**Step 5:** $(s = s_2,\ a = a_1,\ r = 0,\ s' = s_3)$

$$\max_{a'} Q(s_3, a') = \max(Q(s_3, a_1), Q(s_3, a_2)) = \max(0, 5) = 5$$

$$Q(s_2, a_1) \leftarrow 0 + 0.5\left[0 + 0.8 \times 5 - 0\right] = 0.5 \times 4 = \mathbf{2}$$

**Q-table after Step 5:**

|       | $a_1$  | $a_2$ |
|-------|--------|-------|
| $s_1$ | 0      | 0     |
| $s_2$ | **2**  | 0     |
| $s_3$ | 0      | 5     |

---

**(c) Greedy policy at $s_2$ after Step 5** [1]:

$Q(s_2, a_1) = 2 > Q(s_2, a_2) = 0$. The greedy agent selects **$a_1$** in state $s_2$.

---

**(d) Why $Q(s_1, a_1)$ stays zero — qualitative explanation** [2]:

After Step 4, $Q(s_1, a_1)$ is updated using the Bellman target $r + \gamma \max_{a'} Q(s_2, a')$. At that point $Q(s_2, a') = 0$ for all $a'$, so the target is $0 + 0 = 0$ — there is no signal to propagate back to $s_1$.

In Step 5, $Q(s_2, a_1)$ is updated to 2. Once this non-zero value exists, the *next* time the agent visits $s_1$ and takes $a_1$ (reaching $s_2$), the target becomes $0 + 0.8 \times 2 = 1.6 > 0$, and $Q(s_1, a_1)$ will receive a positive update. This illustrates how Q-learning propagates value information **backwards** through the state space over multiple episodes.

---

## Similar Past-Paper Style Addition

### Q6. MDPs, policy extraction, and the discount factor [12 marks]

**(a)** Define a Markov Decision Process (MDP) and explain how it relates to reinforcement learning. [4 marks]

**(b)** Given the following learned Q-table, write down the greedy policy $\pi(s)=\arg\max_a Q(s,a)$. [4 marks]

| State | $Q(s,a_1)$ | $Q(s,a_2)$ |
|---|---:|---:|
| $s_1$ | 1.2 | 3.0 |
| $s_2$ | 2.5 | 2.5 |
| $s_3$ | -1.0 | 0.0 |
| $s_4$ | 4.0 | 1.0 |

**(c)** Explain, without recalculating any Q-values, how reducing the discount factor $\gamma$ from $0.9$ to $0.5$ changes the agent's decision-making focus. [4 marks]

### A6. Mark scheme

**(a)** An MDP is a formal model for sequential decision-making, usually specified by states, actions, transition probabilities, rewards, and a discount factor. The Markov property means the next state depends on the current state and action, not the full history. Reinforcement learning learns good actions or policies in an MDP when the transition/reward model is unknown or learned from interaction.

**(b)** Greedy policy:

- $\pi(s_1)=a_2$ because $3.0>1.2$.
- $\pi(s_2)=a_1$ or $a_2$; the values tie, so either action is greedy unless a tie-breaking rule is specified.
- $\pi(s_3)=a_2$ because $0.0>-1.0$.
- $\pi(s_4)=a_1$ because $4.0>1.0$.

**(c)** A smaller $\gamma$ makes the agent care less about future rewards and more about immediate reward. With $\gamma=0.9$, rewards several steps ahead can strongly influence current Q-values. With $\gamma=0.5$, future value is discounted more aggressively, so the policy becomes more short-sighted and may prefer actions with quicker payoffs even if they lead to worse long-term returns.
