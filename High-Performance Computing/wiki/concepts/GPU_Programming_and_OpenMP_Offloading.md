---
title: "GPU Programming and OpenMP Offloading"
tags: [hpc, week-10, openmp, gpu, programming]
date: 2026-05-05
---

# GPU Programming and OpenMP Offloading

Programming a GPU (the "device") alongside a CPU (the "host") requires different paradigms compared to traditional CPU programming.

## Key Considerations

### 1. Data Movement
The CPU and GPU address completely separate memory spaces, connected typically by a slow PCIe bus. 
*   Data must be explicitly transferred between host and device.
*   Because transfers are slow, algorithms must be designed to **minimize data movement** and maximize data locality on the GPU. Offloading small tasks may actually be slower than running them on the CPU due to the data transfer overhead.

### 2. Hiding Memory Latency
*   **CPUs** hide memory latency by using large, fast [Caches](../concepts/Memory_Hierarchy_and_Cache.md).
*   **GPUs** hide memory latency by **over-committing cores**. Because context switching between threads on a GPU is practically instantaneous, the GPU simply switches to another warp of threads whenever the current warp stalls waiting for a memory fetch. This requires exposing a massive degree of parallelism to the GPU.

### 3. Avoiding Branching
Due to the [Warp architecture](../concepts/GPU_Architecture_and_Warps.md), branching causes thread divergence, forcing parallel threads to execute serially.

## Programming Models
Since standard C/C++ or Fortran cannot natively target GPUs, several programming models exist:
*   **Vendor-Specific:** CUDA (NVIDIA), HIP (AMD), Data Parallel C++ (Intel).
*   **Portable/Directive-Based:** OpenCL, OpenACC, and **OpenMP**.

## OpenMP Offloading
OpenMP (version 4.0+) allows multi-vendor GPU programming via compiler directives that "offload" work to the accelerator.

### The `target` Directive
The `#pragma omp target` construct offloads a block of code to the device.
It is often combined with other directives to distribute the work:
```c
#pragma omp target teams distribute
for(int i = 0; i < N; i++) {
    // Code executed on GPU
}
```

### The `map` Clause
By default, OpenMP will copy necessary data to the GPU and copy results back. However, implicit copying is often inefficient. 
The `map` clause explicitly controls data movement to reduce unnecessary transfers over the PCIe bus:
```c
#pragma omp target teams distribute map(to: a[0:N], b[0:N]) map(from: c[0:N])
for(int i = 0; i < N; i++) {
    c[i] = a[i] + b[i];
}
```
*   `map(to: ...)`: Copies data from host to device before execution.
*   `map(from: ...)`: Copies data from device to host after execution.
*   `map(tofrom: ...)`: Copies data both ways (default behavior for variables if not specified).