---
title: "Partitioning (sharding)"
type: concept
sources: [distributed-architectures-partitioning, distributed-architectures-part-2, review]
related: [replication, key-range-partitioning, hash-partitioning, secondary-indexes-partitioning, rebalancing-partitions, vertical-vs-horizontal-scaling]
updated: 2026-05-02
---

# Partitioning (sharding)

*Splitting a large dataset across nodes so each holds only a subset. The complement to [[replication]] — together they enable horizontal scaling beyond the size of a single machine.*

## Definition

**Partitioning** (a.k.a. **sharding**) is the practice of dividing a dataset into subsets and assigning each subset to a different node. Every record belongs to exactly one partition; a node can hold many partitions.

Different DBMSs call partitions different things:

- **Shard** — MongoDB, Elasticsearch, Firestore.
- **Region** — HBase.
- **Vnode** — Cassandra.
- **Tablet** — Bigtable.

## Why it matters

- **Scaling beyond a single machine.** [[replication]] lets you serve more reads, but every replica still stores everything. Once your dataset exceeds a single machine, you need to partition.
- **Write scaling.** Writes can go to different partitions in parallel.

## Mechanism — combining with replication

The two orthogonal axes (replicate × partition) are typically combined: each partition is replicated across multiple nodes for availability.

In a leader-follower setup, **each partition has its own leader**. A node can be the leader for some partitions and a follower for others — distributing leader load.

## Mechanism — partitioning strategies

| Strategy | How partitions are assigned | Strengths | Weaknesses |
|---|---|---|---|
| Random | Scatter randomly | Even load | Lookup needs all-partition fan-out |
| **[[key-range-partitioning|Key range]]** | Each partition holds a continuous key range | Range queries efficient | Hotspots if keys arrive in order |
| **[[hash-partitioning|Hash]]** | Hash the key, partition by hash range | Even load distribution | Range queries lose efficiency |
| Compound (Cassandra) | Hash the first key, sort by the second within partition | Range queries within a partition | Schema constraint |

## Mechanism — what to partition by

You partition by a **partition key** — usually the primary key of the record. Bad choices create hot spots:

- Sequential timestamps → all new writes go to one partition.
- Celebrity user IDs → all reads of that user's content hit one partition.
- Anything with skewed distribution.

## Mechanism — secondary indexes

Secondary indexes don't fit the partition layout for free. See [[secondary-indexes-partitioning]] for the by-document vs by-term trade-off.

## Mechanism — rebalancing

When nodes are added/removed or partitions grow uneven, data must move. See [[rebalancing-partitions]].

## Trade-offs

- **+** Scales to datasets and write rates that no single machine can handle.
- **−** Hot spots can defeat the entire scheme.
- **−** Cross-partition queries are slow (scatter/gather).
- **−** Multi-partition transactions need [[two-phase-commit|2PC]] or similar.

## Examples in the syllabus

- s. 4 of the lecture lists the per-DBMS terminology.
- Cassandra "vnodes," HBase regions, MongoDB shards.

## Common exam framing

- "Distinguish partitioning from replication. Why are they usually combined?"
- "What is a hot spot, and why does timestamp-keyed range partitioning cause one?"
- "Why does the partition strategy matter for secondary indexes?"

## See also

- [[replication]]
- [[key-range-partitioning]]
- [[hash-partitioning]]
- [[secondary-indexes-partitioning]]
- [[rebalancing-partitions]]
