---
title: "Linearizability"
type: concept
sources: [consistency]
related: [eventual-consistency, cap-theorem, consensus, replication]
updated: 2026-05-02
---

# Linearizability

*The strongest single-object consistency model. The system behaves as if there is one copy of the data and every operation is atomic. Once a client has read a new value, all subsequent reads must see it too.*

## Definition

A storage system is **linearizable** (also: **strong consistency**, **atomic consistency**) if:

1. The system *appears* to clients as if there is **one single copy** of the data.
2. Every operation is **atomic** — it takes effect at some single moment between its invocation and response.
3. Once any client has observed a new value, **all** subsequent operations (by any client) must also see it (or a later one). No regressions.

## Why it matters

Many higher-level guarantees rely on linearizability:

- **Single-leader replication** must elect *one* leader — that decision must be linearizable.
- **Uniqueness constraints** — no two records with the same unique ID; no two passengers booking the same seat — require linearizable atomic compare-and-set.
- **Distributed locks** (DLM) — to claim a lock, you need linearizable agreement on its current state.

## Mechanism — the worked example (s. 11–14)

A register starts at 0. Client C performs `write(x, 1)`. Clients A and B issue concurrent reads.

- A `read` that completes **before** the `write` starts → returns 0.
- A `read` that starts **after** the `write` completes → returns 1.
- A `read` that **overlaps** the `write` → may return either 0 or 1.
- **Linearizability adds:** if any client read 1, every later read (by any client) must also return 1 — even if it overlaps with the original write window.

This is what distinguishes linearizability from "eventually consistent" or "atomic-per-replica" — it's about the **global, real-time** ordering across all clients.

## Mechanism — cost

Linearizability is expensive:

- **Disconnected replicas can't process requests** — they could return stale data, violating the model. So **linearizability sacrifices availability under partition** (it's a CP property).
- **Latency is proportional to network-delay uncertainty.** In a network with variable Round-Trip Times (RTTs), response times for linearizable operations are inevitably high (s. 17).
- Most distributed DBs **don't** offer linearizability by default — they trade it for performance (s. 16).

## Trade-offs vs eventual consistency

| | Linearizable | [[eventual-consistency|Eventual]] |
|---|---|---|
| Reads see most recent write | Always | Eventually |
| Latency | High | Low |
| Availability under partition | Reduced | Full |
| Suitable for | Locks, leader election, uniqueness | High-throughput user-facing reads |

## Examples in the syllabus

- Used to ensure single-leader replication has *one* leader (s. 15).
- Required for unique-ID and seat-booking constraints (s. 15).
- Spanner, ZooKeeper, etcd, FoundationDB are linearizable. Cassandra, DynamoDB, Riak are not (by default).

## Common exam framing

- "Define linearizability. How does it differ from eventual consistency?"
- "Why is linearizability incompatible with high availability under network partitions?"
- "Give two scenarios where linearizability is essential and one where it would be wastefully strict."

## See also

- [[eventual-consistency]]
- [[cap-theorem]]
- [[consensus]]
- [[replication]]
