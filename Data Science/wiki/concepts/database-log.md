---
title: "Database log (append-only file)"
type: concept
sources: [storage-and-retrieval]
related: [hash-index, sstables, lsm-tree, compaction]
updated: 2026-05-02
---

# Database log (append-only file)

*Many storage engines record data in append-only log files. Reads are O(n) without an index — but writes are O(1) and sequential, which is the fastest thing a disk can do.*

## Definition

In this lecture's sense, a **log** is not an audit trail but the **physical data file**: a read-only, append-only sequence of records on disk. Writes append; deletes append a tombstone; updates append a new value (the old one becomes garbage waiting for [[compaction]]).

## Why it matters

Sequential disk writes are dramatically faster than random writes — typically two orders of magnitude on HDDs and still much faster on SSDs. Building the storage engine on a log lets the database absorb high write throughput without paying the random-access tax.

## Mechanism — properties of a log

- **Append-only.** Writes never seek; they extend the file.
- **Read-by-scan is O(n).** This is unacceptable for production use, so logs are paired with indexes ([[hash-index]], [[sstables]], or B-tree leaves).
- **Crash recovery is straightforward.** You don't overwrite, so a partial write at the tail is the only damage; truncate to the last good record.
- **Deletes use tombstones.** A special "this key is deleted" marker is appended. The actual bytes are reclaimed by compaction.
- **Segments + compaction.** A single log file would grow forever; instead, close at a size threshold and roll over. Compaction merges old segments and discards superseded keys.

## Things to consider (s. 8)

- **File format.** Binary is more compact and faster to parse than text.
- **Partially-written records.** Checksums identify torn writes; the recovery process truncates them.
- **Concurrency control.** Single writer is the easiest; multiple writers need coordination (locks, MVCC, or a write-ahead log).
- **Crash recovery of indexes.** The in-memory index is volatile; on restart, either rebuild it from the log (slow) or persist a snapshot.

## Trade-offs

- **+** Sequential writes are fast and friendly to the storage hardware.
- **+** Crash safety is conceptually simple.
- **−** Wastes space until compaction runs.
- **−** Pure log + scan = O(n) reads; needs an index layered on top.

## Examples in the syllabus

- The toy "very simple database" of slides 5–7 — bash `db_set` / `db_get` from the textbook.
- [[lsm-tree|LSM-trees]] (Cassandra, RocksDB, LevelDB) are the production form: log + sorted segments + compaction.

## Common exam framing

- "Why are sequential writes so much faster than random ones, and how do log-structured storage engines exploit this?"
- "How does a log-based engine handle deletes? Why?" → tombstone, lazy reclamation, compaction.
- "Sketch the trade-off between read and write performance in a pure log."

## See also

- [[hash-index]]
- [[sstables]]
- [[lsm-tree]]
- [[compaction]]
