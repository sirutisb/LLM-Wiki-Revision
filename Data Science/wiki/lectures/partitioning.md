---
title: "Lecture: Distributed Architectures — Partitioning"
type: lecture
sources: [distributed-architectures-partitioning, distributed-architectures-part-2]
related: [partitioning, key-range-partitioning, hash-partitioning, secondary-indexes-partitioning, rebalancing-partitions]
updated: 2026-05-02
---

# Lecture: Distributed Architectures — Partitioning

*When the dataset doesn't fit on one machine, you split it. The partition strategy determines how evenly load spreads, whether range queries are efficient, and how you handle secondary indexes.*

> **Source note:** the 2024-style "Partitioning" deck and the 2025 "part 2" deck cover almost identical material. The 2025 deck (canonical) expands secondary indexes into two slides; the 2024 deck has it as one. This page merges both.

## Slide-by-slide notes

- **(s. 2)** Distributing data across nodes — two strategies, often combined:
  - [[replication]] — copies of the same data on every node.
  - [[partitioning]] — different subsets of the data on different nodes.
- **(s. 4)** Vocabulary clash — different DBMSs use different names:
  - **Shard** — MongoDB, Elasticsearch, Firestore.
  - **Region** — HBase.
  - **Vnode** — Cassandra.
- **(s. 5)** Each piece of data belongs to **exactly one** partition; a node can hold many partitions; query load is spread across nodes. Often combined with replication so that each partition has multiple copies.
- **(s. 6)** Combined with leader-follower replication: each partition has its own leader, assigned to one node; that partition's followers live on other nodes. So one node can be a leader for some partitions and a follower for others.
- **(s. 7)** The goal: spread data and load **evenly**. If partitioning is fair, 10 nodes handle 10× the load. **Skewed partitioning** creates **hot-spot nodes** — some partitions are queried disproportionately.
- **(s. 8)** **The simplest approach** — random scattering — distributes data and load evenly, but searching for an item requires querying all nodes. Bad. We need something keyed.
- **(s. 9)** [[key-range-partitioning]] — assign a continuous range of keys to each partition, like volumes of a paper encyclopaedia. Keys are sorted; ranges aren't necessarily evenly spaced.
  - **Pro:** range queries are efficient (adjacent keys, adjacent storage).
  - **Con:** **write hotspots** if keys arrive in order (e.g. timestamps — every new write goes to the same partition).
- **(s. 10–12)** [[hash-partitioning]] — apply a hash function to the key, partition by hash range.
  - **Pro:** distributes keys evenly across partitions; no timestamp hotspot.
  - **Con:** **range queries become expensive** — adjacent keys are scattered.
  - MongoDB workaround: send range queries to all partitions.
  - Cassandra workaround: **compound keys** — hash on the first key, sort within partition by the second. Lets you range-scan inside a single partition.
- **(s. 13)** [[secondary-indexes-partitioning|Secondary indexes]] — unlike the primary key, a secondary index doesn't uniquely identify a record (e.g. "users in city X"). They don't map neatly to the partition layout. Two strategies:
  - **By document** (local indexes).
  - **By term** (global / inverted indexes).
- **(s. 14)** **Partitioning secondary indexes by document:**
  - Each document lives in exactly one partition (by primary key).
  - Each partition maintains its **own local secondary index** of its documents.
  - **Pros:** simple, scalable, writes are local (one partition).
  - **Cons:** reads on the secondary attribute must **fan out to every partition** ("scatter/gather") and merge results.
  - Used by: MongoDB, Cassandra (local secondary indexes).
- **(s. 15)** **Partitioning secondary indexes by term:**
  - The index itself is partitioned, by the secondary attribute (the "term").
  - E.g. an inverted index city → user_ids, partitioned by city.
  - **Pros:** efficient reads — a term query routes to one or a few partitions.
  - **Cons:** **writes are complex** — updating a document means writing to its primary partition *and* updating the term index in another partition; needs coordination.
  - Used by: Elasticsearch, some Cassandra setups.
- **(s. 16)** Summary table:
  | Strategy | Partition basis | Query efficiency | Write complexity | Used by |
  |---|---|---|---|---|
  | By document | Primary key | Fast for key, slow for secondary | Simple | MongoDB |
  | By term | Secondary key (term) | Fast for secondary | Complex (multi-partition writes) | Cassandra, Elasticsearch |
- **(s. 18)** [[rebalancing-partitions|Rebalancing]] — moving data between nodes when:
  - Throughput grows.
  - Dataset grows.
  - A node fails.
- **(s. 19)** Goals of rebalancing:
  - After: load is shared fairly.
  - During: the database keeps serving reads and writes.
  - Move only as much data as needed (network and disk I/O are expensive). **Avoid moving data between partitions.**
- **(s. 20)** **Fixed number of partitions** strategy:
  - Create *many* more partitions than nodes (e.g. 1,000 partitions on 10 nodes → 100 each).
  - When nodes are added, they "steal" entire partitions from other nodes.
  - The number of partitions and the assignment of keys → partitions never changes — only which node hosts each partition.
- **(s. 21)** **Dynamic partitioning:**
  - If a partition exceeds a threshold (e.g. 10 GB), split it in two.
  - If partitions get small, merge them.
  - Used by HBase, MongoDB.

## Key takeaways

1. **Partitioning targets dataset and write scaling**, where [[replication]] targets reads and availability.
2. **Random scatter** distributes load but kills lookups. Real systems hash or range.
3. **Hash partitioning is the default** for write-balanced workloads. **Key-range** is preferred when range queries are common, with care taken to avoid timestamp-style hotspots.
4. **Secondary indexes are the painful part.** *By document* is cheap to write but expensive to query; *by term* is the reverse. Choose based on workload.
5. **Hot spots ruin partition schemes.** A celebrity user, a popular timestamp range, or a bad key-distribution can make one partition the bottleneck.
6. **Rebalancing is incremental.** Production systems either pre-split into many partitions or split dynamically — they never re-shard the whole dataset live.

## Concepts introduced

- [[partitioning]]
- [[key-range-partitioning]]
- [[hash-partitioning]]
- [[secondary-indexes-partitioning]]
- [[rebalancing-partitions]]

## Open questions / things to clarify

- **Consistent hashing** isn't named explicitly in the slides but underpins hash-partitioning rebalancing in real systems (Cassandra, DynamoDB).

## See also

- [[replication]]
- [[partitioning]]
- [[key-range-partitioning]]
- [[hash-partitioning]]
- [[secondary-indexes-partitioning]]
- [[rebalancing-partitions]]
