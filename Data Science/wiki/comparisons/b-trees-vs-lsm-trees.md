---
title: "B-trees vs LSM-trees"
type: comparison
sources: [storage-and-retrieval]
related: [b-tree, lsm-tree, sstables, oltp-vs-olap]
updated: 2026-05-06
---

# Comparison: B-trees vs LSM-trees

*The fundamental choice in storage engine design: update-in-place vs. append-only.*

## Overview

Storage engines generally fall into two categories: **log-structured** (LSM-trees) or **page-oriented** (B-trees). The choice between them is driven by the expected workload (write-heavy vs. read-heavy) and the need for predictable performance.

## Comparison Table

| Dimension | B-trees | LSM-trees |
| :--- | :--- | :--- |
| **Design Philosophy** | Update-in-place (Page-oriented) | Append-only (Log-structured) |
| **Primary Structure** | Fixed-size pages on disk | Memtable (RAM) + SSTables (Disk) |
| **Write Performance** | Lower (Random I/O + WAL) | **Higher** (Sequential I/O) |
| **Read Performance** | **Higher/Predictable** (1 place per key) | Variable (May check multiple levels) |
| **Write Amplification** | Moderate (Torn pages/WAL) | High (Data rewritten during compaction) |
| **Space Overhead** | Lower (Fragments pages) | Higher (Until compaction runs) |
| **Transactionality** | Strong (Easier to lock ranges) | Complex (Atomic across segments) |
| **Best For** | OLTP, transactional consistency | Write-heavy, time-series, logging |

## Detailed Analysis

### Why B-trees win on Reads
In a B-tree, each piece of data is stored in exactly one place (a specific leaf page). Finding a key requires a fixed number of page reads determined by the tree's depth (typically 3 or 4). This results in **predictable latency**.

### Why LSM-trees win on Writes
LSM-trees turn random writes into sequential ones by buffering them in a `memtable`. Periodically, this is flushed to disk as a sorted `SSTable`. Sequential writes are significantly faster than random writes, especially on magnetic hard drives, and even on SSDs.

### The Cost of Compaction
LSM-trees require a background process called **compaction** to merge SSTables and remove duplicates/deleted keys. This can lead to "compaction storms" where the system's performance dips because the background I/O is competing with user requests.

## Exam Framing

- **Scenario:** "A high-frequency trading platform needs to log millions of price updates per second."
  - **Answer:** **LSM-tree**, as it is optimised for high-volume sequential writes.
- **Scenario:** "A banking system requires consistent, low-latency lookups for customer balances."
  - **Answer:** **B-tree**, as it provides the most predictable read latency and fits the transactional (OLTP) model.

## See also

- [[b-tree]]
- [[lsm-tree]]
- [[sstables]]
- [[oltp-vs-olap]]
