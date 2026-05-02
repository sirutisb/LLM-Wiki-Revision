---
title: "Multiple consumers"
type: concept
sources: [stream-processing-2025]
related: [stream-processing, message-broker, messaging-systems]
updated: 2026-05-02
---

# Multiple consumers

*Two distinct patterns for delivering messages when several consumers read the same topic: load balancing (split the work) vs fan-out (broadcast to all).*

## Definition

When multiple consumers subscribe to the same topic, the [[message-broker|message broker]] must decide how to route each message. There are two canonical patterns:

- **Load balancing** — each message is delivered to **one** consumer. The consumers share the workload; each event is processed once. Also called competing consumers or a work queue.
- **Fan-out** — each message is delivered to **all** consumers. Every subscriber sees every event independently. Also called publish/subscribe broadcast.

## Why it matters

The choice between these two patterns determines parallelism, consistency, and ordering guarantees. Picking the wrong pattern can cause duplicate processing (fan-out when you wanted load balancing) or lost processing (load balancing when every service needs the event).

## Mechanism

```
Load balancing:
  Topic  →  Broker  →  Consumer A  (gets messages 1, 3, 5, ...)
                  →  Consumer B  (gets messages 2, 4, 6, ...)

Fan-out:
  Topic  →  Broker  →  Consumer A  (gets ALL messages)
                  →  Consumer B  (gets ALL messages)
```

In Kafka, load balancing is achieved via **consumer groups** (multiple consumers in the same group share partitions). Fan-out is achieved by putting consumers in **different groups** — each group gets its own copy of every message.

## Trade-offs

| | Load balancing | Fan-out |
|---|---|---|
| Throughput | Higher — parallelised | Same as a single consumer per group |
| Ordering | May break (redelivered message goes to different consumer) | Each consumer sees order independently |
| Use case | Parallel workers, task queues | Multiple services needing the same data |
| Processing | Each event once total | Each event once per consumer group |

## Ordering caveat

With load balancing, **acknowledgement + redelivery** can violate ordering. If Consumer A processes message 1 but crashes before acking, the broker redelivers message 1 to Consumer B — who may have already processed message 2. Message 1 arrives "late" relative to message 2 in Consumer B's view.

## Examples in the syllabus

- Stream Processing 2025 s. 16: load-balancing vs fan-out named explicitly.
- Real system: a purchase event needs to go to the inventory service (load balanced across its workers) AND the analytics service (separate consumer group — fan-out).

## Common exam framing

- "Distinguish load balancing and fan-out in a message broker."
- "Why can load balancing cause message ordering to break?"

## See also

- [[message-broker]]
- [[messaging-systems]]
- [[stream-processing]]
