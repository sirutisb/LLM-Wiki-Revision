---
title: "Rebalancing partitions"
type: concept
sources: [distributed-architectures-partitioning, distributed-architectures-part-2]
related: [partitioning, hash-partitioning, key-range-partitioning]
updated: 2026-05-02
---

# Rebalancing partitions

*Moving data between nodes as throughput grows, the dataset grows, or nodes fail. Production systems do this incrementally — never re-shard the whole dataset live.*

## Definition

**Rebalancing** is the process of moving data and load from one node to another in a partitioned cluster. Triggered by:

- Throughput growing past a node's capacity.
- Dataset growing past a node's capacity.
- A node failing.
- Adding a new node.

## Goals (s. 19)

- After rebalancing, load (storage, reads, writes) is shared fairly.
- **During rebalancing, the database keeps serving reads and writes** — no full-cluster downtime.
- **Move as little data as possible** to minimise network and disk I/O. Avoid moving data *between* partitions if you can avoid it.

## Mechanism — Strategy 1: fixed number of partitions

- Create **many more partitions than nodes** (e.g. 1,000 partitions on 10 nodes → 100 each).
- The number of partitions never changes; the assignment of keys → partitions never changes. **Only which node hosts which partition changes.**
- When you add a node, it "steals" entire partitions from other nodes.
- Each partition is small enough to migrate quickly.

Used by: Riak, Couchbase, Elasticsearch, Voldemort.

## Mechanism — Strategy 2: dynamic partitioning

- Partitions split when they exceed a size threshold (e.g. 10 GB) and merge when they shrink below another.
- Like B-tree node splits/merges, but at the partition level.
- Adapts to dataset size automatically.

Used by: HBase, MongoDB (range-sharded mode).

## Mechanism — Strategy 3: partitioning proportional to nodes

A fixed number of partitions **per node**. When you add a node, randomly choose existing partitions to split, taking half of each onto the new node. Used by Cassandra and Ketama.

## Trade-offs

| Strategy | Pros | Cons |
|---|---|---|
| Fixed number | Predictable; partition→key mapping is stable | Have to choose partition count up front (under- or over-shoot is bad) |
| Dynamic | Adapts to size automatically | Splits and merges are operational events; key→partition mapping changes |
| Proportional | Adapts to cluster size | Random splits can cause hotspots |

## Examples in the syllabus

- s. 18–21 cover the topic.
- The fixed-partition strategy (s. 20) and dynamic partitioning (s. 21) are both named.

## Common exam framing

- "Why is rebalancing necessary in a partitioned database?"
- "Compare 'fixed number of partitions' and 'dynamic partitioning.' What are the trade-offs?"
- "List two goals of a good rebalancing strategy."

## See also

- [[partitioning]]
- [[hash-partitioning]]
- [[key-range-partitioning]]
