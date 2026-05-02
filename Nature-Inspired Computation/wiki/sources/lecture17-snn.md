# Lecture 17 — Spiking Neural Networks

**File:** `raw/text/17-snn.txt`
**Lecturer:** Dr David Walker
**Concepts introduced:** [[spiking-neural-networks]]

---

## Summary

Introduces SNNs as a more biologically plausible alternative to standard ANNs. Covers spike coding, LIF neuron dynamics, STDP learning rule, the backpropagation problem with spike functions, surrogate gradient approach, and EA-based SNN optimisation.

## Key content

### Motivation
Robots need: high-dimensional sensor processing with low latency, sparse information processing, energy efficiency, adaptability to dynamic environments. Standard ANNs: high latency, energy hungry, not biologically plausible.

### SNN properties
- Transmit information as discrete spikes over time (third generation neural networks)
- Much more biologically plausible than ANNs
- Sparse activation → low-power computing
- Applications: robotics, speech recognition, temporal pattern recognition

### Information coding
- **Rate coding:** spike frequency represents signal strength
- **Temporal coding:** precise spike timing encodes information
- **Population coding:** pattern across many neurons

### SNN architecture
Spike train = sequence of spikes from one neuron. Each neuron receives and emits spikes.

### Leaky Integrate-and-Fire (LIF) neuron
1. Neuron accumulates charge from input signals
2. When charge ≥ threshold → fires (emits spike on all outgoing connections)
3. Charge resets to 0 after firing
4. Below threshold → charge leaks away over time

### Spike-Timing-Dependent Plasticity (STDP)
- Pre-fires before post → **potentiation** (strengthen synapse)
- Post-fires before pre → **depression** (weaken synapse)
- Supports **unsupervised learning**

### The backpropagation problem
Spiking function derivative = Dirac delta:
$$\delta(x) = 0 \text{ for } x \neq 0; \quad \int_{-\infty}^{\infty} \delta(x) dx = 1$$
No gradient information → cannot use backpropagation.

### Surrogate gradient
Replace spiking function with sigmoid $f(a) = 1/(1+e^{-a})$ for gradient computation:
$$f'(a) = f(a)(1 - f(a))$$
With scaling $k$: $\lim_{k \to \infty} f_k'(a) = \delta(a)$. Allows approximate backpropagation.

### Optimising SNNs with EAs
Optimise weights, delays, thresholds, architecture. **Neural Architecture Search (NAS):** bi-level problem — optimise structure (upper) and weights (lower) alternately.

Challenges:
1. SNN simulation is expensive → combined with EA = very costly
2. Co-evolution of multiple SNN aspects simultaneously

## Key takeaways
- SNN = discrete spikes + leaky integration + threshold firing + STDP learning
- STDP is unsupervised; surrogate gradients enable backpropagation-like training
- EAs useful for SNN because gradient-based training is difficult

## Links to concepts
- [[spiking-neural-networks]]: full treatment
- [[neural-networks]]: ANNs as the predecessor
- [[neuromorphic-computing]]: hardware for running SNNs
- [[evolutionary-algorithms]]: used for SNN optimisation
