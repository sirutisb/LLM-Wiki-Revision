---
title: "Software-hardware co-design"
type: concept
sources: [software-hardware-co-design]
related: [edge-computing, moores-law, tensors, sparse-tensors]
updated: 2026-05-02
---

# Software-hardware co-design

*Designing hardware and software as a coupled, iterative process — each shapes the other — to achieve performance that neither general-purpose hardware nor general-purpose software can deliver alone.*

## Definition

**Software-hardware co-design** is the practice of designing hardware and software jointly and iteratively, so that each is optimised with respect to the other. Rather than designing a chip and then writing software for it, or writing software and hoping hardware keeps up, co-design analyses the full system together.

## Why it matters

As [[moores-law|Moore's Law]] slows, the "free" performance improvements from denser transistors are disappearing. The only path to continued performance growth for AI/ML workloads is specialisation — both the silicon and the algorithms must be shaped to each other.

## Three design approaches

| Approach | Starting point | Advantage | Weakness |
|---|---|---|---|
| **Bottom-up** (platform-based) | Hardware designed first | Stable hardware target | Software may not fully exploit capabilities |
| **Top-down** | Software requirements drive hardware | Hardware matches workload | Hardware changes are expensive |
| **Co-design** | Both designed together | Optimal joint solution | Most complex; requires cross-domain teams |

Example of top-down: Nvidia Volta tensor cores were designed specifically for the matrix multiply operations in DNN training.

## Partitioning — the core decision

A crucial step is **partitioning**: deciding which functions run in hardware (for speed and parallelism) and which stay in software (for flexibility and updateability).

```
Hardware: fixed, fast, parallel   → compute-intensive inner loops
Software: flexible, updatable     → control logic, hyperparameters
```

## Iterative cycle

```
Demand for performance
    ↓
Specialised software (algorithms tuned to workload)
    ↓
Drives need for specialised hardware
    ↓
New hardware enables further software optimisation
    ↓
(repeat)
```

## Edge computing context

AI/ML models are becoming personalised. Processing must move to the **device** rather than the cloud — reduced latency, privacy, offline capability. This creates demand for specialised low-power co-designed chips (NPUs in smartphones, edge accelerators).

## Examples in the syllabus

- Software-hardware co-design s. 3–10: the three approaches and iterative cycle.
- s. 11: partitioning as the crucial co-design step.

## Common exam framing

- "Distinguish top-down, bottom-up, and co-design approaches to hardware-software development."
- "What is partitioning in the context of co-design?"
- "Why does the slowdown of Moore's Law make co-design increasingly important?"

## See also

- [[moores-law]]
- [[edge-computing]]
- [[tensors]]
