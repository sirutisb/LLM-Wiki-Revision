# Self-Organising Maps (SOMs)

**Type:** algorithm / model
**Related:** [[neural-networks]], [[spiking-neural-networks]]
**Source lectures:** [[lecture19-som]]

---

## What it is

A **Self-Organising Map (SOM)** (Kohonen, 1982) is an unsupervised neural network that learns to **map high-dimensional data to a low-dimensional discrete grid** while preserving topological properties. Points that are close in the original space end up near each other on the map.

---

## Supervised vs Unsupervised learning

| | Supervised | Unsupervised |
|--|-----------|-------------|
| Training data | Inputs + labelled targets | Inputs only (no targets) |
| Goal | Learn a function mapping inputs → outputs | Find regularities/structure in inputs |
| Example | Classification, regression | Clustering, dimensionality reduction |

SOM = unsupervised.

---

## Motivation

High-dimensional data (e.g. 100+ features) is hard to visualise or understand. SOM projects it onto a 2D grid in a way that preserves topology — nearby points in the original space → nearby map positions.

---

## Working assumptions

1. Input data from the same class/cluster share common features
2. The SOM will identify these features across many data points
3. The SOM will organise/order input data according to a low-dimensional structure

---

## How it works (overview)

**Structure:** a 2D grid of neurons, each with a weight vector $\mathbf{w}_i$ of the same dimension as the input data.

**Algorithm:**
```
1. Initialise all neuron weights randomly
2. For each input data point x:
   a. COMPETITION: find the "winning" neuron (Best Matching Unit, BMU)
      BMU = argmin_i ||x - w_i||
   b. COOPERATION: define a neighbourhood around the BMU
   c. ADAPTATION: update BMU and its neighbours:
      w_i += η(t) · h(i, BMU, t) · (x - w_i)
      where h is the neighbourhood function (Gaussian typically),
      η(t) is the learning rate (decreases over time)
3. Repeat until convergence
```

**Result:** the map organises so that nearby neurons respond to similar inputs (topographic organisation).

---

## SOM vs MLP (multi-layer perceptron)

| Feature | SOM | MLP |
|---------|-----|-----|
| Learning type | Unsupervised | Supervised |
| Activation functions | None | Sigmoid, ReLU, etc. |
| Input combination | No linear combination | Weighted sum |
| Training | Competitive learning | Backpropagation |
| Output | 2D map position | Class label / value |
| Purpose | Visualisation, clustering | Classification, regression |

**Key difference:** SOMs are very different from MLPs despite both being called "neural networks".

---

## Brain organisation link

The brain is naturally organised into **functional areas** — regions specialising in language, vision, motor control etc. SOMs model this self-organised spatial structure.

---

## Applications

- Visualising high-dimensional data (e.g. gene expression data)
- Discovering natural clusters
- Dimensionality reduction for preprocessing
- Anomaly detection

---

## Connections

- [[neural-networks]] — SOMs are a very different type of neural network (unsupervised, no backprop)
- [[neuromorphic-computing]] — brain's functional area organisation is analogous to SOM

---

## Exam notes

- SOM = unsupervised; learns topology-preserving map from high-D to low-D (usually 2D grid)
- Training: competition (find BMU) → cooperation (define neighbourhood) → adaptation (update weights)
- Very different from MLP: no activation functions, no backpropagation, no linear combination of inputs
- Output: a 2D grid where nearby positions correspond to similar inputs
- Inspired by the brain's topographic organisation of functional areas
