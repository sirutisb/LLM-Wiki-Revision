---
title: "Accelerators and GPUs — Complete Exam Reference (Week 10)"
tags: [hpc, week-10, gpu, accelerator, pascal, openmp, offloading, architecture, final-prep]
date: 2026-05-13
---

# Accelerators and GPUs — Complete Exam Reference (Week 10)

One-stop reference for Week 10: **why accelerators exist**, the **NVIDIA Pascal** architecture as a representative HPC GPU, the **threads / blocks / warps** hierarchy, the four programming considerations specific to GPUs (data movement, latency hiding, branching, programming models), and **OpenMP offloading** with the `target teams distribute` + `map` pattern.

The four units in Week 10:
- **10.1** Background and history of accelerators
- **10.2** GPUs in HPC (connectivity, energy efficiency, exascale)
- **10.3** NVIDIA Pascal architecture
- **10.4** GPU programming for HPC

---

## 1. Why Accelerators Exist (Unit 10.1)

### 1.1 The CPU trade-off

CPUs must deliver "acceptable" performance across an enormous range of workloads — OS scheduling, branchy logic, single-threaded code, I/O, server workloads. CPU design is a four-way compromise:

- Functionality
- Performance
- Energy efficiency
- Cost

For specific workloads (graphics, dense floating-point, ML) you can do far better by building hardware with a different trade-off curve.

### 1.2 What an accelerator is

An **accelerator** (or **co-processor**) is a chip that works **alongside a host CPU** to speed up a narrow class of workloads. The CPU still runs the OS, handles I/O, and orchestrates everything; computationally expensive kernels are **offloaded** to the accelerator.

Not a new idea — the **x87 floating-point co-processor** sat next to early x86 CPUs before FP hardware was integrated into the main processor. The historical pattern is: useful co-processor capabilities eventually migrate onto the CPU die, but in the meantime a co-processor wins on specialised work.

### 1.3 Historical Top500 accelerators

| Year | Accelerator | Notes |
|---|---|---|
| June 2006 | **ClearSpeed** | First accelerator on the Top500; FP accelerator card |
| June 2008 | **IBM Cell** | As used in the PlayStation 3 |
| June 2010 | **NVIDIA GPUs** | First appeared; now the dominant accelerator family |

### 1.4 Why GPUs took over

GPUs (Graphics Processing Units) were built for 3D rendering — projecting 3D objects to a 2D image is overwhelmingly **matrix–vector arithmetic** that is **embarrassingly parallel**:

- Large number of floating-point units
- Support for a very large number of threads
- Memory bandwidth far higher than a CPU (different memory technology, e.g. HBM)

Early GPUs had a **fixed-function rendering pipeline** — silicon hard-wired to do one set of graphics operations. Hardware evolution introduced:

- **Unified (programmable) shaders** — same execution units for all shader stages, programmable.
- **Double-precision floating point** (e.g. AMD RV670 in 2007, NVIDIA GT200 in 2008) — making GPUs usable for scientific HPC, not just graphics.

Result: GPUs evolved from graphics-only hardware to **general-purpose GPU (GPGPU)** compute devices.

---

## 2. GPUs in HPC (Unit 10.2)

### 2.1 Host / device split

The GPU is **not** part of the CPU. They are separate components with **separate physical memory**:

```
       Host (CPU)                    Device (GPU)
   ┌────────────────┐            ┌────────────────┐
   │  CPU cores     │            │  SMs (compute) │
   │  Host RAM      │  ◄──PCIe──►│  GPU memory    │
   └────────────────┘            └────────────────┘
            slow / high-latency link
```

This split is the **single most important fact** in GPU programming. It drives every design decision in Unit 10.4.

### 2.2 PCIe and NVLink

- **PCI Express (PCIe)** is the industry-standard connector. Any motherboard with a free slot and enough power/cooling can host a GPU. Relatively **high latency** → host↔device transfers are expensive.
- **NVLink** is NVIDIA's proprietary higher-bandwidth, lower-latency link used in dense GPU systems and HPC nodes. Only available between NVIDIA components.

**Implication:** *Minimise data transfer between host and device.* This is the central GPU performance rule.

### 2.3 Energy efficiency and the Green500

Energy is a first-class constraint in HPC system design — exascale is as much a power-budget problem as a FLOPs problem. GPUs deliver more **GFlops/Watt** than CPUs.

- **Top500** ranks machines by raw Linpack performance (FLOPs).
- **Green500** ranks the same systems by **GFlops/Watt** — energy efficiency.
- GPU-accelerated systems dominate the top of the Green500. (Note: El Capitan, while #1 on Top500, was ranked 18 on the November 2024 Green500 — being fastest is not the same as being most efficient.)

### 2.4 The exascale era

Most current and planned exascale systems are **GPU-accelerated**, but the vendor mix is broadening:

| System | CPU | Accelerator |
|---|---|---|
| **Frontier** (first exascale) | AMD EPYC | AMD Radeon GPUs |
| **El Capitan** | AMD EPYC | AMD Radeon GPUs |
| **Aurora** | Intel Xeon | Intel Xe GPUs |
| **Perlmutter** | AMD EPYC | NVIDIA GPUs |
| **JUPITER** (Europe's first exascale) | — | NVIDIA GPUs |
| **Fugaku** | A64fx ARM (no separate GPU) | — |

CPU vendors now include AMD, ARM, and Intel; GPU vendors include AMD, Intel, and NVIDIA. **Portability across hardware** is therefore a major concern — favouring open / multi-vendor programming models (OpenMP, OpenACC, OpenCL) over CUDA-only code where possible.

### 2.5 Accelerator-centric architecture

Modern exascale nodes are **accelerator-centric** — most of the compute capability lives in the GPUs, with the CPU acting primarily as an orchestrator. On Frontier, for example, the GPUs supply the bulk of the FLOPs and the CPU is essentially there to feed them.

---

## 3. NVIDIA Pascal Architecture (Unit 10.3)

Used in the syllabus as a representative example of an HPC GPU. Subsequent NVIDIA generations (Volta, Ampere, Hopper) keep the same overall hierarchy.

### 3.1 Top-level layout

A Pascal GPU contains:

- Up to **60 Streaming Multiprocessors (SMs)** per GPU (up to 4 may be disabled due to manufacturing defects — yield management).
- SMs are organised in **blocks of 10** called a **Graphics Processing Cluster (GPC)**. Each GPC contains all elements of the rendering pipeline — effectively an independent mini-GPU.
- **High-bandwidth memory:** 16 GB capacity at **720 GB/s** bandwidth (compare ~68.3 GB/s for an Intel Xeon E5-2640v4 — roughly **10× more bandwidth** than the host CPU).
- **L2 cache:** 4 MB (last-level cache on the GPU). Compare 25 MB L3 on the same Xeon — the GPU has *less* cache but *more* memory bandwidth; that's the trade-off.
- **GigaThread Engine:** the hardware scheduler. Assigns thread blocks to SMs and handles context switches between thread groups *almost for free* compared to a CPU.

### 3.2 The thread hierarchy

This is the single most important diagram for the exam:

```
   Grid (the whole kernel launch)
     │
     ├── Thread Block  ── runs on one SM, up to 1024 threads
     │     │              shared memory + barriers within block
     │     │
     │     ├── Warp ── 32 threads, lock-step SIMD execution
     │     ├── Warp ── 32 threads
     │     └── ... (block subdivided into multiple warps)
     │
     ├── Thread Block ── runs on another SM
     └── ...
```

**Thread block** (coarsest division of workload):
- Up to **1024 threads** per block.
- Scheduled by the GigaThread Engine onto a single SM.
- Threads in the same block can:
  - **Access shared memory** (fast on-chip memory)
  - **Use the SM's cache**
  - **Synchronise** with each other (block-level barriers)

**Warp** (the execution unit):
- A block is subdivided into **warps of 32 threads**.
- All threads in a warp execute the **same instruction at the same time**, just on different data → **SIMD (Single Instruction, Multiple Data)** execution. (NVIDIA's term is SIMT — same idea.)
- All warp scheduling and divergence behaviour follows from this lock-step property.

### 3.3 Inside one SM (Pascal numbers)

Each Streaming Multiprocessor contains:

- **32 double-precision (DP) FP cores** — for FP64 arithmetic.
- **64 single-precision (SP) cores** — for FP32 arithmetic (twice the SP throughput of DP).
- **16 load/store units** — for memory access.
- **16 Special Function Units (SFUs)** — for transcendentals (sin, cos, exp, etc.).
- Register file, shared memory, L1 cache.

The mix of cores per SM is itself a design statement: SP throughput is prioritised over DP because most real workloads (especially ML) use SP or lower.

### 3.4 Context switching: GPU vs CPU

| | CPU | GPU |
|---|---|---|
| Context switch cost | Expensive (save/restore large state to memory) | Near-zero (register file holds many threads' state simultaneously) |
| Threads per core | Few (1–2 with SMT/Hyperthreading) | Many (warps over-committed to each SM) |
| Latency hiding | Large caches | Massive thread parallelism + cheap context switch |

This difference is *the* architectural reason GPU code looks different from CPU code (see §4.2).

---

## 4. GPU Programming for HPC (Unit 10.4)

Four considerations that distinguish GPU programming from CPU programming.

### 4.1 Data movement — minimise PCIe traffic

The CPU and GPU address **separate memory**, connected by a slow bus:

- GPU memory is **smaller** than host memory (e.g. 16 GB vs hundreds of GB).
- Every input array must be **copied to the device** before the kernel runs.
- Every output array must be **copied back to the host** after the kernel runs.
- The bus is slow → there is a **minimum problem size** for offloading to be a win. Tiny work units may be faster on the CPU because the transfer cost dwarfs the compute saved.

**Rule:** keep data on the device for as long as possible. If you have a sequence of GPU kernels, do not copy back between them — let the data live on the GPU until the final result.

### 4.2 Hiding memory latency — by parallelism, not cache

| Strategy | CPU | GPU |
|---|---|---|
| How latency is hidden | Large multi-level **cache** | **Over-commit cores** — switch to another warp when current warp stalls on memory |
| Why it works | Most accesses hit cache | Context switch is almost free; if one warp is waiting on memory, schedule another |

**Consequence:** GPUs *require* a high degree of parallelism to perform well. You need enough warps in flight that whenever any warp stalls on memory there is another one ready to run. A problem with too few threads will leave the GPU idle waiting for memory — no warps to switch to.

On a CPU, **over-committing cores hurts performance** because context switching is expensive. The two architectures want opposite levels of thread oversubscription.

### 4.3 Avoiding branching — branch divergence

GPUs are SIMD/SIMT machines: all 32 threads in a warp execute the same instruction. So what happens at a conditional?

```c
if (threadIdx % 2 == 0) {
    // path A — even threads
} else {
    // path B — odd threads
}
```

**Branch divergence** occurs: the warp executes **both paths serially**, masking out the inactive threads in each pass:

```
Cycle 1: threads 0,2,4,... run path A   (threads 1,3,5,... idle, masked off)
Cycle 2: threads 1,3,5,... run path B   (threads 0,2,4,... idle, masked off)
```

Effective parallel width is halved. With more complex branching, the cost can multiply. Also, GPUs lack the **branch prediction** hardware that CPUs use to mitigate the cost of branches.

**Two implications:**
- Algorithms should be redesigned to **avoid divergent control flow within a warp** — branchless arithmetic, sorted data, or grouping similar work into the same warp.
- Branches that go the **same way for all threads in a warp** are fine — only **divergence** is the problem.

### 4.4 Programming models — pick portability vs control

Standard C/C++/Fortran cannot directly target a GPU. Several models exist:

| Model | Style | Vendor | Portable? |
|---|---|---|---|
| **CUDA** | C/C++/Fortran extensions | NVIDIA only | No (NVIDIA-only) |
| **HIP** | C++ (CUDA-like syntax) | AMD (with NVIDIA back end) | Cross-vendor (AMD ↔ NVIDIA) |
| **Data Parallel C++ (DPC++)** | C++ / SYCL | Intel | Multi-vendor |
| **OpenCL** | C-based, low level | Open standard | Yes, but verbose |
| **OpenACC** | Compiler directives | Open standard | Yes |
| **OpenMP** (4.0+) | Compiler directives | Open standard | Yes |

Trade-off: **vendor-specific** models (CUDA) give the most performance and tooling but lock you in; **directive-based** open models (OpenMP, OpenACC) give portability across NVIDIA/AMD/Intel GPUs but historically less control and slightly lower peak performance. Given the **hardware diversity** of the exascale era (§2.4), portability matters more than it used to.

---

## 5. OpenMP Offloading — the Examinable Pattern

OpenMP 4.0 added GPU offloading through the `target` family of directives. This is the worked example used in the unit (vector addition).

### 5.1 The directives

| Directive                             | What it does                                               |
| ------------------------------------- | ---------------------------------------------------------- |
| `#pragma omp target`                  | Move execution to the device (GPU) for the following block |
| `#pragma omp teams`                   | Spawn a league of thread teams on the device               |
| `#pragma omp distribute`              | Distribute loop iterations across the teams                |
| `#pragma omp target teams distribute` | Combined: offload + spawn teams + distribute loop          |

For a parallel loop on the GPU, the combined form is the standard pattern:

```c
#pragma omp target teams distribute
for (int i = 0; i < N; i++) {
    c[i] = a[i] + b[i];
}
```

This produces device code (e.g. CUDA for an NVIDIA target) that the compiler ships to the GPU. The compiler handles the kernel launch.

### 5.2 The `map` clause — controlling data movement

Without explicit data-mapping instructions, the OpenMP runtime conservatively assumes everything used inside `target` must be copied **both ways** (`tofrom`). This is correct but wasteful.

| Clause | Direction | Use for |
|---|---|---|
| `map(to: a[0:N])` | Host → device, **before** the region | Input arrays (read-only on GPU) |
| `map(from: c[0:N])` | Device → host, **after** the region | Output arrays (written on GPU, not yet on host) |
| `map(tofrom: x[0:N])` | Both directions (the implicit default) | Arrays that are both read and written and must be visible to host afterwards |
| `map(alloc: tmp[0:N])` | Allocated on device only | Scratch arrays — no transfer either way |

Syntax `a[0:N]` is **array section** notation: starting index 0, length N (not "0 to N" inclusive). Required because the compiler can't know how much of a heap-allocated array to copy.

### 5.3 The vector-addition example — why `map` matters

Naïve version, no `map`:

```c
#pragma omp target teams distribute
for (int i = 0; i < N; i++) {
    c[i] = a[i] + b[i];
}
```

Under `nvprof` this generates:

- **3× host-to-device copies** (a, b, *and* c are all implicitly `tofrom` so c is uselessly copied to the GPU before the kernel even starts).
- **1× device-to-host copy** (c after the kernel).

With explicit `map`:

```c
#pragma omp target teams distribute \
    map(to: a[0:N], b[0:N]) map(from: c[0:N])
for (int i = 0; i < N; i++) {
    c[i] = a[i] + b[i];
}
```

- **2× host-to-device copies** (a, b only — c is `from`, so it is *not* copied in).
- **1× device-to-host copy** (c).

The wasted copy of `c` to the device is eliminated. Same compute, less PCIe traffic.

> **Exam line:** the `map` clause exists so the programmer can avoid the default `tofrom` semantics and remove redundant transfers across the slow PCIe bus.

### 5.4 What the compiler generates

For an NVIDIA target, an OpenMP-offloaded loop is compiled into **CUDA** kernels under the hood. The high-level OpenMP source is portable; the generated device code is vendor-specific. This is what makes OpenMP attractive for portability — the same `#pragma` recompiles to AMD HIP, Intel SYCL, or NVIDIA CUDA depending on the target.

---

## 6. Summary — One-Page Cheat Sheet

### Architecture
- GPU = accelerator alongside a host CPU; separate memory; connected by PCIe (high-latency) or NVLink (NVIDIA, faster).
- Pascal: up to 60 SMs; 16 GB high-bandwidth memory @ 720 GB/s; 4 MB L2.
- Each SM (Pascal): 32 DP cores, 64 SP cores, 16 LD/ST, 16 SFU.
- Thread hierarchy: **grid → block (≤1024 threads, runs on one SM, shared memory + sync) → warp (32 threads, lock-step SIMD)**.

### Performance characteristics
- GPUs win on: dense FP, high memory bandwidth, embarrassingly parallel work, energy efficiency (Green500).
- GPUs lose on: small problems (PCIe transfer dominates), branchy code (divergence), tasks needing high single-thread performance.

### Programming rules
1. **Minimise host↔device data movement.** Keep data on the GPU; use `map(to:)` / `map(from:)` explicitly.
2. **Expose massive parallelism.** GPUs hide latency by oversubscription, not cache. Few threads = idle GPU.
3. **Avoid branch divergence within a warp.** If threads in the same warp take different paths, the warp serialises.
4. **Beware minimum granularity.** Small offloaded tasks may be slower than CPU because of transfer overhead.

### OpenMP offloading pattern

```c
#pragma omp target teams distribute \
    map(to: a[0:N], b[0:N]) map(from: c[0:N])
for (int i = 0; i < N; i++) {
    c[i] = a[i] + b[i];
}
```

- `target`         → run on device
- `teams`          → spawn league of teams
- `distribute`     → split loop across teams
- `map(to:)`       → copy in only (input)
- `map(from:)`     → copy out only (output)

### Programming model landscape
- **CUDA** (NVIDIA only), **HIP** (AMD, NVIDIA-back-end), **DPC++** (Intel) — vendor.
- **OpenCL**, **OpenACC**, **OpenMP** — portable / multi-vendor.

### Exascale context
- Frontier, El Capitan, Aurora, JUPITER → all GPU-accelerated, mixed vendors (AMD / Intel / NVIDIA).
- Portability across GPU vendors is now a first-class design concern → favours OpenMP-style directives.

---

## 7. Likely Exam Question Patterns

Based on past papers and the unit summaries, expect:

- **Compare CPU and GPU** along axes of: latency hiding (cache vs oversubscription), context switching cost, branch handling (prediction vs divergence), memory bandwidth, energy efficiency.
- **Explain why minimising host↔device transfer matters**, and how the `map` clause is used to control it. Worked example: vector addition with and without `map`, count the copies.
- **Describe the GPU thread hierarchy:** grid → block → warp, what each means, sizes for Pascal (up to 1024 threads/block, 32 threads/warp), what threads in a block share (memory, barriers).
- **Branch divergence**: define it; explain why it halves (or worse) effective throughput; contrast with CPU branch prediction.
- **Programming-model trade-off**: name CUDA vs OpenMP, give one advantage of each. Justify why portability is important in the exascale era given AMD/Intel/NVIDIA hardware diversity.
- **Top500 / Green500**: explain the difference between the two; explain why GPU-accelerated systems dominate Green500.

---

## See Also

- [Graphics Processing Units (GPUs)](../concepts/Graphics_Processing_Units_GPUs.md) — concept page
- [GPU Architecture and Warps](../concepts/GPU_Architecture_and_Warps.md) — concept page
- [GPU Programming and OpenMP Offloading](../concepts/GPU_Programming_and_OpenMP_Offloading.md) — concept page
- [OpenMP — Complete Exam Reference](OpenMP_Complete_Reference.md) — including `target` / `map` clauses
- [Performance Metrics and Top500](../concepts/Performance_Metrics_and_Top500.md) — Top500 / Green500
- [Compute Node Architecture](Compute_Node_Architecture.md) — how the GPU sits next to the CPU
- [Week 10 Summary](../summaries/Week_10_Summary.md)
