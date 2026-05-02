---
title: "Messaging systems"
type: concept
sources: [stream-processing-2025]
related: [stream-processing, event-streams, message-broker, multiple-consumers]
updated: 2026-05-02
---

# Messaging systems

*Infrastructure that connects event producers to consumers, decoupling them so neither needs to know about the other's timing or location.*

## Definition

A **messaging system** is middleware that accepts events from producers and delivers them to consumers. It implements the **publish/subscribe** model: producers send to named topics or queues; consumers subscribe and receive. The key benefit is decoupling — producers don't need to know who's consuming, and consumers don't need to be online when events are produced.

## Why it matters

Without a messaging layer, producers must push directly to consumers (brittle — consumer might be offline) or consumers must poll a database (wastes resources, adds latency). Messaging systems solve both: they buffer events durably and push/notify consumers as events arrive.

## Mechanism — two approaches

### Approach 1 — Direct messaging (no broker)

- Producer pushes events directly to consumers over TCP/UDP/multicast.
- **Problem:** if the consumer is offline, events are lost. No buffering, no replay.
- Fine for low-latency real-time use cases where some loss is acceptable (live video, games).

### Approach 2 — Message broker

- A server-side [[message-broker|message broker]] sits between producers and consumers.
- Producers write to the broker; consumers read from it.
- The broker buffers messages, persists them, and redelivers on failure.
- See [[message-broker]] for the full breakdown.

## Handling producer/consumer speed mismatch

When producers send faster than consumers can handle (s. 12):

| Strategy | Behaviour | Cost |
|---|---|---|
| **Drop** | Discard excess messages | Data loss |
| **Buffer** | Queue up messages | Memory / disk pressure |
| **Backpressure** | Slow the producer down (flow control) | Producer throughput reduced |

## Trade-offs

- **Durability** — broker-based systems persist messages; direct messaging does not.
- **Ordering** — brokers can guarantee per-partition order; direct messaging has no ordering guarantee.
- **Latency** — direct messaging is slightly lower latency (no broker hop).
- **Complexity** — brokers add an operational component to manage.

## Examples in the syllabus

- Stream Processing 2025 s. 11–16: full discussion of why databases aren't enough, then the messaging system pattern.
- Kafka, RabbitMQ, Pulsar — all broker-based messaging systems.

## Common exam framing

- "Why can't you just poll a database instead of using a messaging system?"
- "What is backpressure and when would a stream system apply it?"
- "Compare direct messaging and broker-based messaging."

## See also

- [[stream-processing]]
- [[event-streams]]
- [[message-broker]]
- [[multiple-consumers]]
