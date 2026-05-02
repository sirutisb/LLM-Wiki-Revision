---
title: "Consensus"
type: concept
sources: [consistency]
related: [two-phase-commit, linearizability, replication, cap-theorem]
updated: 2026-05-02
---

# Consensus

*Getting several nodes to agree on a single value, despite failures. The hardest distributed problem and the foundation under leader election, atomic commit, and strongly-consistent replication.*

## Definition

The **consensus problem** asks: how do a set of nodes agree on a single value when:

- nodes can crash;
- messages can be delayed, duplicated, or lost;
- no global clock is available?

A correct consensus algorithm guarantees:
- **Agreement** — no two nodes decide differently.
- **Validity** — the decided value was proposed by some node.
- **Termination** — every non-crashed node eventually decides.

## Why it matters

Two everyday distributed-systems problems reduce to consensus:

- **Leader election.** When the current leader fails, who becomes the new one? Without agreement, you get **split brain** — two leaders, divergent state.
- **Atomic commit across multiple nodes.** A transaction touching N nodes must commit on all N or abort on all N. (Single-node atomicity is easy; multi-node isn't.)

## Mechanism — why multi-node atomic commit is hard (s. 19)

Naively sending "commit" to every node fails because:

- Some commits succeed; others detect a constraint violation and want to abort.
- Some commit messages are lost in the network.
- Some nodes crash mid-commit.
- Some replicas are temporarily disconnected.

Without a coordination protocol, the system ends up **partially committed**, breaking atomicity.

## Mechanism — protocols

The lecture covers **[[two-phase-commit|two-phase commit (2PC)]]** explicitly:

- A coordinator drives the protocol.
- *Prepare* phase: ask everyone "can you commit?"
- *Commit/abort* phase: if all said yes, commit; otherwise abort.

The slides don't cover **Paxos** or **Raft**, but they're the production-grade alternatives:
- **Paxos** (Lamport 1989/1998) — provably correct, notoriously hard to implement.
- **Raft** (Ongaro & Ousterhout 2014) — a more understandable protocol with the same guarantees; used in etcd, Consul, CockroachDB, TiKV.

## Trade-offs

- **+** Without consensus, you cannot have a single linearizable leader.
- **−** Slow — round-trip latency proportional to network delay.
- **−** Blocks under failures — 2PC blocks if the coordinator dies after prepare; Paxos/Raft need a quorum to make progress.
- **FLP impossibility result:** in a fully asynchronous network with even one crash failure, no deterministic consensus algorithm can guarantee termination. Real systems rely on partial synchrony assumptions to make progress in practice.

## Examples in the syllabus

- Leader election (s. 18) — the failover problem in single-leader [[replication]].
- Atomic commit (s. 18, 19) — the multi-node transaction problem.
- 2PC (s. 20) — the textbook implementation.

## Common exam framing

- "Why is consensus needed in a single-leader replication system?"
- "Explain the steps of two-phase commit. What happens if the coordinator crashes after prepare?"
- "Why is naive 'send commit to everyone' insufficient for atomic multi-node transactions?"

## See also

- [[two-phase-commit]]
- [[linearizability]]
- [[replication]]
- [[cap-theorem]]
