---
title: "Key-range partitioning"
type: concept
sources: [distributed-architectures-partitioning, distributed-architectures-part-2]
related: [partitioning, hash-partitioning, sstables]
updated: 2026-05-02
---

# Key-range partitioning

*Each partition holds a continuous range of keys, sorted. Like volumes of an encyclopaedia. Great for range queries, prone to write hotspots.*

## Definition

In **key-range partitioning**, each partition is assigned a contiguous range of the keyspace. The ranges are not necessarily evenly spaced — they're sized to balance data volume.

Used by: HBase, Bigtable, MongoDB (range-sharded mode).

## Mechanism

```
Partition 1:  [a..g)
Partition 2:  [g..p)
Partition 3:  [p..z]
```

To find a record, look up which range its key falls into → route to that partition. Inside a partition, keys are sorted.

## Trade-offs

**Advantages**
- **Range queries are efficient** — adjacent keys live on the same partition; you can scan in order.
- Sorted access lets you stream results.

**Disadvantages**
- **Write hotspots** when keys arrive in order. If your key is a timestamp, every new record goes to the partition responsible for "now" — that partition's leader bears all the write load while the others sit idle.
- Partition boundaries must be chosen carefully and may need to shift over time (dynamic partitioning).

## Mitigations for the timestamp hotspot

- **Compound key** — prefix the timestamp with something more uniform (sensor ID, region) so writes spread across partitions.
- **Hash-of-timestamp** — gives up range-query benefits.

## Examples in the syllabus

- s. 9 of the lecture is the canonical description; the timestamp hotspot is called out explicitly.
- HBase regions and Bigtable tablets are real implementations.

## Common exam framing

- "What is key-range partitioning? Give one advantage and one disadvantage."
- "Why do timestamps cause write hotspots in key-range partitioning?"
- "Suggest a mitigation."

## See also

- [[partitioning]]
- [[hash-partitioning]]
