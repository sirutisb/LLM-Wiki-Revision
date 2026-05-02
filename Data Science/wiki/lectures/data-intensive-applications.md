---
title: "Lecture: Data-Intensive Applications — Reliability, Scalability, Maintainability"
type: lecture
sources: [data-intensive-applications]
related: [reliability, scalability, maintainability, fault-vs-failure, vertical-vs-horizontal-scaling, twitter-fanout-case-study]
updated: 2026-05-02
---

# Lecture: Data-Intensive Applications — Reliability, Scalability, Maintainability

*The three properties every data-intensive application must satisfy, the building blocks they share, and the trade-offs that shape distributed-system design.*

## Slide-by-slide notes

- **(s. 3)** *Past:* single-server mainframes, static formats, expensive RDBMS (MS SQL, Oracle).
- **(s. 4)** *The Web changed everything:* dynamic content, rapid growth, and companies like Google, eBay, Facebook expose the limits of single-server thinking.
- **(s. 5)** Single-server limitations: **availability / fault tolerance**, **scalability** (synchronisation, consistency), **maintenance**.
- **(s. 6)** The two governing trade-offs: **data consistency vs service availability** (anticipates [[cap-theorem]]) and **single powerful system vs several cheap commodity computers** (anticipates [[vertical-vs-horizontal-scaling]]).
- **(s. 7)** A data-intensive application is built from four functional blocks: **database** (store), **caching** (recompute-avoidance), **indexing** (efficient search), **batch processing** (periodic large-scale jobs).
- **(s. 8)** Each block has many implementations; the right choice depends on the workload. Ex: spatial data → GeoJSON (representation), PostGIS (storage), R-tree (indexing).
- **(s. 9)** The three things a system must be: **Reliable**, **Scalable**, **Maintainable**.
- **(s. 11)** [[reliability]] = correct function, tolerance to user mistakes, good performance under expected load, prevention of unauthorised access. → "resilient systems."
- **(s. 12)** [[fault-vs-failure]] — fault is a *component* misbehaving (hardware or software); failure is the *whole system* stopping. Fault-tolerant systems prevent faults from cascading into failures.
- **(s. 13)** Hardware faults: HDDs, RAM, PSUs. A 10,000-disk cluster sees ~1 dead disk/day. Traditional response: RAID, redundant PSUs, hot-swap CPUs. At scale, even those aren't enough → need infrastructure resilient to individual machine failures.
- **(s. 14)** Software faults are harder to anticipate: correlated across many nodes (a bad monitoring agent, a runaway process), can cause **cascading failures**.
- **(s. 15)** **CrowdStrike outage (Jul 2024)** — 8.5M systems crashed, ~£4.1bn losses. A canonical example of correlated software fault.
- **(s. 17)** [[scalability]] = ability to cope with **increased load**. Definition turns on how you parameterise "load."
- **(s. 18)** Load parameters are domain-specific: requests/sec (web), read/write ratio (DB), concurrent players (game). Bottleneck is usually not the average — it's the extreme cases and the cost-of-operation distribution.
- **(s. 19–20)** **Twitter case (Nov 2012):** post-tweet 4.6k req/s avg / 12k peak; home-timeline 300k req/s. **Fan-out:** each user follows many and is followed by many — drives the architectural choice.
- **(s. 21)** Performance metric depends on system: web → response time; analytics → records/sec or job duration. Two ways to measure: hold system fixed and watch performance, or hold performance fixed and watch resource cost.
- **(s. 22)** Performance is a *distribution*, not a single value. Average response time hides tail behaviour — what fraction of users are *outside* the expected range matters.
- **(s. 23–27)** [[twitter-fanout-case-study]]:
  - Approach 1: insert tweet into a global table; on read, look up follows and merge their tweets sorted by time. Read-heavy, expensive at scale.
  - Approach 2: write fan-out — on post, push the tweet into each follower's home-timeline cache.
  - Twitter started with #1, switched to #2 because reads outweigh writes by ~2 orders of magnitude. 4.6k tweets/s × ~75 followers = **345k cache writes/s** — but reads are now O(1).
  - **Hybrid:** approach 2 for normal users, approach 1 for celebrities (very high follower counts), to avoid runaway fan-out.
- **(s. 28)** [[vertical-vs-horizontal-scaling]] — vertical (scale-up, shared-memory): non-linear cost growth, limited fault tolerance. Horizontal (scale-out, shared-nothing): better cost scaling and fault tolerance.
- **(s. 30)** [[maintainability]] = three sub-properties: **operability**, **simplicity**, **evolvability**.
- **(s. 31)** *Operability:* runtime visibility, monitoring, automation hooks, no single-machine dependencies, predictable behaviour.
- **(s. 32)** *Simplicity:* not the same as "fewer features" — it means removing **accidental complexity** (the kind that arises from implementation, not the problem itself). Abstraction is a key tool.
- **(s. 33)** *Evolvability:* ease of changing the system; flows from simplicity and good abstractions.

## Key takeaways

1. The textbook framework of the entire module: **Reliable, Scalable, Maintainable**. Every later lecture is a deeper dive into one of these.
2. **Faults are inevitable; failures are not.** Fault tolerance is the engineering goal — graceful degradation rather than outage.
3. **Load is multi-dimensional.** You don't reason about "how big" — you reason about *which parameter* is the bottleneck. Twitter's bottleneck was fan-out, not absolute traffic.
4. **Performance is a distribution.** Tail latency (p95, p99) matters more than averages.
5. **Vertical scaling buys time; horizontal scaling buys options.** The economic argument for big-data architectures is that commodity hardware + horizontal scaling beats one-big-box past a certain scale.
6. **Maintainability is about people, not machines.** Operability, simplicity, evolvability all reduce the human cost of running and changing the system.

## Concepts introduced

- [[reliability]]
- [[scalability]]
- [[maintainability]]
- [[fault-vs-failure]]
- [[vertical-vs-horizontal-scaling]]
- [[twitter-fanout-case-study]]

## Open questions / things to clarify

- The CrowdStrike example (s. 15) is illustrative — the lecturer doesn't appear to expect numerical recall. Worth knowing as a *type* of fault (correlated software fault on update), not the figures.
- Fan-out arithmetic on s. 26 (75 followers × 4.6k/s = 345k/s) is a worked example — easy exam fodder if a similar number is given.

## See also

- [[introduction]]
- [[reliability]]
- [[scalability]]
- [[maintainability]]
- [[cap-theorem]]
- [[vertical-vs-horizontal-scaling]]
