---
title: "Lecture: Review"
type: lecture
sources: [review]
related: [reliability, scalability, maintainability, cap-theorem, acid-properties, eventual-consistency, nosql-databases, document-model, vertical-vs-horizontal-scaling, replication, partitioning, batch-processing, stream-processing, event-streams, event-time-vs-processing-time, tensors, sparse-tensors, virtualisation, containerisation]
updated: 2026-05-02
---

# Lecture: Review

*The lecturer's own end-of-module synthesis — the topics covered here are the highest-confidence exam signals. If it's in this deck, it's expected to appear on the exam.*

> **Usage note:** this deck recaps content from across the module. Each section below points to the canonical concept page. Use this as a revision checklist, not a source of new information.

## Topics covered (in order)

### Reliability (s. 2–4)
- Application performs expected function; tolerates user mistakes; good performance under expected load; prevents unauthorised access.
- **Fault vs failure**: fault = one component behaves unexpectedly; failure = the whole system stops providing service.
- → [[reliability]], [[fault-vs-failure]]

### Scalability (s. 5–6)
- Ability to cope with increased load. Load parameters (requests/sec, read/write ratio, simultaneous players). Average case vs outliers.
- → [[scalability]]

### Maintainability (s. 7–8)
- Overall cost to keep a system operational. Three dimensions: **Operability** (easy for ops to run), **Simplicity** (easy for new engineers to understand), **Evolvability** (easy to change).
- → [[maintainability]]

### Consistency — CAP theorem (s. 9–10)
- Consistency: every read gets most-recent write or error. Availability: every request gets a non-error response. Partition tolerance: operates despite disconnection. In distributed systems, partition tolerance is mandatory — choose CA+P impossible, so CP vs AP.
- → [[cap-theorem]]

### ACID (s. 11)
- Atomicity, Consistency, Isolation, Durability. Standard transaction guarantees.
- → [[acid-properties]]

### Eventual consistency (s. 12)
- At any given time, some nodes may have outdated data. Most replicated systems guarantee eventual consistency — all nodes will *eventually* converge; reads will *eventually* return the same value.
- → [[eventual-consistency]]

### NoSQL / Document store (s. 13–15)
- Non-relational, focuses on simplicity, horizontal scalability, availability. Document databases (MongoDB) group documents into collections, without rigid schema.
- → [[nosql-databases]], [[document-model]]

### Scaling (s. 16–17)
- **Vertical scaling**: costs don't scale linearly, limited fault tolerance.
- **Horizontal scaling**: costs scale better, better fault tolerance.
- → [[vertical-vs-horizontal-scaling]]

### Replication (s. 18–19)
- Each node stores a copy (replica). Reduces latency, increases availability, increases read throughput. Constraint: data fits on one machine. Write operations update all copies.
- → [[replication]]

### Partitioning (s. 20–21)
- Each node stores a *subset* (partition). Each piece of data belongs to exactly one partition. Focus on scalability. Often combined with replication.
- → [[partitioning]]

### Batch processing (s. 22–23)
- Takes large input, runs job, produces output. Minutes-to-days latency. Primary metric: **throughput**. Scheduled periodically.
- → [[batch-processing]]

### Stream processing (s. 24–25)
- Unbounded data sources. Batch with ever-shrinking window → eventually processing every event as it arrives.
- → [[stream-processing]]

### Event streams (s. 26)
- Events: small, self-contained, immutable, timestamped. Producer → consumer model. Encoded as JSON, binary, etc.
- → [[event-streams]]

### Event time vs processing time (s. 27)
- Confusing these leads to bad data.
- → [[event-time-vs-processing-time]]

### Tensors (s. 28–32)
- 0-order scalar, 1-order vector, 2-order matrix, 3-order tensor. Real-world shapes: vector (features), timeseries (features × timestamps), image (W×H×C), video (frames × W×H×C). Sparse tensors; DOK representation.
- → [[tensors]], [[sparse-tensors]]

### Virtualisation (s. 33–34)
- Software-based VM; hypervisor; guests interact with host hardware; overhead and redundancy drawbacks.
- → [[virtualisation]]

### Containerisation (s. 35–36)
- OS-level virtualisation; share host OS kernel; isolated, portable, scalable.
- → [[containerisation]]

## What the Review tells us about the exam

The Review deck covers exactly these topics and *excludes* others. Topics covered in other lectures but **not** in the Review include:
- HPC specifics (SLURM job states, Amdahl's Law formula)
- TLP (OpenMP, MPI)
- Software-hardware co-design (bottom-up/top-down details)
- Distributed ML internals (all-reduce implementation, k-means phases)
- Online Learning algorithm details
- Concept Drift algorithm internals (ADWIN window mechanics, DDM formula)

This doesn't mean those topics are out-of-scope — but expect the core concepts listed above to be directly examined.

## Key takeaways

1. **Reliability, Scalability, Maintainability** — the three pillars of the module framework.
2. **CAP, ACID, Eventual Consistency** — consistency concepts always examined.
3. **Replication vs Partitioning** — complementary techniques for scale and availability.
4. **Batch vs Stream** — two halves of the data processing landscape.
5. **Tensors + sparse representations** — the data representation underpinning all ML at scale.
6. **Virtualisation vs Containerisation** — both are in the Review; know the contrast.

## See also

- [[reliability]], [[scalability]], [[maintainability]]
- [[cap-theorem]], [[acid-properties]], [[eventual-consistency]]
- [[batch-processing]], [[stream-processing]]
- [[tensors]], [[sparse-tensors]]
- [[virtualisation]], [[containerisation]]
