---
title: "Replication"
type: concept
sources: [replication, review]
related: [partitioning, leader-follower-replication, synchronous-vs-asynchronous-replication, replication-lag, cap-theorem]
updated: 2026-05-02
---

# Replication

*Keeping a copy of the same data on multiple nodes. Buys you availability, read scalability, and geographic locality — at the cost of consistency complexity.*

## Definition

**Replication** is the practice of storing the same data on multiple machines (replicas). Together with [[partitioning]] it is one of the two basic ways to distribute data.

## Why it matters

Three reasons to replicate:

1. **Latency** — put copies near users (CDNs).
2. **Availability** — survive node failures.
3. **Read scalability** — serve reads from any replica.

The constraints/costs:

- **All replicas store the full dataset.** If your data exceeds a single machine, replication alone isn't enough — you also need [[partitioning]].
- **Writes touch all copies.** Either synchronously (slower, stronger guarantees) or asynchronously (faster, weaker).
- **Replicas can disagree** during propagation → see [[replication-lag]] and [[eventual-consistency]].

## Mechanism — three architectures

| | Single-leader | Multi-leader | Leaderless |
|---|---|---|---|
| Writes go to | One leader | Multiple leaders | Any replica (with quorum) |
| Conflict resolution | None needed (one writer) | Hard | Harder |
| Reads from | Any replica | Any replica | Any replica |
| Examples | PostgreSQL, MySQL, MongoDB | Multi-region SQL | Cassandra, DynamoDB |

The lecture covers **single-leader** in detail (see [[leader-follower-replication]]). Multi-leader and leaderless are mentioned only implicitly.

## Mechanism — sync vs async

A leader propagates writes to followers either:

- **Synchronously** — wait for follower acknowledgement before returning to client (strong, brittle).
- **Asynchronously** — return immediately, propagate in the background (fast, can lose recent writes on failover).
- **Semi-synchronous** — at least one follower must ack; the rest can be async.

See [[synchronous-vs-asynchronous-replication]].

## Mechanism — adding followers (without downtime)

1. Snapshot the leader at point-in-time T.
2. Stream the snapshot to the new follower.
3. New follower requests all changes since T from the leader's replication log.
4. Once caught up, it joins the live replica set.

## Mechanism — failover

- **Follower fails:** recovers from its log; rejoins, requests missed transactions.
- **Leader fails:** elect a new leader (a [[consensus]] problem). Risks: **split brain** (two leaders), lost unreplicated writes, promoting a stale follower.

## Trade-offs

- **+** High availability, lower read latency, good for geo-distribution.
- **−** Adds [[consistency]] problems: stale reads, lost writes on failover, replication lag user-visible bugs.
- **−** Doesn't help if a single machine can't hold the dataset.

## Examples in the syllabus

- Built into PostgreSQL, MongoDB, MySQL (s. 10).
- Netflix CDN scale (s. 5) — 8,492 servers, 578 locations.

## Common exam framing

- "What are the three main reasons to replicate data?"
- "Distinguish synchronous and asynchronous replication. What does each gain and lose?"
- "What is split brain and how does it arise during leader failover?"

## See also

- [[leader-follower-replication]]
- [[synchronous-vs-asynchronous-replication]]
- [[replication-lag]]
- [[partitioning]]
- [[consensus]]
