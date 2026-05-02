# Selection Methods

**Type:** algorithm component
**Related:** [[evolutionary-algorithms]], [[fitness-landscapes]]
**Source lectures:** [[lecture04-ea-detail]]

---

## What it is

**Selection** chooses which individuals in the population will produce offspring. It must be **biased toward fitter individuals** (selection pressure) while maintaining enough diversity to avoid premature convergence.

---

## The selection pressure tradeoff

| Pressure | Effect |
|----------|--------|
| Too low (random) | No evolutionary progress |
| Too high (always best) | Premature convergence to local optimum |
| Moderate | Effective exploration + exploitation |

---

## Method 1: Fitness Proportionate (Roulette Wheel) Selection

**Probability of selecting individual $i$:**
$$P(i) = \frac{f_i}{\sum_{k=1}^{P} f_k}$$

Equivalent to spinning a roulette wheel with sectors proportional to fitness.

**Problems:**
- Requires positive fitness values (breaks for minimisation or negative fitness)
- **Dominance by superfit individuals:** if one individual has $f=100$ and others have $f \approx 0.1$–$0.5$, it dominates selection entirely — diversity collapses
- Sensitive to scaling: adding a constant to all fitnesses changes relative probabilities
- **Rarely used in modern EAs**

---

## Method 2: Rank-Based Selection

Instead of using raw fitness, **rank** individuals from best (rank $P$) to worst (rank $1$). Selection probability is proportional to rank (or a function of rank).

**Variants:**
- **Linear bias:** $P(i) \propto \text{rank}_i$
- **Low bias:** $P(i) \propto \text{rank}_i^{0.5}$ — more equal chances
- **High bias:** $P(i) \propto \text{rank}_i^{2}$ — more pressure toward best

**Advantages over roulette wheel:**
- Immune to superfit dominance (rank differences are bounded)
- Works for any fitness (minimisation, negative values)
- Selection pressure is controllable via the rank function

---

## Method 3: Tournament Selection

```
Repeat t times:
    Choose a random individual from the population
Tournament winner = the individual with best fitness among the t chosen
Return the winner
```

**Parameters:** tournament size $t$

| $t$ | Effect |
|-----|--------|
| 1 | Random selection (no pressure) |
| 2 | Mild pressure |
| Large | High pressure (nearly always picks best) |
| $t = \text{popsize}$ | Deterministic: always picks the best |

**Advantages:**
- Simple and efficient (no sorting required)
- Tunable selection pressure via $t$
- Avoids problems of superfit/superpoor individuals
- Standard method in modern EAs

**Disadvantage:** One extra parameter ($t$) to tune.

---

## Comparison table

| Method | Pressure control | Handles negative fitness | Computationally efficient | Common today |
|--------|----------------|--------------------------|--------------------------|--------------|
| Roulette wheel | Poor | No | Yes | Rarely |
| Rank-based | Good | Yes | Needs sorting | Sometimes |
| Tournament | Excellent | Yes | Yes | Most common |

---

## Exam notes

- Know all three methods and their selection probability formulas/procedures
- **Roulette wheel problems:** superfit dominance, negative fitness incompatibility, minimisation complications
- Tournament selection: increasing $t$ increases selection pressure
- Rank-based: decouples selection from raw fitness values — more robust
- Selection pressure controls the speed of convergence vs. diversity tradeoff
