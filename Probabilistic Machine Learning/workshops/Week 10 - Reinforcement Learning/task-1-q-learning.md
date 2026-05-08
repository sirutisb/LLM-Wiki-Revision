# Task 1 — Q-Learning on a Connected-Locations MDP

**Problem statement (workshop PDF, §1).** An agent is placed in an environment consisting of several connected locations $L_1,\dots,L_9$. Use Q-learning to learn the optimal path from a chosen start location to a target location.

**Workshop instructions:**

1. Study the provided notebook and understand how the Q-learning model is implemented.
2. Identify the locations (states) and the reward matrix used in the environment.
3. Define a new starting location and a new ending location.
4. Use the learned Q-values to find the optimal route.
5. Report the chosen start, the chosen end, and the optimal route returned.

**Concepts:** [[q-learning]], [[reinforcement-learning]], [[markov-decision-process]], [[bellman-equation]], [[lecture-w9]]

---

## What we're trying to do

The big picture of reinforcement learning: we have an **agent** moving through **states** by taking **actions**, receiving **rewards** along the way. We don't know the reward dynamics in advance; the agent must learn — purely from interaction — a **policy** $\pi(s)$ that maximises long-run reward.

Q-learning is the canonical *off-policy*, *model-free* algorithm for this. It learns an *action-value function*
$$
Q(s, a) \approx \text{expected discounted return if we take action } a \text{ in state } s, \text{then act greedily.}
$$
Once $Q$ has converged, the optimal policy is just $\pi^*(s) = \arg\max_a Q(s, a)$.

In this workshop the "states" are 9 connected locations on a small graph; the "actions" are *moving to a neighbour*. The agent has no map — it explores randomly for 1000 episodes, watches which transitions accumulate value, and the Q-table emerges.

### The two equations you must know

**Bellman optimality equation** (defines what $Q^*$ should be):
$$
Q^*(s, a) = \mathbb{E}\!\left[r + \gamma \max_{a'} Q^*(s', a') \,\middle|\, s, a\right].
$$
This is just a self-consistency condition: the value of $(s,a)$ equals the immediate reward plus the discounted value of the *best* next action.

**Q-learning TD update** (turns the equation above into a learning rule):
$$
Q(s, a) \;\leftarrow\; Q(s, a) + \alpha\,\Bigl[\,\underbrace{r + \gamma \max_{a'} Q(s', a') - Q(s, a)}_{\text{TD error } \delta}\,\Bigr].
$$
Each step, we nudge $Q(s,a)$ a little towards the *Bellman target* $r + \gamma \max_{a'} Q(s', a')$. The learning rate $\alpha$ controls how big the nudge is; the discount factor $\gamma \in [0,1)$ controls how much we care about future rewards versus immediate ones.

The "off-policy" property comes from the $\max_{a'}$: we update as if we *will* act greedily next, even though our actual exploration may have been random.

---

## Cell-by-cell walkthrough

### Cell 1 — Imports

```python
import numpy as np
```

Just numpy. Q-learning here is small enough to be a few numpy operations on a $9 \times 9$ matrix.

### Cell 2 — Hyperparameters

```python
gamma = 0.8   # discounting factor
alpha = 0.9   # learning rate
```

Two knobs to internalise:

- **Discount factor $\gamma$.** With $\gamma = 0.8$, a reward $k$ steps away is worth $0.8^k$ as much as a reward right now. Closer to 1 $\Rightarrow$ farsighted agent (cares about distant rewards). Closer to 0 $\Rightarrow$ myopic agent (almost ignores the future). $\gamma$ must be $<1$ for infinite-horizon convergence.
- **Learning rate $\alpha$.** With $\alpha = 0.9$, each TD update *almost completely* overwrites the old estimate with the Bellman target. This is aggressive — it works here because the environment is deterministic. In a stochastic environment you'd want a smaller $\alpha$ (e.g. 0.1) to *average* over noisy samples.

### Cell 3 — States (locations)

```python
location_to_state = {'L1': 0, 'L2': 1, ..., 'L9': 8}
```

Each location $L_i$ gets an integer index $0\dots 8$. This is just a name $\leftrightarrow$ index dictionary so we can use the location names in pretty input/output but indices for matrix arithmetic.

### Cell 4 — Actions

```python
actions = [0, 1, 2, 3, 4, 5, 6, 7, 8]
```

Action $j$ means *"try to go to state $j$"*. There are 9 possible actions (one per state). Whether action $j$ is *legal* in state $i$ is encoded by the reward matrix — illegal moves have reward 0 and never get picked.

### Cell 5 — Reward matrix

```python
rewards = np.array([
    [0,1,0,0,0,0,0,0,0],   # from L1 you can go to L2
    [1,0,1,0,0,0,0,0,0],   # from L2 you can go to L1 or L3
    [0,1,0,0,0,1,0,0,0],   # from L3: L2 or L6
    [0,0,0,0,0,0,1,0,0],   # from L4: L7
    [0,1,0,0,0,0,0,1,0],   # from L5: L2 or L8
    [0,0,1,0,0,0,0,0,0],   # from L6: L3
    [0,0,0,1,0,0,0,1,0],   # from L7: L4 or L8
    [0,0,0,0,1,0,1,0,1],   # from L8: L5, L7, or L9
    [0,0,0,0,0,0,0,1,0],   # from L9: L8
])
```

This is a $9\times 9$ adjacency matrix doubling as a reward signal: `rewards[i, j] = 1` if you can move from $L_{i+1}$ to $L_{j+1}$ in one step, else 0. The graph is undirected (entry $(i,j)$ matches entry $(j,i)$).

In standard RL terminology this defines both:

- The **transition function** (legal next states from state $i$ are the columns where `rewards[i, j] > 0`), and
- The **reward function** (every legal move gives reward 1, illegal moves give 0).

The trick the notebook uses next is to *spike the reward at the goal*.

### Cell 6 — `state_to_location` (inverse map)

```python
state_to_location = dict((s, l) for l, s in location_to_state.items())
```

Reverse dictionary so we can translate the final integer route back to `'L1', 'L2', ...` for printing.

### Cell 7 — `get_optimal_route(start, end)`

This is the whole algorithm. Let's break it into three phases.

#### Phase 1 — Set up the goal

```python
rewards_new = np.copy(rewards)
ending_state = location_to_state[end_location]
rewards_new[ending_state, ending_state] = 999
```

We copy the reward matrix and add a **huge self-loop reward at the goal state**. This is the trick that turns "find a path" into a Q-learning problem: the goal becomes the only place worth a lot, so the Q-values upstream will inflate via Bellman backups (each upstream state inherits a discounted slice of that 999 through the $\max$ in the update).

If we *didn't* spike the goal, every legal move would have reward 1 and Q-values would be roughly equal everywhere — nothing to climb towards.

#### Phase 2 — Train the Q-table

```python
Q = np.zeros((9, 9))               # initialise to zero

for i in range(1000):
    current_state = np.random.randint(0, 9)            # random restart
    playable_actions = [j for j in range(9) if rewards_new[current_state, j] > 0]
    next_state = np.random.choice(playable_actions)    # uniform-random action

    TD = rewards_new[current_state, next_state] \
         + gamma * Q[next_state, np.argmax(Q[next_state, :])] \
         - Q[current_state, next_state]

    Q[current_state, next_state] += alpha * TD
```

What's happening on each iteration:

1. **Pick a random state.** This is *not* a normal episode — there's no rollout, no terminal state. The notebook is doing single-step Q updates from random starts. Over 1000 iterations every $(s, a)$ pair gets visited many times.
2. **List legal actions** from `current_state` (columns of `rewards_new` that are non-zero).
3. **Pick one uniformly at random.** This is the "exploration" — pure random behaviour, no $\epsilon$-greedy needed because we're just sampling transitions to fill in the Q-table.
4. **Compute the TD error**
   $$
   \delta = r + \gamma \max_{a'} Q(s', a') - Q(s, a).
   $$
   `Q[next_state, np.argmax(Q[next_state, :])]` is just `np.max(Q[next_state, :])` written the long way.
5. **Update** $Q(s,a) \leftarrow Q(s,a) + \alpha\,\delta$ — the line right out of the [[bellman-equation]] derivation.

After 1000 iterations the Q-values radiate out from the goal: states near the goal get large Q-values, states far from the goal get smaller (discounted by $\gamma$ each step).

This is **off-policy**: we explored uniformly at random, but the update used $\max_{a'} Q(s', a')$, which assumes we'll act *greedily* in future. That's why the converged $Q$ encodes the *optimal* policy, not the random exploration policy.

#### Phase 3 — Read out the optimal route

```python
route = [start_location]
next_location = start_location
while next_location != end_location:
    starting_state = location_to_state[start_location]
    next_state = np.argmax(Q[starting_state, :])    # greedy w.r.t. learned Q
    next_location = state_to_location[next_state]
    route.append(next_location)
    start_location = next_location
return route
```

Now we *exploit*. From the start state, repeatedly pick the action $a^* = \arg\max_a Q(s, a)$, follow it, and keep going until we land on the goal. This is the **greedy policy** induced by the Q-table:
$$
\pi^*(s) = \arg\max_a Q(s, a).
$$
Because we pumped the goal with reward 999 and let Q-learning propagate that backwards, the greedy policy traces the shortest path through the graph.

### Cell 8 — Run it

```python
print(get_optimal_route('L8', 'L3'))
# ['L8', 'L5', 'L2', 'L3']
```

Verify by inspecting the adjacency:

- $L_8 \to L_5$ (legal, `rewards[7, 4] = 1`)
- $L_5 \to L_2$ (legal, `rewards[4, 1] = 1`)
- $L_2 \to L_3$ (legal, `rewards[1, 2] = 1`)

Three steps, ends at the goal. That is the shortest path — try sketching the graph from the reward matrix and you'll see there's no two-step route from $L_8$ to $L_3$.

### Workshop deliverable (your task)

Pick *your own* `start` and `end` and print the route. Examples that highlight different paths:

| Start | End | Expected route (one of) |
|-------|-----|------------------------|
| `L9`  | `L4` | `['L9','L8','L7','L4']` |
| `L1`  | `L6` | `['L1','L2','L3','L6']` |
| `L4`  | `L9` | `['L4','L7','L8','L9']` |

You should report (i) start, (ii) end, (iii) the route printed by `get_optimal_route`.

---

## Why this works (the bigger picture)

Q-learning's convergence guarantee: **if every state-action pair is visited infinitely often and $\alpha$ decays appropriately, $Q \to Q^*$ regardless of the exploration policy.** This is the [[markov-decision-process]] / [[bellman-equation]] result you'd cite in an exam derivation question.

Here, "infinitely often" is approximated by 1000 random restarts, "decay" is replaced by a constant $\alpha = 0.9$ (works because deterministic environment), and the result is good enough to read off the optimal path.

---

## What to take away for the exam

- **Q-learning update rule (you must memorise this — no formula sheet from Week 3 onwards):**
  $$
  Q(s, a) \;\leftarrow\; Q(s, a) + \alpha\,\bigl[r + \gamma \max_{a'} Q(s', a') - Q(s, a)\bigr].
  $$
- **The bracketed quantity is the TD error** $\delta_t = r + \gamma \max_{a'} Q(s', a') - Q(s, a)$. When $\delta = 0$ everywhere we have reached the Bellman fixed point $Q = Q^*$.
- **Bellman optimality:** $Q^*(s,a) = \mathbb{E}[r + \gamma \max_{a'} Q^*(s', a')]$. Q-learning is just the stochastic-approximation iteration that solves this fixed-point equation.
- **Off-policy:** behaviour policy (how you pick actions while exploring) need not match the target policy (what you're learning the value of). The $\max$ in the update is what makes Q-learning off-policy — it bakes in the assumption of greedy future behaviour.
- **Hyperparameter intuition:**
  - $\gamma$ closer to 1 = farsighted; $\gamma$ small = myopic. Must be $<1$ for convergence.
  - $\alpha$ large = fast learning but unstable in stochastic settings; $\alpha$ small = slow but smooth averaging.
- **Greedy readout:** once trained, optimal policy is $\pi^*(s) = \arg\max_a Q(s, a)$. Exploration was for *learning*; deployment is greedy.
- **Why a goal-reward spike works:** Q-values propagate backwards from the goal through repeated Bellman updates. The size of the spike doesn't matter much — what matters is that one state stands out so the gradient of $Q$ has somewhere to point.
- **Likely exam question:** state the Q-learning update rule, identify $\gamma$ and $\alpha$, explain the role of $\max_{a'}$, or compute one update by hand given a tiny $Q$-table and a transition $(s, a, r, s')$.
- **Connections:** [[reinforcement-learning]] frames the problem; [[markov-decision-process]] is the formal model; [[bellman-equation]] gives the fixed-point that Q-learning solves; [[multi-armed-bandits]] is the *stateless* special case (next task).
