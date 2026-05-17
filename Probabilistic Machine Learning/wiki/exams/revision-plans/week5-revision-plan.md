# Week 5 Revision Plan - MCMC

**Scope:** [[mcmc]], [[monte-carlo-integration]], [[rejection-sampling]], [[importance-sampling]], [[metropolis-hastings]], [[gibbs-sampling]], [[importance-vs-rejection-sampling]], [[mcmc-algorithms]]
**Source:** [[lecture-w5]], [[lecture-w10]], [[examinable-topics]], [[week5_questions]]
**Formula status:** No formula sheet for Week 5. Derivations are not examinable, but the Monte Carlo estimator, rejection sampling acceptance rule, importance weights, self-normalised importance sampling estimator, Metropolis-Hastings acceptance ratio, Metropolis special case, Gibbs update idea, burn-in, stationarity, ergodicity, and detailed balance definitions must be known from memory.

Week 5 is lower priority than Weeks 1-4 and 7, but it is a compact and exam-friendly topic. The likely questions are conceptual comparisons and short algorithm traces: compare rejection sampling with importance sampling, explain why basic sampling fails in high dimensions, write the Metropolis-Hastings algorithm, simplify it to Metropolis, identify Gibbs as an always-accepting special case, or compute an acceptance probability from given numbers.

---

## What To Know Cold

### Core purpose
- [ ] Bayesian inference often needs posterior expectations, not a closed-form posterior:
$$
\mathbb{E}_{p(\theta|\mathcal{D})}[f(\theta)]
=
\int f(\theta)p(\theta|\mathcal{D})\,d\theta.
$$
- [ ] The posterior is usually available only up to normalisation:
$$
p(\theta|\mathcal{D}) = \frac{\tilde{p}(\theta)}{Z},
\qquad
\tilde{p}(\theta)=p(\mathcal{D}|\theta)p(\theta).
$$
- [ ] Sampling methods approximate expectations using samples instead of analytic integration.
- [ ] MCMC is used when direct sampling, rejection sampling, and importance sampling are impractical.

### Monte Carlo integration
- [ ] General estimator:
$$
\mathbb{E}_{p}[f(\theta)]
\approx
\frac{1}{N}\sum_{i=1}^{N} f(\theta_i),
\qquad
\theta_i \sim p(\theta).
$$
- [ ] Posterior mean estimate:
$$
\mathbb{E}[\theta|\mathcal{D}]
\approx
\frac{1}{N}\sum_{i=1}^{N}\theta_i.
$$
- [ ] Posterior variance estimate:
$$
\mathrm{Var}(\theta|\mathcal{D})
\approx
\frac{1}{N}\sum_{i=1}^{N}(\theta_i-\bar{\theta})^2.
$$
- [ ] Convergence rate is $O(1/\sqrt{N})$.
- [ ] Monte Carlo avoids grid-based numerical integration, whose cost grows badly with dimension.
- [ ] Key limitation: it requires samples from the target distribution or a method that produces approximately target-distributed samples.

### Rejection sampling
- [ ] Setup: target $p^*(\theta) \propto \tilde{p}(\theta)$, proposal $q(\theta)$, and envelope constant $M$.
- [ ] Envelope condition:
$$
\tilde{p}(\theta) \leq Mq(\theta)
\quad \text{for all } \theta.
$$
- [ ] Algorithm:
  1. Draw $\theta^* \sim q(\theta)$.
  2. Draw $u \sim \mathrm{Uniform}(0,1)$.
  3. Accept $\theta^*$ if
$$
u \leq \frac{\tilde{p}(\theta^*)}{M q(\theta^*)}.
$$
  4. Otherwise reject and try again.
- [ ] Output: exact independent unweighted samples from the target.
- [ ] Advantage: accepted samples are genuine target samples.
- [ ] Limitation: rejected samples are wasted, and acceptance rate can collapse in high dimensions.
- [ ] Tight $M$ means higher acceptance; loose $M$ means many rejections.

### Importance sampling
- [ ] Draw samples from a proposal $q(\theta)$, but keep all samples and reweight them.
- [ ] Importance weight:
$$
w(\theta)=\frac{p^*(\theta)}{q(\theta)}.
$$
- [ ] Unnormalised weight:
$$
\tilde{w}(\theta)=\frac{\tilde{p}(\theta)}{q(\theta)}.
$$
- [ ] Self-normalised estimator:
$$
\mathbb{E}_{p^*}[f(\theta)]
\approx
\frac{\sum_{i=1}^{N} f(\theta_i)\tilde{w}(\theta_i)}
{\sum_{i=1}^{N}\tilde{w}(\theta_i)},
\qquad
\theta_i \sim q(\theta).
$$
- [ ] Support condition: $q(\theta)>0$ wherever the target has probability mass.
- [ ] Advantage over rejection sampling: no samples are discarded.
- [ ] Limitation: weight degeneracy; a few large weights can dominate the estimate.
- [ ] In high dimensions, proposal-target mismatch causes low effective sample size.

### MCMC foundations
- [ ] A Markov chain is a sequence where the next state depends only on the current state.
- [ ] MCMC constructs a Markov chain whose stationary distribution is the target posterior.
- [ ] Stationary distribution:
$$
p^*(\theta')
=
\int p^*(\theta)T(\theta'|\theta)\,d\theta.
$$
- [ ] Ergodicity: after enough iterations, the chain forgets its initial state and converges to the stationary distribution.
- [ ] Detailed balance is a sufficient condition for stationarity:
$$
p^*(\theta)T(\theta'|\theta)
=
p^*(\theta')T(\theta|\theta').
$$
- [ ] Burn-in: discard early samples because they depend too strongly on the initial state.
- [ ] Autocorrelation: MCMC samples are correlated because each sample depends on the previous one.
- [ ] Effective sample size is smaller than the raw number of iterations.

### Metropolis-Hastings
- [ ] Starting from current state $\theta^{(t)}$, propose:
$$
\theta^* \sim q(\theta^*|\theta^{(t)}).
$$
- [ ] Acceptance probability:
$$
\alpha
=
\min\left(
1,
\frac{\tilde{p}(\theta^*)q(\theta^{(t)}|\theta^*)}
{\tilde{p}(\theta^{(t)})q(\theta^*|\theta^{(t)})}
\right).
$$
- [ ] Draw $u \sim \mathrm{Uniform}(0,1)$.
- [ ] If $u \leq \alpha$, accept: $\theta^{(t+1)}=\theta^*$.
- [ ] If $u > \alpha$, reject: $\theta^{(t+1)}=\theta^{(t)}$.
- [ ] The unknown normalising constant cancels in the ratio, so $\tilde{p}$ is enough.
- [ ] The proposal correction term matters when the proposal is asymmetric.
- [ ] Accepting lower-density proposals sometimes is necessary for exploration and escaping local modes.

### Metropolis special case
- [ ] Metropolis is Metropolis-Hastings with a symmetric proposal:
$$
q(\theta^*|\theta)=q(\theta|\theta^*).
$$
- [ ] The proposal terms cancel:
$$
\alpha
=
\min\left(
1,
\frac{\tilde{p}(\theta^*)}{\tilde{p}(\theta^{(t)})}
\right).
$$
- [ ] A Gaussian random walk proposal is the standard example.
- [ ] Proposal width trade-off: too small gives slow mixing; too large gives too many rejections.

### Gibbs sampling
- [ ] Gibbs sampling updates one component at a time from its full conditional:
$$
\theta_j^{(t+1)}
\sim
p(\theta_j|\theta_{-j},\mathcal{D}).
$$
- [ ] Use the most recent values of the other coordinates when cycling through variables.
- [ ] Gibbs is a special case of Metropolis-Hastings with acceptance probability 1.
- [ ] No proposal tuning is needed.
- [ ] Key limitation: full conditional distributions must be tractable to sample from.
- [ ] Gibbs can mix slowly when parameters are strongly correlated.

### Comparisons
- [ ] Rejection sampling vs importance sampling:

| Dimension | Rejection sampling | Importance sampling |
|-----------|--------------------|---------------------|
| Main action | Discards bad proposals | Keeps all proposals and reweights |
| Output | Exact independent samples | Weighted samples / expectation estimates |
| Needs $M$? | Yes | No |
| Main failure | Low acceptance rate | Weight degeneracy |
| Performance metric | Acceptance rate | Effective sample size |

- [ ] Metropolis-Hastings vs Metropolis vs Gibbs:

| Algorithm | Proposal | Acceptance |
|-----------|----------|------------|
| Metropolis-Hastings | General $q(\theta^*|\theta)$ | $\min(1,A)$ with proposal correction |
| Metropolis | Symmetric proposal | $\min(1,\tilde{p}(\theta^*)/\tilde{p}(\theta))$ |
| Gibbs | Exact full conditional | Always accepts |

- [ ] Laplace vs VI vs MCMC:
  - Laplace: local Gaussian approximation around MAP; fast but crude for non-Gaussian or multimodal posteriors.
  - VI: optimisation over a tractable family; scalable but biased by the chosen family and KL direction.
  - MCMC: asymptotically exact and shape-flexible, but slower and produces correlated samples.

---

## Revision Schedule

### Pass 1 - 40 minutes: memory setup
- [ ] Write the Monte Carlo estimator from memory.
- [ ] Write the rejection sampling envelope condition and acceptance rule from memory.
- [ ] Write the importance weight and self-normalised estimator from memory.
- [ ] Write the Metropolis-Hastings acceptance probability from memory.
- [ ] Write the simplified Metropolis acceptance probability from memory.
- [ ] Explain Gibbs sampling without looking at notes.
- [ ] Define stationary distribution, detailed balance, ergodicity, burn-in, and autocorrelation in one sentence each.

### Pass 2 - 45 minutes: rejection and importance sampling
- [ ] Do [[week5_questions]] Q2.
- [ ] Do [[week5_questions]] Q5.
- [ ] Build a comparison table from memory: goal, output, whether samples are discarded, need for $M$, high-dimensional failure mode.
- [ ] Explain why both methods use a fixed global proposal and why that is the core problem in high dimensions.
- [ ] For a numerical rejection sampling question, always check the envelope condition before computing the accept/reject decision.

### Pass 3 - 60 minutes: MCMC algorithms
- [ ] Do [[week5_questions]] Q3.
- [ ] Do [[week5_questions]] Q4.
- [ ] For each MH trace, write: current density, proposed density, proposal correction if any, ratio, $\alpha$, uniform draw, next state.
- [ ] Practise simplifying MH to Metropolis when the proposal is symmetric.
- [ ] Explain why Gibbs has acceptance probability 1 and when it cannot be used.

### Pass 4 - 35 minutes: conceptual synthesis
- [ ] Do [[week5_questions]] Q1.
- [ ] Explain MCMC vs VI in four dimensions: bias, computational cost, multimodality, scalability.
- [ ] Explain MCMC vs rejection/importance sampling in terms of local moves versus global proposals.
- [ ] Explain why the normalising constant cancels in MH and is avoided in self-normalised importance sampling.

### Final 15-minute check
- [ ] From a blank page, reproduce all essential formulas listed in the formula status line.
- [ ] Write the MH algorithm as numbered steps without notes.
- [ ] Give one advantage and one limitation of rejection sampling, importance sampling, MH, and Gibbs.
- [ ] Complete one MH acceptance calculation and one rejection sampling acceptance calculation.
- [ ] Answer: "Why does MCMC not produce independent samples, and why is this still useful?"

---

## Worked Example 1 - Monte Carlo Posterior Estimates

### Question

Suppose four posterior samples are:
$$
\theta_1=1,\quad \theta_2=2,\quad \theta_3=3,\quad \theta_4=6.
$$

1. Estimate the posterior mean.
2. Estimate the posterior variance using the Week 5 convention with denominator $N$.
3. State one way to reduce the Monte Carlo error.

### Solution

The posterior mean estimate is:
$$
\bar{\theta}
=
\frac{1+2+3+6}{4}
=
3.
$$

The posterior variance estimate is:
$$
\frac{1}{4}\left[(1-3)^2+(2-3)^2+(3-3)^2+(6-3)^2\right]
=
\frac{1}{4}(4+1+0+9)
=
3.5.
$$

To reduce Monte Carlo error, use more samples. The standard Monte Carlo error decreases at rate $O(1/\sqrt{N})$, so reducing error substantially requires many more samples.

---

## Worked Example 2 - Rejection Sampling Decision

### Question

A target has unnormalised density $\tilde{p}(\theta)$. A proposal $q(\theta)$ and envelope constant $M=8$ are used. At a proposed point $\theta^*$:
$$
\tilde{p}(\theta^*)=3,
\qquad
q(\theta^*)=0.5.
$$

1. Check the envelope condition at this point.
2. Compute the acceptance probability.
3. If $u=0.80$, is the proposal accepted?

### Solution

The envelope value is:
$$
Mq(\theta^*)=8 \times 0.5=4.
$$

Since $3 \leq 4$, the envelope condition holds at this point.

The acceptance probability is:
$$
\frac{\tilde{p}(\theta^*)}{Mq(\theta^*)}
=
\frac{3}{4}
=
0.75.
$$

Since $u=0.80>0.75$, the proposal is rejected.

---

## Worked Example 3 - Importance Sampling Estimate

### Question

Three proposal samples have function values and unnormalised importance weights:

| Sample | $f(\theta_i)$ | $\tilde{w}_i$ |
|--------|---------------|---------------|
| 1 | 2 | 1 |
| 2 | 4 | 3 |
| 3 | 10 | 2 |

Compute the self-normalised importance sampling estimate of $\mathbb{E}_{p^*}[f(\theta)]$.

### Solution

Use:
$$
\hat{\mu}
=
\frac{\sum_i f(\theta_i)\tilde{w}_i}{\sum_i \tilde{w}_i}.
$$

The numerator is:
$$
2(1)+4(3)+10(2)=2+12+20=34.
$$

The denominator is:
$$
1+3+2=6.
$$

Therefore:
$$
\hat{\mu}=\frac{34}{6}\approx 5.67.
$$

The sample with $f(\theta)=10$ has a large influence because it has a relatively large weight. If one weight became much larger than all others, that would indicate weight degeneracy.

---

## Worked Example 4 - Metropolis-Hastings Trace

### Question

Current state is $\theta^{(t)}$. A symmetric Gaussian random walk proposes $\theta^*$. The unnormalised densities are:
$$
\tilde{p}(\theta^{(t)})=0.5,
\qquad
\tilde{p}(\theta^*)=0.2.
$$

1. Which algorithmic special case applies?
2. Compute the acceptance probability.
3. If $u=0.30$, what is $\theta^{(t+1)}$?
4. If $u=0.60$, what is $\theta^{(t+1)}$?

### Solution

Because the proposal is symmetric, this is the Metropolis special case of [[metropolis-hastings]]. The proposal terms cancel.

The acceptance probability is:
$$
\alpha
=
\min\left(1,\frac{0.2}{0.5}\right)
=
0.4.
$$

If $u=0.30$, then $u \leq \alpha$, so the move is accepted:
$$
\theta^{(t+1)}=\theta^*.
$$

If $u=0.60$, then $u > \alpha$, so the move is rejected:
$$
\theta^{(t+1)}=\theta^{(t)}.
$$

The lower-density proposal is not automatically rejected. It is accepted with probability 0.4, which helps the chain explore rather than becoming trapped in one mode.

---

## Worked Example 5 - Asymmetric MH Correction

### Question

Current state is $\theta^{(t)}$ and proposal is $\theta^*$. Suppose:
$$
\tilde{p}(\theta^{(t)})=0.4,
\qquad
\tilde{p}(\theta^*)=0.6,
$$
$$
q(\theta^*|\theta^{(t)})=0.5,
\qquad
q(\theta^{(t)}|\theta^*)=0.25.
$$

Compute the Metropolis-Hastings acceptance probability.

### Solution

Use the full MH ratio because the proposal is asymmetric:
$$
\alpha
=
\min\left(
1,
\frac{\tilde{p}(\theta^*)q(\theta^{(t)}|\theta^*)}
{\tilde{p}(\theta^{(t)})q(\theta^*|\theta^{(t)})}
\right).
$$

Substitute the values:
$$
\alpha
=
\min\left(
1,
\frac{0.6 \times 0.25}{0.4 \times 0.5}
\right)
=
\min(1,0.75)
=
0.75.
$$

Even though the proposed point has higher target density, it is not accepted automatically because the proposal mechanism is asymmetric. The reverse move is less likely than the forward move, so the proposal correction reduces the acceptance probability.

---

## Extra Practice To Work On

### Drill A - Rejection sampling

Use $M=12$.

| Proposal | $\tilde{p}(\theta)$ | $q(\theta)$ | $u$ |
|----------|---------------------|-------------|-----|
| 1 | 2 | 0.5 | 0.20 |
| 2 | 4 | 0.5 | 0.90 |
| 3 | 9 | 1.0 | 0.80 |
| 4 | 8 | 0.4 | 0.50 |

Tasks:
- [ ] Check whether the envelope condition holds at each listed point.
- [ ] Compute the acceptance probability at each point where the envelope is valid.
- [ ] State whether each proposal is accepted or rejected.
- [ ] Identify any row that proves $M$ is invalid for the proposal distribution as stated.

### Drill B - Importance sampling

Use the table:

| Sample | $f(\theta_i)$ | $\tilde{p}(\theta_i)$ | $q(\theta_i)$ |
|--------|---------------|-----------------------|---------------|
| 1 | 1 | 0.2 | 0.1 |
| 2 | 3 | 0.5 | 0.5 |
| 3 | 8 | 0.9 | 0.3 |
| 4 | 2 | 0.4 | 0.4 |

Tasks:
- [ ] Compute each unnormalised importance weight $\tilde{w}_i=\tilde{p}(\theta_i)/q(\theta_i)$.
- [ ] Compute the self-normalised importance estimate.
- [ ] Identify which sample has the largest influence on the estimate.
- [ ] Explain what would happen if one weight were 100 times larger than all others.

### Drill C - Metropolis-Hastings

For each row, compute $\alpha$ and decide whether the proposal is accepted.

| Case | Proposal | $\tilde{p}(\theta^{(t)})$ | $\tilde{p}(\theta^*)$ | $q(\theta^*|\theta^{(t)})$ | $q(\theta^{(t)}|\theta^*)$ | $u$ |
|------|----------|---------------------------|-----------------------|-----------------------------|-----------------------------|-----|
| 1 | symmetric | 0.4 | 0.8 | - | - | 0.99 |
| 2 | symmetric | 0.8 | 0.2 | - | - | 0.30 |
| 3 | asymmetric | 0.5 | 1.0 | 0.8 | 0.2 | 0.40 |
| 4 | asymmetric | 0.5 | 0.4 | 0.2 | 0.8 | 0.90 |

Tasks:
- [ ] Use the Metropolis shortcut only for symmetric proposals.
- [ ] Use the full MH formula for asymmetric proposals.
- [ ] State the next state in every case.
- [ ] Explain in one sentence why case 3 is not automatically accepted even though $\tilde{p}(\theta^*)>\tilde{p}(\theta^{(t)})$.

### Drill D - Conceptual short answers

Answer each in two or three sentences:
- [ ] Why is a global proposal hard to design in high dimensions?
- [ ] Why can importance sampling use all samples but still perform badly?
- [ ] Why does rejection sampling produce exact independent samples?
- [ ] Why does MCMC trade independence for scalability?
- [ ] Why does Gibbs sampling require tractable full conditionals?
- [ ] Why does burn-in not fix poor mixing?
- [ ] Why does the normalising constant cancel in MH?
- [ ] Why can VI be faster but more biased than MCMC?

---

## Common Mistakes

- [ ] Saying Week 5 derivations are examinable. They are not; algorithms, formulas, and conceptual comparisons are the exam focus.
- [ ] Forgetting that no formula sheet is provided for Week 5.
- [ ] Using the normalised posterior $p(\theta|\mathcal{D})$ in formulas when the algorithm only needs $\tilde{p}(\theta)$ ratios.
- [ ] Forgetting to cap MH acceptance probabilities at 1.
- [ ] Rejecting every lower-density MH proposal automatically. Lower-density proposals can still be accepted.
- [ ] Using the Metropolis shortcut for an asymmetric proposal.
- [ ] Swapping the proposal correction in MH. The numerator uses the reverse proposal probability $q(\theta^{(t)}|\theta^*)$.
- [ ] Treating rejected MH proposals as disappearing from the chain. The next state is the old state, so the old value is repeated.
- [ ] Treating MCMC samples as independent. They are autocorrelated.
- [ ] Thinking burn-in makes samples independent. Burn-in addresses initialisation bias, not autocorrelation.
- [ ] Confusing rejection sampling with MH. Rejection sampling proposes independently from a global $q$; MH proposes from the current state.
- [ ] Forgetting the rejection sampling envelope condition must hold everywhere, not only at one proposed point.
- [ ] Ignoring support matching in importance sampling. If $q(\theta)=0$ where the target has mass, the estimator misses that region.
- [ ] Saying Gibbs works for any model. It only works directly when full conditionals are tractable to sample from.
- [ ] Saying Gibbs has no randomness because it always accepts. It is still random because each coordinate is sampled from a conditional distribution.
- [ ] Explaining high-dimensional failure only as "slow" without naming the mechanism: low acceptance rate for rejection sampling, weight degeneracy for importance sampling, and poor mixing/autocorrelation for badly tuned MCMC.

---

## Exam-Ready Checklist

You are Week 5-ready when you can:

- [ ] Reproduce the Monte Carlo estimator, rejection sampling acceptance rule, importance weight, self-normalised importance sampling estimator, full MH acceptance probability, and Metropolis special case from memory.
- [ ] Write the rejection sampling algorithm as numbered steps.
- [ ] Write the Metropolis-Hastings algorithm as numbered steps.
- [ ] Explain Gibbs sampling as conditional sampling with acceptance probability 1.
- [ ] Complete a rejection sampling accept/reject calculation without notes.
- [ ] Complete a symmetric and asymmetric MH accept/reject calculation without notes.
- [ ] Compare rejection sampling and importance sampling in a table.
- [ ] Compare MH, Metropolis, and Gibbs in a table.
- [ ] Explain why MCMC uses local Markov-chain moves rather than a fixed global proposal.
- [ ] Explain stationary distribution, detailed balance, ergodicity, burn-in, mixing, and autocorrelation clearly.
- [ ] Explain MCMC vs VI vs Laplace in terms of approximation type, bias, speed, and posterior shape.
- [ ] State that Week 5 has no formula sheet and no examinable derivations.
