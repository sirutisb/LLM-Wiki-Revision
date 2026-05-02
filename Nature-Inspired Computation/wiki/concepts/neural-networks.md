# Artificial Neural Networks (ANNs)

**Type:** algorithm / model
**Related:** [[spiking-neural-networks]], [[neuromorphic-computing]], [[self-organising-maps]], [[evolutionary-algorithms]]
**Source lectures:** [[lecture16-ann]]

---

## What it is

An **Artificial Neural Network (ANN)** is a computational model loosely inspired by the brain's neural architecture. It learns to map input data to desired outputs by adjusting the **weights** of connections between artificial neurons. ANNs are particularly effective for tasks computers struggle with: perception, recognition, generalisation.

---

## Motivation: brains vs computers

| Computer | Human Brain |
|---------|-------------|
| Fast serial processing | Slow but massively parallel |
| Memory and processing separated | Distributed architecture |
| Precise arithmetic | Approximate but generalisable |
| Doesn't forget (hard disk) | Forgets unimportant information |
| Fragile to component removal | Graceful degradation |
| Cannot generalise beyond scope | Generalises to novel situations |

Brain: ~100 billion neurons, each connected to ~10,000 others via synapses.

---

## Biological neuron

| Part | Function |
|------|---------|
| **Dendritic tree** | Receives input signals from other neurons |
| **Cell body (soma)** | Processes incoming signals |
| **Axon** | Transmits output signal to other neurons |
| **Synapse** | Configurable chemical junction — site of learning |

Synapses can **excite** (strengthen signal) or **inhibit** (weaken signal) the post-synaptic neuron.

---

## Symbolic AI vs Connectionism

| | Symbolic AI | Connectionism (ANN) |
|--|-------------|---------------------|
| Reasoning | Explicit (symbols, rules) | Implicit (numbers, weights) |
| System | Expert system (IF-THEN) | Neural network (weighted graph) |
| Knowledge | Programmed | Learned from data |
| Architecture | Serial (fragile) | Distributed (graceful degradation) |
| Scope | Does not generalise | Generalises |
| Interpretability | Interpretable | Black box |

---

## Artificial neuron (McCulloch & Pitts, 1943)

Simple threshold unit: fires if weighted sum of inputs ≥ threshold.
- With threshold 1 and two binary inputs: implements **OR gate**
- With threshold 2 and two binary inputs: implements **AND gate**

**XOR problem:** cannot be solved with a single neuron (not linearly separable).

---

## Multi-layer Perceptron (MLP)

Rumelhardt & McClelland (1986): adding a **hidden layer** solves XOR.

Architecture:
```
Input layer → Hidden layer(s) → Output layer
```
Connections between layers are **weighted**. Learning = finding weights that minimise prediction error.

**Properties:**
- Learns to relate inputs to outputs
- Generalises to unseen examples
- Noise tolerant
- Graceful degradation: remove some neurons → reduced performance, rarely total failure

---

## Training: Backpropagation

Adjust weights to minimise error by propagating error signal backwards from output to input:

**Weight update rule:**
$$w_{ij}^{(t+1)} = w_{ij}^{(t)} + \eta \delta_{pj} o_{pj}$$

where:
- $\eta$ = learning rate
- $\delta_{pj}$ = error signal for node $j$ on pattern $p$
- $o_{pj}$ = output of node $j$ on pattern $p$

**Error computation:**
- **Output units:** $\delta_{pj} = z \cdot o_{pj}(1 - o_{pj})(t_{pj} - o_{pj})$ where $t_{pj}$ is target
- **Hidden units:** $\delta_{pj} = z \cdot o_{pj}(1 - o_{pj}) \sum_k \delta_{pk} w_{pk}$ (backpropagate from layer above)
- $z = f'(a) = f(a)(1 - f(a))$ = derivative of sigmoid activation

---

## Training ANNs with Evolutionary Algorithms

Alternative to backpropagation: use an EA to optimise the weights.

**Encoding:** Each chromosome = all network weights as a real vector.

**Fitness:** Network accuracy on training data, e.g. Mean Absolute Error:
$$\text{MAE} = \frac{\sum_{i=1}^{n} |y_i - t_i|}{n}$$

**Variation:** Additive Gaussian mutation — select weight at random, add small Gaussian noise.

**When EA preferred over backpropagation:**
- Non-differentiable activation functions
- Architecture search (evolving structure as well as weights)
- Noisy or incomplete training data
- Multi-objective weight optimisation

---

## Applications

- Predict fuel consumption from car attributes
- Rainfall-runoff modelling for flood prediction
- Cancer classification from blood values
- Image classification (faces, objects)
- Stock market prediction

---

## Connections

- [[spiking-neural-networks]] — more biologically realistic ANN variant
- [[self-organising-maps]] — unsupervised neural network
- [[evolutionary-algorithms]] — EAs used to train ANN weights (neuroevolution)
- [[neuromorphic-computing]] — hardware implementation of neural computation

---

## Exam notes

- McCulloch & Pitts (1943): first artificial neuron; XOR not solvable without hidden layer
- MLP solves XOR by adding a hidden layer — Rumelhardt & McClelland (1986)
- Backpropagation: output error → propagate back; weights updated via $\Delta w_{ij} = \eta \delta_{pj} o_{pj}$
- Sigmoid derivative: $f'(a) = f(a)(1-f(a))$ — needed for the chain rule in backprop
- EAs as alternative to backprop: each chromosome = weight vector; fitness = MAE or similar
- Graceful degradation: removing neurons reduces performance but usually does not cause total failure
- Connectionism vs symbolic AI: know the comparison table cold
