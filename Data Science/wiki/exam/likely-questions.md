---
title: "Likely exam questions"
type: exam
sources: [review]
related: []
updated: 2026-05-02
---

# Likely exam questions

*Derived from Review deck coverage, slide-level exam framings, and the module structure. Review-deck topics are highest confidence.*

---

## Foundations

### Q1. What are the three NFRs for data-intensive applications? Define each.
**Answer skeleton:**
- **Reliability** — system performs its expected function, tolerates faults/mistakes, prevents unauthorised access. *Fault* = one component misbehaves; *failure* = whole system stops.
- **Scalability** — ability to handle increased load. Measured by load parameters (requests/sec, read/write ratio). Average case and outlier headroom both matter.
- **Maintainability** — overall cost to keep a system running. Three sub-dimensions: *Operability* (easy for ops), *Simplicity* (easy for new engineers), *Evolvability* (easy to change).
→ [[reliability]], [[scalability]], [[maintainability]]

---

## Consistency

### Q2. State the CAP theorem. What does it imply for distributed systems?
**Answer skeleton:**
- CAP: a distributed system cannot simultaneously guarantee Consistency, Availability, and Partition Tolerance.
- Partition tolerance is mandatory (network splits happen) → real choice is **CP** (sacrifice availability) vs **AP** (sacrifice strong consistency).
- CP example: relational DB with synchronous replication. AP example: Dynamo-style key-value store.
→ [[cap-theorem]]

### Q3. Define the four ACID properties.
**Answer skeleton:** Atomicity (all-or-nothing), Consistency (transactions leave DB in valid state), Isolation (concurrent transactions don't interfere), Durability (committed data survives failure).
→ [[acid-properties]]

### Q4. What is eventual consistency? When is it acceptable?
**Answer skeleton:** At any point in time, replicas may differ. Eventually (given no more writes) all replicas converge. No *recency* guarantee. Acceptable when users can tolerate briefly stale reads (shopping cart, social feeds). Not acceptable for money transfers.
→ [[eventual-consistency]]

### Q5. Define linearizability. How does it differ from eventual consistency?
**Answer skeleton:** Linearizability = every operation appears to take effect atomically at some point between its start and end; the system behaves as if there's one copy. This provides *recency*. Eventual consistency only promises convergence — not when. Linearizability is the strongest single-object guarantee.
→ [[linearizability]]

---

## Storage & Data Models

### Q6. Compare LSM-tree and B-tree storage engines.
**Answer skeleton:**
- LSM-tree: writes to memtable, flush to SSTables, compaction merges. Write-optimised; reads may check multiple levels; better compression; no in-place updates.
- B-tree: mutable pages, update in place, WAL for durability. Read-optimised; strong consistency; standard OLTP choice.
→ [[lsm-tree]], [[b-tree]]

### Q7. Distinguish relational, document, and graph data models.
**Answer skeleton:**
- Relational: data in tables, foreign-key joins, schema-on-write, strong consistency, SQL.
- Document: JSON/BSON documents, flexible schema (schema-on-read), locality for hierarchical data, limited joins.
- Graph: vertices + edges, each with properties; property graph model; excels at many-to-many traversals (social graphs, fraud detection).
→ [[relational-model]], [[document-model]], [[graph-model]]

### Q8. What is schema-on-read vs schema-on-write?
**Answer skeleton:** Schema-on-write enforces structure at write time (relational DBs — migrations needed to change). Schema-on-read interprets structure at read time (document stores — flexible, but application bears responsibility). Trade-off: safety vs flexibility.
→ [[schema-on-read]]

---

## Replication & Partitioning

### Q9. Describe leader-follower replication. What are the trade-offs of synchronous vs asynchronous replication?
**Answer skeleton:**
- Leader-follower: leader receives writes and propagates to followers. Reads can go to any replica.
- Sync: follower acknowledged before leader confirms write → durability guarantee but higher write latency; if follower fails, writes block.
- Async: leader confirms immediately → lower latency, but follower may lag; data loss on leader failure.
→ [[leader-follower-replication]], [[synchronous-vs-asynchronous-replication]]

### Q10. What problems can replication lag cause? How can they be mitigated?
**Answer skeleton:**
- Read-your-writes violation: user writes, reads from a lagging replica, sees old data.
- Mitigation: read own writes from leader; track latest write timestamp and wait for replica to catch up.
- Monotonic reads violation: two reads return data from different replica timestamps → user sees "time go backwards".
- Mitigation: route each user's reads to the same replica consistently.
→ [[replication-lag]]

### Q11. Compare key-range and hash partitioning. When would you use each?
**Answer skeleton:**
- Key-range: partitions are contiguous key ranges. Enables efficient range scans. Risk: hotspots on monotonic keys.
- Hash: apply hash to key; assign to partition by hash range. Distributes load evenly. Destroys range ordering.
- Use key-range for time-series or range queries. Use hash for uniform write distribution.
→ [[key-range-partitioning]], [[hash-partitioning]]

---

## Batch & Stream Processing

### Q12. Distinguish online, batch, and stream systems on input, latency, and primary metric.
**Answer skeleton:**

| | Online (services) | Batch | Stream |
|---|---|---|---|
| Input | Live requests | Bounded files | Unbounded events |
| Latency | ms | minutes–days | ms–seconds |
| Metric | Response time | Throughput | Throughput + freshness |

→ [[online-vs-batch-vs-stream]]

### Q13. Describe how MapReduce works. What are mappers, reducers, and the shuffle?
**Answer skeleton:** Mappers read input records and emit (key, value) pairs. Shuffle groups all values for each key and routes them to a reducer. Reducers process each key's values and emit output records. Framework handles distribution, fault tolerance, and data movement.
→ [[mapreduce]]

### Q14. Describe how to implement a join using MapReduce (reduce-side vs map-side).
**Answer skeleton:**
- **Reduce-side join (default):** Run two mappers in parallel — one per dataset — both emit (join_key, tagged_record). Shuffle groups both datasets' records by join key. Reducer receives all records for the same key and performs the join (one-to-many). Avoids per-record database lookups.
- **Map-side join (optimization):** If one dataset is small enough to fit in memory. Load small dataset into a hash table on every mapper. Stream large dataset through mappers; join happens via memory lookup. No shuffle needed.
→ [[reduce-side-join]], [[map-side-join]]

### Q15. What strategies does a stream system use when producers outrun consumers?
**Answer skeleton:** Three options: (1) **Drop** messages — simple, but data loss. (2) **Buffer** in a queue — tolerates bursts, but bounded memory. (3) **Backpressure** — slow the producer down (flow control). Choice depends on whether data loss is acceptable.
→ [[messaging-systems]]

### Q16. Distinguish load balancing and fan-out in a message broker.
**Answer skeleton:** Load balancing: each message goes to one consumer — workers share the work. Fan-out: each message goes to all consumers — each subscriber sees every message independently. Kafka implements these via consumer groups: same group = load balance; different groups = fan-out.
→ [[multiple-consumers]]

### Q17. Why is event-time semantics important in a stream pipeline?
**Answer skeleton:** Event time = when the event happened; processing time = when the system saw it. Network delays cause events to arrive out of order or late. Using processing time puts a delayed batch of events in the wrong window, corrupting aggregations. Event time + watermarks correctly assign each event to its logical window.
→ [[event-time-vs-processing-time]]

---

## Distributed ML / Online Learning

### Q18. Describe how SGD can be parallelised with all-reduce.
**Answer skeleton:** Distribute minibatch B across M workers (each gets B' = B/M samples). Each worker computes its partial gradient. All-reduce sums the partial gradients → each worker now holds the full gradient. All workers update their model identically. Statistically equivalent to serial minibatch SGD.
→ [[sgd-all-reduce]]

### Q19. Distinguish covariate shift, prior probability shift, and concept drift.
**Answer skeleton:**
- Covariate: input distribution changes; output given input unchanged. (Face recogniser meets masked faces.)
- Prior: target distribution changes; inputs unchanged. (Flu model during pandemic.)
- Concept drift: the input→output relationship itself changes. (Fraud patterns evolve.)
→ [[data-shifts]]

### Q20. How does ADWIN detect concept drift?
**Answer skeleton:** Maintains a variable-size window. Grows during stable periods (more data → better estimates). Tests whether any sub-window has a statistically different mean. If yes → drift detected, discard older window portion. No fixed window size to tune.
→ [[adwin]]

### Q21. Describe DDM and its warning/change thresholds.
**Answer skeleton:** Tracks error rate pᵢ and std sᵢ at each step. Maintains p_min, s_min (best observed). Warning: pᵢ + sᵢ ≥ p_min + 2×s_min. Change: pᵢ + sᵢ ≥ p_min + 3×s_min. 2σ/3σ mirrors statistical process control.
→ [[ddm-eddm]]

---

## HPC / Parallelism

### Q22. State Amdahl's Law. What does it imply?
**Answer skeleton:** S = 1 / ((1−p) + p/s). The sequential fraction (1−p) bounds the maximum speedup regardless of cores added. With p=0.9, max speedup = 10× even with infinite processors.
→ [[amdahls-law]]

### Q23. What are the four SLURM entities?
**Answer skeleton:** Nodes (individual computers), Partitions (job queues with constraints), Jobs (resource allocations), Job Steps (parallel tasks within a job).
→ [[slurm]]

### Q24. Distinguish SISD, SIMD, MIMD.
**Answer skeleton:** SISD = single instruction, single data (uniprocessor). SIMD = single instruction, multiple data (same instruction on different data streams simultaneously — GPU cores, vector units). MIMD = multiple instructions, multiple data (each processor has its own instruction stream and data — multi-core CPUs, clusters).
→ [[thread-level-parallelism]]

### Q25. Compare OpenMP and MPI.
**Answer skeleton:** OpenMP: shared memory, single node, compiler-directive parallelism, fork-join model — lightweight for multi-core CPUs. MPI: distributed memory, multi-node, explicit two-sided message passing via communicators/ranks — scales to thousands of nodes.
→ [[openmp]], [[mpi]]

---

## Tensors

### Q26. What is a sparse tensor? Describe the CSR format and how to extract a row.
**Answer skeleton:** Sparse = most elements zero. CSR stores: V (non-zero values), COL_INDEX (column of each non-zero), ROW_INDEX (length m+1 marking row boundaries). Row r: slice V[ROW_INDEX[r] : ROW_INDEX[r+1]], column indices from COL_INDEX same slice.
→ [[sparse-tensors]]

---

## Virtualisation

### Q27. Distinguish virtualisation and containerisation.
**Answer skeleton:** Virtualisation: hypervisor creates full VMs each with their own OS kernel. Strong isolation, heavy overhead. Containerisation: OS-level virtualisation, shares host kernel, packages only app+dependencies. Lightweight, fast startup, portable. VMs better for strong isolation; containers better for rapid deployment and scale.
→ [[virtualisation]], [[containerisation]]

---

## Applied System Design & Past Paper Scenarios

### Q28. Describe the difference between hardware and software faults. Why are software faults often more damaging?
**Answer skeleton:** 
- **Hardware faults:** Usually independent, random (e.g., hard drive crash). Often mitigated by redundancy (RAID, multiple nodes).
- **Software faults:** Harder to anticipate, systematically correlated across nodes (e.g., a bug triggered by specific input). Can cause widespread, cascading failures, taking down the entire system despite redundancy.
→ [[fault-vs-failure]], [[reliability]]

### Q29. Explain data locality in the context of document models. What is one advantage and one disadvantage?
**Answer skeleton:** Data locality means that all data for a given object is stored together in a single continuous string (like JSON). 
- **Advantage:** Fast retrieval. Reading the entire document requires only a single database lookup/disk read.
- **Disadvantage:** If a document is large, updating a small field or reading a single field is inefficient because the whole document must be loaded/rewritten.
→ [[document-model]]

### Q30. What are the benefits and drawbacks of combining replication and partitioning?
**Answer skeleton:** 
- **Benefits:** Achieves both scalability (partitioning distributes data and load) and high availability/fault tolerance (replication ensures data survives node failures).
- **Drawbacks:** Increased system complexity. Requires coordinating distributed transactions across partitions and managing consistency across replicas.
→ [[partitioning]], [[replication]]

### Q31. What are the key considerations when deciding between vertical and horizontal scaling?
**Answer skeleton:**
- **Vertical scaling (scale up):** Simpler to maintain, strong consistency, but cost does not scale linearly (expensive at high end) and offers limited fault tolerance (single point of failure).
- **Horizontal scaling (scale out):** Cost-effective (commodity hardware), highly fault-tolerant, but increases complexity (networking, distributed consistency, data partitioning).
→ [[vertical-vs-horizontal-scaling]]

### Q32. How would you design a scalable and reliable data distribution architecture for a global social media platform (e.g., user profiles, posts, followers)?
**Answer skeleton:**
- **Data Model:** Graph database for the user "follows" network (optimised for traversals). Document or Wide-column store for user posts (schema-on-read, high write throughput).
- **Partitioning:** Hash partitioning on User ID for posts to distribute load evenly. 
- **Replication:** Leader-follower replication across multiple geographic data centres to ensure high availability and low latency globally.
- **Consistency:** Eventual consistency for posts and likes (AP system). Users tolerate slight delays in seeing new posts. Strong consistency (linearizability) is too slow for global scale here.
→ [[cap-theorem]], [[graph-model]], [[document-model]]

### Q33. Design a data pipeline for aggregating daily COVID-19 test results from hospitals to a live dashboard and social media.
**Answer skeleton:**
- **Batch vs Stream:** Use stream processing (e.g., Kafka) to ingest test results as they arrive, enabling real-time dashboard updates. A nightly batch job (MapReduce) can process the immutable daily data for official reporting.
- **Social Media Integration:** Use a message broker with a fan-out pattern to push updates to social media APIs. 
- **Why not MPI?** MPI is for tightly coupled, shared/distributed memory HPC clusters, not for loosely coupled, unreliable web API integration.
→ [[online-vs-batch-vs-stream]], [[messaging-systems]], [[mpi]]

### Q34. For a video recommendation system continuously updated by user interactions, should you use full batch, mini-batch, or online learning?
**Answer skeleton:** A combination. 
- **Online learning:** Updates the model incrementally as each interaction arrives. Essential for adapting instantly to trending videos and short-term concept drift.
- **Batch/Mini-batch:** Run periodically (e.g., nightly) over massive historical datasets to learn deep, complex patterns that online learning might miss.
→ [[online-learning]], [[concept-drift]]

### Q35. What is consensus in a leader-follower architecture, and how does it impact the system?
**Answer skeleton:** Consensus is the process of multiple nodes agreeing on a value or state (e.g., agreeing on the leader or the order of writes).
- **Impact:** Ensures strong consistency and prevents split-brain. However, it requires synchronous communication (e.g., a quorum), which reduces performance (higher latency) and can impact availability during network partitions.
→ [[consensus]], [[leader-follower-replication]]
