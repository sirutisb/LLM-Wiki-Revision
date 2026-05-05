---
title: Hash Index and Log-Structured Storage
type: revision
sources: [storage-and-retrieval]
updated: 2026-05-05
---

# Hash Index and Log-Structured Storage

*Understanding the fundamental "append-only" storage engine used in modern high-performance databases.*

## 1. The Core: Append-Only Log
Instead of updating data in place, many databases treat their physical data file as an **append-only log**.

- **Sequential I/O:** Every write is simply appended to the end of the file. This is extremely fast because it avoids disk "seeks" (moving the physical disk head).
- **Binary Format:** Data is stored in binary for efficiency—it is smaller, requires no escaping, and is faster for a computer to parse than plain text (CSV/JSON).
- **Immutability:** Once written, a record is never changed. Updates and deletes are just *more* appends.

## 2. The Index: Hash Map in RAM
Since scanning a 10GB file for a single key is O(n), we use a **Hash Index** to make it O(1).

- **Structure:** An in-memory hash map that stores `Key -> Byte Offset`.
- **Read Path:** Look up the key in RAM $\rightarrow$ Get the offset (e.g., 4096) $\rightarrow$ Seek to that byte on disk $\rightarrow$ Read the record.
- **Write Path:** Append data to the disk file $\rightarrow$ Update the RAM index with the new offset.

## 3. Handling Change: Tombstones & Compaction
Since we never "edit" the file, we need a way to handle growth and deletions.

- **Updates:** Append the new value. Update the RAM index to point to the new offset. The old version still exists on disk but is effectively "orphaned" by the index.
- **Deletes:** Append a **Tombstone**. This is a special record that tells the database the key is deleted. The RAM index is updated to show no value exists.
- **Segmentation:** The log is broken into "segments" (e.g., every 100MB). When one segment is full, a new one is started.
- **Compaction:** A background process merges segments. It discards old, overwritten values and tombstones, keeping only the **most recent** version of each key. This keeps disk usage under control.

## 4. Key Trade-offs

| Feature        | Advantage                                                  | Disadvantage                                                                                                    |
| :------------- | :--------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------- |
| **Throughput** | Sequential writes are the fastest possible disk operation. | **Write Amplification:** Data is written once to the log, then rewritten during compaction.                     |
| **Lookup**     | O(1) reads via the hash index.                             | **Memory Bound:** The entire index (every key) MUST fit in RAM.                                                 |
| **Queries**    | Simple and predictable performance.                        | **No Ranges:** You cannot efficiently query "all users with ID between 10 and 20" because hashes are unordered. |

## 5. Summary of the Process
1. **Append** to log (Disk) — High performance, sequential.
2. **Update** offset map (RAM) — Fast O(1) lookups.
3. **Tombstone** for deletes — Safe, non-destructive deletion.
4. **Segment** when full — Makes data manageable.
5. **Compact** in background — Reclaims disk space and improves read speed.

*See also: [[sstables]] for how we solve the "RAM limit" and "range query" problems.*
