# Task 2 — Multi-Armed Bandits with $\epsilon$-Greedy

**Problem statement (workshop PDF, §2).** An agent must repeatedly choose between several slot machines (arms), each with an unknown reward distribution. Maximise total reward by balancing **exploration** and **exploitation**.

**Workshop instructions:**

1. Study the implementation of the Multi-Armed Bandit problem.
2. Understand how the $\epsilon$-greedy strategy balances exploration and exploitation.
3. Run the algorithm and observe how the estimated action values are updated over time.
4. Identify which arm is estimated to be the best after learning.
5. Briefly comment on the effect of $\epsilon$ on the learning behaviour.

**Concepts:** [[multi-armed-bandits]], [[reinforcement-learning]], [[lecture-w9]]

---

## What we're trying to do

A **multi-armed bandit (MAB)** is the simplest reinforcement-learning problem: there is a *single state* (the casino) and $K$ actions (pulling arm $a \in \{1,\dots,K\}$). Each arm $a$ pays a stochastic reward drawn from an unknown distribution with mean $\mu_a$. The agent's job is to maximise the cumulative reward
$$
\sum_{t=1}^{T} r_t
$$
without knowing the $\mu_a$ in advance. Equivalently, minimise **regret**
$$
\text{Regret}(T) = T \mu^* - \mathbb{E}\!\left[\sum_{t=1}^{T} r_t\right], \qquad \mu^* = \max_a \mu_a.
$$
This is a *stateless* RL problem — there is no $s'$, no transition, no $\gamma$. All the difficulty lies in the **exploration–exploitation trade-off**:

- **Exploit:** pull the arm that *currently looks best* — but maybe your estimate is wrong because you've barely tried the others.
- **Explore:** try other arms to refine estimates — but every exploration step is one less exploit step, so you pay a regret cost.

$\epsilon$-greedy is the simplest possible compromise: explore with small probability $\epsilon$, otherwise exploit.

### Estimating action values: the sample-average update

After pulling arm $a$ a total of $N_t(a)$ times and getting rewards $r_1, \dots, r_{N_t(a)}$, the natural estimate is
$$
Q_t(a) = \frac{1}{N_t(a)}\sum_{i=1}^{N_t(a)} r_i.
$$
Storing all the rewards is wasteful; the same average can be maintained **incrementally** as
$$
Q_{n}(a) \;\leftarrow\; Q_{n-1}(a) + \frac{1}{n}\bigl[r_n - Q_{n-1}(a)\bigr].
$$
*Algebra check.* The new average $(\sum_{i=1}^{n} r_i)/n$ equals the old average plus a correction:
$$
\frac{1}{n}\sum_{i=1}^n r_i = \frac{n-1}{n}\,Q_{n-1} + \frac{1}{n}\,r_n = Q_{n-1} + \frac{1}{n}(r_n - Q_{n-1}).
$$
Notice the structural similarity to the Q-learning update from Task 1: it's the same TD form
$$
Q \leftarrow Q + \alpha\bigl[\text{target} - Q\bigr]
$$
with target = $r$ (no bootstrapping because there's no next state) and $\alpha = 1/n$ (a *decreasing* step size, because we want the empirical average).

---

## Cell-by-cell walkthrough

### Cell 1 — `epsilon_greedy_bandit` function definition

```python
import numpy as np

def epsilon_greedy_bandit(true_probabilities, epsilon=0.1, trials=1000):
    num_machines = len(true_probabilities)
    estimated_rewards = np.zeros(num_machines)
    visit_counts     = np.zeros(num_machines)

    for t in range(trials):
        if np.random.rand() < epsilon:
            action = np.random.randint(num_machines)         # explore
        else:
            action = np.argmax(estimated_rewards)            # exploit

        reward = 1 if np.random.rand() < true_probabilities[action] else 0

        visit_counts[action] += 1
        estimated_rewards[action] += (reward - estimated_rewards[action]) / visit_counts[action]

    best_machine = np.argmax(estimated_rewards)
    return estimated_rewards, best_machine
```

Walking through what each piece does:

**Initialisation.**

- `estimated_rewards` is the table of $Q_t(a)$ — one estimate per arm, all starting at 0.
- `visit_counts` is $N_t(a)$ — how many times we've pulled each arm so far.

**The loop body — three things every step.**

1. **Action selection ($\epsilon$-greedy).**
   $$
   a_t = \begin{cases} \text{Uniform}(\{1,\dots,K\}) & \text{w.p. } \epsilon \\ \arg\max_a Q_t(a) & \text{w.p. } 1-\epsilon \end{cases}
   $$
   `np.random.rand() < epsilon` flips the explore/exploit coin; `np.argmax(estimated_rewards)` picks the currently-best-looking arm. Ties are broken by `np.argmax` taking the first index.

2. **Pull the arm and observe a reward.** Each arm is a Bernoulli machine: it pays 1 with probability `true_probabilities[action]` and 0 otherwise. `np.random.rand() < p` is a one-line Bernoulli sample.

3. **Incremental sample-average update** for the chosen arm:
   $$
   Q_{n}(a_t) \leftarrow Q_{n-1}(a_t) + \frac{1}{N_t(a_t)}\bigl[r_t - Q_{n-1}(a_t)\bigr].
   $$
   In code: `estimated_rewards[action] += (reward - estimated_rewards[action]) / visit_counts[action]`.

**Readout.** After `trials` iterations, the arm with the highest sample-mean estimate is reported as `best_machine = np.argmax(estimated_rewards)`.

### Cell 2 — Define the (hidden) bandit

```python
true_probabilities = [0.2, 0.5, 0.3, 0.7, 0.4]   # unknown to the agent
```

Five arms with these *true* win probabilities $\mu_a$. The agent does **not** see this list; it only sees rewards. Looking at it from outside, the optimal arm is index 3 ($\mu^* = 0.7$).

### Cell 3 — Run and inspect

```python
estimated_rewards, best_machine = epsilon_greedy_bandit(true_probabilities)
print("Estimated Rewards:", estimated_rewards)
print("Best Machine:", best_machine)
```

Sample output:

```
Estimated Rewards: [0.2  0.545  0.357  0.710  0.45]
Best Machine: 3
```

A few things worth noticing:

- The estimate for arm 3 ($\hat{Q}(3) \approx 0.71$) is very close to the truth ($\mu_3 = 0.7$), because exploitation visited it many times — the sample mean has low variance.
- The estimates for the *other* arms are noisier (e.g. $\hat{Q}(1) = 0.545$ for $\mu_1 = 0.5$), because $\epsilon = 0.1$ means roughly $0.1 \cdot 1000 / 5 = 20$ exploratory pulls per non-greedy arm — fewer samples, larger error.
- Because exploration only allocates ~20% of trials uniformly, most non-best arms get visited so few times that their estimates can deviate noticeably from the truth.

### Workshop deliverable: the effect of $\epsilon$

The PDF asks you to comment on $\epsilon$. Re-run with several values and look at both the *correct identification* of the best arm and the *estimated-reward accuracy*.

| $\epsilon$ | Behaviour |
|------------|-----------|
| $\epsilon = 0$ (pure greedy) | Agent locks onto whichever arm wins first. If the truly-best arm has bad luck early, you can stay stuck on a suboptimal arm forever. **High variance, often wrong.** |
| $\epsilon = 0.01$ | Mostly exploits, almost no exploration. Fast accumulation of reward *if* the early estimates happen to point at the right arm. |
| $\epsilon = 0.1$ (default here) | A common reasonable choice: ~10% exploration. Best arm reliably identified after ~1000 trials; total reward close to optimal. |
| $\epsilon = 0.5$ | Half the trials are random. Estimates of *all* arms become accurate (great for identification) but cumulative reward is poor — you keep pulling losing arms. |
| $\epsilon = 1$ | Pure random; never exploits; total reward $\approx T \cdot \overline{\mu}$, the *mean* of the arms — terrible. |

**The trade-off in one sentence:** small $\epsilon$ exploits well *if* you got lucky early; large $\epsilon$ guarantees identification at the cost of regret. **Decaying** $\epsilon_t \propto 1/t$ (or similar schedule) is the standard fix — explore aggressively early, exploit later.

---

## Connection to Q-learning (Task 1)

A multi-armed bandit is a Markov decision process with **a single state**. Compare:

| Quantity | Bandit (this task) | Q-learning (Task 1) |
|----------|-------------------|---------------------|
| State $s$ | (none / one) | grid location |
| Action value | $Q(a)$ | $Q(s, a)$ |
| Update target | $r$ | $r + \gamma \max_{a'} Q(s', a')$ |
| Step size | $1/N(a)$ (sample average) | $\alpha$ (constant) |
| Exploration | $\epsilon$-greedy | random in this notebook (could also be $\epsilon$-greedy) |
| Discount $\gamma$ | irrelevant (no future state) | central |

The bandit is essentially "Q-learning with the bootstrap term deleted". This is the cleanest place to study exploration vs. exploitation in isolation.

---

## What to take away for the exam

- **Bandit framework:** stateless RL. $K$ arms, reward $r_t \sim$ unknown distribution with mean $\mu_{a_t}$. Goal: maximise $\sum_t r_t$, equivalently minimise regret $T\mu^* - \mathbb{E}[\sum_t r_t]$.
- **Sample-average action-value:** $Q_t(a) = \frac{1}{N_t(a)} \sum_{i=1}^{N_t(a)} r_i$, equivalently the incremental update
  $$
  Q_{n} \leftarrow Q_{n-1} + \frac{1}{n}(r_n - Q_{n-1}).
  $$
  Memorise both forms — they appear in derivation-style questions. ⚠️ *No formula sheet from Week 3 onwards.*
- **$\epsilon$-greedy policy:**
  $$
  a_t = \begin{cases} \text{uniform random arm} & \text{w.p. } \epsilon \\ \arg\max_a Q_t(a) & \text{w.p. } 1-\epsilon \end{cases}
  $$
- **Exploration-exploitation trade-off:**
  - Pure exploit ($\epsilon=0$): low variance once locked on, but can lock on wrong arm forever.
  - Pure explore ($\epsilon=1$): full identification but terrible cumulative reward.
  - Sweet spot: small constant $\epsilon$ (e.g. 0.1) for stationary problems, or *decaying* $\epsilon_t$ for asymptotic optimality.
- **Identification vs. reward.** Higher $\epsilon$ gives more accurate $\hat{\mu}_a$ for *all* arms (good if you only care about *which* is best at the end), but lower expected reward during learning (bad if every pull costs you).
- **Connection to Q-learning:** bandit = MDP with a single state, no discounting, no bootstrapping. The $1/n$ step size is the *sample-average* analogue of the constant learning rate $\alpha$ in [[q-learning]].
- **Likely exam style:** explain the exploration/exploitation trade-off; write down the $\epsilon$-greedy rule and the incremental update; compute one update step by hand given $(Q, N, r)$; describe the effect of varying $\epsilon$.
- **Connections:** [[multi-armed-bandits]], [[reinforcement-learning]], [[q-learning]], [[markov-decision-process]] (single-state special case).
