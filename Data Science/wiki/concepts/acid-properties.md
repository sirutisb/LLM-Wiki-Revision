---
title: "ACID properties"
type: concept
sources: [consistency, review]
related: [cap-theorem, two-phase-commit, eventual-consistency, relational-model]
updated: 2026-05-02
---

# ACID properties

*The classical guarantees of a relational-database transaction: Atomicity, Consistency, Isolation, Durability. The benchmark against which weaker NoSQL guarantees are measured.*

## Definition

ACID is a four-property guarantee for **transactions**:

- **A — Atomicity.** Each transaction is a single, indivisible unit. Either all of its statements take effect or none do (no partial commit on failure).
- **C — Consistency.** A transaction takes the database from one *valid state* to another, preserving all declared invariants (foreign keys, NOT NULLs, application-level rules).
- **I — Isolation.** Concurrent transactions don't interfere — the result is as if they ran one after the other (in some serial order).
- **D — Durability.** Once a transaction commits, its effects survive crashes, power loss, etc.

## Why it matters

ACID is the "high-water mark" of transactional guarantees. Most NoSQL systems trade some of it for [[scalability]] and [[cap-theorem|availability under partition]]. The grade-A exam answer always names what was sacrificed and what was gained.

## Mechanism — Atomicity

Implemented via **write-ahead logs** (single node) or **[[two-phase-commit|2PC]]** (multiple nodes). On a crash, the log lets the DB roll back partially-applied transactions.

## Mechanism — Consistency (the ACID kind)

**Beware:** ACID's C is *not* CAP's C.

- **ACID C:** application invariants hold. The DB rejects writes that would violate constraints.
- **CAP C:** every read sees the most recent write across all replicas.

ACID C is enforced jointly by the application (declares constraints) and the DB (refuses bad data).

## Mechanism — Isolation

Several levels, in order of strength:
- **Read committed** — no dirty reads.
- **Repeatable read** — no non-repeatable reads.
- **Serializable** — equivalent to *some* serial order. Strongest.

Implementations: locking (pessimistic), MVCC (optimistic, used by PostgreSQL, MySQL InnoDB).

## Mechanism — Durability

Implemented by:
- **fsync** before acknowledging a commit (single node).
- **Replication** (durability via redundancy — but adds latency).
- **Write-ahead logs** that survive a crash and are replayed on recovery.

## Why distributed systems struggle with ACID

- **Atomicity** across nodes requires consensus / 2PC (slow, blocks on coordinator failure).
- **Isolation** across replicas requires global coordination.
- **Durability** is easy if you accept replication lag; if you require it before acknowledgement, latency spikes.

→ This is exactly the trade-off in [[cap-theorem|CAP]] and [[eventual-consistency]].

## Examples in the syllabus

- Slide 5 of the Consistency lecture lists all four.
- 2PC (s. 20) is the protocol that extends Atomicity across multiple nodes.

## Common exam framing

- "List and define the four ACID properties."
- "Why is the 'C' in ACID often confused with the 'C' in CAP? Distinguish them."
- "Why are full ACID guarantees expensive in a distributed system? Use isolation as your example."

## See also

- [[cap-theorem]]
- [[two-phase-commit]]
- [[eventual-consistency]]
- [[linearizability]]
