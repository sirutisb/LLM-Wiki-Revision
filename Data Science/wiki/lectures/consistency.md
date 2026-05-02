---
title: "Lecture: Consistency and Consensus"
type: lecture
sources: [consistency]
related: [cap-theorem, acid-properties, eventual-consistency, linearizability, consensus, two-phase-commit]
updated: 2026-05-02
---

# Lecture: Consistency and Consensus

*The exam-critical lecture. Covers the CAP theorem, ACID transactions, eventual consistency, linearizability, and the consensus problem (with two-phase commit).*

## Slide-by-slide notes

- **(s. 2)** In distributed systems, things go wrong constantly — and you can't accept "let it fail." Building reliable systems out of unreliable parts requires algorithms, abstractions, and protocols (e.g. transactions).
- **(s. 3)** [[cap-theorem|CAP theorem]] — "distributed systems? choose two":
  - **C**onsistency: every read receives the most recent write or an error.
  - **A**vailability: every request receives a (non-error) response.
  - **P**artition tolerance: the system continues to operate even if parts of the network become disconnected.
- **(s. 4)** **More precisely**: in the presence of a network partition (which you can't avoid), you must choose between **availability** and **consistency**. CAP isn't really "pick two from three" — partition tolerance is mandatory; CP and AP are the two real choices.
- **(s. 5)** [[acid-properties|ACID properties]] — the relational-database transaction guarantees:
  - **A**tomicity: each transaction is treated as a single unit (all-or-nothing).
  - **C**onsistency (different "C" from CAP): only valid state transitions; constraints preserved.
  - **I**solation: concurrent transactions don't interfere.
  - **D**urability: committed changes survive system failures.
- **(s. 7)** [[eventual-consistency]] — at any moment some nodes have an outdated version of the data. Writes propagate at different speeds. **Most replicated systems guarantee only that all nodes will eventually converge** — read requests will eventually return the same value.
- **(s. 8)** Eventual consistency = **convergence**. *How long?* Unbounded in general — until then reads can return anything. Transient inconsistencies are hard to detect because they typically appear only under faults or high concurrency.
- **(s. 10)** [[linearizability]] motivation — eventual consistency may give different answers to the same question. Ideally a distributed DB **looks like** there's only one copy of the data, and that copy is the most current.
- **(s. 11)** Linearizability formal: every operation appears **atomic**, as if there's a single copy. As soon as a client completes a write, **all** clients must see the new value.
- **(s. 12–14)** Worked example with a register and reads/writes:
  - `read(x) ⇒ v` — client reads register `x`, DB returns value `v`.
  - `write(x, v) ⇒ r` — client writes value `v`; DB returns `ok` or `error`.
  - Reads that don't overlap with the write must show the pre- or post-write value as expected.
  - Reads that **overlap** with the write may return either the old or new value.
  - **Additional constraint** for linearizability: **once any client has read the new value, every subsequent client must too.** No going backwards.
- **(s. 15)** When linearizability is essential:
  - **Single-leader replication** — must agree there's one leader.
  - **Uniqueness constraints** — no two records with the same unique ID; no two passengers booking the same seat.
- **(s. 16)** Linearizability and CAP:
  - If you require linearizability, **disconnected replicas can't serve requests** — you sacrifice availability.
  - Linearizability has performance costs.
  - Many distributed DBs **don't guarantee** linearizability — they trade it for performance.
- **(s. 17)** **Linearizability and network delays** — response time of linearizable reads/writes is **at least proportional to network-delay uncertainty**. In a high-variance network, linearizable response times are inevitably high.
- **(s. 18)** [[consensus]] — getting several nodes to agree on something. Two canonical applications:
  - **Leader election** — who is the new leader after the old one fails?
  - **Atomic commit** — when a transaction touches multiple nodes, all of them must agree to commit (or all to abort).
- **(s. 19)** **Why consensus is hard** — for a multi-node transaction:
  - Commits could succeed on some, fail on others.
  - Some nodes may detect a constraint violation or conflict.
  - Some commit messages might be lost.
  - Some nodes may crash mid-transaction.
- **(s. 20)** [[two-phase-commit|Two-phase commit (2PC)]]:
  - A **coordinator** (or transaction manager) drives the protocol.
  - **Phase 1 (prepare):** coordinator asks each participant "can you commit?" Each replies yes/no.
  - **Phase 2 (commit/abort):** if all said yes, send commit; if any said no, send abort.
  - Achieves atomic commit across nodes — but blocks if the coordinator fails after prepare.

## Key takeaways

1. **CAP is not "pick 2 of 3."** You must have partition tolerance; the real choice is between consistency and availability when partitions happen.
2. **ACID's "C" ≠ CAP's "C."** ACID consistency is "preserves constraints"; CAP consistency is "every read sees the most recent write." Don't conflate them.
3. **Eventual consistency** is the default of most NoSQL/replicated systems. It's a *convergence* guarantee, not a *recency* guarantee.
4. **Linearizability** is the strongest single-object consistency model — "looks like one copy, all operations atomic." Critical for uniqueness, leader election; expensive on availability and latency.
5. **Consensus** generalises linearizability to multi-decision agreement. 2PC is the textbook protocol; it works but blocks under coordinator failure.
6. **Trade-offs you can't escape:** stronger consistency ⇒ worse availability ⇒ worse latency under variable networks.

## Concepts introduced

- [[cap-theorem]]
- [[acid-properties]]
- [[eventual-consistency]]
- [[linearizability]]
- [[consensus]]
- [[two-phase-commit]]

## Open questions / things to clarify

- The lecture covers 2PC but not Paxos / Raft. The slides imply 2PC is the level expected — confirm this is sufficient for the exam.
- Whether ACID's "C" overlap with CAP's "C" needs to be stated in answers — the conflation is a common stumbling block.

## See also

- [[cap-theorem]]
- [[acid-properties]]
- [[eventual-consistency]]
- [[linearizability]]
- [[consensus]]
- [[replication]]
