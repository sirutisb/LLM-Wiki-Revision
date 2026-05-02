---
title: "Batch processing"
type: concept
sources: [batch-processing, review]
related: [stream-processing, mapreduce, online-vs-batch-vs-stream, distributed-filesystem]
updated: 2026-05-02
---

# Batch processing

*Reading a bounded input, running a large job, and producing a bounded output. Optimised for throughput, not latency.*

## Definition

A **batch processing system** takes a large amount of input data, runs a job to process it, and produces output data. Jobs:

- Run for **minutes to days**.
- Are typically **scheduled to run periodically** (every hour, every night).
- Operate on **bounded** input — the job knows when it has finished reading.

The primary performance metric is **throughput** (records per second, dataset per hour) — not latency.

## Why it matters

Batch processing was the first scalable big-data architecture, born of MapReduce / Hadoop. It dominated 2005–2015 and remains the workhorse for periodic analytics, ETL, ML feature generation, and any job that can wait for the next scheduled run.

## Mechanism

Inputs and outputs are **files** (typically on a [[distributed-filesystem]]). The job:

1. Reads its inputs.
2. Applies a transformation (often as a graph of [[mapreduce|MapReduce]] / Spark stages).
3. Writes outputs.

Output is **derived data** — recoverable by re-running the job. This is a powerful property: bugs can be fixed by reprocessing.

## Comparison — batch vs stream

See [[online-vs-batch-vs-stream]] for the three-way comparison. Headline:

| | Batch | Stream |
|---|---|---|
| Input | Bounded | Unbounded |
| Latency | High (minutes–hours) | Low (ms–s) |
| Output | Files | More events |
| Reprocessing | Easy (re-run) | Harder (replay events) |

## Trade-offs

- **+** Throughput-optimised — does the most work per machine-hour.
- **+** Fault tolerance is easy — re-run failed tasks; output is deterministic from input.
- **+** Easy to reprocess for bug fixes or schema changes.
- **−** High latency — by definition, the answer is at least as old as the schedule.
- **−** Can't react to in-flight events.

## Examples in the syllabus

- The opening of the Batch Processing lecture (s. 2) defines all three system classes.
- MapReduce on Hadoop is the canonical example.
- Modern: Apache Spark, Apache Flink (in batch mode), Google Dataflow / BigQuery batch jobs.

## Common exam framing

- "Distinguish batch and stream processing on input characteristics, latency, and primary metric."
- "What is meant by 'derived data' and why is it useful in a batch pipeline?"
- "Why is throughput, rather than response time, the right metric for batch jobs?"

## See also

- [[mapreduce]]
- [[stream-processing]]
- [[online-vs-batch-vs-stream]]
- [[distributed-filesystem]]
