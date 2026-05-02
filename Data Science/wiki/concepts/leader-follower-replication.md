---
title: "Leader-follower replication"
type: concept
sources: [replication]
related: [replication, synchronous-vs-asynchronous-replication, replication-lag, consensus]
updated: 2026-05-02
---

# Leader-follower replication

*One replica is the leader, accepts all writes, and pushes a replication log to the followers. Reads can go anywhere; writes only to the leader.*

## Definition

In **leader-follower** (also called **primary-secondary** or **master-slave**) replication:

1. One replica is designated the **leader** (or primary, master).
2. Clients send all **writes** to the leader, which writes to its local storage.
3. The leader sends each write as part of a **replication log** (or change stream) to every **follower** (or secondary, replica).
4. Each follower applies the changes **in the same order** as the leader.
5. **Reads** can go to the leader or any follower.

Built-in to many DBMS — PostgreSQL, MongoDB, MySQL.

## Why it matters

The simplest replication architecture and by far the most common. It avoids write-conflict problems (only one writer) at the cost of leader-availability concerns.

## Mechanism — the replication log

The leader's log captures every change in order. Forms:

- **Statement-based** — log SQL statements. Fragile (non-deterministic functions, side effects).
- **Write-ahead log shipping** — log low-level page changes. Coupled to storage engine version.
- **Logical (row-based) log** — log row-level changes in a storage-engine-independent format. Most flexible.

Followers apply entries from the log in the same order, ensuring eventual replica equivalence.

## Mechanism — handling failure

- **Follower fails:** on restart, it reads the last processed log position from disk, reconnects to the leader, requests all changes since.
- **Leader fails:** **failover** — promote a follower. Steps:
  1. Detect the leader is gone (timeout, heartbeat failure).
  2. Choose a successor — typically the follower with the most up-to-date replication log position.
  3. Reconfigure the system: clients now send writes to the new leader.

Things that go wrong during failover:

- **Split brain** — old leader thinks it's still leader; two leaders accept writes; conflicts.
- **Lost writes** — writes the old leader had received but not yet replicated are gone.
- **Wrong successor** — choosing a stale follower discards writes others had.

These problems make failover **a [[consensus]] problem** — done correctly, it requires distributed agreement.

## Trade-offs

- **+** Simple model, no write conflicts.
- **+** Read scalability — many followers can serve reads.
- **−** Write throughput is bounded by the leader's capacity.
- **−** Leader is a single point of failure (until failover completes).
- **−** Asynchronous replication exposes [[replication-lag]] anomalies.

## Examples in the syllabus

- s. 10 — diagram and structure.
- PostgreSQL streaming replication, MySQL binlog replication, MongoDB replica sets — all canonical implementations.

## Common exam framing

- "Describe the leader-follower replication model."
- "What is split brain and why does it occur during leader failover?"
- "Why is failover a consensus problem?"

## See also

- [[replication]]
- [[synchronous-vs-asynchronous-replication]]
- [[replication-lag]]
- [[consensus]]
