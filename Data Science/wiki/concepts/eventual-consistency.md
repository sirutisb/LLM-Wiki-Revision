---
title: "Eventual consistency"
type: concept
sources: [consistency, review]
related: [cap-theorem, linearizability, replication, replication-lag]
updated: 2026-05-02
---

# Eventual consistency

*The weakest useful consistency guarantee: if no new writes are made, all replicas will eventually return the same value. Says nothing about how long "eventually" is.*

## Definition

A system is **eventually consistent** if, in the absence of new writes, all replicas will converge to the same state — and reads will eventually return the latest value. The word "eventually" is doing a lot of work: there's no upper bound on how long convergence takes.

## Why it matters

Most replicated NoSQL systems (Cassandra, DynamoDB, Riak, Couchbase, S3) are eventually consistent by default. It's the price they pay for [[cap-theorem|availability under partition]] and high write throughput. Knowing what guarantees you *don't* get is essential.

## Mechanism

- Writes hit different nodes at different times.
- Each node serves reads from its local state.
- Background reconciliation (read-repair, anti-entropy gossip, hinted handoff) propagates changes.
- Eventually, all live replicas converge to the same state.

## What can go wrong (mid-convergence)

- **Stale reads.** A user writes, then immediately reads from another replica that hasn't received the write.
- **Backwards-in-time reads** ([[replication-lag|monotonic-reads violation]]). Read replica A (newer), then B (older) — looks like time went backwards.
- **Conflicting concurrent writes.** Two writes to the same key from different clients hit different leaders. Resolution: last-write-wins (loses data), vector clocks, CRDTs, application merge.

## Stronger guarantees built on top

Even within an eventually consistent system, useful intermediates exist:

- **Read-your-writes (RYW)** — a user always sees their own writes, even if other users see staler state.
- **Monotonic reads** — successive reads from the same user never go backwards in time.
- **Causal consistency** — operations causally related preserve their order across all replicas.

## Trade-offs

- **+** High availability — no replica needs to wait for any other.
- **+** Excellent write throughput — writes are local.
- **+** Survives partitions gracefully (continues serving both sides).
- **−** No bound on staleness.
- **−** Bugs only show up under load and faults — hard to test, hard to debug.
- **−** Requires application logic for read-your-writes-style guarantees.

## Examples in the syllabus

- Most NoSQL DBs default to eventual consistency (Consistency lecture s. 7).
- DNS is the textbook example outside this module — updates take minutes to hours to propagate globally.

## Common exam framing

- "Define eventual consistency. What does 'eventual' guarantee, and what doesn't it guarantee?"
- "Explain why eventual consistency is preferable to strong consistency in many web-scale systems."
- "Give two anomalies a user might observe under eventual consistency and how each can be mitigated."

## See also

- [[cap-theorem]]
- [[linearizability]]
- [[replication]]
- [[replication-lag]]
