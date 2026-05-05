---
title: "Twitter fan-out case study"
type: concept
sources: [data-intensive-applications]
related: [scalability, caching]
updated: 2026-05-02
---

# Twitter fan-out case study

*The textbook illustration of why "scalability" is meaningless without a load parameter — and why writing more is sometimes the right way to read fewer times.*

## Definition

The case study (Kleppmann, *Designing Data-Intensive Applications*) examines how Twitter served two operations in November 2012:

| Operation | Average load | Peak |
|---|---|---|
| Post tweet | 4.6k req/s | >12k req/s |
| Home timeline | 300k req/s | — |

The **read/write ratio is roughly 100:1.** That ratio drives the architecture.

## Why it matters

Twitter's "scaling problem" wasn't tweets-per-second — it was the **fan-out** (each user follows many, is followed by many). The right architecture for the absolute traffic numbers is wrong if you don't model fan-out separately.

## Mechanism — approach 1 (read-time merge)

- **Post:** simply insert into a global tweets table.
- **Read home timeline:** look up the people the user follows, find each of their recent tweets, merge sorted by time.
- **Cost:** every timeline read is a fan-in query across all followed users. With 300k req/s and many followed users per request, this is brutal.

## Mechanism — approach 2 (write-time fan-out)

- **Post:** look up everyone who follows this user, push the new tweet into each of their per-user timeline caches (mailbox model).
- **Read home timeline:** read the user's timeline cache. O(1).
- **Cost:** posts become expensive. Average user has ~75 followers, so 4.6k tweets/s × 75 = **345k cache writes/s** — comparable to the read load, but writes are cheaper than fan-in reads.

Twitter switched from approach 1 to approach 2 once their reads couldn't keep up.

## Mechanism — hybrid

Celebrity users (millions of followers) make approach 2 catastrophic — one tweet triggers millions of cache writes. So: **approach 2 for normal users, approach 1 for celebrities.** The reader merges their cached timeline with on-demand reads of the few celebrity authors they follow.

## Trade-offs

| Dimension                  | Approach 1          | Approach 2                    |
| -------------------------- | ------------------- | ----------------------------- |
| Read latency               | High (fan-in merge) | Low (cache read)              |
| Write cost                 | Cheap (one insert)  | Expensive (fan-out write)     |
| Storage                    | Low                 | High (one entry per follower) |
| Fits high read/write ratio | Bad                 | Good                          |
| Handles celebrities        | OK                  | Bad                           |

## Common exam framing

- "Twitter switched from a read-time merge to a write-time fan-out. Explain the trade-off in terms of load parameters."
- "Why might a hybrid approach be necessary, and what does this tell us about defining 'scalability'?"
- "Estimate the write throughput for write-time fan-out given 4.6k tweets/sec and 75 followers/user." → 345k writes/sec.

## See also

- [[scalability]]
- [[vertical-vs-horizontal-scaling]]
- [[caching]]
