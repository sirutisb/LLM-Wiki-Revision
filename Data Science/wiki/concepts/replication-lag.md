---
title: "Replication lag"
type: concept
sources: [replication]
related: [replication, eventual-consistency, leader-follower-replication, synchronous-vs-asynchronous-replication]
updated: 2026-05-02
---

# Replication lag

*The interval during which a follower is behind the leader. Small in healthy clusters, larger under load or partitions — and the source of most user-visible inconsistency bugs.*

## Definition

**Replication lag** is the time delay between a write committing on the leader and its application on a particular follower. It's effectively zero in synchronous replication and unbounded in (failed-) asynchronous replication.

## Why it matters

Lag is invisible most of the time, but two characteristic anomalies can hit users:

- **Reading your own writes too soon** — you write, then read from a stale follower → "the data isn't there" bug.
- **Reading backwards in time** — successive reads from different followers give increasingly old data → confusing UX, broken counters.

These motivate the two named consistency guarantees added in the lecture.

## Mechanism — read-your-writes (RYW) consistency (s. 16)

> A user always sees any updates they submitted themselves.

Implementations:
- Route reads-after-writes to the leader for a short window.
- Track a *write timestamp* per user; require the read replica's log position to be ≥ that timestamp.
- After a write, set a client-side cookie marking which replica is "fresh enough."

## Mechanism — monotonic reads (s. 17)

> Successive reads by the same user never see things moving backward in time.

Implementation:
- **Sticky sessions** — make each user always read from the *same* replica. As long as their replica only moves forward (which it does), they never go backwards.

## Trade-offs

- **+** Per-user guarantees can be cheap (sticky sessions, leader-routing for short windows) without forcing global linearizability.
- **−** Implementing them correctly across services is fiddly.
- **−** They're per-user — you don't get cross-user freshness for free.

## Examples in the syllabus

- s. 15 — the basic problem ("read from an asynchronous follower, see outdated info").
- s. 16 — the lost-data problem and read-your-writes.
- s. 17 — backwards-in-time reads and monotonic reads.

## Common exam framing

- "What is replication lag and how does it arise?"
- "Explain read-your-writes consistency. Give two implementation strategies."
- "What is monotonic-reads consistency? Suggest a simple way to enforce it."

## See also

- [[replication]]
- [[eventual-consistency]]
- [[synchronous-vs-asynchronous-replication]]
