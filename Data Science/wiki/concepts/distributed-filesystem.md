---
title: "Distributed filesystem"
type: concept
sources: [batch-processing]
related: [batch-processing, mapreduce, replication, partitioning]
updated: 2026-05-02
---

# Distributed filesystem

*A filesystem-shaped abstraction over a cluster of commodity storage nodes. Provides the input/output substrate that batch processing systems sit on top of.*

## Definition

A **distributed filesystem** stores files across many machines while presenting a single filesystem-like API (paths, blocks, read/write). It typically:

- **Splits files into blocks** (e.g. 128 MB) and distributes them across nodes.
- **Replicates** each block (typically 3×) for fault tolerance.
- **Exposes data locality** — clients can ask which node holds a given block, so [[mapreduce|MapReduce]] can place computation near data.

## Examples cited in the slides

- **Colossus** — Google's successor to GFS (Google File System). The current internal storage layer.
- **HDFS** — Hadoop Distributed File System; the open-source canonical example.
- **GlusterFS** — open-source, POSIX-compatible.
- **QFS** — Quantcast File System; HDFS-compatible alternative emphasising erasure coding.

## Why it matters

Without a distributed filesystem, MapReduce-style frameworks would have no input/output substrate. The split-and-replicate behaviour is what enables data locality (mappers run where data lives) and fault tolerance (block replicas survive node failures).

## Mechanism — HDFS as the canonical example

- A single **NameNode** holds metadata (file → blocks → DataNodes).
- Many **DataNodes** hold actual block data, replicated 3× by default.
- Clients ask the NameNode "where are the blocks of /input/data.csv?" and stream from the closest DataNode.
- Block size (128 MB) is large to amortise seek cost — HDFS is built for sequential reads of huge files, not small-file workloads.

## Trade-offs

- **+** Massive horizontal scale — petabytes of capacity, thousands of nodes.
- **+** Built-in fault tolerance via replication.
- **+** Data locality enables efficient batch processing.
- **−** Bad at small files (NameNode metadata blows up).
- **−** No POSIX compliance for HDFS — append-only, no random writes mid-file.
- **−** Single-NameNode bottleneck (HDFS HA mitigates with multiple NameNodes).

## Examples in the syllabus

- s. 6 of the Batch Processing lecture lists the four canonical implementations.

## Common exam framing

- "Why does MapReduce require a distributed filesystem?"
- "What is data locality and why is it important for batch performance?"
- "Briefly contrast a distributed filesystem with a distributed database."

## See also

- [[batch-processing]]
- [[mapreduce]]
- [[replication]]
- [[partitioning]]
