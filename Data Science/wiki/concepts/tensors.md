---
title: "Tensors"
type: concept
sources: [tensor, review]
related: [sparse-tensors, software-hardware-codesign]
updated: 2026-05-02
---

# Tensors

*The universal representation of multi-dimensional data in machine learning — scalars, vectors, and matrices are all tensors of order 0, 1, and 2 respectively.*

## Definition

A **tensor** is a multi-dimensional array of numerical values. The *order* (or rank) of a tensor is the number of dimensions:

| Order | Name | Shape | Example |
|---|---|---|---|
| 0 | Scalar | () | A single temperature reading |
| 1 | Vector | (n,) | Feature vector for one sample |
| 2 | Matrix | (m, n) | Dataset (rows = samples, cols = features) |
| 3+ | Tensor | (d₁, d₂, ..., dₖ) | Image, video, higher-order data |

## Real-world data shapes

| Data type | Tensor shape |
|---|---|
| Feature vector | features |
| Time series | features × timestamps |
| Grayscale image | width × height |
| Colour image | width × height × channels (3 for RGB) |
| Video | frames × width × height × channels |

## Why it matters

Neural networks are fundamentally tensor operations — weights are matrices, activations are vectors or higher-order tensors, and batch training operates on batches of examples stacked as a tensor. The hardware (GPUs, TPUs, tensor cores) is designed specifically around efficient tensor operations.

## Dense vs sparse tensors

See [[sparse-tensors]] for the full treatment. In brief: when most values are zero, storing the full tensor wastes memory. A 10⁶ × 10⁶ dense float64 matrix requires ~58 GB; the same sparse matrix with only n non-zeros needs O(n) space.

## Examples in the syllabus

- Tensor lecture s. 2–3: orders defined; data shapes listed.
- Review s. 28–32: tensors and sparse representations called out as exam-relevant.

## Common exam framing

- "What is the order of a tensor representing a colour video?"
- "Give the tensor shape for a batch of 32 colour images of size 224×224."

## See also

- [[sparse-tensors]]
- [[software-hardware-codesign]]
