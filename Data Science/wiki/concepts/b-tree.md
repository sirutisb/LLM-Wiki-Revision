---
title: "B-tree"
type: concept
sources: [storage-and-retrieval]
related: [lsm-tree, sstables, oltp-vs-olap]
updated: 2026-05-02
---

# B-tree

*The dominant index structure of relational databases. Update-in-place, page-based, and optimised for predictable read performance.*

## Definition

A **B-tree** is a balanced search tree whose nodes are fixed-size **pages** (typically 4 KB) on disk. Each internal page contains a sorted array of keys with pointers to child pages; leaves hold the actual values (or pointers to them in a heap file).

Reading a page involves a single disk seek; the tree is shallow because each page can fan out to hundreds of children. A B-tree of depth 4 with branching factor 500 indexes ~62 billion entries.

## Why it matters

Practically every relational database — PostgreSQL, MySQL/InnoDB, SQL Server, Oracle — uses B-trees (or the leaf-linked B+tree variant) as the default index structure. Knowing how they differ from [[lsm-tree|LSM-trees]] is the canonical exam question on storage engines.

## Mechanism — write path

Writes update pages **in place**:

```
1. Find the leaf page that should contain the new key.
2. If it has space, insert and write the page back.
3. If it's full, split into two pages, push a key up to the parent.
4. The parent might split too — splits propagate up to the root.
```

A **write-ahead log** (WAL) protects against torn page writes — every page modification is logged before it's applied.

## Mechanism — read path

Walk root → internal → leaf, one page-read per level. Read latency is bounded by tree depth, which grows logarithmically.

## Trade-offs vs LSM

See [[lsm-tree#trade-offs-lsm-vs-b-tree]] for the full table. Headline:

- **B-tree wins** on read latency (one place per key, no merge), predictability (no compaction storms), and disk usage.
- **LSM wins** on write throughput, by avoiding random in-place updates.

## Examples in the syllabus

The lecture slides don't introduce B-trees explicitly — the deck stops at LSM. But Kleppmann ch. 3 covers them, and they're the obvious comparison point if asked "why might you choose a B-tree over an LSM-tree?"

## Common exam framing

- "Explain how a B-tree index supports range queries efficiently."
- "Compare B-trees and LSM-trees: which would you pick for (a) a banking ledger, (b) a clickstream ingest pipeline?"
- "What is the role of the write-ahead log in a B-tree storage engine?"

## See also

- [[lsm-tree]]
- [[sstables]]
- [[oltp-vs-olap]]
