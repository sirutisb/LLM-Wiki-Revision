# Lecture 19 — Self-Organising Maps

**File:** `raw/text/ECM3412___ECMM409_25_26 (9).txt`
**Lecturer:** Dr David Walker
**Concepts introduced:** [[self-organising-maps]]

---

## Summary

Introduces Self-Organising Maps (Kohonen networks) as an unsupervised neural network that learns topology-preserving maps from high-dimensional to low-dimensional space. Contrasts with supervised learning and MLPs.

## Key content

### Supervised vs Unsupervised Learning
- **Supervised:** given inputs + targets → find function that fits examples
- **Unsupervised:** given inputs only (no targets) → find regularities/structure in inputs

SOM = unsupervised.

### SOM goal
Learn to map points from a high-dimensional space to a low-dimensional discrete grid that **preserves topological properties**.
- Points close in original space → close map positions
- Uses: visualisation, regularity discovery in high-dimensional data

### Self-organised
Map emerges from local **competition** (which neuron best matches input) and **co-operation** (update winner's neighbours). Brain organisation analogy: functional areas (language, vision) emerge from local neural interactions.

### Working assumptions
1. Same-class data share common features
2. SOM will identify these features across many data points
3. SOM can meaningfully organise/order input data in low-dimensional structure

### SOM vs MLP
- No activation functions
- No linear combination of inputs
- No backpropagation
- Not supervised — very different from MLPs despite both being "neural networks"

## Key takeaways
- SOM = unsupervised; topology-preserving dimensionality reduction
- Training: competition (find BMU) → cooperation (neighbourhood) → adaptation (update weights)
- Fundamentally different from MLP: no backpropagation, no targets, no activation functions

## Links to concepts
- [[self-organising-maps]]: full algorithm treatment
- [[neural-networks]]: contrasted with SOMs
