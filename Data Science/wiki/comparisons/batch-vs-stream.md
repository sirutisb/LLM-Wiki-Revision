---
title: "Batch vs stream processing"
type: comparison
sources: [batch-processing, stream-processing-2025, review]
related: [batch-processing, stream-processing, online-vs-batch-vs-stream, mapreduce, messaging-systems]
updated: 2026-05-02
---

# Batch vs stream processing

*Two halves of the data processing landscape — batch is the workhorse for deep analytics on historical data; stream is the engine for real-time reaction.*

## Summary

Use **batch** when you need complete, high-quality computations over a known dataset and can afford latency (ETL, ML training, nightly reports). Use **stream** when freshness matters and the input is unbounded (fraud detection, real-time recommendations, IoT monitoring). Stream is conceptually batch with an ever-shrinking time window.

## Comparison table

| Dimension | Batch | Stream |
|---|---|---|
| **Input** | Bounded (finite dataset) | Unbounded (continuous events) |
| **Latency** | Minutes–hours | Milliseconds–seconds |
| **Primary metric** | Throughput | Throughput + freshness |
| **Fault tolerance** | Re-run the job | Checkpointing + event replay |
| **State management** | Static — full dataset available | Dynamic — windows, watermarks |
| **Time semantics** | Not usually a concern | Event time vs processing time critical |
| **Frameworks** | MapReduce, Spark | Flink, Kafka Streams, Spark Streaming |
| **Input source** | Distributed filesystem (HDFS) | Message broker (Kafka) |
| **Output** | Files, tables | Events, state updates, dashboards |
| **Complexity** | Simpler to reason about | Harder — out-of-order, late events |

## Key differences explained

**Bounded vs unbounded**: A batch job knows when it's done — it processes all input, produces output, terminates. A stream processor never terminates; it must emit useful output continuously using windowed aggregations.

**Fault tolerance**: If a batch job fails mid-run, restart it (idempotent). A stream system can't restart from scratch — it uses **checkpointing** (periodic state snapshots) and **event replay** (re-reading from the broker's retained log).

**Time complexity**: Batch reasoning is "static" — the full input exists. Stream reasoning requires **watermarks** to decide when enough events have arrived to close a window, and policies for handling late arrivals.

## Decision rule

> If your use case tolerates minutes of latency, use batch. If it requires seconds or sub-second freshness, use stream.

## See also

- [[batch-processing]]
- [[stream-processing]]
- [[online-vs-batch-vs-stream]]
- [[mapreduce]]
- [[event-time-vs-processing-time]]
