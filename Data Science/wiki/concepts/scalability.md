---
title: "Scalability"
type: concept
sources: [data-intensive-applications, review]
related: [reliability, maintainability, vertical-vs-horizontal-scaling, twitter-fanout-case-study, partitioning, replication]
updated: 2026-05-02
---

# Scalability

*A system's ability to cope with increased load — defined not in the abstract but in terms of specific load parameters, performance metrics, and the distribution of response times.*

## Definition

**Scalability** is the term for how a system copes when load grows. It is not a binary property but a *function* — given a load parameter, how does performance respond? Two ways to ask the question:

1. *Hold the system fixed:* if load doubles, what happens to performance?
2. *Hold performance fixed:* if load doubles, how much do we have to grow the resources?

## Why it matters

Single-machine assumptions break down past a threshold. The Big Data era is defined by problems where this threshold is reached routinely (see [[3vs-of-big-data]]). Scalability decisions ripple through the entire architecture — they motivate [[replication]], [[partitioning]], [[batch-processing]], and [[stream-processing]].

## Mechanism — defining load

Load is **domain-specific**. Choose the parameter that captures your bottleneck:

| Domain | Typical load parameter |
|---|---|
| Web service | Requests / second |
| Database | Read/write ratio, queries / second |
| Online game | Concurrent players |
| Analytics | Records / second, dataset volume |

Watch out for:
- **Average vs extreme cases.** The bottleneck is usually the tail (p95, p99 latency), not the mean.
- **Cost-of-operation distribution.** Different operations have different costs; concurrency makes the worst-case ones dominate.
- **Hidden parameters.** Twitter's bottleneck wasn't tweets/sec — it was the **fan-out** (each user follows many, is followed by many). See [[twitter-fanout-case-study]].

## Mechanism — measuring performance

- **Web services:** response time (request → response).
- **Data analysis:** records/sec or job duration.
- Performance is *dynamic* — varies with current load, network conditions. Report a **distribution**, not just a mean. *What fraction of users see acceptable performance?*

## Mechanism — responding to load

Two big architectural levers:

- **[[vertical-vs-horizontal-scaling|Vertical scaling]]** (scale up): bigger machine. Costs grow super-linearly; fault tolerance is limited.
- **[[vertical-vs-horizontal-scaling|Horizontal scaling]]** (scale out): more machines. Costs scale better; fault tolerance improves.

Within horizontal scaling, [[replication]] handles read-scaling and availability, while [[partitioning]] handles write-scaling and dataset volume.

## Trade-offs

- **Vertical** keeps the system simple but caps your ceiling and concentrates risk in one box.
- **Horizontal** removes the ceiling but introduces all the distributed-systems pain ([[consistency]], [[replication-lag]], [[partitioning]] strategies, consensus).
- **Premature horizontal scaling is a tax.** Pay it only once a single machine cannot keep up.

## Examples in the syllabus

- **Twitter** ([[twitter-fanout-case-study]]) — switched from query-time merge (approach 1) to write-time fan-out (approach 2) because the read/write ratio was 100×.
- **Netflix CDN** — 8,492 servers across 578 locations (2018) — geo-distributed scaling for latency and availability.

## Common exam framing

- "What does scalability mean in the context of a data-intensive application? What is the role of load parameters?"
- "Compare vertical and horizontal scaling. When would you prefer each?"
- "Twitter chose write-fan-out over query-time merging — explain the trade-off in terms of load parameters." → ratio of timeline-reads to tweet-posts; latency vs storage cost.

## See also

- [[vertical-vs-horizontal-scaling]]
- [[twitter-fanout-case-study]]
- [[replication]]
- [[partitioning]]
- [[stream-processing]]
