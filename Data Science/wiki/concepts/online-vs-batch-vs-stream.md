---
title: "Online vs batch vs stream systems"
type: concept
sources: [batch-processing, stream-processing]
related: [batch-processing, stream-processing, scalability]
updated: 2026-05-02
---

# Online vs batch vs stream systems

*The three system archetypes that organise the second half of the module — services, batch jobs, and stream processors. Each has a different latency target and primary metric.*

## Definition

| Class | Input | Output | Latency | Primary metric | Example |
|---|---|---|---|---|---|
| **Online (services)** | Live requests | Per-request response | ms | Response time, availability | Web API, database query |
| **Batch (offline)** | Bounded files | Bounded output files | minutes–days | **Throughput** | MapReduce job, nightly ETL |
| **Stream (near-real-time)** | Unbounded event stream | More events / state updates | ms–seconds | Throughput + freshness | Kafka pipeline, fraud detection |

## Why it matters

Naming what kind of system you're building is the first architectural decision. The metric you pick (response time, throughput, freshness) drives every later choice.

## Mechanism — boundary between batch and stream

The lecture frames stream as **the limit of batch with an ever-shrinking window**. As you make the batch window smaller (24h → 1h → 1m → 1s) you eventually start treating each event individually. That's stream processing.

> "We could make this window smaller and smaller… until we forget time windows and analyse every event as they arrive."  
> — Stream Processing s. 7

## Trade-offs

- **Online systems** must answer fast — no time to do heavy analytics inline. Cache, precompute, route.
- **Batch systems** can be more sophisticated (full joins, aggregations, ML training) but are stale by design.
- **Stream systems** sit between: more freshness than batch, more sophistication than online — at the cost of harder fault tolerance, tricky semantics around time and state.

## Examples in the syllabus

- s. 2 of Batch Processing introduces the three classes.
- s. 7 of Stream Processing 2025 frames stream as "batch with an infinitely small window."

## Common exam framing

- "Distinguish online, batch, and stream systems on input characteristics, latency, and primary metric."
- "Why is throughput the right metric for batch but response time the right metric for online?"
- "How does stream processing differ from making a batch system run more often?"

## See also

- [[batch-processing]]
- [[stream-processing]]
