---
title: "LSM-tree (Log-Structured Merge-tree)"
type: concept
sources: [storage-and-retrieval]
related: [sstables, database-log, hash-index, b-tree, compaction]
updated: 2026-05-02
---

# LSM-tree (Log-Structured Merge-tree)

*The storage architecture you get when you combine an in-memory sorted memtable with a series of on-disk SSTable segments and a background compaction process. Optimised for write-heavy workloads.*

## Definition

An **LSM-tree** (Log-Structured Merge-tree) is a write-optimised storage structure made of:

- A **memtable** — an in-memory balanced tree (AVL, red-black) that holds recent writes.
- A sequence of on-disk **[[sstables|SSTable]]** segments — sorted, immutable files written by flushing the memtable.
- A **compaction** process — merges and shrinks segments in the background.
- A **write-ahead log** (WAL) — durability backstop: writes go to the WAL before the memtable, so a crash doesn't lose data still in RAM.

Although Dr Barbosa's slides describe this construction without naming it, the canonical name is **LSM-tree** (LevelDB, RocksDB, Cassandra, HBase, ScyllaDB).

## Why it matters

LSM-trees absorb writes faster than [[b-tree|B-trees]] because they convert random writes into **sequential** ones. They're the workhorse of modern write-heavy systems — time-series databases, log analytics, key-value stores.

## Mechanism

```
Write:
   client -> WAL (durability)
          -> memtable (in RAM)

When memtable full:
   flush memtable -> new SSTable on disk
   new memtable starts empty

Read:
   look in memtable
   then SSTables, newest to oldest
   stop when found

Background:
   compactor merges SSTables, drops tombstones, deduplicates keys
```

## Trade-offs (LSM vs B-tree)

| | LSM-tree | [[b-tree]] |
|---|---|---|
| Write path | Sequential, append + flush | In-place updates + WAL |
| Write throughput | High | Moderate |
| Write amplification | High (compaction rewrites data) | Low–moderate |
| Read latency | Variable — may touch multiple segments | Low and predictable |
| Range queries | Efficient (sorted segments) | Efficient (sorted leaves) |
| Disk space | More (until compaction) | Less |
| Suited to | Write-heavy, log/time-series | Read-heavy, transactional |

## Mechanism — Bloom filters

Reading an absent key in an LSM is expensive — you check every segment. Real implementations attach a **Bloom filter** to each segment ("is this key probably here?") to skip segments quickly when the key isn't there.

## Examples in the syllabus

- s. 16–17 of Storage and Retrieval describe LSM construction (memtable + SSTable flush + background compaction).
- Cassandra ([[partitioning]]) uses LSM internally.
- HBase, RocksDB, LevelDB all use LSM.

## Common exam framing

- "Compare LSM-trees and B-trees on write throughput and read latency."
- "What is the role of the memtable, WAL, and compaction in an LSM-tree?"
- "Why are LSM-trees a natural fit for write-heavy workloads such as time-series ingestion?"

## See also

- [[sstables]]
- [[b-tree]]
- [[database-log]]
- [[compaction]]
