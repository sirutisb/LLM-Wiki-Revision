# Neuromorphic Computing

**Type:** hardware/computing paradigm
**Related:** [[spiking-neural-networks]], [[neural-networks]]
**Source lectures:** [[lecture18-neuromorphic]]

---

## What it is

**Neuromorphic computing** refers to computing architectures inspired by the brain's structure and operation. The term originated in the 1980s for mixed analogue-digital implementations. Today it encompasses any brain-inspired hardware including digital spike-based processors.

---

## von Neumann vs Neuromorphic

| Feature | von Neumann | Neuromorphic |
|---------|-------------|-------------|
| Processing + memory | Separated (CPU + RAM) | Collocated (synapses store + process) |
| Instructions | Program code | Structure of synapses |
| Data encoding | Binary | Spike timing and magnitude |
| Operation model | Sequential (clock-driven) | Event-driven (spike-driven) |
| Power | High | Low |
| Bottleneck | Memory bandwidth | None (data where computation happens) |

The **von Neumann bottleneck**: in conventional computers, moving data between separated CPU and memory is a major performance and energy cost. Neuromorphic architectures eliminate this by co-locating processing and memory.

---

## Key advantages

| Advantage | Mechanism |
|-----------|---------|
| **Parallel operation** | All neurons operate simultaneously |
| **Collocated memory/processing** | Faster + lower energy than fetching from RAM |
| **Scalability** | Add chips = add neurons linearly |
| **Event-driven** | Processing only occurs when a spike arrives → zero cost when idle |

---

## Applications

| Domain | Examples |
|--------|---------|
| **Graph algorithms** | Communication routing, network analysis, graph structure analysis |
| **Optimisation** | Integer optimisation (QUBO, constraint satisfaction), continuous problems, Bayesian optimisation |
| **Neural inference** | Running SNN models at low power |
| **LASSO problem** | Optimising with a SNN simulated on Loihi (Intel's neuromorphic chip) |

---

## Example: Intel Loihi

Intel's **Loihi** chip (Davies et al., 2018) is a neuromorphic manycore processor with on-chip learning. Demonstrated advantages over conventional CPUs for:
- Solving optimisation problems (constraint satisfaction, QUBO)
- Sparse representation learning

---

## Connection to SNNs

Neuromorphic hardware is the **natural platform** for running [[spiking-neural-networks]]:
- Hardware neurons implement the Leaky-Integrate-and-Fire dynamics directly in silicon
- Spike-based communication is intrinsically low-power (event-driven, no clock overhead)
- On-chip learning rules (e.g. STDP) can update weights locally without off-chip communication

---

## Connections

- [[spiking-neural-networks]] — the computation model that neuromorphic hardware implements
- [[neural-networks]] — traditional ANNs run inefficiently on neuromorphic hardware (designed for SNNs)

---

## Exam notes

- Core idea: **collocated memory and processing** (vs. separated in von Neumann)
- Event-driven: computation only when a spike arrives → energy efficient
- Key advantage over conventional parallelism: simpler operations (spike events vs. floating-point matrices)
- Applications: graph algorithms, constraint satisfaction, sparse learning, optimal control
- Loihi (Intel) is the key commercial neuromorphic chip example
