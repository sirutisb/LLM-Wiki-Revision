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

### Intuition: What is a "bit"?
A bit represents one binary decision (e.g., yes/no, true/false). If you have $N$ equally likely possibilities, you need $\log_2(N)$ bits to uniquely identify one of them. For instance, a fair coin flip requires 1 bit ($-\log_2(0.5) = 1$). A fair 8-sided die requires 3 bits ($-\log_2(1/8) = 3$). The negative log appears naturally because probabilities are fractions (reversing the exponent), and we want a positive information value.

### Intuition: Transmitting only surprises
Why does a rare event have more "information"? Bits are not just labels; they describe *deviations from expectation*.

**The Encoding Idea**
Suppose we have 100 animals: 99 are cats and 1 is a dog. 

Instead of naively storing a bit for every animal:
`0 0 0 0 0 0 1 0 0 ...` (100 bits total)

You could instead just store:
`[73]`

Meaning: *"The dog occurred at index 73."*

Now you only need enough bits to encode numbers 0–99. That requires:
$\lceil \log_2(100) \rceil = 7$ bits.

**Why did entropy predict ~6.64 bits?**
Because entropy gives the theoretical ideal average:
$-\log_2(0.01) \approx 6.64$ bits.

Actual computers store whole bits. So practically you'd use 7 bits (or maybe 1 byte) depending on implementation. Entropy provides the theoretical lower bound, not necessarily the exact implementation size.

**Why this compression works**
Because both sender and receiver already assume: *"Everything is a cat unless told otherwise."*
So:
- Cat costs almost nothing to transmit.
- Only unexpected events need explicit transmission.

Information theory is fundamentally about *transmitting only surprises*.

**This is also how real compression works**
Real compressors exploit predictability:
- **Text compression:** In English, 'e' is common and 'z' is rare. Common symbols get short encodings, and rare symbols get longer ones.
- **Video compression:** Most pixels barely change frame-to-frame. Codecs mostly encode *"what changed"* instead of resending the whole image.

**Machine learning connection**
A good probabilistic model predicts reality well. That means:
- Real data becomes unsurprising.
- Coding length becomes small.

Which is why maximizing likelihood, minimizing cross-entropy, and minimizing KL divergence all fundamentally correspond to better compression!

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
