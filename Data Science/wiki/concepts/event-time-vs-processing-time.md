---
title: "Event time vs processing time"
type: concept
sources: [stream-processing-2025, review]
related: [stream-processing, event-streams]
updated: 2026-05-02
---

# Event time vs processing time

*Two clocks govern every stream pipeline: when the event happened vs when the system saw it. Confusing them corrupts aggregations.*

## Definition

- **Event time** — the timestamp embedded in the event itself, recording *when the real-world occurrence happened*.
- **Processing time** — the wall-clock time at which the stream processor *received and processed* the event.

In an ideal network with zero latency these would be identical. In practice they diverge due to network delays, retries, mobile devices going offline, and system clock skew.

## Why it matters

Stream pipelines frequently compute windowed aggregations — "how many purchases in the last 5 minutes?" If you use processing time, a delayed batch of events all arrive together and land in the wrong window, inflating one window and deflating another. Using event time means each event lands in the window it logically belongs to.

## Mechanism — watermarks

Because the stream is unbounded and events can arrive out of order, the processor needs a way to decide "I have seen enough events up to time T — I can now close the window ending at T." This is done via **watermarks**:

- A watermark is a signal that says: "all events with event time ≤ T have (probably) arrived."
- The processor advances the watermark as it observes event timestamps.
- When the watermark passes a window boundary, the processor closes and emits the window result.
- Events that arrive *after* the watermark (late events) can be:
  - **Dropped** — simple, some data loss.
  - **Reprocessed** — window updated, output corrected.
  - **Held** — wait longer before closing windows (increases latency).

## Trade-off: correctness vs latency

Waiting longer for late events (a generous watermark) increases result correctness but increases output latency. A tight watermark reduces latency but risks dropping late events. Systems like Apache Flink expose this trade-off as a tunable parameter.

## Examples in the syllabus

- Review deck: explicitly calls out event-time vs processing-time as an exam-relevant distinction.
- Stream Processing 2025: mentioned in the context of time-windowed aggregations and out-of-order arrivals.

## Common exam framing

- "Why is event-time semantics important in a stream pipeline?"
- "What is a watermark and what problem does it solve?"
- "Give an example of when processing-time semantics would produce a wrong result."

## See also

- [[stream-processing]]
- [[event-streams]]
