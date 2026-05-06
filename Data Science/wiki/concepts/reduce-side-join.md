---
title: "Reduce-side join"
type: concept
sources: [batch-processing]
related: [mapreduce, batch-processing, map-side-join]
updated: 2026-05-02
---

# Reduce-side join

*The MapReduce way to join two datasets: extract the join key in two parallel mapper jobs, let the shuffle bring matching keys together at the reducer.*

## Definition

A **reduce-side join** uses the shuffle phase of [[mapreduce|MapReduce]] to bring records that share a join key together at the reducer. It is the MapReduce-native way to join two large datasets.

## Why it matters

Joins in batch are radically different from joins in OLTP databases. The naïve approach — for each row in dataset A, look up the matching row in dataset B — does random per-record lookups against an external database, killing throughput. The reduce-side join sorts the data so the join becomes local at the reducer.

## Mechanism

```
Dataset 1 — Activity events: (user_id, action)
Dataset 2 — User records:    (user_id, dob, country, ...)

Mappers (run on each dataset in parallel):
  Activity mapper:  emit (user_id, ("activity", action))
  User mapper:      emit (user_id, ("user", dob, country, ...))

Shuffle:
  Group by user_id; both datasets' records for the same user
  arrive at the same reducer.

Reducer:
  Receives all values for user_id X — both the user record
  and all activity events. Performs the join (cartesian product
  / one-to-many) and emits joined records.
```

![[reducer_side_join.png]]
## Trade-offs

- **+** Throughput-friendly — both datasets streamed through, no random reads.
- **+** Scales to datasets that don't fit in memory.
- **−** Skewed join keys (one user with millions of events) overwhelm one reducer — same hot-spot pattern as [[partitioning]].
- **−** Two full passes over the data — expensive shuffle.

## Alternatives

- [[map-side-join|Map-side join (broadcast join)]] — when one side is small enough to fit in memory, ship it to every mapper. Avoids the shuffle.
- **Bucketed sort-merge join** — pre-sort and pre-bucket both datasets so the join is just a merge.

## Examples in the syllabus

- s. 11–13 of the Batch Processing lecture: joining activity events and user records.
- The lecturer's framing: "All locality is good locality" — keep computation on one machine.

## Common exam framing

- "Describe how to implement a join between two datasets using MapReduce."
- "Why would you avoid a per-record database lookup in a batch pipeline?"
- "What is a hot-spot reducer and how can it arise in a join?"

## See also

- [[mapreduce]]
- [[batch-processing]]
- [[partitioning]]
