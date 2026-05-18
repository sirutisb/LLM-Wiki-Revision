---
title: "PikPok Case Study — ML Training & Systems Architecture"
type: exam
sources: [consistency, replication, partitioning, online-learning, distributed-machine-learning]
related: [cap-theorem, acid-properties, consensus, replication, partitioning, eventual-consistency, two-phase-commit, online-learning, batch-vs-online-learning, twitter-fanout-case-study]
updated: 2026-05-18
---

# PikPok Case Study — ML Training & Systems Architecture

*Worked exam case study: designing the ML training strategy and distributed systems architecture for PikPok, a short-video social media platform.*

---

## Case Study Context

You are the data science lead for **PikPok**, a short-video social media platform where users post videos, follow creators, interact via likes and comments, and receive personalised recommendations via **PikPokIT** — an ML model continuously updated from millions of daily user interactions.

---

## Part A — Training Strategy: Full Batch, Mini-Batch, Online, or Combination?

For PikPokIT's recommendation system, a **blend of mini-batch and online learning** is ideal.

- **Mini-batch learning** efficiently handles large datasets by training on smaller subsets, providing scalability. It is statistically more stable than pure online learning and maps well to distributed training via all-reduce ([[sgd-all-reduce]]).
- **Online learning** updates the model with real-time user interactions, keeping recommendations current and adapting rapidly to new trends, viral content, and shifting user preferences ([[online-learning]]).
- This combination ensures the system is both **adaptable** to new trends and **scalable** for processing vast amounts of data, optimising performance and relevance in a dynamic content environment.
- Full batch training is unsuitable here: retraining on the entire dataset every update cycle is computationally prohibitive and introduces too much latency for a live recommendation system.

See also [[batch-vs-online-learning]] for the full trade-off table.

---

## Part B — Systems Architecture: Consistency, CAP, ACID, Partitioning, Replication, Consensus

### 1. CAP Position — AP over CP

PikPok is a **globally distributed, write-heavy, read-heavy social media platform**. Applying [[cap-theorem]]: network partitions are unavoidable at scale, so the real choice is between **consistency and availability under partition**.

PikPok should be designed as an **AP system**:

- A user whose "like" count updates 2 seconds late is acceptable.
- A user who **cannot open the app** because the system refused requests during a partition is not acceptable.

This maps to systems like **Cassandra** (used by Instagram, Netflix) — AP by default, with tunable per-operation consistency levels (you can request a "strong" read for critical operations and an eventual read for feed data).

The **exception**: user authentication and account creation sit closer to CP — stale credentials are a security risk, so those subsystems should prefer consistency over pure availability.

---

### 2. ACID Properties — What You Relax and What You Keep

Full ACID is **expensive in a distributed setting** ([[acid-properties]]):

| Property | PikPok decision | Reason |
|---|---|---|
| **Atomicity** | Kept for writes that span metadata (e.g., "post video + update user stats") — via [[two-phase-commit]] across partitions | Partial posts would be corrupting |
| **Consistency (ACID)** | Kept at schema level; application invariants enforced locally | Standard relational constraint enforcement |
| **Isolation** | **Relaxed** to read-committed or lower for feed/recommendation reads | Full serializability would kill throughput at scale |
| **Durability** | Kept via asynchronous replication + write-ahead logs | Cannot lose user-generated content |

In practice PikPok operates on **BASE semantics** (Basically Available, Soft state, Eventually consistent) for the bulk of its data — the recommendation feed, like counts, view counts — and reserves stronger guarantees for account-critical writes.

---

### 3. Partitioning Strategy

PikPok's dataset vastly exceeds any single machine, so [[partitioning]] is essential. Key data types and their strategies:

| Data entity | Partition key | Strategy | Rationale |
|---|---|---|---|
| User profiles | `user_id` | Hash | Uniform distribution; no range queries on users |
| Videos/metadata | `video_id` | Hash | Prevents hotspots; uploads are uniform |
| Interactions (likes, views, comments) | `user_id` | Hash | Fan-out queries are per-user |
| Feed/recommendations | `user_id` | Hash | Each user owns their feed partition |
| Model training logs | `timestamp` | Key-range | Batch jobs process time-ordered windows |

**Hotspot problem**: The celebrity/creator problem is real — if you partition interactions by `video_id`, a viral video concentrates all writes on one partition. **Mitigation**: add a random suffix to the partition key for high-traffic entities, then aggregate at read time (the same trade-off as Twitter's hybrid fan-out in [[twitter-fanout-case-study]]).

---

### 4. Replication

[[replication]] is combined orthogonally with partitioning: **each partition has its own leader with multiple followers**.

- **Architecture**: single-leader per partition (simplest conflict resolution). Writes go to the partition leader; reads can go to any follower.
- **Sync vs Async** ([[synchronous-vs-asynchronous-replication]]): **asynchronous replication** for write performance. The cost is **replication lag** ([[replication-lag]]) — a user might see a stale like count or follower count for a short window.
  - Mitigated by **read-your-writes consistency**: a user always sees their *own* actions immediately (route their reads to the leader or the replica that has their write).
- **Geographic replication**: replicate partitions across data centres. Reads served from the nearest replica; writes routed to the partition leader regardless of location.

The resulting consistency guarantee for the recommendation feed is **eventual consistency** ([[eventual-consistency]]) — fully acceptable for a video recommendation system where a 500ms stale recommendation is invisible to the user.

---

### 5. Consensus Mechanism

[[consensus]] is needed in two places:

#### a) Leader election (failover)

When a partition leader fails, the replica set must elect a new one. This is a [[consensus]] problem — without a correct agreement protocol, the system risks **split brain**: two nodes both believing they are the leader, accepting conflicting writes and diverging state. During the election window, that partition's writes are briefly unavailable — reinforcing the AP trade-off.

#### b) Cross-partition atomic commits

Some writes span partitions (e.g., "create user account" touches both the profile partition and the auth partition). These require **[[two-phase-commit]] (2PC)**:

1. *Prepare phase*: coordinator asks all involved partition leaders "can you commit?"
2. *Commit phase*: if all yes → commit on all; otherwise → abort on all.

2PC is slow and **blocks if the coordinator crashes after prepare** — so PikPok minimises cross-partition transactions by design, accepting eventual consistency everywhere it can.

---

### Summary — How It All Connects

```
PikPok AP (availability > strict consistency)
     │
     ├── Partitioning (hash on user_id/video_id)
     │        └── Scales writes horizontally; hotspot mitigation for celebrities
     │
     ├── Replication (leader-follower, async, multi-region)
     │        └── High availability + low read latency + geographic locality
     │        └── Eventual consistency for feeds/counts; RYW for user's own actions
     │
     ├── ACID relaxed → BASE (isolation → read-committed; strong ACID only for critical writes)
     │
     └── Consensus (leader election via agreement protocol; 2PC for rare cross-partition transactions)
              └── Minimise 2PC scope → minimise blocking
```

The key design principle: **choose eventual consistency by default, reserve strong consistency and consensus for the few places where correctness is non-negotiable** (auth, payment/ads, atomic multi-entity creates).

---

## See also

- [[cap-theorem]]
- [[acid-properties]]
- [[consensus]]
- [[two-phase-commit]]
- [[replication]]
- [[partitioning]]
- [[eventual-consistency]]
- [[online-learning]]
- [[batch-vs-online-learning]]
- [[twitter-fanout-case-study]]
