---
title: "Lecture: High Performance Computing"
type: lecture
sources: [high-performance-computing]
related: [flops, amdahls-law, moores-law, slurm, thread-level-parallelism]
updated: 2026-05-02
---

# Lecture: High Performance Computing

*Supercomputers, FLOPS scales, Moore's Law hitting its limits, Amdahl's Law bounding parallel speedup, and SLURM as the resource manager that makes clusters usable.*

## Slide-by-slide notes

- **(s. 2)** **Introduction** — HPC systems emphasise processing power, communication, and I/O. Can be distributed or non-distributed. Performance driven by: number of nodes × processors per node × cores per processor.
- **(s. 3)** **[[flops|FLOPS]]** — Floating Point Operations Per Second:
  - GFLOPS = 10⁹; TFLOPS = 10¹²; PFLOPS = 10¹⁵; EFLOPS = 10¹⁸.
  - Smartphones: 1–2 GFLOPS; Laptops: ~10 GFLOPS; Servers: 25–100 GFLOPS; GPUs: 20 GFLOPS–2 TFLOPS.
- **(s. 4)** Network performance is critical for distributed HPC — LAN (Local Area Network) latency and bandwidth are key constraints.
- **(s. 5)** **[[moores-law|Moore's Law]]** — transistor count on integrated circuits doubles approximately every two years. The industry is now lagging behind this prediction.
- **(s. 6–9)** **[[amdahls-law|Amdahl's Law]]** — predicts the theoretical speedup from parallelism:
  - S_latency = 1 / ((1 − p) + p/s)
  - p = fraction of execution time that can be parallelised; s = speedup of that fraction; (1 − p) = sequential fraction that cannot be parallelised.
  - The sequential fraction bounds the maximum speedup, regardless of how many processors you add.
  - *Example*: 10 sequential adds + 100 parallel adds. Single processor: 110 × t_add. 10 processors: 10 × t_add + 100/10 × t_add = 20 × t_add. Speedup = 5.5×.
- **(s. 10–12)** **Resource Management** — dedicated system administrators, support contracts, electricity ($10M/year). Resource management software performs:
  - Resource allocation (assigning hardware to tasks).
  - Workload scheduling.
  - Distributed workload execution and monitoring.
  - Resource types: compute nodes, processing cores, memory, storage, interconnect.
- **(s. 12)** **Jobs** — self-contained work units. Jobs are pending in queues; the queue defines execution order. Jobs can be interactive or batch. Identified by ID.
- **(s. 14–16)** **HPC relevance to data science** — big data handling, complex analytics, ML/DL training on GPU clusters, scientific simulations.
- **(s. 17)** **Key HPC aspects**: parallel computing, cluster computing, heterogeneous computing, scalability, data management.
- **(s. 18–19)** **Tools**: OpenMPI/OpenMP (parallel programming), CUDA/cuDNN (deep learning), Lustre/GPFS (parallel filesystems), SLURM/Torque (job schedulers).
- **(s. 20–26)** **[[slurm|SLURM]]** (Slurm Workload Manager):
  - Open-source, modular, scalable resource manager and scheduler for clusters.
  - **Entities**: Nodes (individual computers) → Partitions (job queues) → Jobs (resource allocations) → Job Steps (parallel tasks within a job).
  - **Node states**: Unknown → Idle, Allocated, Down, Draining, Drained, Completing.
  - **Job states**: Pending, Running, Suspended, Completing, Completed, TimeOut, NodeFail, Cancelled, Failed.
  - Scheduler assigns available nodes to highest-priority jobs in each partition.

## Key takeaways

1. **FLOPS is the currency of HPC** — know the scale (G/T/P/E) and representative benchmarks.
2. **Moore's Law is slowing** — transistor shrinkage can't keep pace, driving demand for specialised hardware and software-hardware co-design.
3. **Amdahl's Law caps parallel speedup** — the sequential fraction is the hard limit. Doubling cores on a 10% sequential workload gives at most 10× speedup, not 2× more.
4. **SLURM organises HPC workloads** — nodes → partitions → jobs → job steps; the scheduler assigns nodes to highest-priority queued jobs.
5. **HPC ≠ just scale** — resource management (SLURM), parallel programming models (OpenMP, MPI), and hardware-aware software are all required.

## Concepts introduced

- [[flops]]
- [[moores-law]]
- [[amdahls-law]]
- [[slurm]]

## Open questions / things to clarify

- s. 8–9 (Amdahl's Law diagrams) are figures — the formula and example are in s. 6–7.
- SLURM node scheduling weight and features (s. 23) are configuration details not likely to be tested.

## See also

- [[thread-level-parallelism]]
- [[software-hardware-codesign]]
- [[scalability]]
