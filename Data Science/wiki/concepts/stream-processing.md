---
title: "Stream processing"
type: concept
sources: [stream-processing-2025, review]
related: [batch-processing, event-streams, messaging-systems, online-vs-batch-vs-stream, event-time-vs-processing-time]
updated: 2026-05-02
---

# Stream processing

*Continuous computation over an unbounded sequence of events. Conceptually, batch with the window shrunk to zero. The architecture for working with data the moment it appears.*

## Definition

A **stream processing system** consumes events from one or more producers, performs computations (filter, aggregate, join, window) over them, and produces output events or state updates — **as the events arrive**, with low latency.

Inputs are unbounded — the system never reaches "end of input" — so the algorithm must produce useful output continuously, often by aggregating over **time windows**.

## Why it matters

Many high-value applications need freshness:

- **Fraud detection** — flag suspicious transactions in milliseconds.
- **Real-time recommendations** — react to the last click.
- **Operational analytics** — dashboards that aren't 24h old.
- **IoT / telemetry** — sensor data is most valuable while it's fresh.

## Mechanism — the limit of batch

The lecture builds the case from batch:

1. Batch processes a bounded chunk → produces output (s. 6).
2. Make the chunks smaller (every hour, every minute, every second).
3. Eventually you treat each event individually — that's stream processing (s. 7).

## Mechanism — components

- **Producers** generate events (web servers, sensors, mobile apps).
- A **[[message-broker]]** (Kafka, Pulsar, RabbitMQ) durably stores events between producers and consumers.
- **Consumers / stream processors** (Flink, Spark Streaming, Kafka Streams) compute over the stream — windowed aggregations, joins, transformations.
- **Sinks** receive results (databases, dashboards, downstream brokers).

## Mechanism — what makes it hard

- **State.** Aggregations need to remember history. State must survive failures (checkpointing).
- **Time.** Out-of-order arrivals, network delay, clock skew. See [[event-time-vs-processing-time]].
- **Exactly-once semantics.** Without care, retries cause duplicate processing.
- **Backpressure.** Producers can outrun consumers — see "drop / buffer / backpressure" (Stream Processing s. 12).

## Trade-offs vs batch

| | Batch | Stream |
|---|---|---|
| Input | Bounded | Unbounded |
| Latency | Minutes–hours | ms–seconds |
| Fault tolerance | Re-run | Checkpointing + replay |
| Reasoning | "Static" — finite I/O | "Dynamic" — windows, watermarks |

## Examples in the syllabus

- The full Stream Processing 2025 deck.
- Review s. 25 puts stream as the natural endpoint of the batch-window-shrinking argument.

## Common exam framing

- "Distinguish stream and batch processing. Give two examples of applications that demand stream processing."
- "Why is event-time semantics important in a stream pipeline?"
- "What strategies can a stream system use when producers outrun consumers?" → drop, buffer, backpressure.

## See also

- [[batch-processing]]
- [[event-streams]]
- [[messaging-systems]]
- [[message-broker]]
- [[event-time-vs-processing-time]]
- [[online-vs-batch-vs-stream]]
