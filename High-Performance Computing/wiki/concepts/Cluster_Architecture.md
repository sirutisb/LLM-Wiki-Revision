---
title: "Cluster Architecture"
tags: [hpc, week-1, architecture, cluster]
date: 2026-05-05
---

# Cluster Architecture

Historically, there have been various supercomputing architectures. Today, current systems integrate many multi-core processors.

## Commodity Clusters
The dominant architecture is the **commodity cluster**.
*   **Definition:** A cluster where both the network and compute nodes are commercial off-the-shelf (OTS) products available for independent procurement. 
*   **Advantage:** Cost-effective balance of performance.

### Main Components
1.  **Compute Nodes:** Provide processor cores and memory required to run workloads. Examples include dual-socket Intel x86 nodes (e.g., 2 processors each with multiple cores sharing memory).
2.  **Interconnect:** The cluster internal network enabling nodes to communicate and access storage. Often uses scalable architectures (e.g., fat tree, hyper-cube) and high-performance hardware (e.g., Infiniband).
3.  **Mass Storage:** Disk arrays (RAID) and storage nodes providing parallel user filesystems (e.g., GPFS).
4.  **Login Nodes:** Provide external access (via SSH) for users and orchestrate queue access to compute nodes.

## Massively Parallel Processing Systems (MPPs)
*   Like clusters, they combine many multi-core processors.
*   Unlike clusters, they use more specialist hardware and fewer off-the-shelf components.
*   Can achieve higher performance but are less cost-effective than commodity clusters. (e.g., Fugaku, IBM BlueGene).