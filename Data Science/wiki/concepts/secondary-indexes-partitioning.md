---
title: "Partitioning secondary indexes"
type: concept
sources: [distributed-architectures-part-2]
related: [partitioning, hash-partitioning, key-range-partitioning]
updated: 2026-05-02
---

# Partitioning secondary indexes

*Secondary indexes don't fit the partition layout for free. Two strategies: by-document (local) or by-term (global). The choice trades read efficiency against write complexity.*

## Definition

A **secondary index** is an index on a non-primary attribute — used for search and sorting rather than direct lookup. Examples: city of a user, tags on a post, status of an order.

In a partitioned database, secondary indexes pose a problem: a record sits in one partition (determined by its primary key), but a secondary attribute (e.g. city) doesn't determine which partition holds the record.

## Mechanism — Strategy 1: partitioning by document (local index)

Each partition keeps its **own local secondary index** covering only its own records.

```
Partition 1 (users 0–999):
  Records:    user42 (city=London), user99 (city=Exeter), ...
  Local idx:  city -> [user_ids in this partition]

Partition 2 (users 1000–1999):
  Records:    user1042 (city=London), ...
  Local idx:  city -> [user_ids in this partition]
```

- **Pros:**
  - Simple. Writes only touch one partition (the document's home).
  - Local operations are fast.
- **Cons:**
  - Queries by the secondary key must **fan out to every partition** ("scatter/gather"), then merge results.
  - Latency = max(per-partition query) + merge.
- Used by: MongoDB, Cassandra (local secondary indexes), Elasticsearch document-based mode.

## Mechanism — Strategy 2: partitioning by term (global / inverted index)

The **index itself is partitioned**, by the secondary attribute (the "term"). Each term is at a known partition.

```
Term-index partition 1 (cities A–M):
  London -> [user42, user1042, user...]
  Exeter -> [user99, ...]

Term-index partition 2 (cities N–Z):
  Norwich -> [...]
  ...
```

- **Pros:**
  - Reads are efficient — a query for "users in London" routes to one (or a few) partition(s) directly.
  - No fan-out.
- **Cons:**
  - **Writes are complex.** Adding a user requires writing the document to its primary-key partition *and* updating the term index on (potentially) a different partition. Needs coordination — distributed transactions or asynchronous index updates (which lag).
- Used by: Elasticsearch (default), some Cassandra setups.

## Summary table (s. 16)

| Strategy | Partition basis | Read latency | Write complexity | Used by |
|---|---|---|---|---|
| **By document** | Primary key | Slow on secondary (fan-out) | Simple | MongoDB |
| **By term** | Secondary key (term) | Fast on secondary | Complex (multi-partition write coordination) | Cassandra, Elasticsearch |

## Examples in the syllabus

- s. 13–16 of the part-2 deck cover both strategies.
- The summary table on s. 16 is high-yield exam material.

## Common exam framing

- "Explain the difference between partitioning a secondary index by document versus by term."
- "Which approach favours read performance, and which favours write simplicity?"
- "Why are writes harder under a global term-partitioned index?"

## See also

- [[partitioning]]
- [[hash-partitioning]]
- [[key-range-partitioning]]
