---
title: "ECMM461 May 2021 — Full Paper with Solutions (older module)"
tags: [hpc, exam, ecmm461, 2021, older-module]
date: 2026-05-08
---

# ECMM461 May 2021 — Full Paper with Solutions

**University of Exeter · College of Engineering, Mathematics and Physical Sciences · Computer Science**  
**Module Leader:** David Acreman · **Duration:** 2 hours + 30 min upload time · **Open book** · **Total: 100 marks**  
*50% paper + 50% coursework.*

*This is the older Master's-level equivalent of ECM3446. Material overlaps heavily with the current undergraduate module — the same concepts, but sometimes with slightly different numbers or framing.*

---

## Question 1 (40 marks)

### 1(a) The graph below plots processor clock frequency against time for different processors produced since 1985.

*[Figure: Clock Frequency vs. Time (1985–2010). Vertical axis: MHz (logarithmic). Horizontal axis: year (linear). Frequency increases approximately linearly (on log scale) from 1985 to mid-2000s, then plateaus.]*

#### (i) What enabled processor clock frequencies to increase prior to 2005? *(2 marks)*

**Answer:**

**Dennard scaling.** As transistor feature sizes shrank (per Moore's Law), the smaller transistors switched faster *and* used less power per unit area. This kept power density roughly constant while clock frequency rose, so manufacturers could simply ship faster chips at every process node.

*Concepts: [Moore's Law and Dennard Scaling](../concepts/Moores_Law_and_Dennard_Scaling.md)*

---

#### (ii) Why are processor clock frequencies no longer increasing? *(2 marks)*

**Answer:**

**Dennard scaling broke down.** At very small feature sizes, leakage currents become significant and threshold voltages can no longer be reduced proportionally. Continuing to push the clock higher exceeds what air-cooling can dissipate (the **power-density wall**). Thermal limits, not transistor count, now bound single-core frequency.

---

#### (iii) What are the implications for high performance computing? *(3 marks)*

**Answer:**

- Single-core performance has plateaued; serial programs cannot ride frequency growth any longer.
- Moore's Law continues to deliver more transistors per chip, but they go into **more cores per processor** rather than faster ones.
- The only way to convert hardware progress into program speed-up is **parallel programming** (OpenMP, MPI, GPUs).
- HPC systems also turn to specialised accelerators (GPUs) and wider vector units (AVX-512) for additional throughput at the same clock.

*Concepts: [Moore's Law and Dennard Scaling](../concepts/Moores_Law_and_Dennard_Scaling.md), [HPC Programming Languages](../concepts/HPC_Programming_Languages.md), [Graphics Processing Units (GPUs)](../concepts/Graphics_Processing_Units_GPUs.md)*

---

### 1(b) The fastest computer on the June 2011 Top500 list was called the K computer. The following table shows information about the K Computer taken from the Top500 website.

| Field | Value |
|:---|:---|
| **Manufacturer** | Fujitsu |
| **Cores** | 705,024 |
| **Processor** | SPARC64 VIIIfx 8C 2GHz |
| **Interconnect** | Custom Interconnect |
| **Linpack Performance (Rmax)** | 10,510 TFlop/s |
| **Theoretical Peak (Rpeak)** | 11,280.4 TFlop/s |
| **HPCG performance** | 602.736 TFlop/s |
| **Power consumption** | 12,659.89 kW |
| **Operating system** | Linux |

#### (i) What is the LINPACK efficiency of the K computer? Show your working. *(2 marks)*

**Answer:**

$$\eta = \frac{R_{max}}{R_{peak}} = \frac{10510}{11280.4} = 0.9317$$

**LINPACK efficiency ≈ 93.2%** — exceptionally high, reflecting the K computer's heavy optimisation for HPL.

*Concepts: [Performance Metrics and Top500](../concepts/Performance_Metrics_and_Top500.md)*

---

#### (ii) Why is the HPCG performance figure significantly less than the Linpack performance figure? *(2 marks)*

**Answer:**

LINPACK measures dense matrix-matrix work (BLAS Level 3, $O(N)$ arithmetic intensity) — heavily compute-bound, hits a high fraction of $R_{peak}$.

HPCG measures sparse linear algebra (3-D Poisson on a 27-point stencil) — $O(1)$ arithmetic intensity with indirect addressing, so it is **memory-bandwidth-bound**. The relevant performance ceiling is `bandwidth × AI`, not $R_{peak}$. On the K computer this gives only $602.7 / 11280 \approx 5.3\%$ of the peak.

HPCG was introduced precisely because it captures the bandwidth, latency, and synchronisation costs that dominate real applications — costs that LINPACK ignores.

*Concepts: [Arithmetic Intensity and Roofline Model](../concepts/Arithmetic_Intensity_and_Roofline_Model.md), [BLAS and Dense Matrices](../concepts/BLAS_and_Dense_Matrices.md), [Sparse Matrices and CSR](../concepts/Sparse_Matrices_and_CSR.md)*

---

#### (iii) Based on the information shown above would you class the K computer as a commodity cluster or an MPP (Massively Parallel Processor) and why? *(2 marks)*

**Answer:**

**MPP.** The "Custom Interconnect" (Tofu) and the SPARC64 VIIIfx (a Fujitsu processor designed specifically for the K computer) are both bespoke parts. Commodity clusters use off-the-shelf x86 + Infiniband.

*Concepts: [Cluster Architecture](../concepts/Cluster_Architecture.md), [Interconnects and Network Topologies](../concepts/Interconnects_and_Network_Topologies.md)*

---

### 1(c) The following C program calculates a Gaussian probability density distribution and converts it to a cumulative distribution.

```c
#include <stdio.h>
#include <math.h>

int main(){
    const int N=201;
    const float dx=0.5;
    const float x0=50.0;
    const float sigma=10.0;
    float a[N];
    float normConst;
    float x;
    float z;

    normConst = 1.0 / ( sigma * sqrt(2.0*M_PI) );

    // Loop 1: Calculate Gaussian probability
    for (int i=0; i<N; i++){
        x = ( (float) i) * dx;
        z = (x-x0) / sigma;
        a[i] = normConst * exp (-0.5*z*z);
    }
    printf("Maximum x value: %g\n", x);

    // Loop 2: Convert to a cumulative distribution
    for (int i=1; i<N; i++){
        a[i] = a[i-1] + a[i]*dx;
    }

    return 0;
}
```

#### (i) Consider whether the first loop (labelled "Loop 1") contains a loop-carried dependency. If there is a dependency say what type of dependency it is and why it exists. If there is no dependency explain why no dependency exists. *(3 marks)*

**Answer:**

**No loop-carried dependency exists.** Each iteration:
- Computes `x` and `z` from the loop index `i` and the const inputs only.
- Writes only to `a[i]` — no other iteration touches that element.
- Does not read any value written by another iteration.

The temptation to call this dependent comes from `x` and `z` being shared scalars in the serial code; that is a *scoping* concern (data race potential, not a true dependency). At the algorithm level, the loop body is fully parallel.

*Concepts: [Data Dependencies and Data Races](../concepts/Data_Dependencies.md)*

---

#### (ii) Consider whether the first loop can be parallelised using OpenMP. If the loop can be parallelised then show the directive or directives you would use. You should ensure that variables are explicitly scoped unless they are declared with the const qualifier. *(3 marks)*

**Answer:**

Yes, this loop can be parallelised. Each thread needs its own `x` and `z` to avoid races; the `a` array is shared (each thread writes a distinct element); and the `printf` after the loop reads `x`, which must hold the value from the sequentially-last iteration — so `x` is `lastprivate`.

```c
#pragma omp parallel for default(none) \
        shared(a) \
        private(z) \
        lastprivate(x)
for (int i=0; i<N; i++){
    x = ((float) i) * dx;
    z = (x-x0) / sigma;
    a[i] = normConst * exp(-0.5*z*z);
}
```

*(The `const`-qualified scalars `N`, `dx`, `x0`, `sigma`, `normConst` don't need explicit scoping per the question's rules.)*

*Concepts: [Variable Scoping in OpenMP](../concepts/Variable_Scoping_OpenMP.md), [Parallel Loops in OpenMP](../concepts/Parallel_Loops_OpenMP.md)*

---

#### (iii) Consider whether the second loop (labelled "Loop 2") contains a loop-carried dependency. If there is a dependency say what type of dependency it is and why it exists. *(3 marks)*

**Answer:**

**Yes — a flow (Read-After-Write / true) dependency exists.** Iteration `i` reads `a[i-1]`, which was written by iteration `i-1`. The loop is a **prefix sum** (cumulative integration): each output depends on the running total of all previous outputs.

*Concepts: [Data Dependencies and Data Races](../concepts/Data_Dependencies.md)*

---

#### (iv) Consider whether the second loop can be parallelised using OpenMP. If the loop can be parallelised then show the directive or directives you would use. If the loop cannot be parallelised by adding one or more OpenMP directives then say that the loop cannot be parallelised and explain why. *(3 marks)*

**Answer:**

**Cannot be parallelised by simply adding OpenMP directives.** A flow dependency means iterations cannot run out of order: if thread B starts iteration 50 before thread A has finished iteration 49, `a[49]` hasn't been updated yet and B reads stale data, producing the wrong cumulative sum.

To parallelise this loop you must rewrite it using a **parallel scan / prefix-sum algorithm** (e.g. Hillis-Steele or Blelloch), which has $O(N \log N)$ work but log-depth parallelism. OpenMP 5.x provides `#pragma omp scan` for exactly this case, but a naive `#pragma omp parallel for` is not correct.

*Concepts: [Data Dependencies and Data Races](../concepts/Data_Dependencies.md)*

---

### 1(d) The following program calculates values of the function y(x) = sin(nx) for n = 1, 2, 3, 4.

```c
#include <stdio.h>
#include <math.h>

int main(){
    const int NPOINTS=1001;
    const int NCURVES=4;
    double dtheta;
    double y[NCURVES][NPOINTS];
    double theta[NPOINTS];

    dtheta = 2*M_PI / ( (float) (NPOINTS-1) );

    for (int n=0; n<NCURVES; n++){
        for(int i=0; i<NPOINTS; i++){
            theta[i] = ( (float) i) * dtheta;
            y[n][i] = sin( ((float) (n+1)) * theta[i]);
        }
    }

    return 0;
}
```

#### (i) Show how you would parallelise this program using OpenMP ensuring that it can scale to make effective use of a modern multi-core processor. *(4 marks)*

**Answer:**

The outer loop runs only `NCURVES = 4` iterations — far too few to scale on a modern multi-core processor (8, 16, 64+ cores). The inner loop runs 1001 iterations. Use `collapse(2)` to merge both loops into 4004 independent iterations:

```c
#pragma omp parallel for default(none) \
        shared(y, theta) \
        firstprivate(dtheta) \
        collapse(2)
for (int n=0; n<NCURVES; n++){
    for(int i=0; i<NPOINTS; i++){
        theta[i] = ( (float) i) * dtheta;
        y[n][i] = sin( ((float) (n+1)) * theta[i]);
    }
}
```

*(Note: writing `theta[i]` from multiple `n`s is a benign race — every iteration writes the same value. A cleaner option is to hoist the `theta` initialisation into its own preceding parallel loop.)*

*Concepts: [Parallel Loops in OpenMP](../concepts/Parallel_Loops_OpenMP.md)*

---

#### (ii) Explain why you chose to parallelise the program in this way. *(3 marks)*

**Answer:**

- The outer loop has only 4 iterations. With more than 4 cores, parallelising the outer loop alone leaves cores idle.
- The inner loop has 1001 iterations and no carried dependencies — scales naturally.
- `collapse(2)` exposes 4004 independent iterations to the runtime, ensuring even very wide processors are saturated and load is balanced across all available threads.

*Concepts: [Parallel Loops in OpenMP](../concepts/Parallel_Loops_OpenMP.md), [Load Balancing and Scheduling](../concepts/Load_Balancing_and_Scheduling.md)*

---

### 1(e) MPI is a widely used parallel programming technology which can be used to write parallel programs to run on a wide range of architectures. OpenMP is another parallel programming technology which can be used instead of, or in combination with, MPI. Describe four situations where you would choose to use OpenMP instead of, or in combination with, MPI. *(8 marks)*

**Answer:**

1. **Targeting one shared-memory node.** OpenMP is native shared-memory; MPI's distribution overhead is wasted on a single server.

2. **Incremental parallelisation of a serial code.** OpenMP requires only `#pragma omp parallel for` and scoping; MPI requires re-architecting to distribute data, which can take weeks.

3. **Hybrid MPI+OpenMP on large clusters.** MPI between nodes, OpenMP within a node — fewer ranks, fewer halos, fewer messages, better memory utilisation.

4. **Memory pressure within a node.** If MPI's per-rank halos or duplicated state would exceed `RAM / cores_per_node`, switch to OpenMP threads which share a single copy of the static data.

*Concepts: [OpenMP vs. MPI](../comparisons/OpenMP_vs_MPI.md), [Hybrid Parallelism (MPI + OpenMP)](../concepts/Hybrid_Parallelism_MPI_OpenMP.md)*

---

## Question 2 (30 marks)

### 2(a) The following paragraph describes the Archer HPC system: The ARCHER hardware consists of the Cray XC30 MPP supercomputer, external login nodes and post processing nodes, and the associated filesystems. There are 4920 compute nodes in ARCHER phase 2 and each compute node has two 12-core Intel Ivy Bridge series processors giving a total of 118,080 processing cores. Each node has a total of 64 GB of memory with a subset of large memory nodes having 128 GB.

#### (i) What is the largest number of processor cores available to an OpenMP program running on Archer and why? *(2 marks)*

**Answer:**

OpenMP is shared-memory; threads of one process can't span nodes. Each ARCHER node has two 12-core processors → **24 cores per node**.

**Maximum: 24 cores.**

*Concepts: [OpenMP](../concepts/OpenMP.md)*

---

#### (ii) What is the largest number of processor cores available to an MPI program running on Archer and why? *(2 marks)*

**Answer:**

MPI scales across distributed memory. **Maximum: 118 080 cores** (all cores on the system).

*Concepts: [Message Passing Interface (MPI)](../concepts/Message_Passing_Interface_MPI.md)*

---

#### (iii) The SHMEM library can be used to write parallel programs. According to Wikipedia, SHMEM is a family of parallel programming libraries, providing one-sided, RDMA, parallel-processing interfaces for low-latency distributed-memory supercomputers, used as parallel programming interface or as low-level interface to build partitioned global address space (PGAS) systems and languages. What is the largest number of processor cores available to a program using SHMEM running on Archer and why? *(2 marks)*

**Answer:**

The Wikipedia text says SHMEM is for *low-latency distributed-memory supercomputers* and underpins PGAS systems. So SHMEM, like MPI, scales across the whole cluster.

**Maximum: 118 080 cores.**

---

### 2(b) Performing large scale calculations requires the use of parallel programs which can scale effectively to use many processors.

#### (i) If a program takes 120 minutes to run on one processor and the maximum parallel speed up is 5 what is the shortest possible run time for the program if the total problem size remains fixed? Show your working. *(3 marks)*

**Answer:**

$$T_{min} = \frac{T_0}{S_{max}} = \frac{120}{5} = 24\ \text{minutes}$$

*Concepts: [Parallel Scaling](../concepts/Parallel_Scaling.md)*

---

#### (ii) If the serial fraction of a program is s = 0.1 how many processors are required to give a speed up of 5 according to idealised strong scaling? *(5 marks)*

**Answer:**

Amdahl: $S_N = \frac{1}{s + p/N}$ with $s = 0.1$, $p = 0.9$.

$$5 = \frac{1}{0.1 + 0.9/N}$$
$$0.1 + \frac{0.9}{N} = 0.2$$
$$\frac{0.9}{N} = 0.1$$
$$N = 9$$

**N = 9 processors.**

---

#### (iii) If the serial fraction of a program is s = 0.1 what is the smallest number of processors required to give a speed up of at least 5 according to idealised weak scaling? *(5 marks)*

**Answer:**

Gustafson: $S_N = s + p \cdot N$ with $s = 0.1$, $p = 0.9$.

$$5 \le 0.1 + 0.9 \cdot N$$
$$4.9 \le 0.9 \cdot N$$
$$N \ge \frac{4.9}{0.9} = 5.444\ldots$$

Round up: **N = 6 processors** (smallest integer giving $S_N \ge 5$). Check: $S_6 = 0.1 + 0.9 \times 6 = 5.5$. ✓

*Concepts: [Parallel Scaling](../concepts/Parallel_Scaling.md)*

---

### 2(c) Consider a two-dimensional partial differential equation (PDE) solver which solves a PDE with one unknown variable u. To solve the PDE it is necessary to calculate values for the second derivative:

$$\nabla^2u = \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}$$

This expression is evaluated using the finite difference stencil:

```
del2u = (u(i+1,j) - 2*u(i,j) + u(i-1,j))/(dx*dx) +
        (u(i,j+1) - 2*u(i,j) + u(i,j-1))/(dy*dy)
```

The calculation is domain decomposed such that each sub-domain comprises 1000 × 1000 grid points. In addition to these grid points each sub-domain stores halo values which are copies of the data on neighbouring processors.

#### (i) How many values need to be exchanged when one halo is sent to one neighbouring process? *(1 mark)*

**Answer:**

A halo to one neighbour is one edge of the sub-domain: **1000 values.**

---

#### (ii) How many bytes need to be sent if the values are represented using IEEE754 double precision? *(2 marks)*

**Answer:**

$1000 \times 8 = \mathbf{8000}$ **bytes.**

---

#### (iii) What is the transmission time for sending a single halo over a network with a latency of 2µs (2 × 10⁻⁶s) and a bandwidth of 25 GB/s (25 gigabytes per second)? Show your working. *(3 marks)*

**Answer:**

$$t = L + \frac{M}{B} = 2.0 \times 10^{-6} + \frac{8000}{25 \times 10^9}$$
$$= 2.0 \times 10^{-6} + 3.2 \times 10^{-7}$$
$$\boxed{t \approx 2.32 \times 10^{-6}\ \text{s} = 2.32\ \mu\text{s}}$$

*Concepts: [Interconnects and Network Topologies](../concepts/Interconnects_and_Network_Topologies.md)*

---

#### (iv) Is the bandwidth or the latency more important for determining the transmission time for sending one halo? Explain your reasoning. *(2 marks)*

**Answer:**

**Latency dominates.** Latency contributes $2.0 \times 10^{-6}$ s; bandwidth contributes $3.2 \times 10^{-7}$ s. Latency is ~6.25× larger. The 8 KB message is small enough that the fixed network setup cost outweighs the time spent actually streaming bytes.

---

#### (v) The PDE solver is modified so that it solves a three-dimensional PDE and each sub-domain contains 1000 × 1000 × 1000 grid points. Is the bandwidth or the latency more important for determining the transmission time for sending one halo in the modified program? Explain your reasoning. *(3 marks)*

**Answer:**

In 3-D, the halo for one face of the sub-domain is 2-D: $1000 \times 1000 = 10^6$ values, or $8 \times 10^6 = 8\ \text{MB}$.

$$t = 2.0 \times 10^{-6} + \frac{8 \times 10^6}{25 \times 10^9}$$
$$= 2.0 \times 10^{-6} + 3.2 \times 10^{-4}$$

The bandwidth term (320 µs) is now ~160 000× larger than the latency term (2 µs). **Bandwidth dominates** in the 3-D case.

As you scale up halo size, the message-size term takes over. The standard intuition: small messages → optimise latency; large messages → optimise bandwidth.

*Concepts: [Interconnects and Network Topologies](../concepts/Interconnects_and_Network_Topologies.md), [Domain Decomposition Overheads](../concepts/Domain_Decomposition_Overheads.md)*

---

## Question 3 (30 marks)

### 3(a) A cluster comprises 64 compute nodes with each compute node constructed from a two socket motherboard. Each socket has a multi-core processor comprising 16 cores with a clock frequency of 2.6 GHz. The instruction set supported by the processors is capable of delivering 4 floating point operations per cycle.

#### (i) What is the peak performance of a single processor core? Show your working. *(2 marks)*

**Answer:**

$$R_{peak,\,core} = R_{clock} \times N_{ops/cycle} = 2.6 \times 10^9 \times 4 = 1.04 \times 10^{10}\ \text{flop/s}$$

**= 10.4 GFlop/s per core.**

*Concepts: [Performance Metrics and Top500](../concepts/Performance_Metrics_and_Top500.md)*

---

#### (ii) What is the peak performance of a single compute node? Show your working. *(2 marks)*

**Answer:**

$$R_{peak,\,node} = N_{sockets} \times N_{cores/socket} \times R_{peak,\,core} = 2 \times 16 \times 10.4 = 332.8\ \text{GFlop/s}$$

---

#### (iii) What is the peak performance of the whole cluster? Show your working. *(2 marks)*

**Answer:**

$$R_{peak,\,cluster} = N_{nodes} \times R_{peak,\,node} = 64 \times 332.8 = 21\,299.2\ \text{GFlop/s} \approx 21.3\ \text{TFlop/s}$$

---

#### (iv) You run a matrix solver based on the BLAS routine DGEMM on one compute node. Do you expect it to achieve large fraction of the compute node peak performance? Explain your reasoning. *(3 marks)*

**Answer:**

**Yes.** DGEMM is dense matrix-matrix multiplication: BLAS Level 3 with $O(N^3)$ FLOPs and $O(N^2)$ memory traffic. As $N$ grows, arithmetic intensity grows as $O(N)$, so the operation is heavily compute-bound. Combined with cache blocking inside optimised BLAS libraries (OpenBLAS, MKL), DGEMM routinely hits 80–95% of $R_{peak}$ on a single node.

*Concepts: [BLAS and Dense Matrices](../concepts/BLAS_and_Dense_Matrices.md), [Arithmetic Intensity and Roofline Model](../concepts/Arithmetic_Intensity_and_Roofline_Model.md), [Cache Blocking (Loop Tiling)](../concepts/Cache_Blocking.md)*

---

#### (v) You run a sparse matrix solver on one compute node. Do you expect it to achieve a large fraction of the compute node peak performance? Explain your reasoning. *(3 marks)*

**Answer:**

**No.** Sparse matrix operations use formats like CSR with indirect addressing (`col_ind`, `row_ptr`). Arithmetic intensity is $O(1)$: each non-zero is multiplied once; data has to be streamed from DRAM with non-contiguous access patterns that defeat the cache. Performance is **memory-bandwidth-bound**, not compute-bound. Typical sparse solvers achieve ~5–10% of $R_{peak}$ on the same node where DGEMM hits 90%+.

*Concepts: [Sparse Matrices and CSR](../concepts/Sparse_Matrices_and_CSR.md), [Arithmetic Intensity and Roofline Model](../concepts/Arithmetic_Intensity_and_Roofline_Model.md)*

---

### 3(b) The following three arrays represent a sparse matrix in compressed sparse row format. The arrays represent the values (`vals`), column indices (`col_ind`) and row pointers (`row_ptr`) with numbering starting from one.

```
vals    =  [ 3,  1,  9, 13,  1,  8, 10 ]
col_ind =  [ 2,  1,  2,  4,  4,  2,  4 ]
row_ptr =  [ 1,  2,  5,  6,  8 ]
```

Write out the matrix in full as a grid of numbers including the zeros. *(9 marks)*

**Answer:**

`row_ptr` has 5 entries → 4 rows. The largest column index is 4 → **4 × 4 matrix**.

Decoding row-by-row (1-indexed):

- **Row 1:** entries from index `row_ptr[1]=1` up to (not including) `row_ptr[2]=2`. Entry 1 only.
  - `vals[1]=3` at column `col_ind[1]=2` → row 1 is `[0, 3, 0, 0]`.

- **Row 2:** entries 2 to 4 (indices 2, 3, 4).
  - `vals[2]=1` at column 1
  - `vals[3]=9` at column 2
  - `vals[4]=13` at column 4 → row 2 is `[1, 9, 0, 13]`.

- **Row 3:** entries 5 to 5 (just index 5).
  - `vals[5]=1` at column 4 → row 3 is `[0, 0, 0, 1]`.

- **Row 4:** entries 6 to 7.
  - `vals[6]=8` at column 2
  - `vals[7]=10` at column 4 → row 4 is `[0, 8, 0, 10]`.

Full matrix:

$$
\begin{pmatrix}
0 & 3 & 0 & 0 \\
1 & 9 & 0 & 13 \\
0 & 0 & 0 & 1 \\
0 & 8 & 0 & 10
\end{pmatrix}
$$

*Concepts: [Sparse Matrices and CSR](../concepts/Sparse_Matrices_and_CSR.md)*

---

### 3(c) A finite difference method is used to solve the advection equation. The time step used to compute the solution is calculated according to the constraint:

$$\Delta t = C \frac{\Delta x}{v_{max}}$$

where $\Delta t$ is the time step, $\Delta x$ is the spacing between grid points, $v_{max}$ is the maximum velocity in the calculation and $C$ is a constant with a value between 0 and 1.

#### (i) How does the computational cost of calculating a one-dimensional solution with N grid points compare with the computational cost of calculating a three-dimensional solution with N grid points in each dimension? You should assume that spatial resolution and number of time steps calculated are the same in both cases. Explain your reasoning. *(2 marks)*

**Answer:**

Grid points: $N$ (1-D) vs $N^3$ (3-D). With same number of time steps, total work scales with grid points:

**The 3-D calculation costs $N^2$ times more than 1-D.**

*Concepts: [Advection Equation](../concepts/Advection_Equation.md), [Numerical Stability and CFL](../concepts/Numerical_Stability_and_CFL.md)*

---

#### (ii) How does the computational cost of the three-dimensional calculation increase if Δx is reduced by a factor of 10? You should assume that end time of the calculation and the extent of the computational domain remain constant. Explain your reasoning. *(4 marks)*

**Answer:**

Three things change when $\Delta x \to \Delta x / 10$ at fixed end time and domain size:

1. **Grid points per dimension** scale as $1/\Delta x$, so they grow by ×10. In 3-D, total grid points grow by $10^3 = 1000$.
2. **Time step** by CFL scales as $\Delta x$, so $\Delta t$ shrinks by ×10.
3. **Number of time steps** to reach the same end time grows by ×10.

Total cost = points × time steps:
$$\text{factor} = 1000 \times 10 = \mathbf{10\,000}$$

**Cost grows by a factor of 10 000.**

*Concepts: [Advection Equation](../concepts/Advection_Equation.md), [Numerical Stability and CFL](../concepts/Numerical_Stability_and_CFL.md)*

---

#### (iii) Consider a different solver which calculates solutions to the Navier-Stokes equations describing fluid dynamics. With this solver the maximum velocity present in the solution increases when the spatial resolution is increased by adding more grid points. Does this make the computational cost larger or smaller compared to the case where the maximum velocity does not change? You should assume that the extent of the computational domain and the number of time steps calculated remain constant. Explain your reasoning. *(3 marks)*

**Answer:**

**Larger cost.** The CFL condition $\Delta t \le C \Delta x / v_{max}$ means $\Delta t$ shrinks both because $\Delta x$ shrank *and* because $v_{max}$ rose. So the number of time steps grows faster than just the spatial-resolution factor would suggest.

Concretely: if $\Delta x$ falls by ×10 and $v_{max}$ rises by some factor $\alpha > 1$, then $\Delta t$ falls by $10\alpha$ and the number of time steps grows by $10\alpha$ (vs ×10 in the constant-$v_{max}$ case). Total cost in 3-D becomes $1000 \times 10\alpha = 10\,000\alpha$ — **larger by a factor of $\alpha$ compared to a solver where $v_{max}$ is constant.**

Physically, in turbulent fluid simulation finer grids resolve smaller, faster eddies — so $v_{max}$ genuinely does grow with resolution, and the computational cost of high-resolution Navier-Stokes scales worse than the naive count of grid points alone would predict.

*Concepts: [Numerical Stability and CFL](../concepts/Numerical_Stability_and_CFL.md), [Advection Equation](../concepts/Advection_Equation.md)*

---

## Concept Backlinks

- [Performance Metrics and Top500](../concepts/Performance_Metrics_and_Top500.md)
- [Cluster Architecture](../concepts/Cluster_Architecture.md)
- [Moore's Law and Dennard Scaling](../concepts/Moores_Law_and_Dennard_Scaling.md)
- [HPC Programming Languages](../concepts/HPC_Programming_Languages.md)
- [OpenMP](../concepts/OpenMP.md)
- [Parallel Loops in OpenMP](../concepts/Parallel_Loops_OpenMP.md)
- [Variable Scoping in OpenMP](../concepts/Variable_Scoping_OpenMP.md)
- [Data Dependencies and Data Races](../concepts/Data_Dependencies.md)
- [Load Balancing and Scheduling](../concepts/Load_Balancing_and_Scheduling.md)
- [Message Passing Interface (MPI)](../concepts/Message_Passing_Interface_MPI.md)
- [MPI Collective Communication](../concepts/MPI_Collective_Communication.md)
- [Domain Decomposition](../concepts/Domain_Decomposition.md)
- [Domain Decomposition Overheads](../concepts/Domain_Decomposition_Overheads.md)
- [Interconnects and Network Topologies](../concepts/Interconnects_and_Network_Topologies.md)
- [Parallel Scaling](../concepts/Parallel_Scaling.md)
- [BLAS and Dense Matrices](../concepts/BLAS_and_Dense_Matrices.md)
- [Sparse Matrices and CSR](../concepts/Sparse_Matrices_and_CSR.md)
- [Cache Blocking (Loop Tiling)](../concepts/Cache_Blocking.md)
- [Arithmetic Intensity and the Roofline Model](../concepts/Arithmetic_Intensity_and_Roofline_Model.md)
- [Advection Equation](../concepts/Advection_Equation.md)
- [Diffusion Equation](../concepts/Diffusion_Equation.md)
- [Numerical Stability and CFL](../concepts/Numerical_Stability_and_CFL.md)
- [OpenMP vs. MPI](../comparisons/OpenMP_vs_MPI.md)
- [Hybrid Parallelism (MPI + OpenMP)](../concepts/Hybrid_Parallelism_MPI_OpenMP.md)
- [Graphics Processing Units (GPUs)](../concepts/Graphics_Processing_Units_GPUs.md)
