---
title: "Vertical vs Horizontal Scaling"
type: concept
sources: [data-intensive-applications, replication, review]
related: [scalability, replication, partitioning, shared-nothing-architecture]
updated: 2026-05-02
---

# Vertical vs Horizontal Scaling

*Two ways to make a system handle more load: make one machine bigger (vertical) or use more machines (horizontal). Big-data systems live almost entirely in horizontal-scaling territory.*

## Definition

- **Vertical scaling** (scale up, *shared-memory* architecture) — increase the resources of a single machine: more cores, more RAM, faster disks.
- **Horizontal scaling** (scale out, *shared-nothing* architecture) — add more machines that cooperate over the network.

## Why it matters

The whole module is, in essence, an exploration of horizontal scaling. The Big Data era happened because horizontal scaling on commodity hardware became cheaper and more capable than buying ever-larger machines.

## Mechanism — comparison

| Dimension | Vertical | Horizontal |
|---|---|---|
| Cost growth | **Super-linear** (premium hardware costs more per unit capability) | Roughly linear (commodity boxes) |
| Fault tolerance | Limited — one box, one fault domain | Strong — node failures absorbed by [[replication]] / [[partitioning]] |
| Programming model | Simple — single machine, shared memory | Hard — distributed concurrency, [[consistency]] |
| Ceiling | Hard physical limits (max RAM, max cores) | Effectively unbounded |
| Latency between "nodes" | Memory bus (ns) | Network (ms) |

## Mechanism — when to choose which

- **Vertical** for: small/medium workloads, low-latency single-machine algorithms (in-memory analytics), early-stage startups (pay the simplicity premium).
- **Horizontal** for: anything past a single-machine ceiling, anywhere that fault tolerance matters more than latency.

In practice modern systems combine both — large nodes (vertical) connected horizontally. The question is whether the *architecture* is shared-nothing.

## Trade-offs

- **Cost curve.** Up to ~16 cores, vertical wins on simplicity-per-pound. Beyond that, horizontal wins on cost-per-unit-throughput.
- **Operational complexity.** Horizontal scaling demands distributed-system competence: failure detection, [[consistency]], network partitions. Vertical scaling does not.
- **Ceiling.** Vertical has one. Horizontal does not (in theory).

## Examples in the syllabus

- **Replication and partitioning** ([[replication]], [[partitioning]]) — the two axes of horizontal scaling for data systems.
- **MapReduce / Hadoop** ([[batch-processing]]) — horizontal scaling of compute.
- **Netflix CDN** — horizontal at the extreme: 8,492 servers across 578 locations (2018).

## Common exam framing

- "Compare vertical and horizontal scaling on cost, fault tolerance, and complexity."
- "Why are most large-scale data systems built as shared-nothing architectures?"
- "Give one scenario where vertical scaling is the correct choice."

## See also

- [[scalability]]
- [[replication]]
- [[partitioning]]
- [[shared-nothing-architecture]]
