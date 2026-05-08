---
title: "ECMM461 May 2021 — Worked Answers (older module)"
tags: [hpc, exam, ecmm461, 2021, older-module]
date: 2026-05-08
---

# ECMM461 May 2021 — Worked Answers

**Module Leader:** David Acreman · **Duration:** 2 hours + 30 min upload · **Open book** · **Total: 100 marks**

This is the older Master's-level equivalent of ECM3446. Material overlaps heavily with the current undergraduate module — the same concepts, but sometimes with slightly different numbers or framing.

---

## Question 1 (40 marks)

### 1(a) Clock-frequency trends graph

#### (i) What enabled clock frequencies to increase prior to 2005? (2 marks)

**Dennard scaling.** As transistor feature sizes shrank (per Moore's Law), the smaller transistors switched faster *and* used less power per unit area. This kept power density roughly constant while clock frequency rose, so manufacturers could simply ship faster chips at every node.

*Concepts: [Moore's Law and Dennard Scaling](../concepts/Moores_Law_and_Dennard_Scaling.md)*

#### (ii) Why frequencies are no longer increasing (2 marks)

**Dennard scaling broke down.** At very small feature sizes, leakage currents become significant and threshold voltages can no longer be reduced proportionally. Continuing to push the clock higher exceeds what air-cooling can dissipate (the **power-density wall**). Thermal limits, not transistor count, now bound single-core frequency.

#### (iii) Implications for HPC (3 marks)

- Single-core performance has plateaued; serial programs cannot ride frequency growth any longer.
- Moore's Law continues to deliver more transistors per chip, but they go into **more cores per processor** rather than faster ones.
- The only way to convert hardware progress into program speed-up is **parallel programming** (OpenMP, MPI, GPUs).
- HPC systems also turn to specialised accelerators (GPUs) and wider vector units (AVX-512) for additional throughput at the same clock.

*Concepts: [Moore's Law and Dennard Scaling](../concepts/Moores_Law_and_Dennard_Scaling.md), [HPC Programming Languages](../concepts/HPC_Programming_Languages.md), [Graphics Processing Units (GPUs)](../concepts/Graphics_Processing_Units_GPUs.md)*

---

### 1(b) The K computer (June 2011 #1)

| Field | Value |
|:---|:---|
| Cores | 705,024 |
| Processor | SPARC64 VIIIfx 8C 2 GHz |
| Interconnect | Custom Interconnect |
| $R_{max}$ | 10,510 TFlop/s |
| $R_{peak}$ | 11,280.4 TFlop/s |
| HPCG | 602.736 TFlop/s |

#### (i) LINPACK efficiency (2 marks)

$$\eta = \frac{R_{max}}{R_{peak}} = \frac{10510}{11280.4} = 0.9317$$

**LINPACK efficiency ≈ 93.2%** — exceptionally high, reflecting the K computer's heavy optimisation for HPL.

*Concepts: [Performance Metrics and Top500](../concepts/Performance_Metrics_and_Top500.md)*

#### (ii) Why is HPCG much lower than LINPACK? (2 marks)

LINPACK measures dense matrix-matrix work (BLAS Level 3, $O(N)$ arithmetic intensity) — heavily compute-bound, hits a high fraction of $R_{peak}$.

HPCG measures sparse linear algebra (3-D Poisson on a 27-point stencil) — $O(1)$ arithmetic intensity with indirect addressing, so it is **memory-bandwidth-bound**. The relevant performance ceiling is `bandwidth × AI`, not `R_peak`. On the K computer this gives only $602.7 / 11280 \approx 5.3\%$ of the peak.

HPCG was introduced precisely because it captures the bandwidth, latency, and synchronisation costs that dominate real applications — costs that LINPACK ignores.

*Concepts: [Arithmetic Intensity and Roofline Model](../concepts/Arithmetic_Intensity_and_Roofline_Model.md), [BLAS and Dense Matrices](../concepts/BLAS_and_Dense_Matrices.md), [Sparse Matrices and CSR](../concepts/Sparse_Matrices_and_CSR.md)*

#### (iii) Commodity cluster or MPP? (2 marks)

**MPP.** The "Custom Interconnect" (Tofu) and the SPARC64 VIIIfx (a Fujitsu processor designed specifically for the K computer) are both bespoke parts. Commodity clusters use off-the-shelf x86 + Infiniband.

*Concepts: [Cluster Architecture](../concepts/Cluster_Architecture.md), [Interconnects and Network Topologies](../concepts/Interconnects_and_Network_Topologies.md)*

---

### 1(c) Parallelising the Gaussian distribution code

```c
const int N=201;
const float dx=0.5;
const float x0=50.0;
const float sigma=10.0;
float a[N];
float normConst, x, z;

normConst = 1.0 / ( sigma * sqrt(2.0*M_PI) );

// Loop 1
for (int i=0; i<N; i++){
    x = ((float) i) * dx;
    z = (x-x0) / sigma;
    a[i] = normConst * exp(-0.5*z*z);
}
printf("Maximum x value: %g\n", x);

// Loop 2
for (int i=1; i<N; i++){
    a[i] = a[i-1] + a[i]*dx;
}
```

#### (i) Loop 1 dependency (3 marks)

**No loop-carried dependency exists.** Each iteration:
- Computes `x` and `z` from the loop index `i` and the const inputs only.
- Writes only to `a[i]` — no other iteration touches that element.
- Does not read any value written by another iteration.

The temptation to call this dependent comes from `x` and `z` being shared scalars in the serial code; that is a *scoping* concern (data race, not a true dependency). At the algorithm level, the loop body is fully parallel.

*Concepts: [Data Dependencies and Data Races](../concepts/Data_Dependencies.md)*

#### (ii) Parallelising Loop 1 (3 marks)

Yes, this loop can be parallelised. Each thread needs its own `x` and `z` to avoid races; the `a` array is shared (each thread writes a distinct element); and the `printf` after the loop reads `x`, which must hold the value from the sequentially-last iteration — so `x` is `lastprivate`.

```c
#pragma omp parallel for default(none) \
        shared(a) \
        firstprivate(dx, x0, sigma, normConst) \
        private(z) \
        lastprivate(x)
for (int i=0; i<N; i++){
    x = ((float) i) * dx;
    z = (x-x0) / sigma;
    a[i] = normConst * exp(-0.5*z*z);
}
```

(`const`-qualified scalars don't need explicit scoping by the question's rules; they are shown in `firstprivate` for clarity.)

*Concepts: [Variable Scoping in OpenMP](../concepts/Variable_Scoping_OpenMP.md), [Parallel Loops in OpenMP](../concepts/Parallel_Loops_OpenMP.md)*

#### (iii) Loop 2 dependency (3 marks)

**Yes — a flow (Read-After-Write / true) dependency exists.** Iteration `i` reads `a[i-1]`, which was written by iteration `i-1`. The loop is a **prefix sum**: each output depends on the running total of all previous outputs.

*Concepts: [Data Dependencies and Data Races](../concepts/Data_Dependencies.md)*

#### (iv) Parallelising Loop 2 (3 marks)

**Cannot be parallelised by simply adding OpenMP directives.** A flow dependency means iterations cannot run out of order: if thread B starts iteration 50 before thread A has finished iteration 49, `a[49]` hasn't been updated yet and B reads stale data, producing the wrong cumulative sum.

To parallelise this loop you must rewrite it using a **parallel scan / prefix-sum algorithm** (e.g. Hillis-Steele or Blelloch), which has $O(N \log N)$ work but log-depth parallelism. OpenMP 5.x does provide `#pragma omp scan` for exactly this case, but a naive `#pragma omp parallel for` is not correct.

*Concepts: [Data Dependencies and Data Races](../concepts/Data_Dependencies.md)*

---

### 1(d) Parallelising sin(nx) for n = 1..4

```c
const int NPOINTS=1001;
const int NCURVES=4;
double y[NCURVES][NPOINTS];
double theta[NPOINTS];
double dtheta = 2*M_PI / ((float)(NPOINTS-1));

for (int n=0; n<NCURVES; n++){
    for(int i=0; i<NPOINTS; i++){
        theta[i] = ((float) i) * dtheta;
        y[n][i] = sin(((float)(n+1)) * theta[i]);
    }
}
```

#### (i) Parallelisation strategy (4 marks)

The outer loop runs only `NCURVES = 4` iterations — that is far too few to scale on a modern multi-core processor (8, 16, 64+ cores). The inner loop runs 1001 iterations, which is plenty.

**Best approach: parallelise the inner loop**, or use `collapse(2)`:

```c
#pragma omp parallel for default(none) \
        shared(y, theta) \
        firstprivate(dtheta) \
        collapse(2)
for (int n=0; n<NCURVES; n++){
    for(int i=0; i<NPOINTS; i++){
        theta[i] = ((float) i) * dtheta;
        y[n][i] = sin(((float)(n+1)) * theta[i]);
    }
}
```

`collapse(2)` flattens the 4 × 1001 = 4004 iterations into a single space, giving the runtime ample work to distribute. (Note: writing `theta[i]` from multiple `n`s is a benign race — every iteration writes the same value, the same way — but a cleaner option is to hoist the `theta` initialisation into its own preceding parallel loop.)

#### (ii) Why this approach? (3 marks)

- The outer loop has only 4 iterations. With more than 4 cores, parallelising it leaves cores idle. Even with 4 cores, work is balanced only by accident (each iteration takes the same time, but the load granularity is huge).
- The inner loop has 1001 iterations and no carried dependencies — scales naturally.
- `collapse(2)` exposes 4004 independent iterations to the runtime, ensuring even very wide processors are saturated.
- Uneven inner-loop work (e.g. for irregular `sin` cost) would also benefit from `schedule(dynamic)` if it mattered, but here every iteration is essentially the same cost.

*Concepts: [Parallel Loops in OpenMP](../concepts/Parallel_Loops_OpenMP.md), [Load Balancing and Scheduling](../concepts/Load_Balancing_and_Scheduling.md)*

---

### 1(e) Four reasons to use OpenMP instead of, or with, MPI (8 marks)

(See ECM3446-24May Q1(e) for full discussion. Picking four:)

1. **Targeting one shared-memory node.** OpenMP is native shared-memory; MPI's distribution overhead is wasted on a single server.
2. **Incremental parallelisation of a serial code.** OpenMP requires only `#pragma omp parallel for` and scoping; MPI requires re-architecting to distribute data.
3. **Hybrid MPI+OpenMP on large clusters.** MPI between nodes, OpenMP within a node — fewer ranks, fewer halos, fewer messages, better memory utilisation.
4. **Memory pressure within a node.** If MPI's per-rank halos or duplicated state would exceed `RAM / cores_per_node`, switch to OpenMP threads which share a single copy.

*Concepts: [OpenMP vs. MPI](../comparisons/OpenMP_vs_MPI.md), [Hybrid Parallelism (MPI + OpenMP)](../concepts/Hybrid_Parallelism_MPI_OpenMP.md)*

---

## Question 2 (30 marks)

### 2(a) ARCHER — 4920 nodes × 24 cores = 118 080 cores

#### (i) Largest cores for OpenMP (2 marks)

OpenMP is shared-memory; threads of one process can't span nodes. Each ARCHER node has two 12-core processors → **24 cores per node**.

**Maximum: 24 cores.**

#### (ii) Largest cores for MPI (2 marks)

MPI scales across distributed memory. **Maximum: 118 080 cores.**

#### (iii) Largest cores for SHMEM (2 marks)

The Wikipedia text says SHMEM is for *low-latency distributed-memory supercomputers* and underpins PGAS systems. So SHMEM, like MPI, scales across the whole cluster.

**Maximum: 118 080 cores.**

*Concepts: [OpenMP](../concepts/OpenMP.md), [Message Passing Interface (MPI)](../concepts/Message_Passing_Interface_MPI.md)*

---

### 2(b) Scaling calculations

#### (i) Shortest run time, 120 min, max speed-up 5 (3 marks)

$$T_{min} = \frac{T_0}{S_{max}} = \frac{120}{5} = 24\ \text{minutes}$$

*Concepts: [Parallel Scaling](../concepts/Parallel_Scaling.md)*

#### (ii) Strong scaling: s = 0.1, S = 5 → N? (5 marks)

Amdahl: $S_N = \frac{1}{s + p/N}$ with $s = 0.1$, $p = 0.9$.

$$5 = \frac{1}{0.1 + 0.9/N}$$
$$0.1 + \frac{0.9}{N} = 0.2$$
$$\frac{0.9}{N} = 0.1$$
$$N = 9$$

**N = 9 processors.**

#### (iii) Weak scaling: s = 0.1, S ≥ 5 → smallest N? (5 marks)

Gustafson: $S_N = s + p \cdot N$ with $s = 0.1$, $p = 0.9$.

$$5 \le 0.1 + 0.9 \cdot N$$
$$4.9 \le 0.9 \cdot N$$
$$N \ge \frac{4.9}{0.9} = 5.444\ldots$$

Round up: **N = 6 processors** (smallest integer giving $S_N \ge 5$). Check: $S_6 = 0.1 + 0.9 \times 6 = 5.5$. ✓

*Concepts: [Parallel Scaling](../concepts/Parallel_Scaling.md)*

---

### 2(c) Halo exchange — 1000 × 1000 sub-domain

#### (i) Values per halo (1 mark)

A halo to one neighbour is one edge of the sub-domain: **1000 values.**

#### (ii) Bytes per halo (2 marks)

$1000 \times 8 = 8000$ bytes.

#### (iii) Transmission time, L = 2 µs, B = 25 GB/s (3 marks)

$$t = L + \frac{M}{B} = 2.0 \times 10^{-6} + \frac{8000}{25 \times 10^9}$$
$$= 2.0 \times 10^{-6} + 3.2 \times 10^{-7}$$
$$\boxed{t \approx 2.32 \times 10^{-6}\ \text{s} = 2.32\ \mu\text{s}}$$

*Concepts: [Interconnects and Network Topologies](../concepts/Interconnects_and_Network_Topologies.md)*

#### (iv) Bandwidth or latency more important? (2 marks)

**Latency dominates.** Latency contributes $2.0 \times 10^{-6}$ s; bandwidth contributes $3.2 \times 10^{-7}$ s. Latency is ~6.25× larger. The 8 KB message is small enough that the fixed network setup cost outweighs the time spent actually streaming bytes.

#### (v) 3-D PDE, 1000 × 1000 × 1000 sub-domain — bandwidth or latency? (3 marks)

In 3-D, the halo for one face of the sub-domain is 2-D: $1000 \times 1000 = 10^6$ values, or $8 \times 10^6 = 8\ \text{MB}$.

$$t = 2.0 \times 10^{-6} + \frac{8 \times 10^6}{25 \times 10^9}$$
$$= 2.0 \times 10^{-6} + 3.2 \times 10^{-4}$$

The bandwidth term (320 µs) is now ~160 000× larger than the latency term (2 µs). **Bandwidth dominates** in the 3-D case. As you scale up halo size, the message-size term takes over.

This is the standard intuition for tuning: small messages → optimise latency (e.g. aggregate, use lower-latency interconnect); large messages → optimise bandwidth (e.g. larger pipes, RDMA, eager-vs-rendezvous protocol tuning).

*Concepts: [Interconnects and Network Topologies](../concepts/Interconnects_and_Network_Topologies.md), [Domain Decomposition Overheads](../concepts/Domain_Decomposition_Overheads.md)*

---

## Question 3 (30 marks)

### 3(a) Cluster: 64 nodes × 2 sockets × 16 cores @ 2.6 GHz, 4 ops/cycle

#### (i) Peak per core (2 marks)

$$R_{peak,\,core} = R_{clock} \times N_{ops/cycle} = 2.6 \times 10^9 \times 4 = 1.04 \times 10^{10}\ \text{flop/s}$$

**= 10.4 GFlop/s per core.**

*Concepts: [Performance Metrics and Top500](../concepts/Performance_Metrics_and_Top500.md)*

#### (ii) Peak per node (2 marks)

$$R_{peak,\,node} = N_{sockets} \times N_{cores} \times R_{peak,\,core} = 2 \times 16 \times 10.4 = 332.8\ \text{GFlop/s}$$

#### (iii) Peak of cluster (2 marks)

$$R_{peak,\,cluster} = N_{nodes} \times R_{peak,\,node} = 64 \times 332.8 = 21\,299.2\ \text{GFlop/s} \approx 21.3\ \text{TFlop/s}$$

#### (iv) DGEMM solver — large fraction of peak? (3 marks)

**Yes.** DGEMM is dense matrix-matrix multiplication: BLAS Level 3 with $O(N^3)$ FLOPs and $O(N^2)$ memory traffic. As $N$ grows, arithmetic intensity grows as $O(N)$, so the operation is heavily compute-bound. Combined with cache blocking inside optimised BLAS libraries (OpenBLAS, MKL), DGEMM routinely hits 80–95% of $R_{peak}$ on a single node.

*Concepts: [BLAS and Dense Matrices](../concepts/BLAS_and_Dense_Matrices.md), [Arithmetic Intensity and Roofline Model](../concepts/Arithmetic_Intensity_and_Roofline_Model.md), [Cache Blocking (Loop Tiling)](../concepts/Cache_Blocking.md)*

#### (v) Sparse matrix solver — large fraction of peak? (3 marks)

**No.** Sparse matrix operations use formats like CSR with indirect addressing (`col_ind`, `row_ptr`). Arithmetic intensity is $O(1)$: each non-zero is multiplied once, then the result is accumulated; data has to be streamed from DRAM with non-contiguous access patterns that defeat the cache. Performance is **memory-bandwidth-bound**, not compute-bound. Typical sparse solvers achieve ~5–10% of $R_{peak}$ on the same node where DGEMM hits 90%+.

*Concepts: [Sparse Matrices and CSR](../concepts/Sparse_Matrices_and_CSR.md), [Arithmetic Intensity and Roofline Model](../concepts/Arithmetic_Intensity_and_Roofline_Model.md)*

---

### 3(b) Reconstructing a CSR matrix (9 marks)

```
vals    = [ 3,  1,  9, 13,  1,  8, 10 ]   (nnz = 7)
col_ind = [ 2,  1,  2,  4,  4,  2,  4 ]
row_ptr = [ 1,  2,  5,  6,  8 ]           (4 rows + sentinel)
```

`row_ptr` has 5 entries, so the matrix has 4 rows. The largest column index is 4, so it's a **4 × 4 matrix**.

**Decoding row-by-row** (1-indexed):

- **Row 1:** entries from index `row_ptr[1] = 1` up to (but not including) `row_ptr[2] = 2`. So entry 1 only.
  - `vals[1] = 3` at column `col_ind[1] = 2` → row 1 is `[ 0, 3, 0, 0 ]`.

- **Row 2:** entries 2 to 4 (i.e. indices 2, 3, 4).
  - `vals[2] = 1` at column 1
  - `vals[3] = 9` at column 2
  - `vals[4] = 13` at column 4 → row 2 is `[ 1, 9, 0, 13 ]`.

- **Row 3:** entries 5 to 5 (just index 5).
  - `vals[5] = 1` at column 4 → row 3 is `[ 0, 0, 0, 1 ]`.

- **Row 4:** entries 6 to 7.
  - `vals[6] = 8` at column 2
  - `vals[7] = 10` at column 4 → row 4 is `[ 0, 8, 0, 10 ]`.

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

### 3(c) Advection equation cost scaling

CFL: $\Delta t = C \dfrac{\Delta x}{v_{max}}$.

#### (i) 1-D N grid points vs 3-D N × N × N grid points (2 marks)

Grid points: $N$ (1-D) vs $N^3$ (3-D). With same number of time steps, total work scales with grid points:

**The 3-D calculation costs $N^2$ times more than 1-D.**

*Concepts: [Advection Equation](../concepts/Advection_Equation.md), [Numerical Stability and CFL](../concepts/Numerical_Stability_and_CFL.md)*

#### (ii) 3-D cost when Δx is reduced by 10 (4 marks)

Three things change:

1. **Grid points per dimension** scale as $1/\Delta x$, so they grow by ×10. In 3-D, total grid points grow by $10^3 = 1000$.
2. **Time step** by CFL scales as $\Delta x$, so $\Delta t$ shrinks by ×10.
3. **Number of time steps** to reach the same end time grows by ×10.

Total cost = points × time steps:
$$\text{factor} = 1000 \times 10 = 10\,000$$

**Cost grows by a factor of 10 000.**

(Compare with the 2-D *diffusion* equation in ECM3446-25May Q3(c)(ii): same factor of 10 000, but for very different reasons — 2-D × 100 spatial × 100 temporal vs 3-D × 1000 spatial × 10 temporal. The diffusion case has worse temporal scaling because $\Delta t \propto (\Delta x)^2$.)

*Concepts: [Advection Equation](../concepts/Advection_Equation.md), [Numerical Stability and CFL](../concepts/Numerical_Stability_and_CFL.md), [Diffusion Equation](../concepts/Diffusion_Equation.md)*

#### (iii) Navier-Stokes: v_max grows with resolution — larger or smaller cost? (3 marks)

**Larger cost.** The CFL condition $\Delta t \le C \Delta x / v_{max}$ means $\Delta t$ shrinks both because $\Delta x$ shrank *and* because $v_{max}$ rose. So the number of time steps grows faster than just the spatial-resolution factor would suggest.

Concretely: if $\Delta x$ falls by ×10 and $v_{max}$ rises by some factor $\alpha > 1$, then $\Delta t$ falls by $10\alpha$ and the number of time steps grows by $10\alpha$ (vs ×10 in the constant-$v_{max}$ case). Total cost in 3-D becomes $1000 \times 10\alpha = 10\,000 \alpha$ — **larger by a factor of $\alpha$ compared to a solver where $v_{max}$ is constant.**

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
