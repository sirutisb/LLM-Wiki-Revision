---
title: "Lecture: Software-Hardware Co-design"
type: lecture
sources: [software-hardware-co-design]
related: [software-hardware-codesign, edge-computing, moores-law, tensors]
updated: 2026-05-02
---

# Lecture: Software-Hardware Co-design

*As Moore's Law slows, performance comes from designing software and hardware together — three approaches (bottom-up, top-down, co-design), the role of partitioning, and edge computing as the emerging deployment frontier.*

## Slide-by-slide notes

- **(s. 2)** **Motivation**: specialised AI/DS applications are pushing beyond what general-purpose hardware can deliver. Two impure extremes already exist: specialised software on general hardware (slow) and general software on specialised hardware (underutilised). Designing both together is expensive but necessary at scale.
- **(s. 3)** **[[software-hardware-codesign|Co-design definition]]**: to meet high-performance demands (as Moore's Law scaling slows), both hardware *and* software must be specialised to each other — hardware designed around a specific algorithm/model, software fine-tuned to that hardware's capabilities.
- **(s. 4)** **AI/ML workload characteristics**: ML models are built on tensor operations. CNNs (image processing) focus on *dense* tensors; graph-based applications (recommendation systems) work with *sparse* tensors. Specialised hardware must handle both efficiently.
- **(s. 5)** **[[edge-computing|Edge computing]]**: AI/ML is increasingly deployed on devices (personalisation requires computation near the user). This creates pressure for specialised hardware and software designed for edge constraints (power, size, latency).
- **(s. 6)** **Beyond AI/ML**: infrastructure processing units (IPUs, DPUs) for datacentre housekeeping; specialised hardware for self-driving vehicles.
- **(s. 7)** **Bottom-up design** (hardware/software): hardware designed first for a general concept → software written to exploit that hardware. Also called *platform-based design*.
- **(s. 8)** **Top-down design** (software/hardware): software workloads drive hardware architecture. *Example*: Nvidia Volta introduced tensor cores specifically designed around the needs of DNN tensor operations.
- **(s. 9)** **Co-design**: hardware and software designed together as a *coupled* process — analysed and optimised jointly.
- **(s. 10)** **Iterative process**: neither approach dominates. Demand → specialised software → new hardware → more specialised software → repeat.
- **(s. 11)** **Partitioning**: a crucial co-design step — deciding which functions go in hardware (for speed and parallelism) vs software (for flexibility and ease of updates).
- **(s. 12)** **Prototyping and simulation**: HDLs (hardware description languages) used to model hardware/software interaction before manufacturing.
- **(s. 13)** **High-level synthesis**: automated translation of a high-level behavioural specification into hardware design (HDL). Decouples algorithmic design from hardware implementation.
- **(s. 14)** **Platform-based design**: start from a predefined platform (set of hardware + software components) to reduce design time and complexity.
- **(s. 15–16)** **Advantages**: design-space exploration (wider trade-off space — power, performance, cost), optimisation at system/architectural/algorithmic levels. Applications: embedded systems, smartphones, automotive, telecommunications (5G).

## Key takeaways

1. **Three design approaches**: bottom-up (hardware first), top-down (software requirements drive hardware), co-design (designed together).
2. **Moore's Law slowdown = co-design necessity** — can no longer wait for the next chip generation.
3. **Partitioning** is the central co-design decision: what goes in hardware, what stays in software.
4. **Edge computing** is the emerging frontier — computation on devices, not in the cloud.
5. **AI/ML workloads** require different hardware for dense tensors (CNNs) vs sparse tensors (graphs).

## Concepts introduced

- [[software-hardware-codesign]]
- [[edge-computing]]

## Open questions / things to clarify

- Specific hardware examples (tensor cores, TPUs) mentioned but not deeply analysed in the slides.

## See also

- [[moores-law]]
- [[tensors]]
- [[sparse-tensors]]
- [[high-performance-computing]]
