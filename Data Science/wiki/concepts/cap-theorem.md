---
title: "CAP theorem"
type: concept
sources: [consistency, review]
related: [acid-properties, eventual-consistency, linearizability, replication]
updated: 2026-05-02
---

# CAP theorem

*In a distributed system experiencing a network partition, you must choose between consistency and availability — you cannot have both. Partition tolerance is not optional.*

## Definition

The **CAP theorem** (Brewer 2000, formalised by Gilbert & Lynch 2002) states that any networked shared-data system can provide at most two of these three:

- **C**onsistency — every read receives the most recent write or an error. (≈ [[linearizability]].)
- **A**vailability — every request receives a non-error response.
- **P**artition tolerance — the system continues to operate despite arbitrary network partitions (some messages between nodes are dropped).

## The "more precise" framing (s. 4)

The "pick 2 of 3" version is misleading. Real networks **do** partition; you don't get to opt out of P. The real statement is:

> **In the presence of a network partition, you must choose between consistency and availability.**

So distributed systems are classified as:

- **CP** — consistent + partition-tolerant. Refuses requests during a partition (sacrifices A). Examples: HBase, MongoDB (default), Spanner.
- **AP** — available + partition-tolerant. Returns possibly-stale data during a partition (sacrifices C). Examples: Cassandra, DynamoDB, Riak.
- **CA** is a fiction — it would mean "no partitions ever," which only holds inside a single machine.

## Why it matters

CAP is the single most important framing for distributed-system design. Every storage system in the module sits on one side or the other. It also shapes which application-level guarantees you can rely on.

## Mechanism — the trade-off in practice

When a partition cuts a cluster in two:

- **CP system**: at least one side refuses to write (or reads return errors) until the partition heals — preserving consistency at the cost of availability.
- **AP system**: both sides accept reads and writes, diverging in state. After the partition heals, [[eventual-consistency]] mechanisms reconcile the divergence (last-write-wins, vector clocks, application-level merge).

## Subtleties

- **Latency-vs-consistency** — even without a full partition, slow networks impose a cost. **PACELC** extends CAP: "if Partition then A or C; *Else* L or C" (latency vs consistency).
- **Per-operation choice** — many systems (Cassandra, DynamoDB) let the application choose consistency level *per query*: strong reads pay latency; eventual reads don't.

## ACID's C vs CAP's C — easily confused

| | ACID's "C" (Consistency) | CAP's "C" (Consistency) |
|---|---|---|
| Meaning | Transaction preserves all defined invariants | Every read returns the most recent write |
| Concern of | The application/schema | The replication system |

## Examples in the syllabus

- s. 3–4 of the Consistency lecture state both forms.
- [[replication]] systems all face this choice; single-leader replication tries to be CP but introduces availability problems on leader failure.

## Common exam framing

- "State the CAP theorem. Why is the 'pick two of three' formulation misleading?"
- "Classify each of MongoDB, Cassandra, and a single-node PostgreSQL on CAP."
- "Why is CA a non-option in real distributed systems?"
- "Distinguish ACID's C from CAP's C."

## See also

- [[acid-properties]]
- [[eventual-consistency]]
- [[linearizability]]
- [[replication]]
