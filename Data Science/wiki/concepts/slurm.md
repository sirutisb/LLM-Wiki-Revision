---
title: "SLURM"
type: concept
sources: [high-performance-computing]
related: [high-performance-computing, flops, amdahls-law]
updated: 2026-05-02
---

# SLURM

*The dominant open-source workload manager for HPC clusters — organises computing resources into nodes, partitions, jobs, and job steps, then schedules queued jobs to available nodes.*

## Definition

**SLURM** (Slurm Workload Manager, formerly Simple Linux Utility for Resource Management) is an open-source, extensible, scalable resource manager and job scheduler for clusters and supercomputers. It performs three core functions: resource allocation, workload scheduling, and distributed workload monitoring.

## Entities hierarchy

```
Cluster
└── Nodes          (individual computers)
    └── Partitions (job queues, each with constraints)
        └── Jobs   (resource allocations to users)
            └── Job Steps (individual parallel tasks within a job)
```

- **Node** — a single computer in the cluster. Has configuration: processor count, memory, disk, features, scheduling weight.
- **Partition** — a logical group of nodes forming a job queue. Imposes constraints (max walltime, max cores, allowed users).
- **Job** — a resource allocation. Can be interactive (real-time) or batch (scripted). Identified by an integer ID.
- **Job Step** — a set of (typically parallel) tasks within a job. Can use all or a fraction of the job's nodes.

## Node states

| State | Meaning |
|---|---|
| Unknown | Initial / unrecognised state |
| Idle | Available for new jobs |
| Allocated | Currently running a job |
| Completing | Job finishing, resources not yet released |
| Down | Unavailable (hardware/network failure) |
| Draining | Allocated or Completing with Drain flag — won't accept new jobs |
| Drained | Idle or Down with Drain flag — administratively taken offline |

## Job states

Pending → Running → (Suspended) → Completing → Completed  
Other terminal states: TimeOut, NodeFail, Cancelled, Failed.

## Scheduling

- The scheduler assigns available nodes to the highest-priority jobs until the node pool is exhausted.
- Priority can be based on queue time, fairshare, QOS, etc.
- Jobs wait in partition queues until enough resources are free.

## Examples in the syllabus

- HPC s. 20–26: full SLURM entity definitions, node states, job states.

## Common exam framing

- "What are the four SLURM entities? Briefly describe each."
- "Distinguish Draining and Drained node states in SLURM."
- "What is the role of a partition in SLURM?"

## See also

- [[high-performance-computing]]
- [[amdahls-law]]
