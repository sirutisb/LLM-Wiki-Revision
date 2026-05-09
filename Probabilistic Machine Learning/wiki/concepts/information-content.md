# Information Content

**Type:** concept
**Week:** 6
**Related:** [[entropy]], [[cross-entropy]], [[mutual-information]]
**Source:** [[lecture-w6]]

## Definition
Information content (or self-information) measures the amount of "surprise" or information gained when a specific outcome of a discrete random variable is observed.

## Motivation
We need a quantitative way to measure how informative an event is. Highly probable events carry little information (low surprise), while rare events carry a lot of information (high surprise).

## How it works
For an event $x$ with probability $P(x)$, the information content is:
$$I(x) = -\log_2 P(x)$$
Units are in bits (if log base 2) or nats (if natural log).

## Key derivation
Not applicable; this is a foundational definition.

## Parameters & intuition
- $P(x) = 1 \implies I(x) = 0$ (no surprise).
- As $P(x) \to 0$, $I(x) \to \infty$ (infinite surprise).
- Additive for independent events: $I(x, y) = I(x) + I(y)$.

## Connections
- [[entropy]] is the expected value of information content over all possible events.

## Exam notes
- May be needed as a stepping stone for entropy calculations.
- Formula status: often expected to know ⚠️
