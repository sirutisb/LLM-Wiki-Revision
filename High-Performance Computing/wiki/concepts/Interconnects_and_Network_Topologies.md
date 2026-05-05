---
title: "Interconnects and Network Topologies"
tags: [hpc, week-7, network, hardware, mpi]
date: 2026-05-05
---

# Interconnects and Network Topologies

Compute nodes in an HPC cluster communicate via an interconnect network (e.g., Gigabit Ethernet or Infiniband).

## Communication Time Model
The transmission time $t$ for a message can be modeled as:
$$ t = L + \frac{M}{B} $$
*   **$L$ (Latency):** The fixed setup time to initiate a message transfer (often in the $\mu s$ range).
*   **$B$ (Bandwidth):** The data transfer rate (e.g., GB/s).
*   **$M$ (Message Size):** The size of the message in bytes.

**Implications:**
*   For **small messages**, latency $L$ dominates the transmission time.
*   For **large messages**, bandwidth $B$ dominates.

## Network Topologies
Networks must balance cost and connectivity. Connecting every node directly is impossible at scale.
*   **Fat Tree:** A common topology where the network looks like a tree with compute nodes at the leaves. The bandwidth (thickness) of the links increases towards the top (root) of the tree to prevent bottlenecks.
*   **Blocking Factor:** Often networks are designed with a blocking factor (e.g., 2:1), meaning there is less bandwidth leaving a local switch than there is internal to the switch. This makes communication between distant racks slower than communication within the same rack.