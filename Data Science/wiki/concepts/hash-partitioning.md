---
title: "Hash partitioning"
type: concept
sources: [distributed-architectures-partitioning, distributed-architectures-part-2]
related: [partitioning, key-range-partitioning, hash-index]
updated: 2026-05-02
---

# Hash partitioning

*Apply a hash function to the key, partition by the resulting hash range. Excellent load distribution, terrible at range queries.*

## Definition

In **hash partitioning**, you compute `hash(key)` and assign the record to a partition based on the hash value. Each partition is responsible for a range of *hashes*, not a range of *keys*.

Used by: Cassandra, DynamoDB, Riak, MongoDB (hash-sharded mode).

## Mechanism

```
hash(user42)   = 0xa3f1c8...   -> Partition 2
hash(user43)   = 0x14d089...   -> Partition 1   (very different bucket)
hash(user44)   = 0xf21044...   -> Partition 3
```

Crucially, **adjacent keys produce non-adjacent hashes** — `user42` and `user43` end up on different partitions.

## Trade-offs

**Advantages**
- **Distributes keys fairly** even under skewed access patterns. The pathological "all writes have key = today" no longer hotspots.
- Robust against adversarial keys.

**Disadvantages**
- **Range queries become expensive.** Keys that were adjacent (`kitty1000` to `kitty2000`) are scattered across all partitions. Either:
  - **MongoDB's solution:** send the range query to **all partitions** (scatter/gather).
  - **Cassandra's solution:** **compound primary key** — hash on the first component, but sort within the partition by the second. So `(user_id, timestamp)` hashes by user, lets you range-scan a user's timeline efficiently.

## Mechanism — consistent hashing

In production hash-partitioning systems, naive `hash(key) mod N` is bad: changing N (adding/removing nodes) reshuffles almost everything. **Consistent hashing** assigns each node a position on a hash ring; each key maps to the next node clockwise. Adding or removing a node only moves keys assigned to that node — minimal rebalancing.

Not named explicitly in the slides, but underlies real systems (Cassandra, DynamoDB).

## Examples in the syllabus

- s. 10–12 of the lecture.
- DynamoDB partition keys are pure hash partitioning.
- Cassandra's compound-key trick (s. 12) is the common workaround for range-on-hash.

## Common exam framing

- "Why does hash partitioning balance load better than key-range partitioning?"
- "What does hash partitioning sacrifice, and how do real systems work around it?"
- "Briefly explain Cassandra's compound-key approach."

## See also

- [[partitioning]]
- [[key-range-partitioning]]
- [[hash-index]]
