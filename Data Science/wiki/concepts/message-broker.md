---
title: "Message broker"
type: concept
sources: [stream-processing-2025]
related: [stream-processing, messaging-systems, event-streams, multiple-consumers]
updated: 2026-05-02
---

# Message broker

*A server-side intermediary that durably stores events between producers and consumers, tolerating disconnections, absorbing bursts, and enabling multiple consumption patterns.*

## Definition

A **message broker** (or message queue) is a server process that accepts events from producers, persists them, and delivers them to consumers on demand. It decouples the two sides in both time (producer and consumer don't need to be running simultaneously) and space (neither knows the other's address).

## Why it matters

Without a broker, a stream system must either use fragile direct connections or poll a database. The broker eliminates both problems: it absorbs bursts, survives consumer crashes, and supports multiple consumers reading the same data independently.

## Mechanism

```
Producer(s)  →  [Broker / topic]  →  Consumer(s)
```

1. Producer publishes an event to a named **topic** (or queue).
2. Broker stores the event (in memory and/or on disk).
3. Consumer(s) pull from or are pushed to from the topic.
4. Consumer sends an **acknowledgement** (ack) after processing.
5. Broker deletes (or marks as consumed) once acked; redelivers if no ack arrives.

## Broker vs database

| Dimension | Database | Message broker |
|---|---|---|
| Retention | Until explicitly deleted | Auto-deleted after delivery |
| Query model | Rich queries, indexes | Topic/queue subscription only |
| Persistence | Long-lived | Short-lived by default |
| Intended use | Store-and-retrieve | Notify-and-consume |

(Kafka bends these rules — it retains messages for a configurable period and allows replay, behaving more like a durable log than a traditional queue.)

## Acknowledgements and redelivery

- A consumer must **ack** each message after successful processing.
- If the broker doesn't receive an ack (consumer crashes, times out), it **redelivers** the message to another consumer.
- This guarantees **at-least-once delivery** — but means the same message may be processed more than once. Consumers must be idempotent or use deduplication to achieve exactly-once.
- Redelivery with [[multiple-consumers|load-balanced consumers]] can cause **out-of-order processing**.

## Examples in the syllabus

- Stream Processing 2025 s. 14–17: broker model introduced as the production-grade approach.
- **Apache Kafka** — the dominant broker in production: partitioned, replicated, log-based, high-retention.
- **RabbitMQ**, **Pulsar** — alternative brokers with different delivery semantics.

## Common exam framing

- "Describe the role of a message broker in a stream processing pipeline."
- "How does a message broker handle a consumer that crashes mid-processing?"
- "What is the difference between a message broker and a database?"

## See also

- [[messaging-systems]]
- [[event-streams]]
- [[multiple-consumers]]
- [[stream-processing]]
