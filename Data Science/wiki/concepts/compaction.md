---
title: "Compaction"
type: concept
sources: [storage-and-retrieval]
related: [database-log, hash-index, sstables, lsm-tree]
updated: 2026-05-02
---

# Compaction

*The background process that reclaims space in log-structured storage by discarding superseded keys and merging segments. Without it, append-only stores grow without bound.*

## Definition

**Compaction** is the act of rewriting one or more storage segments to:

1. Remove superseded versions of a key (only the latest write matters).
2. Drop tombstones (records of deletion) once their masking is complete.
3. Merge multiple segments into one.

It's the dual of "append-only writes": appends are cheap because they never overwrite; compaction periodically pays the bill.

## Why it matters

Every log-structured engine ([[hash-index]] over a [[database-log|log]], [[sstables|SSTables]], [[lsm-tree|LSM-trees]]) needs compaction. Without it, the on-disk size grows monotonically and reads slow down (more segments to consult).

## Mechanism

For an SSTable-based system:

```
Old SSTables (sorted by key):
  S1: [a:1, b:2, c:3, d:4]
  S2: [b:9, e:5]                  <-- newer

Compactor mergesort over S1 + S2:
  a:1, b:9 (S2 wins), c:3, d:4, e:5

Result: one new SSTable; S1 and S2 are deleted.
```

Compaction strategies trade off CPU/IO vs space and read amplification:

- **Size-tiered (Cassandra default):** merge segments of similar size. Cheap CPU, more disk space.
- **Levelled (LevelDB, RocksDB):** organise segments into levels of fixed size, each ~10× the previous. More CPU, less disk space, more predictable read latency.

## Trade-offs

- **+** Reclaims space, drops dead keys, keeps reads fast.
- **+** Tombstones can finally be dropped (after they've masked all older versions).
- **−** Background CPU and disk I/O cost during compaction (write amplification).
- **−** Compaction storms can interfere with foreground throughput on busy systems.

## Examples in the syllabus

- Storage and Retrieval s. 12: the cat-video counter example — millions of writes for the same key, compaction reduces it to one entry.
- Every [[lsm-tree|LSM-tree]] system runs compaction continuously.

## Common exam framing

- "Why is compaction necessary in a log-structured storage engine?"
- "Briefly explain the difference between size-tiered and levelled compaction strategies."
- "What is write amplification and why is compaction the main source of it?"

## See also

- [[database-log]]
- [[sstables]]
- [[lsm-tree]]
