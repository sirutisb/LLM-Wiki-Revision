---
title: "Two-phase commit (2PC)"
type: concept
sources: [consistency]
related: [consensus, acid-properties, replication]
updated: 2026-05-02
---

# Two-phase commit (2PC)

*The textbook protocol for atomic commit across multiple nodes. A coordinator drives a "prepare/commit" handshake. Achieves atomicity but blocks if the coordinator fails after the prepare phase.*

## Definition

**Two-phase commit (2PC)** is a distributed algorithm for achieving **atomic transaction commit** across multiple participants. It introduces a special node called the **coordinator** (or **transaction manager**) that drives the protocol.

## Mechanism

```
Phase 1 — Prepare:
  Coordinator: "Can you commit transaction T?"  -->  to all participants
  Each participant:
    - lock the records, write the changes to its WAL
    - reply "yes" (ready to commit) or "no" (will abort)

Phase 2 — Commit / Abort:
  If all participants said "yes":
    Coordinator: "Commit T."  -->  to all participants
    Each participant: apply the changes, release locks, reply "ack"
  If any participant said "no":
    Coordinator: "Abort T."   -->  to all participants
    Each participant: roll back, release locks, reply "ack"
```

Once a participant has voted "yes" in phase 1, it **must** be able to commit when phase 2 arrives — even if it crashes and reboots between the two phases. This is enforced via the WAL.

## Why it matters

2PC is the standard answer to "how do you make a multi-node transaction atomic?" It's used by XA-compliant transaction managers, classic distributed RDBMS, and some NoSQL databases.

## Trade-offs

- **+** Achieves atomic commit across nodes.
- **+** Conceptually simple compared to Paxos/Raft.
- **− Blocks if the coordinator crashes** after participants have voted yes but before the commit decision arrives. Participants are stuck holding locks, waiting for someone to tell them what to do. (This is called the **blocking problem** of 2PC.)
- **−** Slow — two round trips for every transaction.
- **−** Requires every participant to be available during the protocol (sacrifices availability).

## Mechanism — the blocking problem in detail

After phase 1, a participant that voted "yes" is in a **prepared** state. It cannot decide unilaterally:
- **Cannot commit** — others may have voted no.
- **Cannot abort** — others may have voted yes; aborting would break atomicity.

If the coordinator dies before sending the phase-2 message, the prepared participants are stuck. Recovery requires either the coordinator to come back, or a complex protocol like 3PC (rarely used because it has its own problems).

## Examples in the syllabus

- s. 20 of the Consistency lecture is the canonical description.
- Used to extend [[acid-properties|ACID atomicity]] across multiple nodes — fits naturally with [[consensus]] discussion.

## Common exam framing

- "Describe the two phases of 2PC. What problem does each solve?"
- "What happens if the coordinator crashes between phase 1 and phase 2?"
- "Why does 2PC sacrifice availability?"

## See also

- [[consensus]]
- [[acid-properties]]
- [[cap-theorem]]
