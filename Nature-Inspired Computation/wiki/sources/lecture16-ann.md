# Lecture 16 — Neural Networks

**File:** `raw/text/16-ann.txt`
**Lecturer:** Dr David Walker
**Concepts introduced:** [[neural-networks]]

---

## Summary

Introduces ANNs by contrasting computers with human brains, covering biological neurons, symbolic AI vs connectionism, the perceptron, MLPs, backpropagation, and EAs as an alternative training approach. Includes a rainfall-runoff modelling case study.

## Key content

### Computers vs humans
Computers: fast serial, no mistakes, separated memory/processing, large indefinite storage.
Humans: distributed, learns, generalises, memory/processing co-located, forgets unimportant info.

Implication: computers excel at calculation; humans excel at perception, reasoning, learning.

### Brain structure
~100 billion neurons, each connected to ~10,000 others. Synapses = configurable chemical junctions = site of learning. Neurons: dendritic tree (receive), cell body (process), axon (transmit).

### Symbolic AI vs Connectionism
Symbolic: explicit rules, programmed knowledge, serial, interpretable.
Connectionism: implicit numbers, learned knowledge, distributed, black box.
Connectionism enables: perception, generalisation, noise tolerance, graceful degradation.

### McCulloch & Pitts neuron (1943)
Simple threshold unit. With threshold 1: OR gate. With threshold 2: AND gate. Cannot compute XOR (not linearly separable).

### Multi-layer Perceptron (MLP)
Rumelhardt & McClelland (1986): add hidden layer → solves XOR.
Architecture: input → hidden(s) → output. Learning = finding weights to minimise error.

**Graceful degradation:** removing neurons reduces performance but rarely causes total failure (unlike symbolic systems).
**Generalisation:** learns patterns that allow noise tolerance and recognition of novel instances.

### Backpropagation
$$w_{ij}^{(t+1)} = w_{ij}^{(t)} + \eta \delta_{pj} o_{pj}$$

Error signals:
- Output units: $\delta_{pj} = f'(o_{pj})(t_{pj} - o_{pj})$ where $f'(a) = f(a)(1-f(a))$
- Hidden units: $\delta_{pj} = f'(o_{pj}) \sum_k \delta_{pk} w_{pk}$

### Training with EAs
Each chromosome = all network weights (real vector). Fitness = mean absolute error:
$$\text{MAE} = \frac{\sum_{i=1}^{n} |y_i - t_i|}{n}$$

Additive Gaussian mutation: select one weight at random, add small Gaussian noise.

### Case study: Rainfall-runoff modelling
Single hidden layer (10 neurons) + single output neuron. Input: rainfall + air temperature. Output: predicted sewer flow. Cross-validation per rainfall event. EA-optimised weights. Evaluated with Nash-Sutcliffe Efficiency Coefficient (best = 1).

## Key takeaways
- ANNs = approximate biological neural computation; enable learning and generalisation
- Backpropagation requires differentiable activation functions
- EAs as alternative: useful when backprop inapplicable (non-differentiable activations, SNN) or for architecture search

## Links to concepts
- [[neural-networks]]: full treatment
- [[spiking-neural-networks]]: previewed at end of lecture
- [[evolutionary-algorithms]]: EAs used for ANN weight optimisation
