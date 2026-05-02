---
title: "Topic: Storage"
type: topic
sources: []
related: [lsm-tree, b-tree, sstables, hash-index, database-log, compaction, oltp-vs-olap, distributed-filesystem]
updated: 2026-05-02
---

# Topic: Storage

*How data is durably stored — from single-node storage engines to distributed filesystems.*

## Storage engines

Two dominant architectures:

- **[[lsm-tree]]** — write-optimised; append-only; memtable + SSTable + compaction.
- **[[b-tree]]** — read-optimised; mutable pages; in-place updates; standard OLTP.

Supporting concepts:
- [[database-log]] — the append-only foundation.
- [[hash-index]] — in-memory index for fast key lookups over a log.
- [[sstables]] — sorted, immutable on-disk files in LSM trees.
- [[compaction]] — background merge of SSTables; reclaims space, removes tombstones.

## Workload types

- [[oltp-vs-olap]] — online transaction processing (many small random reads/writes) vs online analytical processing (large sequential scans).

## Distributed storage

- [[distributed-filesystem]] — HDFS, Colossus; blocks, replication, data locality for batch jobs.

## See also

- [[lsm-tree]]
- [[b-tree]]
- [[oltp-vs-olap]]
- [[batch-processing]]
