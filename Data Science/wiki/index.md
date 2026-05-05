# Data Science at Scale — Index

The catalog of every page in this wiki. Updated on every ingest. Use this to find pages; drill into them for the actual content.

## Lectures

*One page per source deck — slide-by-slide notes plus key takeaways.*

- [[introduction]] — Sets the scene: Big Data era, enabling forces, transformed domains, the 3Vs.
- [[data-intensive-applications]] — Reliability, Scalability, Maintainability; fault vs failure; Twitter fan-out case study; vertical vs horizontal scaling.
- [[storage-and-retrieval]] — Log-structured storage, hash indexes, SSTables, LSM-tree, B-tree; OLTP vs OLAP.
- [[data-models-nosql]] — Relational, document, graph data models; NoSQL families; schema-on-read vs schema-on-write.
- [[consistency]] — CAP theorem, ACID, eventual consistency, linearizability, consensus, 2PC.
- [[replication]] — Leader-follower replication, sync/async, failover, replication lag, read-your-writes, monotonic reads.
- [[partitioning]] — Key-range, hash, secondary indexes (by-document/by-term), rebalancing.
- [[batch-processing]] — Three system classes, Unix philosophy, MapReduce, distributed filesystems, workflows, reduce-side vs map-side joins.
- [[stream-processing]] — Events, messaging systems, direct vs broker, load-balancing vs fan-out, acks/redelivery, event time.
- [[distributed-machine-learning]] — Communication patterns, SGD with all-reduce, parallel k-means via MapReduce.
- [[online-learning]] — Full batch vs mini-batch vs online learning; three data shift types (covariate, prior, concept drift).
- [[concept-drift-detection]] — Concept drift types (gradual, abrupt, recurring); ADWIN, DDM, EDDM algorithms.
- [[high-performance-computing]] — FLOPS scales, Moore's Law, Amdahl's Law, SLURM entities and states.
- [[thread-level-parallelism]] — Flynn's taxonomy (SISD/SIMD/MIMD); OpenMP fork-join; MPI communicators, ranks, point-to-point.
- [[tensors]] — Tensor orders (0–3+); real-world data shapes; sparse tensors; DOK, COO, CSR formats.
- [[software-hardware-codesign]] — Bottom-up, top-down, co-design approaches; partitioning; edge computing.
- [[virtualisation-and-containerisation]] — Hypervisors, VMs, snapshots; containers, OS-level virtualisation; orchestration, PaaS.
- [[review]] — Lecturer's synthesis: all Review-deck topics listed with links to canonical concept pages.

## Concepts

*Reusable definitions and explanations of recurring ideas.*

### Foundations
- [[3vs-of-big-data]] — Volume, Velocity, Variety (+ Veracity, Value): each V breaks a different assumption.
- [[big-data-era]] — The convergence enabling the whole module.
- [[data-sources-timeline]] — Machine → employee → user → device-generated data.
- [[iaas]] — Infrastructure as a Service: cloud making big-data infrastructure rentable.
- [[reliability]] — System performs expected function, tolerates faults, is secure.
- [[scalability]] — Ability to handle increased load; load parameters; fan-out case study.
- [[maintainability]] — Operability + Simplicity + Evolvability.
- [[fault-vs-failure]] — Component misbehaviour vs whole-system stoppage.
- [[vertical-vs-horizontal-scaling]] — Scale up vs scale out.
- [[twitter-fanout-case-study]] — Write fan-out vs read-time merge; the hybrid approach.

### Storage engines
- [[database-log]] — Append-only log: the foundation of all durable storage.
- [[hash-index]] — In-memory hashtable over a log; fast lookups; bounded key space.
- [[sstables]] — Sorted, immutable on-disk files; the output layer of LSM-trees.
- [[lsm-tree]] — Log-Structured Merge-tree: write-optimised; memtable + SSTables + compaction.
- [[b-tree]] — Balanced page-tree: read-optimised; mutable in-place updates.
- [[compaction]] — Background merge of SSTables; reclaims space, removes tombstones.
- [[oltp-vs-olap]] — Row-oriented OLTP vs column-oriented OLAP workloads.
- [[distributed-filesystem]] — HDFS, Colossus: split + replicate + data locality.

### Data models
- [[relational-model]] — Tables, foreign keys, SQL, schema-on-write, impedance mismatch.
- [[document-model]] — JSON/BSON, schema-on-read, locality, limited joins.
- [[graph-model]] — Vertices + directed edges + properties; multi-hop traversals.
- [[key-value-store]] — Simplest NoSQL; pure key→value lookup.
- [[wide-column-store]] — Sparse rows with flexible column sets (Cassandra, HBase).
- [[nosql-databases]] — The four NoSQL families and when to use each.
- [[schema-on-read]] — Schema-on-read vs schema-on-write trade-off.
- [[locality-storage]] — Storing related data together to reduce I/O.

### Consistency
- [[cap-theorem]] — Consistency, Availability, Partition Tolerance — choose two (P mandatory).
- [[acid-properties]] — Atomicity, Consistency, Isolation, Durability.
- [[eventual-consistency]] — Convergence guarantee, no recency guarantee.
- [[linearizability]] — Strongest single-object consistency; one-copy illusion.
- [[consensus]] — Getting distributed nodes to agree; leader election; atomic commit.
- [[two-phase-commit]] — Distributed atomic commit: prepare + commit.

### Replication
- [[replication]] — Copies on multiple nodes; availability and read scale.
- [[leader-follower-replication]] — Single writer, multiple read replicas.
- [[synchronous-vs-asynchronous-replication]] — Durability vs latency trade-off.
- [[replication-lag]] — Staleness and read anomalies (read-your-writes, monotonic reads).

### Partitioning
- [[partitioning]] — Subsets of data on different nodes; horizontal scale.
- [[key-range-partitioning]] — Contiguous key ranges; range queries; hotspot risk.
- [[hash-partitioning]] — Hash-based uniform distribution; no range queries.
- [[secondary-indexes-partitioning]] — By-document (local, scatter-gather reads) vs by-term (global, efficient reads).
- [[rebalancing-partitions]] — Fixed partition count vs dynamic split/merge.

### Batch & stream processing
- [[batch-processing]] — Bounded input; throughput metric; MapReduce; derived data.
- [[mapreduce]] — Map + shuffle + reduce; data locality; workflows.
- [[unix-philosophy]] — Composable tools; stdin/stdout; the inspiration for MapReduce.
- [[distributed-filesystem]] — (also in storage)
- [[reduce-side-join]] — MapReduce join via shuffle; avoids per-record lookups.
- [[map-side-join]] — Optimized join in the mapper; uses broadcast hash tables.
- [[online-vs-batch-vs-stream]] — Three system archetypes; input, latency, primary metric.
- [[stream-processing]] — Unbounded events; low latency; batch with vanishing window.
- [[event-streams]] — Small, immutable, timestamped records; producer/consumer model.
- [[messaging-systems]] — Pub/sub infrastructure; direct vs broker; drop/buffer/backpressure.
- [[message-broker]] — Server-side intermediary; durability; ack/redelivery.
- [[multiple-consumers]] — Load balancing (one consumer) vs fan-out (all consumers).
- [[event-time-vs-processing-time]] — When event happened vs when system saw it; watermarks.

### Distributed ML
- [[communication-patterns]] — Push, pull, broadcast, reduce, all-reduce, wait, barrier.
- [[sgd-all-reduce]] — Distributed minibatch SGD via all-reduce; statistically equivalent to serial.
- [[parallel-kmeans]] — MapReduce k-means: map=assign, combine=local sums, reduce=update centroids.

### Online learning & drift
- [[online-learning]] — Per-observation updates; learning rate; immediate adaptation.
- [[batch-vs-online-learning]] — Full batch vs mini-batch vs online comparison.
- [[data-shifts]] — Covariate shift, prior probability shift, concept drift — the three types.
- [[concept-drift]] — Input→output relationship changes; gradual/abrupt/recurring.
- [[adwin]] — Adaptive windowing drift detector; grows stable, shrinks on change.
- [[ddm-eddm]] — Error-rate drift detectors; DDM warning 2σ, change 3σ; EDDM for gradual.

### HPC & parallelism
- [[flops]] — Floating Point Ops/sec; G/T/P/EFLOPS scale; device benchmarks.
- [[moores-law]] — Transistor doubling every 2 years; now slowing.
- [[amdahls-law]] — S=1/((1−p)+p/s); sequential fraction caps speedup.
- [[slurm]] — HPC job scheduler; nodes, partitions, jobs, job steps; states.
- [[thread-level-parallelism]] — Flynn's taxonomy; SISD/SIMD/MIMD; threads vs processes.
- [[openmp]] — Shared-memory, fork-join, compiler-directive parallel API.
- [[mpi]] — Distributed-memory message passing; communicators, ranks, two-sided.

### Tensors
- [[tensors]] — Scalar/vector/matrix/tensor; data shapes for ML.
- [[sparse-tensors]] — Sparse format motivation; DOK, COO, CSR representations.

### Software-hardware & deployment
- [[software-hardware-codesign]] — Bottom-up, top-down, co-design; partitioning; iterative cycle.
- [[edge-computing]] — Compute on device; low power; personalisation.
- [[moores-law]] — (also in HPC)
- [[virtualisation]] — Hypervisor, VMs, snapshots; hardware-level isolation.
- [[containerisation]] — OS-level virtualisation; shared kernel; portable, lightweight.
- [[container-orchestration]] — Automated multi-container management; PaaS.

## Comparisons

*Side-by-side comparisons of competing options. Exam gold.*

- [[batch-vs-stream]] — Bounded/unbounded input; latency; fault tolerance; when to use each.
- [[vms-vs-containers]] — Isolation level; kernel sharing; startup time; use cases.
- [[replication-vs-partitioning]] — Complementary techniques; what each solves; used together.
- [[relational-vs-document-vs-graph]] — Data shape, join support, schema flexibility, examples.

## Topics

*Higher-level themes that group related concepts.*

- [[distributed-systems]] — Replication, partitioning, consistency, coordination.
- [[storage]] — Storage engines, workloads, distributed filesystems.
- [[machine-learning-at-scale]] — Distributed training, online learning, drift detection.

## Exam prep

*Revision-focused pages.*

- [[likely-questions]] — 27 anticipated exam questions with answer skeletons.
- [[cheatsheet]] — One-page condensed reference: formulas, definitions, key trade-offs.
- [[glossary]] — Term → one-line definition → concept page, alphabetical.

## Sources (raw decks)

| Deck | Lecture page | Status |
|---|---|---|
| Module Overview_2025 | — | meta — folded into bootstrap |
| Introduction | [[introduction]] | ✅ ingested 2026-05-02 |
| Data Intensive Applications_2025 | [[data-intensive-applications]] | ✅ ingested 2026-05-02 |
| Storage and Retrieval (+ 2024) | [[storage-and-retrieval]] | ✅ ingested 2026-05-02 |
| Data Models and NoSQL databases_2025 | [[data-models-nosql]] | ✅ ingested 2026-05-02 |
| Consistency_2025 | [[consistency]] | ✅ ingested 2026-05-02 |
| Distributed Architectures - Replication | [[replication]] | ✅ ingested 2026-05-02 |
| Distributed Architectures - Partitioning | [[partitioning]] | ✅ ingested 2026-05-02 |
| Distributed Architectures - part 2 (2025) | merged into [[partitioning]] | ✅ ingested 2026-05-02 |
| Batch Processing | [[batch-processing]] | ✅ ingested 2026-05-02 |
| Stream Processing (+ 2025) | [[stream-processing]] | ✅ ingested 2026-05-02 |
| Distributed Machine Learning | [[distributed-machine-learning]] | ✅ ingested 2026-05-02 |
| Online Learning | [[online-learning]] | ✅ ingested 2026-05-02 |
| Concept Drift Detection | [[concept-drift-detection]] | ✅ ingested 2026-05-02 |
| High performance Computing | [[high-performance-computing]] | ✅ ingested 2026-05-02 |
| TLP | [[thread-level-parallelism]] | ✅ ingested 2026-05-02 |
| tensor | [[tensors]] | ✅ ingested 2026-05-02 |
| Software-hardware co-design | [[software-hardware-codesign]] | ✅ ingested 2026-05-02 |
| Virtualisation and Containerisation | [[virtualisation-and-containerisation]] | ✅ ingested 2026-05-02 |
| Review | [[review]] | ✅ ingested 2026-05-02 (LAST — lecturer's synthesis) |
