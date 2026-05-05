---
title: "Graphics Processing Units (GPUs)"
tags: [hpc, week-10, hardware, accelerators]
date: 2026-05-05
---

# Graphics Processing Units (GPUs)

## History of Accelerators
Using an accelerator to supplement the CPU is not new. Early x86 CPUs relied on floating-point coprocessors (like the x87) before floating-point units were integrated into the main processor. 

As 3D graphics rendering evolved, specialized hardware (GPUs) was developed to handle the massive number of matrix-vector operations required. Modern GPUs have moved away from fixed-function rendering pipelines to unified shaders that support general-purpose computation and double-precision arithmetic.

## GPUs in HPC
GPUs are highly parallel devices containing a large number of floating-point units and high memory bandwidth. These characteristics are extremely desirable for HPC workloads.
*   **The Exascale Era:** Most modern supercomputers (like Frontier, El Capitan, and Aurora) use an accelerator-centric architecture, relying heavily on GPUs from vendors like NVIDIA, AMD, and Intel.
*   **Connectivity:** The CPU (host) and GPU (device) are physically separate and have distinct memory spaces. They typically connect via the **PCI Express (PCIe)** interface. Because PCIe has high latency, a fundamental principle of GPU programming is to minimize data transfer between the host and the device. Some systems use proprietary interconnects like NVIDIA's NVLink for improved connectivity.

## Energy Efficiency and the Green500
Energy efficiency is a critical factor in HPC system design due to power consumption limits and cooling requirements. GPUs offer much better energy efficiency (measured in GFlops/Watt) than traditional CPUs.
*   **Green500:** A companion to the [Top500 List](../concepts/Performance_Metrics_and_Top500.md) that ranks supercomputers by their energy efficiency. GPU-accelerated systems dominate the top of the Green500 list.