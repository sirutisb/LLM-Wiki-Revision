---
title: "Hash index"
type: concept
sources: [storage-and-retrieval]
related: [database-log, sstables, lsm-tree, compaction]
updated: 2026-05-02
---

# Hash index

*An in-memory hash map from key → byte offset in the data file. Simple, fast for point lookups, and totally useless for range queries.*

## Definition

A **hash index** is the simplest practical index for a [[database-log|log-structured]] store: keep a hash map in RAM where every key points to the byte offset of the most recent value for that key in the log file. Every write appends to the log *and* updates the map.

This is the indexing strategy of **Bitcask** (the storage engine of Riak).

## Why it matters

It's the cheapest possible upgrade from O(n) log scans to O(1) point lookups. The downsides are equally cheap to state.

## Mechanism

```
Log file (on disk):
  ...
  offset 4096:  cat42 -> {name: "Whiskers", views: 5}
  offset 4128:  dog17 -> {name: "Buddy", views: 12}
  offset 4160:  cat42 -> {name: "Whiskers", views: 6}   <-- newer

In-memory hash map:
  cat42 -> 4160
  dog17 -> 4128
```

- **Read:** look up the offset in the map, seek, read.
- **Write:** append to log, update the map.
- **Delete:** append a tombstone, remove from the map.
- **Compaction:** rewrite a segment, keeping only the latest value per key. Update the map's offsets.

## Trade-offs

**Advantages**
- Sequential writes are much faster than random disk access.
- Crash recovery is simpler — you don't overwrite, so the old value persists until compacted, and you can rebuild the map by scanning the log.

**Disadvantages**
- The hash table must **fit in memory.** If the keyset is huge, you can't.
- **No range queries.** Hashes are unordered, so retrieving keys `kitty1000` to `kitty2000` requires scanning every key in the map.
- High write rates with many distinct keys lead to constant compaction work.

## Examples in the syllabus

- The simple key-value DB of Storage and Retrieval s. 10–13.
- Bitcask (Riak) is the canonical real implementation.

## Common exam framing

- "Describe the structure of a hash index and the operations needed for read, write, and delete."
- "Give two reasons why a hash index might be unsuitable for a particular workload." → memory, ranges.
- "Why must compaction run alongside a hash-index storage engine?"

## See also

- [[database-log]]
- [[sstables]]
- [[compaction]]
