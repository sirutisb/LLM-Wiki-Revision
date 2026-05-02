---
title: "Lecture: Distributed Architectures — Replication"
type: lecture
sources: [replication]
related: [replication, leader-follower-replication, synchronous-vs-asynchronous-replication, replication-lag, vertical-vs-horizontal-scaling]
updated: 2026-05-02
---

# Lecture: Distributed Architectures — Replication

*Keeping a copy of the data on every node — the "how" of horizontal scaling for reads, geographic latency, and availability.*

## Slide-by-slide notes

- **(s. 3)** Until now we've abstracted *where* things were stored. From here on: distributed data systems — multiple machines / storage devices.
- **(s. 4–5)** Distributed systems range from two boxes on one PSU to global CDNs. **Netflix CDN: 8,492 servers across 578 locations (2018).**
- **(s. 6)** [[vertical-vs-horizontal-scaling]] recap.
- **(s. 7)** Two ways to distribute data:
  - **[[replication]]** — every node keeps a *copy*.
  - **[[partitioning]]** — every node keeps a *subset*.
  - Often combined: each partition is replicated.
- **(s. 9)** Why replicate?
  - **Reduce latency** — keep data geographically close to users.
  - **Increase availability** — system survives if some replicas fail.
  - **Increase read performance** — more machines to serve reads.
  - *Constraint:* the data has to fit on a single machine; if not, you also need [[partitioning]].
  - *Cost:* writes touch *all* copies.
- **(s. 10)** [[leader-follower-replication]]:
  - One replica is the **leader**; writes go only to the leader.
  - The leader sends the change to **followers** as a **replication log**; followers apply it in order.
  - Reads can go to any replica.
  - Built into PostgreSQL, MongoDB, MySQL.
- **(s. 11)** [[synchronous-vs-asynchronous-replication|Synchronous replication]] — the leader waits for the followers to confirm before reporting success.
  - All-synchronous is brittle: any slow follower stalls writes.
  - **Semi-synchronous** — at least one follower must be synchronous. If it goes down, an asynchronous follower is promoted to synchronous.
- **(s. 12–13)** **Adding new followers** — naive copy-while-running doesn't work because the data changes during the copy. Procedure:
  1. Take a snapshot of the leader at a point in time.
  2. Copy the snapshot to the new follower.
  3. New follower requests changes since the snapshot's position in the replication log.
  4. After processing the backlog, the follower has **caught up**.
- **(s. 14)** **Recovering from failures:**
  - **Follower failure** — recovers from its log: knows the last processed transaction, requests changes from leader.
  - **Leader failure (failover)** — promote a follower (often the most up-to-date one). Many things go wrong:
    - **Split brain** — two leaders simultaneously.
    - Data loss if the old leader had unreplicated writes.
    - Promoting the wrong replica.
- **(s. 15)** [[replication-lag]] — read-only queries can hit any replica, but asynchronous followers may be stale.
- **(s. 16)** **Read-your-writes consistency** — a user must see their own writes immediately. Strategy: route reads-after-writes to the leader (or to the user's own writes destination) for a short window.
- **(s. 17)** **Monotonic reads** — successive reads from the *same user* shouldn't go backwards in time. Strategy: **route the same user to the same replica** consistently (sticky sessions).

## Key takeaways

1. **Replication = horizontal scaling for reads + availability + locality.** It does *not* solve the dataset-too-big-for-one-machine problem — that's [[partitioning]].
2. **Leader-follower is the dominant pattern.** Multi-leader and leaderless are alternatives but less common in this module.
3. **Synchronous = strong consistency, fragile; asynchronous = weak consistency, robust.** Semi-synchronous is the practical middle.
4. **Failover is hard.** Split brain, lost writes, promoting the wrong replica — needs [[consensus]] to do correctly.
5. **Replication lag manifests as user-visible bugs.** Read-your-writes and monotonic reads are the two named guarantees that rescue UX.

## Concepts introduced

- [[replication]]
- [[leader-follower-replication]]
- [[synchronous-vs-asynchronous-replication]]
- [[replication-lag]]

## Open questions / things to clarify

- Multi-leader and leaderless replication aren't covered — the deck stops at single-leader. Worth checking whether they appear elsewhere or in workshops.

## See also

- [[partitioning]]
- [[consensus]]
- [[cap-theorem]]
- [[eventual-consistency]]
