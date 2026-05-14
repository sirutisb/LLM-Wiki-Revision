---
title: "Week 6 Practice Questions: Memory and Cache"
tags: [hpc, week-6, memory, cache, roofline, numa, practice]
date: 2026-05-14
---

# Week 6 Practice Questions: Memory and Cache

> **Scope:** Memory hierarchy, cache levels, locality, cache misses, cache blocking (loop tiling), arithmetic intensity, roofline model (including cache-aware variant), NUMA, first-touch policy, hybrid MPI+OpenMP, and problem-size effects on benchmarking.

---

## Section A: Short Answer / Definitions

---

### Q1
**Define the term "memory hierarchy" and explain why it exists in modern HPC processors.**

**Model Answer (4 marks)**
- The memory hierarchy is a layered system of storage organised by speed, size, and cost. (1)
- Accessing main memory (DRAM) takes approximately 100 clock cycles, far longer than the CPU can execute instructions. Without a hierarchy the CPU would stall most of the time waiting for data. (1)
- Faster levels (registers, L1, L2, L3 cache) are smaller and physically closer to the processor, reducing latency. (1)
- The hierarchy exploits the observation that programs typically reuse a small working set repeatedly (temporal locality), so keeping that set in fast cache avoids repeated slow DRAM accesses. (1)

---

### Q2
**State the typical sizes and access latencies for each level of the memory hierarchy, from registers down to disk storage. Explain the trade-off involved.**

**Model Answer (5 marks)**

| Level | Typical Size | Approximate Latency |
|---|---|---|
| Registers | < 1 KB | < 1 cycle |
| L1 Cache | 32–64 KB per core | ~4 cycles |
| L2 Cache | 256 KB – 1 MB per core | ~12 cycles |
| L3 Cache | 8–64 MB shared | ~40 cycles |
| Main Memory (DRAM) | 16–512 GB | ~100 cycles |
| Disk / SSD | TB range | Millions of cycles |

- (1 mark for each level with correct trend — accept approximate values)
- The trade-off: faster memory is more expensive per byte and physically larger circuits, so only small amounts can be placed close to the processor. (1)
- Cost per byte increases dramatically as you move towards the CPU, so the hierarchy is a compromise between speed and capacity. (1)

---

### Q3
**What is a cache line? How does it relate to spatial locality?**

**Model Answer (3 marks)**
- A cache line is the smallest unit of data transfer between main memory and cache, typically 64 bytes on modern x86 processors. (1)
- When a single byte or word is requested, the entire 64-byte cache line containing it is loaded into cache. (1)
- Spatial locality means that data near a recently accessed address is likely to be needed soon. If a program accesses memory sequentially (stride-1 access), subsequent elements will already be in the cache line just loaded, dramatically reducing cache misses. (1)

---

### Q4
**Distinguish between temporal locality and spatial locality. For each, give one concrete programming example that exploits it.**

**Model Answer (4 marks)**
- **Temporal locality:** A memory location accessed recently is likely to be accessed again soon. Example: a loop variable `i` used as an array index — it is read and incremented on every iteration, remaining in a register or L1 cache. (2)
- **Spatial locality:** Memory locations near a recently accessed location are likely to be accessed soon. Example: iterating over a 1D array `for (int i = 0; i < N; i++) sum += a[i];` — each element is adjacent in memory, so successive accesses hit the same or adjacent cache lines. (2)

---

### Q5
**Name the three classical categories of cache miss and briefly describe each.**

**Model Answer (3 marks)**
- **Compulsory miss (cold miss):** Occurs the very first time a data block is accessed. The data has never been in cache and must be fetched from memory regardless of cache size. (1)
- **Capacity miss:** Occurs when the working set is too large to fit in the cache. Even with perfect replacement policy, data is evicted and must be re-fetched. (1)
- **Conflict miss:** Occurs in direct-mapped or set-associative caches when multiple data blocks compete for the same cache set, causing evictions even though the cache is not full. (1)

---

### Q6
**What is memory bandwidth and how does it differ from memory latency? Which is typically the dominant bottleneck in large-scale HPC applications?**

**Model Answer (3 marks)**
- **Latency** is the time delay between issuing a memory request and receiving the first byte of data (measured in nanoseconds or clock cycles). (1)
- **Bandwidth** is the sustained rate at which data can be transferred between memory and the CPU (measured in GB/s). (1)
- In large HPC applications that operate on data sets far exceeding cache size, memory **bandwidth** is typically the dominant bottleneck, because the CPU is continuously streaming large arrays and the bandwidth limit is hit before latency dominates. (1)

---

### Q7
**What does it mean for an algorithm to be "memory-bound" versus "compute-bound"?**

**Model Answer (2 marks)**
- **Memory-bound:** The algorithm's performance is limited by the rate at which data can be transferred from memory to the processor. The CPU is frequently idle waiting for data. Increasing FLOP/s of the processor would not improve performance. (1)
- **Compute-bound:** The algorithm's performance is limited by the number of floating-point operations the CPU can execute per second. Data arrives fast enough that the CPU is kept fully occupied. Increasing memory bandwidth would not improve performance. (1)

---

## Section B: Roofline Model

---

### Q8
**A system has the following specifications:**
- **Peak compute performance (R_peak):** 100 GFLOP/s
- **Peak memory bandwidth:** 20 GB/s

**(a)** Write the formula for the Roofline attainable performance P as a function of arithmetic intensity I.

**(b)** Calculate the **ridge point** (the arithmetic intensity at which the transition from memory-bound to compute-bound occurs).

**(c)** A matrix-vector multiplication kernel has an arithmetic intensity of 0.25 FLOP/byte. Is it memory-bound or compute-bound on this system? What is its performance ceiling according to the Roofline model?

**(d)** A dense matrix-matrix multiplication achieves an arithmetic intensity of 8 FLOP/byte. Is it memory-bound or compute-bound? What is its performance ceiling?

**Model Answer (8 marks)**

**(a)** (2 marks)
```
P = min(R_peak, Bandwidth × I)
P = min(100 GFLOP/s, 20 GB/s × I)
```

**(b)** (2 marks)
The ridge point is where the two limits are equal:
```
Bandwidth × I_ridge = R_peak
20 × I_ridge = 100
I_ridge = 5 FLOP/byte
```

**(c)** (2 marks)
- AI = 0.25 FLOP/byte < 5 FLOP/byte (ridge point) → **memory-bound**
- Performance ceiling: P = 20 GB/s × 0.25 FLOP/byte = **5 GFLOP/s**
  (only 5% of peak compute is theoretically achievable)

**(d)** (2 marks)
- AI = 8 FLOP/byte > 5 FLOP/byte (ridge point) → **compute-bound**
- Performance ceiling: P = min(100, 20 × 8) = min(100, 160) = **100 GFLOP/s**
  (limited by peak compute, not memory bandwidth)

---

### Q9
**Explain the "Cache-Aware Roofline Model." How does it differ from the basic Roofline model, and what additional information does it provide to the programmer?**

**Model Answer (5 marks)**
- The basic Roofline model uses a single memory bandwidth value (DRAM bandwidth), producing one slanted "slope" and one horizontal "roof." (1)
- In practice, CPUs have a multi-level memory hierarchy (L1, L2, L3, DRAM), each with significantly different bandwidths. The L1 cache may deliver data 10–100x faster than DRAM. (1)
- The cache-aware model introduces **multiple slanted ceilings** — one for each cache level. The L1 roof is the steepest (fastest), DRAM is the shallowest. (1)
- If an algorithm's working set fits in L2, it sits under the L2 bandwidth roof rather than the slow DRAM roof, achieving much higher performance at the same arithmetic intensity. (1)
- This explains why cache blocking dramatically improves performance even without changing the arithmetic intensity: it lifts the kernel from the DRAM bandwidth ceiling to a faster cache ceiling. (1)

---

### Q10
**A system has three cache levels with the following peak bandwidths:**
- L1: 1000 GB/s
- L2: 200 GB/s
- L3: 80 GB/s
- DRAM: 25 GB/s
- **R_peak:** 500 GFLOP/s

**A stencil kernel has arithmetic intensity I = 1.5 FLOP/byte.**

**(a)** Compute the attainable performance ceiling for this kernel under each bandwidth level.

**(b)** If the working set fits in L3, what performance ceiling applies? If it is forced to DRAM, what is the ceiling?

**(c)** What does this demonstrate about cache blocking?

**Model Answer (6 marks)**

**(a)** (3 marks — 0.5 per bandwidth level, allow 0.5 for comparison with R_peak)
```
L1:   min(500, 1000 × 1.5) = min(500, 1500) = 500 GFLOP/s  (compute-bound under L1)
L2:   min(500,  200 × 1.5) = min(500,  300) = 300 GFLOP/s
L3:   min(500,   80 × 1.5) = min(500,  120) = 120 GFLOP/s
DRAM: min(500,   25 × 1.5) = min(500,   37.5) = 37.5 GFLOP/s
```

**(b)** (2 marks)
- Working set in L3: ceiling = **120 GFLOP/s**
- Working set in DRAM: ceiling = **37.5 GFLOP/s**
- Difference factor: 120 / 37.5 = **3.2x** potential speedup from keeping data in L3 vs. DRAM.

**(c)** (1 mark)
Cache blocking keeps the working set in a faster cache level without altering the algorithm's arithmetic intensity, moving the kernel to a higher performance ceiling. A 3x+ speedup is achievable here purely from better data locality.

---

### Q11
**On a log-log Roofline plot, describe what the axes represent and sketch (in words) the shape of the performance limit curve. Mark clearly where the ridge point is and label the memory-bound and compute-bound regions.**

**Model Answer (4 marks)**
- X-axis: Arithmetic Intensity (FLOP/byte) on a log scale. (0.5)
- Y-axis: Attainable Performance (GFLOP/s) on a log scale. (0.5)
- The curve consists of two segments: (1)
  - A slanted line rising from lower-left (slope = memory bandwidth on log-log axes) — this is the **memory-bound region** where P = Bandwidth × I.
  - A flat horizontal line at R_peak — this is the **compute-bound region**.
- The two lines meet at the **ridge point** (I_ridge = R_peak / Bandwidth). (1)
- To the left of the ridge point: memory-bound. To the right: compute-bound. (1)

---

## Section C: Arithmetic Intensity Calculations

---

### Q12
**Consider the following C code performing vector addition:**

```c
// Arrays a, b, c each have N double-precision (8-byte) elements
for (int i = 0; i < N; i++) {
    c[i] = a[i] + b[i];
}
```

**(a)** Count the number of floating-point operations per loop iteration.

**(b)** Count the bytes of data movement per loop iteration (assume all data comes from/goes to DRAM, and no cache reuse between iterations).

**(c)** Calculate the arithmetic intensity.

**(d)** Is this kernel memory-bound or compute-bound on a typical HPC system with a ridge point of 5 FLOP/byte? What implication does this have for optimisation?

**Model Answer (6 marks)**

**(a)** (1 mark)
1 FLOP per iteration (one addition: `a[i] + b[i]`).

**(b)** (2 marks)
- Read `a[i]`: 8 bytes
- Read `b[i]`: 8 bytes
- Write `c[i]`: 8 bytes
- Total: **24 bytes** per iteration

**(c)** (1 mark)
```
AI = 1 FLOP / 24 bytes ≈ 0.042 FLOP/byte
```

**(d)** (2 marks)
- 0.042 << 5 → **heavily memory-bound**
- Implication: increasing the CPU's FLOP/s (e.g., adding more cores or using SIMD) will not improve performance. The bottleneck is memory bandwidth. The only meaningful optimisation is reducing data movement — e.g., fusing this loop with adjacent loops to increase reuse of loaded data.

---

### Q13
**A finite-difference stencil in 1D updates each element of array `u` using its two neighbours:**

```c
// u_new[i] = c0*u[i-1] + c1*u[i] + c2*u[i+1]
// c0, c1, c2 are scalar constants
for (int i = 1; i < N-1; i++) {
    u_new[i] = c0*u[i-1] + c1*u[i] + c2*u[i+1];
}
```

**(a)** Count FLOPs per iteration (count multiply and add as separate operations).

**(b)** Estimate bytes moved per iteration, assuming `u` and `u_new` are double-precision arrays and ignoring cache effects (streaming from DRAM).

**(c)** Calculate the arithmetic intensity.

**(d)** Would cache blocking help this kernel? Explain.

**Model Answer (6 marks)**

**(a)** (2 marks)
- 3 multiplications: `c0*u[i-1]`, `c1*u[i]`, `c2*u[i+1]`
- 2 additions: summing the three products
- Total: **5 FLOPs** per iteration

**(b)** (2 marks)
- Read 3 elements of `u`: 3 × 8 = 24 bytes (with perfect reuse, only ~8 bytes new data per iteration due to sliding window, but ignoring cache: 24 bytes)
- Write 1 element of `u_new`: 8 bytes
- Total (ignoring reuse): **32 bytes** per iteration
- With sliding-window reuse: ~16 bytes (1 new read + 1 write), giving AI ≈ 5/16 ≈ 0.31 FLOP/byte — accept either approach if explained.

**(c)** (1 mark)
Ignoring reuse: AI = 5/32 ≈ **0.16 FLOP/byte** (memory-bound)
With reuse: AI = 5/16 ≈ **0.31 FLOP/byte** (still memory-bound)

**(d)** (1 mark)
Cache blocking has **limited benefit** for a 1D stencil because temporal reuse is minimal — each element is only used once or twice before being overwritten. However, in 2D/3D stencils, blocking along spatial dimensions can significantly improve reuse. The 1D case is inherently low-AI and primarily benefits from reducing memory traffic via loop fusion rather than blocking.

---

### Q14
**For a naive dense matrix-matrix multiplication `C = A * B` of N×N matrices (double precision):**

**(a)** State the total number of floating-point operations.

**(b)** State the total bytes of data read/written (ignoring cache, reading all matrices from DRAM).

**(c)** Derive the arithmetic intensity as a function of N. What happens to AI as N grows?

**(d)** Compare this to vector addition and explain the implication for the Roofline model position of matrix multiplication.

**Model Answer (6 marks)**

**(a)** (1 mark)
For each of the N² elements of C: N multiplications and N additions = 2N FLOPs.
Total FLOPs = **2N³**

**(b)** (2 marks)
- Matrix A: N² × 8 bytes = 8N² bytes
- Matrix B: N² × 8 bytes = 8N² bytes
- Matrix C: N² × 8 bytes = 8N² bytes (write)
- Total: **24N²** bytes

**(c)** (2 marks)
```
AI = 2N³ / 24N² = N/12 FLOP/byte
```
As N grows, AI grows **linearly with N**. For large N (e.g., N=1000): AI ≈ 83 FLOP/byte — strongly compute-bound.

**(d)** (1 mark)
Vector addition has AI ≈ 0.042 FLOP/byte (fixed, independent of N) — always sits deep in the memory-bound region. Matrix multiplication's AI increases with N and for large matrices sits well to the right of the ridge point in the compute-bound region. This makes dense matrix multiply an excellent candidate for SIMD vectorization and core-level optimisation, while vector addition can only be improved by reducing memory traffic.

---

### Q15
**Consider this code:**

```c
double dot = 0.0;
for (int i = 0; i < N; i++) {
    dot += x[i] * y[i];
}
```

**(a)** Calculate the arithmetic intensity (x, y are double-precision arrays, result is a scalar accumulator in a register).

**(b)** A colleague suggests that on a machine with R_peak = 50 GFLOP/s and bandwidth = 40 GB/s, this kernel should achieve close to 50 GFLOP/s. Evaluate this claim.

**Model Answer (4 marks)**

**(a)** (2 marks)
- FLOPs per iteration: 1 multiply + 1 add = **2 FLOPs**
- Bytes per iteration: read x[i] (8B) + read y[i] (8B) = **16 bytes** (dot is accumulated in a register, no memory write per iteration)
- AI = 2 / 16 = **0.125 FLOP/byte**

**(b)** (2 marks)
- Ridge point = 50 / 40 = 1.25 FLOP/byte
- AI = 0.125 << 1.25 → **heavily memory-bound**
- Roofline ceiling: P = 40 × 0.125 = **5 GFLOP/s** (only 10% of peak)
- The colleague's claim is incorrect. The kernel cannot approach peak compute because it is memory-bound, not compute-bound.

---

## Section D: Cache Blocking (Loop Tiling)

---

### Q16
**The following code performs a naive matrix transpose of an N×N matrix:**

```c
// Naive transpose: B[j][i] = A[i][j]
for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
        B[j][i] = A[i][j];
    }
}
```

**(a)** Explain why this code has poor cache behaviour for large N. Refer to spatial locality and cache lines.

**(b)** Rewrite the code using cache blocking with block size `B` (use `B` as the variable name for block size to avoid confusion with matrix B — rename matrix B to `T` for transpose). Annotate the key loops.

**(c)** Explain how the blocked version improves cache performance.

**Model Answer (8 marks)**

**(a)** (3 marks)
- In C, 2D arrays are stored in **row-major order**: `A[i][0], A[i][1], ..., A[i][N-1]` are contiguous in memory.
- The read `A[i][j]` accesses a new element of row i each iteration — this is a **stride-1 (sequential) read** with good spatial locality, loading a full cache line of row i. (1)
- The write `T[j][i]` writes to column i of matrix T. In row-major layout, `T[0][i], T[1][i], ..., T[N-1][i]` are separated by N doubles (N × 8 bytes). For large N this is a **stride-N write**, meaning each write accesses a different cache line. (1)
- For large N (e.g., N=1024), the stride-N writes cause a cache miss on **every single write**, because each new row of T lands on a completely different cache line that has been evicted since it was last touched. The entire matrix T must be read from and written to DRAM repeatedly. (1)

**(b)** (3 marks)
```c
// Blocked transpose: block size BS
// T[j][i] = A[i][j]
for (int ii = 0; ii < N; ii += BS) {          // outer tile loop over rows of A
    for (int jj = 0; jj < N; jj += BS) {      // outer tile loop over cols of A
        // Process BS x BS block
        for (int i = ii; i < ii + BS && i < N; i++) {   // inner: rows in block
            for (int j = jj; j < jj + BS && j < N; j++) { // inner: cols in block
                T[j][i] = A[i][j];
            }
        }
    }
}
```
(Award marks for: outer tiled loops stepping by BS, inner loops bounded to block, correct index usage — 1 mark per feature)

**(c)** (2 marks)
- With blocking, the inner loops work on a BS×BS sub-block of A and T that fits in cache. (1)
- The BS columns of T that are written (`T[jj..jj+BS][ii..ii+BS]`) are loaded into cache once at the start of the inner block, reused for all BS rows, then evicted. This converts the stride-N access pattern into a cache-friendly block access, reducing cache misses on T by a factor of approximately BS. (1)

---

### Q17
**A developer is optimising a matrix multiplication kernel. The system's L1 cache is 32 KB. Matrices are stored as double-precision (8 bytes per element).**

**(a)** If we want three square blocks (sub-matrices of A, B, and C) to fit simultaneously in the 32 KB L1 cache, derive the maximum block size `BS`.**

**(b)** The developer uses `-O3` compiler optimisation and finds the performance improves significantly. Explain what the compiler may have done automatically.**

**(c)** The developer tries `BS = 256` on the same system. Explain what will likely happen to performance.**

**Model Answer (5 marks)**

**(a)** (2 marks)
Three BS×BS double matrices in cache: 3 × BS² × 8 bytes ≤ 32,768 bytes
```
BS² ≤ 32768 / 24 = 1365
BS ≤ √1365 ≈ 36.9
```
Maximum block size: **BS = 36** (or 32 as a power-of-2 practical choice). (Award marks for correct algebra and a reasonable answer in range 32–36)

**(b)** (2 marks)
With `-O3`, the compiler may auto-vectorize (SIMD), auto-unroll inner loops, and in some cases perform **automatic loop tiling / cache blocking** if it can determine there are no loop-carried dependencies. It may also use prefetch instructions to hide memory latency. (1 mark each for any two valid points)

**(c)** (1 mark)
BS = 256 means each block is 256×256 × 8 = 524,288 bytes ≈ 512 KB. Three such blocks require ~1.5 MB — far exceeding the 32 KB L1 cache and likely even the L2. The blocks will not fit in cache, causing frequent cache evictions and eliminating the benefit of blocking. Performance may be worse than a well-tuned smaller block size. The optimal block size must be chosen to match the hardware cache dimensions.

---

### Q18
**Without using code, explain in prose the concept of "loop tiling" as applied to a matrix operation. Your answer should explain the problem it solves, the mechanism, and the performance trade-off involved in choosing the tile size.**

**Model Answer (4 marks)**
- **Problem:** When operating on matrices too large to fit in cache, a naive nested loop will evict data from cache before it can be reused, resulting in repeated, expensive DRAM accesses. (1)
- **Mechanism:** Loop tiling restructures the iteration space into smaller "tiles" or "blocks" that fit within a target cache level. The outer loops advance through the matrix in steps of the tile size; the inner loops process one complete tile at a time. All operations on a tile complete before the tile's data is evicted. (1)
- **Benefit:** Data loaded from DRAM is reused multiple times within the cache rather than once. For matrix multiplication, this can increase arithmetic intensity by a factor proportional to the tile size. (1)
- **Tile size trade-off:** The tile must be small enough that all working data (e.g., three sub-matrices) fits simultaneously in the target cache level. Too small: overhead from loop management dominates. Too large: tiles exceed cache, defeating the purpose. Optimal tile size is hardware-specific and depends on cache capacity and associativity. (1)

---

## Section E: NUMA and First-Touch Policy

---

### Q19
**Explain what NUMA (Non-Uniform Memory Access) is and why it arises in modern multi-socket HPC nodes.**

**Model Answer (4 marks)**
- NUMA arises in systems with multiple processor sockets, each having its own physically attached RAM and its own integrated memory controller. (1)
- Accessing RAM on the same socket as the requesting core ("local access") is fast, traversing only the local memory controller. (1)
- Accessing RAM attached to a different socket ("remote access") requires the request to traverse a CPU-to-CPU interconnect (e.g., Intel QPI, AMD Infinity Fabric), introducing additional latency. (1)
- Because access time differs depending on the physical location of the memory, access is "non-uniform." On a dual-socket node, remote access can be 1.5–2x slower than local access, a significant penalty in bandwidth-bound workloads. (1)

---

### Q20
**Explain the Linux first-touch memory allocation policy. What is actually allocated when `malloc` is called?**

**Model Answer (3 marks)**
- When `malloc` is called, the OS allocates only a **virtual address space reservation** — a mapping in the process's page table. No physical RAM page is assigned at this point. (1)
- Physical memory is allocated only when a page is **first accessed** (read or written) — the "first touch." At that moment, the OS assigns a physical page from the memory bank closest to the CPU core that executed the first touch instruction. (1)
- Once placed, the physical page remains on that socket's memory controller for the lifetime of the allocation. It does not automatically migrate even if other sockets subsequently access it more frequently. (1)

---

### Q21
**The following OpenMP code initialises an array in a sequential loop and then processes it in parallel:**

```c
double *arr = malloc(N * sizeof(double));

// Initialise (sequential, runs on master thread — Socket 0, core 0)
for (int i = 0; i < N; i++) arr[i] = 0.0;

// Process in parallel (threads on both sockets)
#pragma omp parallel for
for (int i = 0; i < N; i++) result[i] = arr[i] * 2.0;
```

**(a)** Identify the performance problem this code has on a dual-socket NUMA system.

**(b)** Provide a corrected version of the code that resolves this problem.

**(c)** Explain why the corrected version improves performance.

**Model Answer (7 marks)**

**(a)** (3 marks)
- The sequential initialisation loop runs entirely on the master thread, which executes on Socket 0, core 0. (1)
- By the first-touch policy, every page of `arr` is first touched by Socket 0's core, so all physical pages are allocated in RAM Bank 0, attached to Socket 0's memory controller. (1)
- In the parallel computation, OpenMP threads on Socket 1 must fetch data from RAM Bank 0, crossing the slow CPU-to-CPU interconnect on every single memory access. This introduces a NUMA penalty on half the threads, degrading bandwidth for the entire parallel section. (1)

**(b)** (2 marks)
```c
double *arr = malloc(N * sizeof(double));

// Parallel initialisation — each thread first-touches its own portion
#pragma omp parallel for
for (int i = 0; i < N; i++) arr[i] = 0.0;

// Parallel computation — now data is local to each thread's socket
#pragma omp parallel for
for (int i = 0; i < N; i++) result[i] = arr[i] * 2.0;
```
(1 mark for adding `#pragma omp parallel for` to the initialisation; 1 mark for explanation/correct placement)

**(c)** (2 marks)
- With parallel initialisation, thread 0 (Socket 0) first-touches indices 0..N/2 → pages land in RAM Bank 0. Thread N_t/2 (Socket 1) first-touches indices N/2..N → pages land in RAM Bank 1. (1)
- During the parallel computation, each socket's threads access only their local RAM bank. No cross-socket traffic occurs, and both sockets' memory controllers contribute to total bandwidth, effectively doubling available bandwidth compared to the buggy version. (1)

---

### Q22
**Describe the hybrid MPI+OpenMP parallelisation strategy for a dual-socket NUMA node with 16 cores per socket (32 cores total). How does it avoid NUMA effects? Compare it to a pure OpenMP approach using all 32 threads.**

**Model Answer (6 marks)**

**Pure OpenMP (32 threads across both sockets):**
- 32 OpenMP threads span both sockets. Unless great care is taken with parallel initialisation, data may be allocated predominantly on one socket. (1)
- Even with correct parallel initialisation, OpenMP's shared address space means that load imbalance or false sharing can cause inter-socket communication. Managing NUMA affinity requires explicit use of tools like `numactl` or `OMP_PROC_BIND`. (1)

**Hybrid MPI + OpenMP (1 MPI process per socket, 16 OpenMP threads each):**
- Launch 2 MPI processes — one pinned to each socket. Each MPI process has an independent address space. (1)
- Each process calls `malloc` and initialises its own data. All first-touches for each process occur on that process's socket, so all memory is local. (1)
- Each process then spawns 16 OpenMP threads, all confined to its socket. All threads access only local RAM. No cross-socket traffic occurs. (1)
- This approach achieves full utilisation of both sockets' memory bandwidth and avoids NUMA penalties entirely, without requiring any special NUMA-awareness in the OpenMP code. (1)

---

## Section F: Problem Size and Benchmarking

---

### Q23
**A researcher is testing the scalability of a climate model. The production run uses a 1 km grid (10 GB memory footprint, 1,440 time steps, runs for 5 hours). To speed up testing, she reduces the grid to 10 km resolution (100 MB memory footprint) and runs the same number of time steps.**

**(a)** Identify the problem with this approach.

**(b)** Propose a correct alternative approach that preserves predictive value for the production run.

**(c)** Explain the "golden rule" for choosing representative test cases in HPC benchmarking.**

**Model Answer (5 marks)**

**(a)** (2 marks)
- The 100 MB footprint fits entirely within L3 cache (typically 8–64 MB on modern CPUs) or at worst the L3 region. The production 10 GB footprint resides entirely in DRAM and is bandwidth-limited. (1)
- The small test case will show artificially high performance (cache-resident), masking the memory bandwidth bottleneck. Optimisations that improve cache performance (e.g., vectorisation, instruction-level parallelism) will look effective, but optimisations needed for the real problem (e.g., cache blocking, data layout) will be invisible. Performance measurements will be misleading. (1)

**(b)** (2 marks)
Keep the 1 km resolution (10 GB memory footprint) but drastically reduce the number of time steps — e.g., run 10 steps instead of 1,440. The test finishes quickly (minutes instead of hours) while retaining the same per-step memory access pattern and DRAM bandwidth bottleneck. (2)

**(c)** (1 mark)
**Golden rule:** Maintain the representative data size (memory footprint) but reduce the total amount of work (iterations, time steps, queries). Never shrink the problem's data footprint — shrink its duration instead. This ensures the test experiences the same memory hierarchy behaviour as the production run.

---

### Q24
**The table below shows benchmark results for a matrix operation at different problem sizes. Explain the observed pattern.**

| N (matrix dimension) | Performance (GFLOP/s) |
|---|---|
| 64 | 45 |
| 128 | 42 |
| 512 | 38 |
| 1024 | 12 |
| 2048 | 10 |
| 4096 | 9 |

**Model Answer (4 marks)**
- For small N (64–512): the matrix fits in L1/L2/L3 cache. The operation is cache-resident, data is delivered at high bandwidth, and performance is close to peak compute. The slight decline from N=64 to N=512 reflects the transition through L1 → L2 → L3, each with lower bandwidth. (2)
- At N≈1024–4096: the matrix no longer fits in any cache level. Data must stream from DRAM, which has much lower bandwidth. Performance drops sharply (from ~38 to ~12 GFLOP/s) as the kernel becomes heavily memory-bound. (1)
- The near-flat performance from N=1024 onward indicates the kernel has hit the DRAM bandwidth ceiling, and further increases in N do not change the bottleneck — it remains memory-bound throughout. (1)

---

## Section G: Multi-Part Exam Questions

---

### Q25 (Multi-Part: Memory Hierarchy and Roofline)

**A dual-socket HPC node has the following specifications:**
- Each socket: 16-core CPU, 32 KB L1 cache per core, 256 KB L2 per core, 20 MB L3 shared per socket
- DRAM: 128 GB total (64 GB per socket), bandwidth = 50 GB/s per socket (100 GB/s total)
- Peak compute: 64 GFLOP/s per socket (128 GFLOP/s total)
- Cache bandwidths: L1 = 2 TB/s, L2 = 400 GB/s, L3 = 150 GB/s per socket

Consider the following kernel operating on N-element double-precision arrays:

```c
// SAXPY: y[i] = a * x[i] + y[i]
for (int i = 0; i < N; i++) {
    y[i] = a * x[i] + y[i];
}
```

**(a)** Calculate the arithmetic intensity of this SAXPY kernel. (2 marks)

**(b)** Calculate the ridge point of this system using DRAM bandwidth. (1 mark)

**(c)** Determine whether SAXPY is memory-bound or compute-bound on this system. (1 mark)

**(d)** If N = 1,000 (total data ≈ 16 KB), under which bandwidth roof does SAXPY operate? What is the attainable performance ceiling? (2 marks)

**(e)** If N = 10,000,000 (total data ≈ 160 MB >> all caches), what is the attainable GFLOP/s? (1 mark)

**(f)** A programmer proposes to improve performance by using AVX-512 SIMD to execute 8 double operations simultaneously. Will this help? Justify your answer using the Roofline model. (2 marks)

**(g)** What optimisation strategy would actually improve performance for large N? (1 mark)

**Model Answer (10 marks)**

**(a)** (2 marks)
- Per iteration: 1 multiply (`a * x[i]`) + 1 add (+ `y[i]`) = **2 FLOPs**
- Bytes per iteration: read x[i] (8B) + read y[i] (8B) + write y[i] (8B) = **24 bytes**
- AI = 2 / 24 = **0.083 FLOP/byte**

**(b)** (1 mark)
Ridge point = R_peak / Bandwidth = 128 / 100 = **1.28 FLOP/byte**

**(c)** (1 mark)
AI = 0.083 << 1.28 → **heavily memory-bound**

**(d)** (2 marks)
N=1000: x and y arrays = 2 × 1000 × 8 = 16 KB total. This fits comfortably in the **L1 cache** (32 KB per core).
Under L1: P = min(128, 2000 × 0.083) = min(128, 166) → limited by **R_peak = 128 GFLOP/s** (the kernel is compute-bound when cache-resident in L1, because L1 bandwidth is so high it is no longer the bottleneck).

**(e)** (1 mark)
N=10M: 160 MB >> all caches → data streams from DRAM.
P = min(128, 100 × 0.083) = min(128, **8.3 GFLOP/s**) → ceiling is **8.3 GFLOP/s** (only 6.5% of peak).

**(f)** (2 marks)
AVX-512 increases the **peak compute rate** (R_peak). However, since SAXPY is memory-bound (AI = 0.083 << ridge point), the bottleneck is DRAM bandwidth, not compute. Raising R_peak merely shifts the horizontal roof upward, which does not change the performance ceiling on the slanted memory-bandwidth line. (1)
The attainable performance of 8.3 GFLOP/s is determined by `Bandwidth × AI`, not by R_peak. AVX-512 will have negligible effect for large N. (1)

**(g)** (1 mark)
To improve performance for large N, reduce memory traffic. Strategies include: **loop fusion** (combine SAXPY with a subsequent loop to increase AI by reusing loaded data), or ensuring stride-1 access (already the case here). Alternatively, use **multithreading** to exploit combined per-socket bandwidth if only one socket is currently used, increasing effective bandwidth up to 100 GB/s total.

---

### Q26 (Multi-Part: Cache Blocking and Arithmetic Intensity)

**Consider the following naive matrix-matrix multiplication for N×N double-precision matrices A, B, C:**

```c
for (int i = 0; i < N; i++)
    for (int j = 0; j < N; j++)
        for (int k = 0; k < N; k++)
            C[i][j] += A[i][k] * B[k][j];
```

**(a)** Identify the problematic memory access pattern in this code for large N. Which array, and what type of access pattern does it exhibit? (3 marks)

**(b)** Explain what happens in terms of cache performance when computing one row of C (i.e., fixed i, varying j and k) for large N. (2 marks)

**(c)** Rewrite the loop nest using cache blocking with tile size T. (3 marks)

**(d)** A system has an L2 cache of 512 KB. Calculate the maximum tile size T such that the active blocks of A, B, and C fit simultaneously in L2. (2 marks)

**(e)** Explain why cache blocking increases the effective arithmetic intensity of this kernel. (2 marks)

**(f)** State one other optimisation (besides cache blocking) that is commonly applied to matrix multiplication to further improve performance. (1 mark)

**Model Answer (13 marks)**

**(a)** (3 marks)
- Matrix **A**: accessed as `A[i][k]` — for fixed i, k varies in the inner loop. In C row-major layout, `A[i][0..N-1]` is contiguous → **stride-1 (good spatial locality)**. (1)
- Matrix **C**: accessed as `C[i][j]` — for fixed i, j is the middle loop → stride-1 within the j-loop iteration, reused across k → **good temporal locality** (same element updated N times). (1)
- Matrix **B**: accessed as `B[k][j]` — for fixed j (outer over j), k varies in the inner loop. In row-major layout, `B[0][j], B[1][j], ..., B[N-1][j]` are separated by N doubles → **stride-N (poor spatial locality)**. Each access to a new k loads a new cache line containing only one useful element. (1)

**(b)** (2 marks)
- For fixed i and j, the inner k-loop accesses a full row of A (good, stride-1) and a full column of B (bad, stride-N). For large N (e.g., N=1024), the column of B spans N×8 = 8,192 bytes per step, touching a different cache line each iteration. (1)
- By the time the j-loop moves to the next j, the column of B just accessed has been evicted from cache. B must be re-read from DRAM for every (i,j) pair → N² cache misses on B, each fetching from DRAM. Performance is dominated by DRAM bandwidth. (1)

**(c)** (3 marks)
```c
// Cache-blocked matrix multiplication, tile size T
for (int ii = 0; ii < N; ii += T)
    for (int jj = 0; jj < N; jj += T)
        for (int kk = 0; kk < N; kk += T)
            // Multiply T×T sub-block of A by T×T sub-block of B, add to C
            for (int i = ii; i < ii + T && i < N; i++)
                for (int j = jj; j < jj + T && j < N; j++)
                    for (int k = kk; k < kk + T && k < N; k++)
                        C[i][j] += A[i][k] * B[k][j];
```
(1 mark per outer tiled loop structure; 1 mark for correct inner loop bounds — total 3)

**(d)** (2 marks)
Three T×T double matrices in 512 KB L2:
```
3 × T² × 8 bytes ≤ 512 × 1024 = 524,288 bytes
T² ≤ 524,288 / 24 = 21,845
T ≤ √21,845 ≈ 147.8
```
Maximum tile size: **T = 147** (or 128 as the largest power-of-two below this). (Award marks for correct arithmetic.)

**(e)** (2 marks)
- In the naive version, each element of B is loaded from DRAM N² times (once per (i,j) pair). In the blocked version, each T×T block of B is loaded from DRAM once but reused T times within the block computation. (1)
- The total data movement from DRAM is reduced by a factor of T for matrix B. Since FLOPs remain 2N³ but bytes transferred fall, the effective AI = 2N³ / (reduced bytes) increases proportionally. For large T, the kernel moves from memory-bound toward compute-bound. (1)

**(f)** (1 mark)
Any one of: **SIMD vectorisation** (AVX2/AVX-512), **loop unrolling** (reducing loop overhead and enabling better instruction scheduling), **using an optimised BLAS library** (e.g., OpenBLAS, MKL) which implements highly tuned blocking and SIMD internally, or **prefetching** (software or hardware prefetch instructions to hide memory latency).

---

### Q27 (Multi-Part: NUMA, First-Touch, and Hybrid Parallelism)

**A cluster node has 2 sockets, each with 12 cores and 64 GB of local RAM (128 GB total). A fluid dynamics application allocates a large 3D grid using a single `malloc` call and then runs the following code:**

```c
// Phase 1: Initialise grid (called before parallelisation is set up)
init_grid(grid, N);  // sequential, runs on Socket 0

// Phase 2: Time-stepping loop
for (int step = 0; step < MAX_STEPS; step++) {
    #pragma omp parallel for schedule(static)
    for (int i = 0; i < N; i++) {
        update_cell(grid, i);  // reads and writes grid[i] and its neighbours
    }
}
```

**(a)** Identify the NUMA issue with this code. Be specific about which hardware resources are involved and where the bottleneck arises. (3 marks)

**(b)** On a simple memory-bandwidth model, if one socket provides 40 GB/s and cross-socket bandwidth is 15 GB/s, estimate the combined effective bandwidth available to the parallel section versus the theoretical maximum if memory were perfectly distributed. (3 marks)

**(c)** Propose two modifications to the code that would mitigate the NUMA issue. (4 marks)

**(d)** Explain the architectural argument for using **one MPI process per socket with 12 OpenMP threads each** instead of **24 OpenMP threads across the whole node**. What happens to the address spaces? (3 marks)

**Model Answer (13 marks)**

**(a)** (3 marks)
- `init_grid` runs sequentially on Socket 0 (core 0). Under first-touch policy, every page of `grid` is first-touched by Socket 0 → all physical memory allocated in Socket 0's RAM Bank (64 GB on Socket 0). (1)
- In Phase 2, `#pragma omp parallel for` distributes iterations across all 24 cores (12 per socket). Cores on Socket 1 (cores 12–23) must access `grid` data that physically resides in Socket 0's RAM Bank. (1)
- Every memory access by Socket 1 threads must cross the CPU-to-CPU interconnect to Socket 0's memory controller, which throttles throughput to the cross-socket link speed (much lower than local bandwidth). Socket 0 also has to service both its own 12 threads and 12 threads from Socket 1 simultaneously, saturating Socket 0's memory controller. (1)

**(b)** (3 marks)
- 12 threads on Socket 0 → served by Socket 0's local controller at 40 GB/s.
- 12 threads on Socket 1 → served via cross-socket link at 15 GB/s.
- **Effective combined bandwidth ≈ 40 + 15 = 55 GB/s** (assume Socket 0 can handle both local and remote requests, capped at 40 GB/s; cross-socket adds 15 GB/s). (2)
  *(Accept: Socket 0 saturates at 40 GB/s handling all 24 threads, giving ~40 GB/s effective — both interpretations are valid if justified.)*
- **Theoretical maximum** with perfect distribution: 40 + 40 = **80 GB/s** (both local controllers serving their own 12 threads).
- The NUMA bug costs approximately 25–40 GB/s of bandwidth — a significant fraction. (1)

**(c)** (4 marks) — 2 marks per strategy, 2 strategies required:

**Strategy 1 — Parallel initialisation:**
```c
#pragma omp parallel for schedule(static)
for (int i = 0; i < N; i++) init_cell(grid, i);
```
Distribute the initialisation loop across all 24 threads with the same static schedule as the computation loop. Socket 1 threads first-touch their portion → pages land in Socket 1's RAM. (2)

**Strategy 2 — Hybrid MPI+OpenMP:**
Split the grid domain between two MPI processes (one per socket). Each MPI process independently allocates and initialises its half of the grid, performing all first-touches locally. Each process then runs 12 OpenMP threads within its socket. No cross-socket memory access occurs. (2)

**(d)** (3 marks)
- **Address space isolation:** Each MPI process has a completely separate virtual address space. `malloc` in process 0 allocates from Socket 0's RAM; `malloc` in process 1 allocates from Socket 1's RAM. There is no shared memory between processes, so no possibility of first-touch contamination from another socket. (1)
- **Pure OpenMP (24 threads):** All 24 threads share a single address space with a single `malloc`. Unless explicitly parallelised and bound to sockets with correct scheduling, initialisation defaults to a single thread → all memory on Socket 0. Thread binding and `OMP_PROC_BIND` must be correctly set. (1)
- **Conclusion:** The MPI+OpenMP approach makes NUMA-awareness automatic and architecturally guaranteed — each socket's data lives on that socket's RAM by construction, regardless of initialisation patterns. This is why one-MPI-process-per-socket is the standard pattern in production HPC codes. (1)

---

*End of Week 6 Practice Questions*

---

## Quick Reference: Key Formulas

```
Arithmetic Intensity:  AI = FLOPs / Bytes
Roofline attainable:   P  = min(R_peak, Bandwidth × AI)
Ridge point:           I_ridge = R_peak / Bandwidth
Vector addition AI:    1 FLOP / 24 bytes ≈ 0.042 FLOP/byte  (2 reads + 1 write, double)
Dot product AI:        2 FLOPs / 16 bytes = 0.125 FLOP/byte  (2 reads, double)
SAXPY AI:              2 FLOPs / 24 bytes ≈ 0.083 FLOP/byte  (2 reads + 1 write, double)
Dense MatMul AI:       2N³ / 24N² = N/12 FLOP/byte
Cache block size:      BS ≤ sqrt(Cache_size / (num_matrices × bytes_per_element))
```

## Topic Coverage Checklist

| Topic | Questions |
|---|---|
| Memory hierarchy levels & latency | Q1, Q2 |
| Cache lines & spatial locality | Q3, Q4 |
| Cache miss types | Q5 |
| Bandwidth vs latency | Q6 |
| Memory-bound vs compute-bound | Q7, Q12, Q15 |
| Roofline formula & ridge point | Q8 |
| Cache-aware Roofline | Q9, Q10, Q25d |
| Roofline log-log plot | Q11 |
| Arithmetic intensity (vector ops) | Q12, Q13, Q15 |
| Arithmetic intensity (matrix mult) | Q14, Q25a |
| Cache blocking — explanation | Q16a, Q18 |
| Cache blocking — implementation | Q16b, Q26c |
| Cache blocking — block size | Q17a, Q26d |
| Compiler optimisation | Q17b |
| Problem size & benchmarking | Q23, Q24 |
| NUMA architecture | Q19, Q27a |
| First-touch policy | Q20, Q21a, Q27a |
| First-touch fix (parallel init) | Q21b, Q27c |
| Hybrid MPI+OpenMP | Q22, Q27d |
| SAXPY multi-part | Q25 (all) |
| Matrix multiply multi-part | Q26 (all) |
| NUMA multi-part | Q27 (all) |
