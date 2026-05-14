---
title: "Week 1 Practice Questions: Introduction to HPC"
tags: [hpc, week-1, practice]
date: 2026-05-14
---

# Week 1 Practice Questions: Introduction to HPC

**Scope:** HPC definition and applications, FLOP/s and performance metrics, HPL and HPCG benchmarks, Top500 list, peak performance calculation, Moore's Law, Dennard Scaling, why parallelism is mandatory, cluster architecture (compute nodes, login nodes, storage, interconnects, MPPs), and HPC programming languages (C, C++, Fortran, OpenMP, MPI).

**Exam format note:** Questions are styled on the actual ECM3446 exam pattern (2023–2025). Calculation questions allow a non-programmable scientific calculator. Model answers are written to the level of detail an examiner expects — if a question is worth 2 marks, your real answer needs at least 2 distinct correct points.

---

## Section A: Short Answer / Definition

### Q1 — Define HPC *(2 marks)*

Define "High Performance Computing (HPC)". Give one example of an application domain where HPC is essential.

> **Model Answer:**
>
> HPC involves **aggregating computing power in a way that delivers performance far beyond that of a typical desktop or workstation**, used to solve large-scale problems in science, engineering, or business. (1 mark)
>
> Example application domains (any one): Computational Fluid Dynamics (CFD), weather forecasting / climate modelling (e.g. Met Office), astrophysics (e.g. galaxy formation simulations), genomics/bioinformatics. (1 mark)

---

### Q2 — What is a FLOP/s? *(2 marks)*

What does the unit **flop/s** measure? State the typical order of magnitude achieved by the world's fastest HPC systems.

> **Model Answer:**
>
> A **flop/s** (floating-point operations per second) measures the number of floating-point arithmetic operations a system can perform every second. It is the primary unit of HPC performance. (1 mark)
>
> The world's fastest systems achieve **10s to 100s of petaflop/s** ($10^{16}$–$10^{17}$ flop/s); as of 2023 the leading machine (Frontier) exceeded 1 exaflop/s ($10^{18}$ flop/s). (1 mark)

---

### Q3 — HPL benchmark *(2 marks)*

What is the **High-Performance Linpack (HPL)** benchmark, and what does it measure?

> **Model Answer:**
>
> HPL solves a **dense system of linear equations** $Ax = b$ using **LU factorisation** on a dense matrix. It measures sustained **floating-point performance in flop/s** ($R_{max}$). It is the ranking benchmark for the Top500 list. (2 marks — need: dense linear system + LU factorisation + flop/s metric)

---

### Q4 — State Moore's Law *(2 marks)*

State Moore's Law as originally formulated by Gordon Moore. Is it still valid today?

> **Model Answer:**
>
> Moore's Law states: "**the number of transistors incorporated in a chip will approximately double every 24 months**". (1 mark)
>
> It remains **partially valid** — transistor density continues to increase, though progress is slowing. However, we now get more *cores* per chip rather than faster individual cores. (1 mark)

---

### Q5 — Define Dennard Scaling *(3 marks)*

Define Dennard Scaling and state its current status. Explain the consequence for HPC.

> **Model Answer:**
>
> Dennard Scaling is the rule that **power density (power per unit area) stays constant as transistors shrink** — smaller transistors run faster *and* consume less energy per unit area. (1 mark)
>
> Dennard scaling **broke down in the mid-2000s** due to physical limits (leakage current, gate-oxide thickness). As a result, **processor clock frequencies have stalled at approximately 2–4 GHz** since ~2005 — further frequency increases would produce heat that cannot be dissipated. (1 mark)
>
> Consequence for HPC: single-core performance can no longer increase through clock speed alone; instead, **parallel programming is required** to exploit the additional cores that Moore's Law continues to deliver. (1 mark)

---

### Q6 — What is the Top500 list? *(3 marks)*

Describe the Top500 list: what it ranks, how often it is published, and what benchmark it uses.

> **Model Answer:**
>
> The **Top500 list** is a ranking of the **500 fastest known supercomputers in the world**. (1 mark)
>
> It is **published twice a year** (typically June and November). (1 mark)
>
> Systems are ranked by their measured **HPL (High-Performance Linpack)** performance, $R_{max}$, in flop/s. It also reports $R_{peak}$ (theoretical maximum). It has been running since the mid-1990s, providing a long-term dataset of global HPC trends. (1 mark)

---

### Q7 — Define peak performance ($R_{peak}$) *(3 marks)*

Write down the formula for the theoretical peak performance ($R_{peak}$) of a compute node. Define each symbol.

> **Model Answer:**
>
> $$R_{peak} = N_{sockets} \times N_{cores/socket} \times R_{clock} \times N_{ops/cycle}$$
>
> Where:
> - $N_{sockets}$ — number of processor sockets per node
> - $N_{cores/socket}$ — number of CPU cores per socket
> - $R_{clock}$ — processor clock frequency (Hz or GHz)
> - $N_{ops/cycle}$ — floating-point operations a core can execute per clock cycle (depends on vector instruction width and whether FMA is supported)
>
> Multiply a single node's $R_{peak}$ by the total number of compute nodes to get the cluster peak.

---

### Q8 — Compiled languages in HPC *(2 marks)*

Why does HPC predominantly use **compiled languages** rather than interpreted languages? Name the three dominant compiled languages in HPC.

> **Model Answer:**
>
> Compiled languages produce a machine-code executable **ahead of time**, allowing the compiler to perform optimisations (loop unrolling, vectorisation, inlining) that would be too costly to perform at runtime by an interpreter. This gives much higher sustained performance. (1 mark)
>
> The three dominant compiled languages in HPC are **C, C++, and Fortran**. (1 mark — need all three)

---

### Q9 — Commodity cluster components *(4 marks)*

List and briefly describe the **four main components** of a commodity HPC cluster.

> **Model Answer:**
>
> 1. **Compute nodes** — Provide the processor cores and memory needed to run computational workloads (e.g. dual-socket Intel x86 nodes with multiple cores per socket). (1 mark)
> 2. **Interconnect** — The internal high-speed network that allows nodes to communicate and access storage; uses scalable architectures (e.g. fat-tree topology) and high-performance hardware (e.g. Infiniband). (1 mark)
> 3. **Mass storage** — Disk arrays (RAID) and storage nodes providing a shared, parallel user filesystem (e.g. GPFS / Lustre). (1 mark)
> 4. **Login nodes** — Provide external user access via SSH and manage queue submission (scheduler) to the compute nodes. Users compile and test code here but do not run production jobs directly. (1 mark)

---

### Q10 — OpenMP vs MPI: one-line distinction *(2 marks)*

In one sentence each, state what **OpenMP** is used for and what **MPI** is used for in HPC.

> **Model Answer:**
>
> **OpenMP** is a directives-based parallel programming API for **shared-memory** systems, adding thread-level parallelism to C, C++, or Fortran code via compiler pragmas. (1 mark)
>
> **MPI (Message Passing Interface)** is a library-based standard for **distributed-memory** parallel programming, using explicit function calls to pass messages between processes across nodes of a cluster. (1 mark)

---

## Section B: Calculations / Quantitative

### Q11 — Peak performance calculation *(5 marks)*

A compute node has the following specification:

- Number of sockets: 2
- Cores per socket: 32
- Clock frequency: 3.0 GHz
- Floating-point operations per cycle: 8

A cluster contains 200 of these compute nodes.

**(a)** Calculate the peak performance ($R_{peak}$) of a **single compute node** in GFlop/s. Show your working.

**(b)** Calculate the peak performance of the **entire cluster** in TFlop/s.

> **Model Answer:**
>
> **(a)** Using $R_{peak} = N_{sockets} \times N_{cores/socket} \times R_{clock} \times N_{ops/cycle}$:
>
> $$R_{peak} = 2 \times 32 \times 3.0 \times 10^9 \times 8 = 1536 \times 10^9 \text{ flop/s} = \mathbf{1536 \text{ GFlop/s}}$$
>
> (3 marks — formula applied correctly, arithmetic correct, correct unit)
>
> **(b)** Cluster peak:
>
> $$R_{peak,cluster} = 1536 \text{ GFlop/s} \times 200 = 307\,200 \text{ GFlop/s} = \mathbf{307.2 \text{ TFlop/s}}$$
>
> (2 marks — multiply correctly by node count, convert to TFlop/s)

---

### Q12 — Linpack efficiency and peak core performance *(5 marks)*

A supercomputer has the following Top500 data:

| Field | Value |
|---|---|
| Cores | 786,432 |
| Processor | Custom 1.6 GHz |
| Rmax (Linpack) | 8,586.61 TFlop/s |
| Rpeak | 10,066.33 TFlop/s |

**(a)** Calculate the **Linpack efficiency** of this system. Show your working. *(2 marks)*

**(b)** Calculate the theoretical peak performance of a **single processor core**. Show your working. *(2 marks)*

**(c)** Using the clock frequency, determine how many **floating-point operations per cycle** each core can perform. *(1 mark)*

> **Model Answer:**
>
> **(a)** Linpack efficiency:
>
> $$\eta = \frac{R_{max}}{R_{peak}} = \frac{8586.61}{10066.33} = \mathbf{0.853 = 85.3\%}$$
>
> **(b)** Per-core peak:
>
> $$R_{peak,core} = \frac{10\,066.33 \times 10^{12}}{786\,432} \approx 1.28 \times 10^{10} \text{ flop/s} \approx \mathbf{12.8 \text{ GFlop/s}}$$
>
> **(c)** Ops per cycle:
>
> $$N_{ops/cycle} = \frac{12.8 \times 10^9}{1.6 \times 10^9} = \mathbf{8 \text{ ops/cycle}}$$
>
> This is consistent with a 4-wide double-precision SIMD unit with FMA ($4 \times 2 = 8$).

---

### Q13 — Choosing between two node types *(6 marks)*

You must choose between two compute node specifications (same cost):

| | Node Type 1 | Node Type 2 |
|---|---|---|
| Sockets | 2 | 2 |
| Cores per socket | 64 | 28 |
| Clock frequency | 2.2 GHz | 2.8 GHz |
| Ops per cycle | 4 | 16 |

**(a)** Calculate $R_{peak}$ for each node type in GFlop/s. Which has the higher peak? *(4 marks)*

**(b)** Your application **cannot use vector instructions or FMA** (effectively 1 op/cycle per core). Which node type would you now recommend, and why? *(2 marks)*

> **Model Answer:**
>
> **(a)**
>
> Type 1: $R_{peak} = 2 \times 64 \times 2.2 \times 10^9 \times 4 = \mathbf{1126.4 \text{ GFlop/s}}$
>
> Type 2: $R_{peak} = 2 \times 28 \times 2.8 \times 10^9 \times 16 = \mathbf{2508.8 \text{ GFlop/s}}$
>
> **Type 2 has the higher theoretical peak** (approximately 2.23× Type 1). (2 marks for both calculations correct, 1 mark for identifying Type 2 as higher, 1 mark for units)
>
> **(b)** If the application issues only scalar (non-vector, non-FMA) instructions, the effective ops/cycle collapses to ~1 for both nodes. The comparison then reduces to:
>
> - Type 1 effective: $2 \times 64 \times 2.2\ \text{GHz} = 281.6\ \text{GFlop/s (scalar)}$
> - Type 2 effective: $2 \times 28 \times 2.8\ \text{GHz} = 156.8\ \text{GFlop/s (scalar)}$
>
> **Recommend Type 1** — it has more cores per node, which matters more than clock speed when vector instructions cannot be used. (1 mark for recommendation, 1 mark for clear reasoning about why ops/cycle advantage disappears)

---

### Q14 — Frontier peak performance derivation *(4 marks)*

The June 2023 Top500 list shows **Frontier** with:

- Total cores: 8,699,904
- Processor: AMD EPYC 64C 2 GHz
- $R_{peak}$: 1,679.82 PFlop/s
- $R_{max}$ (Linpack): 1,194.00 PFlop/s

**(a)** Calculate Frontier's Linpack efficiency. *(2 marks)*

**(b)** Calculate the per-core $R_{peak}$ in GFlop/s and verify the implied ops/cycle is plausible for a modern CPU. *(2 marks)*

> **Model Answer:**
>
> **(a)** $\eta = \frac{1194.00}{1679.82} = \mathbf{0.711 = 71.1\%}$
>
> **(b)** Per-core: $R_{peak,core} = \frac{1679.82 \times 10^{15}}{8\,699\,904} \approx 1.931 \times 10^{11}\ \text{flop/s} \approx \mathbf{193\ \text{GFlop/s}}$
>
> Implied ops/cycle: $193 \times 10^9 / (2 \times 10^9) \approx 96\ \text{ops/cycle}$.
>
> This is plausible for a modern AMD EPYC — using 512-bit AVX-2 vector units with FMA, processing multiple FP64 values per cycle across wide issue ports, the per-core peak can reach this level.

---

## Section C: Explain and Describe

### Q15 — Why can't we just get a faster processor? *(8 marks)*

A researcher says: *"Moore's Law is still going. Why can't I just buy a much faster processor and run my serial program quicker?"*

Explain clearly why the researcher has misunderstood Moore's Law, and why parallel programming is now the only path to higher single-program performance.

> **Model Answer:**
>
> The researcher is confusing **Moore's Law** (a statement about transistor density) with **clock-frequency scaling** (a separate phenomenon that has stopped):
>
> **Moore's Law (still progressing, slowly):**
> Moore's Law states that transistor count doubles approximately every two years. This buys *more transistors* per chip — but the semiconductor industry now uses those transistors to add **more cores per chip**, not to make individual cores faster. (2 marks)
>
> **Dennard Scaling (broken since mid-2000s):**
> Dennard scaling was the property that as transistors shrank, they became faster *and* more energy-efficient, keeping power density constant. Physical limits (leakage current, finite gate-oxide thickness) caused this to break down. Pushing frequencies higher would push power and heat past what cooling systems can remove — the so-called **power wall**. (2 marks)
>
> **Consequence — frequencies are stalled:**
> Clock speeds have been stuck around 2–4 GHz since approximately 2005. Small single-core performance improvements still occur (wider vector units, better branch prediction, larger caches), but these are not the order-of-magnitude gains seen in the 1990s. The researcher cannot buy a chip that is, say, 10× faster in clock speed. (2 marks)
>
> **Implication — only parallelism scales:**
> Modern chips have many cores (e.g. 64 per socket) because Moore's Law continues to provide transistors. A serial program uses exactly one core and leaves all others idle — it cannot benefit from the additional hardware. To use the hardware that Moore's Law delivers, programs must be **parallelised**. (2 marks)

---

### Q16 — Describe the HPL benchmark workload and explain why it differs from real applications *(6 marks)*

Explain what workload the HPL benchmark uses and why real-world HPC applications typically achieve **much lower performance** than their HPL $R_{max}$ scores suggest.

> **Model Answer:**
>
> **What HPL measures:**
> HPL solves a dense system of linear equations $Ax = b$ via LU factorisation. It is a BLAS Level 3 (dense matrix-matrix) operation with **high arithmetic intensity** (approximately $O(N)$ FLOPs per byte) — it is heavily **compute-bound**, achieving a high fraction of $R_{peak}$. (2 marks)
>
> **Why real applications underperform:**
>
> 1. **Low arithmetic intensity:** Most real codes (sparse solvers, finite-difference stencils, graph algorithms) perform $O(1)$ FLOPs per byte — they are **memory-bandwidth-bound**, never reaching $R_{peak}$ no matter how many FP cores exist. (1 mark)
> 2. **No vectorisation:** HPL uses the widest available AVX vector instructions with FMA. Many legacy or unoptimised codes cannot exploit these, collapsing effective ops/cycle to 1. (1 mark)
> 3. **Communication overhead:** HPL is carefully tuned to overlap MPI communication with computation. Real applications often stall on halo exchanges, collectives, and load imbalance. (1 mark)
> 4. **Cache efficiency:** HPL applies cache blocking to keep operands in L1/L2. Real applications with irregular access patterns spend far more time waiting on DRAM. (1 mark)
>
> The HPCG benchmark was introduced specifically to complement HPL — it solves a sparse problem and reports performance 1–2 orders of magnitude lower than HPL on the same hardware, better representing real application behaviour.

---

### Q17 — Commodity cluster vs MPP *(4 marks)*

Explain the difference between a **commodity cluster** and a **Massively Parallel Processing (MPP)** system. Give one advantage and one disadvantage of each.

> **Model Answer:**
>
> **Commodity cluster:**
> Built entirely from **commercial off-the-shelf (OTS)** components — standard x86 processors, standard Infiniband or Ethernet interconnects, standard storage arrays. Both compute nodes and network are independently procurable products.
>
> - *Advantage:* Cost-effective; components are widely available and cheaper; easier to procure and replace. (1 mark)
> - *Disadvantage:* Performance ceiling limited by commercial network latency/bandwidth; cannot match the tightly-coupled performance of a purpose-built MPP. (1 mark)
>
> **MPP (e.g. Fugaku, IBM BlueGene):**
> Combines many multi-core processors like a cluster but uses **specialist hardware** — custom interconnects, custom processors — rather than off-the-shelf parts.
>
> - *Advantage:* Achieves higher peak performance and lower communication latency through custom network design; can reach the top of the Top500. (1 mark)
> - *Disadvantage:* Far more expensive to procure and maintain; less flexible; custom components not readily replaceable. (1 mark)

---

### Q18 — Why is Fortran still used in HPC? *(3 marks)*

Despite being one of the oldest high-level programming languages, Fortran remains widely used in HPC. Give **three reasons** that explain why.

> **Model Answer:**
>
> 1. **Legacy codebases:** Many major HPC libraries and scientific codes (e.g. weather models, fluid dynamics solvers) were written in Fortran over decades. Rewriting them would cost enormous effort for uncertain gain. (1 mark)
> 2. **Compiler optimisation:** Fortran's language rules (e.g. no pointer aliasing by default) make it easier for compilers to auto-vectorise and optimise array operations aggressively. (1 mark)
> 3. **Array syntax and performance:** Fortran has native multi-dimensional array syntax and column-major memory layout well-suited to dense matrix operations; modern Fortran (90/95/2003) supports parallelism extensions. (1 mark)

---

### Q19 — Explain the role of login nodes in an HPC cluster *(3 marks)*

Explain the purpose of **login nodes** in an HPC cluster. What can and cannot be done on them?

> **Model Answer:**
>
> Login nodes provide **external user access** to the HPC cluster via SSH (Secure Shell). They are the entry point users interact with directly. (1 mark)
>
> **What users do on login nodes:** compile code, edit source files, write job scripts, submit jobs to the batch scheduler (e.g. SLURM/PBS), monitor queued jobs, and perform small-scale interactive testing. (1 mark)
>
> **What should not be done on login nodes:** run production computations or memory-intensive workloads. Login nodes are shared between all users simultaneously; running large jobs on them degrades the experience for everyone. All production work must be submitted via the job scheduler to the compute nodes. (1 mark)

---

## Section D: Multi-Part Exam Questions

### Q20 — Top500 and system classification *(12 marks)*

The following information is taken from the Top500 website for a system called **Mira** (June 2012):

| Field | Value |
|---|---|
| Manufacturer | IBM |
| Cores | 786,432 |
| Processor | Power BQC 16C 1.6 GHz |
| Interconnect | Custom Interconnect |
| Rmax | 8,586.61 TFlop/s |
| Rpeak | 10,066.33 TFlop/s |
| HPCG performance | 167.049 TFlop/s |
| Power consumption | 3,945.00 kW |
| OS | Linux |

**(a)** What benchmark is used to rank systems on the Top500 list and what does it measure? *(2 marks)*

**(b)** Calculate the Linpack efficiency of Mira. *(2 marks)*

**(c)** Calculate the theoretical peak performance of a single processor core on Mira. *(2 marks)*

**(d)** Based on the information in the table, would you classify Mira as a commodity cluster or an MPP? Justify your answer. *(3 marks)*

**(e)** Mira's HPCG performance is 167 TFlop/s while its HPL performance is 8,587 TFlop/s — a ratio of roughly 1:51. Explain why HPCG performance is so much lower. *(3 marks)*

> **Model Answer:**
>
> **(a)** The **High-Performance Linpack (HPL)** benchmark. It measures the sustained floating-point performance (in flop/s) achieved when solving a dense system of linear equations $Ax = b$ via LU factorisation. (2 marks)
>
> **(b)** $\eta = \frac{R_{max}}{R_{peak}} = \frac{8586.61}{10066.33} = 0.853 = \mathbf{85.3\%}$ (2 marks)
>
> **(c)** $R_{peak,core} = \frac{10\,066.33 \times 10^{12}}{786\,432} \approx 1.28 \times 10^{10}\ \text{flop/s} = \mathbf{12.8\ \text{GFlop/s per core}}$ (2 marks)
>
> **(d)** Mira is an **MPP (Massively Parallel Processor)**. The key indicator is the **"Custom Interconnect"** — a commodity cluster uses off-the-shelf networking (Infiniband or Ethernet), not custom hardware. Additionally, the IBM Power BQC processor is a custom chip (BlueGene/Q), not a standard x86 commodity part. Both the network and processor are specialist components, not commercially available off-the-shelf products. (3 marks: classify correctly + at least 2 supporting reasons)
>
> **(e)** HPCG solves a **sparse linear problem** (3D Poisson equation with a 27-point stencil) that performs $O(1)$ floating-point operations per byte transferred from memory — it is **memory-bandwidth-bound**. HPL performs $O(N)$ FLOPs per byte (dense matrix, compute-bound). On any real system, the memory bandwidth is orders of magnitude below what would be needed to feed the FP units at $R_{peak}$, so memory-bound workloads like HPCG are limited by bandwidth and achieve only a small fraction of HPL performance. The gap reflects the real performance bottleneck (memory, not FLOPs) that HPL conceals. (3 marks: sparse vs dense, memory-bound vs compute-bound, bandwidth bottleneck)

---

### Q21 — Moore's Law, Dennard Scaling, and the programming implications *(10 marks)*

**(a)** State Moore's Law and Dennard Scaling. For each, state whether it still holds today and the reason for your answer. *(4 marks)*

**(b)** Explain why the end of Dennard Scaling means that clock speeds can no longer increase. *(2 marks)*

**(c)** A researcher claims: "Since transistor counts are still doubling, I can expect my single-threaded program to run twice as fast every two years." Explain the flaw in this reasoning. *(2 marks)*

**(d)** What does this mean for HPC programmers? Give two specific implications. *(2 marks)*

> **Model Answer:**
>
> **(a)**
>
> - **Moore's Law:** the number of transistors on a chip doubles approximately every 24 months. **Still holds (partially)** — transistor counts continue to increase, though the doubling rate has slowed from 24 to ~36 months. (1 mark)
> - **Dennard Scaling:** as transistors shrink, power density stays constant — smaller transistors are faster *and* more power-efficient. **No longer holds** — broke down in the mid-2000s because of leakage currents at very small feature sizes, removing the relationship between transistor size and energy efficiency. (1 mark for each, 2 marks total)
>
> **(b)** When Dennard Scaling held, shrinking transistors also lowered threshold voltages, so frequency could increase without increasing power consumption. With Dennard Scaling broken, increasing clock frequency raises power consumption and heat proportionally. At frequencies above ~4 GHz, power dissipation exceeds what air-cooling systems can remove, creating a **power/thermal wall**. Chip manufacturers therefore fixed frequencies and instead spent transistor budgets on adding more cores. (2 marks)
>
> **(c)** The flaw: additional transistors are now used to add **more processor cores**, not to make existing cores faster. A single-threaded program uses exactly one core regardless of how many cores the chip has. It cannot benefit from additional cores — it will not run faster as transistor count doubles. The researcher's reasoning held in the era of Dennard Scaling (when more transistors → higher frequency → faster single-thread performance) but not today. (2 marks)
>
> **(d)** Implications for HPC programmers:
> 1. **Parallelism is mandatory:** to make a program run faster on modern hardware, it must be written to use multiple cores simultaneously, via OpenMP, MPI, or a combination. (1 mark)
> 2. **Single-core performance is largely fixed:** optimisation must focus on how well code exploits the available cores, cache hierarchy, and vector instruction sets — not on expecting hardware clock improvements. (1 mark)

---

### Q22 — Cluster architecture design question *(9 marks)*

You are designing an HPC cluster for a university research group. The group will run computational fluid dynamics simulations that require large amounts of memory and cross-node communication.

**(a)** Identify and describe the **four main hardware components** the cluster must include, and state the key performance characteristic most important for each. *(8 marks)*

**(b)** Should you choose a commodity cluster or an MPP architecture? Justify your choice with reference to cost and performance. *(1 mark)*

> **Model Answer:**
>
> **(a)**
>
> 1. **Compute nodes** — House the CPUs (and optionally GPUs), memory, and local disk. Key characteristic: **high core count and large per-node memory** (CFD simulations often require tens to hundreds of GB RAM per node). Multi-socket nodes (e.g. 2-socket with 32 cores each) offer both. (2 marks)
>
> 2. **High-speed interconnect** — The internal network over which MPI processes exchange halo data. Key characteristic: **low latency and high bandwidth** (Infiniband is typical; fat-tree topology provides good bisection bandwidth). CFD simulations with domain decomposition are sensitive to communication latency per halo exchange. (2 marks)
>
> 3. **Mass storage / parallel filesystem** — Disk arrays and storage nodes providing a shared filesystem all compute nodes can access simultaneously. Key characteristic: **high aggregate I/O bandwidth** (parallel filesystems such as Lustre or GPFS allow many nodes to read/write simultaneously without bottlenecking). CFD codes write large checkpoint files and read mesh data. (2 marks)
>
> 4. **Login nodes** — The entry point for users: SSH access, compilation, and job submission. Key characteristic: **availability and network connectivity** (users must be able to submit jobs and monitor them at all times; the login node does not need extreme compute power). (2 marks)
>
> **(b)** For a university research group, a **commodity cluster** is the appropriate choice. Off-the-shelf components (x86 nodes, Infiniband) deliver good performance at much lower cost, making it affordable within a typical research budget. An MPP would deliver higher peak performance but at a cost that far exceeds what a university group can justify for general research workloads. (1 mark)

---

## Section E: Compare and Contrast

### Q23 — Compare OpenMP and MPI *(8 marks)*

Complete the comparison table below and use it to discuss when you would choose each technology.

| Characteristic | OpenMP | MPI |
|---|---|---|
| Memory model | ? | ? |
| How parallelism is expressed | ? | ? |
| Scales beyond one node? | ? | ? |
| Programming effort | ? | ? |
| Typical use case | ? | ? |

Then answer: **for a researcher who needs to parallelise a for-loop-heavy serial C program to run on a single 12-core workstation as quickly as possible, which should they choose and why?**

> **Model Answer:**
>
> | Characteristic | OpenMP | MPI |
> |---|---|---|
> | Memory model | **Shared memory** — all threads see the same address space | **Distributed memory** — each process has its own private memory |
> | How parallelism is expressed | **Compiler directives** (`#pragma omp parallel for`) added to existing serial code | **Library function calls** (`MPI_Send`, `MPI_Recv`, `MPI_Bcast`, etc.) |
> | Scales beyond one node? | **No** — confined to cores within a single shared-memory node | **Yes** — scales across the entire cluster via the interconnect |
> | Programming effort | **Low** — incremental; serial structure preserved; add pragmas and scoping clauses | **High** — requires explicit data distribution, halo exchange design, and collective communication |
> | Typical use case | Loop parallelism on a single node; rapid parallelisation of existing codes | Large-scale distributed computation; multi-node clusters |
>
> (1 mark per row correctly completed = 5 marks)
>
> **Recommendation: OpenMP.** (1 mark)
>
> Reasons: (2 marks — need at least 2)
> - The target hardware is a **single shared-memory node** — MPI's inter-node communication infrastructure is unnecessary overhead.
> - The program is serial with most work in for loops — exactly OpenMP's forte; adding `#pragma omp parallel for` is fast to implement.
> - Speed of development matters: OpenMP allows the researcher to deliver a parallel version quickly without redesigning data structures.
> - 12 cores is well within OpenMP's scaling range for typical scientific loops.

---

### Q24 — Compare HPL and HPCG *(6 marks)*

Compare the **HPL** and **HPCG** benchmarks across the following dimensions: workload type, arithmetic intensity, performance bottleneck, and what aspect of HPC system performance each best reflects.

Present your answer as a structured table followed by a brief conclusion.

> **Model Answer:**
>
> | Dimension | HPL | HPCG |
> |---|---|---|
> | **Workload** | Dense system of linear equations $Ax=b$ via LU factorisation | Sparse system via conjugate gradient on a 3D Poisson stencil |
> | **Arithmetic intensity** | High — $O(N)$ FLOPs per byte (BLAS Level 3, DGEMM-like) | Low — $O(1)$ FLOPs per byte (sparse, indirect memory access) |
> | **Performance bottleneck** | Compute-bound — limited by FP throughput | Memory-bandwidth-bound — limited by DRAM/cache bandwidth |
> | **What it measures** | Peak sustained FP throughput (best-case system performance) | Real memory subsystem and network performance (typical application behaviour) |
> | **Fraction of Rpeak achieved** | High (often 70–90%) | Very low (often 1–5% of Rpeak) |
>
> (1 mark per row correctly populated = 5 marks)
>
> **Conclusion:** HPL is useful for comparing raw compute capability between systems but is unrepresentative of most real workloads. HPCG fills this gap by testing memory bandwidth and sparse operations — the bottleneck that determines performance for the majority of real HPC applications. Together they give a more complete picture of system capability. (1 mark)

---

### Q25 — True/False with Justification *(10 marks — 2 marks each)*

For each statement, write **True** or **False** and give a brief justification (2–3 sentences). A wrong answer with a correct justification earns 1 mark; a correct answer with no justification earns 1 mark.

**(a)** "Dennard Scaling predicts that as transistors shrink, chip power consumption stays constant."

**(b)** "The Top500 list ranks HPC systems by their HPCG performance."

**(c)** "An OpenMP program can use all cores across multiple nodes of a cluster."

**(d)** "Fortran is obsolete in modern HPC and no longer used."

**(e)** "A system with a higher $R_{peak}$ will always outperform a system with a lower $R_{peak}$ on real applications."

> **Model Answer:**
>
> **(a) FALSE** — Dennard Scaling predicts that **power density** (power per unit area) stays constant as transistors shrink, not total chip power consumption. If you shrink transistors and add more of them to the same area, total power is maintained. The point is that smaller transistors are individually more efficient (use less power per operation), enabling higher frequencies at the same power budget. (2 marks)
>
> **(b) FALSE** — The Top500 ranks systems by their **HPL (High-Performance Linpack)** performance ($R_{max}$). HPCG is an additional benchmark that is reported alongside HPL but is **not** the ranking criterion. The HPCG list is a separate ordering. (2 marks)
>
> **(c) FALSE** — OpenMP is a **shared-memory** programming model. A single OpenMP program is a process whose threads all share one memory address space, which requires shared physical memory. This limits OpenMP to the cores within a **single compute node**. To use cores across multiple nodes, MPI (or a hybrid MPI+OpenMP approach) is required. (2 marks)
>
> **(d) FALSE** — Fortran is very much still in use in HPC. A large volume of active HPC code in weather forecasting, climate modelling, and computational physics is written in Fortran. It has compiler advantages (array semantics, no aliasing by default) that make it amenable to aggressive optimisation, and modern Fortran (90/2003/2018) continues to be updated. Rewriting legacy codes is prohibitively expensive. (2 marks)
>
> **(e) FALSE** — $R_{peak}$ is a theoretical maximum assuming perfect utilisation of all hardware. Real applications are almost always **memory-bandwidth-bound** or limited by communication overhead, meaning they achieve only a fraction of $R_{peak}$. A system with higher $R_{peak}$ but lower memory bandwidth could perform worse on a sparse or stencil workload than a system with lower $R_{peak}$ but higher bandwidth. The relevant metric depends on the application's arithmetic intensity. (2 marks)

---

## Appendix: Key Formulas for Week 1

```
Peak performance:
  R_peak = N_sockets × N_cores_per_socket × R_clock × N_ops_per_cycle

Linpack efficiency:
  η = R_max / R_peak

Cluster peak:
  R_peak_cluster = R_peak_node × N_nodes

Unit conversions:
  1 GFlop/s = 10^9 flop/s
  1 TFlop/s = 10^12 flop/s
  1 PFlop/s = 10^15 flop/s
  1 EFlop/s = 10^18 flop/s
```

---

## Appendix: Quick-Reference Concept Index

| Topic | Key Facts to Remember |
|---|---|
| HPC definition | Aggregating compute power beyond a typical workstation; scientific, engineering, business uses |
| FLOP/s | Floating-point operations per second; fastest systems: 10s–100s PFlop/s (Frontier: 1.19 EFlop/s) |
| HPL | Dense Ax=b via LU factorisation; BLAS Level 3; compute-bound; ranks Top500 |
| HPCG | Sparse 3D Poisson CG; memory-bound; 1–5% of R_peak; complements HPL |
| Top500 | Ranked by HPL (R_max); published twice yearly; tracks global HPC trends since 1990s |
| R_peak formula | N_sockets × N_cores/socket × R_clock × N_ops/cycle |
| Moore's Law | Transistor count doubles ~every 24 months; still holds (slowing); gives more *cores* not faster cores |
| Dennard Scaling | Power density constant as transistors shrink; **broken** since mid-2000s; caused clock speed stall |
| Why parallelism | Dennard broken → clocks stalled; Moore continues → more cores; must program parallel to benefit |
| Commodity cluster | OTS components; cost-effective; compute nodes + interconnect + storage + login nodes |
| MPP | Specialist hardware; custom interconnects; higher performance but more expensive (Fugaku, BlueGene) |
| Compiled languages | C, C++, Fortran; compile-time optimisation; no interpreter overhead |
| OpenMP | Shared memory; directives; single node only; low programmer effort |
| MPI | Distributed memory; library calls; scales across entire cluster; high programmer effort |
