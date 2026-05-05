---
title: SSTables and LSM-Trees
type: revision
sources: [storage-and-retrieval]
updated: 2026-05-05
---

# SSTables and LSM-Trees

*The evolution of log-structured storage: moving from unsorted logs (Hash Indexes) to sorted segments (SSTables) to solve memory and query limitations.*

## 1. The Problem with Hash Indexes
As discussed in [[Log-Structured-Storage]], simple hash indexes have two major flaws:
1.  **Memory Bound:** Every key must be in RAM. If you have more keys than RAM can hold, the system fails.
2.  **No Range Queries:** You can't efficiently find a range of keys (e.g., all IDs between 100 and 200) because hashes are unordered.

## 2. The Solution: SSTables (Sorted String Tables)
An **SSTable** is a segment file where the keys are **sorted**. This simple change unlocks two massive improvements:

### A. Sparse Indexes (Solving the RAM Limit)
Because the file is sorted, we don't need to store every key in RAM. We only need a **Sparse Index**—storing the offset for every (e.g.) 4KB of data.
- To find a key, we look in the sparse index to find the range it falls into, then scan that small 4KB chunk on disk.
- **Result:** We can store millions of keys using only a few MB of RAM.

### B. Efficient Range Queries
Since keys are sorted on disk, a range query (e.g., `Get keys A to C`) is just a sequential read starting from "A" and stopping at "C". Disk sequential I/O is extremely fast.

## 3. The Mechanism: How it works (LSM-Trees)
Since we can't "append" to a sorted file while keeping it sorted, we use an **LSM-tree** (Log-Structured Merge-Tree) approach:

1.  **The Memtable (In RAM):** New writes are added to a sorted tree structure in memory (e.g., Red-Black tree).
2.  **The Flush (To Disk):** When the Memtable gets big enough, it is written to disk as a new, immutable SSTable segment.
3.  **The Read Path:** To find a key, check the Memtable first, then check SSTable segments from newest to oldest.
4.  **Compaction (Mergesort):** A background process merges multiple SSTables. Because they are sorted, this uses a high-performance **Mergesort** algorithm to discard old values and tombstones.

## 4. Comparison Table

| Feature | Hash Index (Unsorted Log) | SSTable (LSM-Tree) |
| :--- | :--- | :--- |
| **On-disk order** | Order of arrival | **Sorted by key** |
| **In-Memory Index** | **Dense** (Every key in RAM) | **Sparse** (One key per block) |
| **Range Queries** | Impossible (requires full scan) | **Native & Efficient** |
| **Memory Usage** | High (grows with # of keys) | **Low** (fixed per block) |
| **Merging** | Basic deduplication | **Mergesort** (very efficient) |

## 5. Summary
- **SSTables** provide sorted, immutable storage on disk.
- **Memtables** handle the sorting in RAM before writing.
- **LSM-Trees** are the overall architecture combining both.
- Together, they allow databases to handle massive datasets with high write throughput and efficient range searches while staying within RAM limits.

*See also: [[Log-Structured-Storage]] for the foundations.*
