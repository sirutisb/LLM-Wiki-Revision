---
title: "SSTables (Sorted String Tables)"
type: concept
sources: [storage-and-retrieval]
related: [database-log, hash-index, lsm-tree, compaction, b-tree]
updated: 2026-05-02
---

# SSTables (Sorted String Tables)

*An on-disk segment file in which every key appears at most once and keys are kept in sorted order. Enables range queries, sparse indexes, and efficient merge-compaction.*

## Definition

An **SSTable** is a segment file with two extra invariants beyond a plain [[database-log|log]]:

1. **Each key appears at most once per segment.**
2. **Keys are sorted.**

These two changes unlock most of the benefits of modern log-structured storage.

## Why it matters

Sorting changes everything:

- **Range queries** — keys `kitty1000` … `kitty2000` are physically adjacent. Read once, walk forward.
- **Sparse in-memory index** — you don't need every key in RAM. Indexing every (e.g.) 1,000th key is enough; binary-search the segment between two indexed keys.
- **Cheap compaction** — merging two sorted segments is a mergesort step, even if neither fits in memory.

## Mechanism — write path

```
1. Write arrives  -->  in-memory balanced tree (AVL, red-black) called the memtable.
2. When memtable exceeds threshold (e.g. a few MB), flush it to disk as a new SSTable.
3. New writes go to a new memtable instance; the old SSTable is the most recent on-disk segment.
```

This is the construction algorithm of an [[lsm-tree|LSM-tree]].

## Mechanism — read path

```
1. Look in the memtable.
2. If miss, look in the most recent SSTable.
3. Then the next-most-recent, ... oldest.
4. Use the sparse index to seek directly to the relevant region.
```

Reads can be slow if a key has been compacted into deep segments. Bloom filters are commonly added to skip segments quickly when the key is absent.

## Mechanism — compaction

A background process merges adjacent SSTables. Because they're sorted, this is mergesort:

```
SSTable A:  [apple:1, banana:2, cherry:3]
SSTable B:  [banana:9, date:4, eel:5]
Merged:     [apple:1, banana:9 (newer wins), cherry:3, date:4, eel:5]
```

Tombstones get dropped here too.

## Trade-offs vs hash index

| | [[hash-index]] | SSTable |
|---|---|---|
| Memory cost | Every key in RAM | Sparse — only every Nth key |
| Range queries | No | Yes |
| Compaction | Per segment | Mergesort across segments |
| Write throughput | Highest (just append) | High (append + memtable) |
| Read latency | O(1) hash lookup | O(log N) within segment, possibly multiple segments |

## Examples in the syllabus

- The construction described in s. 14–17 is exactly an [[lsm-tree|LSM-tree]].
- LevelDB, RocksDB, Cassandra, HBase, Bigtable all use SSTables under the hood.

## Common exam framing

- "Why is the in-memory index of an SSTable sparse rather than dense?"
- "Describe the role of the memtable in an SSTable-based storage engine."
- "How does compaction work over sorted segments? Why is sorting essential to it?"

## See also

- [[lsm-tree]]
- [[hash-index]]
- [[b-tree]]
- [[compaction]]
