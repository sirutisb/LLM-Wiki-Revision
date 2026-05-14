---
title: "Week 10 Practice Questions: GPUs and Accelerators"
tags: [hpc, week-10, gpu, openmp, practice]
date: 2026-05-14
---

# Week 10 Practice Questions: GPUs and Accelerators

> **Coverage:** GPU as accelerator, energy efficiency & Green500, Streaming Multiprocessors, CUDA core counts, thread blocks, warps, SIMD/SIMT execution, branch divergence, memory coalescing, occupancy, latency hiding, PCIe bottleneck, host-to-device transfer, OpenMP offloading directives, `map` clauses, and data-movement optimisation.
>
> Source pages: `wiki/concepts/Graphics_Processing_Units_GPUs.md`, `wiki/concepts/GPU_Architecture_and_Warps.md`, `wiki/concepts/GPU_Programming_and_OpenMP_Offloading.md`, `wiki/final_prep/Accelerators_and_GPUs.md`

---

## Section A: Short Answer / Definitions

### Q1. What is a Streaming Multiprocessor (SM)?

**Model Answer (3 marks)**

- An SM is the fundamental compute building block of an NVIDIA GPU. [1]
- Each SM contains its own collection of floating-point cores (e.g. Pascal: 32 DP cores + 64 SP cores), load/store units (16), special function units (16), a register file, shared memory, and an L1 cache. [1]
- Thread blocks are scheduled onto individual SMs; all threads in a block execute on the same SM and can share that SM's fast on-chip shared memory and synchronise with one another. [1]

---

### Q2. Define a **warp** in the context of GPU execution.

**Model Answer (3 marks)**

- A warp is a group of **32 threads** that the GPU hardware schedules and executes together as a single unit. [1]
- All 32 threads in a warp execute the **same instruction simultaneously**, but each on a different data element — this is called SIMD (Single Instruction, Multiple Data) or SIMT (Single Instruction, Multiple Thread) execution. [1]
- Warps are the smallest unit of scheduling on an SM; a thread block is divided into multiple warps, all of which reside on the same SM. [1]

---

### Q3. What is a **thread block** and what is the maximum number of threads it may contain (for the NVIDIA Pascal architecture)?

**Model Answer (2 marks)**

- A thread block is a logical group of threads that is assigned to run on a single SM. Threads within the same block can access a shared on-chip memory space and synchronise with each other via barriers. [1]
- The maximum size of a thread block in Pascal is **1024 threads**. [1]

---

### Q4. What is GPU **occupancy**, and why does high occupancy generally improve performance?

**Model Answer (3 marks)**

- Occupancy is the ratio of **active warps on an SM** to the **maximum number of warps the SM can theoretically support**. [1]
  - `Occupancy = active warps / max warps per SM`
- High occupancy means many warps are resident on each SM simultaneously. [1]
- Because the GPU hides memory latency by switching to another warp whenever the current warp stalls waiting for a memory fetch, having more active warps increases the chance that at least one is always ready to execute — keeping the SM's compute units busy rather than idle. [1]

---

### Q5. What does the **Green500** list measure, and why do GPU-accelerated systems dominate it?

**Model Answer (3 marks)**

- The Green500 ranks supercomputers by **energy efficiency**, measured in **GFlops/Watt** (billions of floating-point operations per second per watt). [1]
- It is a companion list to the Top500 (which ranks by raw Linpack FLOPs); a machine can be #1 on the Top500 and much lower on the Green500 (e.g. El Capitan is #1 on Top500 but ranked 18 on Green500 in November 2024). [1]
- GPU-accelerated systems dominate the Green500 because GPUs deliver significantly more GFlops/Watt than CPUs — they are purpose-built for dense floating-point computation and are therefore more energy-efficient at that workload than a general-purpose CPU. [1]

---

### Q6. Name **three** programming models available for GPU computation, and classify each as either vendor-specific or portable.

**Model Answer (3 marks — 1 per correct pair)**

| Programming Model | Classification |
|---|---|
| CUDA | Vendor-specific (NVIDIA only) |
| HIP | Cross-vendor (AMD primary; NVIDIA back-end) |
| OpenCL | Portable / open standard |
| OpenACC | Portable / directive-based |
| OpenMP (4.0+) | Portable / directive-based |
| Data Parallel C++ (DPC++) / SYCL | Intel primary; multi-vendor |

*(Any three correct rows earn full marks.)*

---

### Q7. What is the role of the **GigaThread Engine** in an NVIDIA GPU?

**Model Answer (2 marks)**

- The GigaThread Engine is the hardware scheduler on the GPU. It assigns thread blocks to available SMs and performs context switches between warp groups on each SM. [1]
- Context switching on the GPU is **almost free** in time cost because the register file simultaneously holds the state (registers) of all resident warps — there is no need to save/restore to memory, unlike a CPU context switch. [1]

---

## Section B: GPU Architecture — Explain and Describe

### Q8. Explain the concept of **SIMD execution** on a GPU warp. What happens when threads in a warp take **different branches** (branch divergence)?

**Model Answer (5 marks)**

**SIMD execution (2 marks):**
- SIMD stands for Single Instruction, Multiple Data. In GPU hardware (NVIDIA terms this SIMT), all 32 threads in a warp execute the **exact same instruction** at every clock cycle, but each thread applies that instruction to its own data element. [1]
- This allows the GPU to apply one instruction decode/dispatch circuit to 32 simultaneous arithmetic operations, achieving high throughput at low hardware cost per operation. [1]

**Branch divergence (3 marks):**
- Branch divergence occurs when the threads within a single warp evaluate a conditional differently — some threads take the `if` path and others take the `else` path. [1]
- Because all threads must execute the same instruction, the hardware serialises the two paths: first it executes the `if` body with the relevant threads active and the remainder **masked off** (idle), then it executes the `else` body with the other threads active and the first group masked off. [1]
- The result is that the effective throughput is halved (or worse with more branches) — the warp uses fewer than 32 active threads during each serial pass. Additionally, GPUs lack the sophisticated **branch prediction** hardware found in CPUs that would otherwise mitigate this cost. [1]

---

### Q9. Describe how GPUs hide **memory latency**. How does this strategy differ from the approach taken by CPUs?

**Model Answer (4 marks)**

- **CPUs** hide memory latency using **large multi-level caches** (L1, L2, L3). When a data item is not in cache the CPU stalls or uses out-of-order execution to continue other work; the cache absorbs most accesses so stalls are infrequent. [1]
- **GPUs** hide memory latency through **massive thread oversubscription**. The GPU schedules many more warps onto each SM than there are physical execution slots. When the currently executing warp issues a memory load and stalls waiting for the data to arrive, the hardware performs an instantaneous context switch to another warp that is ready to run. [1]
- This works because GPU context switching is almost free — the register file retains the state of all resident warps simultaneously, so no save/restore operation is needed. [1]
- **Consequence:** a GPU needs a very large number of active threads (high parallelism / occupancy) to hide latency effectively. A GPU given too few threads will leave SMs idle waiting on memory, just as a CPU would stall without cache. Over-committing threads on a GPU is beneficial; on a CPU the same strategy would be harmful due to expensive context switches. [1]

---

### Q10. Explain what **memory coalescing** is and why it matters for GPU memory performance.

**Model Answer (3 marks)**

- Memory coalescing refers to the GPU hardware's ability to combine multiple memory requests from different threads in the same warp into a single, wider memory transaction when the addresses are **contiguous (adjacent)** in memory. [1]
- When threads in a warp access consecutive memory locations (e.g. thread 0 reads address 0, thread 1 reads address 1, …, thread 31 reads address 31), the memory controller issues one wide read. If accesses are **strided or scattered**, the controller must issue multiple separate transactions, consuming more bus bandwidth and increasing latency. [1]
- Because GPU memory bandwidth is a key bottleneck, algorithms should be designed so that threads in the same warp access adjacent memory locations, ensuring accesses coalesce and the high available bandwidth (e.g. 720 GB/s for Pascal) is exploited efficiently rather than wasted on redundant transactions. [1]

---

### Q11. List **four** characteristics of GPU architecture that make GPUs well-suited to HPC workloads, and for each characteristic explain the limitation or workload type where a GPU performs poorly.

**Model Answer (4 marks — 1 per characteristic + limitation pair)**

| GPU Strength | Limitation / Where GPU Loses |
|---|---|
| High density of floating-point units → excellent throughput for dense arithmetic | Poor single-thread performance — GPUs have low clock speeds per individual thread |
| Very high memory bandwidth (e.g. 720 GB/s vs ~68 GB/s for a CPU) | Small working sets may fit in CPU cache and be served faster from cache |
| Efficient for embarrassingly parallel, regular work | Highly branchy or irregular algorithms suffer from warp divergence |
| Excellent energy efficiency (GFlops/Watt) → Green500 leadership | The PCIe link is slow: small offloaded tasks may be slower overall due to data transfer overhead exceeding the compute saving |

---

## Section C: OpenMP Offloading

### Q12. What does the following OpenMP directive do? Identify and explain the role of each component.

```c
#pragma omp target teams distribute parallel for
for (int i = 0; i < N; i++) {
    c[i] = a[i] + b[i];
}
```

**Model Answer (5 marks)**

- `target` — offloads the following code block from the host CPU to the device (GPU). Execution moves to the GPU for the duration of the loop. [1]
- `teams` — spawns a **league of thread teams** on the device. Each team is analogous to a set of thread blocks that can each run independently on different SMs. [1]
- `distribute` — distributes the loop iterations across the league of teams, so each team handles a subset of the `i` values. [1]
- `parallel for` — within each team, this further distributes iterations across individual threads within that team using a parallel work-sharing loop, so the full GPU thread hierarchy is exploited. [1]
- Combined effect: the loop body `c[i] = a[i] + b[i]` is executed on the GPU, with iterations distributed first across teams (thread blocks / SMs) and then across threads within each team. This is the standard pattern for offloading a simple parallel loop to a GPU with OpenMP. [1]

---

### Q13. Explain the four `map` clause variants in OpenMP offloading. For each one, state the direction of data transfer and give a typical use case.

**Model Answer (4 marks)**

| Clause | Transfer Direction | Typical Use Case |
|---|---|---|
| `map(to: a[0:N])` | Host → device **before** the target region | Read-only input arrays: data needed by the GPU kernel but not written back |
| `map(from: c[0:N])` | Device → host **after** the target region | Write-only output arrays: results computed by the GPU that the host needs |
| `map(tofrom: x[0:N])` | Host → device before **and** device → host after (the implicit default) | Arrays that are both read and modified on the device and must reflect updates on the host |
| `map(alloc: tmp[0:N])` | Allocated on device only — **no transfer** in either direction | Scratch / temporary arrays used only internally by the GPU kernel |

*(1 mark per row — any four fully correct rows.)*

---

### Q14. The following code performs a vector addition on the GPU without explicit `map` clauses. Identify the problem, explain how many data transfers occur, and rewrite the code to fix it.

```c
double a[N], b[N], c[N];
// ... initialise a and b on host ...

#pragma omp target teams distribute
for (int i = 0; i < N; i++) {
    c[i] = a[i] + b[i];
}
// c is used on host afterwards
```

**Model Answer (5 marks)**

**Problem identified (2 marks):**
- Without explicit `map` clauses, OpenMP applies the default `tofrom` semantics to all arrays referenced inside the `target` region. [1]
- This causes **three host-to-device copies** (`a`, `b`, and `c` are all copied *in* before the kernel) plus **one device-to-host copy** (`c` is copied back after the kernel). The copy of `c` *to* the device is entirely wasteful — `c` is only ever written on the GPU, never read from its initial host values. [1]

**Transfer count without fix:** 3 copies in + 1 copy out = **4 transfers total**.

**Corrected code (2 marks):**

```c
double a[N], b[N], c[N];
// ... initialise a and b on host ...

#pragma omp target teams distribute \
    map(to: a[0:N], b[0:N]) map(from: c[0:N])
for (int i = 0; i < N; i++) {
    c[i] = a[i] + b[i];
}
// c is used on host afterwards
```

**Corrected transfer count (1 mark):** 2 copies in (`a`, `b`) + 1 copy out (`c`) = **3 transfers total**. The redundant copy of `c` to the device is eliminated, reducing unnecessary PCIe bus traffic.

---

### Q15. Write an OpenMP offloaded kernel that computes the dot product of two arrays `a[N]` and `b[N]`. Use appropriate `map` clauses. The result should be stored in a scalar `double result` on the host.

**Model Answer (5 marks)**

```c
double a[N], b[N];
double result = 0.0;
// ... initialise a and b on host ...

#pragma omp target teams distribute parallel for \
    map(to: a[0:N], b[0:N]) map(tofrom: result) \
    reduction(+: result)
for (int i = 0; i < N; i++) {
    result += a[i] * b[i];
}

// result is now available on host
```

**Key marking points:**
- `map(to: a[0:N], b[0:N])` — input arrays copied to device, not back. [1]
- `map(tofrom: result)` — the scalar accumulator must go both ways: its initial value (0.0) must be on the device before the kernel, and the final accumulated value must come back. [1]
- `reduction(+: result)` — required for a correct parallel reduction across all threads/teams; without it, the accumulation would involve a data race. [1]
- `target teams distribute parallel for` — full directive chain to distribute work across teams and then across threads within each team. [1]
- Array section notation `a[0:N]` — correct syntax (start index 0, length N). [1]

---

### Q16. A developer wants to run three successive GPU kernels on the same dataset. She currently writes the following structure:

```c
// Kernel 1
#pragma omp target teams distribute map(to: data[0:N]) map(from: data[0:N])
for (int i = 0; i < N; i++) { /* ... */ }

// Kernel 2
#pragma omp target teams distribute map(to: data[0:N]) map(from: data[0:N])
for (int i = 0; i < N; i++) { /* ... */ }

// Kernel 3
#pragma omp target teams distribute map(to: data[0:N]) map(from: data[0:N])
for (int i = 0; i < N; i++) { /* ... */ }
```

How many PCIe transfers does this generate? Describe a better approach and explain why it is more efficient.

**Model Answer (4 marks)**

**Transfer count as written:**
- Each kernel copies `data` to the device (1 transfer in) and back (1 transfer out) → **6 PCIe transfers total** (2 per kernel × 3 kernels). [1]

**Better approach — use `omp target data` to keep data on the device:**

```c
#pragma omp target data map(to: data[0:N]) map(from: data[0:N])
{
    // Kernel 1
    #pragma omp target teams distribute
    for (int i = 0; i < N; i++) { /* ... */ }

    // Kernel 2
    #pragma omp target teams distribute
    for (int i = 0; i < N; i++) { /* ... */ }

    // Kernel 3
    #pragma omp target teams distribute
    for (int i = 0; i < N; i++) { /* ... */ }
}
```

**Explanation (2 marks):**
- `omp target data` establishes a data environment that persists across multiple `target` regions inside the block. `data` is copied to the device once at the start and copied back once at the end. [1]
- This reduces transfers to **2 total** (1 in + 1 out), regardless of how many kernels are run in between. The fundamental principle is to keep data resident on the device for as long as possible and avoid round-tripping across the slow PCIe bus between kernels. [1]

---

## Section D: Calculations

### Q17. A thread block is configured with 256 threads. How many warps does this block contain? Show your working.

**Model Answer (2 marks)**

```
Warps per block = threads per block / warp size
               = 256 / 32
               = 8 warps
```

- Warp size on NVIDIA GPUs is **32 threads**. [1]
- A 256-thread block is divided into **8 warps**. [1]

---

### Q18. A kernel is launched with a grid of 4096 thread blocks, each containing 512 threads.

**(a)** How many warps does each block contain?
**(b)** What is the total number of threads in the entire grid?
**(c)** What is the total number of warps in the entire grid?

**Model Answer (4 marks)**

**(a) Warps per block:**
```
Warps per block = 512 / 32 = 16 warps
```
[1]

**(b) Total threads:**
```
Total threads = 4096 blocks × 512 threads/block = 2,097,152 threads (≈ 2 million)
```
[1]

**(c) Total warps:**
```
Total warps = 4096 blocks × 16 warps/block = 65,536 warps
```
*(Alternatively: 2,097,152 total threads / 32 = 65,536 warps)* [1]

**Bonus note (no mark, but exam-relevant):** Not all warps will be active at once — only as many as there are SMs × max warps per SM. The excess warps queue until SMs become free. [1]

---

### Q19. An SM on a Pascal GPU can support a maximum of 64 active warps simultaneously. A kernel launches thread blocks of 128 threads each. An SM currently has 4 thread blocks assigned to it.

**(a)** How many warps are active on this SM?
**(b)** What is the occupancy of this SM?
**(c)** If occupancy should be at least 50% for good latency hiding, is this configuration adequate?

**Model Answer (4 marks)**

**(a) Active warps:**
```
Warps per block = 128 / 32 = 4 warps
Active warps = 4 blocks × 4 warps/block = 16 active warps
```
[1]

**(b) Occupancy:**
```
Occupancy = active warps / max warps = 16 / 64 = 0.25 = 25%
```
[1]

**(c) Adequacy:**
- At 25% occupancy, the configuration **does not meet** the 50% threshold. [1]
- The SM will likely have periods of idleness: when the 16 resident warps stall on memory fetches, there are insufficient alternative warps to keep the execution units busy. Performance will be memory-latency-bound. To improve occupancy, the programmer should use larger thread blocks (e.g. 512 or 1024 threads) or launch more blocks per SM to increase the resident warp count. [1]

---

### Q20. A Pascal GPU has 60 SMs. Each SM can hold a maximum of 64 warps. A kernel is launched with thread blocks of 1024 threads each.

**(a)** How many warps are in each thread block?
**(b)** How many thread blocks can a single SM host simultaneously (limited by warp capacity)?
**(c)** What is the maximum total number of warps active across the entire GPU at once?

**Model Answer (4 marks)**

**(a) Warps per block:**
```
1024 / 32 = 32 warps per block
```
[1]

**(b) Blocks per SM (warp-limited):**
```
Max blocks per SM = floor(64 max warps / 32 warps per block) = floor(2.0) = 2 blocks per SM
```
[1]

**(c) Total active warps across GPU:**
```
Total active warps = 60 SMs × 64 warps per SM = 3,840 warps
```
*(Or equivalently: 60 SMs × 2 blocks × 32 warps = 3,840 warps.)* [1]

**Note:** In practice, resource limits other than warp count (register file size, shared memory per block) may further restrict the number of blocks per SM. [1]

---

### Q21. A GPU has a PCIe connection to the host with a bandwidth of 16 GB/s. A kernel operates on three arrays of doubles: `a[N]`, `b[N]`, and `c[N]`, where N = 100,000,000 (100 million elements). Each `double` is 8 bytes.

**(a)** What is the total size of one array in GB?
**(b)** Without `map` optimisation, how long does the data transfer phase take (ignoring kernel runtime)?
**(c)** With explicit `map(to: a, b) map(from: c)`, how does the transfer time change?

**Model Answer (4 marks)**

**(a) Size of one array:**
```
Size = 100,000,000 × 8 bytes = 800,000,000 bytes = 0.8 GB
```
[1]

**(b) Transfer time without optimisation (default tofrom — 3 arrays in, 1 array out):**
```
Data transferred = 3 × 0.8 GB (to device) + 1 × 0.8 GB (from device) = 3.2 GB
Transfer time = 3.2 GB / 16 GB/s = 0.2 seconds
```
[1]

**(c) Transfer time with explicit map:**
```
Data transferred = 2 × 0.8 GB (a, b to device) + 1 × 0.8 GB (c from device) = 2.4 GB
Transfer time = 2.4 GB / 16 GB/s = 0.15 seconds
```
Saving = 0.2 − 0.15 = **0.05 seconds** (25% reduction in transfer time). [1]

**Conclusion:** Explicit `map` clauses eliminate the redundant copy of the output array `c` to the device, reducing PCIe traffic by 0.8 GB and improving transfer time by 25%. This saving grows linearly with N and is significant at large problem sizes. [1]

---

## Section E: Compare and Contrast

### Q22. Compare CPU and GPU architectures across the following dimensions: number of cores, cache design, context-switching cost, branch handling, and memory bandwidth. Use a table in your answer.

**Model Answer (5 marks — 1 per dimension)**

| Dimension | CPU | GPU |
|---|---|---|
| Number of cores | Few powerful cores (e.g. 8–64), each with high clock speed and out-of-order execution | Many simpler cores (e.g. thousands of CUDA cores across 60 SMs), lower per-core clock speed |
| Cache design | Large multi-level cache (e.g. 25 MB L3) to reduce memory latency for any workload | Small cache (e.g. 4 MB L2 on Pascal), lower cache-to-bandwidth ratio; relies on bandwidth rather than hit rate |
| Context-switching cost | **Expensive** — must save/restore large register state to memory; few threads per core | **Near-zero** — register file retains all resident warps' state simultaneously; fast switching between warps |
| Branch handling | Sophisticated **branch prediction** hardware mitigates the cost of unpredictable branches | No branch prediction; branch divergence within a warp causes **serial execution** of each divergent path |
| Memory bandwidth | Relatively low (e.g. ~68 GB/s for a CPU) | Very high (e.g. 720 GB/s for Pascal) due to wide memory bus and HBM technology |

---

### Q23. A computational task is described as **memory-bound** on a GPU. Contrast this with a **compute-bound** task. What practical steps can a programmer take to improve performance in the memory-bound case?

**Model Answer (5 marks)**

**Definitions (2 marks):**
- A **compute-bound** task has enough arithmetic to keep the GPU's floating-point units fully occupied. The bottleneck is computation speed (FLOPs), not data supply. Adding more memory bandwidth would not help.
- A **memory-bound** task requires data faster than the memory system can supply it. The GPU's compute units are frequently idle waiting for memory fetches. The bottleneck is memory bandwidth (or latency), not FLOPs. [2 total]

**Practical improvements for memory-bound case (3 marks — any three):**
1. **Increase arithmetic intensity** — restructure the algorithm to perform more computation per byte fetched (e.g. cache blocking / tiling in shared memory so data is reused multiple times before being evicted). [1]
2. **Ensure memory coalescing** — redesign data access patterns so threads in the same warp access contiguous memory addresses, allowing the memory controller to issue fewer, wider transactions and exploit the full bandwidth. [1]
3. **Increase occupancy** — expose more warps to the SM so that when one warp stalls on a memory fetch, others are available to run, hiding the latency even if bandwidth is the bottleneck. [1]
4. **Use shared memory as a programmer-managed cache** — load a tile of data into fast on-chip shared memory once and reuse it multiple times within the block, reducing global memory accesses. [1]
5. **Reduce redundant data transfers** — keep data on the GPU for as long as possible; avoid unnecessary host-to-device round trips. [1]

---

## Section F: Multi-Part Exam Questions

### Q24. GPU Fundamentals (Multi-Part)

**(a)** The NVIDIA Pascal architecture is described as "accelerator-centric". Explain what is meant by the host/device split and why it is the most important design consideration when writing GPU code. **(3 marks)**

**(b)** A thread block of 384 threads is launched on a Pascal GPU. How many warps does it contain? What happens if a conditional branch is encountered where exactly half the threads in one warp take the `if` path and the other half take the `else` path? **(4 marks)**

**(c)** Explain why GPUs first appeared on the **Green500** list before they appeared as a dominant force on the **Top500**. **(3 marks)**

---

**Model Answer — Q24(a) (3 marks):**

- The host/device split means the CPU (host) and GPU (device) are **separate physical components** with **completely separate memory spaces**. [1]
- Any data needed by the GPU must be **explicitly copied from host memory to device memory** before computation, and results must be copied back afterwards. This transfer occurs over the PCIe bus, which has high latency and limited bandwidth compared to the GPU's internal memory bandwidth. [1]
- This is the most important consideration because the transfer cost can easily dominate runtime if not managed carefully. A kernel that would be faster on the GPU may still be *slower end-to-end* than a CPU-only version if the data transfer overhead exceeds the compute speedup. The programmer must structure code to minimise the frequency and volume of host↔device transfers. [1]

---

**Model Answer — Q24(b) (4 marks):**

- Warps = 384 / 32 = **12 warps**. [1]
- The specific warp experiences **branch divergence** — the 32 threads do not all take the same path. [1]
- The hardware executes both paths **serially**: first the 16 threads taking the `if` branch execute while the other 16 are masked off (idle); then the 16 threads taking the `else` branch execute while the first group is masked off. [1]
- In this case the warp achieves only 50% utilisation during each serial pass — the effective throughput of this warp is halved compared to a warp with no divergence. More complex multi-way divergence causes worse serialisation. [1]

---

**Model Answer — Q24(c) (3 marks):**

- The Top500 measures peak **Linpack FLOPs** — raw compute throughput. Early GPUs, even with high FLOPs, were limited by the immature GPU programming ecosystem and the overhead of host↔device data transfer, making them difficult to exploit for the Linpack benchmark at large scale. [1]
- The Green500 measures **GFlops/Watt**. GPUs deliver dramatically better energy efficiency for the floating-point work they are designed for, so even moderate GPU deployments showed clear Green500 improvements earlier than they could demonstrate Top500 dominance. [1]
- As GPU programming tooling matured (CUDA, OpenCL) and the host↔device bottleneck was better managed in large-scale deployments (NVLink, GPU-direct RDMA), GPU-accelerated machines also began dominating the Top500 — Frontier (AMD GPUs) became the first exascale system. [1]

---

### Q25. OpenMP Offloading in Depth (Multi-Part)

A researcher has the following CPU code she wants to port to a GPU using OpenMP:

```c
void compute(double *x, double *y, double *out, int N) {
    for (int i = 0; i < N; i++) {
        double t = x[i] * x[i] + y[i] * y[i];
        if (t > 1.0) {
            out[i] = t;
        } else {
            out[i] = 0.0;
        }
    }
}
```

**(a)** Rewrite this function with OpenMP offloading directives to run the loop on a GPU. Include appropriate `map` clauses and explain your choice for each one. **(5 marks)**

**(b)** Identify the potential GPU performance problem in the inner loop body and explain its cause. **(3 marks)**

**(c)** Suggest a refactoring of the loop body that avoids this problem while preserving correctness. **(2 marks)**

---

**Model Answer — Q25(a) (5 marks):**

```c
void compute(double *x, double *y, double *out, int N) {
    #pragma omp target teams distribute parallel for \
        map(to: x[0:N], y[0:N]) map(from: out[0:N])
    for (int i = 0; i < N; i++) {
        double t = x[i] * x[i] + y[i] * y[i];
        if (t > 1.0) {
            out[i] = t;
        } else {
            out[i] = 0.0;
        }
    }
}
```

**Explanation of `map` choices:**
- `map(to: x[0:N], y[0:N])` — `x` and `y` are **read-only** inputs; they need to be on the device before the kernel runs, but the results do not need to come back. [1]
- `map(from: out[0:N])` — `out` is a **write-only** output. There is no need to copy the (uninitialized or stale) host values of `out` to the device before the kernel; only the computed values need to return to the host afterwards. [1]
- `target teams distribute parallel for` — offloads to the device, spawns a league of teams, and distributes iterations across teams and then threads, exploiting the full GPU thread hierarchy for this simple loop. [1]
- Array section syntax `x[0:N]` — required because the compiler cannot infer the size of a pointer-based array. The `0` is the starting index and `N` is the length. [1]
- Scalar `t` is a private local variable (declared inside the loop); it does not need a `map` clause. [1]

---

**Model Answer — Q25(b) (3 marks):**

- The inner loop contains an `if/else` conditional. This creates **branch divergence** on the GPU. [1]
- Within a warp, some threads will have `t > 1.0` (taking the `if` path) and others will have `t <= 1.0` (taking the `else` path), depending on their input data. Because the warp executes in lock-step SIMD, it cannot simultaneously take both paths. [1]
- The hardware serialises the two paths — first executing the `if` branch for the relevant threads (masking the rest) then executing the `else` branch for the remainder — reducing effective throughput proportionally. Additionally, the GPU lacks the branch prediction hardware CPUs use to mitigate this penalty. [1]

---

**Model Answer — Q25(c) (2 marks):**

Replace the `if/else` with branchless arithmetic using a conditional expression or multiplication by a mask:

```c
// Option 1: ternary (may still generate divergence in some compilers)
out[i] = (t > 1.0) ? t : 0.0;

// Option 2: branchless arithmetic using a boolean mask cast to double
double mask = (double)(t > 1.0);   // 1.0 if condition true, 0.0 if false
out[i] = mask * t;
```

- Option 2 is fully branchless: all threads execute the same arithmetic operations regardless of the value of `t`, eliminating divergence. [1]
- The condition `(t > 1.0)` evaluates to an integer 0 or 1 in C, which is cast to a double and multiplied by `t`. When `t <= 1.0`, `mask = 0.0` and `out[i] = 0.0`. When `t > 1.0`, `mask = 1.0` and `out[i] = t`. The result is identical to the original. [1]

---

### Q26. GPU Occupancy and Latency Hiding (Multi-Part)

**(a)** Define GPU **occupancy** precisely and explain why it is related to the GPU's ability to hide memory latency. **(3 marks)**

**(b)** A Pascal SM has a maximum of 64 concurrent warps. A kernel uses thread blocks of 64 threads. How many blocks can the SM host simultaneously, and what is the occupancy? **(3 marks)**

**(c)** A programmer increases the block size to 512 threads. Recompute the warps per block, how many blocks fit on the SM (warp-limited), and the resulting occupancy. Does increasing block size always improve performance? **(4 marks)**

---

**Model Answer — Q26(a) (3 marks):**

- Occupancy = **active warps on an SM** / **maximum warps the SM supports**. For Pascal, the denominator is 64. [1]
- The GPU hides memory latency by switching to another warp whenever the current warp stalls waiting for a memory fetch from global memory. This warp switch is almost free because the register file holds all resident warps' state. [1]
- Higher occupancy means more warps are available to switch to. If occupancy is very low, there may be no ready warp to schedule when the active warp stalls, leaving the SM idle. High occupancy increases the probability that at least one warp is always ready, keeping execution units busy and effectively hiding latency behind computation. [1]

---

**Model Answer — Q26(b) (3 marks):**

- Warps per block = 64 threads / 32 = **2 warps per block**. [1]
- Maximum blocks on SM (warp-limited) = 64 max warps / 2 warps per block = **32 blocks**. [1]
- Active warps = 32 blocks × 2 warps = 64 warps. Occupancy = 64 / 64 = **100%**. [1]

---

**Model Answer — Q26(c) (4 marks):**

- Warps per block at 512 threads = 512 / 32 = **16 warps per block**. [1]
- Maximum blocks on SM (warp-limited) = floor(64 / 16) = **4 blocks**. [1]
- Active warps = 4 × 16 = 64. Occupancy = 64 / 64 = **100%**. Occupancy is unchanged; both configurations achieve 100% in this warp-limited model. [1]

- Increasing block size does **not** always improve performance:
  - Other resource limits may bind before warp count — e.g. register usage per thread (a block using many registers may reduce how many blocks can fit on an SM) or shared memory per block.
  - Very large blocks may also cause load imbalance if the total iteration count is not a multiple of the block size, leaving some threads idle.
  - On the other hand, larger blocks amortise per-block overhead and may improve cache/shared-memory reuse. The optimal block size must be tuned empirically. [1]

---

*End of Week 10 Practice Questions*

---

> **Quick Reference — Key Numbers (Pascal GPU)**
>
> | Quantity | Value |
> |---|---|
> | SMs per GPU (max) | 60 |
> | Threads per warp | 32 |
> | Max threads per block | 1024 |
> | DP FP cores per SM | 32 |
> | SP FP cores per SM | 64 |
> | Load/Store units per SM | 16 |
> | Special Function Units per SM | 16 |
> | GPU memory bandwidth | 720 GB/s |
> | GPU L2 cache | 4 MB |
> | Max warps per SM (occupancy denominator) | 64 |
