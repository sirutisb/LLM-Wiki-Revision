# Lecture 18 — Neuromorphic Computing

**File:** `raw/text/ECM3412___ECMM409_25_26 (6).txt`
**Lecturer:** Dr David Walker
**Concepts introduced:** [[neuromorphic-computing]]

---

## Summary

Introduces neuromorphic computing as a computing paradigm inspired by brain architecture. Contrasts with von Neumann architecture; describes key advantages (parallel, collocated memory/processing, event-driven, scalable) and applications in graph algorithms and optimisation.

## Key content

### Term origin
1980s: originally referred to mixed analogue-digital implementations of brain-inspired techniques. Now: broad range of brain-inspired hardware.

### von Neumann vs Neuromorphic
| Feature | von Neumann | Neuromorphic |
|---------|-------------|-------------|
| Processing + memory | Separated | Collocated in synapses |
| Instructions | Programs | Synapse structure |
| Data encoding | Binary | Spike timing/magnitude |

### Key advantages
- **Parallel operation:** all neurons operate simultaneously
- **Collocated memory/processing:** eliminates memory bandwidth bottleneck; faster and lower energy
- **Scalability:** add chips = add neurons
- **Event-driven:** processing only on spike arrival; zero power when quiet

### Applications
- Graph algorithms: routing, network analysis
- Optimisation: QUBO, constraint satisfaction, continuous problems, Bayesian optimisation
- LASSO problem solved with SNN on Loihi (Intel)

### Intel Loihi
Neuromorphic manycore processor with on-chip learning (Davies et al., IEEE Micro 2018).

## Key takeaways
- Core idea: bring memory and processing together (vs. von Neumann separation)
- Event-driven = energy-efficient; no clock overhead
- Ideal hardware platform for running SNNs at scale

## Links to concepts
- [[neuromorphic-computing]]: full treatment
- [[spiking-neural-networks]]: the computation model
