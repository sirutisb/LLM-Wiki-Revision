# Spiking Neural Networks (SNNs)

**Type:** model / algorithm
**Related:** [[neural-networks]], [[neuromorphic-computing]], [[evolutionary-algorithms]]
**Source lectures:** [[lecture17-snn]]

---

## What it is

A **Spiking Neural Network (SNN)** is a neural network model that more closely mimics the brain's actual neural behaviour. Unlike ANNs (which pass continuous real-valued activations), SNN neurons communicate through **discrete spike events** — brief electrical pulses — over time. This makes SNNs the "third generation" of neural network models.

---

## Motivation

Why SNNs over standard ANNs?

| Challenge | ANN limitation | SNN advantage |
|-----------|---------------|---------------|
| Temporal data (speech, video) | Processes fixed-size snapshots | Naturally handles time sequences via spike timing |
| Energy efficiency | Neurons always active | Sparse activation: neuron only fires when needed |
| Biological plausibility | Approximation | Close to real neural dynamics |
| Robotics (dynamic environments) | High latency | Low-latency event-driven processing |

Applications: robotics, speech recognition, sensory processing, temporal pattern recognition.

---

## Information coding in SNNs

Neurons communicate using **spikes** (action potentials). Information can be encoded as:

| Coding type | How | Example |
|------------|-----|---------|
| **Rate coding** | Spike rate (frequency) represents value | High rate = high signal |
| **Temporal coding** | Spike timing relative to others | Earlier spike = stronger signal |
| **Population coding** | Distribution across many neurons | Pattern of activity across 100 neurons |

A sequence of spikes from one neuron is called a **spike train**.

---

## Neuron dynamics: Leaky Integrate-and-Fire (LIF)

1. The neuron **accumulates charge** from incoming spikes
2. When charge exceeds a **threshold** → the neuron **fires** (emits a spike on all outgoing connections)
3. After firing → charge resets to 0
4. Below threshold → charge **leaks away** over time (the "leaky" part)

This simple model captures: threshold activation, refractory period, and temporal integration.

---

## Spike propagation

Spikes travel through the network: a fired neuron sends spikes to its post-synaptic neurons, which may integrate enough charge to fire themselves, propagating the signal through the network.

---

## Spike-Timing-Dependent Plasticity (STDP)

The key **learning rule** for SNNs — how synaptic weights are modified based on timing:

| Scenario | Effect | Name |
|----------|--------|------|
| Pre-synaptic neuron fires **before** post-synaptic | Synapse **strengthened** | Long-Term Potentiation (LTP) |
| Post-synaptic neuron fires **before** pre-synaptic | Synapse **weakened** | Long-Term Depression (LTD) |

**STDP supports unsupervised learning** — no labelled data needed. The network self-organises based on temporal correlations in its inputs.

---

## The backpropagation problem in SNNs

In standard ANNs, backpropagation requires the **derivative** of the activation function. The spiking function's derivative is the **Dirac delta**:
$$\delta(x) = 0 \text{ for all } x \neq 0, \quad \int_{-\infty}^{\infty} \delta(x) \, dx = 1$$

This has **no useful gradient information** (undefined at 0, zero everywhere else) → **backpropagation cannot be applied directly** to SNNs.

---

## Surrogate gradient approach

Replace the spiking function with a **smooth surrogate** (e.g. sigmoid) for gradient computation:
$$f(a) = \frac{1}{1 + e^{-a}}, \quad f'(a) = f(a)(1 - f(a))$$

With scaling factor $k$:
$$f_k(a) = \frac{1}{1 + e^{-ka}}, \quad \lim_{k \to \infty} f_k'(a) = \delta(a)$$

As $k$ increases, the sigmoid derivative narrows to approximate the Dirac delta. This allows **approximated backpropagation** through SNNs.

---

## Optimising SNNs with Evolutionary Algorithms

EAs offer an alternative to backpropagation (especially useful since backprop is problematic for SNNs):

**What to optimise:** network weights, delays, thresholds, architecture (structure)

**Neural Architecture Search (NAS):**
- Often formulated as **bi-level optimisation**: optimise structure (upper problem) + weights (lower problem)
- Periodically switch between optimising structure and weights

**Challenges:**
1. Evaluating SNNs is expensive (need to simulate spike dynamics) → combined with EA = very costly
2. Co-evolution: multiple aspects of the SNN optimised simultaneously

---

## SNN vs ANN comparison

| Feature | ANN | SNN |
|---------|-----|-----|
| Activation | Continuous real value | Discrete spike |
| Timing | Static (no time) | Temporal dynamics |
| Energy | High (all neurons active) | Low (sparse activation) |
| Biological plausibility | Low | High |
| Training | Backpropagation | STDP / surrogate gradients / EAs |
| Maturity | Mature (deep learning) | Emerging |
| Applicability | Vision, NLP, general ML | Temporal data, robotics, neuromorphic HW |

---

## Connections

- [[neural-networks]] — ANNs are the predecessor; SNNs are more biologically realistic
- [[neuromorphic-computing]] — SNNs are the computation model for neuromorphic hardware
- [[evolutionary-algorithms]] — EAs used for SNN architecture search and weight optimisation

---

## Exam notes

- SNNs communicate via **discrete spikes**, not continuous activations
- Three information coding methods: rate, temporal, population
- LIF neuron: accumulate → threshold → fire → reset; below threshold: leak
- STDP: pre-fires-before-post → **potentiation** (strengthen); post-fires-before-pre → **depression** (weaken)
- Backprop fails: spiking derivative = Dirac delta (no gradient) → use surrogate gradient (sigmoid)
- EAs used for: bi-level SNN optimisation (structure + weights simultaneously)
