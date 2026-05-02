---
title: "Replication vs partitioning"
type: comparison
sources: [distributed-architectures-replication, distributed-architectures-partitioning, review]
related: [replication, partitioning, scalability, cap-theorem]
updated: 2026-05-02
---

# Replication vs partitioning

*Two complementary techniques for distributing data — replication copies the same data to multiple nodes; partitioning splits different data across nodes. Production systems use both together.*

## Summary

**Replication** solves availability and read scalability — more copies means more machines can serve reads and the system survives node failures. **Partitioning** solves storage and write scalability — data too large to fit on one machine is spread across many. They're not alternatives; they're used together.

## Comparison table

| Dimension | Replication | Partitioning |
|---|---|---|
| **What it stores** | Full copy of all data | Subset of data |
| **Primary goal** | Availability, read throughput, latency | Storage scalability, write throughput |
| **Data size constraint** | All data must fit on one node | Removes this constraint |
| **Fault tolerance** | Survive node failures (other replicas serve) | Reduces blast radius per node |
| **Consistency challenge** | Replication lag, stale reads | Cross-partition queries, scatter-gather |
| **Complexity** | Leader failover, split brain | Rebalancing, hotspot avoidance |
| **Used in** | MySQL leader-follower, Cassandra | Cassandra, HBase, MongoDB |

## Key differences explained

**Replication lag** is the core consistency challenge for replication — followers can serve stale data. Partitioning's consistency challenge is cross-partition operations: a query spanning multiple partitions must scatter to all and gather results.

**Hotspots** are partitioning's performance trap — if one partition key is disproportionately popular (celebrity user, sequential timestamps), one node gets overwhelmed while others idle. Replication doesn't have this problem (all replicas get all writes).

## Used together

In practice: data is partitioned first (spread across N nodes for scale), then each partition is replicated (K copies per partition for fault tolerance). Every node is the leader for some partitions and a follower for others.

## Decision rule

> Use partitioning when data won't fit on one machine or writes need horizontal scale. Use replication for read scale and availability. Use both in production.

## See also

- [[replication]]
- [[partitioning]]
- [[scalability]]
- [[cap-theorem]]
