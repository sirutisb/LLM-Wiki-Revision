---
title: "Lecture: Storage and Retrieval"
type: lecture
sources: [storage-and-retrieval, storage-and-retrieval-2024]
related: [database-log, hash-index, sstables, lsm-tree, b-tree, oltp-vs-olap]
updated: 2026-05-02
---

# Lecture: Storage and Retrieval

*How databases physically store data on disk and find it again — the core distinction between log-structured and page-based engines, and why the workload (transactional vs analytical) drives the choice.*

## Slide-by-slide notes

- **(s. 2)** *Past:* the format we hand to the database and how we query it from the application side. *Today:* what the database does internally.
- **(s. 3)** A database has two fundamental jobs: **store** what you give it, and **retrieve** it on request. The big design choice is the **storage engine**, and the right choice depends on the workload:
  - **Transactional (OLTP):** write-intensive, many small reads/writes by primary key.
  - **Analytical (OLAP):** read-intensive, scans over many rows, aggregations.
  - See [[oltp-vs-olap]] for the full comparison.
- **(s. 5–6)** *A very simple database* is a key-value store. Reads and writes both live in a single append-only file. Question: what's the performance profile?
  - Write: O(1) — append.
  - Read: O(n) — scan from the start.
- **(s. 7)** [[database-log]] — many real databases use a *log* (read-only data files storing records in sequence) to record data. O(n) reads are unacceptable, so we need indexes.
- **(s. 8)** Things to consider when implementing a log:
  - **File format** — binary is more efficient than plain text.
  - **Deletes** — rather than scan and rewrite, append a special **tombstone** record.
  - **Crash recovery** — if the in-memory hash map is lost, you must rebuild it.
  - **Partially-written records** — checksums and atomic-write protocols.
  - **Concurrency control** — single writer, many readers is the easy case.
- **(s. 10)** [[hash-index]] — keep an in-memory hash map from key to byte offset in the log file. Every append updates the map. Simple, efficient — *as long as the hash map fits in memory*. (Bitcask is the canonical implementation.)
- **(s. 11)** **Segment files** — append-only files would grow forever. So: close the file when it hits a certain size and start a new segment. Old segments become candidates for compaction.
- **(s. 12)** **Compaction** — discard duplicate keys (only the latest write matters). Example: a counter that's been written millions of times — compaction reduces it to one entry.
- **(s. 13)** [[hash-index|Hash table]] **trade-offs:**
  - *Pro:* sequential writes are much faster than random disk access; crash recovery is simple (you don't overwrite, you append).
  - *Con:* the hash table must fit in memory; range queries (`kitty1000` to `kitty2000`) require scanning every key.
- **(s. 14–17)** [[sstables|SSTables]] (Sorted String Tables):
  - Each key appears once per segment.
  - Keys are kept **sorted**.
  - Compaction = merge two sorted segments → sorted output (mergesort step).
  - **In-memory index is sparse** — you only index a fraction of keys; binary-search the segment for the rest.
  - **Range queries** are now efficient.
- **(s. 17)** Construction: writes go into an in-memory balanced tree (a **memtable**, e.g. AVL tree). When the memtable fills, dump it to disk as a new SSTable. Reads consult: memtable → newest SSTable → next-newest → … → oldest. Background process performs **compaction and merging**.

> **The above describes the [[lsm-tree|LSM-tree]] (Log-Structured Merge-tree) family — used by LevelDB, RocksDB, Cassandra, HBase.** The lecturer doesn't name "LSM" explicitly in the slides but the architecture is exactly this.

## Background — material the slides assume but don't fully explain

The deck stops at LSM-trees but the textbook chapter (Kleppmann ch. 3) goes further. Likely assumed for the exam:

- **[[b-tree|B-trees]]** — the page-based alternative to LSM. Update-in-place rather than append. Used by virtually every relational DB. Differences: B-trees write each key in *one* place (so reads are fast and predictable); LSM appends and merges (so writes are fast).
- **[[oltp-vs-olap]]** — the workload distinction (transactional vs analytical) drives the engine choice; column-oriented storage is the OLAP-side answer.

## Key takeaways

1. Databases choose a storage engine to suit a workload. **OLTP wants point-key access; OLAP wants column scans.**
2. **Logs are the foundation.** Append-only is fast and crash-friendly; the indexing question is how to retrieve from a log without O(n) scans.
3. **Hash indexes** are simple but capped by memory and weak on ranges.
4. **SSTables / LSM-trees** trade some write amplification (compaction) for fast writes, range queries, and a sparse in-memory index.
5. **B-trees** trade higher write cost (in-place) for fast, predictable reads — they dominate relational DBs.
6. **Compaction** is what makes log-structured storage practical. Without it, disk usage grows without bound.

## Concepts introduced

- [[database-log]]
- [[hash-index]]
- [[sstables]]
- [[lsm-tree]]
- [[b-tree]]
- [[oltp-vs-olap]]
- [[compaction]]

## Open questions / things to clarify

- The slides do not cover B-trees explicitly, but they're textbook material. Confirm with Hugo whether B-trees are examinable.
- Column-oriented storage / OLAP engines (Parquet, columnar warehouses) are referenced via the OLTP/OLAP distinction but not detailed in the deck.

## See also

- [[hash-index]]
- [[sstables]]
- [[lsm-tree]]
- [[b-tree]]
- [[oltp-vs-olap]]
- [[data-models-nosql]]
