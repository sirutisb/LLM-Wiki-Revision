---
title: "Synchronous vs asynchronous replication"
type: concept
sources: [replication]
related: [replication, leader-follower-replication, replication-lag, eventual-consistency]
updated: 2026-05-02
---

# Synchronous vs asynchronous replication

*The dial that trades latency for durability. Synchronous waits for follower acknowledgement; asynchronous doesn't. Real systems sit somewhere in between.*

## Definition

When a leader receives a write, it must propagate it to followers. Two ways to do that:

- **Synchronous** — the leader waits for at least one (or more, or all) followers to confirm receipt before reporting success to the client.
- **Asynchronous** — the leader applies the write locally, returns success to the client immediately, and propagates to followers in the background.

## Why it matters

This single choice drives the consistency / availability / latency triple. Strong durability guarantees on individual writes vs high write throughput — pick one.

## Mechanism — fully synchronous

- Every follower must ack before commit succeeds.
- **Pro:** all replicas are guaranteed to see the write before any client.
- **Con:** any slow / failed follower stalls *every* write — system availability collapses.

In practice, **fully synchronous is rarely used.** It's too brittle.

## Mechanism — fully asynchronous

- Leader commits locally, returns to client, then pushes to followers.
- **Pro:** lowest write latency; system tolerates slow / failed followers.
- **Con:** **on leader failure, recent writes can be lost** — they hadn't been replicated yet.

This is the default in most production single-leader systems.

## Mechanism — semi-synchronous

The lecture's recommended middle ground (s. 11):

- **At least one follower must be synchronous.** Writes need its ack.
- The other followers replicate asynchronously.
- If the synchronous follower goes offline or slow, an asynchronous follower is **promoted to synchronous** in its place.

This bounds the worst-case data loss to "what one synchronous follower had" while keeping latency acceptable.

## Trade-offs summary

| | Sync | Semi-sync | Async |
|---|---|---|---|
| Write latency | High | Medium | Low |
| Tolerates slow follower | No | Yes (after promote) | Yes |
| Risk of write loss on failover | None | Bounded | Possible |
| Throughput | Low | Medium | High |

## Examples in the syllabus

- s. 11 of the Replication lecture covers all three.
- MySQL semi-sync replication is the textbook real implementation.

## Common exam framing

- "Compare synchronous, semi-synchronous, and asynchronous replication on latency, throughput, and risk of write loss."
- "Why is fully synchronous replication rarely used in practice?"
- "Under asynchronous replication, what happens to writes that were committed by the leader but not yet propagated when the leader fails?"

## See also

- [[replication]]
- [[leader-follower-replication]]
- [[replication-lag]]
